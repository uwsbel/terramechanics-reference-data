# FC-15, Figure C-15, LSM Dense (printed C-37, PDF page 151), reader Claude

Series `lsm-dense` (series.csv). The page prints "LSM Dense" as the box title and the caption
"Figure C-15. LSM Dense", which agrees with series.csv and figures-rows.csv (avg density 91.20).
The x-axis title prints "(x10^1)" without a space.

## The box, as printed

    LSM Dense
    Avg. Density = 91.20
    Angle of Friction = 41.05
    Tan Theta = .8710
    Cohesion = 213.?6

1. The "=" signs print as filled bars; decimal points look like commas in the scan.
2. Tan Theta: a short thin mark sits between the "=" and ".8710", too small for a minus sign; read
   as a speck. tan(41.05 deg) = 0.8710, consistent.
3. Cohesion: the tenths digit is broken (`box-cohesion.png`): a serif at the top left, a top bar
   turning down at the right, and a foot at the lower left, with the middle missing. Read as 7
   (213.76), possibly 3 (213.36); the comparison below uses 213.76, and the alternative changes it by
   0.4 psf. Taken in psf.

## Calibration (cal-p1/)

1. `calibrate_axes.py detect` on box u 650..2765, v 1345..3755, 8 bands, x 0 to 7000 psf, y 0 to
   8000 psf. The frame continues above the 8000 line (to v 881) around the text box; the detection
   box starts just above the 8000 line.
2. All 8 vertical and 9 horizontal lines detected in 8 of 8 bands; none predicted. The vertical
   lines fan out (tilt +0.0051 at x = 0 to +0.0115 at x = 7000, a keystone of the scan or the
   drafting); horizontal lines tilt -0.0019 to -0.0041. Affine residuals: x RMS 6.0 psf (max 18.9),
   y RMS 12.1 psf (max 27.9), that is at most 0.27 and 0.35 percent of the spans, the largest of this
   batch but under the 0.5 percent limit; the piecewise map follows each line's own tilt.
3. Piecewise map with `--image`: all 8 x lines and 9 y lines verified on the ink, location errors
   0.50 to 1.07 px; nothing rejected (`cal-p1/knots-summary.json`).
4. Spacing: vertical lines 290 to 294 px per 1000 psf, horizontal lines 287 to 300 px.
5. By-eye label checks, three per axis, in `calibration-eye-checks.csv`; every label sits nearest
   its line (largest offset: 400.00, 11.5 px above its line, 280 px from the neighbours).

## Points (points-p1.csv, points-p1-native.csv)

8 markers, 11 trace samples, 3 features; all `lsm-dense`, panel 1; psf, piecewise map.

Markers: 8 upright triangles, none overlapping another; centroids of the triangle reconstructed
from its stroke centre lines (rule 8), checked in `check-tri*.png` (stroke-centre and edge-inset
estimates within 1.3 px). Bounds 2 to 3 px in u, 5.5 to 7 px in v (at least height/6, heights 27
to 31 px).

1. Triangle 1 (x 179, y 419): the drawn line crosses its lower right corner; right side read on the
   rows clear of the line, base on its central columns. Bound 2.5 / 5.5 px.
2. Triangle 2 (x 750, y 801): sits in a gap of the drawn line (about u 890 to 927).
3. Triangles 3 (x 1768, y 1393), 4 (x 2357, y 2644), 6 (x 3825, y 3095) and 7 (x 4412, y 4436):
   clear of the line.
4. Triangle 5 (x 2935, y 3041): its base coincides with the y = 3000 grid line (merged band v 2822 to
   2832.75; grid line alone 2825.5 to 2831.5) and its right base corner touches the x = 3000 line.
   The base centre is fixed at v 2827.3, the middle of the band, between hole bottom plus half a
   stroke (2825.8) and band bottom minus half a stroke (2829); the right side is read on the rows
   clear of the vertical grid line. Bound 3 / 7 px.
5. Triangle 8 (x 4703, y 4068): clear of the line, which passes above its upper left and ends above
   it; a speck inside its hole touches the base.

Not symbols: specks right of triangles 2, 3 and 7 at their base level (u 932 to 947 v 3490; u 1233
v 3313; u 1991 to 1999 v 2422) and a dot at u 1905, v 3325. Not recorded.

The drawn line: straight on the page (v = 4282.04 - 0.88490 u over 1083 clean columns, RMS 0.66 px,
by thirds -0.11, +0.16, -0.05 px), 10.5 px thick across (14 px vertical run), continuous from the
left frame to its end except the gap around triangle 2. Trace samples are the centre of the ink from
a local straight fit over clean columns within 16 px; bound 5.2 px (half the thickness):

1. Left end, x = 0: the line runs into the left frame; its ink is hidden under the frame (no ink
   left of it). Placed at the frame's centre line, u 688.0, v 3673.2; bound 4.5 px u, 9 px v.
2. x = 500 to 4500 psf every 500 (9 samples); x = 1000, 2000, 3000, 4000 on vertical grid lines
   (x = 1000 also where the line crosses the y = 1000 line); centres from clean columns on both
   sides.
3. Right end, x = 4751: the line ends with a squared end above and right of triangle 8 (last ink
   column u 2071 at the end's lower corner); centre line end u 2067.5, v 2452.1; bound 3 px u,
   8 px v.

Features: first point and last point (as trace samples 1 and 11); intercept: the line reaches the
x = 0 axis (left frame), u 688.0, v 3673.2, bound 1 px u, 5.2 px v.

## Comparison with the printed box (not used to move any point)

| quantity | printed | this reading (piecewise) | difference | same reading, affine map |
|---|---|---|---|---|
| slope of the trace samples (least squares, 11) | Tan Theta .8710 | 0.8692 (41.00 deg) | -0.0018 (-0.2 percent) | 0.8723 (+0.2 percent) |
| end-to-end slope | | 0.8698 | -0.0012 | 0.8723 |
| shear stress at the intercept feature | Cohesion 213.76 psf | 163.2 psf, bound 19.1 | -50.5 psf | 140.0 psf (-73.8) |
| intercept of the least-squares line through the trace | | 154.1 psf | -59.7 psf | 154.2 psf |

1. The slope agrees with Tan Theta within 0.2 percent. The level does not: the drawn line lies
   50 to 73 psf (15 to 21 px) below the printed line y = 213.76 + 0.8710 x along its whole length
   (-50 at x = 0, -73 near x = 3000 to 3500, -56 at the right end), well outside the bounds.
2. Diagnostic only: a least-squares line through the 8 markers as read gives slope 0.8671 and
   intercept 218.5 psf (affine: 0.8695, 220.4 psf), close to the printed values. On this figure the
   markers reproduce the printed fit and the drawn line is parallel to it but lower.
3. The affine map's intercept (140.0 psf, x -17.1) differs from the piecewise one mainly because
   the affine map misplaces the left frame by 17 psf in x (the keystone); the piecewise value is the
   one tied to the drawn lines.

## Calibration sensitivity (affine minus piecewise)

Markers: x -14 to +3 psf, y -16 to +17 psf. Trace: x -17 to +3 psf, y -23 to +16 psf, largest at the
left frame, where the fanning vertical lines put the affine map furthest from the drawn x = 0 line.
Through the piecewise map the straight drawn line bows by about +/-12 psf (+9 and +12 at the ends,
-8 near x = 3000).

## Ambiguities

1. The tenths digit of the printed cohesion (7 or 3).
2. Triangle 5's base is under the y = 3000 grid line; its centre is uncertain by about 1.5 px, which
   the 7 px v bound covers.
3. Left end hidden under the frame (u 684 to 692).
4. Marker registration (bounding-box middle or centroid) not established; the v bound covers both.

## Files

`cal-p1/` (anchors.csv, calibration.json, knots-summary.json), `calibration-eye-checks.csv`,
`points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`, `notes.md`. Working files: `read_env.py`,
`config.json`, `helper-log.txt`, `helper-*.json`, `compare_box.py`, `montage.py`,
`label_centre.py`, `check-tri*.png`, `check-montage.png`, `affine-check.csv`, `eye-*.png`, `t*.png`,
`tri-montage.png`, `zz*.png`, `box-text.png`, `box-cohesion.png`.
