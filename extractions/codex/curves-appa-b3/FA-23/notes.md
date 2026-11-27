Blind reading, batch curves-appa-b3, FA-23, panel 1. Only packet pages and protocol were used. All pixel coordinates refer to the original unrotated page, p0048.png.

Calibration uses printed Dr 0 through 1.0 (all eleven labelled vertical lines), linear rightward, and labelled unit weights 55 through 100 pcf in steps of 5, reciprocal downward. Unlabelled horizontal subdivisions are not knots. Both the minimum-density and maximum-density labels refer to the same horizontal lines. The extra grid above the first labelled line in A-3, A-7 and A-23 is excluded. Trace/label positions above the first verified labelled line are explicitly extrapolated; no reciprocal is typed as a measurement.

Detected lines were refined against page ink. Standard 6 px half-window is used for checks except the thick bottom frame, whose 14 px half-window includes the white background needed to locate its core. This adaptation is in out/reading_lib.py; tools were not modified. All 11 x and 10 y knots pass the protocol's coverage and 2 px end-deviation checks; none are predicted. Initial detection is retained for reproducibility. Values and read bounds use piecewise interpolation with verified line errors and the declared transform. Native y values are pcf. The affine map is diagnostic only.

Affine RMS residual: Dr 0.00203883 (0.2039% of span; 2.809 px), reciprocal-y 4.038374e-06 (0.0494% of reciprocal span; 1.104 px). Maximum residual: x 0.5697% and reciprocal-y 0.1019% of span. Three by-eye checks per axis: Dr 0, 0.5, 1.0; pcf 55, 75, 100. See calibration-eye-checks.csv and the check crops. Every other labelled calibration line was also checked against the page grid.

The maximum affine x residual exceeds 0.5% although its RMS does not. The box/threshold detection was followed by direct ink refinement before extraction. The remaining maximum reflects uneven grid drafting; every labelled line passes its own ink check. Piecewise values preserve that grid rather than applying the global affine discrepancy to the points.

End labels, left -> right (printed numbers; not imposed on the trace calibration):

- mean: 61.4 -> 83.1.
- upper: 53.6 -> 71.2.
- lower: 69.2 -> 94.0.

Each series has eleven trace samples, in drawing order: left ink end, nominal Dr 0.1 through 0.9, right ink end. Dashed samples falling in gaps move to the nearest visible dash end; individual notes identify moves. Enlarged crops were used to distinguish curve ink from grid ink. Bounds represent half the observed stroke thickness; overlapping end strokes use the merged ink width. The stroke meets the frame at most ends, so its exact termination within the frame cannot be separated from frame ink. Endpoint features repeat the endpoint coordinates; label features lie at the bounding-box centre of their printed glyphs (2 px centre-reading bound). Native coordinates of label features describe their page position, not a measurement of the number printed in the label. No markers, knees or interior peaks are drawn; these monotonic straight traces have endpoint extrema already recorded. Rules 8 and 9 have no applicable symbols or derived-envelope identities.

The task text says 25–65 pcf for all pages; this page prints a different range, recorded above and used in calibration.

Counts: mean: 11 trace, 4 feature; upper: 11 trace, 4 feature; lower: 11 trace, 4 feature.
