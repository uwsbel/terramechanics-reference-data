Blind reading, batch curves-appa-b3, FA-47, panel 1. Only packet pages and protocol were used. All pixel coordinates refer to the original unrotated page, p0096.png.

Calibration uses printed Dr 0 through 1.0 (all eleven labelled vertical lines), linear rightward, and labelled unit weights 55 through 115 pcf in steps of 5, reciprocal downward. Unlabelled horizontal subdivisions are not knots. Both the minimum-density and maximum-density labels refer to the same horizontal lines. The extra grid above the first labelled line in A-3, A-7 and A-23 is excluded. Trace/label positions above the first verified labelled line are explicitly extrapolated; no reciprocal is typed as a measurement.

Detected lines were refined against page ink. Standard 6 px half-window is used for checks except the thick bottom frame, whose 14 px half-window includes the white background needed to locate its core. This adaptation is in out/reading_lib.py; tools were not modified. All 11 x and 13 y knots pass the protocol's coverage and 2 px end-deviation checks; none are predicted. Initial detection is retained for reproducibility. Values and read bounds use piecewise interpolation with verified line errors and the declared transform. Native y values are pcf. The affine map is diagnostic only.

Affine RMS residual: Dr 0.0008459017 (0.0846% of span; 1.168 px), reciprocal-y 7.094567e-06 (0.0748% of reciprocal span; 1.946 px). Maximum residual: x 0.3348% and reciprocal-y 0.2145% of span. Three by-eye checks per axis: Dr 0, 0.5, 1.0; pcf 55, 85, 115. See calibration-eye-checks.csv and the check crops. Every other labelled calibration line was also checked against the page grid.

End labels, left -> right (printed numbers; not imposed on the trace calibration):

- mean: 74.4 -> 89.4.
- upper: 73.5 -> 89.4.
- lower: 75.3 -> 89.4.

Each series has eleven trace samples, in drawing order: left ink end, nominal Dr 0.1 through 0.9, right ink end. Dashed samples falling in gaps move to the nearest visible dash end; individual notes identify moves. Enlarged crops were used to distinguish curve ink from grid ink. Bounds represent half the observed stroke thickness; overlapping end strokes use the merged ink width. The stroke meets the frame at most ends, so its exact termination within the frame cannot be separated from frame ink. Endpoint features repeat the endpoint coordinates; label features lie at the bounding-box centre of their printed glyphs (2 px centre-reading bound). Native coordinates of label features describe their page position, not a measurement of the number printed in the label. No markers, knees or interior peaks are drawn; these monotonic straight traces have endpoint extrema already recorded. Rules 8 and 9 have no applicable symbols or derived-envelope identities.

The task text says 25–65 pcf for all pages; this page prints a different range, recorded above and used in calibration.

The caption prints RSM Soil without an a/b suffix; the supplied figure and series IDs are retained.

Ambiguity: the single printed 89.4 right label has a short detached leader beside the converging ends. There are no three separate right labels. It is recorded at the same text centre for each series to identify the shared annotation, not as three independently printed numbers. Its individual leader association is uncertain: closest to upper, but adjacent to the combined cluster. Mean and lower meet in merged ink at the right frame; their last feature uses the same observed cluster centre and a 5 px half-width bound. Upper ends slightly above them.

Counts: mean: 11 trace, 4 feature; upper: 11 trace, 4 feature; lower: 11 trace, 4 feature.
