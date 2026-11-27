"""Write data/experiments/<id>/observations.csv and series.json from canonical curve points.

Usage:
    python tools/build_observations.py <canonical_points.csv> --figure FC-1B --source bendix-1968-vol2 \
        --series-map qa/<batch>/series-map.csv --panel-map qa/<batch>/panel-map.csv \
        --cal-a <dir> --cal-b <dir> --batch curves-pilot-b1 [--out data/experiments]

Inputs:
    canonical_points.csv   written by tools/diff_curves.py --canonical: one row per matched point
                           with pixel coordinates, x_native, y_native, bounds, status, source and
                           the other reading's values.
    series-map.csv         series_id, experiment_id  (which experiment a plotted series belongs to)
    panel-map.csv          [figure_id,] panel, x_quantity, x_unit, x_si_unit, y_quantity, y_unit,
                           y_si_unit (printed units and the SI unit each converts to; units as
                           tools/to_si.py names them: mil, psf, inch, ...); with a figure_id column,
                           the rows of this figure (a batch whose figures differ in units); optional
                           record_panel (the record's panel number for that figure panel, when a
                           record spans several figures), relation (a panel that re-plots another)
                           and note (what a user of the panel's values must know); the last two are
                           written to series.json as given
    --figure               one figure, or several when one record spans them (the impact runs:
                           Figs. 4-19 and 4-20); a record's figures go in one call, since each call
                           rewrites the records it touches
    --cal-a, --cal-b       each reading's calibrations, one directory per --figure, normally
                           qa/<batch>/rederived/<reader>/<figure> (tools/reconcile_curves.py):
                           calibration.json and, for piecewise maps (D-025), knots.json, whose lines
                           and location errors go to series.json
    --breaks               qa/<batch>/breaks.csv, optional: a drawn line's explicit breaks (a scan dropout the
                           readers stopped at), as the rows on either side; series.json `breaks`
    --audits               qa/audits.csv (the default; --no-audits skips it): the human audits recorded by
                           tools/ingest_review.py. A point two reviewers answered `ok` (pair outcome
                           `confirmed`) gets status `audited` if the readings had agreed on it, else
                           `confirmed`, its earlier status kept in the note; every other pair outcome
                           (single, split, flagged, cannot-tell, or a mix such as `ok + cannot tell`) is appended to the note and leaves the
                           status alone; a verdict on a reading a decision has since replaced (source
                           `<reader>-interp`) is noted as superseded and not applied (roadmap 4c,
                           2026-10-30, reviewed by Codex). The audit object
                           names the reading whose numbering `sequence` is: the canonical reading of the
                           panel, which is `source` unless a decision kept the other reading's value
                           (`<reader>-interp`), where it is the other reader.

Output, per experiment (SI canonical, native kept for traceability, never computed from):
    observations.csv  experiment_id, series_id, panel, point_kind, sequence, x_si, y_si,
                      x_bound_si, y_bound_si, x_native, y_native, x_read_bound, y_read_bound,
                      x_unit_native, y_unit_native, pixel_u, pixel_v, status, source, note
    series.json       figure, panel quantities and units, conversion factors, both submissions'
                      calibration residuals, point counts by status, the reading rules version.
                      A record from several figures also lists `figures`, gives each panel its
                      `figure_id` and `figure_panel`, and keys calibrations by figure (F4-20/cal-p1).
Rows of an experiment keep the order of the canonical file within each panel and series (drawing
order: tools/diff_curves.py writes the other reading's samples before the start of the canonical
trace first and those after its end last), never sorted by x. Until 2026-10-13 rows were sorted by
sequence, which was right while every row came from one reading's numbering; since points of both
readings can be in one series, `sequence` is the numbering of the reading named in `source`.
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from to_si import FACTORS  # noqa: E402
from ingest_review import pair_outcome  # noqa: E402  (one definition of a pair outcome, shared with the ingest)

ROOT = Path(__file__).resolve().parents[1]

COLS = ["experiment_id", "series_id", "panel", "point_kind", "sequence", "x_si", "y_si", "x_bound_si", "y_bound_si",
        "x_native", "y_native", "x_read_bound", "y_read_bound", "x_unit_native", "y_unit_native",
        "pixel_u", "pixel_v", "status", "source", "note"]


def read(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def figure_rows(a, fig, cal_dirs):
    """One figure's points as record rows, by experiment. Returns (rows by experiment, the readers' calibrations,
    piecewise, printed labels by series, the panel map, the record panel of each figure panel, the Codex model).
    A record read from several figures (the impact runs of Figs. 4-19 and 4-20) numbers its panels across them by
    the panel map's record_panel column; without it a figure's panels are the record's. Audit objects keep the
    figure's own panel numbers."""
    audits = defaultdict(list)   # object -> [(auditor, outcome, chunk)], this batch and figure only
    if not a.no_audits and Path(a.audits).exists():
        for r in read(a.audits):
            if r["batch"] == a.batch and r["object"].startswith(fig + "/"):
                m = re.search(r"chunk (W\d+-\d+)", r.get("note", ""))
                audits[r["object"]].append((r["auditor"], r["outcome"], m.group(1) if m else ""))

    # a batch's canonical file can hold several figures (series ids repeat across figures): keep this one
    pts = [r for r in read(a.points) if r.get("figure_id", fig) == fig]
    # a printed label read as a feature (the friction angle of a failure envelope) is text, not a
    # point of the curve: it goes to series.json as printed, not into observations.csv
    is_label = lambda r: r["point_kind"] == "feature" and (r.get("note") or "").strip().lower().startswith("label")
    labels = {}
    for r in pts:
        if is_label(r):
            labels.setdefault(r["series_id"], []).append(r["note"].split(":", 1)[-1].strip().split(";")[0])
    pts = [r for r in pts if not is_label(r)]
    meta = ROOT / "extractions" / "codex" / a.batch / "meta.json"   # the Codex run's own record of its model
    codex_model = "gpt-6-astra high"
    if meta.exists():
        m = json.loads(meta.read_text(encoding="utf-8-sig"))
        codex_model = f"{m.get('model', '?')} {m.get('reasoning_effort', '')}".strip()
    smap = {r["series_id"]: r["experiment_id"] for r in read(a.series_map) if r.get("figure_id", fig) == fig}
    pmap = {r["panel"]: r for r in read(a.panel_map) if r.get("figure_id", fig) == fig}
    rec = {p: (r.get("record_panel") or p) for p, r in pmap.items()}   # the record's panel of each figure panel
    cal = {}
    piecewise = False
    for label, d in zip(a.labels.split(","), cal_dirs):
        cal[label] = {}
        # the adopted calibration of each panel (cal-p1, cal-fc1b-p1); a reader's rejected variants
        # (cal-p1-A, cal-p1-B, ...) are kept in its submission but are not the calibration of the data
        cands = sorted(Path(d).glob("cal-*p*/calibration.json")) or sorted(Path(d).glob("*/calibration.json"))
        for p in [c for c in cands if re.search(r"p\d$", c.parent.name)] or cands:
            c = json.loads(p.read_text(encoding="utf-8"))
            # a calibration made by hand from tick marks may lack a field (no box on Fig. C-2A): keep what it has
            cal[label][p.parent.name] = {k: c[k] for k in ("x_per_px", "y_per_px", "rms_residual_x", "rms_residual_y",
                                                           "max_residual_x", "max_residual_y", "n_anchors", "box", "method",
                                                           "x_transform", "y_transform")
                                         if k in c}
            kj = p.parent / "knots.json"
            if kj.exists():   # the piecewise map of the data (D-025): its lines, their location errors, the lines not used
                k = json.loads(kj.read_text(encoding="utf-8"))
                line = lambda kn: {"value": kn["value"], "location_error_px": kn["location_error_px"]}
                cal[label][p.parent.name]["map"] = {
                    "model": k["model"], "submitted_calibration": k["submitted_calibration"],
                    "x_lines": [line(kn) for kn in k["x"]], "y_lines": [line(kn) for kn in k["y"]],
                    "lines_not_on_the_ink": [{"axis": ax, "value": kn["value"], "reason": kn["reason"]}
                                             for ax in ("x", "y") for kn in k["rejected_" + ax]],
                    "recovered_lines": len(k.get("recovered_lines", []))}
                piecewise = True
    # a point no reading could give a series (an unassigned marker still open after adjudication) belongs to
    # no experiment: it stays in the batch's canonical file and is listed here, never guessed into a record
    orphans = [r for r in pts if r["series_id"] not in smap]
    for r in orphans:
        print(f"not in any record (series {r['series_id'] or '(none)'} has no experiment): {r['point_kind']} {r['source']} "
              f"{r['sequence']} at pixel ({r['pixel_u']}, {r['pixel_v']}), status {r['status']}")
    pts = [r for r in pts if r["series_id"] in smap]
    # explicit breaks of a drawn line (qa/<batch>/breaks.csv: a scan dropout the readers stopped at): the two rows on
    # either side, which must follow each other in the canonical drawing order of the series; to series.json
    breaks = {}
    if a.breaks and Path(a.breaks).exists():
        for b in read(a.breaks):
            if b["figure_id"] != fig:
                continue
            # the drawn line's own rows, as the plot draws them (a feature row is not on the line the pen lifts from)
            ser = [f"{r['source']}|{r['sequence']}" for r in pts if r["panel"] == b["panel"] and r["series_id"] == b["series_id"]
                   and r["point_kind"] in ("trace", "gridline")]
            if b["after"] not in ser or b["before"] not in ser or ser.index(b["before"]) != ser.index(b["after"]) + 1:
                sys.exit(f"{fig} panel {b['panel']} {b['series_id']}: break {b['after']} / {b['before']} is not two consecutive rows")
            breaks.setdefault(smap[b["series_id"]], []).append({
                "panel": rec[b["panel"]], "series_id": b["series_id"],
                "after": dict(zip(("source", "sequence"), b["after"].split("|"))),
                "before": dict(zip(("source", "sequence"), b["before"].split("|"))), "reason": b["reason"]})
    by_exp = {}
    # on a transformed axis (D-027) values span decades, so SI values keep six significant digits rather than a
    # fixed number of decimals, which would write a small grain size's bound as zero (Codex's review)
    first = next(iter(cal.values()), {})
    def si(v, f, axis, panel, places):
        t = first.get(f"cal-p{panel}", {}).get(f"{axis}_transform", "linear")
        return round(v * f, places) if t == "linear" else float(f"{v * f:.6g}")
    for r in pts:
        pm = pmap[r["panel"]]
        fx, fy = FACTORS[(pm["x_unit"], pm["x_si_unit"])], FACTORS[(pm["y_unit"], pm["y_si_unit"])]
        row = {
            "experiment_id": smap[r["series_id"]], "series_id": r["series_id"], "panel": rec[r["panel"]],
            "_figure_panel": r["panel"],   # the printed figure's panel this row comes from (not written to the CSV)
            "point_kind": r["point_kind"], "sequence": int(r["sequence"]),
            "x_si": si(float(r["x_native"]), fx, "x", r["panel"], 9), "y_si": si(float(r["y_native"]), fy, "y", r["panel"], 6),
            "x_bound_si": si(float(r["x_read_bound"]), fx, "x", r["panel"], 9),
            "y_bound_si": si(float(r["y_read_bound"]), fy, "y", r["panel"], 6),
            "x_native": r["x_native"], "y_native": r["y_native"], "x_read_bound": r["x_read_bound"], "y_read_bound": r["y_read_bound"],
            "x_unit_native": pm["x_unit"], "y_unit_native": pm["y_unit"],
            "pixel_u": r["pixel_u"], "pixel_v": r["pixel_v"], "status": r["status"], "source": r["source"],
            "note": (r.get("note", "") + (" | decision: " + r["decision_note"] if r.get("decision_note") else "")).strip(),
        }
        if audits:
            src = r["source"]
            owner = src if "-interp" not in src else ("claude" if src.startswith("codex") else "codex")
            found = [audits[k] for k in (f"{fig}/{r['panel']}/{r['series_id']}/{r['point_kind']}/{o}/{r['sequence']}"
                                         for o in dict.fromkeys((owner, src))) if k in audits]
            if found:
                rows_a = list({u: (u, v, c) for u, v, c in found[0]}.values())   # one verdict per auditor (the last)
                oc = pair_outcome([v for _, v, _ in rows_a])
                who = ", ".join(dict.fromkeys(f"{u} ({c})" if c else u for u, _, c in rows_a))
                if src != owner:
                    # the reviewers judged the reading a decision has since replaced at this sample (D-030: the
                    # value is the other reader's, interpolated): their verdict is history, not a check of this value
                    row["note"] = (row["note"] + f" | audit: {oc} by {who}, on the {owner} reading before the decision replaced it; not applied").strip(" |")
                    oc = f"superseded ({oc})"
                elif oc == "confirmed":
                    # two reviewers answered ok on this reading's own point: `audited` for a point the two readings
                    # agreed on, `confirmed` for one that rested on a rule, a re-read or one reading (Codex's review)
                    new = "audited" if row["status"] == "agreed" else "confirmed"
                    row["note"] = (row["note"] + f" | audit: confirmed by {who}; was {row['status']}").strip(" |")
                    row["status"] = new
                else:
                    row["note"] = (row["note"] + f" | audit: {oc} by {who}").strip(" |")
                row["audit"] = oc
        by_exp.setdefault(row["experiment_id"], []).append(row)
    # two panels of this figure in one record panel of the same record would mix their units (Codex's review); the
    # panels of different records may share a record panel number (each DPT record of Fig. 2-54 is its own panel 1)
    for exp in by_exp:
        used = {}
        for fp in sorted({r["panel"] for r in pts if smap.get(r["series_id"]) == exp}, key=int):
            if rec[fp] in used:
                sys.exit(f"{fig}: panels {used[rec[fp]]} and {fp} both map to record panel {rec[fp]} of {exp} in {a.panel_map}")
            used[rec[fp]] = fp

    return by_exp, cal, piecewise, labels, pmap, rec, codex_model, breaks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("points")
    ap.add_argument("--figure", required=True, nargs="+", help="one or more figures; a record's figures go in one call")
    ap.add_argument("--source", required=True)
    ap.add_argument("--series-map", required=True)
    ap.add_argument("--panel-map", required=True)
    ap.add_argument("--breaks", help="qa/<batch>/breaks.csv: explicit breaks of a drawn line (figure_id, panel, series_id, "
                    "after, before as source|sequence, reason), written to series.json and honored by the plots")
    ap.add_argument("--cal-a", required=True, nargs="+", help="per figure, in the order of --figure")
    ap.add_argument("--cal-b", required=True, nargs="+", help="per figure, in the order of --figure")
    ap.add_argument("--batch", required=True)
    ap.add_argument("--labels", default="claude,codex")
    ap.add_argument("--out", default="data/experiments")
    ap.add_argument("--audits", default=str(ROOT / "qa" / "audits.csv"))
    ap.add_argument("--no-audits", action="store_true")
    a = ap.parse_args()
    if not len(a.figure) == len(a.cal_a) == len(a.cal_b):
        sys.exit("--figure, --cal-a and --cal-b need one entry per figure")
    by_exp = {}   # experiment -> [(figure, rows, cal, piecewise, labels, pmap, rec)], in the order of --figure
    breaks_of = {}   # experiment -> explicit breaks of its drawn lines (qa/<batch>/breaks.csv)
    codex_model = ""
    for fig, ca, cb in zip(a.figure, a.cal_a, a.cal_b):
        rows_by_exp, cal, piecewise, labels, pmap, rec, codex_model, brk = figure_rows(a, fig, (ca, cb))
        for exp, rows in rows_by_exp.items():
            by_exp.setdefault(exp, []).append((fig, rows, cal, piecewise, labels, pmap, rec))
            breaks_of.setdefault(exp, []).extend(brk.get(exp, []))

    out_root = Path(a.out)
    for exp, parts in sorted(by_exp.items()):
        multi = len(parts) > 1
        owner = {}   # record panel -> (figure, figure panel, panel map row); a record panel comes from one figure only
        # from the figure panels that supply this record's rows, not from the whole panel map: there, the last of
        # several panels mapped to one record panel won, and each DPT record named figure panel 3 (Codex's review)
        for fig, prow, _, _, _, pmap, rec in parts:
            for fp in dict.fromkeys(r["_figure_panel"] for r in prow):
                rp = rec[fp]
                if rp in owner and owner[rp][:2] != (fig, fp):
                    sys.exit(f"{exp}: record panel {rp} is mapped from {owner[rp][0]} panel {owner[rp][1]} and {fig} panel {fp}")
                owner[rp] = (fig, fp, pmap[fp])
        rows = [r for part in parts for r in part[1]]
        rows.sort(key=lambda r: (int(r["panel"]), r["series_id"]))  # stable: drawing order within a series
        piecewise = any(part[3] for part in parts)
        labels = {}
        for part in parts:
            for sid, ts in part[4].items():
                labels.setdefault(sid, []).extend(ts)
        # one figure: the readers' calibrations by panel (cal-p1, ...); several: by figure and panel (F4-20/cal-p1)
        cal = parts[0][2] if not multi else {
            label: {f"{fig}/{k}": v for fig, _, c, *_ in parts for k, v in c.get(label, {}).items()}
            for label in dict.fromkeys(l for part in parts for l in part[2])}
        d = out_root / exp
        d.mkdir(parents=True, exist_ok=True)
        with (d / "observations.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n", extrasaction="ignore")   # `audit` feeds series.json only
            w.writeheader()
            w.writerows(rows)
        panels = sorted({r["panel"] for r in rows}, key=int)

        def panel_entry(p):
            fig, fp, pm = owner[p]
            # the figure and its panel, when the record spans figures or renumbers a panel (each DPT record of Fig. 2-54
            # is its own panel 1, from figure panel 1, 2 or 3)
            e = {"figure_id": fig, "figure_panel": fp} if multi or fp != p else {}
            e.update({"x_quantity": pm["x_quantity"], "x_unit_native": pm["x_unit"], "x_unit_si": pm["x_si_unit"],
                      "x_factor": FACTORS[(pm["x_unit"], pm["x_si_unit"])],
                      "y_quantity": pm["y_quantity"], "y_unit_native": pm["y_unit"], "y_unit_si": pm["y_si_unit"],
                      "y_factor": FACTORS[(pm["y_unit"], pm["y_si_unit"])]})
            if pm.get("relation"):   # a panel that re-plots another (Fig. 4-20 cross-plots the histories of Fig. 4-19)
                e["relation"] = pm["relation"]
            if pm.get("note"):       # what a user of this panel's values must know (a misprinted axis label)
                e["note"] = pm["note"]
            return e
        side = {
            "experiment_id": exp, "source": a.source, "figure_id": parts[0][0], "batch": a.batch,
        }
        if multi:
            side["figures"] = [part[0] for part in parts]
        side.update({
            "reading_rules": "docs/CURVE-READING.md (2026-10-08)",
            "method": f"two independent readings (Claude, Codex {codex_model}) with their own axis calibrations, "
                      "compared by tools/diff_curves.py; " + (
                          "values from each reading's pixels on a piecewise map between its verified lines (D-025); canonical "
                          "reading chosen by the lines checked against the ink of the page (more verified lines, then closer "
                          "to the ink, then the first submission), " if piecewise else
                          "canonical reading chosen by the smaller calibration residual, ") +
                      "never averaged; status agreed where the two readings matched within the sum of their bounds, resolved where a "
                      "page re-read settled a disagreement (qa/<batch>/decisions*.csv), one-sided-verified where only one "
                      "reading holds the point and the other agent verified it on the page, one-sided where nobody has; "
                      "`source` names the reading each point comes from and whose numbering `sequence` is",
            "panels": {p: panel_entry(p) for p in panels},
            "calibrations": cal,
            "points": {"total": len(rows), "by_status": dict(Counter(r["status"] for r in rows)),
                       "by_kind": dict(Counter(r["point_kind"] for r in rows)), "by_panel": dict(Counter(r["panel"] for r in rows))},
            "audit": {"source": "qa/audits.csv (tools/ingest_review.py)",
                      "points_sampled": sum(1 for r in rows if r.get("audit")),
                      "by_pair_outcome": dict(Counter(r["audit"] for r in rows if r.get("audit"))),
                      "rule": "a point both reviewers answered ok has status audited (it was agreed) or confirmed (it rested on "
                              "a rule, a re-read or one reading); the earlier status is in the note; any other outcome is noted "
                              "and leaves the status as the readings left it; a verdict on a reading a decision has since "
                              "replaced is kept as history (superseded) and not applied"},
            "bounds": ("x_read_bound and y_read_bound are reading bounds in printed units: the largest change of value over the "
                       "point's pixel interval on the piecewise map, plus the location error of the two lines around it (D-025; the "
                       "global calibration residual is not added, see qa/<batch>/calibration-sensitivity.md for the affine "
                       "difference)" if piecewise else
                       "x_read_bound and y_read_bound are reading bounds in printed units (pixel bound times the local scale plus "
                       "the calibration RMS residual)") + "; x_bound_si and y_bound_si are the same in SI. They are not standard deviations.",
            "pixel_frame": (f"pixel_u, pixel_v refer to the unrotated 300 dpi rendering of PDF page of {parts[0][0]} "
                            if not multi else
                            "pixel_u, pixel_v refer to the unrotated 300 dpi rendering of the PDF page of the panel's figure "
                            "(panels: figure_id) ") + "(tools/render_pages.py), origin top-left, u right, v down.",
        })
        printed = sorted({t for s in {r["series_id"] for r in rows} for t in labels.get(s, [])})
        if printed:   # only figures that carry printed labels on their lines; other records are unchanged
            side["printed_labels"] = printed
        if breaks_of.get(exp):   # only records whose lines have an explicit break; other records are unchanged
            side["breaks"] = breaks_of[exp]
        (d / "series.json").write_text(json.dumps(side, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"{exp}: {len(rows)} points, {dict(Counter(r['status'] for r in rows))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
