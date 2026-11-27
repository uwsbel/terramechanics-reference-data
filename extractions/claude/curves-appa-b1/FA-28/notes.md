# FA-28, blind reading (Claude), batch curves-appa-b1

Page `p0056.png` (printed A-55). Caption as printed: "Figure A-28. Angle of Internal Friction (as
determined by the direct shear test) Versus Relative Density for SS Soil". It matches the figures
index. One panel, upright, full grid, one solid curve, no symbols, no legend. Series id `curve`.

## Calibration (`cal-p1/`)

1. `tools/calibrate_axes.py detect`, box u 735 to 2335, v 1420 to 3550, 10 bands, x values 0, 0.2,
   0.4, 0.6, 0.8, 1.0 (left frame to right frame), y values 25 to 50 by 5 (bottom frame to the line
   labelled 50).
2. The top frame line (v 1219) carries no printed label. By the spacing it would be 55, but it is
   unlabelled, so the box starts below it and it is not an anchor. The curve never comes near it.
3. All 12 lines detected in 10 of 10 bands; none predicted. Affine residuals: x RMS 0.0032, max
   0.0049 (0.49 percent of the 0 to 1 span, just under the 0.5 percent threshold); y RMS 0.022 deg,
   max 0.046 deg (0.09 and 0.19 percent of the 25 deg span). The x residual comes from uneven
   drafting of the vertical lines (spacings 302, 312, 304, 315, 320 px from left to right), which
   the piecewise map follows.
4. Piecewise ink check (`cal-p1/knots-ink-check.json`): all 6 x lines and all 6 y lines verified,
   ink found at 14 or 15 of 15 positions each, ink line within 0.55 px of the fitted line at both
   ends; location errors 0.50 to 0.91 px.
5. Labels checked by eye (`calibration-eye-checks.csv`): all six y labels and all six x labels.
   The "25" is printed about 15 px above the bottom frame line it labels; "40" about 4 px below
   its line; the x labels have their decimal point under the line. No label sits on a wrong line.

## Points (`points-p1.csv`, `points-p1-native.csv`)

1. `curve`: 21 trace samples (left end, Dr 0.05 to 0.95 every 0.05, right end) and 2 features.
   Bounds 6 px in u and v: the line is 11 to 13 px thick measured across it (median 11.6 px).
2. Samples were located with `helpers/trace.py`: the dark mask (gray below 160) is opened with a
   7 px square, which removes the thin grid lines (3 to 7 px) and keeps the curve; the curve's
   centre in each column is the midpoint of its run; at each target Dr the centre is a straight
   line fitted to the clean columns within 8 px, and the u is iterated until the piecewise map
   gives the target Dr. Columns where the curve crosses a grid line (run thicker than its
   neighbours) are not used. Samples at Dr 0.2, 0.4, 0.6, 0.8 sit on vertical grid lines and are
   therefore taken from the curve on either side of the line; checked on zoomed overlays at 0.2
   and 0.8 (`check-0p2.png`, `check-0p8.png`): on the centre of the line.
3. Left end: the curve's ink starts at u 773 (one row reaches u 771), 4 to 5 px clear of the left
   frame (frame ink u 759 to 767), so the first sample is at Dr 0.0065, phi 28.85 deg, not on the
   frame.
4. Right end: the curve runs into the right frame (frame ink u 2305 to 2312, Dr 1.0 at u 2308);
   where the curve's ink stops being separable from the frame is u about 2303. The last sample is
   at u 2303, v 2296.5 (Dr 0.997, phi 41.03 deg) with a u bound of 6 px that reaches the frame
   centre; `piecewise` flags it `extrapolated x` only because that bound reaches past the x = 1.0
   line.
5. Features: first point (left end) and last point (right end). The curve rises monotonically, so
   its maximum is the last point. It is a smooth S shape with its steepest part near Dr 0.40 to
   0.50 (inflection); there is no knee or kink, so no knee feature is recorded.

## Ambiguities

1. Right end at the frame: the drawn end is hidden in the frame ink; the last point could be read
   anywhere from u 2300 to the frame centre at 2308 (Dr 0.995 to 1.0, phi change under 0.03 deg).
2. A speck at about u 2118, v 2490 (22 dark pixels), below the curve near Dr 0.88, is dirt, not a symbol.
3. The x = 0.4 grid line is broken in places between v 1476 and 1593, just above the y = 50 line; it is far from
   the curve and was still detected in all bands.

## Files

`cal-p1/` (anchors.csv, calibration.json, knots-ink-check.json), `calibration-eye-checks.csv`,
`points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`, crops (`crop-*.png`, `eye-*.png`,
`check-*.png`), helpers in `helpers/`.
