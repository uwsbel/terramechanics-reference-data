"""Arithmetic check of the printed derived columns of a subscale drag table (AM-68-1 Vol. I, Figs. 4-6a to 4-16).

    python tools/check_drag_table.py <table.csv> [--out report.md] [--csv checks.csv] [--json summary.json]

The tables print, for each run, the inputs (D, d, V_H, the mean DPT reading, Dr, gamma), the measured loads (F_D, F_V)
and angle, and four derived columns: F_D / (d gamma A_ft), V_H / sqrt(d g), F_D / A_ft and F_V / A_pt. The areas are
defined on Figure 4-4 only by name (A_ft the total horizontal frontal area, A_pt the vertical frontal area, both drawn
at a pitched attitude), not by a formula, so the check uses what the printed numbers fix without them:

1. V_H / sqrt(d g), recomputed with d in feet and g = 32.174 ft/s^2 (standard gravity), against the printed value;
2. the two pressure columns against each other: (F_D / A_ft) / (F_D / (d gamma A_ft)) = d gamma, with F_D / A_ft in
   psi (inferred: no unit is printed), d in inches and gamma in lb/in^3 (pcf / 1728). Each row admits an interval of
   factors k with printed F_D/A_ft = k x F_D/(d gamma A_ft) x d gamma / 1728 inside the printed rounding of the three
   printed numbers; the intervals of all rows are intersected at full precision. A non-empty intersection is a
   common factor every row fits (reported as the effective unit weight k x gamma); a row outside it is named;
3. the areas each row implies, A_ft = F_D / (F_D / A_ft) and A_pt = F_V / (F_V / A_pt), in square inches, as
   heuristic flags only: rows of one pad diameter D are compared, A_ft also within one depth (three rows or more),
   and a row is named when its whole interval lies more than 15 percent from the median of its group. The areas also
   depend on the pad's pitch (Fig. 4-4), which the check does not model, so a flag is a place to look, not an error.

Conventions: a printed number carries half a unit of its last printed digit; the depths d and diameters D are nominal
set points of the rig (Fig. 4-2 lists the planned depths) and are taken as exact, fractions such as "1 1/2" included.
A cell with `?` (an unreadable digit) or a zero divisor is skipped and listed. The check shows the printed columns
consistent with each other or not; it does not show a transcription right (two readings must agree cell by cell,
tools/diff_tables.py).
"""
import argparse
import csv
import json
import math
import statistics
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

G_FT = 9.80665 / 0.3048   # standard gravity in ft/s^2


def num(s, exact=False):
    """A printed number and half a unit of its last printed digit (0 when `exact`, and for fractions)."""
    s = (s or "").strip()
    if not s or "?" in s:
        return None, None
    try:
        if "/" in s:
            return float(sum(Fraction(p) for p in s.split())), 0.0
        v = float(s)
    except ValueError:
        return None, None
    dec = len(s.split(".")[1]) if "." in s else 0
    return v, (0.0 if exact else 0.5 * 10 ** (-dec))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("table")
    ap.add_argument("--out")
    ap.add_argument("--csv")
    ap.add_argument("--json", help="a summary for the record (tools/build_run_table.py) and the site")
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.table, encoding="utf-8-sig", newline="")))
    checks, skipped, ivals = [], [], []
    groups = defaultdict(list)   # (area, D, d or None) -> [(run, low, high)]
    for r in rows:
        run = r["run_number"]
        D, _ = num(r["D_in"], exact=True)
        d, _ = num(r["d_in"], exact=True)
        vh, bvh = num(r["VH_fps"])
        g, bg = num(r["gamma_pcf"])
        fd, bfd = num(r["FD_lb"])
        fv, bfv = num(r["FV_lb"])
        c10, b10 = num(r["FD_over_d_gamma_Aft"])
        c11, b11 = num(r["VH_over_sqrt_dg"])
        c12, b12 = num(r["FD_over_Aft"])
        c13, b13 = num(r["FV_over_Apt"])
        # 1. V_H / sqrt(d g): the computed interval against the printed one
        if None in (d, vh, c11) or not d:
            skipped.append(f"{run}: V_H/sqrt(dg) (a missing or zero input)")
        else:
            s = math.sqrt(d / 12.0 * G_FT)
            lo, hi = (vh - bvh) / s, (vh + bvh) / s
            ok = hi >= c11 - b11 and lo <= c11 + b11
            checks.append([run, "VH/sqrt(dg)", f"{vh / s:.4f}", r["VH_over_sqrt_dg"], f"{b11 + bvh / s:.4f}", "ok" if ok else "off"])
        # 2. the factor interval of this row
        if None in (d, g, c10, c12) or not (d and g and c10):
            skipped.append(f"{run}: F_D/A_ft against F_D/(d gamma A_ft) (a missing or zero input)")
        else:
            comp = lambda c, gg: c * d * gg / 1728.0
            klo = (c12 - b12) / comp(c10 + b10, g + bg)
            khi = (c12 + b12) / comp(max(c10 - b10, 1e-12), max(g - bg, 1e-12))
            ivals.append((run, klo, khi, comp(c10, g), c12))
        # 3. implied areas, grouped by pad diameter (and depth for A_ft)
        if None not in (fd, c12) and c12 and fd:
            groups[("A_ft", D, d)].append((run, (fd - bfd) / (c12 + b12), (fd + bfd) / max(c12 - b12, 1e-12)))
        if None not in (fv, c13) and c13 and fv:
            groups[("A_pt", D, None)].append((run, (fv - bfv) / (c13 + b13), (fv + bfv) / max(c13 - b13, 1e-12)))
    # the common factor: the intersection of every row's interval, at full precision
    summary = {"table": a.table, "runs": len(rows), "skipped": skipped}
    if ivals:
        lo, hi = max(x[1] for x in ivals), min(x[2] for x in ivals)
        common = lo <= hi
        mid = (lo + hi) / 2 if common else statistics.median((x[1] + x[2]) / 2 for x in ivals)
        for run, klo, khi, comp, printed in ivals:
            ok = klo <= mid <= khi
            checks.append([run, "FD/Aft against FD/(d gamma Aft) x d gamma", f"{comp:.4f}", f"{printed}", f"{klo:.5f} to {khi:.5f}",
                           "fits the common factor" if ok else "off"])
        g0 = statistics.median(num(r["gamma_pcf"])[0] for r in rows if num(r["gamma_pcf"])[0] is not None)
        summary["factor"] = {"common": common, "low": lo if common else None, "high": hi if common else None, "used": mid,
                             "raw_range": [min(x[4] / x[3] for x in ivals), max(x[4] / x[3] for x in ivals)],
                             "effective_gamma_pcf": [g0 * lo, g0 * hi] if common else None, "printed_gamma_pcf": g0,
                             "rows_off": [c[0] for c in checks if c[1].startswith("FD/Aft") and c[-1] == "off"]}
    # area flags
    area_rows = []
    for (name, D, d), vals in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][1] or 0, kv[0][2] or 0)):
        if name == "A_ft" and len(vals) < 3:
            for run, l, h in vals:
                checks.append([run, f"implied {name} (D {D:g}, d {d:g} in)", f"{(l + h) / 2:.3f}", "", f"{(h - l) / 2:.3f}", "too few rows to compare"])
            continue
        med = statistics.median((l + h) / 2 for _, l, h in vals)
        far = [run for run, l, h in vals if h < 0.85 * med or l > 1.15 * med]
        label = f"implied {name} (D {D:g}" + (f", d {d:g} in)" if d is not None else ", all depths)")
        area_rows.append((label, len(vals), med, min((l + h) / 2 for _, l, h in vals), max((l + h) / 2 for _, l, h in vals), far))
        for run, l, h in vals:
            checks.append([run, label, f"{(l + h) / 2:.3f}", "", f"{(h - l) / 2:.3f}", "flag" if run in far else "ok"])
    summary["flags"] = sorted({c[0] for c in checks if c[-1] in ("off", "flag")}, key=lambda s: [int(x) for x in s.split("-")])
    # report
    off = [c for c in checks if c[-1] in ("off",)]
    out = ["# Arithmetic check of the derived columns", "", f"Table: `{a.table}`; {len(rows)} runs.", ""]
    if ivals:
        f = summary["factor"]
        out.append(f"F_D/A_ft against F_D/(d gamma A_ft) x d gamma (psi, inferred): printed over computed ranges from "
                   f"{f['raw_range'][0]:.4f} to {f['raw_range'][1]:.4f}. " +
                   (f"Every row admits a common factor of {f['low']:.5f} to {f['high']:.5f} within the printed rounding (the "
                    f"rows' intervals intersect): the printed columns are consistent with each other if the derived column "
                    f"used a unit weight of {f['effective_gamma_pcf'][0]:.3f} to {f['effective_gamma_pcf'][1]:.3f} pcf instead of "
                    f"the printed {f['printed_gamma_pcf']:g}. Which input differs, the page does not say."
                    if f["common"] else
                    f"No single factor fits every row; with the median {f['used']:.5f}, the rows named below stay outside."))
        out.append("")
    out += ["Rows outside the printed rounding:", "", "| run | check | computed | printed | tolerance or factor interval | verdict |",
            "|---|---|---|---|---|---|"]
    out += [f"| {' | '.join(c)} |" for c in off] or ["| | (none) | | | | |"]
    out += ["", "## Areas implied by each row (square inches), heuristic flags", "",
            "Grouped by pad diameter, and by depth for A_ft (three rows or more). A row is flagged when its whole interval lies "
            "more than 15 percent from its group's median. The areas also depend on the pad's pitch, which is not modeled: a "
            "flag is a place to look, not an error.", "",
            "| group | rows | median | min | max | flagged |", "|---|---|---|---|---|---|"]
    out += [f"| {lab} | {n} | {m:.2f} | {mn:.2f} | {mx:.2f} | {', '.join(fr) or 'none'} |" for lab, n, m, mn, mx, fr in area_rows]
    if skipped:
        out += ["", "Skipped: " + "; ".join(skipped)]
    text = "\n".join(out) + "\n"
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    if a.csv:
        with open(a.csv, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(["run_number", "check", "computed", "printed", "tolerance", "verdict"])
            w.writerows(checks)
    if a.json:
        Path(a.json).write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
