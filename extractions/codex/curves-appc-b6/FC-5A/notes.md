# FC-5A: independent reading, panel 1

Source: packet/p0129.png, original unrotated 300-dpi image, pixel coordinates u right / v down. Only this packet was consulted. The context page p0115.png identifies Appendix C as direct shear data from Notre Dame, with the C-5A exception.

## Calibration

All interior calibration lines are actual detected printed grid lines; none are predicted. The affine map and detected-line samples are in cal-p1/calibration.json, with 42 anchors on C-5A/C-6A and 56 on C-7A. The frame box is [790, 1250, 2300, 3040].

RMS residual x / y: 4.969617 / 7.582867 native units. Maximum residual x / y: 8.709032 / 15.409157. These are below 0.5% of the axis spans. Three printed labels per axis were checked independently against the tick/grid intersections read by eye, recorded in calibration-eye-checks.csv and shown in cal-p1/eye-label-checks.png. Position differences are compared to the 4-pixel eye bound plus the calibration RMS. C-5A's upper frame is unlabelled; its value 6000 follows the printed 1000-psf spacing, and it is not one of the three printed-label checks.

## Reading conventions

Markers were read first, from the labelled zoomed crops. Clear circle/square centers have 2-pixel bounds; overlaps are widened. Triangles use reconstructed centroids, with v bounds at least one sixth of their reconstructed height. No hidden data-sheet readings were available or used. Blank series_id means identity unresolved; it does not create a new density series.

Trace guide equations in read_helpers.py only locate the ink. Samples themselves use the center of a visible ink run, checked in trace-checks-*.png. A guide is never used to fill a dash gap. Sampling proceeds from the left ink end at nominal 250-psf intervals (2 psi on C-7A), ending at the last ink; labels and marker rims are avoided. Where the nominal abscissa falls in a dash/erasure gap, marker, or grid merge, the sample is moved to the nearest clean part of the same line, with the nominal target in its note. Thus x_native can differ from the nominal target. Bounds are half the measured stroke thickness perpendicular to the line, expressed as a conservative equal u/v radius. Endpoint bounds use the typical full stroke, rather than the thin cap or thick frame. C-5A's converging fits have fused ink near the origin, noted on affected trace rows.

The intercept features use the drawn straight line's meeting with the calibrated x=0 axis; short obscured joins or gaps are reconstructed locally, with widened feature bounds. They are geometric features, not additional test markers. First, maximum, and last line roles are carried by the endpoint trace rows; a straight rising fit has no knee. Angle-label features are at the printed text's center, not points on the fit. The native-unit CSV is generated with tools/calibrate_axes.py apply, including calibration RMS in its read bounds.

## Counts

| Series | Marker | Trace | Feature |
|---|---:|---:|---:|
| dr2-13 | 5 | 21 | 2 |
| dr30 | 5 | 20 | 2 |
| dr48 | 5 | 17 | 2 |
| unassigned | 1 | 0 | 0 |
| dr77 | 5 | 13 | 2 |

## Legend, line labels, and ambiguities

The legend prints SS Soil; circles: gamma 95.2 to 97.6 Lb./Ft.^3, Dr .02 to .13; squares: 100, Dr .30; downward triangles: 103, Dr .48; upward triangles: 107, Dr .77. The three latter entries cite **Bendix Report No. MM-65-2**, differing from MM-66-2 in figures-rows.csv. Series IDs are retained.

The lowest fit is dr2-13, labelled **29°**; the next is dr30, **32.8°**; the next is dr48, **36.9°**; the steepest is dr77, **41.5°**. All start in the fused origin ink. The 29° line has a dashed right extension to the right frame; dashed samples are marked. Erasures at circles and vertical grid lines are not separate observations.

The downward triangle at approximately (1343,2602) overlaps an upward triangle and lies on the 41.5° fit. It remains dr48 by shape. Near (1208,2747), the downward triangle's base and fit merge with the horizontal grid; its centroid was reconstructed from the sides. At (912,2960), the surviving angular outline cannot confidently distinguish a downward triangle from a square; one wide-bound unassigned marker records it. A further square or downward triangle could be wholly hidden in that stack; no second center is supported by the surviving ink, so none is invented. The upper triangle near (910,2929) is separately visible.
