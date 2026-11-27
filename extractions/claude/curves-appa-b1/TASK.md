# Blind reading of Figure A-4, Figure A-8, Figure A-20, Figure A-24, Figure A-28, Figure A-40, Figure A-48, batch curves-appa-b1

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
   - `p0009.png`: Figure A-4 (FA-4), printed page A-8
   - `p0016.png`: Figure A-8 (FA-8), printed page A-15
   - `p0041.png`: Figure A-20 (FA-20), printed page A-40
   - `p0049.png`: Figure A-24 (FA-24), printed page A-48
   - `p0056.png`: Figure A-28 (FA-28), printed page A-55
   - `p0079.png`: Figure A-40 (FA-40), printed page A-78
   - `p0097.png`: Figure A-48 (FA-48), printed page A-96
   Context pages: none.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

## These figures

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
