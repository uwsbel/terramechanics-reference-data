# FC-19, blind reading (Claude), batch curves-appc-b10

Figure C-19, "Angle of Internal Friction vs. Relative Density", printed page C-41, page image
`p0155.png` (3213 x 4558 px, 300 dpi, upright). One panel. Legend text inside the plot: "RC2 Soil"
(with a short underline running right from it to about u 1420, v 1487; not traced). Axis titles:
y "phi_DS - Degrees", x "D_r". What is printed matches `series.csv`: open circles, one solid curve,
two dashed curves, soil RC2.

## Calibration (`cal-p1/`)

1. `tools/calibrate_axes.py detect` with box u 860..2600, v 1450..3400 (inside the frame, so the
   frame lines are not taken as the first and last values), x values 0, 0.1, ..., 1.0, y values 30,
   35, 40, 45, 50, `--bands 10`. All 11 vertical and 5 horizontal lines detected in 10 of 10 bands;
   no `predicted` line.
2. Affine residuals: x RMS 0.0014, max 0.0029 (0.29 percent of the labelled span 1.0); y RMS 0.016
   deg, max 0.035 deg (0.17 percent of the labelled span 20 deg). Grid drafted unevenly in x (153 to
   162 px per 0.1), which the piecewise map takes as drawn. Lines tilt about 0.8 degrees (vertical
   lines du/dv +0.011 to +0.015, horizontal dv/du -0.007 to -0.010).
3. Ink check (`piecewise --image`, record in `cal-p1/knots-check.json`): all 16 lines verified,
   none rejected; ink found at 12 of 12 positions on every x line and 25 of 25 on every y line; the
   reader's lines are within 0.7 px of the ink's line at both ends; location errors 0.5 to 1.3 px.
4. By-eye label checks: all 11 x labels and all 5 y labels checked on zoomed crops
   (`crops/ylab*.png`, `crops/xlabA.png`, `crops/xlabB.png`), each label sitting at its own line
   (y labels within 6 px of the line they name, line spacing 383 px; x labels within 16 px, line
   spacing 153 to 162 px; the "0.4" label is printed 16 px left of its line, still unambiguous).
   See `calibration-eye-checks.csv`.
5. The frame extends beyond the labelled lines on all four sides, unlabelled: left frame at Dr
   -0.093, right frame at Dr 1.099, bottom frame at 24.97 deg, top frame at 55.0 deg (affine
   extrapolation, measured at four places each). The frame lines are not knots (no printed value).
   As a result every value above the y = 50 line (the upper parts of all three curves and the right
   circle) is flagged `piecewise extrapolated y` in `points-p1-native.csv` (30 of 73 rows); the
   samples right of the x = 1.0 line and the left ends at the x = 0 line are flagged extrapolated in
   x (by at most 0.007 in Dr). Largest difference affine minus piecewise: 0.0024 in Dr, 0.06 deg.

## Which curve is which

1. `mean`: the only solid curve, the middle one; from the left circle (Dr about 0, 42.85 deg) to
   the x = 1.0 grid line (52.85 deg). S-shaped: flatter at the left, steepest near Dr 0.5, flatter
   again at the right; no knee or kink.
2. `upper`: dashed, above the solid curve; 8 dashes; 44.23 deg at its left end (Dr 0.00) to
   53.87 deg at its right end (Dr 1.004).
3. `lower`: dashed, below the solid curve; 8 dashes; 41.52 deg at its left end (Dr 0.00) to
   51.69 deg at its right end (Dr 1.007).

No curve crosses or touches another.

## Markers (series `data`)

1. Circle 1 at Dr 0.006, 42.97 deg: "single". The x = 0 grid line runs through its left part and the
   solid curve passes through the lower half of its hole (the curve's ink is visible inside the ring
   from u 969 and thickens the bottom of the ring to 14 px against 7 px at the top), so the center is
   taken from the ring's outer extents (u 953 to 989, v 2195 to 2233) and the bound widened to 3 px.
2. Circle 2 at Dr 0.951, 53.00 deg: "single", clean, between the upper dashed curve and the solid
   curve, touching neither.

No circle is cut by the frame. No pair of circles is joined by a horizontal line on this figure.

## Short horizontal strokes (not joining lines, not traced)

Several short horizontal strokes appear, none with a circle at either end:

1. u 1028 to 1113, v about 2107: a thin stroke leaving the first upper dash and running right to the
   x = 0.1 grid line.
2. u 1071 to 1112, v about 2313: a broken stroke just below the first lower dash, ending at the
   x = 0.1 grid line.
3. u 1870 to 1897, v about 1906: a stroke along the lower edge of the start of the lower dash at
   Dr 0.58, ending at the x = 0.6 grid line.
4. u 2459 to 2480, v about 1385: a spur off the last upper dash, just above circle 2.
5. Isolated dashes or specks at about (1448, 1781), (2099, 1567), (1707, 2175), (1646, 1825),
   (1657, 1923), and a 2 px dot at (2001, 1837) just right of the end of the lower dash at u 1993.

They may be drafting remnants; they carry no symbol and are left out of every series. Worth a look
by the adjudicator in case one of them is meant as data.

## Traces

1. Centerline per column from the ink (helpers `centerline.py`, `sample.py`): grid lines masked,
   runs touching a masked grid line set aside, a robust fit per dash rejects stray ink; the line's
   v at a sample is a local straight fit over the clean columns within 12 px (24 px where the
   curve crosses a grid line intersection).
2. Samples at the left end, every 0.05 of Dr placed with the piecewise x map, and the right end.
   Samples on a vertical grid line (Dr 0.1, 0.2, ...) are where the drawn line passes through the
   grid line, read from its ink on both sides; noted per row.
3. Dashed curves, rule 7: a 0.05 sample falling in a gap moves to the nearest dash end, on the ink,
   1.5 px inside the dash's last column. Moved: upper at Dr 0.10, 0.25, 0.50, 0.65, 0.90; lower at
   Dr 0.40, 0.55, 0.80, 0.90. Their x values are therefore not multiples of 0.05 (for example
   0.0919, 0.2619). Dash extents were checked on pixel dumps; the three dash ends closest to a grid
   line (upper at u 1728, lower at u 1572 and u 2347) stop 3 px or more short of it, so they are
   real ends, not hidden in a grid line.
4. Bounds: half the line thickness. Vertical runs are 9 px, perpendicular thickness 7.6 to 8.0 px,
   bound 4.0 px (mean, lower) and 4.5 px (upper) in u and v.
5. Counts: mean 21 trace (left end, Dr 0.05 to 0.95, right end; the Dr 0.00 and 1.00 samples are the
   ends), upper 22 and lower 22 (left end at Dr 0.00, Dr 0.05 to 1.00, right end just past 1.0).

## Ends (features, rule 3: first and last point; the last point is also the maximum; no knee)

1. `mean` first point (u 965, v 2223.5, bounds 4 and 5 px): the line's start is hidden. Its ink is
   visible inside circle 1 from u 969, and further left it merges with the ring and the x = 0 grid
   line (u about 961). The point is placed in the middle of that stretch, with a bound covering it.
   Ambiguous: whether the solid curve starts at Dr 0 or somewhere under the circle cannot be told.
2. `mean` last point (u 2507.5, v 1439, bounds 3 and 5 px): the line runs into the x = 1.0 grid line
   (grid ink u 2507 to 2510) and no ink appears right of it, so the end is in the grid line. The
   bound covers it.
3. `upper` first point (u 961, v 2118): the first dash begins at the x = 0 grid line, merging with it;
   no ink to the left. Last point (u 2514, v 1360): the last dash crosses the x = 1.0 grid line and
   ends 5 px past it.
4. `lower` first point (u 963.5, v 2325.5): begins at the x = 0 grid line, merging with it. Last
   point (u 2521, v 1529): the last dash crosses the x = 1.0 grid line and ends 10 px past it.

## Files

1. `cal-p1/calibration.json`, `cal-p1/anchors.csv`, `cal-p1/knots-check.json`
2. `calibration-eye-checks.csv`
3. `points-p1.csv` (reader's pixels, bounds, notes) and `points-p1-native.csv` (same rows with
   `x_native`, `y_native`, `x_read_bound`, `y_read_bound`, `cal_model` from
   `tools/calibrate_axes.py piecewise --image`)
4. `overlay-p1.png` (points over the figure, box u 760..2740, v 1240..3720)
5. `crops/` (zoomed crops used for the reading), `helpers/` (centerline.py, sample.py,
   eye_checks.py, the per-column centerlines, and affine-check.csv for the affine comparison)
