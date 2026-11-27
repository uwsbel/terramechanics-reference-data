# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b11\rederived\claude\FC-22\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b11\rederived\codex\FC-22\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 55 | 55 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0130 | 0.0130 |
| RMS residual x, y | 0.001, 0.013 | 0.001, 0.012 |

Corners of claude's box [770, 1450, 2500, 3360] mapped by both calibrations (tolerance 0.00 in x, 0.04 in y):

- (-0.0, 52.5) vs (-0.0, 52.5)
- (1.1, 52.3) vs (1.1, 52.3)
- (-0.1, 27.6) vs (-0.1, 27.6)
- (1.0, 27.4) vs (1.0, 27.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.76 | 0.50 | 0.42 | 12 | 1.11 | 0.70 | agree |
| x | 0.1 | 0.64 | 0.54 | 0.30 | 12 | 1.27 | 0.57 | agree |
| x | 0.2 | 0.41 | 0.50 | 0.40 | 12 | 0.82 | 0.66 | agree |
| x | 0.3 | 0.48 | 0.32 | 0.26 | 12 | 0.89 | 0.50 | agree |
| x | 0.4 | 0.65 | 0.47 | 0.41 | 12 | 0.92 | 0.59 | agree |
| x | 0.5 | 0.21 | 0.21 | 0.21 | 12 | 0.61 | 0.50 | agree |
| x | 0.6 | 0.82 | 0.30 | 0.43 | 12 | 0.94 | 0.70 | agree |
| x | 0.7 | 0.10 | 0.22 | 0.25 | 12 | 0.67 | 0.59 | agree |
| x | 0.8 | 0.48 | 0.29 | 0.19 | 12 | 0.69 | 0.54 | agree |
| x | 0.9 | 0.31 | 0.29 | 0.34 | 12 | 0.81 | 0.68 | agree |
| x | 1 | 0.25 | 0.46 | 0.24 | 12 | 0.77 | 0.55 | agree |
| y | 30 | 0.22 | 0.19 | 0.20 | 25 | 0.60 | 0.63 | agree |
| y | 35 | 0.26 | 0.30 | 0.27 | 25 | 0.61 | 0.67 | agree |
| y | 40 | 0.27 | 0.35 | 0.32 | 25 | 0.56 | 0.52 | agree |
| y | 45 | 0.26 | 0.54 | 0.51 | 25 | 0.82 | 1.07 | agree |
| y | 50 | 0.25 | 0.27 | 0.33 | 25 | 0.68 | 0.59 | agree |

Both maps along every verified line and every interval midline (324 places): largest difference 0.0005083 in x (tolerance 0.001049, claude 0.6), 0.003367 in y (tolerance 0.02467, claude 50); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 16 shared lines checked against the ink, mean of the median distances 0.36 px (claude: x 0.37, y 0.33), 0.32 px (codex: x 0.31, y 0.33), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

4 series in claude, 4 in codex.


## Points

Matched: 74; agreed 74; disagreed 0; unmatched 3 (kept as one-sided: 0 of claude, 3 of codex).

No point disagreements.
