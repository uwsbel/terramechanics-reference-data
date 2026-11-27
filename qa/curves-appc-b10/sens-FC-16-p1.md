# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b10\rederived\claude\FC-16\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b10\rederived\codex\FC-16\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 55 | 55 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0130 | 0.0130 |
| RMS residual x, y | 0.001, 0.007 | 0.001, 0.008 |

Corners of claude's box [680, 1240, 2480, 3495] mapped by both calibrations (tolerance 0.00 in x, 0.03 in y):

- (-0.1, 54.7) vs (-0.1, 54.7)
- (1.1, 54.5) vs (1.1, 54.5)
- (-0.1, 25.3) vs (-0.1, 25.3)
- (1.1, 25.2) vs (1.1, 25.2)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.28 | 0.43 | 0.31 | 12 | 0.75 | 0.58 | agree |
| x | 0.1 | 0.15 | 0.28 | 0.31 | 12 | 0.55 | 0.63 | agree |
| x | 0.2 | 0.47 | 0.23 | 0.23 | 12 | 0.53 | 0.50 | agree |
| x | 0.3 | 0.78 | 0.36 | 0.28 | 12 | 1.12 | 0.63 | agree |
| x | 0.4 | 0.16 | 0.33 | 0.37 | 12 | 0.61 | 0.76 | agree |
| x | 0.5 | 0.33 | 0.32 | 0.28 | 12 | 0.69 | 0.56 | agree |
| x | 0.6 | 0.62 | 0.26 | 0.22 | 12 | 0.82 | 0.62 | agree |
| x | 0.7 | 0.16 | 0.29 | 0.24 | 12 | 0.69 | 0.58 | agree |
| x | 0.8 | 0.08 | 0.30 | 0.30 | 12 | 0.66 | 0.61 | agree |
| x | 0.9 | 0.17 | 0.18 | 0.14 | 12 | 0.50 | 0.50 | agree |
| x | 1 | 0.35 | 0.20 | 0.19 | 12 | 0.50 | 0.58 | agree |
| y | 30 | 0.24 | 0.44 | 0.37 | 25 | 0.99 | 0.74 | agree |
| y | 35 | 0.15 | 0.55 | 0.56 | 25 | 0.91 | 1.02 | agree |
| y | 40 | 0.29 | 0.38 | 0.42 | 25 | 0.78 | 0.76 | agree |
| y | 45 | 0.57 | 0.43 | 0.49 | 25 | 0.91 | 0.81 | agree |
| y | 50 | 0.20 | 0.61 | 0.76 | 25 | 0.90 | 1.12 | agree |

Both maps along every verified line and every interval midline (324 places): largest difference 0.0005645 in x (tolerance 0.00113, codex 0.3), 0.006962 in y (tolerance 0.0225, codex 45); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 16 shared lines checked against the ink, mean of the median distances 0.35 px (claude: x 0.29, y 0.48), 0.34 px (codex: x 0.26, y 0.52), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

4 series in claude, 4 in codex.


## Points

Matched: 94; agreed 94; disagreed 0; unmatched 5 (kept as one-sided: 0 of claude, 5 of codex).

No point disagreements.
