# Independent packet reading: FC-3A

Read only the supplied page images, introduction, protocol and series identifiers. No external or other-reader extraction consulted. Figure-index reading/notes columns were not used as measurements or identity evidence. All coordinates refer to the unrotated 300 dpi page.

## Calibration

Affine RMS residuals: x 3.404 psf; y 12.825 psf. Maximum residuals: x 8.946; y 28.391 psf.
Six independent printed-label checks (three per axis) are recorded in calibration-eye-checks.csv and visually documented in cal-p1/eye-checks.png. Increasing normal stress is rightward; increasing shear stress is upward. Both quantities use psf.

There is no interior grid. The supplied detect command was run, but its grid assumption picked up legend borders (and, with sparse thresholds, curves) or interpolated nonexistent interior lines. The rejected trials are not the operative calibration. The operative cal-p1 files use every labeled bottom/left axis tick intersection measured on packet ink and the independently measured frame tilt. The same supplied fit_affine function fits those anchors; apply computes native values and bounds. Axis tick centers are recorded in calibration.json. No predicted interior grid lines are claimed or used. This tick-anchor adaptation is necessary to apply the protocol to these gridless figures.

## Series, printed legend and angle associations

- dr0-15: printed angle 38°; markers 5, trace samples 21, features 2 (intercept and printed angle center).
- dr100-130: printed angle 47°; markers 5, trace samples 21, features 2 (intercept and printed angle center).

Legend: hollow circle, gamma 57.9 to 59.4 lb/ft^3, Dr 0 to .15; square, gamma 75, Dr 1.0 to 1.3. These match the supplied identifiers. The lower circle-associated fit carries 38°; the upper square-associated fit carries 47°. The right-hand extensions are dashed as well as the left-hand intercept extensions. The upper endpoint is on the final dash below the top frame, not the top frame. No symbol identity conflict or hidden marker was observed.

## Ink sampling and bounds

Markers were read before trace sampling and reviewed at 3x enlargement. Every symbol is retained with its drawn shape. Clean marker centers use 2 pixel bounds; overlap and identity caveats use the stated wider bounds.
Every trace sample is on visible fitted-line ink, excluding all marker neighborhoods. Endpoints were separately checked on enlarged packet crops. Regular targets are every 250 psf from the left, followed by the observed right cap. When a target falls in a dash gap, marker neighborhood or grid interference, the nearest visible line ink is read and the target/actual x difference is noted. No sample was inserted by interpolation into a white gap. Samples on dashed portions are marked dashed. Sample bounds are half the observed line thickness (column thickness, including diagonal projection); endpoint bounds use the adjacent cap stroke width, not marker size. Only the hidden intercept feature uses an extrapolated location with a wide bound.
Sequences are independent within each series and kind. Trace order is left-to-right drawing order. The first and last trace samples also document the monotonic fitted line endpoints; the requested feature rows are intercept and label center. Angle label centers were measured from the printed glyph bounding boxes, including the degree sign.

Files: cal-p1/anchors.csv, cal-p1/calibration.json, cal-p1/eye-checks.png, calibration-eye-checks.csv, points-p1.csv, points-p1-native.csv, overlay-p1.png and notes.md. Additional marker, endpoint and trace crops are retained for review.
