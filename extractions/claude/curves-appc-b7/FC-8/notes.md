# FC-8 (Figure C-8, RS Loose), printed page C-24, page image p0138.png

Reader: Claude (blind reading, batch curves-appc-b7). One panel, one series `rs-loose`.

## What is printed

Caption: "Figure C-8. RS Loose". Box title: "RS LOOSE" (matches the series id given in series.csv).
The four values in the box, as printed:

1. Avg. Density = 40.40
2. Angle of Friction = 38.63
3. Tan Theta = .7992
4. Cohesion = 242.12

A short horizontal line segment is drawn in the box to the right of "Angle of Friction" (u about 2155
to 2420, v about 927): a legend sample, not data. atan(.7992) = 38.63 deg, so the two printed angle
values agree with each other. Cohesion 242.12 is in psf (the intercept read below is about 250 psf;
in axis units, x 10^1, it would be 2421 psf, which the page rules out).

## Calibration (cal-p1/)

`calibrate_axes.py detect` with box 715 1052 2810 3445, 8 bands, x = 0..7000 psf (8 vertical lines,
labels 00 to 700.00), y = 0..8000 psf (9 horizontal lines, labels 00. to 800.00). All 17 lines
detected in 7 or 8 of 8 bands, none predicted; all 17 verified against the ink by the piecewise check
(x lines within 0.5 px of the ink at both ends, y lines within 1.3 px). Affine residuals: x RMS 4.1 psf
(max 9.2), y RMS 10.4 psf (max 19.7), 0.06 and 0.13 percent of the spans, under the 0.5 percent limit.
The grid is unevenly drawn: y spacing 287.5 to 299.7 px per 1000 psf (the 0 to 1000 interval is the
widest), x spacing 284.8 to 293.8 px; values come from the piecewise map, so this is read as drawn.

The plot frame continues about 490 px above the 800.00 line to enclose the text box; the frame top is
not a grid line and the detect box starts just above the 800.00 line. Label checks by eye
(calibration-eye-checks.csv): 5 y labels and 6 x labels, each centred within 5 px of its line except
800.00, printed 14 px above its line (still 293 px from the next line, so no ambiguity).

## Points (points-p1.csv, points-p1-native.csv, overlay-p1.png)

1. 6 markers, all `triangle-up`, centroids per rule 8: the triangle is reconstructed from its strokes
   (straight-line fits of the left and right side centres row by row, base centreline from the base
   rows; apex and base corners where they cross; helper `tri_sides.py`, grid lines and the fitted line
   masked where they touch). Side fits within 0.6 px RMS. Bounds 2 px across, 5.5 px (about height/6;
   heights 30 to 33 px) in the apex direction. The apex reconstructed from the sides lies 1 to 3 px
   above the visible ink top (the drawn apex is slightly blunt); the vertex-from-outer-ink estimate
   (`tri.py`) differs by at most 3 px in v, inside the bound. Marker 4 (about 2929, 2921 psf) has its
   apex merged into the y = 3000 grid line and its right base corner into the x = 3000 grid line
   (u bound 3 px). No overlapping symbols, no hidden symbol found along the line.
2. 11 trace samples: left end, x = 500 to 4500 every 500 psf, right end. Each interior sample is the
   local straight-line fit of the line's centre (midpoint of the dark run) over 32 to 41 columns
   (helper `trace.py`), which bridges the grid-line crossings at x = 1000, 2000, 3000, 4000. Bounds:
   0.5 px in u (a chosen abscissa), 7.5 px in v (half the line's vertical extent of 15 px; the line is
   about 12 px thick perpendicular to itself). The ends get 3.5 px in u.
3. 3 features: first point (= trace 1), last point (= trace 11, also the trace maximum), intercept.

The drawn line has two gaps where the pen was lifted around a symbol: u 935 to 968 (marker 2) and
u 1421 to 1447 (marker 3). No trace sample is in a gap. The line is straight on the page (centre RMS
0.96 px about one straight line over 409 columns).

Left end: the line's ink starts at the left frame (x = 0) and merges with the frame ink; there is no
ink of the line left of the frame. Its centre at the x = 0 line (u 740.2) is extrapolated from the
straight stretch u 760 to 930 (v 3332.9; the blob at the junction itself centres about 3 px higher).
This is also the intercept: the line reaches the normal-stress-zero axis.
Right end: the line ends inside the ink of the y = 4000 grid line, at about x = 4671 psf (the last
marker is at x = 4685). The pen-centre end is about u 2101, the last ink column u 2107; the sample is
placed between (u 2104.5) with a 3.5 px bound.

## Comparison with the printed box values (nothing was moved to agree)

1. Slope of the trace samples (least squares over the 11): 0.8000, against Tan Theta .7992: +0.0008
   (+0.10 percent). Interior end-to-end (x = 500 to 4500): 0.8011 (+0.24 percent).
2. Intercept feature: 250.0 psf, against Cohesion 242.12 psf: +7.9 psf (about 2.4 px), inside the
   sample's bound of 30.5 psf. The least-squares fit through the 11 trace samples gives 242.4 psf.
3. The trace samples scatter about their own straight line by -8 to +9 psf in a smooth bow (ends
   high, middle low). The line is straight on the page; the bow is the uneven grid drafting carried
   by the piecewise map (wider 0 to 1000 interval, narrower 4000 to 5000), a calibration effect, not
   a curvature of the drawn line.
   Against the printed equation (242.12 + .7992 x), the trace samples differ by +8 psf at x = 0,
   +1 to -5 psf from x = 1000 to 3500, +11 at 4500 and +13 at the right end: everywhere inside the
   samples' bounds (about 30 psf). The drawn line agrees with the printed values.
4. For information only: a least-squares line through the 6 read markers gives slope 0.8078 and
   intercept 243.7 psf (38.93 deg), close to the printed values.

## Ambiguities

1. Right end location along the line (pen-centre end against last ink column, 6 px apart); bounded.
2. Left end merges with the frame; its centre is an extrapolation of the line (about 3 px below the
   junction blob's centre); inside the 7.5 px bound.
3. Marker 4 touches two grid lines; centroid reconstructed from its strokes.

## Files

cal-p1/ (anchors.csv, calibration.json), calibration-eye-checks.csv, points-p1.csv,
points-p1-native.csv, overlay-p1.png, notes.md; helpers knots_check.py, tri_sides.py, tri.py,
trace.py, fitcheck.py; crops c_*.png, lab_*.png, m*.png, ov*.png, box.png.
