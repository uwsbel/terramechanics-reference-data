# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b7\rederived\claude\FC-10A\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b7\rederived\codex\FC-10A\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4305 | 3.4309 |
| y per px | 3.4213 | 3.4213 |
| RMS residual x, y | 3.577, 9.927 | 3.457, 10.235 |

Corners of claude's box [575, 1377, 2700, 3762] mapped by both calibrations (tolerance 10.46 in x, 23.58 in y):

- (-79.7, 8099.0) vs (-79.1, 8099.1)
- (7209.2, 8023.6) vs (7210.6, 8023.5)
- (-211.8, -60.4) vs (-212.3, -60.3)
- (7077.1, -135.8) vs (7077.3, -135.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.11 | 0.43 | 0.37 | 24 | 0.77 | 0.63 | agree |
| x | 1000 | 0.54 | 0.24 | 0.35 | 24 | 1.31 | 0.73 | agree |
| x | 2000 | 0.49 | 0.61 | 0.61 | 24 | 1.04 | 1.21 | agree |
| x | 3000 | 0.24 | 0.28 | 0.23 | 24 | 0.69 | 0.70 | agree |
| x | 4000 | 0.13 | 0.28 | 0.32 | 24 | 0.78 | 0.71 | agree |
| x | 5000 | 0.27 | 0.41 | 0.36 | 24 | 0.70 | 0.58 | agree |
| x | 6000 | 0.61 | 0.38 | 0.32 | 24 | 0.96 | 0.81 | agree |
| x | 7000 | 0.39 | 0.40 | 0.48 | 24 | 0.50 | 0.86 | agree |
| y | 0 | 0.41 | 0.48 | 0.25 | 21 | 1.06 | 0.71 | agree |
| y | 1000 | 0.04 | 0.31 | 0.29 | 21 | 0.50 | 0.51 | agree |
| y | 2000 | 0.61 | 0.50 | 0.27 | 21 | 1.28 | 0.63 | agree |
| y | 3000 | 0.36 | 0.31 | 0.27 | 21 | 0.59 | 0.50 | agree |
| y | 4000 | 0.52 | 0.25 | 0.36 | 21 | 1.11 | 0.52 | agree |
| y | 5000 | 0.57 | 0.21 | 0.30 | 21 | 0.60 | 0.68 | agree |
| y | 6000 | 0.57 | 0.48 | 0.32 | 21 | 1.13 | 0.82 | agree |
| y | 7000 | 0.26 | 0.43 | 0.39 | 21 | 0.62 | 0.72 | agree |
| y | 8000 | 0.38 | 0.53 | 0.30 | 21 | 0.96 | 0.81 | agree |

Both maps along every verified line and every interval midline (344 places): largest difference 1.704 in x (tolerance 6.26, claude 6000), 1.68 in y (tolerance 6.523, codex 2000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.38 px (claude: x 0.38, y 0.39), 0.34 px (codex: x 0.38, y 0.31), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 18; agreed 18; disagreed 0; unmatched 0 (kept as one-sided: 0 of claude, 0 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
