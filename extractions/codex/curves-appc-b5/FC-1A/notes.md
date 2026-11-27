# Independent packet reading: FC-1A

Read only the supplied page images, introduction, protocol and series identifiers. No external or other-reader extraction consulted. Figure-index reading/notes columns were not used as measurements or identity evidence. All coordinates refer to the unrotated 300 dpi page.

## Calibration

Affine RMS residuals: x 23.927 psf; y 9.974 psf. Maximum residuals: x 32.585; y 18.155 psf.
Six independent printed-label checks (three per axis) are recorded in calibration-eye-checks.csv and visually documented in cal-p1/eye-checks.png. Increasing normal stress is rightward; increasing shear stress is upward. Both quantities use psf.

All grid lines were detected and confirmed. No predicted grid line was used. The x RMS residual is 0.598% of the 4000 psf span, exceeding the 0.5% protocol flag. I changed the box from 920,1570,2110,3315 to 914,1568,2113,3316 and changed bands/dark/fraction from 5/200/0.6 to 9/140/0.5 before reading points. Residual remained about 24 psf because the printed grid is uneven (successive x spacings roughly 285-311 pixels). The residual is retained in all native reading bounds; it has not been concealed by using predicted evenly spaced lines.

## Series, printed legend and angle associations

- dr50-57: printed angle 45.5°; markers 9, trace samples 15, features 2 (intercept and printed angle center).
- dr73-88: printed angle 47°; markers 4, trace samples 16, features 2 (intercept and printed angle center).
- dr100-116: printed angle 51°; markers 7, trace samples 16, features 2 (intercept and printed angle center).

Legend: hollow circle, gamma 46.7 to 47.4 lb/ft^3, Dr .50 to .57; filled circle, gamma 49.2 to 51.1, Dr .73 to .88; upward triangle, gamma 53 to 55.4, Dr 1.0 to 1.16. The lower, middle and upper drawn fits carry 45.5°, 47° and 51° respectively.
The plot triangles point downward. The triangle at (928.3,3169.5) is on the lower dashed fit at the axis, so it is recorded as dr50-57, with a 14 pixel bound for axis overlap and the legend mismatch. The filled circle near (1013,3089) is on the lower dashed fit and is assigned dr50-57 despite its fill. Hollow circles near (1092.4,2916.5) and (1608.6,2412.9) sit by the middle fit and are assigned dr73-88 despite their fill.
The filled circle near (1440.5,2482) lies much closer to the upper fit than to the middle fit; it is assigned dr100-116 by that line neighborhood, with a 7 pixel bound and an explicit identity caveat. It is off the line, so this assignment is less secure than the triangle assignments. The lower circle at (1777.6,2318.6) is close to the vertical grid and fit; its bound is widened to 5 pixels.
The lower fit intercept is obscured by the axis triangle: its feature has a 15 pixel bound. Its first trace sample is the actual first visible dash beyond the triangle, not the triangle outline. The lower solid fit ends before the last circle; the right endpoint is on that line cap rather than on the circle or horizontal grid. No hidden additional marker is inferred.

## Ink sampling and bounds

Markers were read before trace sampling and reviewed at 3x enlargement. Every symbol is retained with its drawn shape. Clean marker centers use 2 pixel bounds; overlap and identity caveats use the stated wider bounds.
Every trace sample is on visible fitted-line ink, excluding all marker neighborhoods. Endpoints were separately checked on enlarged packet crops. Regular targets are every 250 psf from the left, followed by the observed right cap. When a target falls in a dash gap, marker neighborhood or grid interference, the nearest visible line ink is read and the target/actual x difference is noted. No sample was inserted by interpolation into a white gap. Samples on dashed portions are marked dashed. Sample bounds are half the observed line thickness (column thickness, including diagonal projection); endpoint bounds use the adjacent cap stroke width, not marker size. Only the hidden intercept feature uses an extrapolated location with a wide bound.
Sequences are independent within each series and kind. Trace order is left-to-right drawing order. The first and last trace samples also document the monotonic fitted line endpoints; the requested feature rows are intercept and label center. Angle label centers were measured from the printed glyph bounding boxes, including the degree sign.

Files: cal-p1/anchors.csv, cal-p1/calibration.json, cal-p1/eye-checks.png, calibration-eye-checks.csv, points-p1.csv, points-p1-native.csv, overlay-p1.png and notes.md. Additional marker, endpoint and trace crops are retained for review.
