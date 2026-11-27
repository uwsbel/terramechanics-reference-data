# FC-7B: independent blind reading

Source: packet/p0136.png, unrotated 300-dpi image, printed page C-22. RSM-b; Dr 1.0, gamma 89 PCF. Only the supplied packet and its protocol were used. Context p0115 and p0135 was inspected for experiment context; no coordinates were read from the failure-envelope figure.

## Axes and independent label checks

Horizontal motion is x in inches (0 to .32); horizontal load is y in psi (0 to 35). The printed motion labels increase UP the scanned page; the load labels increase LEFT. Pixel u increases rightward and v downward. Calibration used tools/calibrate_axes.py detect with --x-direction up --y-direction left, 72 grid intersections, 5 bands, dark=200, min-frac=0.6. The frame box and full fitted line parameters are in cal-p1/calibration.json.

RMS residual: x=0.000149469 inch (0.0467% of span); y=0.023344119 psi (0.0667% of span). Maximum residual: x=0.000418489 inch; y=0.055575423 psi. These pass the 0.5%-of-span criterion.

By-eye printed labels: x=.04, .16, .32; y=5, 15, 30. Their independently inspected unrotated grid positions and fitted values are in calibration-eye-checks.csv. All six confirm the correct directions. All gridlines were detected in all five bands. No predicted lines.

## Symbols, identity, and ordering

The printed normal stresses match the packet series IDs. Symbols, described with the figure upright: highest stress=quarter-circle (open D-shaped/rounded quadrant), 13.8=star, 10.2=triangle-up, 6.6=diamond, 5.1=square, 3.4=circle. No legend-number correction is required. Legend gamma values match the supplied state.

Every output point is point_kind=marker, panel=1. There are no trace, feature, or gridline data rows. The sequence lists visible markers in their loading/motion progression from the baseline toward the top of the page; no interpolated points or hidden extra symbols were created. With symbols only there is no drawn path establishing a separate unloading branch.

Marker counts:

- n27p1psi: 22
- n13p8psi: 19
- n10p2psi: 16
- n6p6psi: 16
- n5p1psi: 17
- n3p4psi: 17

Total: 107 marker rows.

## Bounds and ambiguities

Clean marker centers have 2-px half-bounds. Gridline interference is noted per point and generally receives 5 px; difficult intersections receive 6-8 px. Touching symbols and symbols obscured by the baseline receive approximately half-symbol-size bounds of 15-18 px. Such bounds express reading uncertainty, not standard deviations. Distinct outlines establish the identities even when their centers have broad bounds. Short isolated horizontal ink and tails were not sampled as curves. Helper component detection was used only to locate candidate ink; merged components were split and their identities checked by eye on the enlarged crops.

Crowded groups include quarter-circle/star pairs near (1541,3267)/(1558,3241), triangle/star near (1833,3246)/(1855,3268), diamond/circle/square/triangle near u=1948-2036, v=3219-3266, square/circle/triangle near u=2095-2138, and square/circle near u=2194-2207. At the longest displacement the square and circle near (2041,1750)/(2075,1749) touch across the 5-psi gridline. Each distinct visible outline is separately recorded. The square at (2251,3268) has interior stray ink and meets the baseline; there is insufficient evidence to add another hidden symbol. No series identity remains unassigned among the 107 recorded markers.

## Files and verification

Required files: cal-p1/anchors.csv, cal-p1/calibration.json, calibration-eye-checks.csv, points-p1.csv, points-p1-native.csv, overlay-p1.png, and notes.md. Supporting enlarged unrotated pixel-grid crops, candidate contact sheets, and overlay crops are retained here. Own helpers are under out/; tools/ was not changed.

The native conversion was run with tools/calibrate_axes.py apply. Its three-decimal rounding would discard some small inch bounds, so a helper retained the SAME affine conversion and bound formula at six decimals: |axis coefficient u|*u_bound + |axis coefficient v|*v_bound + RMS residual. No uncertainty was rounded to zero. Native x units are inch; native y units are psi.

Final overlay was checked against the full plot and enlarged origin crops. Row counts, panel/kind, positive bounds, unique per-series sequences, and equality of raw/native marker identifiers were checked. Coordinates remain in the unrotated scan throughout.
