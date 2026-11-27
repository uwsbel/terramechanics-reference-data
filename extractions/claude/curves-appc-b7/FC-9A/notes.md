# FC-9A (Figure C-9A, RS Dense), printed page C-25, page image p0139.png

Reader: Claude (blind reading, batch curves-appc-b7). One panel, one series `rs-dense`.

## What is printed

Caption: "Figure C-9A. RS Dense". Box title: "RS Dense" (matches the series id given in series.csv).
The four values in the box, as printed:

1. Avg. Density = 54.20
2. Angle of Friction = 52.55
3. Tan Theta = 1.3059
4. Cohesion = 634.20

atan(1.3059) = 52.56 deg, consistent with the printed angle to rounding. Cohesion is read as psf (the
intercept read below is about 622 psf). No legend line is drawn in this box.

## Calibration (cal-p1/)

`calibrate_axes.py detect` with box 630 1395 2715 3775, 8 bands, x = 0..7000 psf (8 vertical lines,
labels 00. to 700.00), y = 0..8000 psf (9 horizontal lines, labels 00 to 800.00). All 17 lines
detected (7 or 8 of 8 bands), none predicted, all verified against the ink (within 0.45 px at both
ends). Affine residuals: x RMS 3.7 psf (max 7.2), y RMS 10.4 psf (max 18.3), 0.05 and 0.13 percent
of the spans. Uneven drafting: y 285.6 to 299.7 px per 1000 psf (0 to 1000 widest, 4000 to 5000
narrowest), x 284.7 to 293.3 px; the piecewise map reads it as drawn.

The frame continues about 490 px above the 800.00 line around the text box; the detect box starts just
above the 800.00 line. A white blemish wipes the y = 4000 line right of about u 2050 and parts of the
x = 5000 line; both lines were still found in 7 of 8 bands and pass the ink check. Label checks by eye
(calibration-eye-checks.csv): 5 y labels and 7 x labels; the y labels on this page sit with their
baseline near their line (centres 5 to 16 px above it), the x labels within 9 px of their line.

## Points (points-p1.csv, points-p1-native.csv, overlay-p1.png)

1. 6 markers, all `triangle-up`, centroids per rule 8: triangle reconstructed from its strokes (fits
   of the side centres row by row, base centreline from the base rows; helper `tri_sides.py`, with
   grid lines and the fitted line masked where they touch; side fits within 0.6 px RMS). Bounds 2 px
   across, 5.5 px in the apex direction (heights 30 to 31 px). Marker 1 (about 303, 1042 psf) has its
   base on the y = 1000 grid line, merged with it: the base is taken as 6 px thick from its visible
   top edge (v bound 6 px). Marker 4 touches the fitted line at
   its right base corner (line pixels masked). Marker 5 (about 2929, 4542 psf) has its right base
   corner merged with the x = 3000 grid line (u bound 3 px). A stray horizontal stroke runs right
   from marker 2's base (u 845 to 923, v 3327 to 3330); it is not part of the symbol and not data.
2. 8 trace samples: left end, x = 500, 1000, 2000, 2500, 3000, 3500, right end. The line is steep
   (about 18 px vertical extent, 11 px thick across); v bound 9 px (half the vertical extent), u bound
   0.5 px at chosen abscissae.
   **x = 1500 is not sampled**: it falls in the drawn gap around marker 3 (the lower segment's ink
   ends at about u 1086, x 1495; the upper resumes at about u 1095, x 1525; no ink at x = 1500).
   x = 3000 sits exactly at the pen-centre start of the segment above the gap around marker 5, under
   the x = 3000 grid line; its centre comes from the columns to the right.
3. 3 features: first point (= trace 1), last point (= trace 8, the trace maximum), intercept.

Gaps in the drawn line (pen lifted around a symbol): u 730 to 752 (marker 1), 823 to 842 (marker 2),
1086 to 1095 (marker 3, ink), 1502 to 1516 (marker 5, ink). The line touches marker 4 without a gap.
Centre RMS about one straight line: 0.93 px over 295 columns.

Left end: the ink starts at the left frame (x = 0), no ink left of it; centre at the x = 0 line from
the line's fit (v 3565.4). This is the intercept. Right end: the line stops at about x = 3549 psf
(pen-centre end about u 1677.5, last ink about u 1682 at v 2198), inside the grid cell, below the
y = 6000 line; the last marker is at x = 3511.

## Comparison with the printed box values (nothing was moved to agree)

1. Slope of the trace samples (least squares over the 8): 1.3166, against Tan Theta 1.3059: +0.0107
   (+0.82 percent). Interior end-to-end (x = 500 to 3500): 1.3189 (+1.0 percent).
2. Intercept feature: 621.8 psf, against Cohesion 634.20 psf: -12.4 psf (about 3.6 px), inside the
   sample's bound of 33 psf. The fit through the trace samples gives 617.3 psf.
3. So the drawn line is slightly steeper than the printed equation (634.20 + 1.3059 x): -12 psf at
   x = 0, -13 at 500, -2 at 1000, -4 at 2000, +4 at 2500, +12 at 3000, +26 at 3500, +27 at the right
   end (x = 3549). All inside the samples' bounds (about 33 psf).
   The trace samples scatter about their own straight line by -9 to +6 psf, the uneven grid carried
   by the piecewise map (the line is straight on the page).
4. For information only: a least-squares line through the 6 read markers gives slope 1.2825 and
   intercept 719.9 psf (52.06 deg), noticeably different from the printed 1.3059 and 634.20. The
   drawn line agrees with the printed values better than the read markers do; either the printed fit
   used values that differ from the plotted symbols, or more tests than the six plotted. Not resolved
   from this page.

## Ambiguities

1. Marker 1's base is hidden in the y = 1000 grid line ink (base thickness assumed 6 px like the
   other symbols).
2. Right end location along the line (pen-centre against ink end, about 4.5 px apart); bounded.
3. The stray stroke at marker 2: a drafting or scanning artefact, left out.

## Files

cal-p1/ (anchors.csv, calibration.json), calibration-eye-checks.csv, points-p1.csv,
points-p1-native.csv, overlay-p1.png, notes.md; helpers knots_check.py, tri_sides.py, tri.py,
trace.py, fitcheck.py; crops c_*.png, lab_*.png, m*.png, box.png.
