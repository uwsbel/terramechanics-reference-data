# FA-48, blind reading (Claude), batch curves-appa-b1

Page `p0097.png` (printed A-96). Caption as printed: "Figure A-48. Angle of Internal Friction (as
determined by the direct shear test) Versus Relative Density for RSM Soil". It matches the figures
index title. The soil is printed as "RSM"; the `RSM-b` in `series.csv` is the index's name and is
not printed on the page. One panel, upright, full grid, one solid curve, no symbols, no legend.
Series id `curve`.

## Calibration (`cal-p1/`)

1. `tools/calibrate_axes.py detect`, box u 770 to 2400, v 1430 to 3350, 10 bands, x values 0 to 1.0
   by 0.2 (left frame to right frame), y values 30 to 50 by 5.
2. The top frame (v about 1242) and the bottom frame (v about 3536) carry no printed labels (by
   spacing they would be 55 and 25), so they are outside the box and are not anchors.
3. All 11 lines detected in 10 of 10 bands; none predicted. Affine residuals: x RMS 0.0031, max
   0.0062, which is 0.62 percent of the 0 to 1 span, above the 0.5 percent threshold; y RMS 0.039
   deg, max 0.066 deg (0.19 and 0.33 percent of the 20 deg anchored span).
4. The x residual is the drawing, not the detection: the vertical lines are unevenly spaced (at
   v 2400: 306, 311, 300, 319, 316 px from left to right), the ink check puts every line within
   0.63 px of its ink, and three other boxes, band counts and thresholds (6, 10 and 14 bands; dark
   200 and 160) all give the same x RMS 0.003 and max 0.006. The values come from the piecewise
   map between the verified lines, which follows the uneven spacing, so the box was kept.
5. Piecewise ink check (`cal-p1/knots-ink-check.json`): all 6 x lines and all 5 y lines verified,
   ink found at every position; location errors 0.50 to 1.04 px. The y = 50 line has a break at
   u 1214 to 1247 (24 columns without ink), far from the curve; it was still detected in all bands.
6. Labels checked by eye (`calibration-eye-checks.csv`): all five y labels and all six x labels.
   The y labels sit 4 to 8 px above their lines; the x decimal points are within 7 px of their
   lines; the "0" is about 14 px left of the left frame. No label is closer to a different line.

## Points (`points-p1.csv`, `points-p1-native.csv`)

1. `curve`: 21 trace samples (left end, Dr 0.05 to 0.95 every 0.05, right end) and 2 features.
   Bounds 6 px in u and v (the line is 11 to 12.7 px thick across it).
2. Samples located with `helpers/trace.py --open 7 --tol 2`: dark mask (gray below 160) opened with
   a 7 px square, column runs followed from the left end, columns where a grid line joins the curve
   (run more than 2 px longer than the local median) not used, the centre at the target Dr a
   straight line fitted to the clean columns within 8 px. Samples at Dr 0.2, 0.4, 0.6, 0.8 sit on
   vertical grid lines and come from the curve on either side.
3. Dr 0.85: the drawn line has a joint between two strokes from u 2093 to 2118 where it is only
   about 6 px tall and its lower part is missing (`crop-dr085.png`). The sample is the centre of
   that thin ink, read on the raw mask (v 1667.0); the strokes on either side extrapolate to v 1670
   to 1671.5 there, inside the 6 px bound. The slopes either side of the joint agree (-0.49 and
   -0.44 px per px), so it is a drafting joint, not a kink.
4. Left end: the curve runs into the left frame (frame ink u 791 to 799); first column clear of the
   frame u 802, v 2539.5 (Dr 0.004, phi 38.17 deg), with a u bound of 7 px reaching the frame
   centre.
5. Right end: the curve runs into the right frame (frame ink u 2334 to 2342); last column clear of
   the frame u 2332, v 1570.0 (Dr 0.996, phi 50.63 deg), u bound 6 px reaching the frame centre.
6. The curve crosses the y = 50 line at about Dr 0.92. The sample at Dr 0.95 (50.25 deg) and the
   right end (50.63 deg) lie above the highest labelled line and are flagged `extrapolated y` by
   `piecewise` (by at most 50 px, under a quarter of a grid interval; the unlabelled top frame is
   not used). The left end is flagged `extrapolated x` only because its u bound reaches the frame.
7. Features: first point and last point. The curve rises monotonically, so its maximum is the last
   point. Its slope changes smoothly (steepest near Dr 0.45 to 0.65, flatter beyond 0.8); no knee or
   kink, so no knee feature.

## Ambiguities

1. The two ends are hidden in the frame ink; either could be anywhere from the first clear column
   to the frame centre (Dr change under 0.005, phi change under 0.05 deg).
2. The Dr 0.85 sample sits on a thin joint of the drawn line (point 3 above).
3. Specks in the plot, not symbols: dots of 6 to 7 px at u 1174, v 2558 (Dr 0.25, phi 37.9), u 1230,
   v 2218 (Dr 0.28, phi 42.3) and u 1309, v 2553 (Dr 0.33, phi 38.0).

## Files

`cal-p1/` (anchors.csv, calibration.json, knots-ink-check.json), `calibration-eye-checks.csv`,
`points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`, crops (`crop-*.png`, `eye-*.png`,
`check-*.png`), helpers in `helpers/`.
