# FC-14, Figure C-14, LSM Loose (printed C-36, PDF page 150), reader Claude

Series `lsm-loose` (series.csv). The page prints "LSM Loose" as the box title and the caption
"Figure C-14. LSM Loose", which agrees with series.csv and figures-rows.csv (avg density 75.20).
The y-axis title prints "(x10^1)" without a space.

## The box, as printed

    LSM Loose
    Avg. Density = 75.20
    Angle of Friction = 43.95
    Tan Theta = .9642
    Cohesion = -109.97

The "=" signs print as filled bars; decimal points look like commas in the scan. The minus sign of
the cohesion is clear. tan(43.95 deg) = 0.9642, consistent with Tan Theta. Cohesion taken in psf.

## Calibration (cal-p1/)

1. `calibrate_axes.py detect` on box u 615..2700, v 1375..3795, 8 bands, x 0 to 7000 psf, y 0 to
   8000 psf. The frame continues above the 8000 line (to v 918) around the text box; the detection
   box starts just above the 8000 line.
2. All 8 vertical and 9 horizontal lines detected in 8 of 8 bands; none predicted. The page is
   rotated more than its neighbours (horizontal lines tilt +0.0085 to +0.0107, vertical lines -0.0034
   to -0.0046, so the grid is also slightly sheared). Affine residuals: x RMS 3.6 psf (max 6.9),
   y RMS 10.5 psf (max 19.7), at most 0.25 percent of a span.
3. Piecewise map with `--image`: all 8 x lines and 9 y lines verified on the ink, location errors
   0.59 to 1.29 px; nothing rejected (`cal-p1/knots-summary.json`).
4. Spacing: vertical lines 289 to 293 px per 1000 psf, horizontal lines 287 to 299 px.
5. By-eye label checks, three per axis, in `calibration-eye-checks.csv`; every label sits on its line
   (offsets -7.9 to +3.2 px).

## Points (points-p1.csv, points-p1-native.csv)

8 markers, 11 trace samples, 3 features; all `lsm-loose`, panel 1; psf, piecewise map.

Markers: 8 upright triangles, none overlapping another; centroids of the triangle reconstructed
from its stroke centre lines (rule 8), checked in `check-tri*.png`. Bounds 2 to 3 px in u, 5.5 to
6.5 px in v (at least height/6, heights 27 to 30 px).

1. Triangle 1 (x 118, y 207): the drawn line crosses its right base corner; right side read on the
   rows clear of the line, base on its central columns.
2. Triangle 2 (x 710, y 415), triangle 4 (x 2338, y 1878, just below the y = 2000 grid line),
   triangle 5 (x 2919, y 2863, right base corner 4 px from the x = 3000 grid line) and triangle 6
   (x 3822, y 3740): clear of the line.
3. Triangle 3 (x 1750, y 1612): the line's dash ends at its lower left and resumes from its upper
   right side; right side taken as the mirror of the left about the base axis (u 1147.5); edge-inset
   estimate used (v 3268.2), the stroke-centre estimate gives v 3269.2. Bound 3 / 6.5 px.
4. Triangle 7 (x 4443, y 3976): the y = 4000 grid line runs through its middle and the drawn line
   touches its apex and upper left side; right side read on the rows clear of both and mirrored about
   the base axis (u 1933.0); edge estimate used (v 2585.9), the stroke-centre estimate gives v 2586.8
   and the base with the figure's typical height gives about 2586.1. Bound 3 / 6.5 px.
5. Triangle 8 (x 4711, y 4233): the drawn line passes close above its apex and upper left side and
   ends above it.

Not symbols: short dashes or specks to the right of triangles 2, 3 and 8 at their base level
(u 868 to 879 v 3629; u 1172 to 1180 v 3274 to 3280; u 2032 to 2042 v 2520), and a speck left of the
frame corner (u 617 to 622, v 3748). Not recorded.

The drawn line: straight on the page (v = 4328.25 - 0.92062 u over 994 clean columns, RMS 0.75 px,
by thirds -0.20, +0.24, -0.04 px), 9.6 px thick across (13 px vertical run). It is continuous except
across triangle 3 (gap u 1128 to 1152, the triangle in between) and a 3 px jog at u 1194 to 1197
where two drawn pieces meet slightly offset (no symbol there). Trace samples are the centre of the
ink from a local straight fit over clean columns within 16 px; bound 4.8 px (half the thickness):

1. Left end, x = 0: the line runs into the bottom left corner of the frame. Its centre line meets
   the x = 0 line 1.7 px below the y = 0 line's centre and the y = 0 line 1.8 px right of the x = 0
   line; no ink beyond the corner. Placed on the x = 0 line, u 635.3, v 3743.0 (x 0.3, y -4.4 psf,
   flagged `extrapolated x y` because it lies inside the corner's ink, a fraction of a pixel beyond
   the outermost lines); bound 4.5 px u, 8 px v.
2. x = 500 to 4500 psf every 500 (9 samples); x = 1000, 2000, 3000, 4000 on vertical grid lines,
   centres from clean columns on both sides.
3. Right end, x = 4726: the line ends with a squared end above triangle 8 (last ink column u 2019,
   at the end's lower corner); the centre line's end is at u 2016.0, v 2472.6; bound 3 px u,
   7.5 px v.

Features: first point and last point (as trace samples 1 and 11); intercept: the line reaches the
x = 0 axis in the frame corner, u 635.3, v 3743.0, y -4.4 psf, bound 1 px u, 4.8 px v.

## Comparison with the printed box (not used to move any point)

| quantity | printed | this reading (piecewise) | difference | same reading, affine map |
|---|---|---|---|---|
| slope of the trace samples (least squares, 11) | Tan Theta .9642 | 0.9258 (42.79 deg) | -0.0384 (-4.0 percent) | 0.9293 (-3.6 percent) |
| end-to-end slope | | 0.9262 | -0.0380 | 0.9290 |
| shear stress at the intercept feature | Cohesion -109.97 psf | -4.4 psf, bound 19.8 | +105.6 psf | -21.1 psf (+88.9) |
| intercept of the least-squares line through the trace | | -15.7 psf | +94.3 psf | -18.8 psf |

1. The drawn line does not agree with the printed values. It runs from the origin corner of the
   frame (x 0, y about 0), whereas the printed cohesion would put it 110 psf (about 32 px) below the
   frame at x = 0, crossing y = 0 at x = 114 psf (33 px right of the corner). Its slope is 4 percent
   below Tan Theta. Against the printed line y = -109.97 + 0.9642 x the trace runs from +105 psf at
   x = 0 to -74 psf at its right end, crossing near x = 2200 psf.
2. Not a calibration effect: on the page the line's slope is 0.9206 px/px (0.926 piecewise, 0.929
   affine, in value units); Tan Theta .9642 would need about 0.968 px/px, 65 px more rise over the
   line's 1380 px run.
3. Diagnostic only: a least-squares line through the 8 markers as read gives slope 0.9293 and
   intercept -52.0 psf (affine: 0.9326, -55.7 psf). The markers as read do not reproduce the printed
   values either; they lie between the drawn line and the printed one.

## Calibration sensitivity (affine minus piecewise)

Markers: x -4 to +2 psf, y -12 to +16 psf. Trace: x -5 to +5 psf, y -17 to +15 psf. Through the
piecewise map the straight drawn line bows by about +/-12 psf (+11 and +13 at the ends, -13 at
x = 2500), the effect of the uneven horizontal grid spacing.

## Ambiguities

1. Left end hidden in the frame corner; whether the line's ink stops exactly at the corner or a
   pixel or two inside it cannot be told.
2. Triangles 3 and 7 rest on a symmetry assumption (sides merged with the line or cut by a grid line).
3. Marker registration (bounding-box middle or centroid) not established; the v bound covers both.

## Files

`cal-p1/` (anchors.csv, calibration.json, knots-summary.json), `calibration-eye-checks.csv`,
`points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`, `notes.md`. Working files: `read_env.py`,
`config.json`, `helper-log.txt`, `helper-*.json`, `compare_box.py`, `montage.py`,
`label_centre.py`, `check-tri*.png`, `check-montage.png`, `affine-check.csv`, `eye-*.png`, `t*.png`,
`tri-montage.png`, `zz*.png`, `z-corner.png`, `box-text.png`.
