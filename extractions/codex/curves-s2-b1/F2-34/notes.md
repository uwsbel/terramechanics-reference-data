# F2-34, panel 1 — independent packet reading

Only this workspace's packet and protocol were used; no other reader's output or earlier figure reading was sought. Source: packet/p0090.png, 300 dpi, unrotated. All CSV coordinates use that page's original origin, u right and v down. The overlay has the full page dimensions and is also unrotated.

**The load-axis label is printed `Load - Lbs. x 100`. Values 0, 200, 400, 600, 800, 1000, 1200 are supplied and exported with unit `lb`, exactly as directed; no multiplication by 100 is applied.** This printed label is also recorded in calibration-eye-checks.csv and calibration.json.

`lpt87` is A, the thick continuous recorder line labelled A LPT No. 87, started at the soil surface. `lpt88` is B, the thin wavy line labelled B LPT No. 88, started two inches below the surface. The printed setup gives a 108-inch by 36-inch test bin. `fit` is the shallow thick straight ink reached by the Slope = AγNq = 54 lbs./in. arrow, **not** the much steeper thick continuation of A. The leader and adjacent A/B labels settle identity. Its upper end includes a small separated cap immediately above a short scan break; the terminal cap is retained. No marker symbols occur.

B and the fit are close and cross over approximately 4–5 inches, with distinct branches visible on either side. The three lines converge around 2.3 inches; B then turns rapidly toward zero load near its 2-inch start. A also crosses the fit near its initial bend. Bounds and notes mark these crossings. B continues beyond the last printed penetration label (6) to slightly beyond the unlabelled 8-inch grid line. These native values are flagged as extrapolated, since unlabelled continuation lines were not promoted to labelled calibration knots.

## Calibration

Penetration increases up the page; load increases left. Both axes are linear. The initial detected affine map is a diagnostic: RMS residuals 0.009165 in and 1.480950 lb; maxima 0.017650 in and 2.842182 lb. Neither exceeds 0.5% of the calibrated axis span. Native values and bounds use the protocol's piecewise map between verified ink lines, with line-location errors propagated and no global affine RMS added.

Verified x knots: 0, 1, 2, 3, 4, 5, 6 in. Verified y knots: 0, 200, 400, 600, 800, 1000, 1200 lb. All final knots pass the tool's ink test; no predicted line is used as a knot. The y = 1000 line was remeasured on the page from 19 ink anchors (straight-line RMS 0.443 px), replacing its initial rejected/predicted position. Original diagnostic anchors are preserved in anchors-before-recovery.csv. The frame beyond the final printed penetration label has no assigned calibration value.

By-eye checks: penetration 0, 3, 6; load 0, 600, 1200. Every checked numeral was visually linked to its own printed grid line on the original page. The CSV records the eye-read pixel position and difference from the fitted line. Maximum absolute eye-versus-line difference: 0.31 px.

## Sampling, bounds, and review

Recorder traces are sampled at quarter-inch targets plus first, global peak, knees/recorder steps, and last features. Straight lines have samples at both ink ends and each labelled penetration crossing; intercept and label-centre features are separate. Label-centre features are annotations, not load measurements, and their native values must not be used as curve data. Sequence follows the visible drawing order; the load drops are retained. There is no macroscopic doubling back in penetration.

Guides in out/guides.py were read from this packet's coordinate-labelled crops. Actual exported samples were recentered on the ink; guides themselves are not exported as measured data. Stroke bounds vary with the measured local normal thickness (half the width), using nearby clean stroke at grid crossings. Crossings/merged lines have enlarged bounds and notes. Faint scan gaps or dash/dot gaps are sampled on nearby ink and noted, not in the white gap. The full supplied D-031 own-ink checker is absent from tools/; ink-proximity-checks.csv is only a supplementary pixel-distance screen, includes grid ink, and is explicitly not a substitute for D-031. All final non-label points have dark ink within 2 px in that screen; line identity was reviewed on the page and overlays. Coordinate-grid detail crops include zoom 3 and 25-pixel grid spacing.

Counts (trace / feature / marker):

- lpt87: 26 / 6 / 0
- lpt88: 25 / 7 / 0
- fit: 8 / 2 / 0

## Files

- cal-p1/calibration.json and anchors.csv: detection diagnostic and final piecewise anchor inputs.
- cal-p1/verified-knots.json: ink verification and local line-location bounds; recovery files where applicable.
- calibration-eye-checks.csv: three printed labels per axis checked by eye.
- points-p1.csv: original pixel readings and local pixel bounds.
- points-p1-native.csv: piecewise native values/bounds, units, and extrapolation flags.
- overlay-p1.png: points and bounds on the full original unrotated page.
- calibration-sensitivity.csv: per-series maximum affine-versus-piecewise difference, excluding label features.
- ink-proximity-checks.csv and the named zoom crops: supplementary review artifacts.
