# Blind reading of Figure C-16, Figure C-17, Figure C-18, Figure C-19, batch curves-appc-b10

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
   - `p0152.png`: Figure C-16 (FC-16), printed page C-38
   - `p0153.png`: Figure C-17 (FC-17), printed page C-39
   - `p0154.png`: Figure C-18 (FC-18), printed page C-40
   - `p0155.png`: Figure C-19 (FC-19), printed page C-41
   Context pages: `p0115.png`.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

## These figures

Figures C-16, C-17, C-18 and C-19 plot the **direct-shear angle of internal friction** phi_DS (degrees) against
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

## Lessons from earlier figures

1. A trace sample belongs on the drawn line's ink, never on a plotted symbol's outline or in the white gap between a dash and a symbol; a curve's first and last trace samples are where the line's ink starts and ends.
2. Where small symbols overlap, a symbol you cannot identify gets a note and a wide bound, never a guess; check that each mark is on a symbol and not on a neighbour or a speck of dirt.
3. Triangle centers are centroids (rule 8).
4. Check every printed axis label by eye against the line you anchor it to: a label printed off its line, or a frame that extends past the first or last labelled line, has misled readers before.

## Tools (folder `tools/`)

Python with Pillow and NumPy: `<local path>` (set
PYTHONIOENCODING=utf-8). Run each script with `--help` first: `tools/calibrate_axes.py detect|apply`
(grid lines, tilt, figures printed sideways with `--x-direction`/`--y-direction`), `tools/plot_grid.py
lines|crop|scan|overlay`. A figure with ticks but no grid lines: calibrate on the measured ticks
(your own helper, writing the same `calibration.json` layout, with `box`); a map whose interior lines
are only predicted from the frame does not count as calibrated (protocol section 4). Write helpers
under `out/`; do not modify `tools/`.

Finish with a short answer: per figure the counts per series and kind, the calibration residuals,
the by-eye label checks, the ambiguities, and the files written. Do not paste the CSVs.

## For the Claude reader

You read ONE figure (named in your task) in your own workspace; write under `out/<figure_id>/`.
Blindness: do not open anything under the project repository, the dan-codex-from-claude folder, or
any other folder of the scratchpad than your workspace and this TASK.md. Look at PNGs with the Read
tool; make zoomed crops with `tools/plot_grid.py crop` (zoom 3 to 6).
