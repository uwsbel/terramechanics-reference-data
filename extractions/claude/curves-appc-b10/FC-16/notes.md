# FC-16, Figure C-16, printed page C-38, PDF page 152 (p0152.png): blind reading, Claude

Caption as printed: "Figure C-16. Angle of Internal Friction vs. Relative Density". Axis titles: y
"phi_DS - Degrees", x "D_r". The only text inside the plot is "RS Soil" (upper left). The page prints
no legend: the roles of the series (circles = data, solid curve = mean, dashed curves = upper and
lower) are taken from `series.csv`; nothing on the page contradicts them. One panel, upright.

## Calibration (`cal-p1/`)

1. `calibrate_axes.py detect` on box u 680..2480, v 1240..3495 (inside the frame, so the outermost
   tracks are the outermost labelled lines, not the frame), 12 bands, dark 200, min-frac 0.5. x
   values 0, 0.1, ..., 1.0 on the 11 vertical lines; y values 30, 35, 40, 45, 50 on the 5 horizontal
   lines. Every line detected in 12 of 12 bands; none predicted. 55 anchors.
2. Affine residuals: x rms 0.0014, max 0.0034 (0.34 percent of the 1.0 span); y rms 0.0066 deg,
   max 0.013 deg (0.07 percent of the 20 deg span). Both under the 0.5 percent threshold.
3. Ink check of every line (`check_knots.py`, the tool's own `AxisKnots` check; record in
   `cal-p1/knots-check.json`): all 16 lines verified, ink found at 12 of 12 (x) and 25 of 25 (y)
   positions, the reader's line within 0.66 px of the ink's line at both ends; location errors 0.50
   to 1.12 px. No line rejected. Values in `points-p1-native.csv` come from `calibrate_axes.py
   piecewise --image` (D-025). The affine map differs from the piecewise one by at most 0.0026 in
   Dr and 0.024 deg (`cal-p1/points-p1-affine-diagnostic.csv`, diagnostic only).
4. The grid is drafted unevenly in x: interval widths at the bottom of the plot 154, 160, 160, 151,
   155, 157, 157, 147, 158, 158 px (0 to 1.0); the 0.7 to 0.8 interval is the narrowest. The lines
   are tilted about 0.5 degree (u grows by about 20 px from top to bottom of the plot); the 0.8 and
   0.9 lines are tilted less than the others (0.005 and 0.006 against about 0.009 du/dv).
5. By-eye label checks (`calibration-eye-checks.csv`): all 11 x labels and all 5 y labels read on
   zoomed crops and their glyph centres measured. Every label sits within 16 px of its line (grid
   spacing about 155 px in x, 384 px in y). The 0.8 label is printed 15 px left of its line; still
   unambiguous.

### Frame extent beyond the labelled lines (not anchored)

The frame carries no labels and is not a knot. Measured on the page and converted by
extrapolation: left frame at Dr -0.095 (centre u 639 at the top to 651 at the bottom, 10 to 12 px
wide), right frame at Dr 1.099 (u 2496 to 2510), top frame at 54.98 deg (v about 1211), bottom frame
at 25.00 deg (v about 3517). So the frame runs one grid interval past the labelled lines on all
four sides: about -0.1 to 1.1 in Dr and 25 to 55 deg in phi. Values left of Dr 0, right of Dr
1.0 or above 50 deg are flagged `extrapolated` in `cal_model`, as are some samples on the Dr 0 and
1.0 lines whose bound interval crosses the line (32 of 94 rows in all).

## Circles (series `data`, 11 markers)

Centres are least-squares circle fits to the ring (`circles.py`: edge points on rays every 3
degrees, rays disturbed by crossing lines rejected; ring radius 16.1 to 16.7 px, fit rms 0.35 to
0.56 px). A ring search over the whole plot (`find_circles.py`) finds no other circle. Pairs are
numbered from the left; the three circles on the right frame have no joining line ("single").

| seq | note | Dr | phi deg |
|---|---|---|---|
| 1 | pair 1 left, cut by the left frame (frame through its centre) | -0.097 | 38.82 |
| 2 | pair 1 right, Dr 0 grid line through it | 0.002 | 38.88 |
| 3 | pair 2 left, Dr 0.5 grid line through it, in a gap of the upper dashed curve | 0.499 | 45.78 |
| 4 | pair 2 right, overlaps the solid curve | 0.572 | 45.74 |
| 5 | pair 3 left, overlaps the solid curve | 0.729 | 46.67 |
| 6 | pair 3 right | 0.873 | 46.67 |
| 7 | pair 4 left, Dr 1.0 grid line through it, upper dashed curve touches its top | 1.001 | 50.74 |
| 8 | single, cut by the right frame, upper dashed curve passes through it | 1.100 | 52.55 |
| 9 | single, cut by the right frame, solid curve passes through it | 1.101 | 49.63 |
| 10 | single, cut by the right frame, lower dashed curve ends at its ring | 1.099 | 46.65 |
| 11 | pair 4 right, OUTSIDE the frame (right of the right frame) | 1.131 | 50.77 |

Bounds: 2 px for clean centres (2, 6, 11), 3 px for circles cut by the frame or overlapping or
touching a curve (1, 3, 4, 5, 7, 8, 9, 10). Circles 1 and 8 to 10 sit exactly on the frame lines (Dr
-0.1 and 1.1), and circle 11 and the right ends of two curves lie outside the frame: what is printed
is recorded, the plotted Dr range is not interpreted.

## Curves (traces)

Which is which: the solid line is `mean`; the dashed line above it is `upper`; the dashed line below
it is `lower`. They do not cross or touch one another anywhere. All three rise monotonically, so the
maximum of each trace is its last point; there is no knee or kink (slopes change gradually, see
below), so each trace has two features, first and last point.

Method: the ink centre line of every dash was measured column by column (`measure.py`; columns
under grid lines, frames and circles skipped; rms about a quadratic per dash 0.43 to 0.75 px), and
each sample takes v from a straight fit to the measured centres of the same dash within 10 px
(15 to 25 px where a grid line removes columns). Samples at Dr 0, 0.1, ..., 1.0 fall on vertical
grid lines; where the dash runs continuously through the line, the value is from the dash's ink on
both sides. Bound: half the line thickness across the line, 2.5 to 5 px.

1. `mean` (solid, continuous): ink from u 660 (Dr -0.085, 39.02 deg) to u 2545 (Dr 1.129, 50.08
   deg). At its left end it runs into the ring of circle 1 at the left frame; the first sample is the
   first ink clear of the ring. It crosses the lower half of circle 4 and the upper half of circle 5
   (no sample falls there). At the right it passes through circle 9 and the frame (hidden from u 2483
   to 2515) and continues outside the frame to u 2546. 26 trace samples; the Dr 1.10 sample is
   moved +16 px to the first clear ink right of circle 9.
2. `upper` (dashed, 14 dashes, gaps 19 to 47 px): ink from u 653 (Dr -0.090, 39.41 deg) to u 2530
   (Dr 1.121, 52.85 deg). The first dash emerges from under the left frame (the line may start under
   it). The dashes stop either side of circle 3 (gap u 1537 to 1582); the next dash starts at that
   circle's ring and has a 2 px pen break at u 1598 to 1599, treated as one dash. The last dash
   passes through circle 8 and the frame (hidden u 2480 to 2516) and ends outside the frame. 26
   trace samples; moved: Dr 0.50 (+18 px, gap holding circle 3), Dr 1.05 (-6 px, gap), Dr 1.10 (-19
   px, nearest clear ink left of circle 8).
3. `lower` (dashed, 11 dashes): ink from u 653 (Dr -0.090, 37.97 deg) to u 2479 (Dr 1.085, 46.60
   deg). The first dash emerges from under the left frame. The dashes stop either side of circle 2
   (gap u 754 to 820). The last dash runs into the ring of circle 10 on the right frame; nothing of
   the curve continues beyond that circle. 25 trace samples (none at Dr 1.10, which is past the
   curve's end); moved to the nearest dash end: Dr 0.00 (+30 px, gap holding circle 2), 0.10 (-13
   px), 0.80 (+6 px, gap holding the crossings of the 45 deg and Dr 0.8 lines), 0.90 (+26 px), 1.00
   (+12 px).

Shape (slopes between successive samples, deg per unit Dr): `upper` about 11 at the left, 9.5 to
10 between Dr 0.5 and 0.8, then steepening to 12 at Dr 1.0 and 16 on the last dash (the last dash
curves upward through circle 8; it meets the extrapolation of the previous dash within 3 px, so the
upturn is curvature, not a kink). `mean` about 10.6 up to Dr 0.4, flattening to 6.7 at Dr 0.7 to
0.75, steepening again to 9.7 at the end. `lower` flattens steadily from 9.2 to 2.7.

## Ambiguities and things to look at

1. Ends at the frames: the left ends of `upper` and `lower` are where ink emerges from under the
   left frame; whether the lines begin under the frame cannot be seen. The right ends of `upper` and
   `mean` are outside the frame (Dr 1.12 and 1.13).
2. Dr 1.10 samples of `upper` and `mean` are under a circle and the frame and were moved to the
   nearest clear ink: `upper` 19 px to the left (the clear ink to the right is also 19 px away; the
   left side was taken), `mean` 16 px to the right (18 px to the left).
3. Circle 11 (pair 4 right) lies outside the frame; its joining line crosses the right frame.
4. Stray ink not read: a short spur below the start of the last `upper` dash (u 2452 to 2462, v 1434
   to 1437), a speck below the last `lower` dash (u 2440 to 2452, v 1863 to 1868), a short horizontal
   stroke above "RS Soil" (u about 1150 to 1240, v about 1333), a dotted underline under the x labels
   0.9 and 1.0 (scan artefact).
5. The x grid is unevenly drafted (0.7 to 0.8 interval 147 px against 151 to 160 elsewhere); the
   piecewise map reads it as drawn.

## Files (under `out/FC-16/`)

`points-p1.csv` (pixels), `points-p1-native.csv` (piecewise values), `overlay-p1.png`,
`calibration-eye-checks.csv`, `cal-p1/` (anchors.csv, calibration.json, knots-check.json,
points-p1-affine-diagnostic.csv), `crops/` (zoomed crops used for the reading), and the helper
scripts `label_centers.py`, `check_knots.py`, `track.py`, `clean.py`, `model.py`, `dashes.py`,
`measure.py`, `sample.py`, `circles.py`, `find_circles.py`, `write_points.py` (with their
intermediate json files).
