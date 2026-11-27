# Blind reading of Figure A-2, Figure A-6, Figure A-18, Figure A-22, Figure A-26, Figure A-38, Figure A-46, batch curves-appa-b2

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
   - `p0007.png`: Figure A-2 (FA-2), printed page A-6
   - `p0014.png`: Figure A-6 (FA-6), printed page A-13
   - `p0039.png`: Figure A-18 (FA-18), printed page A-38
   - `p0047.png`: Figure A-22 (FA-22), printed page A-46
   - `p0054.png`: Figure A-26 (FA-26), printed page A-53
   - `p0077.png`: Figure A-38 (FA-38), printed page A-76
   - `p0095.png`: Figure A-46 (FA-46), printed page A-94
   Context pages: none.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

## These figures

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
