# Blind reading of one direct shear data sheet (Appendix C, AM-68-1 Vol. II)

You are one of two independent readers of a plotted figure from a 1968 NASA report. The other
reader works elsewhere. Your reading will be compared cell by cell with the other one;
disagreements are settled from the page image, with credit to whichever reading was right. So:
read carefully, state your bounds honestly, and never guess a point you cannot see.

## Blindness rules (strict)

1. Work ONLY inside your workspace folder (given in your task). Everything you need is there:
   `packet/` (the page images, the figure's index row, the series list, the protocol
   `CURVE-READING.md`), `tools/` (two Python scripts), `out/` (write everything here).
2. Do NOT open, read, grep or list anything under
   `<repository>` (the project repository) or under
   `<local path>`. Do not look for any earlier reading of
   this or any similar figure. If you catch yourself about to, stop.
3. Do not modify `tools/`. Helper scripts you write go under `out/`.

## Environment

Python with Pillow and NumPy: `<local path>`. Set
`PYTHONIOENCODING=utf-8`. Use the Bash tool with forward slashes. You can look at any PNG with the
Read tool; that is how you read marker centers by eye: make zoomed crops with
`tools/plot_grid.py crop` (zoom 3 or 4, labeled pixel grid) and read them.

## The figure

A data sheet with two panels on one page, 300 dpi, unrotated. Pixel coordinates: `u` to the
right, `v` downward, origin top-left of the page image. Upper panel: shear stress (psf) versus
shear displacement (thousandths of an inch). Lower panel: dilation displacement (thousandths of
an inch) versus the same shear displacement. One series per direct shear test; `packet/series.csv`
gives the series ids (`n<normal stress psf as printed>`) and the legend on the page gives each
test's symbol. The lower panel uses the same symbols. Read the axis ranges off the page (upper
panels run to 5000, 6000 or 8000 psf; lower panels are -100 to +100 or -150 to +50).

## Tools

1. `tools/calibrate_axes.py detect <image> --box u0 v0 u1 v1 --x-values ... --y-values ... --out <dir>`
   locates the grid lines in narrow bands (the scans are tilted by up to a degree), fits an
   affine pixel-to-value map on the grid intersections and writes `anchors.csv` and
   `calibration.json`. Options: `--bands` (20 to 24 for a tall panel), `--min-frac` (0.35 to
   0.55), `--snap` (6), `--frame-frac` (0.4 keeps a grid line hidden behind the legend). A line
   marked `predicted` was interpolated: check it on the image. Then
   `tools/calibrate_axes.py apply <calibration.json> <points.csv> <out.csv>` adds the
   printed-unit values and bounds (the `-native.csv` files).
2. `tools/plot_grid.py lines|crop|scan|overlay`: grid-line candidates in a box; a zoomed crop
   with a labeled pixel grid; a column scan listing the dark runs along chosen columns (center v
   and thickness); an overlay of your points on the page to check your own assignment.

Run each script with `--help` first to see its exact arguments.

## Method (follow `packet/CURVE-READING.md`; this is the short form)

1. Calibrate each panel: choose the box around the plot frame, run `detect` with the printed
   gridline values, check at least three labels per axis by eye against the fitted pixel
   positions, and record those checks in `out/<FIG>/calibration-eye-checks.csv` (figure, panel,
   axis, printed label, fitted pixel, eye pixel). Residual above 0.5 percent of the axis span:
   fix the box or thresholds before reading any point.
2. Markers first. Every plotted symbol in both panels is a point: `point_kind = marker`, with
   `symbol` (`x | asterisk | square | plus | triangle-down | triangle-up | circle`) and its
   series. Read centers from zoomed crops. Clean marker: bound 2 px. Overlapping markers, a
   marker on a gridline or on the frame, a symbol that could belong to two series: wider bound
   and a `note`. A marker you cannot find: a row with a note saying which series and roughly
   where, or omit it and say so in `notes.md`.
3. Traces: sample the drawn curve of every upper-panel series at least every 5 thousandths of
   displacement (`trace`), at columns of your choice away from vertical gridlines, in drawing
   order (`sequence` 1 up, never sorted by x if a curve doubles back). Bound: half the line
   thickness. `tools/plot_grid.py scan` lists the dark runs along a column; assign runs to series
   by following each curve from its markers. Where two curves merge or share ink, say so in the
   note and widen the bound. Where the lower panel also has drawn lines through its markers,
   sample them too.
4. Features: for every upper-panel curve, `feature` points for the first point, the peak (of the
   drawn line, not of the markers) and the last point.
5. Columns of `points-p<n>.csv`, exactly: `figure_id, panel, series_id, point_kind, sequence,
   pixel_u, pixel_v, u_bound_px, v_bound_px, symbol, note`. `panel` is 1 (upper) or 2 (lower).
   Then `apply` the calibration to get `points-p<n>-native.csv`.
6. Overlay your points on the page (`plot_grid.py overlay`) as `overlay-p1.png`,
   `overlay-p2.png`, look at them with the Read tool, and fix what is wrong before finishing.

## Deliverables, all under `out/<FIG>/`

`cal-p1/`, `cal-p2/`, `calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`,
`points-p2.csv`, `points-p2-native.csv`, `overlay-p1.png`, `overlay-p2.png`, `notes.md` (your
method, the eye checks, every ambiguity: merging curves, doubled strokes, markers on gridlines or
the frame, points beyond the axis range, legend misprints, and anything a later reader should
know), plus any helper scripts you wrote.

Finish with a short report: per panel, points per series by kind; calibration residuals; the
ambiguities; the files written. Do not paste CSV contents into the report. Take the time the
figure needs; a complete, honest reading matters more than speed, but do not polish beyond what
the protocol asks.
