# F2-32, panel 1 — independent packet reading

Only this workspace's packet and protocol were used; no other reader's output or earlier figure reading was sought. Source: packet/p0088.png, 300 dpi, unrotated. All CSV coordinates use that page's original origin, u right and v down. The overlay has the full page dimensions and is also unrotated.

`lpt93` follows the long dashed line labelled LPT No. 93, Gp = 16.2; `lpt53` follows the solid recorder curve identified by the leader from LPT No. 53, Gp = 15.6; `lpt52` follows the dotted curve identified by the leader from LPT No. 52, Gp = 15.4. The arrows and styles agree. The visible starts are approximately 0, 2, and **1 inch**, respectively; the 1-inch start of LPT 52 is printed evidence, despite the prompt's general description of 0- or 2-inch starts. `fit` is the thin straight ink reached by the Slope = 6.5 lbs./in. = AγNq leader. Its low end reaches the load axis near the printed 4.7-lb intercept. The equation block is not a curve. No marker symbols occur.

The dotted and solid records are only a few pixels apart over much of the upper linear portion, and sometimes merge. I use the dotted left branch and continuous solid right branch where separately visible, with wider bounds in the overlap. The dotted upper termination merges with the fit and the 7-inch grid line: its endpoint has a 12-pixel bound and explicit note. The thin fit passes through this same region. The dashed start cap projects slightly beyond the zero-penetration line; its observed pixels are retained. Quarter-inch targets falling in a dash/dot gap are displaced to nearby ink, with the actual displacement recorded in the note and actual coordinates converted to native units.

## Calibration

Penetration increases up the page; load increases left. Both axes are linear. The initial detected affine map is a diagnostic: RMS residuals 0.009686 in and 0.074351 lb; maxima 0.027360 in and 0.183822 lb. Neither exceeds 0.5% of the calibrated axis span. Native values and bounds use the protocol's piecewise map between verified ink lines, with line-location errors propagated and no global affine RMS added.

Verified x knots: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 in. Verified y knots: 0, 10, 20, 30, 40, 50, 60, 70 lb. All final knots pass the tool's ink test; no predicted line is used as a knot. The x = 2 line was remeasured on the page from 35 ink anchors (straight-line RMS 0.486 px), replacing its initial rejected/predicted position. Original diagnostic anchors are preserved in anchors-before-recovery.csv. The frame beyond the final printed penetration label has no assigned calibration value.

By-eye checks: penetration 0, 4, 9; load 0, 30, 70. Every checked numeral was visually linked to its own printed grid line on the original page. The CSV records the eye-read pixel position and difference from the fitted line. Maximum absolute eye-versus-line difference: 0.72 px.

## Sampling, bounds, and review

Recorder traces are sampled at quarter-inch targets plus first, global peak, knees/recorder steps, and last features. Straight lines have samples at both ink ends and each labelled penetration crossing; intercept and label-centre features are separate. Label-centre features are annotations, not load measurements, and their native values must not be used as curve data. Sequence follows the visible drawing order; the load drops are retained. There is no macroscopic doubling back in penetration.

Guides in out/guides.py were read from this packet's coordinate-labelled crops. Actual exported samples were recentered on the ink; guides themselves are not exported as measured data. Stroke bounds vary with the measured local normal thickness (half the width), using nearby clean stroke at grid crossings. Crossings/merged lines have enlarged bounds and notes. Faint scan gaps or dash/dot gaps are sampled on nearby ink and noted, not in the white gap. The full supplied D-031 own-ink checker is absent from tools/; ink-proximity-checks.csv is only a supplementary pixel-distance screen, includes grid ink, and is explicitly not a substitute for D-031. All final non-label points have dark ink within 2 px in that screen; line identity was reviewed on the page and overlays. Coordinate-grid detail crops include zoom 3 and 25-pixel grid spacing.

Counts (trace / feature / marker):

- lpt93: 28 / 5 / 0
- lpt53: 21 / 5 / 0
- lpt52: 25 / 4 / 0
- fit: 10 / 2 / 0

## Files

- cal-p1/calibration.json and anchors.csv: detection diagnostic and final piecewise anchor inputs.
- cal-p1/verified-knots.json: ink verification and local line-location bounds; recovery files where applicable.
- calibration-eye-checks.csv: three printed labels per axis checked by eye.
- points-p1.csv: original pixel readings and local pixel bounds.
- points-p1-native.csv: piecewise native values/bounds, units, and extrapolation flags.
- overlay-p1.png: points and bounds on the full original unrotated page.
- calibration-sensitivity.csv: per-series maximum affine-versus-piecewise difference, excluding label features.
- ink-proximity-checks.csv and the named zoom crops: supplementary review artifacts.
