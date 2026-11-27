# FC-6A: independent reading, panel 1

Source: packet/p0131.png, original unrotated 300-dpi image, pixel coordinates u right / v down. Only this packet was consulted. The context page p0115.png identifies Appendix C as direct shear data from Notre Dame, with the C-5A exception.

## Calibration

All interior calibration lines are actual detected printed grid lines; none are predicted. The affine map and detected-line samples are in cal-p1/calibration.json, with 42 anchors on C-5A/C-6A and 56 on C-7A. The frame box is [900, 1220, 2420, 3020].

RMS residual x / y: 3.039642 / 6.327674 native units. Maximum residual x / y: 6.527847 / 12.392331. These are below 0.5% of the axis spans. Three printed labels per axis were checked independently against the tick/grid intersections read by eye, recorded in calibration-eye-checks.csv and shown in cal-p1/eye-label-checks.png. Position differences are compared to the 4-pixel eye bound plus the calibration RMS. C-5A's upper frame is unlabelled; its value 6000 follows the printed 1000-psf spacing, and it is not one of the three printed-label checks.

## Reading conventions

Markers were read first, from the labelled zoomed crops. Clear circle/square centers have 2-pixel bounds; overlaps are widened. Triangles use reconstructed centroids, with v bounds at least one sixth of their reconstructed height. No hidden data-sheet readings were available or used. Blank series_id means identity unresolved; it does not create a new density series.

Trace guide equations in read_helpers.py only locate the ink. Samples themselves use the center of a visible ink run, checked in trace-checks-*.png. A guide is never used to fill a dash gap. Sampling proceeds from the left ink end at nominal 250-psf intervals (2 psi on C-7A), ending at the last ink; labels and marker rims are avoided. Where the nominal abscissa falls in a dash/erasure gap, marker, or grid merge, the sample is moved to the nearest clean part of the same line, with the nominal target in its note. Thus x_native can differ from the nominal target. Bounds are half the measured stroke thickness perpendicular to the line, expressed as a conservative equal u/v radius. Endpoint bounds use the typical full stroke, rather than the thin cap or thick frame. C-5A's converging fits have fused ink near the origin, noted on affected trace rows.

The intercept features use the drawn straight line's meeting with the calibrated x=0 axis; short obscured joins or gaps are reconstructed locally, with widened feature bounds. They are geometric features, not additional test markers. First, maximum, and last line roles are carried by the endpoint trace rows; a straight rising fit has no knee. Angle-label features are at the printed text's center, not points on the fit. The native-unit CSV is generated with tools/calibrate_axes.py apply, including calibration RMS in its read bounds.

## Counts

| Series | Marker | Trace | Feature |
|---|---:|---:|---:|
| dr5-40 | 5 | 21 | 1 |
| unassigned | 1 | 0 | 0 |
| dr19-28 | 4 | 20 | 1 |
| dr103-107 | 5 | 20 | 1 |

## Legend, line assignment, and ambiguities

The legend prints LSM Soil; upward triangles: gamma 66.8 to 75.2 Lb./Ft.^3, Dr .05 to .40; circles: 71.1 to 73, Dr .19 to .28; squares: 91 to 93.3, Dr 1.03 to 1.07. IDs are retained as given. The upper author fit is assigned to dr5-40, the middle to dr19-28, and the lower to dr103-107 from the high-load shape order and the drawn line continuations. Several individual symbols depart substantially from that order.

**No friction-angle labels are printed on this page.** There are therefore no angle-label feature rows for C-6A. This is an evidence-based exception to the requested one label per series; no angle was calculated or supplied. The numbers **3820** and **3680** label the vertical and horizontal dashed construction through the high-load group, not angles or another failure envelope. Grid/frame and these construction lines are excluded from series traces.

The square at (1786,2128) is on the upper fit; the square near (1147,2774) is also beside it. Both remain dr103-107 by shape. Upright triangles near (1763,2208) and (2027,1919) sit on the middle fit and remain dr5-40 by shape. The circle at (1442,2527) overlaps the upright triangle at (1444,2551); both centers are recorded separately with wide bounds.

The distinct downward triangle at (1787,2148), immediately below the square, has no corresponding legend shape. It is recorded with blank series_id and wide bounds, rather than guessing between density groups. There is no confidently identifiable circle in that same stack. The printed zero at approximately (894,3056), outside the lower-left frame, is an axis label, not a plotted circle.

Circle and square fits have dashed low-load extensions. The circle extension continues below the horizontal frame and is sampled where it reaches the extrapolated x=0 axis. The square's earlier low-load join is obscured by the triangle/frame: its first trace row is at the first separately identifiable dashed ink near (994,2968), explicitly not a claim to a resolved original left endpoint. Its intercept lies in the obscured/gapped join and is a geometric feature. The circle and square fits nearly coalesce at low load; their samples around 1000-1500 psf consequently share or adjoin ink. The upper fit has visible erasure gaps but is not designated dashed solely because it is interrupted.
