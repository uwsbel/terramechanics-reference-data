# Blind reading of Figure C-1B (direct shear data sheet), pilot batch curves-pilot-b1

You are one of two independent readers of a plotted figure from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of this figure. Work only
from the evidence packet in this workspace and the protocol it contains. Your output will be
compared cell by cell with the other reading; disagreements are settled from the page image, with
credit to whichever reading was right, so read carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. `p0117.png`: AM-68-1 Vol. II (NASA CR-92215), Figure C-1B, printed page C-3, PDF page 117,
   rendered at 300 dpi, unrotated. Pixel coordinates in everything you write refer to this image:
   `u` to the right, `v` downward, origin top-left.
2. `p0115.png`, `p0116.png`: the two pages before it (Appendix C introduction, Figure C-1A failure
   envelopes), for context.
3. `figures-rows.csv`: the figure's rows in the project's figures index (FC-1B and FC-1A).
4. `experiment-rows.csv`: the seven experiment rows these curves are evidence for (one direct
   shear test per normal stress: 294, 587, 1172, 1760, 2345, 2935, 3520 psf, RS soil at Dr .50 to
   .57). Use series ids `n294`, `n587`, `n1172`, `n1760`, `n2345`, `n2935`, `n3520`.
5. `CURVE-READING.md`: the reading protocol. Follow it. Its sections 2 and 3 define the files you
   produce and their columns.

## Tools (folder `tools/`)

Python interpreter with Pillow and NumPy: `<local path>`.

1. `tools/calibrate_axes.py detect <image> --box u0 v0 u1 v1 --x-values ... --y-values ... --out <dir>`
   locates the grid lines (tracked across narrow bands, because the scan is tilted by about a
   degree), fits an affine pixel-to-value map on the grid intersections and writes `anchors.csv`
   and `calibration.json`. Options: `--bands` (strips; 20 to 24 for a tall panel), `--min-frac`
   (dark fraction for a run; 0.35 works on this scan), `--snap` (pixels a line may move between
   bands; 6), `--frame-frac` (fraction of bands a line must span; 0.4 keeps a grid line that is
   hidden behind the legend for half its length). A line the tool could not find is marked
   `predicted`: check it on the image. Then `tools/calibrate_axes.py apply <calibration.json>
   <points.csv> <out.csv>` adds the printed-unit values and bounds.
2. `tools/plot_grid.py lines|crop|scan|overlay`: grid-line candidates in a box; a zoomed crop with
   a labeled pixel grid (read marker centers from these; zoom 3 or 4); a column scan listing the
   dark runs along chosen columns (center v and thickness; a drawn 12-px curve, a 6-px grid line,
   a marker blob); an overlay of your points on the page to check your own assignment.

You may write your own helper scripts; put them under `out/` too. Do not modify `tools/`.

## What to produce (write everything under `out/`)

1. `out/cal-p1/` and `out/cal-p2/`: the calibration of the upper panel (shear stress tau, psf,
   0 to 6000, versus shear displacement, thousandths of an inch, 0 to 250) and of the lower panel
   (dilation, thousandths of an inch, -100 to +100, same abscissa). Check at least three labels per
   axis by eye against the fitted positions and say so in the notes.
2. `out/points-p1.csv` and `out/points-p1-native.csv`: the seven drawn curves of the upper panel,
   sampled at least every 5 thousandths of displacement (your choice of columns; avoid the vertical
   grid-line columns), `point_kind = trace`, plus `feature` points (first point, peak, last point)
   for each curve, and the plotted markers if you can place them (`marker`, with `symbol`).
   Columns exactly as `CURVE-READING.md` section 3 lists them, `panel = 1`, `figure_id = FC-1B`.
3. `out/points-p2.csv` and `out/points-p2-native.csv`: every marker of the lower panel
   (`point_kind = marker`, with `symbol` in `x | asterisk | square | plus | triangle-down |
   triangle-up | circle` and the series it belongs to; the legend says "Same Notation As Above").
   Markers that overlap, sit on a grid line or could belong to two series get a wider bound and a
   note; a marker you cannot find gets a note saying which series and roughly where.
4. `out/overlay-p1.png`, `out/overlay-p2.png`: `plot_grid.py overlay` of your points on the page.
5. `out/notes.md`: your method (columns chosen, how you assigned runs to curves, how you identified
   symbols), the by-eye calibration checks, every ambiguity, and anything about the figure a later
   reader should know (where curves break, where markers hide each other, the legend entries as
   printed).

Finish with an answer that summarizes the counts (points per series and panel), the calibration
residuals, and the ambiguities, and lists the files written. Do not paste the full CSVs into the
answer; the files are the deliverable. Budget: about an hour.
