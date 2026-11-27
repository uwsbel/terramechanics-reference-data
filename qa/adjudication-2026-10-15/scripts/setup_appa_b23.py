"""Batch configs for the Appendix A grain-size curves (log grain-size axis, printed sideways; batch
curves-appa-b2) and density charts (unit weight on a reciprocal axis; batch curves-appa-b3). Both need
the axis transforms of D-027."""
import csv
import json
from pathlib import Path

ROOT = Path(r"<repository>")
rows = {r["id"]: r for r in csv.DictReader(open(ROOT / "corpus/1968-vol2/figures.csv", encoding="utf-8-sig"))}

LESSONS = [
    "A trace sample belongs on the drawn line's ink, never on a plotted symbol's outline or in the white gap between dashes; a curve's first and last trace samples are where the line's ink starts and ends.",
    "Check every printed axis label by eye against the line you anchor it to: a label printed off its line, or a frame that extends past the first or last labelled line, has misled readers before.",
    "Give the printed values to the tool and declare the axis transform (docs/CURVE-READING.md rule 5); never type a logarithm or a reciprocal.",
]

GRAIN = ["FA-2", "FA-6", "FA-18", "FA-22", "FA-26", "FA-38", "FA-46"]
DENSITY = ["FA-3", "FA-7", "FA-19", "FA-23", "FA-27", "FA-39", "FA-47"]

GRAIN_SPECIFIC = """## These figures

Figures A-2, A-6, A-18, A-22, A-26, A-38 and A-46 are **grain-size distribution curves**: percent finer
than by weight against grain size (mm), one soil per figure, printed **sideways** on the page (read the
page as scanned: grain size increases up the page, percent finer to the left; pass `--x-direction up
--y-direction left` to `calibrate_axes.py detect`). The grain-size axis is a **log axis**
(`--x-transform log10`): give the printed grain sizes (0.02, 0.05, 0.1, ...), never their logarithms.
The page also carries a second scale of U.S. standard sieve numbers, a table of grain-size parameters
and a classification strip: none of these is read as points (the table's values are already
transcribed).

Calibration: anchor the grid lines that carry a printed grain-size label and the labelled percent
lines (0 to 100). The printed log paper has many unlabelled subdivision lines and dashed sieve lines:
do not anchor them unless you can name each one's value without doubt from the printed labels (rule
5); when in doubt leave them out. Say in `calibration-eye-checks.csv` which label each checked line
carries; check that the frame lines are or are not labelled.

Series (`series.csv`): `average` the solid curve; `upper` and `lower` the dashed curves of the range on
either side of it (`upper` the one with the higher percent finer at a given grain size).

What to produce, under `out/<figure_id>/`:

1. `cal-p1/` and `calibration-eye-checks.csv` (three printed labels per axis checked by eye).
2. `points-p1.csv` and `points-p1-native.csv`, `panel = 1`, grain size in mm, percent finer in percent:
   - each curve as `trace` samples in drawing order from its fine end (small grain size): its first
     point, then every 0.05 decade of grain size (0.0200, 0.0224, 0.0251, ... : ten to the power of
     steps of 0.05), and, where the curve rises by more than 10 percent between two such samples, extra
     samples at every 5 percent finer between them, then its last point. On a dashed curve a sample in
     a gap moves to the nearest dash end (rule 7). Bound: half the line thickness. Where the three
     curves run together, say so in the note and widen the bound rather than guess which is which.
   - any plotted symbol on the curves as `marker` (series of the curve it is on).
   - `feature` points per rule 3 for every trace (first point, last point, any knee).
3. `overlay-p1.png` and `notes.md` (which curve is which, where they merge, the frame and the labels).
"""

DENSITY_SPECIFIC = """## These figures

Figures A-3, A-7, A-19, A-23, A-27, A-39 and A-47 are **density charts**: unit weight (pcf) against
relative density Dr, one soil per figure, upright. The unit-weight axis runs **downward** (25 pcf at the
top, 65 at the bottom; the left scale is labelled minimum density, the right one maximum density, on
the same lines) and its lines are evenly spaced in 1/gamma: it is a **reciprocal axis**
(`--y-transform reciprocal --y-direction down`); give the printed unit weights, never their
reciprocals. Dr runs from 0 to 1.0 to the right (linear). The figure draws straight lines from a
minimum density printed at Dr = 0 to a maximum density printed at Dr = 1.0, each end labelled with its
value (for example 40.1 and 51.8).

Calibration: anchor the lines that carry a printed unit-weight label (25, 30, ... 65) and the labelled
Dr lines; the many unlabelled lines between the unit-weight labels are evenly spaced in 1/gamma, and you
may anchor them only if you can name each one's value without doubt. Say in
`calibration-eye-checks.csv` which label each checked line carries.

Series (`series.csv`): `mean` the solid line; `upper` and `lower` the dashed lines above and below it on
the page.

What to produce, under `out/<figure_id>/`:

1. `cal-p1/` and `calibration-eye-checks.csv` (three printed labels per axis checked by eye).
2. `points-p1.csv` and `points-p1-native.csv`, `panel = 1`, unit weight in pcf:
   - each line as `trace` samples in drawing order from Dr = 0: its left end, every 0.1 of Dr, its
     right end. On a dashed line a sample in a gap moves to the nearest dash end (rule 7). Bound: half
     the line thickness.
   - `feature` points per rule 3 (first and last point); and per line one `feature` at each end label
     with note "label: <the printed value>" placed at the label's center, so the printed value can be
     matched to its line (the leader lines show which label belongs to which line).
3. `overlay-p1.png` and `notes.md` (which label belongs to which line, anything ambiguous).
"""


def write(batch, figs, roles, specific):
    cfg = {"batch": batch, "source": "1968-vol2", "context_pages": [],
           "figures": {f: {"series": [{"series_id": s, "role": r, "soil": rows[f]["soils"]} for s, r in roles]} for f in figs},
           "specific": specific, "lessons": LESSONS}
    d = ROOT / "qa" / batch
    d.mkdir(parents=True, exist_ok=False)
    (d / "batch.json").write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(batch, figs)


write("curves-appa-b2", GRAIN, [("average", "solid curve"), ("upper", "dashed curve with the higher percent finer"),
                                ("lower", "dashed curve with the lower percent finer")], GRAIN_SPECIFIC)
write("curves-appa-b3", DENSITY, [("mean", "solid line"), ("upper", "dashed line above the solid one on the page"),
                                  ("lower", "dashed line below the solid one on the page")], DENSITY_SPECIFIC)
