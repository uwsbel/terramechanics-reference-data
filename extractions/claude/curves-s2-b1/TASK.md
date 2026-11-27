# Blind reading of Figure 2-29, Figure 2-32, Figure 2-33, Figure 2-34, batch curves-s2-b1

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
   - `p0080.png`: Figure 2-29 (F2-29), printed page 2-55
   - `p0088.png`: Figure 2-32 (F2-32), printed page 2-63
   - `p0089.png`: Figure 2-33 (F2-33), printed page 2-64
   - `p0090.png`: Figure 2-34 (F2-34), printed page 2-65
   Context pages: `p0077.png`, `p0086.png`, `p0091.png`.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

## These figures

Figures 2-29, 2-32, 2-33 and 2-34 are **load-penetration records**: the load on a cylindrical penetrator (lb) against its penetration into the soil bed (in), one panel each, from Section II of Volume I. All four are printed **sideways**: read the page as scanned, with penetration increasing **up** the page and load increasing to the **left** (`--x-direction up --y-direction left` to `calibrate_axes.py detect`). Both axes are linear with a drawn grid; anchor the labelled grid lines (penetration every inch, load every 200 lb on 2-29 and 2-34, every 10 lb on 2-32, every 500 lb on 2-33) and check three printed labels per axis by eye (`calibration-eye-checks.csv`). The frame may extend past the last labelled line.

Each figure draws one or more **recorded traces** (the chart-recorder record of one test, LPT = load penetration test, numbered; a wavy or stepped line) and, on 2-32, 2-33 and 2-34, one or two **straight lines** drawn by the authors: a thin or thick straight line labelled `Slope = ... lbs./in.` (the authors' fit to the linear part of a trace, series `fit`) and on 2-33 a second straight line labelled `Bearing Capacity Equation` (series `bce`). The text blocks of equations beside the curves are not points. `series.csv` gives the id of every curve with its printed label and line style; where a label's leader arrow and the line style disagree, follow the arrow and say so in `notes.md`.

On Figure 2-34 the load axis is labelled `Load - Lbs. x 100`: give the tool the numbers printed on the axis (0 to 1200) with unit `lb` and record the printed label in `notes.md` and in `calibration-eye-checks.csv`; do not multiply. The other three figures print plain pounds.

What to produce, under `out/<figure_id>/`:

1. `cal-p1/` and `calibration-eye-checks.csv` (three printed labels per axis checked by eye).
2. `points-p1.csv` and `points-p1-native.csv`, `panel = 1`:
   - every recorded trace as `trace` samples in drawing order from where its ink starts (penetration 0, or 2 in for the tests started two inches below the surface) to where it ends: one sample every 0.25 in of penetration, plus the features of rule 3 (first point, peak of the trace, every knee or kink, last point) as `feature` rows with a note saying which (`first`, `peak`, `knee`, `last`). A trace that doubles back keeps its drawing order (rule 4). Bound: half the line thickness (rule 7). Where two traces cross or run together, say so in `note` and widen the bound.
   - each straight line (`fit`, `bce`) as `trace` samples at both ends of its ink and at every labelled penetration line it crosses, plus one `feature` with note `intercept` where it meets the load axis (penetration 0) if its ink reaches it, and one `feature` with note `label: <the printed text>` at the center of its printed label.
   - no markers: these figures plot no symbols. If you see any, record them as `marker` with a note.
3. `overlay-p1.png`, `notes.md` (which line carries which printed label, where traces cross, the Figure 2-34 axis label, anything ambiguous).

Context pages (text only, for the setup): PDF 77 describes Figure 2-29 (the test whose DPT record 54074 is shown elsewhere); PDF 86 and 91 describe the bearing-capacity comparison of Figures 2-32 to 2-34. Read them for understanding; nothing on them is a point.

## Lessons from earlier figures

1. A trace sample belongs on the drawn line's ink, never on a plotted symbol's outline or in the white gap between dashes; a curve's first and last trace samples are where the line's ink starts and ends.
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
