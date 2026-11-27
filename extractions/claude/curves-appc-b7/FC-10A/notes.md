# FC-10A (Figure C-10A, PS Loose), printed page C-28, page image p0142.png

Reader: Claude (blind reading, batch curves-appc-b7). One panel, one series `ps-loose`.

## What is printed

Caption: "Figure C-10A. PS Loose". Box title: "PS Loose" (matches the series id given in series.csv).
The four values in the box, as printed:

1. Avg. Density = 25.90
2. Angle of Friction = 43.44
3. Tan Theta = .9471
4. Cohesion = 488.69

atan(.9471) = 43.44 deg, consistent. Cohesion read as psf. A short dash follows the box title and
another short dash is drawn inside the plot just below the 800.00 line (u about 1322 to 1395, v about
1481); neither is data.

## Calibration (cal-p1/)

`calibrate_axes.py detect` with box 575 1377 2700 3762, 8 bands, x = 0..7000 psf (8 vertical lines,
labels 00 to 700.00), y = 0..8000 psf (9 horizontal lines, labels 00 to 800.00). The page is turned
by about 0.9 deg (vertical lines lean +0.016 du/dv, horizontal lines -0.010 dv/du). All 17 lines
detected in 8 of 8 bands, none predicted, all verified against the ink (within 0.9 px at both ends).
Affine residuals: x RMS 3.6 psf (max 7.3), y RMS 9.9 psf (max 18.1), 0.05 and 0.12 percent of the
spans. Uneven drafting: y 287.9 to 299.9 px per 1000 psf (0 to 1000 widest, 4000 to 5000
narrowest), x 285.6 to 294.3 px; the piecewise map reads it as drawn.

The frame continues about 490 px above the 800.00 line around the text box; the detect box starts just
above the 800.00 line. Label checks by eye (calibration-eye-checks.csv): 5 y labels and 8 x labels,
all within 9 px of their line.

## Points (points-p1.csv, points-p1-native.csv, overlay-p1.png)

1. 6 markers, all `triangle-up`, drawn with a slightly heavier stroke than on FC-8 to FC-9C (side
   runs 7 to 9 px). Centroids per rule 8 from the side and base strokes (helper `tri_sides.py`, the
   fitted line and grid lines masked where they touch; side fits within 0.6 px RMS; heights 27 to 29
   px). Bounds 2 px across, 5 px in the apex direction. Marker 1: the fitted line passes just left of
   its apex. Marker 5: the y = 4000 grid line hides its apex. Marker 6: the line's upper end runs into
   its left side (left side fitted on 8 rows only, u bound 2.5 px). Stray horizontal strokes run right
   from the bases of markers 2 and 6; not part of the symbols, not data.
2. 10 trace samples: left end, x = 500 to 4000 every 500 psf, right end. v bound 7.5 px (half the
   15 px vertical extent; 8 to 8.5 px at the ends and on the last segment), u bound 0.5 px at chosen
   abscissae. Each interior sample is the local fit of the line's centre on its own segment.
   x = 1500 falls on the end cap where the segment after the gap around marker 2 starts (ink present,
   centre of the cap agrees with the segment's fit to 0.1 px).
3. 3 features: first point (= trace 1), last point (= trace 10, the trace maximum), intercept.

Gaps in the drawn line around markers 2 (u about 1030 to 1062), 4 (about 1462 to 1480) and 5 (about
1652 to 1678, where the line also crosses the y = 4000 grid line). Each segment is straight within
0.4 to 0.7 px RMS. The first three segments are collinear within 1 px; **the last segment (u 1680 to
the end) is drawn about 2 px thicker and its centre lies about 4 px below the extension of the
others** (an offset of about 13 psf at x = 4000, inside the samples' bounds).

Left end: the ink starts at the left frame (x = 0) and merges with it; the junction's centre
(3594.9) sits about 3.7 px above the first segment's extrapolation (3598.6); the sample is taken
between (3596.5, v bound 8 px). This is the intercept. Right end: the line's end cap runs into the
left side of marker 6; pen-centre end about u 1867 to 1869, sample at u 1868.5 (x = 4301 psf); the
last marker is at x = 4355.

## Comparison with the printed box values (nothing was moved to agree)

1. Slope of the trace samples (least squares over the 10): 0.9578, against Tan Theta .9471: +0.0107
   (+1.13 percent). Interior end-to-end (x = 500 to 4000): 0.9579 (+1.14 percent).
2. Intercept feature: 509.2 psf, against Cohesion 488.69 psf: +20.5 psf (about 6 px), inside the
   sample's bound of 29 psf. The fit through the trace samples gives 499.3 psf.
3. **The drawn line lies above the printed equation everywhere, increasingly to the right**: +21 psf
   at x = 0, +14 at 500, +21 at 1000, +25 at 1500, +27 at 2000, +30 at 2500, +40 at 3000, +52 at
   3500, +52 at 4000, +65 at the right end (x = 4301). From x = 3000 on, the difference (40 to 65
   psf, 12 to 19 px) exceeds the samples' bounds (29 to 33 psf). The trace samples scatter about their
   own straight line by -8 to +10 psf (uneven grid, plus the last segment's 4 px offset), which does
   not account for this. This is a real disagreement between the drawn line and the printed values,
   recorded as found.
4. For information only: a least-squares line through the 6 read markers gives slope 0.9573 and
   intercept 502.5 psf (43.75 deg), close to the drawn line (0.9578, 499.3) and, like it, steeper
   and higher than the printed values.

## Ambiguities

1. Left end centre at the frame junction (3.7 px spread between the junction and the extrapolation);
   bounded.
2. Right end merges with marker 6's left side.
3. The last segment's offset from the rest of the line (drafting or scan), recorded, not corrected.

## Files

cal-p1/ (anchors.csv, calibration.json), calibration-eye-checks.csv, points-p1.csv,
points-p1-native.csv, overlay-p1.png, notes.md; helpers knots_check.py, tri_sides.py, tri.py,
trace.py, fitcheck.py; crops c_*.png, lab_*.png, ov*.png, box.png.
