# FC-9B (Figure C-9B, RS Dense), printed page C-26, page image p0140.png

Reader: Claude (blind reading, batch curves-appc-b7). One panel, one series `rs-dense`.

## What is printed

Caption: "Figure C-9B. RS Dense". Box title: "RS DENSE" (matches the series id given in series.csv).
The four values in the box, as printed:

1. Avg. Density = 54.40
2. Angle of Friction = 46.65
3. Tan Theta = 1.0594
4. Cohesion = 698.23

atan(1.0594) = 46.65 deg, consistent. Cohesion read as psf. A short legend dash is drawn in the box
right of "Tan Theta" (u about 2135 to 2180, v about 1388); not data.

## Calibration (cal-p1/)

`calibrate_axes.py detect` with box 622 1452 2720 3832, 8 bands, x = 0..7000 psf (8 vertical lines,
labels 00 to 700.00), y = 0..8000 psf (9 horizontal lines, labels 00 to 800.00). The page is turned
by about 0.6 deg (vertical lines lean +0.010 du/dv). All 17 lines detected in 8 of 8 bands, none
predicted, all verified against the ink (within 0.7 px at both ends). Affine residuals: x RMS 4.1 psf
(max 10.3), y RMS 11.0 psf (max 22.7), 0.06 and 0.14 percent of the spans. Uneven drafting: y 287.5
to 298.9 px per 1000 psf (0 to 1000 widest, 4000 to 5000 narrowest), x 284.9 to 297.1 px (0 to 1000
widest); the piecewise map reads it as drawn.

The frame continues about 490 px above the 800.00 line around the text box; the detect box starts just
above the 800.00 line. Label checks by eye (calibration-eye-checks.csv): 5 y labels, 7 x labels, all
centred within 9 px of their line.

## Points (points-p1.csv, points-p1-native.csv, overlay-p1.png)

1. **4 markers** only, all `triangle-up` (about x = 1000, 2051, 2931, 4129 psf); none hidden along the
   line or elsewhere on the plot. Centroids per rule 8 from the side and base strokes (helper
   `tri_sides.py`; side fits within 0.6 px RMS; heights 31 to 33 px). Marker 1 has the x = 1000 grid
   line running through it (apex hidden); marker 2's left base corner is on the x = 2000 grid line;
   marker 3's right base corner merges with the x = 3000 grid line and with the fitted line; marker 4's
   base merges with the y = 5000 grid line (taken as the 6 rows just below it, v bound 6 px) and the
   fitted line's upper end runs into its left half. A stray horizontal stroke lies right of marker 1
   (u 1025 to 1110, v 3280), like the one beside FC-9A's marker 2; not data.
2. 8 trace samples: left end, x = 500, 1500, 2500, 3000, 3500, 4000, right end as seen. v bound 9 px
   (half the 18 px vertical extent), u bound 0.5 px at chosen abscissae.
   **x = 1000 and x = 2000 are not sampled.** x = 2000 falls in the drawn gap around marker 2 (no ink,
   u 1222 to 1258). x = 1000 falls where the segment below marker 1 ends, under the x = 1000 grid
   line: whether the line's ink reaches u 948.7 cannot be seen (no line ink right of the grid line
   below the symbol).
3. 3 features: first point (= trace 1), last visible point (= trace 8), intercept.

Gaps in the drawn line: around marker 1 (ink ends under the x = 1000 grid line, resumes at u 967) and
marker 2 (u 1222 to 1258). The line runs through marker 3's base corner without a gap. Centre RMS
about one straight line: 0.71 px over 343 columns.

Left end: the ink starts at the left frame (x = 0), with a small cap bulging 2 px right of the frame;
centre at the x = 0 line extrapolated from u 668 to 935 (v 3618.0). This is the intercept.
Right end: the line runs into the base of marker 4 and the y = 5000 grid line at about x = 4051 psf;
any continuation under that ink (to about x = 4130, the marker's x) is hidden, so the last point is
the last visible one.

## Comparison with the printed box values (nothing was moved to agree)

1. Slope of the trace samples (least squares over the 8): 1.0577, against Tan Theta 1.0594: -0.0017
   (-0.16 percent). Interior end-to-end (x = 500 to 4000): 1.0590 (-0.04 percent).
2. Intercept feature: 681.1 psf, against Cohesion 698.23 psf: -17.2 psf (about 5 px), inside the
   sample's bound of 33 psf. The fit through the trace samples gives 672.6 psf.
3. **The drawn line lies below the printed equation everywhere**: -17 psf at x = 0, -22 at 500, -37 at
   1500, -41 at 2500, -39 at 3000, -34 at 3500, -24 at 4000. In the mid-range (x = 1500 to 3500) the
   difference (34 to 41 psf, 10 to 12 px) exceeds the samples' bounds (about 33 psf): the printed
   equation's line would run along the upper edge of the drawn line's ink or just above it. Part of
   the shape is the uneven grid carried by the piecewise map (the trace samples bow by -11 to +9 psf
   about their own straight line, while the line is straight on the page); the offset of about
   -17 to -24 psf at the ends is not explained by that bow. This is a disagreement between the
   drawn line and the printed values, recorded as found.
4. For information only: a least-squares line through the 4 read markers gives slope 1.0444 and
   intercept 727.5 psf (46.24 deg).

## Ambiguities

1. x = 1000 trace sample omitted (end of a segment hidden under a grid line).
2. The line's right end is hidden under marker 4's base; the last point is the last visible one.
3. Marker 4's base merges with the y = 5000 grid line; base position assumed (bounded).

## Files

cal-p1/ (anchors.csv, calibration.json), calibration-eye-checks.csv, points-p1.csv,
points-p1-native.csv, overlay-p1.png, notes.md; helpers knots_check.py, tri_sides.py, tri.py,
trace.py, fitcheck.py; crops c_*.png, lab_*.png, ov*.png, box.png.
