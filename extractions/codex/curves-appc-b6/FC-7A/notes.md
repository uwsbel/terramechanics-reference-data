# FC-7A: independent reading, panel 1

Source: packet/p0135.png, original unrotated 300-dpi image, pixel coordinates u right / v down. Only this packet was consulted. The context page p0115.png identifies Appendix C as direct shear data from Notre Dame, with the C-5A exception.

## Calibration

All interior calibration lines are actual detected printed grid lines; none are predicted. The affine map and detected-line samples are in cal-p1/calibration.json, with 42 anchors on C-5A/C-6A and 56 on C-7A. The frame box is [620, 940, 2560, 3175].

RMS residual x / y: 0.026014 / 0.031288 native units. Maximum residual x / y: 0.053255 / 0.080176. These are below 0.5% of the axis spans. Three printed labels per axis were checked independently against the tick/grid intersections read by eye, recorded in calibration-eye-checks.csv and shown in cal-p1/eye-label-checks.png. Position differences are compared to the 4-pixel eye bound plus the calibration RMS. C-5A's upper frame is unlabelled; its value 6000 follows the printed 1000-psf spacing, and it is not one of the three printed-label checks.

## Reading conventions

Markers were read first, from the labelled zoomed crops. Clear circle/square centers have 2-pixel bounds; overlaps are widened. Triangles use reconstructed centroids, with v bounds at least one sixth of their reconstructed height. No hidden data-sheet readings were available or used. Blank series_id means identity unresolved; it does not create a new density series.

Trace guide equations in read_helpers.py only locate the ink. Samples themselves use the center of a visible ink run, checked in trace-checks-*.png. A guide is never used to fill a dash gap. Sampling proceeds from the left ink end at nominal 250-psf intervals (2 psi on C-7A), ending at the last ink; labels and marker rims are avoided. Where the nominal abscissa falls in a dash/erasure gap, marker, or grid merge, the sample is moved to the nearest clean part of the same line, with the nominal target in its note. Thus x_native can differ from the nominal target. Bounds are half the measured stroke thickness perpendicular to the line, expressed as a conservative equal u/v radius. Endpoint bounds use the typical full stroke, rather than the thin cap or thick frame. C-5A's converging fits have fused ink near the origin, noted on affected trace rows.

The intercept features use the drawn straight line's meeting with the calibrated x=0 axis; short obscured joins or gaps are reconstructed locally, with widened feature bounds. They are geometric features, not additional test markers. First, maximum, and last line roles are carried by the endpoint trace rows; a straight rising fit has no knee. Angle-label features are at the printed text's center, not points on the fit. The native-unit CSV is generated with tools/calibrate_axes.py apply, including calibration RMS in its read bounds.

## Counts

| Series | Marker | Trace | Feature |
|---|---:|---:|---:|
| dr53 | 6 | 15 | 2 |
| dr100 | 6 | 15 | 2 |

## Legend, line labels, and ambiguities

The legend prints RSM-b Soil; dotted circles: gamma 82 Lb/ft^3, Dr 0.53; dotted upright triangles: gamma 89 Lb/ft^3, Dr 1.0. IDs dr53 and dr100 are retained. The axes print **Normal Load - PSI** and **Shear Load - PSI**; the caption's Normal Shear Stress wording does not change the axis quantities.

The lower dotted-circle fit carries **45°**, not 46° (confirmed in angle-detail.png). The steeper dotted-triangle fit carries **50.5°**. Both have dashed extensions reaching the shear-load axis. The 50.5° line ends at the top frame; the last triangle is a separate marker below and to the right of that ink endpoint. The 45° fit also continues beyond the upper-left side of its last circle, ending near (2309,1377), not at that circle's center.

Central dots are visible in both symbol groups and are preserved in the symbol descriptions. Triangle points are centroids, not their dots or bounding-box midpoints. Some symbols overlap grid lines and fits, particularly the circle/triangle pair near normal load 10 psi; their bounds are widened. No additional unidentified marker was found.
