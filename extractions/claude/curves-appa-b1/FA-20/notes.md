# FA-20, panel 1: reading notes (Claude, blind, batch curves-appa-b1)

Page `p0041.png` (printed A-40). Caption as printed: "Figure A-20. Angle of Internal Friction (as
determined by the direct shear test) Versus Relative Density for RSM Soil". Axis titles: "Angle of
Internal Friction, phi, (Degrees)" and "Relative Density, Dr". One panel, upright, full grid, one solid
curve, no symbols, no legend. Series id `curve` as given in `series.csv`. The caption prints "RSM";
the index's soil `RSM-a` is its own identifier and the page gives no suffix.

## Calibration (`cal-p1/`)

1. `calibrate_axes.py detect`, box u 790..2380, v 1470..3220, 9 bands, x values 0, 0.2, ..., 1.0
   (left frame to right frame), y values 30, 35, 40, 45, 50 (the 30 line to the top frame).
2. The bottom frame line (v about 3412, one interval below 30) carries no printed label; it is left
   out of the box and of the map. The curve never goes below y = 36.8.
3. All 11 lines detected in 9 of 9 bands, none predicted. Affine residuals: x rms 0.002 (0.2 %), max
   0.003 (0.3 %); y rms 0.023 deg (0.12 % of the 30 to 50 span), max 0.048 deg (0.24 %).
4. Ink check (`cal-p1/knots-check.json`): every line verified, ink at 12 of 12 (x) and 15 of 15 (y)
   positions. Location errors 0.50 to 0.91 px, except the right frame (x = 1.0) at 1.58 px (its ink
   line is 0.96 px off the fitted line at one end, scatter 0.61 px).
5. Grid spacing: 302.1, 308.5, 312.4, 313.3 and 309.0 px per 0.2 of Dr; 383.4, 389.6, 380.4 and
   382.0 px per 5 deg (50 to 30). The piecewise map reads it as drawn; affine minus piecewise on the
   trace: up to 0.003 in Dr and 0.044 deg (`cal-p1/points-p1-affine.csv`).
6. Labels checked by eye: all five y labels and all six x labels (`calibration-eye-checks.csv`). The
   x label "0" is printed 17 px right of the left frame line it labels (no other line within 280 px);
   the other x labels sit 2 to 7 px from their lines.

## Trace (`points-p1.csv`, `points-p1-native.csv`)

1. Method (`out/trace_curve.py columns`), u 818 to 2352 (1535 columns): 1407 clean, 73 with one
   edge merged into the y = 40 or y = 45 line (centre from the free edge and the local vertical
   thickness), 31 inside the 0.2, 0.4, 0.6 and 0.8 vertical lines (samples interpolated between the
   clean columns either side, 8 to 10 px apart; the curve's ink runs through), 24 marked `break`.
2. White breaks and holes in the curve's ink (print defects; the ink continues at the same level on
   both sides), columns not used (`out/mark_breaks.py`): u 876 to 884 (Dr 0.04), 1609 to 1618
   (Dr 0.54), 2117 to 2121 (Dr 0.85). No sample falls in them: Dr 0.05 is at u 887.4, 0.55 at
   1655.2, 0.85 at 2125.6, all on clean columns of normal thickness.
3. Samples: the left end, Dr 0.05 to 0.95 every 0.05 (19), the right end: 21 trace samples. Bound
   6.0 px in u and v (half of a perpendicular line thickness of 11.1 to 12.6 px, median 11.9); 7.0 px
   in v at Dr 0.30, where the curve crosses the y = 40 line and its centre came from one edge.
4. Ends: the curve's ink runs into both frame lines, nothing beyond them. First sample at the left
   frame's inner edge, u 817.5 (frame ink 806 to 816, centre 811.6), v 2504.8: Dr 0.004, phi 36.86.
   Last sample at the right frame's inner edge, u 2352.5 (frame ink 2353 to 2361, centre 2357.2),
   v 1765.3: Dr 0.997, phi 46.48. Both flagged `extrapolated x` because their u bound reaches the frame
   line's centre.
5. Shape (slopes between successive samples, deg per unit Dr): 10.4 to 10.8 over the first 0.1,
   then straight at 11.0 from Dr 0.10 to 0.40; a gradual bend, 10.0, 9.7, 9.4, 9.2, 9.0 from Dr 0.40
   to 0.65; then 8.5 to 8.6 from Dr 0.65 to 0.90, easing to 8.1 over the last 0.05.

## Features

1. First point and last point as the trace ends above.
2. Knee rule (the same for every figure Claude read in this batch): straight stretches of the traced
   centre are fitted (`out/stretch_slopes.py`); where the slopes of the stretches on either side of a
   bend differ by 20 % or more of the steeper, the bend is a knee, placed at the curvature-weighted
   centroid of the bend between them (`out/curvature.py`, `out/bend_centroid.py`, quadratic fits over
   120 px windows), with bounds 80 px in u (about 0.05 in Dr) and |slope| x 80 px + half the line
   thickness in v.
3. Knee: one, at u 1571, v 2102.0 (Dr 0.495, phi 42.12; read bounds 0.053 in Dr, 0.58 deg). A
   gradual bend, not a kink: straight stretches dv/du -0.544 (u 818 to 1370) and -0.420 (u 1800 to
   2350), a 23 % change. The bend is made of two gentle sub-bends (curvature peaks near u 1480 and
   1735, Dr 0.45 and 0.60) with a short stretch at -0.474 (u 1560 to 1660) between them, each under
   the threshold on its own (13 % and 11 %); counted as one bend, the knee at its centroid.
   A single-breakpoint two-segment fit puts the break at u 1588 (rms 1.5 px against 13.0 px for one
   line).

## Ambiguities

1. The knee is the weakest call of the feature set: the bend spans Dr 0.37 to 0.64 and another
   reader may place it anywhere there, or record its two sub-bends as two knees, or none (the change
   is 23 %, near the 20 % threshold).
2. The first and last samples sit at the frames' inner edges; whether the drawn curve ends at the
   frame centre or its inner edge cannot be told from the ink (u bounds cover both).

## Files

`cal-p1/` (anchors.csv, calibration.json, knots-check.json, points-p1-affine.csv),
`calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`,
`points-spec-p1.json` (ends, knee and bounds fed to `out/build_points.py`), `columns-p1.csv` and
`columns-p1-inframe.csv` (traced columns; the latter clipped to the frame and with the break columns
marked), `crops/`.
