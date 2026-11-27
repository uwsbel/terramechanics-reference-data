# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b8\rederived\claude\FC-11B\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b8\rederived\codex\FC-11B\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4268 | 3.4269 |
| y per px | 3.4199 | 3.4198 |
| RMS residual x, y | 3.481, 10.903 | 3.442, 10.867 |

Corners of claude's box [630, 1365, 2730, 3765] mapped by both calibrations (tolerance 10.35 in x, 25.19 in y):

- (-97.9, 8063.0) vs (-97.5, 8062.7)
- (7098.3, 8116.0) vs (7098.9, 8116.1)
- (-82.2, -144.5) vs (-82.4, -144.5)
- (7114.1, -91.5) vs (7114.1, -91.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.19 | 0.63 | 0.61 | 24 | 1.04 | 0.94 | agree |
| x | 1000 | 0.13 | 0.24 | 0.25 | 24 | 0.58 | 0.70 | agree |
| x | 2000 | 0.18 | 0.59 | 0.62 | 24 | 0.71 | 0.87 | agree |
| x | 3000 | 0.14 | 0.38 | 0.42 | 24 | 0.69 | 0.61 | agree |
| x | 4000 | 0.19 | 0.46 | 0.44 | 24 | 0.74 | 0.64 | agree |
| x | 5000 | 0.08 | 0.33 | 0.32 | 24 | 0.50 | 0.56 | agree |
| x | 6000 | 0.29 | 0.36 | 0.36 | 24 | 0.73 | 0.98 | agree |
| x | 7000 | 0.18 | 0.23 | 0.23 | 24 | 0.50 | 0.50 | agree |
| y | 0 | 0.55 | 0.36 | 0.36 | 21 | 0.87 | 0.60 | agree |
| y | 1000 | 0.14 | 0.32 | 0.39 | 21 | 0.66 | 0.68 | agree |
| y | 2000 | 0.16 | 0.33 | 0.34 | 21 | 0.56 | 0.60 | agree |
| y | 3000 | 0.17 | 0.39 | 0.39 | 21 | 0.76 | 0.71 | agree |
| y | 4000 | 0.24 | 0.44 | 0.42 | 21 | 0.62 | 0.56 | agree |
| y | 5000 | 0.20 | 0.41 | 0.39 | 21 | 0.70 | 0.57 | agree |
| y | 6000 | 0.12 | 0.51 | 0.47 | 21 | 0.77 | 0.73 | agree |
| y | 7000 | 0.20 | 0.42 | 0.31 | 21 | 0.95 | 0.91 | agree |
| y | 8000 | 0.21 | 0.84 | 0.91 | 21 | 1.18 | 1.01 | agree |

Both maps along every verified line and every interval midline (369 places): largest difference 1.055 in x (tolerance 5.848, claude 6000), 1.998 in y (tolerance 5.18, codex 0); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.43 px (claude: x 0.40, y 0.45), 0.42 px (codex: x 0.41, y 0.44), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 17; agreed 17; disagreed 0; unmatched 1 (kept as one-sided: 0 of claude, 1 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
