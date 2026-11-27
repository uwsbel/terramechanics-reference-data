"""Reconcile the two readings of every figure and panel of a curve batch (docs/CURVE-READING.md, section 4).

Usage:
    python tools/reconcile_curves.py <batch> [--maps affine] [--bound-scale 0.5]

Reads qa/<batch>/overlays.csv: figure_id, panel, image, box, points_a, points_b, name, and optionally
cal_a, cal_b (a reading's calibration directory when it is not cal-p<panel> next to its points file:
the pilot's cal-fc1b-p1, Claude's tick map of FC-3A) and canonical, canonical_reason (to name the
canonical reading instead of the rule of tools/diff_curves.py), and feature_roles (`leading`: how
tools/diff_curves.py pairs the features of a history with several peaks, minima and knees per series,
from batch curves-s4-b1; empty keeps the earlier rule), and max_gap (a trace step wider than this, in x, is a
drawn gap; for a history sampled at several spacings by rule, from batch curves-s2-b4; empty keeps three times the
reading's median spacing), and end_dedup (`yes`: the other reading's sample at a trace's canonical end is not
appended when it is the same point within both readings' bounds; from batch curves-s2-b4). points_a is Claude's points file,
points_b Codex's; only their pixels and pixel bounds are used.

Maps (D-025, the default): each reading is re-derived from its own pixels with the piecewise map of its
own calibration (tools/calibrate_axes.py, every line checked against the ink of the page), plus any
line recovered for it in qa/<batch>/knots.csv (figure_id, panel, reader, x_value, y_value, u, v,
x_source, y_source, note: a line the reader left out whose value the page supports, such as the left
frame at x = 0 on FC-6B and FC-6D). Written under qa/<batch>/rederived/<reader>/<figure>/:
cal-p<panel>/ (calibration.json as submitted, anchors.csv with the recovered lines, knots.json: the
lines used, their location errors and ink distances) and points-p<panel>-native.csv, with the role words
of qa/<batch>/feature-roles.csv applied (figure_id, panel, reader, series_id, sequence, submitted_role, role,
reason: a feature named by another convention than the batch's, from curves-s5-b1). The submissions
under extractions/ are never touched. With --maps affine the points files are used as submitted.

Then, per figure and panel, tools/diff_curves.py runs with qa/<batch>/decisions-<figure>-p<panel>.csv
when present, writing diff-<figure>-p<panel>.md and canonical-<figure>-p<panel>.csv; then
qa/<batch>/canonical.csv, all figures and panels in one file, with the series renames of
qa/<batch>/series-ids.csv applied (figure_id, submitted, series_id, note: a series id the evidence
packets gave wrongly; the submissions keep the id they were given, and decisions name points by it);
and, with piecewise maps, qa/<batch>/calibration-sensitivity.md: per canonical series, the largest
difference between the piecewise values and the affine ones from the same pixels, and the change of
the initial and overall secant slopes (D-025: a correlated calibration sensitivity, reported, not
added to the bounds). Prints one line per figure and panel.

The trace samples that qa/<batch>/ink-checks.csv (tools/check_trace_ink.py, D-031) shows off their line's own ink
are excluded from both readings before the comparison, as a hand exclusion would be (D-032, 2026-10-30); the diff
report lists every hand decision the check overrides. --no-ink-checks turns this off.

With --bound-scale the comparison is rerun with every bound scaled (sensitivity check) and only the
reports sens-<figure>-p<panel>.md are written.
"""
import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import calibrate_axes  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
READERS = (("claude", "points_a", "cal_a"), ("codex", "points_b", "cal_b"))
INITIAL_FRACTION = 0.1   # the initial secant: from the first trace sample over this share of the trace's x extent


def load(p):
    with Path(p).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, cols):
    with Path(path).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


ROLE_WORDS = ("knee, minimum", "knee", "peak", "first", "last")   # the roles a feature-roles.csv row may name


def submitted_role(note):
    """The role a feature note opens with, as one of ROLE_WORDS (longest first, whole words), or None."""
    m = re.match(r"\s*(knee, minimum|knee|peak|first|last)(?=[\s:;,(]|$)", note or "")   # "peakT", "first2" are not roles
    return m.group(1) if m else None


def renamed_note(role, note):
    """The rederived note of a renamed feature: the batch's role first (tools/diff_curves.py reads it there), then the
    submitted note verbatim."""
    return f"{role} (role renamed by qa/<batch>/feature-roles.csv; submitted note: {note})"


def check_roles(q, roles, overlays):
    """Validate qa/<batch>/feature-roles.csv against the submissions before anything is written: known figure, panel and
    reader; recognized role words; one row per feature; the submitted note opens with exactly the submitted role."""
    need = {"figure_id", "panel", "reader", "series_id", "sequence", "submitted_role", "role", "reason"}
    if roles and not need <= set(roles[0]):
        sys.exit(f"feature-roles.csv: columns {sorted(need - set(roles[0]))} missing")
    ovs = {(ov["figure_id"], ov["panel"]): ov for ov in overlays}
    seen = set()
    for fr in roles:
        k = (fr["figure_id"], fr["panel"], fr["reader"], fr["series_id"], fr["sequence"])
        where = f"feature-roles.csv: {' '.join(k)}"
        if k in seen:
            sys.exit(f"{where}: named twice")
        seen.add(k)
        if (fr["figure_id"], fr["panel"]) not in ovs:
            sys.exit(f"{where}: no such figure and panel in overlays.csv")
        col = {lab: pc for lab, pc, _ in READERS}.get(fr["reader"])
        if not col:
            sys.exit(f"{where}: reader must be one of {[lab for lab, _, _ in READERS]}")
        if fr["role"] not in ROLE_WORDS or fr["submitted_role"] not in ROLE_WORDS or fr["role"] == fr["submitted_role"]:
            sys.exit(f"{where}: role and submitted_role must be two different words of {ROLE_WORDS}")
        hit = [r for r in load(ROOT / ovs[(fr["figure_id"], fr["panel"])][col]) if r["panel"] == fr["panel"] and
               r["point_kind"] == "feature" and r["series_id"] == fr["series_id"] and r["sequence"] == fr["sequence"]]
        if len(hit) != 1:
            sys.exit(f"{where}: {len(hit)} features in the submission, one expected")
        if submitted_role(hit[0]["note"]) != fr["submitted_role"]:
            sys.exit(f"{where}: the submitted note opens with {submitted_role(hit[0]['note'])!r}, not {fr['submitted_role']!r}")


def rederive(q, ov, label, pts, cal_dir, knots, roles=()):
    """A reading's values from its pixels on its piecewise map; returns (points file, calibration file)."""
    fid, p = ov["figure_id"], ov["panel"]
    out = q / "rederived" / label / fid
    cal_out = out / f"cal-p{p}"
    cal_out.mkdir(parents=True, exist_ok=True)
    shutil.copy2(cal_dir / "calibration.json", cal_out / "calibration.json")
    anchors = calibrate_axes.load_anchors(cal_dir)
    added = [k for k in knots if (k["figure_id"], k["panel"], k["reader"]) == (fid, p, label)]
    # a recovered line replaces the reader's own anchors of that value (a misplaced line, rejected by the
    # ink check, would otherwise be fitted together with the measured one); an anchor keeps its other axis
    for ax in ("x", "y"):
        vals = {float(k[f"{ax}_value"]) for k in added if k.get(f"{ax}_value")}
        for an in anchors:
            if str(an.get(f"{ax}_value", "")).strip() and float(an[f"{ax}_value"]) in vals:
                an[f"{ax}_value"], an[f"{ax}_source"] = "", "replaced by a recovered line (qa/<batch>/knots.csv)"
    anchors += [{c: k.get(c, "") for c in ("x_value", "y_value", "u", "v", "x_source", "y_source")} for k in added]
    cols = list(dict.fromkeys(c for a in anchors for c in a))
    write_csv(cal_out / "anchors.csv", anchors, cols)
    image = ROOT / ov["image"]
    cal, X, Y = calibrate_axes.piecewise_maps(cal_out, image)
    summary = calibrate_axes.knots_summary(X, Y)
    summary.update({"model": "piecewise between verified lines (D-025)", "submitted_calibration": cal_dir.relative_to(ROOT).as_posix(),
                    "recovered_lines": added, "image": ov["image"]})
    (cal_out / "knots.json").write_text(json.dumps(summary, indent=1), encoding="utf-8", newline="\n")
    rd = load(pts)
    rows = [r for r in rd if r["panel"] == p]
    # a feature's role word is a naming convention, not a measurement: qa/<batch>/feature-roles.csv renames it where a
    # reader followed another convention than the batch's (from curves-s5-b1: peaks and minima of a compression panel
    # named by the curve as drawn instead of the signed value), so that the two readings' features pair by role. The
    # rows were validated against the submissions in main(); the submitted note is kept verbatim behind the new role.
    for fr in roles:
        if (fr["figure_id"], fr["panel"], fr["reader"]) != (fid, p, label):
            continue
        r, = [r for r in rows if r["point_kind"] == "feature" and r["series_id"] == fr["series_id"] and r["sequence"] == fr["sequence"]]
        r["note"] = renamed_note(fr["role"], r["note"])
    calibrate_axes.piecewise_rows(cal, X, Y, rows)
    cols = list(rd[0].keys()) + [c for c in ("x_native", "y_native", "x_read_bound", "y_read_bound", "cal_model") if c not in rd[0]]
    out_pts = out / f"points-p{p}-native.csv"
    write_csv(out_pts, rows, cols)
    return out_pts, cal_out / "calibration.json"


def secant_index(rows, frac):
    """The sample a secant from the first trace sample ends at: the first beyond `frac` of the trace's x extent."""
    xs = [r[0] for r in rows]
    if len(rows) < 2 or max(xs) == min(xs):
        return None
    x0 = rows[0][0]
    target = x0 + frac * (max(xs) - min(xs)) * (1 if rows[-1][0] >= x0 else -1)
    for j, (x, _) in enumerate(rows[1:], 1):
        if abs(x - x0) >= abs(target - x0) and x != x0:
            return j
    return len(rows) - 1


def secant(rows, j):
    """Slope from the first sample to sample j. The piecewise and affine secants of a series end at the same
    sample, chosen on the piecewise values (Codex, 2026-10-14: chosen separately they could span different
    parts of the curve)."""
    if j is None:
        return None
    (x0, y0), (x, y) = rows[0], rows[j]
    return (y - y0) / (x - x0) if x != x0 else None


def sensitivity(q, canon, cal_files):
    """calibration-sensitivity.md: piecewise against affine values from the same pixels."""
    by = defaultdict(list)
    for r in canon:
        by[(r["figure_id"], r["panel"], r["series_id"])].append(r)
    lines = ["# Calibration sensitivity: piecewise against affine maps", "",
             "Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the "
             "affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the "
             f"initial secant slope (first sample to the first sample beyond {INITIAL_FRACTION:.0%} of the trace's x extent) and "
             "of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration "
             "sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.", "",
             "| figure | panel | series | points | max dx | max dy | initial secant | overall secant |", "|---|---|---|---|---|---|---|---|"]
    for (fid, p, sid), rows in sorted(by.items()):
        dx = dy = 0.0
        pw, af = [], []
        for r in rows:
            cal = cal_files[(fid, p, r["source"].removesuffix("-interp"))]   # an interpolated value: that reader's map
            u, v = float(r["pixel_u"]), float(r["pixel_v"])
            tx, ty = calibrate_axes.axis_transforms(cal)   # the affine map is in the plotting coordinates (D-027)
            xa = calibrate_axes.TRANSFORMS[tx][1](cal["ax"][0] * u + cal["ax"][1] * v + cal["ax"][2])
            ya = calibrate_axes.TRANSFORMS[ty][1](cal["ay"][0] * u + cal["ay"][1] * v + cal["ay"][2])
            x, y = float(r["x_native"]), float(r["y_native"])
            dx, dy = max(dx, abs(x - xa)), max(dy, abs(y - ya))
            if r["point_kind"] == "trace":
                pw.append((x, y))
                af.append((xa, ya))
        cells = []
        for frac in (INITIAL_FRACTION, 1.0):
            j = secant_index(pw, frac) if len(pw) >= 2 else None
            sp, sa = secant(pw, j), secant(af, j)
            cells.append(f"{100 * (sp / sa - 1):+.1f}%" if sp is not None and sa not in (None, 0) else "")
        lines.append(f"| {fid} | {p} | {sid} | {len(rows)} | {dx:.4g} | {dy:.4g} | {cells[0]} | {cells[1]} |")
    (q / "calibration-sensitivity.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch")
    ap.add_argument("--maps", choices=["piecewise", "affine"], default="piecewise")
    ap.add_argument("--bound-scale")
    ap.add_argument("--ink-checks", action=argparse.BooleanOptionalAction, default=True,
                    help="exclude the trace samples qa/<batch>/ink-checks.csv shows off their line (D-031 v1, applied 2026-10-30, D-032; "
                         "--no-ink-checks reproduces the readings before it)")
    a = ap.parse_args()
    q = ROOT / "qa" / a.batch
    renames = {(r["figure_id"], r["submitted"]): r["series_id"] for r in load(q / "series-ids.csv")} if (q / "series-ids.csv").exists() else {}
    knots = load(q / "knots.csv") if (q / "knots.csv").exists() else []
    breaks = load(q / "breaks.csv") if (q / "breaks.csv").exists() else []
    roles = load(q / "feature-roles.csv") if (q / "feature-roles.csv").exists() else []
    if roles and a.maps != "piecewise":
        sys.exit("qa/<batch>/feature-roles.csv is applied to the rederived readings: use --maps piecewise")
    check_roles(q, roles, load(q / "overlays.csv"))   # before the rederived readings are removed and rewritten
    if a.bound_scale and a.maps == "piecewise":
        # the sensitivity rerun reuses the rederived readings: their renamed notes must be exactly the current set
        # (a rename added, removed or changed since they were written stops the run)
        want = {(fr["figure_id"], fr["panel"], fr["reader"], fr["series_id"], fr["sequence"]): fr["role"] for fr in roles}
        for ov in load(q / "overlays.csv"):
            for label, pcol, _ in READERS:
                sub = {(r["series_id"], r["sequence"]): r["note"] for r in load(ROOT / ov[pcol])
                       if r["panel"] == ov["panel"] and r["point_kind"] == "feature"}
                cached = [r for r in load(q / "rederived" / label / ov["figure_id"] / f"points-p{ov['panel']}-native.csv")
                          if r["point_kind"] == "feature"]
                if {(r["series_id"], r["sequence"]) for r in cached} != set(sub):
                    sys.exit(f"qa/{a.batch}/rederived/ is stale for {ov['figure_id']} panel {ov['panel']} {label} "
                             f"(its features differ from the submission's): rerun without --bound-scale first")
                for r in cached:
                    k = (ov["figure_id"], ov["panel"], label, r["series_id"], r["sequence"])
                    expect = renamed_note(want[k], sub[k[3:]]) if k in want else sub[k[3:]]
                    if r["note"] != expect:
                        sys.exit(f"qa/{a.batch}/rederived/ is stale for {' '.join(k)} (feature-roles.csv changed since it "
                                 f"was written): rerun without --bound-scale first")
    if a.maps == "piecewise" and not a.bound_scale and (q / "rederived").exists():
        shutil.rmtree(q / "rederived")   # regenerated from the submissions every run
    merged, header, cal_files = [], None, {}
    print(f"{'figure':<8}{'panel':>5}  {'canonical':<10}{'matched':>8}{'agreed':>8}{'disagreed':>10}{'unmatched':>10}  statuses")
    for ov in load(q / "overlays.csv"):
        fid, p = ov["figure_id"], ov["panel"]
        files = {}
        for label, pcol, ccol in READERS:
            pts = ROOT / ov[pcol]
            cal_dir = ROOT / ov[ccol] if ov.get(ccol) else pts.parent / f"cal-p{p}"
            cal_files[(fid, p, label)] = json.loads((cal_dir / "calibration.json").read_text(encoding="utf-8"))
            if a.maps == "piecewise":
                files[label] = rederive(q, ov, label, pts, cal_dir, knots, roles) if not a.bound_scale else (
                    q / "rederived" / label / fid / f"points-p{p}-native.csv", q / "rederived" / label / fid / f"cal-p{p}" / "calibration.json")
            else:
                files[label] = (pts, cal_dir / "calibration.json")
        (pa, ca), (pb, cb) = files["claude"], files["codex"]
        cmd = [sys.executable, str(ROOT / "tools" / "diff_curves.py"), str(pa), str(pb), "--cal-a", str(ca), "--cal-b", str(cb),
               "--labels", "claude,codex", "--panel", p]
        if a.maps == "piecewise":
            cmd += ["--maps", "piecewise", "--image", str(ROOT / ov["image"])]
        if ov.get("canonical"):   # optional overlays.csv columns: canonical (claude|codex), canonical_reason
            cmd += ["--canonical-from", ov["canonical"], "--canonical-reason", ov.get("canonical_reason", "")]
        if ov.get("feature_roles"):   # optional overlays.csv column: leading, for histories with several peaks and knees
            cmd += ["--feature-roles", ov["feature_roles"]]
        if ov.get("max_gap"):   # optional overlays.csv column: the panel's drawn-gap threshold in x (a history sampled by rule)
            cmd += ["--max-gap", ov["max_gap"]]
        if ov.get("end_dedup") == "yes":   # optional overlays.csv column: no duplicate of a trace's canonical end
            cmd += ["--end-dedup"]
        # a documented break in a drawn line (qa/<batch>/breaks.csv, also read by tools/build_observations.py) is not
        # interpolated across. Its span: the two ends of the gap measured on the page (optional gap_u1, gap_v1,
        # gap_u2, gap_v2, from curves-s5-b1), mapped on each reading's own calibration (Codex's review: one span in x
        # misplaces the gap on the other reading's map); else from the sample before it to the sample after it in the
        # reading named, the same x for both readings
        for br in breaks:
            if (br["figure_id"], br["panel"]) != (fid, p):
                continue
            if all(br.get(c) for c in ("gap_u1", "gap_v1", "gap_u2", "gap_v2")):
                if a.maps != "piecewise":
                    sys.exit("breaks.csv: a break given by its pixels needs --maps piecewise")
                for label, flag in (("claude", "--break-a"), ("codex", "--break-b")):
                    _, X, _ = calibrate_axes.piecewise_maps(files[label][1].parent, ROOT / ov["image"])
                    xs = sorted(X.value(float(br[f"gap_u{e}"]), float(br[f"gap_v{e}"]))[0] for e in (1, 2))
                    cmd += [flag, br["series_id"], repr(xs[0]), repr(xs[1])]
                continue
            xs = []
            for end in (br["after"], br["before"]):
                reader, seq = end.split("|")
                hit = [r for r in load(files[reader][0]) if r["point_kind"] == "trace" and r["series_id"] == br["series_id"]
                       and r["sequence"] == seq]
                if len(hit) != 1:
                    sys.exit(f"breaks.csv: {fid} panel {p} {br['series_id']} {end}: no such trace sample")
                xs.append(hit[0]["x_native"])
            cmd += ["--break", br["series_id"], *xs]
        if a.bound_scale:
            out = q / f"sens-{fid}-p{p}.md"
            cmd += ["--bound-scale", a.bound_scale, "--out", str(out)]
        else:
            out = q / f"diff-{fid}-p{p}.md"
            canon = q / f"canonical-{fid}-p{p}.csv"
            cmd += ["--out", str(out), "--canonical", str(canon)]
            if (q / f"decisions-{fid}-p{p}.csv").exists():
                cmd += ["--decisions", str(q / f"decisions-{fid}-p{p}.csv")]
            if a.ink_checks and (q / "ink-checks.csv").exists():
                cmd += ["--ink-checks", str(q / "ink-checks.csv")]
        # a panel's earlier report and canonical file go first, so that a comparison that stops on an input error
        # (exit status 2) can never leave them in place to be read as this run's (Codex's review, 2026-11-19)
        out.unlink(missing_ok=True)
        if not a.bound_scale:
            canon.unlink(missing_ok=True)
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        # diff_curves exits 1 when it finds disagreements, and so does a Python traceback: tell them apart
        if r.returncode not in (0, 1) or "Traceback" in r.stderr or not out.exists() or (not a.bound_scale and not canon.exists()):
            sys.exit(f"{fid} panel {p}: tools/diff_curves.py failed\n{r.stderr}")
        rep = out.read_text(encoding="utf-8")
        m = re.search(r"Matched: (\d+); agreed (\d+); disagreed (\d+); unmatched (\d+)", rep)
        c = re.search(r"Canonical reading: (\w+)", rep).group(1)
        st = ""
        if not a.bound_scale:
            rows = load(canon)
            for row in rows:
                row["series_id"] = renames.get((fid, row["series_id"]), row["series_id"])
            header = header or list(rows[0].keys())
            merged += rows
            st = ", ".join(f"{k} {v}" for k, v in sorted(Counter(r["status"] for r in rows).items()))
        print(f"{fid:<8}{p:>5}  {c:<10}{m.group(1):>8}{m.group(2):>8}{m.group(3):>10}{m.group(4):>10}  {st}")
    if not a.bound_scale:
        write_csv(q / "canonical.csv", merged, header)
        print(f"{q / 'canonical.csv'}: {len(merged)} points, " + ", ".join(f"{k} {v}" for k, v in sorted(Counter(r['status'] for r in merged).items())))
        if a.maps == "piecewise":
            sensitivity(q, merged, cal_files)
    return 0


if __name__ == "__main__":
    sys.exit(main())
