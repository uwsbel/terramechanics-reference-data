# Blind reading of Figure 5-24, Figure 5-25, Figure 5-31, Figure 5-32, batch curves-s5-b1

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
   - `p0329.png`: Figure 5-24 (F5-24), printed page 5-49
   - `p0330.png`: Figure 5-25 (F5-25), printed page 5-50
   - `p0336.png`: Figure 5-31 (F5-31), printed page 5-56
   - `p0337.png`: Figure 5-32 (F5-32), printed page 5-57
   Context pages: `p0324.png`, `p0325.png`.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

## These figures

Four figures of Section V of Volume I record two drops of the 1/6-scale Lunar Module model onto loose RS soil, NASA Test No. 1 (a vertical drop) and NASA Test No. 2 (a drop with horizontal velocity). All four are printed **sideways** (rotation 90 in the figures index: turn the page to read it); work in the pixel coordinates of the unrotated image, as always. Context pages: PDF 324 (printed 5-44, the correlation tests) and PDF 325 (Table 5-T3, the detail correlation drops); nothing on them is a point.

1. **Figure 5-24** (`p0329.png`, NASA Test No. 1) and **Figure 5-31** (`p0336.png`, NASA Test No. 2): one panel each, footpad penetration depth (inches) against time (seconds, 0 to 0.1), one solid line, series `pen`.
2. **Figure 5-25** (`p0330.png`, NASA Test No. 1) and **Figure 5-32** (`p0337.png`, NASA Test No. 2): three panels sharing the time axis (seconds, 0 to 0.10), read upright top to bottom: panel 1 Strut No. 3 (`strut3`), panel 2 Strut No. 2 (`strut2`), panel 3 Strut No. 1 (`strut1`), each the axial load in pounds, one solid line per panel. Each panel's axis title says (Tension) or (Compression), and its labels may carry a sign (`+40`, `-60`): record every label exactly as printed in `calibration-eye-checks.csv`, anchor each line at the value its printed label gives, and where a label's sign or digits break the panel's own sequence (a `-60` above `+40`, a damaged `.09`), anchor the line from the sequence, not the misprint, and say so in `notes.md`. A trace that crosses below a panel's 0 line takes values beyond 0 on that panel's scale; record them as the scale gives them. An inset diagram and the drop's conditions are printed at the right of Figures 5-25 and 5-32: they are not points; quote the conditions in `notes.md`.

What to produce, under `out/<figure_id>/`:

1. `cal-p<n>/` for each panel and `calibration-eye-checks.csv`.
2. `points-p<n>.csv` and `points-p<n>-native.csv`: every trace as `trace` samples in drawing order from where its ink starts to where it ends: one sample every 0.002 s up to 0.02 s and every 0.005 s after, and on steep parts also one every 0.2 in (Figures 5-24 and 5-31) or every 5 lb (Figures 5-25 and 5-32), whichever spacing is finer there; plus the features of rule 3 as `feature` rows, each note **beginning with its role word**: `first`, `peak` for each local maximum, `knee, minimum` for a local minimum, `knee` for another clear bend, `last`. Bound: half the line thickness (rule 7). No markers: the figures plot no symbols.
3. `overlay-p<n>.png` and `notes.md` (the labels as printed, any label slip and how you anchored it, the inset's conditions, where a trace is hard to follow).

## Lessons from earlier figures

1. A trace sample belongs on the drawn line's ink, never on a grid line, a label or the inset; a curve's first and last trace samples are where the line's ink starts and ends.
2. Check every printed axis label by eye against the line you anchor it to: a label printed off its line, a label missing from an evenly spaced sequence, a label with a wrong sign or digit, or a frame that extends past the last labelled line, has misled readers before (Figure 4-19 of this report skips the label 110 on its time axis).
3. A thick line's center is known to within half its width: measure the width where you sample it and give that half-width as the bound, not a fixed number.
4. The description of a figure in this task is itself a reading and has been wrong before (it once called a dashed reference line the zero of a scale, which the printed ruler contradicted): trust the page, keep the ids given, and report every difference in notes.md.
5. Begin every feature note with its role word (first, peak, knee, last): the comparison of the two readings pairs features by that word.

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
