# Blind reading of Figure C-12, Figure C-13, Figure C-14, Figure C-15, batch curves-appc-b9

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
   - `p0148.png`: Figure C-12 (FC-12), printed page C-34
   - `p0147.png`: Figure C-13 (FC-13), printed page C-35
   - `p0150.png`: Figure C-14 (FC-14), printed page C-36
   - `p0151.png`: Figure C-15 (FC-15), printed page C-37
   Context pages: `p0115.png`.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

## These figures

Figures C-12, C-13, C-14 and C-15 are **computer-plotted failure envelopes**: shear strength against normal stress,
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
