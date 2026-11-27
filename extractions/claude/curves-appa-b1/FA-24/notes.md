# FA-24, panel 1: reading notes (Claude, blind, batch curves-appa-b1)

Page `p0049.png` (printed A-48). Caption as printed: "Figure A-24. Angle of Internal Friction (as
determined by the direct shear test) Versus Relative Density for the RC2 Soil" (the scan shows the
first letter of "Figure" as "E", a print defect). Axis titles: "Angle of Internal Friction, phi,
(Degrees)" and "Relative Density, Dr". One panel, upright, full grid, one solid curve, no symbols, no
legend. Series id `curve` as given in `series.csv`; the page agrees with it.

## Calibration (`cal-p1/`)

1. **The frame extends one grid interval past the labelled lines at both ends of y.** Printed y
   labels: 30, 35, 40, 45, 50, each on an interior line. The top frame (v 1226) and the bottom frame
   (v 3531) carry no label. Only the labelled lines are anchored: `calibrate_axes.py detect`, box
   u 760..2360, v 1450..3330 (between each frame and the nearest labelled line), 9 bands, x values 0,
   0.2, ..., 1.0 (left frame to right frame, both labelled), y values 30, 35, 40, 45, 50.
2. All 11 lines detected in 9 of 9 bands, none predicted. Affine residuals: x rms 0.002 (0.2 %),
   max 0.004 (0.4 %); y rms 0.027 deg (0.13 % of the 30 to 50 span), max 0.048 deg (0.24 %).
3. Ink check (`cal-p1/knots-check.json`): every line verified, ink at 12 of 12 (x) and 15 of 15 (y)
   positions; location errors 0.50 to 1.26 px (largest: the right frame, its ink line 1.03 px off the
   fitted line at one end).
4. Grid spacing at mid-height: 305.9, 307.4, 306.0, 318.8 and 309.4 px per 0.2 of Dr (the 0.6 to 0.8
   interval is the widest); 385.5, 388.9, 383.1 and 381.2 px per 5 deg (50 to 30). Affine minus
   piecewise on the trace: up to 0.004 in Dr and 0.02 deg (`cal-p1/points-p1-affine.csv`).
5. Labels checked by eye: all five y labels and all six x labels (`calibration-eye-checks.csv`), each
   on the line it is anchored to. The x labels "0" and "1.0" are printed 9 px right of their frame
   lines; a dashed rule printed after "0.2" and a dotted leader at v 2187 left of the frame are print
   artefacts.

## Extrapolation above y = 50

The curve crosses the 50 line at about Dr 0.72 and ends at phi 52.9. Every point above the 50 line
(trace samples Dr 0.75 to 0.95 and the right end, the second knee and the last-point feature: 8
rows) is flagged `extrapolated y` in `points-p1-native.csv`: its value comes from the 45 to 50 interval carried past the 50 line.
Cross-check, not used as an anchor: the same map puts the unlabelled top frame at 54.94 to 54.98
(the frame lies 382 px above the 50 line against 386 px for 45 to 50). If that frame is 55, the
extrapolation error at the curve's highest point (about 214 px above the 50 line) is about 0.03 deg,
well inside the read bounds (0.09 to 0.11 deg).

## Trace (`points-p1.csv`, `points-p1-native.csv`)

1. Method (`out/trace_curve.py columns`), u 791 to 2327 (1537 columns): 1411 clean, 58 with one edge
   merged into the y = 45 or y = 50 line (centre from the free edge and the local vertical
   thickness), 31 inside the 0.2, 0.4, 0.6 and 0.8 vertical lines (samples interpolated between the
   clean columns either side, 8 to 9 px apart; the curve's ink runs through), 37 marked `break`.
2. White breaks in the curve's ink (print defects), columns not used (`out/mark_breaks.py`): a notch
   in the lower half at u 852 to 859 (Dr 0.04); holes where the curve crosses the 50 line, u 1915 to
   1921 (Dr 0.74); a diagonal crack across the whole line at u 2179 to 2200 (Dr 0.90 to 0.91). Across
   the crack, straight lines fitted on either side agree within 1.2 px at u 2190 and one quadratic fits
   both sides with rms 0.67 px: a crack, not a drawn jog. No sample falls in a break: Dr 0.05 is at u
   861.5, Dr 0.90 at u 2177.6, on clean columns of normal thickness.
3. Stray marks near the curve, not part of it: specks below the y = 45 line at u 1215 to 1230 and a
   blob on the right of the 0.6 vertical line at v 1735 to 1740, both separated from the curve by
   white.
4. Samples: the left end, Dr 0.05 to 0.95 every 0.05 (19), the right end: 21 trace samples. Bound
   6.0 px in u and v (half of a perpendicular line thickness of 10.4 to 11.5 px, median 11.2).
5. Ends: the curve's ink runs into both frame lines, nothing beyond them. First sample at the left
   frame's inner edge, u 790.5 (frame ink 780 to 790, centre 785.0), v 2145.0: Dr 0.004, phi 43.03.
   Last sample at the right frame's inner edge, u 2327.5 (frame ink 2328 to 2337, centre 2332.6),
   v 1386.8: Dr 0.997, phi 52.89 (extrapolated y). The ends are flagged `extrapolated x` because their
   u bound reaches the frame line's centre.
6. Shape (slopes between successive samples, deg per unit Dr): an S-shaped curve. Concave up from
   the left end, 5.0, 5.8, 7.2, 8.4, 9.3 to 10.1 at Dr 0.25 to 0.30; nearly straight, 10.4 to 12.2,
   steepening slowly from Dr 0.30 to 0.80; then a shoulder, 11.1, 10.1, 10.0 and 8.4 over the last
   0.05.

## Features

1. First point and last point as the trace ends above.
2. Knee rule (the same for every figure Claude read in this batch): straight stretches of the traced
   centre are fitted (`out/stretch_slopes.py`); where the slopes of the stretches on either side of a
   bend differ by 20 % or more of the steeper, the bend is a knee, placed at the curvature-weighted
   centroid of the bend between them (`out/curvature.py`, `out/bend_centroid.py`, quadratic fits over
   120 px windows), with bounds 80 px in u (about 0.05 in Dr) and |slope| x 80 px + half the line
   thickness in v. Both bends here are gradual; neither is a kink.
3. Knee 1, the toe: u 1052, v 2062.5 (Dr 0.175, phi 44.10; read bounds 0.053, 0.52 deg). Straight
   stretches dv/du -0.276 (u 791 to 900) and -0.524 (u 1230 to 1430), a 47 % change; the curvature is
   spread almost evenly over u 850 to 1210 (Dr 0.04 to 0.27), so the knee's position is soft.
4. Knee 2, the shoulder: u 2157, v 1465.0 (Dr 0.887, phi 51.87, extrapolated y; read bounds 0.052,
   0.64 deg). Straight stretches dv/du -0.572 (u 1600 to 2020) and -0.417 (u 2250 to 2327), a 27 %
   change; curvature peak at u 2235 (Dr 0.94). On clean ink just left of the crack.
5. Not recorded: the slow steepening between the toe and the shoulder (-0.524 to -0.572, 8 %).

## Ambiguities

1. Both knees sit on spread-out bends; the toe could be placed anywhere from Dr 0.05 to 0.27 and the
   shoulder from Dr 0.80 to 0.95.
2. The shoulder's straight stretch after the bend is short (u 2250 to 2327, 77 px), so its slope,
   and with it the 27 %, rests on little ink.
3. Values above 50 depend on extrapolation (see above); the top frame was not anchored because it
   carries no printed value.

## Files

`cal-p1/` (anchors.csv, calibration.json, knots-check.json, points-p1-affine.csv),
`calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`,
`points-spec-p1.json` (ends, knees and bounds fed to `out/build_points.py`), `columns-p1.csv` and
`columns-p1-inframe.csv` (traced columns; the latter clipped to the frame and with the break columns
marked), `crops/`.
