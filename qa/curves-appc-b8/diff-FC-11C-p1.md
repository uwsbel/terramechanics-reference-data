# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b8\rederived\claude\FC-11C\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b8\rederived\codex\FC-11C\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4305 | 3.4306 |
| y per px | 3.4177 | 3.4176 |
| RMS residual x, y | 5.591, 10.954 | 5.599, 10.825 |

Corners of claude's box [575, 1395, 2705, 3800] mapped by both calibrations (tolerance 14.62 in x, 25.20 in y):

- (-98.5, 8137.2) vs (-98.0, 8136.7)
- (7207.4, 8064.0) vs (7208.2, 8063.8)
- (-230.8, -82.0) vs (-231.4, -82.3)
- (7075.1, -155.2) vs (7074.8, -155.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.12 | 1.38 | 1.30 | 24 | 1.56 | 1.59 | agree; claude off the ink; codex off the ink |
| x | 1000 | 0.22 | 0.38 | 0.44 | 24 | 0.68 | 0.74 | agree |
| x | 2000 | 0.28 | 0.55 | 0.56 | 24 | 1.20 | 1.19 | agree |
| x | 3000 | 0.39 | 0.25 | 0.30 | 24 | 0.55 | 0.68 | agree |
| x | 4000 | 0.77 | 0.38 | 0.40 | 24 | 1.12 | 0.87 | agree |
| x | 5000 | 0.30 | 0.46 | 0.43 | 24 | 0.88 | 0.73 | agree |
| x | 6000 | 0.38 | 0.40 | 0.40 | 24 | 1.03 | 0.80 | agree |
| x | 7000 | 0.22 | 0.32 | 0.40 | 24 | 0.71 | 0.69 | agree |
| y | 0 | 0.33 | 0.18 | 0.24 | 21 | 0.80 | 0.50 | agree |
| y | 1000 | 0.32 | 0.25 | 0.41 | 20 | 0.55 | 0.73 | agree |
| y | 2000 | 0.25 | 0.35 | 0.33 | 21 | 0.65 | 0.50 | agree |
| y | 3000 | 0.41 | 0.44 | 0.36 | 21 | 0.92 | 0.57 | agree |
| y | 4000 | 0.33 | 0.25 | 0.41 | 19 | 0.87 | 0.67 | agree |
| y | 5000 | 0.24 | 0.44 | 0.40 | 20 | 0.87 | 1.00 | agree |
| y | 6000 | 0.38 | 0.52 | 0.37 | 20 | 0.92 | 0.78 | agree |
| y | 7000 | 0.14 | 0.42 | 0.42 | 20 | 0.83 | 0.91 | agree |
| y | 8000 | 0.71 | 0.59 | 0.46 | 20 | 1.38 | 0.89 | agree |

Both maps along every verified line and every interval midline (344 places): largest difference 2.009 in x (tolerance 6.803, claude 4000), 2.028 in y (tolerance 7.765, codex 8000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.44 px (claude: x 0.51, y 0.38), 0.45 px (codex: x 0.53, y 0.38), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 23; agreed 23; disagreed 0; unmatched 1 (kept as one-sided: 0 of claude, 1 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
