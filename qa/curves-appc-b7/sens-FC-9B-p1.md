# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b7\rederived\claude\FC-9B\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b7\rederived\codex\FC-9B\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4310 | 3.4311 |
| y per px | 3.4196 | 3.4198 |
| RMS residual x, y | 4.081, 10.966 | 4.145, 10.990 |

Corners of claude's box [622, 1452, 2720, 3832] mapped by both calibrations (tolerance 11.66 in x, 25.38 in y):

- (-50.0, 8087.1) vs (-50.9, 8087.4)
- (7147.8, 8057.5) vs (7147.2, 8058.0)
- (-132.2, -51.6) vs (-132.5, -51.7)
- (7065.6, -81.1) vs (7065.6, -81.0)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.58 | 0.55 | 0.56 | 24 | 0.91 | 1.08 | agree |
| x | 1000 | 0.44 | 0.55 | 0.38 | 24 | 0.98 | 0.96 | agree |
| x | 2000 | 0.51 | 0.55 | 0.60 | 24 | 1.07 | 1.08 | agree |
| x | 3000 | 0.25 | 0.27 | 0.24 | 24 | 0.63 | 0.75 | agree |
| x | 4000 | 0.59 | 0.31 | 0.27 | 24 | 0.79 | 0.61 | agree |
| x | 5000 | 0.38 | 0.30 | 0.32 | 24 | 0.57 | 0.60 | agree |
| x | 6000 | 0.26 | 0.57 | 0.58 | 24 | 1.09 | 0.80 | agree |
| x | 7000 | 0.26 | 0.43 | 0.53 | 24 | 0.87 | 0.90 | agree |
| y | 0 | 0.06 | 0.46 | 0.44 | 21 | 0.62 | 0.58 | agree |
| y | 1000 | 0.36 | 0.41 | 0.45 | 21 | 1.10 | 0.75 | agree |
| y | 2000 | 0.24 | 0.39 | 0.33 | 21 | 1.08 | 0.84 | agree |
| y | 3000 | 0.14 | 0.38 | 0.40 | 21 | 0.64 | 0.80 | agree |
| y | 4000 | 0.31 | 0.34 | 0.35 | 21 | 0.62 | 0.70 | agree |
| y | 5000 | 0.06 | 0.59 | 0.60 | 21 | 0.88 | 0.89 | agree |
| y | 6000 | 0.29 | 0.28 | 0.35 | 21 | 0.59 | 0.72 | agree |
| y | 7000 | 0.40 | 0.55 | 0.56 | 21 | 0.75 | 1.03 | agree |
| y | 8000 | 0.35 | 0.70 | 0.74 | 21 | 1.17 | 0.95 | agree |

Both maps along every verified line and every interval midline (354 places): largest difference 2.063 in x (tolerance 6.968, claude 0), 1.454 in y (tolerance 6.073, codex 7000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.45 px (claude: x 0.44, y 0.46), 0.45 px (codex: x 0.44, y 0.47), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 15; agreed 15; disagreed 0; unmatched 2 (kept as one-sided: 0 of claude, 2 of codex).

No point disagreements.
