"""Batch configs for Appendix B (modulus plots FB-3 to FB-7, batch curves-appb-b1) and the Appendix A
friction-angle charts (FA-4, 8, 20, 24, 28, 40, 48, batch curves-appa-b1). Linear axes only: the
grain-size (log) and density (reciprocal) charts wait for the axis transforms."""
import csv
import json
from pathlib import Path

ROOT = Path(r"<repository>")
rows = {r["id"]: r for r in csv.DictReader(open(ROOT / "corpus/1968-vol2/figures.csv", encoding="utf-8-sig"))}

LESSONS = [
    "A trace sample belongs on the drawn line's ink, never on a plotted symbol's outline or in the white gap between a line and a symbol; a curve's first and last trace samples are where the line's ink starts and ends.",
    "Where small symbols overlap, a symbol you cannot identify gets a note and a wide bound, never a guess; check that each mark is on a symbol and not on a neighbour or a speck of dirt.",
    "Check every printed axis label by eye against the line or tick you anchor it to: a label printed off its line, or a frame that extends past the first or last labelled line, has misled readers before.",
]

APPB = {"FB-3": [("dr99", "Dense, Dr = 0.99"), ("dr30", "Loose, Dr = 0.30")],
        "FB-4": [("dr86", "Dense, Dr = 0.86"), ("dr22", "Loose, Dr = 0.22")],
        "FB-5": [("dr84", "Dense, Dr = 0.84"), ("dr26", "Loose, Dr = 0.26")],
        "FB-6": [("dr82", "Dense, Dr = 0.82"), ("dr02", "Loose, Dr = 0.02")],
        "FB-7": [("dr104", "Dr = 1.04"), ("dr99p5", "Dr = 0.995"), ("dr77", "Dr = 0.77")]}

APPB_SPECIFIC = """## These figures

Figures B-3 to B-7 plot a **modulus** E = rho c^2 (kips/in.^2) against the **confining pressure**
sigma_3 (psi), one soil per figure, one panel, upright. Each density group is one series
(`series.csv`, named by its printed Dr in hundredths): its plotted symbols are measurements, and the
straight segments drawn by the authors through or near them form one polyline per group, labelled
with the group's Dr. On B-3 to B-6 every symbol is an open circle; on B-7 the three groups have three
symbols (the legend labels say which), and a group may have symbols but no line.

The plots have a frame with ticks and printed labels and no grid lines: calibrate on the measured
ticks (see Tools), with the frame lines only where a printed label sits on them. Some labels are
poorly printed: a label that does not fit the printed sequence is reported in notes.md and anchors
nothing unless the tick spacing confirms its value. The frame of B-6 is visibly skewed on the page;
fit each tick line with its own tilt and check the residuals.

What to produce, under `out/<figure_id>/`:

1. `cal-p1/` and `calibration-eye-checks.csv` (three printed labels per axis checked by eye).
2. `points-p1.csv` and `points-p1-native.csv`, `panel = 1`:
   - every plotted symbol as `marker`, with `symbol` (`circle`, `filled circle`, `square with x`, or a
     described shape) and its series. Where both groups use the same symbol, the series is the group
     whose line the symbol sits on or is nearest to, with a note when that is not clear; two
     overlapping symbols are two markers if they can be told apart, otherwise one with a note and a
     wide bound.
   - each group's polyline as `trace` samples in drawing order from its left end: its left end, every
     vertex, every 1 psi of confining pressure between them, and its right end. Bound: half the line
     thickness (rule 7).
   - `feature` points per rule 3: the polyline's first and last point and every vertex (note
     "vertex"); and one `feature` per group with note "label: <the printed text>" at the center of the
     group's printed label.
3. `overlay-p1.png` and `notes.md` (which polyline carries which label, symbols whose group is unclear,
   labels that do not fit their sequence, anything ambiguous).
"""

APPA = ["FA-4", "FA-8", "FA-20", "FA-24", "FA-28", "FA-40", "FA-48"]

APPA_SPECIFIC = """## These figures

Figures A-4, A-8, A-20, A-24, A-28, A-40 and A-48 plot the **angle of internal friction** phi
(degrees, as determined by the direct shear test) against **relative density** Dr
(dimensionless), one soil per figure (named in the caption), one panel, upright, on a grid. Each
shows one solid curve, except A-40, which may show a cross-hatched band between two lines and
symbols instead; read what is printed.

Calibration: the frame may extend past the first or last labelled grid line. Anchor only lines
whose printed labels you have checked by eye; units: x `none` (Dr), y `deg`.

Series (`series.csv`): `curve` for the solid curve; on A-40 `band-top` and `band-bottom` for the edges
of a hatched band and `data` for any symbols (if the figure shows a single curve after all, use
`curve` and say so in notes.md).

What to produce, under `out/<figure_id>/`:

1. `cal-p1/` and `calibration-eye-checks.csv` (three printed labels per axis checked by eye).
2. `points-p1.csv` and `points-p1-native.csv`, `panel = 1`:
   - each curve (or band edge) as `trace` samples in drawing order from its left end: its left end,
     then every 0.05 of Dr, then its right end. Bound: half the line thickness (rule 7).
   - any plotted symbol as `marker` in series `data`.
   - `feature` points per rule 3 for every trace (first point, last point, any knee).
3. `overlay-p1.png` and `notes.md`.
"""


def write(batch, figures, specific):
    cfg = {"batch": batch, "source": "1968-vol2", "context_pages": [], "figures": figures,
           "specific": specific, "lessons": LESSONS}
    d = ROOT / "qa" / batch
    d.mkdir(parents=True, exist_ok=False)
    (d / "batch.json").write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(batch, list(figures))


write("curves-appb-b1",
      {f: {"series": [{"series_id": s, "label_printed": l, "soil": rows[f]["soils"]} for s, l in ss]} for f, ss in APPB.items()},
      APPB_SPECIFIC)
write("curves-appa-b1",
      {f: {"series": ([{"series_id": "curve", "role": "solid curve", "soil": rows[f]["soils"]}] if f != "FA-40" else
                      [{"series_id": "band-top", "role": "upper edge of the hatched band", "soil": rows[f]["soils"]},
                       {"series_id": "band-bottom", "role": "lower edge of the hatched band", "soil": rows[f]["soils"]},
                       {"series_id": "data", "role": "symbols, if any", "soil": rows[f]["soils"]},
                       {"series_id": "curve", "role": "a single solid curve, if that is what is printed", "soil": rows[f]["soils"]}])}
       for f in APPA},
      APPA_SPECIFIC)
