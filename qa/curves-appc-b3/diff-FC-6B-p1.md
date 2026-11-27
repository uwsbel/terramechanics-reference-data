# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b3\rederived\claude\FC-6B\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b3\rederived\codex\FC-6B\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 25 | 30 |
| x per px | 0.1734 | 0.1709 |
| y per px | 3.4089 | 3.4078 |
| RMS residual x, y | 0.555, 8.045 | 1.463, 8.029 |

Corners of claude's box [900, 895, 2140, 2130] mapped by both calibrations (tolerance 2.19 in x, 19.48 in y):

- (40.7, 4100.7) vs (42.8, 4099.9)
- (255.8, 4102.6) vs (254.7, 4102.1)
- (40.1, -109.3) vs (42.1, -108.7)
- (255.1, -107.4) vs (254.0, -106.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.12 | 0.40 | 0.40 | 24 | 0.61 | 0.52 | agree |
| x | 50 | 0.00 | 0.37 | 0.37 | 12 | 0.96 | 0.95 | agree |
| x | 100 | 0.05 | 0.22 | 0.23 | 12 | 0.50 | 0.50 | agree |
| x | 150 | 0.09 | 0.33 | 0.34 | 12 | 0.92 | 0.94 | agree |
| x | 200 | 0.48 | 0.24 | 0.15 | 12 | 0.50 | 0.59 | agree |
| x | 250 | 0.29 | 0.27 | 0.36 | 12 | 1.17 | 1.00 | agree |
| y | 0 | 0.11 | 0.39 | 0.33 | 12 | 0.78 | 0.78 | agree |
| y | 1000 | 0.17 | 0.46 | 0.34 | 12 | 1.00 | 0.63 | agree |
| y | 2000 | 0.24 | 0.48 | 0.52 | 12 | 0.76 | 1.08 | agree |
| y | 3000 | 0.34 | 0.31 | 0.30 | 12 | 0.79 | 0.94 | agree |
| y | 4000 | 0.07 | 0.62 | 0.62 | 12 | 1.68 | 1.35 | agree |

Both maps along every verified line and every interval midline (250 places): largest difference 0.07457 in x (tolerance 0.3606, codex 200), 1.381 in y (tolerance 7.358, claude 3000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.37 px (claude: x 0.30, y 0.45), 0.36 px (codex: x 0.31, y 0.42), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 354; agreed 353; disagreed 1; unmatched 12 (kept as one-sided: 0 of claude, 12 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n734 | marker | 11/11 | 217.8, 348.3 (0.5, 9.6) | 218.9, 326.9 (0.5, 9.2) | -1.2 | +21.4 | **disagree** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
