# F2-29, panel 1 — independent packet reading

Only this workspace's packet and protocol were used; no other reader's output or earlier figure reading was sought. Source: packet/p0080.png, 300 dpi, unrotated. All CSV coordinates use that page's original origin, u right and v down. The overlay has the full page dimensions and is also unrotated.

`lpt27` is the single wavy recorder trace, labelled LPT #27, 2-inch Diameter Cylinder, D.P.T. Record No. 54074, Pen Rate 1/2 inch Per Min., Plate Compactor. The boxed text is an annotation, not plotted points. The context on p0077 describes the hydraulic advance and x-y recorder. The initial local load maximum and subsequent load minimum are retained in drawing order. The global load maximum is at the upper terminal ink, near 8 inches. No marker symbols occur.

## Calibration

Penetration increases up the page; load increases left. Both axes are linear. The initial detected affine map is a diagnostic: RMS residuals 0.006155 in and 0.796523 lb; maxima 0.014044 in and 1.355416 lb. Neither exceeds 0.5% of the calibrated axis span. Native values and bounds use the protocol's piecewise map between verified ink lines, with line-location errors propagated and no global affine RMS added.

Verified x knots: 0, 1, 2, 3, 4, 5, 6, 7, 8 in. Verified y knots: 0, 200, 400, 600, 800, 1000, 1200 lb. All final knots pass the tool's ink test; no predicted line is used as a knot. The frame beyond the final printed penetration label has no assigned calibration value.

By-eye checks: penetration 0, 4, 8; load 0, 600, 1200. Every checked numeral was visually linked to its own printed grid line on the original page. The CSV records the eye-read pixel position and difference from the fitted line. Maximum absolute eye-versus-line difference: 0.50 px.

## Sampling, bounds, and review

Recorder traces are sampled at quarter-inch targets plus first, global peak, knees/recorder steps, and last features. Straight lines have samples at both ink ends and each labelled penetration crossing; intercept and label-centre features are separate. Label-centre features are annotations, not load measurements, and their native values must not be used as curve data. Sequence follows the visible drawing order; the load drops are retained. There is no macroscopic doubling back in penetration.

Guides in out/guides.py were read from this packet's coordinate-labelled crops. Actual exported samples were recentered on the ink; guides themselves are not exported as measured data. Stroke bounds vary with the measured local normal thickness (half the width), using nearby clean stroke at grid crossings. Crossings/merged lines have enlarged bounds and notes. Faint scan gaps or dash/dot gaps are sampled on nearby ink and noted, not in the white gap. The full supplied D-031 own-ink checker is absent from tools/; ink-proximity-checks.csv is only a supplementary pixel-distance screen, includes grid ink, and is explicitly not a substitute for D-031. All final non-label points have dark ink within 2 px in that screen; line identity was reviewed on the page and overlays. Coordinate-grid detail crops include zoom 3 and 25-pixel grid spacing.

Counts (trace / feature / marker):

- lpt27: 33 / 21 / 0

## Files

- cal-p1/calibration.json and anchors.csv: detection diagnostic and final piecewise anchor inputs.
- cal-p1/verified-knots.json: ink verification and local line-location bounds; recovery files where applicable.
- calibration-eye-checks.csv: three printed labels per axis checked by eye.
- points-p1.csv: original pixel readings and local pixel bounds.
- points-p1-native.csv: piecewise native values/bounds, units, and extrapolation flags.
- overlay-p1.png: points and bounds on the full original unrotated page.
- calibration-sensitivity.csv: per-series maximum affine-versus-piecewise difference, excluding label features.
- ink-proximity-checks.csv and the named zoom crops: supplementary review artifacts.
