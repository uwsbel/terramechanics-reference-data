# Blind reading of Figure C-5B, Figure C-6B, Figure C-6C, Figure C-6D (direct shear data sheets), batch curves-appc-b3

You are one of two independent readers of plotted figures from a 1968 NASA report. The other
reader works elsewhere; you must not look for or use any other reading of these figures, nor any
earlier reading of a similar figure. Work only from the evidence packet in this workspace and the
protocol it contains. Your output will be compared cell by cell with the other reading;
disagreements are settled from the page image, with credit to whichever reading was right, so
read carefully and state your bounds honestly.

## Evidence packet (folder `packet/`)

1. Page images from AM-68-1 Vol. II (NASA CR-92215), Appendix C, rendered at 300 dpi, unrotated.
   Pixel coordinates in everything you write refer to these images: `u` to the right, `v`
   downward, origin top-left. The figures to read, one per page:
   - `p0130.png`: Figure C-5B (FC-5B), printed page C-16, SS soil, Dr .02 to .13 (gamma 95.2 to 97.6), 5 tests
   - `p0132.png`: Figure C-6B (FC-6B), printed page C-18, LSM soil, Dr .19 to .28 (gamma 71.1 to 73), 5 tests
   - `p0133.png`: Figure C-6C (FC-6C), printed page C-19, LSM soil, Dr 1.03 to 1.07 (gamma 91 to 93.3), 5 tests
   - `p0134.png`: Figure C-6D (FC-6D), printed page C-20, LSM soil, Dr .05 to .40 (gamma 66.8 to 75.2), 5 tests
   The other pages in the folder are context (the Appendix C introduction and the failure
   envelope figures these data sheets belong to).
2. `figures-rows.csv`: the figures' rows in the project's figures index (axes, units, legend as
   printed, notes from the inventory).
3. `series.csv`: the series of each figure, one per direct shear test, with the series id to use
   (`n<normal stress in psf as listed>`, for example `n4695`). The ids come from the project's
   figures index, which is itself a reading and has been wrong before: if the legend on the page
   prints a different number for a test, keep the id given but say so in notes.md with the number
   as printed (FC-6C lists 1961 and 714, FC-6D lists 3814 and 147: check them on the page). Every data sheet has two
   panels: shear stress (psf) versus shear displacement (thousandths of an inch) above, dilation
   displacement (thousandths of an inch) versus shear displacement below. The legend of each
   figure gives the symbol of each test; the lower panel uses the same symbols.
4. `CURVE-READING.md`: the reading protocol. Follow it. Its sections 2 and 3 define the files you
   produce and their columns.

## Two lessons from earlier figures of this kind (now rule 7 of the protocol)

1. A trace sample belongs on the drawn line's ink, never on a plotted symbol's outline or in the
   white gap between a dash and a symbol; a curve's first and last trace samples are where the
   line's ink starts and ends, not on the first or last symbol (that symbol is a marker).
2. Where small symbols stack in the lower panel, a symbol you cannot identify gets a note and a
   wide bound, never a guess.

## Tools (folder `tools/`)

Python interpreter with Pillow and NumPy: `<local path>`.

1. `tools/calibrate_axes.py detect <image> --box u0 v0 u1 v1 --x-values ... --y-values ... --out <dir>`
   locates the grid lines (tracked across narrow bands, because these scans are tilted by up to a
   degree), fits an affine pixel-to-value map on the grid intersections and writes `anchors.csv`
   and `calibration.json`. Options: `--bands` (strips; 20 to 24 for a tall panel), `--min-frac`
   (dark fraction for a run; 0.35 to 0.55), `--snap` (pixels a line may move between bands; 6),
   `--frame-frac` (fraction of bands a line must span; 0.4 keeps a grid line hidden behind the
   legend for half its length). A line the tool could not find is marked `predicted`: check it on
   the image. Then `tools/calibrate_axes.py apply <calibration.json> <points.csv> <out.csv>` adds
   the printed-unit values and bounds. Read the axis ranges off each page: they differ between
   figures (upper panels run to 5000, 6000 or 8000 psf; lower panels are -100 to +100 or -150 to
   +50 thousandths; check each one).
2. `tools/plot_grid.py lines|crop|scan|overlay`: grid-line candidates in a box; a zoomed crop with
   a labeled pixel grid (read marker centers from these; zoom 3 or 4); a column scan listing the
   dark runs along chosen columns (center v and thickness); an overlay of your points on the page
   to check your own assignment.

You may write your own helper scripts; put them under `out/` too. Do not modify `tools/`.

## What to produce (write everything under `out/<figure_id>/`, one folder per figure)

1. `cal-p1/` and `cal-p2/`: the calibration of the upper and lower panel. Check at least three
   labels per axis by eye against the fitted positions and record the checks in a
   `calibration-eye-checks.csv` (figure, panel, axis, printed label, fitted pixel, eye pixel).
2. `points-p1.csv` and `points-p1-native.csv`: for the upper panel, every plotted marker
   (`point_kind = marker`, with `symbol` and series), the drawn curve of every series sampled at
   least every 5 thousandths of displacement (`trace`; your choice of columns, avoid the vertical
   grid-line columns), and `feature` points (first point, peak, last point) per curve. Columns
   exactly as `CURVE-READING.md` section 3 lists them, `panel = 1`, `figure_id` as in the index.
3. `points-p2.csv` and `points-p2-native.csv`: every marker of the lower panel (`marker`, with
   `symbol` and series). Markers that overlap, sit on a grid line or could belong to two series
   get a wider bound and a note; a marker you cannot find gets a note saying which series and
   roughly where. Where a lower panel also has drawn lines through the markers, sample them as
   `trace` too.
4. `overlay-p1.png`, `overlay-p2.png`: `plot_grid.py overlay` of your points on the page.
5. `notes.md`: your method, the by-eye calibration checks, every ambiguity (curves that merge or
   share ink, doubled strokes, markers on gridlines or on the frame, points beyond the axis range,
   misprints in the legend), and anything about the figure a later reader should know.

Finish with an answer that summarizes, per figure, the counts (points per series and panel), the
calibration residuals, and the ambiguities, and lists the files written. Do not paste the full
CSVs into the answer; the files are the deliverable. Budget: about two hours for the four figures.
Work figure by figure and finish each one completely before starting the next, so that a partial
result is still usable.
