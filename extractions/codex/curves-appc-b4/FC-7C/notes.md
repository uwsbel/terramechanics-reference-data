# FC-7C: independent blind reading

Source: packet/p0137.png, unrotated 300-dpi image, printed page C-23. RSM-b; Dr 0.53, gamma 82 PCF. Only the supplied packet and its protocol were used. Context p0115 and p0135 was inspected for experiment context; no coordinates were read from the failure-envelope figure.

## Axes and independent label checks

Horizontal motion is x in inches (0 to .32); horizontal load is y in psi (0 to 35). The printed motion labels increase UP the scanned page; the load labels increase LEFT. Pixel u increases rightward and v downward. Calibration used tools/calibrate_axes.py detect with --x-direction up --y-direction left, 72 grid intersections, 5 bands, dark=200, min-frac=0.4. The frame box and full fitted line parameters are in cal-p1/calibration.json.

RMS residual: x=0.000249866 inch (0.0781% of span); y=0.014811737 psi (0.0423% of span). Maximum residual: x=0.000527078 inch; y=0.042225620 psi. These pass the 0.5%-of-span criterion.

By-eye printed labels: x=.04, .16, .32; y=5, 15, 30. Their independently inspected unrotated grid positions and fitted values are in calibration-eye-checks.csv. All six confirm the correct directions. The additional x=.28 check inspects the sole predicted line. Its right-end ink is at v=1584.5 at u=2300, versus the fitted line v=1582.34 (2.16 px). The printed .28 label and visible line confirm it. The initial min-frac=.6 detection predicted both 30 psi and .28 in; lowering to .4 detected 30 psi in all five bands. Final calibration has only .28 in predicted.

## Symbols, identity, and ordering

The printed normal stresses match the packet series IDs. Symbols, described with the figure upright: highest stress=quarter-circle (open D-shaped/rounded quadrant), 13.8=star, 10.2=triangle-up, 6.6=diamond, 5.1=square, 3.4=circle. No legend-number correction is required. Legend gamma values match the supplied state.

Every output point is point_kind=marker, panel=1. There are no trace, feature, or gridline data rows. The sequence lists visible markers in their loading/motion progression from the baseline toward the top of the page; no interpolated points or hidden extra symbols were created. With symbols only there is no drawn path establishing a separate unloading branch.

Marker counts:

- n26p5psi: 16
- n13p8psi: 17
- n10p2psi: 15
- n6p6psi: 15
- n5p1psi: 15
- n3p4psi: 16
- unidentified: 1

Total: 95 marker rows.

## Bounds and ambiguities

Clean marker centers have 2-px half-bounds. Gridline interference is noted per point and generally receives 5 px; difficult intersections receive 6-8 px. Touching symbols and symbols obscured by the baseline receive approximately half-symbol-size bounds of 15-18 px. Such bounds express reading uncertainty, not standard deviations. Distinct outlines establish the identities even when their centers have broad bounds. Short isolated horizontal ink and tails were not sampled as curves. Helper component detection was used only to locate candidate ink; merged components were split and their identities checked by eye on the enlarged crops.

One separately visible angular marker at (2220,3290), below the square/circle pair at approximately (2220,3273)/(2242,3270), is partly hidden by the baseline and neighbors. Its outline cannot securely distinguish star from diamond. It is included as series_id=unidentified, symbol=unidentified, with 20-px half-bounds, and is excluded from the six assigned-series counts. This explicitly follows protocol rule 7: no series assigned by guess. The uncertainty includes shape/identity, not merely center location. It remains for adjudication from the page.

Other touching groups are quarter-circle/star near (2027,3290)/(2060,3283), square/circle near (2184,3238)/(2204,3238), (2152,3182)/(2166,3182), and (2131,3121)/(2154,3121). The first circle (2292,3283) meets the baseline. Their per-row bounds and notes retain this uncertainty. No invisible initial point was inferred.

## Files and verification

Required files: cal-p1/anchors.csv, cal-p1/calibration.json, calibration-eye-checks.csv, points-p1.csv, points-p1-native.csv, overlay-p1.png, and notes.md. Supporting enlarged unrotated pixel-grid crops, candidate contact sheets, and overlay crops are retained here. Own helpers are under out/; tools/ was not changed.

The native conversion was run with tools/calibrate_axes.py apply. Its three-decimal rounding would discard some small inch bounds, so a helper retained the SAME affine conversion and bound formula at six decimals: |axis coefficient u|*u_bound + |axis coefficient v|*v_bound + RMS residual. No uncertainty was rounded to zero. Native x units are inch; native y units are psi.

Final overlay was checked against the full plot and enlarged origin crops. Row counts, panel/kind, positive bounds, unique per-series sequences, and equality of raw/native marker identifiers were checked. Coordinates remain in the unrotated scan throughout.
