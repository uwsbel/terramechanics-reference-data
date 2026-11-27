# F2-33, panel 1 — independent packet reading

Only this workspace's packet and protocol were used; no other reader's output or earlier figure reading was sought. Source: packet/p0089.png, 300 dpi, unrotated. All CSV coordinates use that page's original origin, u right and v down. The overlay has the full page dimensions and is also unrotated.

`lpt74` is A, the thin wavy trace labelled A LPT No. 74, Gp = 103, started at the soil surface. `lpt75` is B, the thick recorder trace labelled B LPT No. 75, Gp = 105, started two inches below the soil surface. The printed setup says four-inch-diameter cylinder and surface test run in a 36-inch by 36-inch bin. `fit` follows the thick, steep straight line reached by the Slope = AγNq = 316 lbs./in. arrow. `bce` follows the shallower straight line reached by the Bearing Capacity Equation, φ = 49.5° arrow. No marker symbols occur.

The surface-start record crosses the steep fit near its first local failure peak and then drops before recovering; that reversal in load is retained. The below-surface record crosses/runs with the steep fit around 2.7–3.3 inches, then has a local drop before rising again. The records also cross near 2.3 inches, and both cross the bearing-capacity line. Bounds are wider at these locations. The fit's low terminal ink has a small bulb/hook merging into the load-axis ink; the intercept feature is placed on that terminal ink, rather than prolonging an ideal mathematical line. The equation block is not sampled.

## Calibration

Penetration increases up the page; load increases left. Both axes are linear. The initial detected affine map is a diagnostic: RMS residuals 0.009957 in and 3.532248 lb; maxima 0.020073 in and 6.252906 lb. Neither exceeds 0.5% of the calibrated axis span. Native values and bounds use the protocol's piecewise map between verified ink lines, with line-location errors propagated and no global affine RMS added.

Verified x knots: 0, 1, 2, 3, 4, 5 in. Verified y knots: 0, 500, 1000, 1500, 2000, 2500 lb. All final knots pass the tool's ink test; no predicted line is used as a knot. The frame beyond the final printed penetration label has no assigned calibration value.

By-eye checks: penetration 0, 3, 5; load 0, 1000, 2500. Every checked numeral was visually linked to its own printed grid line on the original page. The CSV records the eye-read pixel position and difference from the fitted line. Maximum absolute eye-versus-line difference: 0.29 px.

## Sampling, bounds, and review

Recorder traces are sampled at quarter-inch targets plus first, global peak, knees/recorder steps, and last features. Straight lines have samples at both ink ends and each labelled penetration crossing; intercept and label-centre features are separate. Label-centre features are annotations, not load measurements, and their native values must not be used as curve data. Sequence follows the visible drawing order; the load drops are retained. There is no macroscopic doubling back in penetration.

Guides in out/guides.py were read from this packet's coordinate-labelled crops. Actual exported samples were recentered on the ink; guides themselves are not exported as measured data. Stroke bounds vary with the measured local normal thickness (half the width), using nearby clean stroke at grid crossings. Crossings/merged lines have enlarged bounds and notes. Faint scan gaps or dash/dot gaps are sampled on nearby ink and noted, not in the white gap. The full supplied D-031 own-ink checker is absent from tools/; ink-proximity-checks.csv is only a supplementary pixel-distance screen, includes grid ink, and is explicitly not a substitute for D-031. All final non-label points have dark ink within 2 px in that screen; line identity was reviewed on the page and overlays. Coordinate-grid detail crops include zoom 3 and 25-pixel grid spacing.

Counts (trace / feature / marker):

- lpt74: 18 / 9 / 0
- lpt75: 10 / 8 / 0
- fit: 6 / 2 / 0
- bce: 7 / 2 / 0

## Files

- cal-p1/calibration.json and anchors.csv: detection diagnostic and final piecewise anchor inputs.
- cal-p1/verified-knots.json: ink verification and local line-location bounds; recovery files where applicable.
- calibration-eye-checks.csv: three printed labels per axis checked by eye.
- points-p1.csv: original pixel readings and local pixel bounds.
- points-p1-native.csv: piecewise native values/bounds, units, and extrapolation flags.
- overlay-p1.png: points and bounds on the full original unrotated page.
- calibration-sensitivity.csv: per-series maximum affine-versus-piecewise difference, excluding label features.
- ink-proximity-checks.csv and the named zoom crops: supplementary review artifacts.
