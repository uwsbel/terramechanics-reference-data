# Blind reading of Figure B-3, Figure B-4, Figure B-5, Figure B-6, Figure B-7, batch curves-appb-b1

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
   - `p0109.png`: Figure B-3 (FB-3), printed page 6
   - `p0110.png`: Figure B-4 (FB-4), printed page 7
   - `p0111.png`: Figure B-5 (FB-5), printed page 8
   - `p0112.png`: Figure B-6 (FB-6), printed page 9
   - `p0113.png`: Figure B-7 (FB-7), printed page 10
   Context pages: none.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

## These figures

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

## Lessons from earlier figures

1. A trace sample belongs on the drawn line's ink, never on a plotted symbol's outline or in the white gap between a line and a symbol; a curve's first and last trace samples are where the line's ink starts and ends.
2. Where small symbols overlap, a symbol you cannot identify gets a note and a wide bound, never a guess; check that each mark is on a symbol and not on a neighbour or a speck of dirt.
3. Check every printed axis label by eye against the line or tick you anchor it to: a label printed off its line, or a frame that extends past the first or last labelled line, has misled readers before.

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
