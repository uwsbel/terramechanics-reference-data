# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b3\rederived\claude\FA-39\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b3\rederived\codex\FA-39\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 341 | 143 |
| x per px | 0.0007 | 0.0007 |
| y per px | 0.0000 | 0.0000 |
| RMS residual x, y | 0.001, 0.000 | 0.001, 0.000 |

Corners of claude's box [850, 1826, 2280, 3188] mapped by both calibrations (tolerance 0.00 in x, 0.00 in y (in the plotting coordinates of linear x, reciprocal y)):

- (-0.0, 64.8) vs (-0.0, 64.7)
- (1.0, 64.9) vs (1.0, 64.8)
- (-0.0, 95.4) vs (-0.0, 95.4)
- (1.0, 95.6) vs (1.0, 95.6)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.28 | 0.35 | 0.33 | 20 | 0.66 | 0.92 | agree |
| x | 0.1 | 0.30 | 0.26 | 0.34 | 20 | 0.50 | 0.72 | agree |
| x | 0.2 | 0.26 | 0.24 | 0.18 | 20 | 0.54 | 0.50 | agree |
| x | 0.3 | 0.49 | 0.39 | 0.41 | 20 | 1.05 | 0.53 | agree |
| x | 0.4 | 0.28 | 0.24 | 0.28 | 20 | 0.50 | 0.69 | agree |
| x | 0.5 | 0.62 | 0.29 | 0.28 | 20 | 0.50 | 0.71 | agree |
| x | 0.6 | 0.67 | 0.33 | 0.42 | 20 | 0.56 | 0.82 | agree |
| x | 0.7 | 0.47 | 0.27 | 0.24 | 20 | 0.83 | 0.56 | agree |
| x | 0.8 | 0.29 | 0.29 | 0.24 | 20 | 0.61 | 0.50 | agree |
| x | 0.9 | 0.25 | 0.21 | 0.22 | 20 | 0.56 | 0.53 | agree |
| x | 1 | 0.72 | 0.20 | 0.40 | 20 | 0.50 | 0.68 | agree |
| y | 65 | 0.12 | 0.28 | 0.28 | 25 | 0.54 | 0.50 | agree |
| y | 70 | 0.17 | 0.20 | 0.17 | 25 | 0.59 | 0.50 | agree |
| y | 75 | 0.34 | 0.18 | 0.31 | 25 | 0.55 | 0.54 | agree |
| y | 80 | 0.22 | 0.37 | 0.44 | 25 | 0.93 | 0.70 | agree |
| y | 85 | 0.12 | 0.35 | 0.37 | 25 | 0.51 | 0.50 | agree |
| y | 90 | 0.11 | 0.35 | 0.36 | 25 | 0.59 | 0.57 | agree |
| y | 95 | 0.15 | 0.32 | 0.28 | 25 | 0.51 | 0.50 | agree |
| y | 66 | | | | | 0.72 | | only in claude |
| y | 67 | | | | | 0.96 | | only in claude |
| y | 68 | | | | | 1.00 | | only in claude |
| y | 69 | | | | | 0.74 | | only in claude |
| y | 71 | | | | | 0.66 | | only in claude |
| y | 72 | | | | | 0.78 | | only in claude |
| y | 73 | | | | | 0.50 | | only in claude |
| y | 74 | | | | | 0.57 | | only in claude |
| y | 76 | | | | | 0.50 | | only in claude |
| y | 77 | | | | | 0.76 | | only in claude |
| y | 78 | | | | | 0.62 | | only in claude |
| y | 79 | | | | | 0.77 | | only in claude |
| y | 81 | | | | | 1.13 | | only in claude |
| y | 82 | | | | | 0.83 | | only in claude |
| y | 83 | | | | | 0.50 | | only in claude |
| y | 84 | | | | | 0.64 | | only in claude |
| y | 86 | | | | | 1.07 | | only in claude |
| y | 87 | | | | | 0.83 | | only in claude |
| y | 88 | | | | | 0.83 | | only in claude |
| y | 89 | | | | | 0.63 | | only in claude |
| y | 91 | | | | | 0.74 | | only in claude |
| y | 92 | | | | | 0.60 | | only in claude |
| y | 93 | | | | | 0.60 | | only in claude |
| y | 94 | | | | | 0.89 | | only in claude |
| y | 55 | | | | | | 0.55 | only in codex |
| y | 60 | | | | | | 0.50 | only in codex |
| y | 100 | | | | | | 0.52 | only in codex |
| y | 105 | | | | | | 0.53 | only in codex |
| y | 110 | | | | | | 0.50 | only in codex |
| y | 115 | | | | | | 0.52 | only in codex |

(In the plotting coordinates: linear x, reciprocal y.) Both maps along every verified line and every interval midline (649 places): largest difference 0.0005462 in x (tolerance 0.0009049, claude 1), 2.02e-05 in y (tolerance 4.08e-06, claude 89); 147 beyond the two maps' line errors.

Canonical reading: claude (**coverage cannot be ranked** (lines claude: x [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], y [65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0]; codex: x [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], y [55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0, 115.0]): recover the missing lines or name the canonical reading in overlays.csv; meanwhile first submission by the ink; 18 shared lines checked against the ink, mean of the median distances 0.28 px (claude: x 0.28, y 0.29), 0.31 px (codex: x 0.30, y 0.32)); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 39; agreed 39; disagreed 0; unmatched 7 (kept as one-sided: 0 of claude, 7 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
