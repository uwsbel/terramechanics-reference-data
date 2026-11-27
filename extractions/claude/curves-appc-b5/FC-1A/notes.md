# FC-1A, Claude reading (batch curves-appc-b5)

Source: AM-68-1 Vol. II (NASA CR-92215), Appendix C, Figure C-1A, printed C-2, page image
`packet/p0116.png` (300 dpi, unrotated). One upright panel, failure envelopes of RS soil: maximum
shear stress (psf) against normal stress (psf). Pixel coordinates are those of `p0116.png`.

## 1. Calibration

1. `tools/calibrate_axes.py detect` with box `905 1567 2125 3325`, x values 0 to 4000 step 1000,
   y values 0 to 6000 step 1000, default thresholds. All 12 gridlines were found in 5 of 5 bands;
   no line is `predicted`.
2. Residuals: x rms 23.87 psf (0.60 % of the 4000 psf span, max 31.8 psf); y rms 10.18 psf
   (0.17 % of the 6000 psf span, max 19.8 psf). **The x residual is above the 0.5 % threshold.**
3. Cause: the printed grid itself is unevenly spaced. Between the drawn vertical lines there are
   286.3, 287.2, 294.5 and 311.5 px per 1000 psf (left to right); horizontal spacings run from
   281.9 to 294.7 px. Every printed axis label sits on its drawn gridline (within 1 to 5 px, see
   `calibration-eye-checks.csv`: 5 x labels and 7 y labels checked by eye on zoomed crops and
   confirmed by ink extents), so the labels and lines are right and an affine map cannot follow
   the drawing exactly.
4. As the protocol asks, the box and thresholds were changed before reading points: a tighter
   box with 9 bands gave x rms 23.98 psf, and `--dark 140 --min-frac 0.5` gave 23.96 psf (both kept
   under `work/cal-variant-a`, `work/cal-variant-b`). The residual is a property of the drawing,
   not of the detection, so the first fit (`cal-p1/`) is used.
5. Consequence for users: affine x values differ from a local reading against the nearest drawn
   gridlines by up to about 32 psf. The drawn shear-stress axis (normal stress 0) reads x = +23
   to +27 psf; points between 2000 and 3000 psf read about 27 psf low; the 4000 line reads +32.
   y values differ by up to about 20 psf (largest at the 6000 line, outside the data).

## 2. Lines and printed angles

| line (on the page) | printed label | label center (u, v) | series | slope of the drawn line |
|---|---|---|---|---|
| upper, steepest | 51° | (1687.5, 2055.0) | dr100-116 (triangles) | 52.2 deg (affine), 52.0 deg (local grid) |
| middle | 47° | (1684.5, 2233.0) | dr73-88 (filled circles) | 47.7 deg (affine), 47.5 deg (local grid) |
| lower | 45.5° | (1811.5, 2214.0) | dr50-57 (open circles) | 46.1 deg (affine), 45.9 deg (local grid) |

1. Each label is written along its line on the upper-left side, at 45 to 48 px (perpendicular,
   label center to line centerline) from that line. "51°" is 45 px above the upper line. "47°"
   sits between the upper and middle lines, 48 px from the middle one and 63 px from the upper.
   "45.5°" sits between the middle and lower lines and is in fact nearer the middle line (32 px)
   than the lower one (46 px); it is assigned to the lower
   line because of the consistent upper-left placement of all three labels and because the slope
   order of the lines matches the order of the printed angles. Flag for review.
2. The drawn lines are 0.4 to 1.2 deg steeper than their printed angles, in either calibration
   (a straight fit to my trace samples). The ordering agrees; the printed angles were presumably
   computed, the lines drawn by hand.
3. Structure of each line: dashed from the shear-stress axis to the symbol near 600 psf, solid
   from there on. Upper line: dashes reach the axis; solid from the triangle at u 1091.7. Middle
   line: dashes reach the axis; solid from the open circle at u 1092.4 (the line is interrupted
   around that circle). Lower line: the dashes do **not** reach the axis; the first dash stops at
   the upper-right corner of the triangle drawn on the axis (u 945), so its intercept is an
   extrapolation of 20 px along a straight fit to the dashed part (rms 0.95 px); solid from the
   open circle at u 1102.4.
4. Intercepts (where the line meets the drawn axis): upper (927.0, 3087.5), y = 769 psf; middle
   (927.1, 3117.5), y = 665 psf; lower (927.3, 3179.3), y = 450 psf (all with x about +24 psf
   from the calibration residual at the axis).
5. Right ends: upper line ink ends at u 1972 (end sample 3571 psf); middle at u 1959 (3536 psf);
   lower line ends against the outline of its last circle at u 1940 (end sample 3464 psf), so
   that line has no 3500 psf sample.

## 3. Legend and symbols

1. Legend as printed: "RS SOIL"; open circle, gamma = 46.7 to 47.4 Lb./Ft.^3 (Dr = .50 to .57);
   filled circle, gamma = 49.2 to 51.1 (Dr = .73 to .88); upward triangle, gamma = 53 to 55.4
   (Dr = 1.0 to 1.16). The Dr ranges match the series ids given in `series.csv`.
2. **All seven plotted triangles point down**, while the legend shows an upward triangle. They are
   recorded as `triangle-down`.
3. 20 symbols in all: 9 open circles, 4 filled circles, 7 downward triangles. A search for every
   enclosed white hole in the plot and for bulges along the three lines found no other symbol.
4. Centers: hollow symbols at the centroid of their enclosed white interior (for a triangle this is
   the incenter; the center of the outline's bounding box is about 3.5 px lower, so triangles carry
   a v bound of 3 px); filled circles at the midpoint of their disk edges. Clean markers 2 px,
   markers merged with a line or gridline 2.5 px.
5. The axis titles print as "max (PSF)" and "(PSF)"; the Greek letters (tau, sigma) are not visible
   in the scan.

## 4. Identity calls (symbols that do not match their line)

The task rule is: where a symbol of another shape or fill sits on a group's line, assign it by the
line. Four symbols are affected. I followed the rule for two and departed from it for two, where
the page gives evidence against the line; both readings are written into each point's note.

1. Open circle at (1092.4, 2916.5), 586 psf: the solid part of the 47° line starts at this circle
   (the line is broken around it and tangent to its lower-right); 67 px above the 45.5° line.
   **dr73-88 by the line** (rule followed).
2. Open circle at (1608.6, 2412.9), 2343 psf: tangent to the solid 47° line (19 px below its
   centerline), 51 px above the 45.5° line, and dr50-57 already has an open circle at this normal
   stress on its own line (u 1611.3). **dr73-88 by the line** (rule followed).
3. Filled circle at (1012.8, 3087.6), 315 psf: sits on the **dashed extension** of the 45.5° line
   (3 px from its centerline), 42 px below the 47° dashed line. **Kept dr73-88 by legend**
   (departs from the literal rule, which gives dr50-57). Reasons: the fill matches the legend; the
   dashed parts are extrapolations that start below the 600 psf point of every line, so they are
   not drawn through the 300 psf points (the lowest open circle lies 31 px off its own dashed
   part); dr50-57 already has its 300 psf point (open circle at u 1006.5) while dr73-88 has no
   other; this circle has the same normal stress as the triangle at u 1014.3 (1 px apart), while
   the open circle is 7 px to the left; and the two open circles in items 1 and 2 show that
   dr73-88 symbols were sometimes left unfilled, not that other groups' symbols were filled.
   If the rule is to be applied literally, change this row to dr50-57.
4. Triangle at (928.3, 3169.5), on the drawn axis (normal stress 0 as drawn, 485 psf): the 45.5°
   dashed line stops at its upper-right corner and would pass 7 px below its center; it is 51 px
   below the 51° dashed line. **Kept dr100-116 by shape** (the only triangle group; departs from
   the literal rule, which gives dr50-57). This is the least certain call on the page: it may be a
   dr100-116 test at zero normal stress lying 288 psf under its line, a dr50-57 point drawn with the
   wrong symbol, or a mark at the 45.5° intercept rather than a test. The axis ink is interrupted
   inside the symbol, so it was drawn over the axis on purpose. Needs the response sheets
   (FC-1B to FC-1D) to settle.

With these calls each group has one test per normal stress level: dr50-57 at 293, 620, 1184,
1789, 2352, 2918, 3502 psf; dr73-88 at 315, 586, 1770, 2343, 2932, 3514 psf; dr100-116 at 27(?),
321, 584, 1557, 2355, 2933, 3525 psf.

## 5. Trace samples

1. Samples at every 250 psf of calibrated normal stress, on the center of the line's vertical ink
   run in the chosen column; bound = half the line's perpendicular thickness (upper 5.3 px, middle
   4.8 px, lower 5.3 px), in u and in v.
2. Where the target column falls on a vertical gridline, on a crossing with a horizontal gridline,
   in a dash gap, or in a gap where the line is broken at a symbol, the sample was moved to the
   nearest clean column (2 to 13 px) and the note gives the target and the shift. No sample sits on
   a symbol outline or in a white gap.
3. Left ends: upper and middle lines on the axis centerline (their dashes reach the axis; the
   dash centerline is extrapolated 3 px into the axis ink); lower line at the end of its first
   dash (947.0, 3156.0), which is not on the axis.
4. Breaks in the lines: upper line at the triangle near 1500 psf (u 1361 to 1375) and at the
   triangle near 2930 psf plus the 3000 psf gridline (u 1777 to 1804); lower line at its circles
   (u 1593 to 1620, 1773 to 1791) and at the 3000 psf gridline. The vertical 3000 psf gridline is
   erased behind the "45.5°" label (about v 2195 to 2285).

## 6. Counts

| series | marker | trace | feature |
|---|---|---|---|
| dr50-57 | 7 | 15 | 2 |
| dr73-88 | 6 | 16 | 2 |
| dr100-116 | 7 | 16 | 2 |

Files: `cal-p1/` (anchors.csv, calibration.json), `calibration-eye-checks.csv`, `points-p1.csv`,
`points-p1-native.csv`, `overlay-p1.png`, this file; reader's scripts and crops under `work/` and
`crops/`.
