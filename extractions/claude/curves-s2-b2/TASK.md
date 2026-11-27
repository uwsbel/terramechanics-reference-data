# Blind reading of Figure 2-45, Figure 2-46, Figure 2-47, Figure 2-48, batch curves-s2-b2

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
   - `p0106.png`: Figure 2-45 (F2-45), printed page 2-81
   - `p0107.png`: Figure 2-46 (F2-46), printed page 2-82
   - `p0108.png`: Figure 2-47 (F2-47), printed page 2-83
   - `p0109.png`: Figure 2-48 (F2-48), printed page 2-84
   Context pages: `p0105.png`.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

## These figures

Figures 2-45, 2-46, 2-47 and 2-48 are **load-penetration records**: the load on a penetrator (lb) against its penetration into the soil bed (in), one panel each, two recorded traces per figure (a four-inch cylinder and a four-inch footpad in the same soil bed), from Section II of Volume I. Figures 2-45 and 2-48 are printed **sideways**: read the page as scanned, with penetration increasing **up** the page and load increasing to the **left** (`--x-direction up --y-direction left` to `calibrate_axes.py detect`). Figures 2-46 and 2-47 are upright (penetration to the right, load up). Both axes are linear with a drawn grid; anchor the labelled grid lines (penetration every inch; load every 25 or 50 lb on 2-45, every 100 lb on 2-46, every 500 lb on 2-47, every 200 lb on 2-48) and check three printed labels per axis by eye (`calibration-eye-checks.csv`). On 2-45 the frame extends past the last labelled load line (250) and the penetration axis runs to 7; on 2-46 the penetration axis ends at 6 with a short tick beyond; on 2-47 the load frame top is 2000.

Each figure draws two **recorded traces** (the chart-recorder record of one test, LPT = load penetration test, numbered), one solid and one dotted or dashed; `series.csv` gives the id of each with its printed label and line style. On Figure 2-47 the two traces cross near 0.5 in and again near 6 in, and the printed label of LPT No. 101 has a leader arrow to the dashed curve: follow the arrow and the line style together, and say in `notes.md` how you told the two apart where they cross or run together. No straight fit lines are drawn on these four figures.

What to produce, under `out/<figure_id>/`:

1. `cal-p1/` and `calibration-eye-checks.csv` (three printed labels per axis checked by eye).
2. `points-p1.csv` and `points-p1-native.csv`, `panel = 1`:
   - every recorded trace as `trace` samples in drawing order from where its ink starts (penetration 0) to where it ends: one sample every 0.25 in of penetration, plus the features of rule 3 (first point, peak of the trace, every knee or kink, last point) as `feature` rows with a note saying which (`first`, `peak`, `knee`, `last`). A trace that doubles back keeps its drawing order (rule 4). Bound: half the line thickness (rule 7); on a dotted line sample on the dots, never in the gaps between them, and widen the bound to half the dot spacing along the line. Where the two traces cross or run together, say so in `note` and widen the bound.
   - no markers: these figures plot no symbols. If you see any, record them as `marker` with a note.
3. `overlay-p1.png`, `notes.md` (which line carries which printed label, where the traces cross, anything ambiguous).

Context page (text only, for the setup): PDF 105 introduces the cylinder-against-footpad comparison. Read it for understanding; nothing on it is a point.

## Lessons from earlier figures

1. A trace sample belongs on the drawn line's ink, never on a plotted symbol's outline or in the white gap between dashes or dots; a curve's first and last trace samples are where the line's ink starts and ends.
2. Check every printed axis label by eye against the line you anchor it to: a label printed off its line, or a frame that extends past the first or last labelled line, has misled readers before.
3. On a sideways page the pixel coordinates still refer to the page as scanned; declare the directions to the tool and never rotate the image.
4. A thick line's center is known to within half its width: measure the width where you sample it and give that half-width as the bound, not a fixed number.

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
