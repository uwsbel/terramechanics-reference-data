# Blind reading of Figure A-3, Figure A-7, Figure A-19, Figure A-23, Figure A-27, Figure A-39, Figure A-47, batch curves-appa-b3

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
   - `p0008.png`: Figure A-3 (FA-3), printed page A-7
   - `p0015.png`: Figure A-7 (FA-7), printed page A-14
   - `p0040.png`: Figure A-19 (FA-19), printed page A-39
   - `p0048.png`: Figure A-23 (FA-23), printed page A-47
   - `p0055.png`: Figure A-27 (FA-27), printed page A-54
   - `p0078.png`: Figure A-39 (FA-39), printed page A-77
   - `p0096.png`: Figure A-47 (FA-47), printed page A-95
   Context pages: none.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

## These figures

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

## Lessons from earlier figures

1. A trace sample belongs on the drawn line's ink, never on a plotted symbol's outline or in the white gap between dashes; a curve's first and last trace samples are where the line's ink starts and ends.
2. Check every printed axis label by eye against the line you anchor it to: a label printed off its line, or a frame that extends past the first or last labelled line, has misled readers before.
3. Give the printed values to the tool and declare the axis transform (docs/CURVE-READING.md rule 5); never type a logarithm or a reciprocal.

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
