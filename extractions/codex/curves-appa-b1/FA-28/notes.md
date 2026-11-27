# FA-28: blind page reading, panel 1

Source: packet/p0056.png, unrotated 300-dpi page. Only this evidence packet was used; no other reading or earlier extraction was consulted. Caption soil: SS. x is relative density Dr, unit `none`; y is internal friction angle phi, unit `deg`, direct shear test.

Counts: {'curve/trace': 21, 'curve/feature': 4}. Marker count: 0. Samples are in drawing order from the left endpoint, with interior samples every 0.05 Dr, then the right endpoint. Feature rows repeat the first and last positions; the last point is also the peak of each increasing curve. Rounded knees are not sharp observed corners: their feature bounds span the visually plausible transition region. Trace bounds are half the local line thickness; at grid/frame/hatch junctions that thickness is read on the adjoining curve or edge, not the merged junction ink. Scan defects are noted on affected records.

## Calibration and by-eye checks

All six printed x labels 0, 0.2, 0.4, 0.6, 0.8 and 1.0 were checked by eye against their own vertical lines. Printed y labels 25,30,35,40,45,50 were each checked against their own horizontal line at the left axis. See calibration-eye-checks.csv and cal-p1/label-checks.png for the line associations and enlarged source snippets. No value was assigned to an unlabelled frame. The lower frame is excluded unless explicitly labelled (25 degrees on A-28).

Affine diagnostic residuals: RMS x = 0.00324529 Dr, y = 0.022176 deg; maximum absolute x = 0.00488761 Dr, y = 0.044872 deg. RMS residuals are below 0.5% of each calibrated axis span. The final ink-verified map uses 6 x lines and 6 y lines, with no predicted or rejected knots. Each verified line and its ink offsets/location error is saved in cal-p1/knots-verified.json. Native values and bounds use tools/calibrate_axes.py piecewise --image (D-025), including line-position errors and the pixel rectangle, without adding the affine residual. 2 rows have an extrapolation flag; the tool also flags an endpoint when its uncertainty rectangle crosses an outer knot, even if its centre is on that knot.

Per-series maximum absolute difference, piecewise minus affine, among trace samples: {'curve': {'max_abs_x': 0.004618700535925673, 'max_abs_y': 0.04209098646602172}}. These are correlated calibration sensitivities, not added random error bars.

## Ambiguities and page evidence

The first connected curve cap starts at (770,3223), after three white columns between it and the left frame. Its extreme left is worn down to a one-pixel strand connected to the thicker cap. The recorded bound is half the adjoining 12-pixel stroke. Its native Dr is slightly positive; there is no invented trace sample at zero. The sigmoid has two rounded knees, near Dr 0.3 and 0.65, recorded with broad feature-location bounds. No symbols are identified. The unlabelled top frame is excluded.

## Files

cal-p1/ contains anchors.csv, calibration.json, knots-verified.json, and label-checks.png. calibration-eye-checks.csv records the by-eye checks. points-p1.csv stores page-pixel readings; points-p1-native.csv adds piecewise native values and reading bounds. overlay-p1.png is the full unrotated page overlay; overlay-detail.png is a plot crop for review. trace-grid-*.png (or band-grid.png) are enlarged pixel-grid crops, and samples-check*.png show every trace sample against the page ink. Full-page pixel coordinates apply to all CSVs, including those reviewed on crops.
