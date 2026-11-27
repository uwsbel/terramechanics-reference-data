# FA-22, panel 1

Blind reading from packet/p0047.png only; all pixels refer to the original 3213 by 4558 unrotated page. Printed caption: Average and Range of Six Samples of RC2 Soil.

The solid curve is `average`; `upper` is the dashed range with higher percent finer (leftward on the scanned page at fixed grain size), and `lower` the other dashed range. Grain size increases up and percent finer increases left. Native values are mm and percent, with x_transform=log10. FA-18 prints RSM without the index's '-a' suffix; its supplied id and series ids are retained. FA-46's caption uses singular 'Sample', as printed. No table values, classification strip, or sieve scale ticks are observations.

## Calibration and eye checks

All printed grain labels 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0 and 9.0 and all percent labels 0, 10, ..., 100 were associated with their actual rulings by eye. The 0 and 100 percent frames are labelled. The fine-end grain frame is 0.02; the coarse frame extends past the labelled 9.0 line and is not used as a knot. Unlabelled log subdivisions and dashed sieve rulings were excluded from calibration.

The initial detect result is preserved separately. Some detections followed a minor subdivision or table border; the final labelled major rulings were measured on visible ink with the table excluded and robust straight-line fits. All 12 x and 11 y lines pass the protocol ink check. See cal-p1/anchors.csv and piecewise-knots.json. Affine diagnostic RMS: 0.0024906 decades and 0.048691 percentage points; maxima 0.0058729 decades and 0.140281 percentage points. Native values and bounds use verified piecewise knots, never the global residual.

## Reading and uncertainty

Markers were examined before sampling traces, using source crops and the marker atlas. Circular symbols often overlap curves, dashed sieve lines and each other. The visible centers are recorded with the symbol-extent bound (14 px) because those overlaps prevent a clean 2 px center claim. Separately unidentifiable range symbols are omitted, with their locations individually listed in marker-omissions.csv. A marker candidate was only a crop locator, not automatically an observation. No triangles were identified; rule 8 does not apply. These are distribution curves, not derived peak envelopes; rule 9 does not supply another source of identity.

Each trace is sampled from the fine end in drawing order, at nominal 0.02 times 10^(0.05*n) mm within its visible extent. Intervals rising more than 10 percent have additional nominal 5-percent samples. Nominal values in notes are sampling requests; x_native and y_native always come from actual ink pixels. In a dash gap or beneath a marker a sample was moved to nearby line ink and the displacement noted; none is a white-gap interpolation or a symbol outline. The first/last features duplicate the trace ink endpoints; broad knees have separate features. The last point also identifies the monotone trace's maximum, so a duplicate peak observation is not added.

Through the coarse shoulders and particularly the fine tails, the curves can run together. Overlaps were read as shared visible ink with a widened bound, not three invented centers. In the near-zero tails of FA-2, FA-6, FA-18 and FA-46 the curve additionally merges into the labelled 0-percent frame; the extent and individual branch positions there are uncertain. FA-26 also approaches that frame. FA-38 has close but often distinguishable curves throughout; the coarse symbols stack. FA-22 has the widest readable range, with separated fine-end circles. Endpoint extent cannot be sharper than the visible merge/marker thickness; flagged bounds reflect that limitation. Normal trace bounds are half the measured line core thickness; wider bounds are expressly flagged. Broad knees are not sharp mathematical breakpoints.

## Calibration sensitivity

- average: largest affine versus piecewise grain difference 0.08591 mm; percent difference 0.0966 percentage points.
- upper: largest affine versus piecewise grain difference 0.08067 mm; percent difference 0.1017 percentage points.
- lower: largest affine versus piecewise grain difference 0.08067 mm; percent difference 0.09233 percentage points.

Counts (trace / marker / feature):
- average: 43 / 14 / 4
- upper: 43 / 11 / 4
- lower: 43 / 13 / 4

## Delivery verification

Every trace and feature center was checked against dark source-image ink; this confirms ink, while the overlay and the stated merge bounds carry curve identity. All 23 labelled knots pass the independent ink checks. Values or bound corners reaching beyond the verified frame are explicitly flagged `extrapolated` in cal_model; 15 rows have that flag, mainly uncertainty intervals touching the 0/100-percent frame. No values were clipped to 0 or 100. Endpoint marks are the last identifiable curve ink at a marker/frame merge, with widened extent bounds; an exact hidden endpoint cannot be claimed.
