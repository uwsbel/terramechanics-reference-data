# FA-8, panel 1: reading notes (Claude, blind, batch curves-appa-b1)

Page `p0016.png` (printed A-15). Caption as printed: "Figure A-8. Angle of Internal Friction (as
determined by the direct shear test) Versus Relative Density for PS Soil". Axis titles: "Angle of
Internal Friction, phi, (Degrees)" and "Relative Density, Dr". One panel, upright, full grid, one solid
curve, no symbols, no legend. Series id `curve` as given in `series.csv`; the page agrees with it.

## Calibration (`cal-p1/`)

1. `calibrate_axes.py detect`, box u 840..2425, v 1500..3250, 9 bands, x values 0, 0.2, ..., 1.0
   (left frame to right frame), y values 30, 35, 40, 45, 50 (the 30 line to the top frame).
2. The bottom frame line (v about 3444, one grid interval below 30) carries no printed label; it is
   left out of the box and of the map. The curve never goes below y = 43.
3. All 11 lines detected in 9 of 9 bands, none predicted. Affine residuals: x rms 0.003 (0.3 % of the
   0 to 1 span), **max 0.006 (0.6 %, above the 0.5 % guide)**; y rms 0.026 deg (0.13 % of the 30 to 50
   span), max 0.044 deg (0.22 %).
4. The x residual is the drafting, not the detection: the vertical lines are unevenly spaced, 294.7,
   304.9, 315.0, 307.6 and 311.7 px per 0.2 of Dr, and every line lies on its ink (next item). A
   different box cannot change the spacing, so the box was kept; values come from the piecewise map,
   which reads the grid as drawn. Affine minus piecewise on the trace: up to 0.005 in Dr and 0.03 deg
   (`cal-p1/points-p1-affine.csv`).
5. Ink check (`cal-p1/knots-check.json`): every line verified, ink at 12 of 12 (x) and 15 of 15 (y)
   positions, end offsets 0.34 px or less, location errors 0.50 to 0.92 px.
6. Labels checked by eye: all five y labels and all six x labels (`calibration-eye-checks.csv`), each
   on the line it is anchored to.

## Trace (`points-p1.csv`, `points-p1-native.csv`)

1. Method (`out/trace_curve.py columns`), u 870 to 2393 (1524 columns): 1444 clean, 40 with one edge
   merged into the y = 45 line (centre from the free edge and the local vertical thickness), 33 inside
   the 0.2, 0.4, 0.6 and 0.8 vertical lines (samples interpolated between the clean columns either
   side, 9 to 10 px apart; the curve's ink runs through), 7 marked `break`.
2. A hairline white break crosses the curve's ink at u 1995 to 2001 (Dr 0.737 to 0.743), slanted,
   3 to 4 px wide: a print defect, not a gap in the drawn curve (the ink continues on both sides at the
   same level). Those 7 columns are not used; no sample falls in them (Dr 0.75 is at u 2008.8, on clean
   columns).
3. Stray marks near the curve, not part of it: a row of dots about 10 px below the curve at u 1660 to
   1690, v 1858 (white gap between them and the curve), and a speck at about (1696, 1843). The tracker
   followed the curve's run, and `out/cols_check.py` flags no column there.
4. The curve crosses the y = 45 line exactly at the 0.4 vertical line. The Dr 0.40 sample is
   interpolated between two one-edge columns (u 1459 and 1469) to v 1901.6; a quadratic fit through the
   clean columns within 60 to 90 px gives 1901.2 to 1901.6. Its v bound is 7.5 px. Ink pools at that
   triple crossing (vertical run 18 px at u 1453 to 1454).
5. Samples: the left end, Dr 0.05 to 0.95 every 0.05 (19), the right end: 21 trace samples. Bound
   6.5 px in u and v (half of a perpendicular line thickness of 11.5 to 13.2 px, median 12.3).
6. Ends: the curve's ink runs into both frame lines, nothing beyond them. First sample at the left
   frame's inner edge, u 869.5 (frame ink 858 to 868, centre 863.0), v 2063.0: Dr 0.004, phi 43.00.
   Last sample at the right frame's inner edge, u 2393.5 (frame ink 2394 to 2403), v 1633.5: Dr 0.997,
   phi 48.58. Both flagged `extrapolated x` because their u bound reaches the frame line's centre (the
   curve's own ink is hidden in the frame). A small blob on the right frame's outer edge at v 1616 to
   1620 belongs to the frame.
7. Shape (slopes between successive samples, deg per unit Dr): an S-shaped curve. Concave up from
   the left end, 3.0, 3.5, 3.8, 4.7, 6.0, 6.8 to 7.3 at Dr 0.30 to 0.35; a gentle inflection near Dr 0.38
   (the curve crosses the 0.4 and 45 intersection); nearly straight at 6.2 to 6.7 from Dr 0.40 to 0.75;
   flatter, 5.0 to 5.2, from Dr 0.75 to 0.95; 5.9 over the last 0.05.

## Features

1. First point and last point as the trace ends above.
2. Knee rule (the same for every figure Claude read in this batch): straight stretches of the traced
   centre are fitted (`out/stretch_slopes.py`); where the slopes of the stretches on either side of a
   bend differ by 20 % or more of the steeper, the bend is a knee, placed at the curvature-weighted
   centroid of the bend between them (`out/curvature.py`, `out/bend_centroid.py`, quadratic fits over
   120 px windows), with bounds 80 px in u (about 0.05 in Dr) and |slope| x 80 px + half the line
   thickness in v. Every bend here is gradual; none is a kink.
3. Knee 1, the toe of the S: u 1124, v 2014.5 (Dr 0.176, phi 43.62; read bounds 0.054, 0.35 deg).
   Straight stretches dv/du -0.167 (u 870 to 990) and -0.364 (u 1250 to 1400), a 54 % change; the
   curvature peaks at u 1170 (Dr 0.20).
4. Knee 2, the flattening: u 2012, v 1732.5 (Dr 0.752, phi 47.29; read bounds 0.052, 0.39 deg).
   Straight stretches dv/du -0.311 (u 1530 to 1950) and -0.246 (u 2080 to 2230), a 21 %
   change, just over the rule's threshold. The knee is on clean ink just right of the hairline break.
5. Not recorded (under 20 %): the inflection near Dr 0.38 (-0.364 to -0.311, 15 %) and the slight
   steepening over the last 0.1 of Dr (-0.246 to -0.271, 9 %).

## Ambiguities

1. Knee placement on a smooth bend is a judgement: for the toe anywhere from Dr 0.10 to 0.25 is
   defensible, hence the wide bounds. The second knee (21 %) is a borderline call; another reader may
   not record it, or may record the inflection near Dr 0.38 instead.
2. The first and last samples sit at the frames' inner edges; whether the drawn curve ends at the
   frame centre or its inner edge cannot be told from the ink (u bounds cover both).

## Files

`cal-p1/` (anchors.csv, calibration.json, knots-check.json, points-p1-affine.csv),
`calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`,
`points-spec-p1.json` (ends, knee and bounds fed to `out/build_points.py`), `columns-p1.csv` and
`columns-p1-inframe.csv` (traced columns; the latter clipped to the frame and with the break columns
marked), `crops/`.
