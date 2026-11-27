# FA-4, panel 1: reading notes (Claude, blind, batch curves-appa-b1)

Page `p0009.png` (printed A-8). Caption as printed: "Figure A-4. Angle of Internal Friction (as
determined by the direct shear test) Versus Relative Density for RS Soil". Axis titles: "Angle of
Internal Friction phi, (Degrees)" and "Relative Density, Dr". One panel, upright, full grid, one solid
curve, no symbols, no legend. Series id `curve` as given in `series.csv`; the page agrees with it.

## Calibration (`cal-p1/`)

1. `calibrate_axes.py detect`, box u 805..2405, v 1365..3100, 9 bands, x values 0, 0.2, ..., 1.0
   (left frame to right frame), y values 30, 35, 40, 45, 50 (the 30 line to the top frame).
2. The bottom frame line (v about 3309, one grid interval below 30, so presumably 25) carries no
   printed label. It is left out of the box and of the map. The curve never goes below y = 40, so
   nothing is read near it.
3. All 11 lines detected in 9 of 9 bands, none predicted. Affine residuals: x rms 0.002 (0.2 % of the
   0 to 1 span), max 0.004 (0.4 %); y rms 0.023 deg (0.12 % of the 30 to 50 span), max 0.035 deg.
4. Ink check (`cal-p1/knots-check.json`, from `out/knots_check.py`, which calls the tool's own
   `piecewise_maps` with the page): every line verified, ink found at 12 of 12 (x) and 15 of 15 (y)
   positions, offsets of the reader's line from the ink's line at its ends 0.6 px or less, location
   errors 0.56 to 1.10 px.
5. The grid is drafted unevenly in x: 305, 309, 307, 321 and 312 px per 0.2 (the 0.6 to 0.8 interval
   is the widest). The piecewise map reads it as drawn; the affine map differs from it by up to 0.004
   in Dr and 0.02 deg in phi on the trace (`cal-p1/points-p1-affine.csv`).
6. Labels checked by eye: all five y labels and all six x labels (`calibration-eye-checks.csv`). Each
   sits on the line it is anchored to. The top label reads 50: its first glyph has a squared top that
   looks like a 6 at low zoom, but its left side is open below the bowl, the same 5 as in 35 and 45,
   and 50 continues the 30, 35, 40, 45 sequence.

## Trace (`points-p1.csv`, `points-p1-native.csv`)

1. Method (`out/trace_curve.py columns`): the curve's ink run is followed column by column from
   u 839 to 2382 (1544 columns): 1462 clean, 51 with one edge merged into a horizontal grid line
   (centre from the free edge and the local vertical thickness), 31 inside the 0.2, 0.4, 0.6 and 0.8
   vertical lines (the curve's ink runs through them unbroken; samples there are interpolated between
   the clean columns 8 to 10 px apart either side). `out/cols_check.py`: 4 columns depart from the
   local trend by more than 2 px or 3 px of thickness (stray ink at u 1134, 1852, 2183, 2184); none
   is used by a sample.
2. Samples: the left end, Dr 0.05 to 0.95 every 0.05 (19), the right end: 21 trace samples. Values
   by the piecewise map.
3. Line thickness: vertical run 12 to 15 px, about 12.5 px across the line. Bound 6.5 px in u and v
   (half the thickness, rule 7); 7.5 px in v where the centre came from one edge (the left end and
   Dr 0.50, where the curve meets the y = 40 and y = 45 lines).
4. Ends. The curve's ink runs into both frame lines; nothing beyond them. First sample at the left
   frame's inner edge, u 838.5 (frame ink u 828 to 838, centre 832.5), v 2145.5: Dr 0.004, phi 40.08.
   Here the curve's bottom edge lies on the y = 40 grid line. Last sample at the right frame's inner
   edge, u 2382.5 (frame ink 2384 to 2393), v 1501.0: Dr 0.996, phi 48.59. Both are flagged
   `extrapolated x` because their u bound reaches past the frame line's centre, which is meant: the
   curve's own ink is hidden inside the frame.
5. Shape (slopes between successive samples): straight from the left end to Dr 0.40, 9.5 over the first 0.05 (one-edge centre at the end), then 9.9 to 10.3
   deg per unit Dr (dv/du -0.50 within 0.02); a gradual bend, 9.0 to 9.3 from Dr 0.40 to 0.50, 8.2 and
   7.6 to Dr 0.60; 6.8 to 6.9 from Dr 0.60 to 0.85; then steepening slightly, 7.4 to 7.9, to Dr 1.0.

## Features

1. First point and last point as the trace ends above.
2. Knee rule (the same for every figure Claude read in this batch): straight stretches of the traced
   centre are fitted (`out/stretch_slopes.py`); where the slopes of the stretches on either side of a
   bend differ by 20 % or more of the steeper, the bend is a knee, placed at the curvature-weighted
   centroid of the bend between them (`out/curvature.py`, `out/bend_centroid.py`, quadratic fits over
   120 px windows), with bounds 80 px in u (about 0.05 in Dr) and |slope| x 80 px + half the line
   thickness in v.
3. Knee: one, at u 1645, v 1756.0 (Dr 0.527, phi 45.19; read bounds 0.053 in Dr, 0.54 deg), on the
   ink just right of where the curve crosses the y = 45 line. A gradual bend, not a kink: straight
   stretches dv/du -0.496 (u 850 to 1440, rms 0.6 px) and -0.318 (u 1800 to 2050), a 36 % change;
   the curvature peaks at u 1650; a single-breakpoint two-segment fit would put it at u 1610 (rms
   1.8 px against 16.8 px for one line).
4. Not recorded: the gentle steepening over the last quarter (straight stretch u 2200 to 2380 at
   dv/du -0.374 against -0.318 before it, 15 %).

## Ambiguities

1. The knee position is a judgement on a smooth bend; another reader may place it anywhere from
   Dr 0.40 to 0.60, hence the wide bounds.
2. Whether the drawn curve "starts" at Dr 0 or at the frame's inner edge cannot be told from the ink
   (it is inside the 9 px frame line); the first sample's u bound covers both.

## Files

`cal-p1/` (anchors.csv, calibration.json, knots-check.json, points-p1-affine.csv),
`calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`,
`points-spec-p1.json` (ends, knee and bounds fed to `out/build_points.py`), `columns-p1.csv` and
`columns-p1-inframe.csv` (the traced columns), `crops/`.
