# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b5\rederived\claude\FC-4A\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b5\rederived\codex\FC-4A\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 54 | 14 |
| x per px | 3.4352 | 3.4289 |
| y per px | 3.4399 | 3.4248 |
| RMS residual x, y | 0.728, 0.472 | 6.727, 2.267 |

Corners of claude's box [900, 1145, 2400, 3510] mapped by both calibrations (tolerance 10.89 in x, 6.18 in y):

- (-75.0, 8053.9) vs (-70.6, 8019.4)  **disagree**
- (5077.8, 8081.0) vs (5072.8, 8042.4)  **disagree**
- (-76.8, -81.3) vs (-81.9, -80.2)
- (5076.1, -54.2) vs (5061.5, -57.3)  **disagree**

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.14 | 0.37 | 0.30 | 21 | 0.50 | 0.51 | agree |
| x | 5000 | 3.44 | 0.14 | 1.61 | 30 | 0.55 | 2.57 | **disagree**; codex off the ink |
| x | 1000 | | | | | | 0.50 | only in codex |
| x | 2000 | | | | | | 0.50 | only in codex |
| x | 3000 | | | | | | 0.50 | only in codex |
| x | 4000 | | | | | | 0.50 | only in codex |
| y | 0 | 1.26 | 0.41 | 0.49 | 15 | 0.88 | 1.46 | agree |
| y | 8000 | | | | | 0.60 | | only in claude |
| y | 1000 | | | | | | 1.53 | only in codex |
| y | 2000 | | | | | | 1.33 | only in codex |
| y | 3000 | | | | | | 0.50 | only in codex |
| y | 4000 | | | | | | 0.50 | only in codex |
| y | 5000 | | | | | | 0.50 | only in codex |
| y | 6000 | | | | | | 0.87 | only in codex |
| y | 7000 | | | | | | 0.86 | only in codex |

Both maps along every verified line and every interval midline (206 places): largest difference 23.59 in x (tolerance 3.569, codex 2000), 36.06 in y (tolerance 6.027, claude 8000); 123 beyond the two maps' line errors.

Canonical reading: codex (named by the batch: Codex's map is fitted on the measured tick marks; Claude's on lines predicted from the frame, whose small residual shows internal consistency only (D-024); the data-sheet peaks agree with Codex's map by 16 psf more on the Dr 0 group; **coverage cannot be ranked** (lines claude: x [0.0, 5000.0], y [0.0, 8000.0]; codex: x [0.0, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0], y [0.0, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0, 6000.0, 7000.0]): recover the missing lines or name the canonical reading in overlays.csv; meanwhile first submission by the ink; 3 shared lines checked against the ink, mean of the median distances 0.30 px (claude: x 0.25, y 0.41), 0.80 px (codex: x 0.95, y 0.49)); points are evaluated at codex's samples.

## Series

2 series in codex, 2 in claude.


## Points

Matched: 57; agreed 54; disagreed 3; unmatched 2 (kept as one-sided: 0 of codex, 2 of claude).

| series | kind | seq (codex/claude) | codex x, y (bounds) | claude x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| dr0 | marker | 3/3 | 2929.4, 2760.5 (8.6, 9.3) | 2946.9, 2772.5 (8.7, 9.6) | -17.5 | -11.9 | **disagree** |
| dr0 | marker | 5/5 | 4714.0, 4557.7 (14.1, 8.6) | 4699.0, 4589.1 (8.7, 9.4) | +15.0 | -31.4 | **disagree** |
| dr95 | marker | 2/2 | 1703.0, 4412.8 (8.4, 8.6) | 1715.7, 4432.6 (8.6, 9.4) | -12.7 | -19.8 | **disagree** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
