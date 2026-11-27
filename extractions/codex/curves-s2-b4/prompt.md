# Blind reading of Figure 2-54, batch curves-s2-b4

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
   - `p0117.png`: Figure 2-54 (F2-54), printed page 2-92
   Context pages: `p0115.png`, `p0116.png`.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

## This figure

Figure 2-54 (`p0117.png`, printed page 2-92) shows three **drop penetrometer (DPT) records**: the deceleration of the penetrometer against time as it hits a soil bed, one oscillograph trace per record. It is printed **sideways** (rotation 90 in the figures index: turn the page to read it); work in the pixel coordinates of the unrotated image, as always. The context pages are PDF 115 (printed 2-90, the DPT and how it is used) and PDF 116 (Figure 2-53, the DPT and its schematic); nothing on them is a point.

Read upright, the figure has **three panels**, top to bottom: panel 1 is Record No. 53958 (RS loose), panel 2 Record No. 54025 (RS intermediate), panel 3 Record No. 54-65 (LPT No. 26, RS dense). Each panel has one solid trace, its own deceleration ruler (G's) with labeled ticks (panel 1: 0, 10, 20; panel 2: 0, 10, 20, 30; panel 3: 0 to 80 by 10) and a dashed zero line. Deceleration increases upward on the upright figure.

**Time.** The vertical timing lines run across all three panels. A bar with arrows marked `.01 sec` shows the spacing: check by eye that its arrows meet two adjacent timing lines, and say so in `notes.md`. The figure prints **no time origin**. Use this convention, in **milliseconds**: the timing line that carries the three G rulers (the rulers' zero ticks stand on it) is **0 ms**; the lines to its right are 10, 20, 30, ... ms and those to its left -10, -20, ... ms. Anchor every timing line you can see clearly in each panel, in each panel's own `cal-p<n>/`. Left of the timing grid each trace is cut by **break marks** (a zigzag in the line): that part is not on the time base; do not read it.

**Deceleration.** Calibrate each panel on its own ruler: anchor the labeled ticks and, where you are sure of their value (count them between labels), the minor ticks; the dashed zero line is 0 g. Record each check in `calibration-eye-checks.csv`.

**Points**, under `out/F2-54/`, `points-p1.csv`, `points-p2.csv`, `points-p3.csv` and their `-native.csv`:

1. the trace as `trace` samples in drawing order, from the first timing line right of the break marks to the right end of its ink: one sample every 0.5 ms from 2 ms before the trace leaves zero to 5 ms after its main peak, every 1 ms up to 20 ms, every 2 ms after that, and on the steep parts also one every 2 g (panels 1 and 2) or 5 g (panel 3), whichever spacing is finer there;
2. the features of rule 3 as `feature` rows, each note **beginning with its role word**: `first` (where the trace's ink begins, at the first timing line right of the break marks), `knee, onset` for the point where the trace leaves its zero level, `peak` for each local maximum, `knee, minimum` for the local minimum after a peak, `knee` for any other clear bend, `last` (the right end of the ink);
3. bounds: half the line thickness (rule 7), measured where you sample; where the trace runs on the dashed zero line or a timing line, say so in `note` and widen the bound;
4. no markers: the figure plots no symbols.

Also `overlay-p<n>.png` and `notes.md` (the scale-bar check, the time convention as you applied it, where the trace is hard to follow, anything ambiguous).

## Lessons from earlier figures

1. A trace sample belongs on the drawn line's ink, never on a grid line, a ruler tick or a label; a curve's first and last trace samples are where the line's ink starts and ends.
2. Check every printed axis label by eye against the line or tick you anchor it to: a label printed off its line, a label missing from an evenly spaced sequence, or a frame that extends past the first or last labelled line, has misled readers before (Figure 4-19 of this report skips the label 110 on its time axis).
3. A thick line's center is known to within half its width: measure the width where you sample it and give that half-width as the bound, not a fixed number.
4. The description of a figure in this task is itself a reading and has been wrong before (it once stated two line styles the wrong way round): trust the page, keep the ids given, and report every difference in notes.md.
5. Begin every feature note with its role word (first, peak, knee, last): the comparison of the two readings pairs features by that word, and a note that begins otherwise may be paired with the wrong feature.

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
