# FC-9C (Figure C-9C, RS Dense), printed page C-27, page image p0141.png

Reader: Claude (blind reading, batch curves-appc-b7). One panel, one series `rs-dense`.

## What is printed

Caption: "Figure C-9C. RS Dense". Box title: "RS DENSE" (matches the series id given in series.csv).
The four values in the box, as printed:

1. Avg. Density = 54.30
2. Angle of Friction = 49.39
3. Tan Theta = 1.1663
4. Cohesion = 700.44

atan(1.1663) = 49.39 deg, consistent. Cohesion read as psf. No legend line in this box.

## Calibration (cal-p1/)

`calibrate_axes.py detect` with box 530 1402 2615 3782, 8 bands, x = 0..7000 psf (8 vertical lines,
labels 00 to 700.00), y = 0..8000 psf (9 horizontal lines, labels 00 to 800.00). All 17 lines
detected in 8 of 8 bands, none predicted, all verified against the ink (within 0.9 px at both ends).
Affine residuals: x RMS 4.2 psf (max 8.9), y RMS 10.2 psf (max 18.6), 0.06 and 0.13 percent of the
spans. Uneven drafting: y 285.3 to 299.0 px per 1000 psf (0 to 1000 widest, 4000 to 5000
narrowest), x 286.2 to 295.7 px; the piecewise map reads it as drawn.

The frame continues about 490 px above the 800.00 line around the text box; the detect box starts just
above the 800.00 line. Label checks by eye (calibration-eye-checks.csv): 5 y labels and 8 x labels,
all within 11 px of their line (the y labels sit with their baseline near the line).

## Points (points-p1.csv, points-p1-native.csv, overlay-p1.png)

1. **11 markers**, all `triangle-up`. Centroids per rule 8 from the side and base strokes (helper
   `tri_sides.py`, grid lines and the fitted line masked where they touch; side fits within 0.8 px
   RMS; heights 30 to 34 px). Bounds 2 to 3 px across, 5.5 px in the apex direction.
   - Marker 1 (about x = -10, y = 471 psf) straddles the left frame: the x = 0 line runs through it,
     its base does not close at the right corner, and its centroid is 3 px left of the x = 0 line
     (flagged `extrapolated x` by the tool). It is a plotted symbol at zero normal stress.
   - Marker 6's left side runs along the x = 2000 grid line and cannot be fitted: its centroid uses
     the right side and the base with the triangle's axis through the apex (u bound 3 px).
   - Grid lines run through markers 2 (y = 1000), 4 (x = 1000, through the apex), 10 and 11
     (y = 5000); marker 8's right base corner merges with the x = 3000 grid line.
   - Markers 8 and 9 have nearly the same normal stress (x about 2942 and 2921 psf) at different
     shear stresses (4498 and 3869 psf); they are two separate symbols, 180 px apart.
2. 9 trace samples: left end, x = 500, 1500, 2000, 2500, 3000, 3500, 4000, right end. v bound 9 px
   (half the 18 px vertical extent), u bound 0.5 px at chosen abscissae.
   **x = 1000 is not sampled**: the line is interrupted around marker 4 there (lower segment's ink ends
   at about u 828, the upper segment's ink starts at about u 856 behind the x = 1000 grid line), so
   no line ink can be seen at u 852.6.
3. 3 features: first point (= trace 1), last point (= trace 9, the trace maximum), intercept.

Gaps in the drawn line around markers 2 (about u 625 to 650), 3 (about u 732 to 746) and 4 (u 828 to
856). Centre RMS about one straight line: 1.17 px over 343 columns; local slopes on the page vary
from -1.154 to -1.175 between stretches, i.e. the line is straight to about 1.5 px.

Left end: the ink starts at the left frame (x = 0) and merges with it (no ink left of the frame);
centre at the x = 0 line extrapolated from the stretches u 568 to 618 and 655 to 725 (3558.5 and
3559.1; taken 3559.0). This is the intercept. Right end: pen-centre end about u 1742, ink extreme
about u 1746 at v 2182; sample at u 1744 (x = 4087 psf); the last marker is at x = 4119.

## Comparison with the printed box values (nothing was moved to agree)

1. Slope of the trace samples (least squares over the 9): 1.1531, against Tan Theta 1.1663: -0.0132
   (-1.13 percent). Interior end-to-end (x = 500 to 4000): 1.1541 (-1.05 percent).
2. Intercept feature: 686.4 psf, against Cohesion 700.44 psf: -14.0 psf (about 4 px), inside the
   sample's bound of 32 psf. The fit through the trace samples gives 674.3 psf.
3. **The drawn line lies well below the printed equation over most of its length**: -14 psf at x = 0,
   -26 at 500, -51 at 1500, -67 at 2000, -74 at 2500, -76 at 3000, -70 at 3500, -69 at 4000, -68 at
   the right end. From x = 1500 on, the difference (51 to 76 psf, 15 to 22 px) is larger than the
   samples' bounds (about 33 psf): at x = 3000 the printed equation's line would run about 13 px above
   the top edge of the drawn line's ink. The drawn line is straight on the page; the trace samples bow
   by -14 to +12 psf about their own straight line because of the uneven grid, which does not account
   for a 70 psf offset. This is a real disagreement between the drawn line and the printed values,
   recorded as found.
4. For information only: a least-squares line through the 11 read markers gives slope 1.1533 and
   intercept 710.9 psf (49.07 deg): its slope matches the drawn line's, its intercept is 25 psf above
   the drawn line's and 10 psf above the printed cohesion.

## Ambiguities

1. Marker 1 sits on the frame with an incomplete base; its centroid is just outside the plot (x about
   -10 psf).
2. Marker 6's left side is hidden by a grid line (symmetry used).
3. x = 1000 trace sample omitted (gap around marker 4 behind a grid line).

## Files

cal-p1/ (anchors.csv, calibration.json), calibration-eye-checks.csv, points-p1.csv,
points-p1-native.csv, overlay-p1.png, notes.md; helpers knots_check.py, tri_sides.py, tri.py,
trace.py, fitcheck.py; crops c_*.png, lab_*.png, ov*.png, box.png.
