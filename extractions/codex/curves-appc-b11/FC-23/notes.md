# FC-23, panel 1

Independent reading from packet/p0159.png, unrotated 300 dpi. Context p0115 identifies these as relationships from direct-shear results. Units are Dr: none and phi_DS: deg.

Six printed labels identify the curves: RC2 and SS are solid; PS uses short dashes; RS uses longer dashes; RSM-b uses long dashes on the steep ascending line; RSM-a uses long dashes on the shallower middle line. The series ids retain the packet's lower-case spelling. No markers are printed. Label features record the centers of RC2, PS, RS, RSM-b, RSM-a and SS. RC2 and PS touch/cross close to Dr 0.08-0.10, around (1070,2210). RSM-b crosses RS near Dr 0.53, around (1770,2070), and crosses PS near Dr 0.66-0.69, around (2000,1930). RS and PS touch/cross around Dr 0.89-0.93, around (2340,1830). These crossing regions contain merged ink; the line styles on each side determine continuation. PS and RS reach the right frame; RS starts at the left frame. RSM-a also ends against the right frame. Other endpoints are inside the frame. No circle symbols occur.

The frame extends roughly one density grid interval to the left of 0 and to the right of 1.0. Its top and bottom extend beyond the labelled 50 and 30 degree lines. None of these unlabelled frame lines is a value anchor. Checked labels: x 0, 0.5, 1.0; y 30, 40, 50. All eleven x lines (0 through 1.0 in steps of 0.1) and five y lines (30 through 50 in steps of 5) were inspected against page ink and passed the protocol's ink check, without predicted knots.

Affine diagnostic RMS: x=0.002266 Dr; y=0.038606 deg. Maximum residuals: x=0.005030, y=0.065077 deg. Native values and bounds use the verified piecewise maps, with calibration-line uncertainty propagated through the pixel intervals. Points outside the labelled knots are flagged extrapolated.

Samples follow drawing order, from left ink end through Dr multiples of 0.05 to the right ink end. Dashed samples in gaps move to nearby visible ink; notes retain the target Dr. At grid crossings the solid-line center follows the visible continuation on each side. Endpoints were checked on enlarged page crops. Trace bounds are half the visible line width (usually 2-4 px); symbol overlaps use approximately the symbol radius. There are no discrete knees or interior maxima distinguishable from smooth curvature; every trace's maximum is its right end, tagged 'last point; peak'. Curve crossings and the sigmoid inflection of SS are not treated as knees. Rule 8 has no application because no triangles are printed; rule 9 requires no additional identity assignment because all symbols here belong to the panel's data series.

Counts:

- rc2: trace 23
- rc2: feature 3
- ps: trace 24
- ps: feature 3
- rs: trace 26
- rs: feature 3
- rsm-b: trace 23
- rsm-b: feature 3
- rsm-a: trace 24
- rsm-a: feature 3
- ss: trace 23
- ss: feature 3

Files: cal-p1/calibration.json, anchors.csv, verified-knots.json, calibration-sensitivity.md; calibration-eye-checks.csv; points-p1.csv; points-p1-native.csv; overlay-p1.png. Reading crops are supplementary inspection aids.

The largest affine x residual is 0.005030 Dr (0.503% of the labelled span), just above the 0.5% diagnostic threshold. A changed box (900,1640,2530,3280), 25 bands and min-frac 0.5 was rechecked in cal-p1-recheck; it preserves the uneven grid spacing and does not materially improve the residual. All knots of the submitted calibration pass direct ink verification. The piecewise map is retained because the excess is drafted spacing, not an unverified or predicted anchor.
