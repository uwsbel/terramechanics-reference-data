# FC-22, panel 1

Independent reading from packet/p0158.png, unrotated 300 dpi. Context p0115 identifies these as relationships from direct-shear results. Units are Dr: none and phi_DS: deg.

The panel prints 'RSM-b Soil'. Two open circles sit on the solid mean; one also crosses the 45 degree grid line. Both get 18 px bounds. Neither is cut by the frame. Upper and lower are the dashed curves above and below mean. The traces continue beyond the last circle to their own ink endpoints near Dr 1.0.

The frame extends roughly one density grid interval to the left of 0 and to the right of 1.0. Its top and bottom extend beyond the labelled 50 and 30 degree lines. None of these unlabelled frame lines is a value anchor. Checked labels: x 0, 0.5, 1.0; y 30, 40, 50. All eleven x lines (0 through 1.0 in steps of 0.1) and five y lines (30 through 50 in steps of 5) were inspected against page ink and passed the protocol's ink check, without predicted knots.

Affine diagnostic RMS: x=0.001144 Dr; y=0.011698 deg. Maximum residuals: x=0.002758, y=0.023995 deg. Native values and bounds use the verified piecewise maps, with calibration-line uncertainty propagated through the pixel intervals. Points outside the labelled knots are flagged extrapolated.

Samples follow drawing order, from left ink end through Dr multiples of 0.05 to the right ink end. Dashed samples in gaps move to nearby visible ink; notes retain the target Dr. At grid crossings the solid-line center follows the visible continuation on each side. Endpoints were checked on enlarged page crops. Trace bounds are half the visible line width (usually 2-4 px); symbol overlaps use approximately the symbol radius. There are no discrete knees or interior maxima distinguishable from smooth curvature; every trace's maximum is its right end, tagged 'last point; peak'. Curve crossings and the sigmoid inflection of SS are not treated as knees. Rule 8 has no application because no triangles are printed; rule 9 requires no additional identity assignment because all symbols here belong to the panel's data series.

Counts:

- data: marker 2
- mean: trace 23
- mean: feature 2
- upper: trace 23
- upper: feature 2
- lower: trace 23
- lower: feature 2

Files: cal-p1/calibration.json, anchors.csv, verified-knots.json, calibration-sensitivity.md; calibration-eye-checks.csv; points-p1.csv; points-p1-native.csv; overlay-p1.png. Reading crops are supplementary inspection aids.
