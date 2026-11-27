# Blind reading of Figure 4-19, Figure 4-20, batch curves-s4-b1

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
   - `p0208.png`: Figure 4-19 (F4-19), printed page 4-23
   - `p0209.png`: Figure 4-20 (F4-20), printed page 4-24
   Context pages: `p0192.png`, `p0206.png`, `p0207.png`.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

## These figures

Figures 4-19 and 4-20 are **vertical impact tests** from Section IV of Volume I: a 6.17 in footpad dropped vertically onto beds of RS soil at three relative densities, the same three runs (Run No. 4, 10 and 12) in both figures. This is the first batch with time on an axis.

**Figure 4-19** (`p0208.png`, printed upright) has **two panels** sharing the time axis (milliseconds): panel 1 (top) is the vertical force on the footpad (pounds), panel 2 (bottom) its displacement into the soil (inches). Each panel draws the three runs: Run No. 4 solid, Run No. 10 dotted, Run No. 12 long dashes (legend in panel 1). Check **every** printed time label against the grid line it stands under, by eye, and record each check in `calibration-eye-checks.csv`; anchor only lines whose value you are sure of, and say in `notes.md` how you assigned values to the time grid lines beyond 100. Figure 4-20 plots the same runs against displacement: at a given time, panel 1's force and panel 2's displacement should land on that run's Figure 4-20 curve, which is a check on the time axis you may use; say if you did. The force pulse is short and steep (a peak within the first few milliseconds): sample it densely.

**Figure 4-20** (`p0209.png`) is printed **sideways** (rotation 90 in the figures index: turn the page to read it); one panel, vertical force (pounds) against displacement (inches). The three runs, same line styles. Each trace ends where the footpad stops and the force falls; a trace that doubles back (unloading at the largest displacement) keeps its drawing order (rule 4). Work in the pixel coordinates of the unrotated image, as always.

What to produce, under `out/<figure_id>/`:

1. `cal-p1/` (and for Figure 4-19 also `cal-p2/`) and `calibration-eye-checks.csv`.
2. `points-p<n>.csv` and `points-p<n>-native.csv`, with `panel` 1 or 2:
   - every recorded trace as `trace` samples in drawing order from where its ink starts to where it ends. Figure 4-19: one sample every 1 ms up to 10 ms, every 2 ms up to 30 ms, every 5 ms after that, and on the steep parts of the force pulse also one every 50 lb of force (whichever spacing is finer there). Figure 4-20: one sample every 0.1 in of displacement and every 50 lb of force where the curve is steep (whichever is finer). Plus the features of rule 3 as `feature` rows with a note saying which: `first`, `last`, every knee or kink (`knee`), each local maximum of the force (`peak`) and the local minimum after it (`knee`, minimum). Bound: half the line thickness (rule 7); on a dotted or dashed line sample on the ink, never in the gaps, and widen the bound to half the gap along the line. Where traces cross or run together, say so in `note` and widen the bound.
   - no markers: these figures plot no symbols. If you see any, record them as `marker` with a note.
3. `overlay-p<n>.png`, `notes.md` (which line is which run, where traces cross or run together, the time-axis labels, anything ambiguous).

Context pages (text only, for the setup): PDF 192 (printed 4-7) describes the impact test program, PDF 206 (Figure 4-17, printed 4-21) the oblique impact test parameter values, PDF 207 (printed 4-22) introduces Figures 4-19 to 4-22. Read them for understanding; nothing on them is a point.

## Lessons from earlier figures

1. A trace sample belongs on the drawn line's ink, never on a plotted symbol's outline or in the white gap between dashes or dots; a curve's first and last trace samples are where the line's ink starts and ends.
2. Check every printed axis label by eye against the line you anchor it to: a label printed off its line, a label missing from an evenly spaced sequence, or a frame that extends past the first or last labelled line, has misled readers before.
3. A thick line's center is known to within half its width: measure the width where you sample it and give that half-width as the bound, not a fixed number.
4. The description of a figure in this task is itself a reading and has been wrong before (it once stated two line styles the wrong way round): trust the page, keep the ids given, and report every difference in notes.md.

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
