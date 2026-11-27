# curves-appb-b1: independent blind reading

All five readings use only the supplied evidence packet. Pixel coordinates are on the original unrotated 300 dpi pages.

Counts are **marker / trace / feature**. RMS residuals are affine diagnostics in psi / kips/in.^2; the native CSVs use the verified piecewise map.

| Figure | Counts by series (M/T/F) | RMS x / y | By-eye x labels | By-eye y labels |
|---|---|---|---|---|
| [FB-3](FB-3/notes.md) | dr99: 5/9/4; dr30: 6/12/4 | 0.01126 / 0.00738 | 0, 6, 14 | 7, 13, 18 |
| [FB-4](FB-4/notes.md) | dr86: 7/10/4; dr22: 8/11/5 | 0.00928 / 0.00475 | 0, 6, 14 | 0, 5, 10 |
| [FB-5](FB-5/notes.md) | dr84: 7/9/4; dr26: 6/8/4 | 0.00982 / 0.01759 | 0, 6, 12 | 5, 20, 40 |
| [FB-6](FB-6/notes.md) | dr82: 7/10/4; dr02: 6/11/4 | 0.00817 / 0.01230 | 0, 6, 14 | 5, 17, 29 |
| [FB-7](FB-7/notes.md) | dr104: 9/0/1; dr99p5: 7/10/5; dr77: 9/12/5 | 0.00993 / 0.00662 | 0, 8, 16 | 0, 6, 11 |

All affine maximum residuals are below 0.5% of the respective axis span. Each tick stub and labelled frame side is measured and independently tilted. Short stubs provide limited directional leverage: the largest affine-versus-piecewise difference over B-6 dr82 is 0.825 psi and 0.263 kips/in.^2. Per-series sensitivities are recorded in each cal-p1/calibration-sensitivity.md; the small affine RMS is not a claim of cross-plot directional precision.

Ambiguities and reading limits:

- FB-3: the printed y label between 7 and 9 looks like "3"; spacing confirms 8. One unresolved dense knee cluster is represented by one marker with a wide bound.
- FB-4: overlapping dense and loose circle clusters are separately recorded where residual arcs distinguish them; their bounds are widened.
- FB-5: the lower right loose circle is a partial arc; the leading zero of the loose density label is damaged.
- FB-6: the skewed frame and all ticks retain separate fitted tilts; broken/frame-overlapping circles have wider bounds.
- FB-7: dr104 is squares with x and has no polyline. The open-circle line is dr99p5 and the filled-circle line is dr77. Axis/symbol ink conceals both line origins: first-point features have 70 px bounds and traces begin at separable ink.

Every requested sample blocked by a symbol or absent line ink is documented in trace-omissions.csv: 3, 1, 3, 0, and 6 rows for FB-3 through FB-7. These samples are omitted under rule 7, rather than placed on a symbol outline or white gap. Trace segment IDs preserve the breaks.

Each figure directory contains:

- cal-p1/ with calibration.json, measured anchors.csv, tick-fits.csv, verified-knots.json, line-fits.csv, all-label crops, trace ink crops, and calibration sensitivity.
- calibration-eye-checks.csv (three labels per axis).
- points-p1.csv and points-p1-native.csv, panel 1.
- overlay-p1.png at the source image dimensions.
- notes.md and trace-omissions.csv.

validation.json records 223 rows, six eye checks per figure, 96 verified axis knots, and zero trace centers on white. input-sha256.json records the source packet hashes. Coordinate-grid crops and helper scripts are kept under out/.

Rebuild from this workspace with the supplied Python interpreter, in this order: out/calibrate_ticks.py, out/tick_maps.py, out/refine_centers.py, out/extract.py, out/validate.py. The tools/ files are unchanged.
