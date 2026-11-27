# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b8\rederived\claude\FC-10C\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b8\rederived\codex\FC-10C\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4321 | 3.4323 |
| y per px | 3.4242 | 3.4241 |
| RMS residual x, y | 4.123, 11.181 | 4.030, 10.972 |

Corners of claude's box [468, 1455, 2555, 3865] mapped by both calibrations (tolerance 11.59 in x, 25.58 in y):

- (-95.0, 8078.6) vs (-95.2, 8078.2)
- (7067.8, 8145.6) vs (7068.0, 8145.7)
- (-63.2, -173.4) vs (-63.5, -173.4)
- (7099.5, -106.4) vs (7099.8, -106.0)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.37 | 0.56 | 0.47 | 24 | 1.31 | 1.04 | agree |
| x | 1000 | 0.11 | 0.44 | 0.48 | 24 | 0.72 | 0.76 | agree |
| x | 2000 | 0.06 | 0.67 | 0.65 | 24 | 1.08 | 1.04 | agree |
| x | 3000 | 0.19 | 0.31 | 0.29 | 24 | 0.64 | 0.65 | agree |
| x | 4000 | 0.00 | 0.43 | 0.43 | 24 | 0.81 | 0.81 | agree |
| x | 5000 | 0.22 | 0.36 | 0.35 | 24 | 0.82 | 0.68 | agree |
| x | 6000 | 0.30 | 0.41 | 0.47 | 24 | 0.72 | 1.00 | agree |
| x | 7000 | 0.11 | 0.31 | 0.31 | 24 | 0.50 | 0.50 | agree |
| y | 0 | 0.42 | 0.32 | 0.24 | 21 | 0.79 | 0.61 | agree |
| y | 1000 | 0.20 | 0.27 | 0.25 | 21 | 0.90 | 0.73 | agree |
| y | 2000 | 0.58 | 0.37 | 0.16 | 21 | 0.88 | 0.50 | agree |
| y | 3000 | 0.16 | 0.20 | 0.32 | 21 | 0.50 | 0.67 | agree |
| y | 4000 | 0.17 | 0.33 | 0.39 | 21 | 1.00 | 0.79 | agree |
| y | 5000 | 0.34 | 0.25 | 0.18 | 21 | 0.66 | 0.50 | agree |
| y | 6000 | 0.24 | 0.43 | 0.42 | 21 | 0.63 | 0.57 | agree |
| y | 7000 | 0.41 | 0.49 | 0.38 | 21 | 1.06 | 0.68 | agree |
| y | 8000 | 0.09 | 0.55 | 0.59 | 21 | 1.14 | 1.22 | agree |

Both maps along every verified line and every interval midline (354 places): largest difference 1.121 in x (tolerance 7.985, claude 0), 1.672 in y (tolerance 5.328, claude 2000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.39 px (claude: x 0.44, y 0.36), 0.37 px (codex: x 0.43, y 0.32), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 21; agreed 21; disagreed 0; unmatched 2 (kept as one-sided: 0 of claude, 2 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
