# FC-12, Figure C-12, RC2 Loose (printed C-34, PDF page 148), reader Claude

Series `rc2-loose` (series.csv). The page prints "RC2 Loose" as the box title and the caption
"Figure C-12. RC2 Loose", which agrees with series.csv and figures-rows.csv (avg density 58.00).

## The box, as printed

    RC2  Loose
    Avg. Density = 58.00
    Angle of Friction = 43.07
    Tan Theta = .9349
    Cohesion = 145.81

The "=" signs print as filled bars, and in the scan the decimal points of 58.00, 43.07 and 145.81
look like commas. tan(43.07 deg) = 0.9350, consistent with the printed Tan Theta. Cohesion is
taken in psf: the axes print "(x 10^1)", but the line meets the x = 0 axis near 150 psf, not near
1458 psf.

## Calibration (cal-p1/)

1. `calibrate_axes.py detect` on box u 560..2650, v 1365..3770, 8 bands, x values 0 to 7000 psf
   (vertical lines), y values 0 to 8000 psf (horizontal lines). The plot frame continues above the
   8000 line (to v 900) around the text box; the detection box starts just above the 8000 line so
   the frame top is not taken as a grid line.
2. All 8 vertical and 9 horizontal lines detected in 8 of 8 bands; none predicted. Affine residuals:
   x RMS 3.9 psf (max 7.7), y RMS 10.0 psf (max 20.8), that is 0.06 and 0.13 percent of the spans
   (max 0.26 percent), below the 0.5 percent limit.
3. Piecewise map (D-025) with `--image`: all 8 x lines and all 9 y lines verified on the ink,
   location errors 0.54 to 0.85 px; nothing rejected. Summary in `cal-p1/knots-summary.json`.
4. The grid is unevenly spaced: horizontal lines 288 to 299 px per 1000 psf (at u 1300), vertical
   lines 288 to 294 px per 1000 psf; the horizontal lines fan from a tilt of 0.0032 (top) to 0.0062
   (bottom). This is why the piecewise and affine values differ (below).
5. By-eye label checks: six labels, three per axis, in `calibration-eye-checks.csv`; every label sits
   on the line it was anchored to (offsets 2 to 8 px).

## Points (points-p1.csv, points-p1-native.csv)

8 markers, 11 trace samples, 3 features; all `rc2-loose`, panel 1. Values in psf, piecewise map.

Markers: 8 upright triangles, none overlapping another. Centres are centroids of the triangle
reconstructed from its stroke centre lines (rule 8): sides fitted row by row, base fitted column by
column, apex at the intersection of the sides, with the grid lines and the drawn line masked. A
second estimate (outer edges inset by half the stroke) agrees within 0.7 px for 7 of 8 symbols.
Bounds: 2 px in u; 5.5 px in v (at least height/6, heights 27 to 33 px). Per symbol:

1. Triangle 1 (x 158, y 227 psf): the drawn line passes over its apex and upper left side. The
   left side is taken as the mirror of the right side about the base midpoint (all clean symbols
   are isosceles within 1 px). Bound 3 px u, 6 px v.
2. Triangles 2, 4, 5, 7 sit in gaps of the drawn line. Triangle 5's right base corner touches the
   x = 3000 grid line; triangle 3's apex touches the y = 2000 grid line.
3. Triangle 6 (x 3814, y 3710): its lower right side is covered by the start of the next dash; the
   right side is taken as the mirror of the left one. The stroke-centre and edge estimates differ by
   1.4 px in v (2645.0, 2646.4); the edge estimate is used because its apex agrees with the ink top.
   Bound 3 px u, 6 px v.
4. Triangle 8 (x 4682, y 4548): the drawn line ends in its base; the base centre is read on the
   clean right part of the base.

Not symbols: a short faint dash right of triangle 1 at the base level (u 670 to 697, v 3673), a
dotted trail right of triangle 2 (u 827 to 872, v 3512) and a small mark right of triangle 8
(u 1975 to 1982, v 2412 to 2417). They look like pen drag or dirt and are not recorded.

The drawn line: straight on the page (fit v = 4232.32 - 0.93021 u over 751 clean columns, RMS 0.86
px, mean residual by thirds +0.09, -0.20, +0.11 px), about 11 px thick across (15 px vertical run),
drawn as dashes that stop short of the symbols near it (gaps around triangles 2, 4, 5 and 7).
Trace samples are the centre of the ink at each sampling column, from a local straight fit over
clean columns within 16 px (never the global fit), bound half the thickness, 5.5 px:

1. Left end, x = 0: the line runs into the left frame; its ink is hidden under the frame (no ink
   left of it), so the end is placed at the frame's centre line, bound 4.5 px u (the frame's
   half-width) and 9.5 px v (half the thickness plus the slope times the u bound).
2. x = 500, 1000, ..., 4500 psf (9 samples). x = 1000, 2000, 3000 and 4000 fall on vertical grid
   lines; their centres come from clean columns on both sides, or on one side within 10 px where the
   line also touches a horizontal grid line (x = 1000 and 2000) or a dash starts at the grid line
   (x = 3000, the dash after triangle 5 starts at u 1448, just left of the x = 3000 line).
3. Right end, x = 4684: the line runs into the base of triangle 8. Its end is hidden in the base
   stroke; the triangle's hole stays white, so the line ends before u 1952. Placed where the centre
   line meets the base's lower edge, bound 4.5 px u, 9.5 px v.

Features: first point and last point (same pixels as trace samples 1 and 11) and the intercept: the
line reaches the x = 0 axis (left frame), so the intercept is the centre line of the drawn line at
the frame's centre line, u 583.5, v 3685.4, bound 1 px u, 5.5 px v. Its x is -0.4 psf, which is why
`cal_model` flags it (and the first point) as extrapolated in x by less than one pixel.

## Comparison with the printed box (not used to move any point)

| quantity | printed | this reading (piecewise) | difference | same reading, affine map |
|---|---|---|---|---|
| slope of the trace samples (least squares, 11 samples) | Tan Theta .9349 | 0.9286 (42.88 deg) | -0.0063 (-0.7 percent) | 0.9304 (-0.5 percent) |
| end-to-end slope of the trace | | 0.9286 | -0.0063 | 0.9303 |
| shear stress at the intercept feature | Cohesion 145.81 psf | 158.6 psf, bound 20.4 | +12.8 psf | 147.9 psf (+2.1) |
| intercept of the least-squares line through the trace | | 139.6 psf | -6.2 psf | 141.1 psf |

1. The drawn line agrees with the printed Tan Theta to 0.7 percent and with the printed cohesion
   within the intercept's bound. Against the printed line y = 145.81 + 0.9349 x, the trace samples
   lie between +13 psf (at x = 0) and -45 psf (at x = 3000) under the piecewise map.
2. The intercept feature (158.6) is 19 psf above the least-squares line through the trace (139.6):
   near the frame the ink sits about 3 px above the straight line through the rest of the trace,
   which in pixels is straight within 1 px. Through the piecewise map the straight drawn line bows by
   +/-20 psf (+19 at both ends, -20 at x = 3000), a correlated calibration effect of the unevenly
   spaced grid, not a feature of the line.
3. Diagnostic only: a least-squares line through the 8 markers as read gives slope 0.9397 and
   intercept 115.3 psf (affine: 0.9413, 117.0), so the markers as read do not reproduce the printed
   cohesion; their registration point is unknown (rule 8) and a y offset of a few pixels in the
   symbol reference changes the intercept by about 3.4 psf per pixel.

## Calibration sensitivity (affine minus piecewise)

Markers: x within +/-6 psf, y -9 to +14 psf. Trace: x -6 to +8 psf, y -11 to +14 psf; the largest
differences are in the middle of the plot (y 2000 to 3500 psf) where the horizontal grid spacing is
smallest (288 to 290 px per 1000 psf).

## Ambiguities

1. Right end of the line: hidden in the base of triangle 8, between where it meets the base's lower
   edge (u 1949) and the white hole (u 1952); bound 4.5 px.
2. Left end: hidden under the left frame (u 579 to 588).
3. Triangle 1's apex and triangle 6's lower right side are hidden; both reconstructed by symmetry.
4. Marker registration (bounding-box middle against centroid) is not established; the v bound of
   at least height/6 covers both.

## Files

`cal-p1/` (anchors.csv, calibration.json, knots-summary.json), `calibration-eye-checks.csv`,
`points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`, `notes.md`. Working files: `read_env.py`
and `config.json` (the reading helper and its settings), `helper-log.txt`, `helper-*.json`,
`compare_box.py`, `montage.py`, `check-tri*.png` and `check-montage.png` (symbol reconstructions),
`affine-check.csv` (affine values, for the sensitivity only), `eye-*.png`, `z*.png`, `box-text.png`
(crops).
