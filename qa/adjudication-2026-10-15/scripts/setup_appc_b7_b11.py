"""Batch configs for the last Appendix C figures: the computer-plotted envelopes FC-8 to FC-15
(batches curves-appc-b7, b8, b9) and the friction-angle charts FC-16 to FC-23 (b10, b11).
Writes qa/<batch>/batch.json; the packets are then written by tools/make_reading_packet.py."""
import csv
import json
from pathlib import Path

ROOT = Path(r"<repository>")
rows = {r["id"]: r for r in csv.DictReader(open(ROOT / "corpus/1968-vol2/figures.csv", encoding="utf-8-sig"))}

COMPUTER = {"curves-appc-b7": ["FC-8", "FC-9A", "FC-9B", "FC-9C", "FC-10A"],
            "curves-appc-b8": ["FC-10B", "FC-10C", "FC-11A", "FC-11B", "FC-11C"],
            "curves-appc-b9": ["FC-12", "FC-13", "FC-14", "FC-15"]}
PHI = {"curves-appc-b10": ["FC-16", "FC-17", "FC-18", "FC-19"],
       "curves-appc-b11": ["FC-20", "FC-21", "FC-22", "FC-23"]}

LESSONS = [
    "A trace sample belongs on the drawn line's ink, never on a plotted symbol's outline or in the white gap between a dash and a symbol; a curve's first and last trace samples are where the line's ink starts and ends.",
    "Where small symbols overlap, a symbol you cannot identify gets a note and a wide bound, never a guess; check that each mark is on a symbol and not on a neighbour or a speck of dirt.",
    "Triangle centers are centroids (rule 8).",
    "Check every printed axis label by eye against the line you anchor it to: a label printed off its line, or a frame that extends past the first or last labelled line, has misled readers before.",
]

COMPUTER_SPECIFIC = """## These figures

Figures {names} are **computer-plotted failure envelopes**: shear strength against normal stress,
one panel each, upright, on a grid with a line at every 100 printed units, with a box above the plot
that prints the test group, its average density, angle of friction, tan theta and cohesion. Each
figure has one series (`series.csv`): its plotted symbols are the peak shear stresses of the direct
shear tests of the group, and the straight line is the least-squares fit.

Units: both axis titles print `(x 10^1)`, so a tick printed `100.00` is 1000 psf. Calibrate in psf
(anchor value = ten times the printed label) and say in `calibration-eye-checks.csv` which printed
label each checked line carries.

What to produce, under `out/<figure_id>/`:

1. `cal-p1/` and `calibration-eye-checks.csv` (three printed labels per axis checked by eye).
2. `points-p1.csv` and `points-p1-native.csv`, `panel = 1`, values in psf:
   - every plotted symbol as `marker`, with `symbol` (`triangle-up`, or a described shape if another
     is printed) and the series of `series.csv`. Two symbols that overlap are two markers if they can
     be told apart; otherwise one marker with a note and a wide bound.
   - the drawn straight line as `trace` samples in drawing order from its left end: its left end,
     then every 500 psf of normal stress, then its right end. Bound: half the line thickness (rule 7).
   - `feature` points per rule 3 (the line's first and last point) and one `feature` with note
     "intercept" where the line meets the normal-stress-zero axis, if it reaches it (if it stops
     short, no intercept, and say so).
3. `overlay-p1.png` and `notes.md`. In notes.md, transcribe the four values printed in the box as
   printed, then compare them with your reading: the slope of your trace samples against "Tan
   Theta", and the shear stress of your intercept against "Cohesion" (in psf). Report the
   differences; do NOT move any point to agree with the printed values, which are evidence about
   the authors' computation, not about where the ink is.
"""

PHI_SPECIFIC = """## These figures

Figures {names} plot the **direct-shear angle of internal friction** phi_DS (degrees) against
**relative density** Dr (dimensionless), one panel each, upright. Figures C-16 to C-20 and C-22 show,
for one soil, open circles (some joined in pairs by a short horizontal line: one friction angle
measured over a range of Dr), a solid curve and two dashed curves. Figure C-21 shows circles and a
cross-hatched band between two lines instead of the curves. Figure C-23 shows six curves, each
labelled with a soil name, in different line styles, and no symbols.

Calibration: the frame may extend past the first and last labelled grid lines (left of 0, right of
1.0). Anchor only grid lines whose printed labels you have checked by eye; say in
`calibration-eye-checks.csv` which label each checked line carries. Units: x `none` (Dr), y `deg`.

Series (`series.csv`): `data` for every circle; `mean` the solid curve; `upper` and `lower` the
dashed curves above and below it; on C-21 `band-top` and `band-bottom` the two edges of the
hatched band; on C-23 one series per printed soil label.

What to produce, under `out/<figure_id>/`:

1. `cal-p1/` and `calibration-eye-checks.csv` (three printed labels per axis checked by eye).
2. `points-p1.csv` and `points-p1-native.csv`, `panel = 1`:
   - every circle as `marker` in series `data`, `symbol` = `circle` (or what is printed). A circle at
     an end of a horizontal joining line gets note "pair <n> left" or "pair <n> right" (pairs
     numbered from the left); a circle with no joining line gets note "single". A circle cut by the
     frame or overlapping a curve or another circle: say so in the note and widen the bound.
   - each curve (and on C-21 each band edge) as `trace` samples in drawing order from its left end:
     its left end, then every 0.05 of Dr, then its right end. On a dashed curve a sample whose Dr
     falls in a gap between dashes moves to the nearest dash end, on the ink (rule 7). Bound: half
     the line thickness. The horizontal lines joining pairs of circles and the hatching are not
     traced. On C-23, identify each curve by its printed label and its line style, and say in
     notes.md where curves cross or touch.
   - `feature` points per rule 3 for every trace (first point, last point, any knee); on C-23 one
     `feature` per soil with note "label: <the printed text>" at the label's center.
3. `overlay-p1.png` and `notes.md` (which curve is which, circles cut by the frame, the frame's
   extent beyond the labelled lines, anything ambiguous).
"""


def name(fids):
    return ", ".join("C-" + f[3:] for f in fids[:-1]) + " and C-" + fids[-1][3:]


def computer_series(fid):
    title = rows[fid]["title_as_printed"].strip()          # e.g. "RS Loose"
    return [{"series_id": title.lower().replace(" ", "-"), "title_printed": title,
             "soil": rows[fid]["soils"], "state_printed": rows[fid]["states"]}]


def phi_series(fid):
    soil = rows[fid]["soils"]
    if fid == "FC-23":
        return [{"series_id": s.lower(), "role": "curve labelled " + s, "soil": s}
                for s in ("RC2", "PS", "RS", "RSM-b", "RSM-a", "SS")]
    roles = [("data", "open circles"), ("band-top", "upper edge of the hatched band"),
             ("band-bottom", "lower edge of the hatched band")] if fid == "FC-21" else \
            [("data", "open circles"), ("mean", "solid curve"), ("upper", "dashed curve above the solid one"),
             ("lower", "dashed curve below the solid one")]
    return [{"series_id": s, "role": r, "soil": soil} for s, r in roles]


for batches, specific, series in ((COMPUTER, COMPUTER_SPECIFIC, computer_series), (PHI, PHI_SPECIFIC, phi_series)):
    for batch, fids in batches.items():
        cfg = {"batch": batch, "source": "1968-vol2", "context_pages": [115],
               "figures": {f: {"series": series(f)} for f in fids},
               "specific": specific.format(names=name(fids)), "lessons": LESSONS}
        d = ROOT / "qa" / batch
        d.mkdir(parents=True, exist_ok=False)
        (d / "batch.json").write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        print(batch, fids)
