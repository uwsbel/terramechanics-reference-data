# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b10\rederived\claude\FC-18\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b10\rederived\codex\FC-18\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 55 | 55 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0130 | 0.0130 |
| RMS residual x, y | 0.001, 0.011 | 0.001, 0.011 |

Corners of claude's box [800, 1200, 2560, 3370] mapped by both calibrations (tolerance 0.00 in x, 0.04 in y):

- (-0.0, 54.1) vs (-0.0, 54.1)
- (1.1, 53.9) vs (1.1, 53.9)
- (-0.1, 25.8) vs (-0.1, 25.8)
- (1.1, 25.7) vs (1.1, 25.7)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.70 | 0.35 | 0.19 | 12 | 0.94 | 0.50 | agree |
| x | 0.1 | 0.29 | 0.24 | 0.20 | 12 | 0.58 | 0.50 | agree |
| x | 0.2 | 0.16 | 0.26 | 0.25 | 12 | 0.76 | 0.54 | agree |
| x | 0.3 | 0.68 | 0.51 | 0.17 | 12 | 0.78 | 0.50 | agree |
| x | 0.4 | 0.28 | 0.26 | 0.22 | 12 | 0.51 | 0.50 | agree |
| x | 0.5 | 0.54 | 0.25 | 0.20 | 12 | 0.70 | 0.50 | agree |
| x | 0.6 | 0.36 | 0.27 | 0.26 | 12 | 0.54 | 0.50 | agree |
| x | 0.7 | 0.44 | 0.11 | 0.21 | 12 | 0.50 | 0.80 | agree |
| x | 0.8 | 0.31 | 0.26 | 0.24 | 12 | 0.77 | 0.50 | agree |
| x | 0.9 | 0.33 | 0.26 | 0.27 | 12 | 1.16 | 0.50 | agree |
| x | 1 | 0.43 | 0.36 | 0.21 | 12 | 0.58 | 0.67 | agree |
| y | 30 | 0.39 | 0.42 | 0.33 | 25 | 1.08 | 0.76 | agree |
| y | 35 | 0.47 | 0.46 | 0.45 | 25 | 1.16 | 0.67 | agree |
| y | 40 | 0.32 | 0.62 | 0.60 | 25 | 0.97 | 1.11 | agree |
| y | 45 | 0.17 | 0.71 | 0.70 | 25 | 1.04 | 0.88 | agree |
| y | 50 | 0.18 | 0.58 | 0.58 | 25 | 1.17 | 0.97 | agree |

Both maps along every verified line and every interval midline (317 places): largest difference 0.0005858 in x (tolerance 0.0009291, claude 0), 0.005387 in y (tolerance 0.02491, codex 35); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 16 shared lines checked against the ink, mean of the median distances 0.37 px (claude: x 0.28, y 0.56), 0.32 px (codex: x 0.22, y 0.53), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

4 series in claude, 4 in codex.


## Points

Matched: 81; agreed 81; disagreed 0; unmatched 1 (kept as one-sided: 0 of claude, 1 of codex).

No point disagreements.
