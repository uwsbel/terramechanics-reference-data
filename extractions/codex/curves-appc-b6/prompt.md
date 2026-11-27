# Blind reading of Figure C-5A, Figure C-6A, Figure C-7A, batch curves-appc-b6

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
   - `p0129.png`: Figure C-5A (FC-5A), printed page C-15
   - `p0131.png`: Figure C-6A (FC-6A), printed page C-17
   - `p0135.png`: Figure C-7A (FC-7A), printed page C-21
   Context pages: `p0115.png`.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

## These figures

Figures C-5A, C-6A and C-7A are **failure envelopes**: maximum shear stress against normal stress (psf on C-5A and C-6A; shear load against normal load in psi on C-7A), one panel each, upright. Each density group of the legend is one series: its plotted symbols are the peak shear stresses of the direct shear tests of that group, and a straight line drawn through them (solid, often extended to the shear-stress axis by a dashed part) is the authors' fit, labelled with a friction angle. Series ids are in `series.csv`, named by the printed Dr range of the group in hundredths (`dr2-13` for Dr .02 to .13). On C-5A only the first group has data sheets in this appendix; the others come from an earlier test series.

What to produce, under `out/<figure_id>/`:

1. `cal-p1/` and `calibration-eye-checks.csv` (three printed labels per axis checked by eye; these figures may have ticks but no grid lines).
2. `points-p1.csv` and `points-p1-native.csv`, `panel = 1`:
   - every plotted symbol as `marker`, with `symbol` (`circle`, `filled circle`, `square`, `triangle-up`, `triangle-down`, `x`, `plus`, `asterisk`, `dotted circle`, `dotted triangle`, or a described shape) and its series. Where a symbol's shape and the line it sits on disagree, give the series by shape and say so in the note (rule 9).
   - each drawn line as `trace` samples in drawing order from its left end: its left end (on the shear-stress axis if the dashed part reaches it), then every 250 psf of normal stress (every 2 psi on C-7A), then its right end. Mark samples on the dashed part with "dashed" in the note. Bound: half the line thickness (rule 7).
   - per series one `feature` with note "intercept" (where the line meets the normal-stress-zero axis) and one `feature` with note "label: <the printed angle>" placed at the printed angle label's center.
3. `overlay-p1.png`, `notes.md` (which line carries which printed angle, symbols that do not match the legend, anything ambiguous).

## Lessons from earlier figures

1. A trace sample belongs on the drawn line's ink, never on a plotted symbol's outline or in the white gap between a dash and a symbol; a curve's first and last trace samples are where the line's ink starts and ends.
2. Where small symbols overlap, a symbol you cannot identify gets a note and a wide bound, never a guess; check that each mark is on the named symbol and not on a neighbour.
3. Triangle centers are centroids (rule 8).
4. On an envelope a symbol sitting on another group's line belongs to the group of its shape; dashed extensions are extrapolations and pass through other groups' symbols near the axis.

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
