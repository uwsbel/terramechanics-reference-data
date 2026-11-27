"""Write the record of a printed table of runs (kind `run-table`, D-050 roadmap step 6b): data/experiments/<id>/runs.csv
and runs.json, from the cells two readings agreed on (qa/<batch>/agreed.csv, tools/diff_tables.py).

    python tools/build_run_table.py <batch> --experiment b68-drag-f4-6a --figure F4-6a [--out data/experiments]
    python tools/build_run_table.py tables-s5-b1 --family mdrop --soil-family RS --experiment b68-mdrop-t5-3-rs --figure T5-3

Each row of the printed table is one physical test (a run); the record keeps every printed value exactly as printed
(fractions such as "1 1/2" as printed) and its SI value converted once with the factors of tools/to_si.py, never from
another SI value. A cell the readings did not agree on would be empty in agreed.csv and is written empty with status
`pending-review`; every value comes from both readings or from neither.

Each family of printed tables has its own column map (`FAMILIES`):

- `drag`, the subscale drag tables (Figs. 4-6a to 4-16). The four derived columns the report prints (F_D/(d gamma
  A_ft), V_H/sqrt(dg), F_D/A_ft, F_V/A_pt) are kept as printed, the dimensionless ones without conversion and the two
  pressures in Pa, for the arithmetic check of qa/<batch>/arithmetic.md (tools/check_drag_table.py), whose per-row
  verdicts are carried in `check`.
- `mdrop`, Table 5-T3 (the detail correlation drops of the 1/6-scale LM model, from 2026-11-20): one row per drop,
  `run_number` the printed NASA Test No. and `bendix_drop_no` the Bendix drop number, the bed's soil as printed, and
  `same_test_as`, the index record that holds the same drop's time histories (a `single` mdrop row whose printed label
  is that NASA Test No.), so that no drop is counted twice. `--soil-family` keeps the rows whose printed Soil begins
  with that family: the table mixes RS and SS beds, and the index holds one record per soil family.

Human audits (qa/audits.csv, tools/ingest_review.py; D-050, from 2026-11-21): the student reviewers check a sample of a
table's cells (object `<figure>/1/<printed column>/cell/agreed/<row key>`). Each run gets `audit`, its audited cells in
printed order as `<printed column> <pair outcome> by <reviewer> (<chunk>), ...`, the pair outcome as for a curve point
(`confirmed` when every reviewer of the cell answered ok, two of them for a second review; `single (ok)` while one has;
`split`, `flagged`, `cannot-tell`, or a mix such as `ok + cannot tell`); a run's `status` stays as the readings left it, since a sample checks a few of its
cells. runs.json `audit` counts the record's cells, the cells sampled and the cells two reviewers confirmed.
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from to_si import FACTORS  # noqa: E402
from ingest_review import pair_outcome  # noqa: E402  (one definition of a pair outcome, shared with the ingest)

ROOT = Path(__file__).resolve().parents[1]

# printed column -> (quantity, native unit, SI unit, SI column, native column); SI unit None: kept as printed
DRAG = [
    ("D_in", "footpad diameter D", "in", "m", "D_m"),
    ("d_in", "footpad depth d: from the soil surface to the bottom of the pad at zero pitch (Fig. 4-4), a nominal set point "
             "held by locking the loading piston (printed 3-13, PDF 154); the pad's ball pivot may have been free or clamped, "
             "which is not stated per run (Fig. 3-10)", "in", "m", "d_m"),
    ("VH_fps", "horizontal velocity V_H", "ft_s", "m_s", "VH_m_s"),
    ("gp_bar", "mean dynamic penetrometer peak deceleration of the bed, g_p bar", "g", "m_s2", "gp_bar_m_s2"),
    ("Dr", "relative density D_r", "none", "none", "Dr"),
    ("gamma_pcf", "unit weight gamma", "pcf", "N_m3", "unit_weight_N_m3"),
    ("FD_lb", "drag load F_D", "lbf", "N", "FD_N"),
    ("FV_lb", "vertical load F_V", "lbf", "N", "FV_N"),
    ("alpha_deg", "footpad pitch angle alpha", "deg", "deg", "alpha_deg"),
    ("FD_over_d_gamma_Aft", "F_D / (d gamma A_ft), as printed (dimensionless)", "none", "none", "FD_over_d_gamma_Aft"),
    ("VH_over_sqrt_dg", "V_H / sqrt(d g), as printed (dimensionless)", "none", "none", "VH_over_sqrt_dg"),
    ("FD_over_Aft", "F_D / A_ft, as printed (psi)", "psi", "Pa", "FD_over_Aft_Pa"),
    ("FV_over_Apt", "F_V / A_pt, as printed (psi)", "psi", "Pa", "FV_over_Apt_Pa"),
]
MDROP = [
    ("VV_in_s", "vertical velocity V_v at touchdown, sign as printed", "in_s", "m_s", "VV_m_s"),
    ("Vh_in_s", "horizontal velocity V_h at touchdown", "in_s", "m_s", "Vh_m_s"),
    ("tau_s", "time interval tau between model release and touchdown", "s", "s", "tau_s"),
    ("Dr", "relative density D_r of the bed", "none", "none", "Dr"),
    ("gamma_pcf", "soil density gamma of the bed, printed in Lb./Ft.^3 (a unit weight)", "pcf", "N_m3", "unit_weight_N_m3"),
    ("phi_deg", "internal angle of friction phi of the bed", "deg", "deg", "phi_deg"),
]
EXTRA_SI = [("gamma_pcf", "pcf", "kg_m3", "bulk_density_kg_m3")]   # the mass density as well (under standard gravity)

FAMILIES = {
    "drag": {"ids": [("run_number", "run_number")], "text": [], "cols": DRAG, "link": None,
             "precision": ("each value carries the precision of its printing (half a unit of its last printed digit), except "
                           "the diameters D and depths d, nominal set points of the rig, taken as exact; no reading bound "
                           "applies to a transcribed number. The units of F_D/A_ft and F_V/A_pt are not printed; psi is "
                           "inferred from their magnitudes and the other columns. Printed values are in the columns named by "
                           "their printed unit (D_in, FD_lb, ...); a column kept as printed (Dr, alpha_deg, the dimensionless "
                           "derived columns) is not repeated")},
    "mdrop": {"ids": [("nasa_test_no", "run_number"), ("bendix_drop_no", "bendix_drop_no")],
              "text": [("soil", "soil_printed")], "cols": MDROP, "link": "same_test_as",
              # what both readings of batch tables-s5-b1 quote from the legend and the text (qa/tables-s5-b1/review.md)
              "definitions": (
                  "The table's legend: V_v is the vertical velocity, V_h the horizontal velocity, tau the time interval between "
                  "model release and touchdown, D_r the soil relative density, gamma the soil density (printed in Lb./Ft.^3, a "
                  "unit weight) and phi the internal angle of friction (Table 5-T3, printed 5-45, PDF 325). The velocities \"were "
                  "calculated based on the exact time interval between the instant of model release to the instant of ground "
                  "contact\", measured from the readings of the accelerometer in the x direction (printed 5-44, PDF 324), into "
                  "whose output a pulse was injected at release (printed 5-39, PDF 319); no formula is printed. Signs are as "
                  "printed; the report's fixed axes point up from the ground and along the horizontal velocity (printed 5-18, "
                  "PDF 298). Every drop had zero angular rates, zero pitch and roll and a 45-degree yaw (a 2-2 landing) (printed "
                  "5-44, PDF 324), on a level bed (printed 5-43, PDF 323). A new bed was prepared for every drop; dynamic "
                  "penetrometer readings were taken on it after the drop, away from the footpads, and the report points to the "
                  "correlation of D_r with those readings (Paragraph 2.7.1) and to Section II for the other properties (printed "
                  "5-44, PDF 324). Section V prints the time histories of NASA Tests No. 1 and 2 (Figs. 5-22 to 5-39); Section VI "
                  "plots the measured histories of all eight drops against the report's computer simulation (Figs. 6-11 and 6-13 "
                  "to 6-19, printed 6-17 to 6-53, PDF 375 to 411), with the drop conditions again in Fig. 6-10 (printed 6-15, "
                  "PDF 373)."),
              "no_histories": "not yet extracted (the report plots them against its simulation in Section VI)",
              "precision": ("each value carries the precision of its printing (half a unit of its last printed digit); no "
                            "reading bound applies to a transcribed number. Printed values are in the columns named by their "
                            "printed unit (VV_in_s, Vh_in_s, gamma_pcf); a column kept as printed (tau_s, Dr, phi_deg) is not "
                            "repeated and keeps the printed digits, a leading decimal point included ('.298')")},
}


def value(s):
    """A printed number, or None for an empty cell or one with an unreadable digit (`?`, kept in the native column)."""
    s = (s or "").strip()
    if not s or "?" in s:
        return None
    try:
        return float(sum(Fraction(p) for p in s.split())) if "/" in s else float(s)
    except ValueError:
        return None


def same_test_records(test_type):
    """NASA Test No. (as printed) -> the index record of the same drop: a `single` row of the test type whose printed
    label is 'NASA Test No. <n>' (the records of the drops' time histories, batch experiments-s3s5-b1)."""
    out = {}
    for r in csv.DictReader(open(ROOT / "data" / "experiments" / "index.csv", encoding="utf-8", newline="")):
        lab = r["test_label_printed"].strip()
        if r["test_type"] == test_type and r["kind"] == "single" and lab.startswith("NASA Test No. "):
            n = lab[len("NASA Test No. "):].strip()
            if n in out:
                sys.exit(f"two records label NASA Test No. {n}: {out[n]}, {r['experiment_id']}")
            out[n] = r["experiment_id"]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch")
    ap.add_argument("--experiment", required=True)
    ap.add_argument("--figure", required=True)
    ap.add_argument("--family", choices=sorted(FAMILIES), default="drag")
    ap.add_argument("--soil-family", help="keep the rows whose printed Soil begins with this family (mdrop)")
    ap.add_argument("--source", default="bendix-1968-vol1")
    ap.add_argument("--out", default="data/experiments")
    ap.add_argument("--audits", default=str(ROOT / "qa" / "audits.csv"), help="the human audits (tools/ingest_review.py)")
    ap.add_argument("--no-audits", action="store_true")
    a = ap.parse_args()
    fam = FAMILIES[a.family]
    COLS = fam["cols"]
    q = ROOT / "qa" / a.batch
    rows = list(csv.DictReader(open(q / "agreed.csv", encoding="utf-8-sig", newline="")))
    if a.soil_family:
        if not fam["text"] or fam["text"][0][0] != "soil":
            sys.exit(f"--soil-family needs a table with a Soil column; family {a.family} has none")
        # a row whose Soil the readings did not agree on (empty) or could not read (`?`) belongs to no record yet: stop,
        # rather than leave it out of every family's record without a word (Codex's review, 2026-11-20)
        unsure = [r.get(fam["ids"][0][0], "?") for r in rows if not (r.get("soil") or "").strip() or "?" in r["soil"]]
        if unsure:
            sys.exit(f"rows {', '.join(unsure)} of qa/{a.batch}/agreed.csv have no agreed Soil: resolve them before --soil-family")
        rows = [r for r in rows if (r.get("soil") or "").split()[:1] == [a.soil_family]]
        if not rows:
            sys.exit(f"no row of qa/{a.batch}/agreed.csv has a Soil beginning with {a.soil_family}")
    key = fam["ids"][0][0]
    checks = {}
    if (q / "arithmetic-checks.csv").exists():
        for c in csv.DictReader(open(q / "arithmetic-checks.csv", encoding="utf-8", newline="")):
            if c["verdict"] in ("off", "flag"):
                checks.setdefault(c["run_number"], []).append(f"{c['check']}: computed {c['computed']}, printed {c['printed'] or '-'}")
    links = same_test_records(a.family) if fam["link"] else {}
    # the human audits of this table's cells, by (row key, printed column): [(auditor, outcome, chunk)]
    cell_audits = defaultdict(list)
    if not a.no_audits and Path(a.audits).exists():
        for r in csv.DictReader(open(a.audits, encoding="utf-8-sig", newline="")):
            parts = r["object"].split("/")
            # the exact form ingest writes for a table cell; anything else (another panel or source, a curve's column)
            # must not count toward a cell's confirmation (Codex's review, 2026-11-21, round 5)
            if (r["batch"] == a.batch and r.get("column") == "position+value" and len(parts) == 6
                    and parts[0] == a.figure and parts[1] == "1" and parts[3] == "cell" and parts[4] == "agreed"):
                m = re.search(r"chunk (W\d+-\d+)", r.get("note", ""))
                cell_audits[(parts[5], parts[2])].append((r["auditor"], r["outcome"], m.group(1) if m else ""))
    printed_cols = [c for c in (rows[0] if rows else {}) if c not in (key, "note", "status")]
    audited, n_cells = [], 0
    cols = ["experiment_id"] + [o for _, o in fam["ids"]] + ([fam["link"]] if fam["link"] else [])
    for _, _, _, _, si in COLS:
        cols.append(si)
    # the printed values, except where the SI column already holds them as printed (the same name)
    cols += [x[3] for x in EXTRA_SI] + [o for _, o in fam["text"]] + [n for n, *_ in COLS if n not in cols] + ["status", "check", "audit"]
    out_rows = []
    for r in rows:
        o = {"experiment_id": a.experiment}
        for i, oc in fam["ids"]:
            o[oc] = r.get(i, "")
        if fam["link"]:
            o[fam["link"]] = links.get(r.get(key, "").strip(), "")
        for t, oc in fam["text"]:
            o[oc] = r.get(t, "")
        # a printed identifier or text cell with no agreed value (empty) or an unreadable glyph (`?`) leaves the run
        # pending, like a number would (Codex's review, 2026-11-20: a blank Bendix number had passed as agreed)
        missing = [c for c, _ in fam["ids"] + fam["text"] if not (r.get(c) or "").strip() or "?" in r.get(c, "")]
        for native, _, fu, tu, si in COLS:
            v = value(r.get(native))
            o[native] = r.get(native, "")
            if v is None:
                missing.append(native)
                if si != native:   # a column kept as printed is its own SI column: its printed text (a `?`) stays
                    o[si] = ""
            elif fu == tu:   # kept as printed (a dimensionless number, an angle): its printed digits stand
                o[si] = r[native]
            else:
                o[si] = f"{v * FACTORS[(fu, tu)]:.6g}"
        for native, fu, tu, si in EXTRA_SI:
            v = value(r.get(native))
            o[si] = f"{v * FACTORS[(fu, tu)]:.6g}" if v is not None else ""
        o["status"] = "pending-review" if missing else "agreed"
        o["check"] = "; ".join(checks.get(r[key], []))
        notes = []
        for c in printed_cols:
            # only a cell the transcriptions agree on now counts, in the total and in the audits: one that has since
            # become empty or unreadable (`?`) keeps its history in qa/audits.csv and is not shown as checked (round 5)
            agreed_now = bool((r.get(c) or "").strip()) and "?" not in r.get(c, "")
            n_cells += agreed_now
            if agreed_now and (r[key], c) in cell_audits:
                rows_a = list({u: (u, v, ch) for u, v, ch in cell_audits[(r[key], c)]}.values())   # the last verdict per reviewer
                oc = pair_outcome([v for _, v, _ in rows_a])
                who = ", ".join(dict.fromkeys(f"{u} ({ch})" if ch else u for u, _, ch in rows_a))
                notes.append(f"{c} {oc} by {who}")
                audited.append(oc)
        o["audit"] = "; ".join(notes)
        out_rows.append(o)
    d = ROOT / a.out / a.experiment
    d.mkdir(parents=True, exist_ok=True)
    with (d / "runs.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(out_rows)
    meta = json.loads((ROOT / "extractions" / "codex" / a.batch / "meta.json").read_text(encoding="utf-8-sig"))
    side = {
        "experiment_id": a.experiment, "source": a.source, "figure_id": a.figure, "batch": a.batch, "kind": "run-table",
        "method": (f"two independent transcriptions of the printed table (Claude; Codex {meta.get('model', '?')} "
                   f"{meta.get('reasoning_effort', '')}), compared cell by cell by tools/diff_tables.py, every number exactly as "
                   "printed; a cell enters only when both agree (status agreed)"),
        "runs": len(out_rows), "by_status": {s: sum(1 for o in out_rows if o["status"] == s) for s in sorted({o["status"] for o in out_rows})},
        "columns": [{"printed": n, "quantity": qn, "unit_native": fu, "unit_si": tu, "column_si": si,
                     "factor": FACTORS.get((fu, tu), 1.0)} for n, qn, fu, tu, si in COLS]
                   + [{"printed": n, "quantity": "bulk density (unit weight under standard gravity)", "unit_native": fu,
                       "unit_si": tu, "column_si": si, "factor": FACTORS[(fu, tu)]} for n, fu, tu, si in EXTRA_SI],
    }
    if a.family == "drag":   # the drag file's keys, in their committed order
        side["derived_columns"] = ("A_ft is the total horizontal frontal area and A_pt the vertical frontal area of the footpad "
                                   "(labels of Fig. 4-4, printed 4-6, PDF 191; no formula printed); g in V_H/sqrt(dg) is not defined "
                                   "on the page. The arithmetic check is qa/" + a.batch + "/arithmetic.md; rows outside the printed "
                                   "rounding are named in `check`.")
    else:
        side["selection"] = (f"the rows of the printed table whose Soil begins with {a.soil_family}" if a.soil_family
                             else "every row of the printed table")
        side["same_test_as"] = ("the index record of the same drop (its time histories), a single mdrop row whose printed label "
                                "is the run's NASA Test No.; empty when the index holds none")
        for k in ("definitions", "no_histories"):
            if fam.get(k):
                side[k] = fam[k]
    side["audit"] = {"source": "qa/audits.csv (tools/ingest_review.py)", "cells": n_cells, "cells_sampled": len(audited),
                     "cells_confirmed": sum(1 for oc in audited if oc == "confirmed"),
                     "by_pair_outcome": dict(sorted(Counter(audited).items())),
                     "rule": ("the student reviewers check a sample of the printed cells against the scan, each cell for its row "
                              "and column (A) and its value as printed (B); a cell is confirmed when two reviewers answered ok; "
                              "`audit` in runs.csv lists each run's audited cells with their outcome; a run's status stays as the "
                              "two transcriptions left it")}
    side["precision"] = fam["precision"]
    side["pending_cells"] = ("a cell with an unreadable digit (`?`) keeps it in the printed column, its SI value is empty and its "
                             "row is pending-review" + ("" if a.family == "drag" else
                                                        "; a column kept as printed holds the printed text, `?` included"))
    arith = ROOT / "qa" / a.batch / "arithmetic.json"   # tools/check_drag_table.py --json
    if arith.exists():
        side["arithmetic"] = json.loads(arith.read_text(encoding="utf-8"))
        side["arithmetic"]["report"] = f"qa/{a.batch}/arithmetic.md"
    (d / "runs.json").write_text(json.dumps(side, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"{a.experiment}: {len(out_rows)} runs, {side['by_status']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
