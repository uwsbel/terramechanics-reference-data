# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b9\rederived\claude\FC-13\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b9\rederived\codex\FC-13\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4334 | 3.4336 |
| y per px | 3.4230 | 3.4231 |
| RMS residual x, y | 4.358, 10.129 | 3.956, 10.033 |

Corners of claude's box [680, 1350, 2775, 3755] mapped by both calibrations (tolerance 11.75 in x, 23.58 in y):

- (-78.0, 8090.8) vs (-78.0, 8090.9)
- (7114.9, 8098.0) vs (7115.3, 8098.0)
- (-112.5, -141.6) vs (-112.6, -141.6)
- (7080.4, -134.4) vs (7080.7, -134.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.20 | 0.35 | 0.33 | 24 | 0.82 | 0.73 | agree |
| x | 1000 | 0.15 | 0.33 | 0.39 | 24 | 0.59 | 0.51 | agree |
| x | 2000 | 0.12 | 0.47 | 0.49 | 24 | 1.07 | 1.00 | agree |
| x | 3000 | 0.27 | 0.40 | 0.33 | 24 | 0.99 | 0.69 | agree |
| x | 4000 | 0.31 | 0.35 | 0.46 | 24 | 0.89 | 0.84 | agree |
| x | 5000 | 0.48 | 0.46 | 0.37 | 24 | 0.93 | 0.66 | agree |
| x | 6000 | 0.79 | 0.44 | 0.74 | 24 | 0.69 | 1.38 | agree |
| x | 7000 | 0.32 | 0.30 | 0.35 | 24 | 0.64 | 0.67 | agree |
| y | 0 | 0.22 | 0.33 | 0.28 | 21 | 0.56 | 0.52 | agree |
| y | 1000 | 0.08 | 0.26 | 0.27 | 21 | 0.66 | 0.67 | agree |
| y | 2000 | 0.04 | 0.29 | 0.30 | 21 | 0.53 | 0.51 | agree |
| y | 3000 | 0.27 | 0.31 | 0.32 | 21 | 0.60 | 0.55 | agree |
| y | 4000 | 0.07 | 0.28 | 0.33 | 21 | 0.62 | 0.71 | agree |
| y | 5000 | 0.31 | 0.27 | 0.26 | 21 | 0.59 | 0.59 | agree |
| y | 6000 | 0.00 | 0.17 | 0.17 | 21 | 0.59 | 0.59 | agree |
| y | 7000 | 0.15 | 0.24 | 0.28 | 21 | 0.54 | 0.50 | agree |
| y | 8000 | 0.11 | 0.30 | 0.39 | 21 | 0.61 | 0.64 | agree |

Both maps along every verified line and every interval midline (402 places): largest difference 2.285 in x (tolerance 7.97, claude 6000), 1.184 in y (tolerance 4.621, claude 5000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.33 px (claude: x 0.39, y 0.27), 0.36 px (codex: x 0.43, y 0.29), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 19; agreed 19; disagreed 0; unmatched 2 (kept as one-sided: 0 of claude, 2 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
