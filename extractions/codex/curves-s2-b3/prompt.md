# Blind reading of Figure 2-42, Figure 2-44, batch curves-s2-b3

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared point by point with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so read
carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images, 300 dpi, unrotated; pixel coordinates in everything you write refer to them (`u`
   right, `v` down, origin top-left). The figures to read:
   - `p0102.png`: Figure 2-42 (F2-42), printed page 2-77
   - `p0104.png`: Figure 2-44 (F2-44), printed page 2-79
   Context pages: `p0099.png`.
2. `figures-rows.csv`: the figures' rows in the project's figures index.
3. `series.csv`: the series of each figure with the id to use. The ids come from the figures index,
   which is itself a reading and has been wrong before: if the page prints something different, keep
   the id given and report what is printed in notes.md.
4. `CURVE-READING.md`: the protocol. Follow it, including rules 7 to 9.

## These figures

Figures 2-42 and 2-44 are **load-penetration records** from Section II of Volume I: the load on a four-inch cylinder (lb) against its penetration into a bed of dense RS soil (in), one panel each. Both are printed **upright** (penetration to the right, load up). Both axes are linear with a drawn grid; check three printed labels per axis by eye (`calibration-eye-checks.csv`).

**Figure 2-42** (`p0102.png`) draws four recorded traces (LPT = load penetration test, numbered), lettered A to D by circled letters; the inset key gives each letter's test number, Gp, unit weight and penetration rate. Anchor the penetration grid lines (0 to 3 in, every inch) and the load grid lines (0 to 1200 lb, every 200 lb). The top edge of the frame, above 1200, has no label: do not anchor it. A label 627 with a short tick sits just above the 600 line: it marks a value, not a grid line; do not anchor it. Trace B is a solid line and trace D is drawn in long dashes; A and C are a dotted line and a short-dashed line: decide which is which from the circled letters and the line styles, and say in `notes.md` how you decided. The four traces rise together and overlap below about 0.4 in and 800 lb: follow each by its line style, widen the bound where they run together, and say so in `note`. A trace that leaves the plot ends where its ink meets the frame.

**Figure 2-44** (`p0104.png`) draws five recorded traces from bins of three sizes (key: A 18 by 36 inch bin, B 36 by 36 inch, C 54 by 36 inch; Gp values in parentheses). Three traces have their label printed along the line (LPT No. 73, 69 and 64A, each after its bin letter); two have a label printed below the curves with an arrow to the line (LPT No. 74 and LPT No. 24). Line styles are solid, dashed and dotted, and some traces may share a style: identify each trace by its label or arrow, follow it through crossings by style and continuity, and say in `notes.md` how you told them apart. Anchor the penetration grid lines (0 to 5 in, every inch) and the load grid lines (0 to 2000 lb, every 500 lb); the key box covers the middle of the 2000 line, so anchor that line on the parts that show. Short strokes near the labels that belong to no trace are not samples.

What to produce, under `out/<figure_id>/`:

1. `cal-p1/` and `calibration-eye-checks.csv` (three printed labels per axis checked by eye).
2. `points-p1.csv` and `points-p1-native.csv`, `panel = 1`:
   - every recorded trace as `trace` samples in drawing order from where its ink starts (penetration 0) to where it ends: one sample every 0.25 in of penetration and, on the steep rise at the start, also one every 100 lb of load (whichever spacing is finer there), plus the features of rule 3 as `feature` rows with a note saying which: `first`, `last`, every knee or kink (`knee`), the first local maximum of the load (`peak`, first maximum) and the local minimum after it (`knee`, minimum), and the highest load of the trace if it is not the last point (`peak`). A trace that doubles back keeps its drawing order (rule 4). Bound: half the line thickness (rule 7); on a dotted or dashed line sample on the ink, never in the gaps, and widen the bound to half the gap along the line. Where traces cross or run together, say so in `note` and widen the bound.
   - no markers: these figures plot no symbols. If you see any, record them as `marker` with a note.
3. `overlay-p1.png`, `notes.md` (which line carries which printed label, where the traces cross, anything ambiguous).

Context page (text only, for the setup): PDF 99 (printed 2-74) discusses the rate tests (Figures 2-40 to 2-43) and the bin-size tests (Figure 2-44). Read it for understanding; nothing on it is a point.

## Lessons from earlier figures

1. A trace sample belongs on the drawn line's ink, never on a plotted symbol's outline or in the white gap between dashes or dots; a curve's first and last trace samples are where the line's ink starts and ends.
2. Check every printed axis label by eye against the line you anchor it to: a label printed off its line, or a frame that extends past the first or last labelled line, has misled readers before.
3. A thick line's center is known to within half its width: measure the width where you sample it and give that half-width as the bound, not a fixed number.
4. The description of a figure in this task is itself a reading and has been wrong before (it once said two traces cross twice where they cross once): trust the page, keep the ids given, and report every difference in notes.md.

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
