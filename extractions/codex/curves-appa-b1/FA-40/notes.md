# FA-40: blind page reading, panel 1

Source: packet/p0079.png, unrotated 300-dpi page. Only this evidence packet was used; no other reading or earlier extraction was consulted. Caption soil: LSM. x is relative density Dr, unit `none`; y is internal friction angle phi, unit `deg`, direct shear test.

Counts: {'band-top/trace': 21, 'band-top/feature': 2, 'band-bottom/trace': 21, 'band-bottom/feature': 2}. Marker count: 0. Samples are in drawing order from the left endpoint, with interior samples every 0.05 Dr, then the right endpoint. Feature rows repeat the first and last positions; the last point is also the peak of each increasing curve. Rounded knees are not sharp observed corners: their feature bounds span the visually plausible transition region. Trace bounds are half the local line thickness; at grid/frame/hatch junctions that thickness is read on the adjoining curve or edge, not the merged junction ink. Scan defects are noted on affected records.

## Calibration and by-eye checks

All six printed x labels 0, 0.2, 0.4, 0.6, 0.8 and 1.0 were checked by eye against their own vertical lines. Printed y labels 30,35,40,45,50 were each checked against their own horizontal line at the left axis. See calibration-eye-checks.csv and cal-p1/label-checks.png for the line associations and enlarged source snippets. No value was assigned to an unlabelled frame. The lower frame is excluded unless explicitly labelled (25 degrees on A-28).

Affine diagnostic residuals: RMS x = 0.00294874 Dr, y = 0.018350 deg; maximum absolute x = 0.00481530 Dr, y = 0.035003 deg. RMS residuals are below 0.5% of each calibrated axis span. The final ink-verified map uses 6 x lines and 5 y lines, with no predicted or rejected knots. Each verified line and its ink offsets/location error is saved in cal-p1/knots-verified.json. Native values and bounds use tools/calibrate_axes.py piecewise --image (D-025), including line-position errors and the pixel rectangle, without adding the affine residual. 8 rows have an extrapolation flag; the tool also flags an endpoint when its uncertainty rectangle crosses an outer knot, even if its centre is on that knot.

Per-series maximum absolute difference, piecewise minus affine, among trace samples: {'band-bottom': {'max_abs_x': 0.004492872604989873, 'max_abs_y': 0.026728881510599933}, 'band-top': {'max_abs_x': 0.004651496582556369, 'max_abs_y': 0.01221332035689926}}. These are correlated calibration sensitivities, not added random error bars.

## Ambiguities and page evidence

The page prints a cross-hatched band bounded by the 45- and 40-degree horizontal lines, extending over the full labelled Dr 0 to 1 range. This differs from the index states field Dr .40 to 1.00. Read band-top and band-bottom; no single curve and no distinct data symbols are printed. Crosses and diamonds are intersections of the repeated hatching, not plotted markers. White scars and stray short dashes in the band cannot be identified as symbols and are not counted. No triangle or test identity is inferred. Both edges are flat in native coordinates, so the peak extends along the edge and has no unique x. An initial box clipped the right frame at its bottom and failed its ink check (2.54 px); the final widened box includes its whole stroke, and all six x lines pass. The hatch vertex at bottom sample 20 is excluded from the line-thickness estimate.

## Files

cal-p1/ contains anchors.csv, calibration.json, knots-verified.json, and label-checks.png. calibration-eye-checks.csv records the by-eye checks. points-p1.csv stores page-pixel readings; points-p1-native.csv adds piecewise native values and reading bounds. overlay-p1.png is the full unrotated page overlay; overlay-detail.png is a plot crop for review. trace-grid-*.png (or band-grid.png) are enlarged pixel-grid crops, and samples-check*.png show every trace sample against the page ink. Full-page pixel coordinates apply to all CSVs, including those reviewed on crops.
