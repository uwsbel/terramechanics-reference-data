# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b8\rederived\claude\FC-11A\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b8\rederived\codex\FC-11A\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4249 | 3.4250 |
| y per px | 3.4184 | 3.4184 |
| RMS residual x, y | 3.887, 9.972 | 3.841, 10.016 |

Corners of claude's box [685, 1440, 2780, 3830] mapped by both calibrations (tolerance 11.15 in x, 23.41 in y):

- (-99.1, 8058.3) vs (-99.1, 8058.2)
- (7076.0, 8121.4) vs (7076.3, 8121.6)
- (-77.0, -111.2) vs (-76.9, -111.4)
- (7098.1, -48.2) vs (7098.4, -48.0)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.16 | 0.30 | 0.27 | 24 | 0.50 | 0.50 | agree |
| x | 1000 | 0.08 | 0.34 | 0.34 | 24 | 0.50 | 0.56 | agree |
| x | 2000 | 0.27 | 0.36 | 0.45 | 24 | 0.71 | 0.99 | agree |
| x | 3000 | 0.40 | 0.34 | 0.23 | 24 | 0.64 | 0.58 | agree |
| x | 4000 | 0.27 | 0.49 | 0.53 | 24 | 0.68 | 0.96 | agree |
| x | 5000 | 0.11 | 0.22 | 0.24 | 24 | 0.54 | 0.50 | agree |
| x | 6000 | 0.15 | 0.35 | 0.38 | 24 | 0.95 | 1.10 | agree |
| x | 7000 | 0.03 | 0.17 | 0.19 | 24 | 0.50 | 0.50 | agree |
| y | 0 | 0.12 | 0.38 | 0.41 | 21 | 0.76 | 0.89 | agree |
| y | 1000 | 0.20 | 0.31 | 0.24 | 21 | 0.83 | 0.62 | agree |
| y | 2000 | 0.19 | 0.53 | 0.38 | 21 | 1.14 | 0.97 | agree |
| y | 3000 | 0.09 | 0.49 | 0.43 | 21 | 0.96 | 0.86 | agree |
| y | 4000 | 0.11 | 0.31 | 0.38 | 21 | 0.81 | 0.88 | agree |
| y | 5000 | 0.10 | 0.37 | 0.39 | 21 | 0.86 | 0.87 | agree |
| y | 6000 | 0.08 | 0.38 | 0.36 | 21 | 0.67 | 0.60 | agree |
| y | 7000 | 0.17 | 0.45 | 0.46 | 21 | 0.76 | 0.65 | agree |
| y | 8000 | 0.07 | 0.65 | 0.62 | 21 | 1.32 | 1.37 | agree |

Both maps along every verified line and every interval midline (360 places): largest difference 1.105 in x (tolerance 5.693, codex 3000), 0.5903 in y (tolerance 5.763, between claude 0 and codex 1000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.38 px (claude: x 0.32, y 0.43), 0.37 px (codex: x 0.33, y 0.41), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 19; agreed 19; disagreed 0; unmatched 2 (kept as one-sided: 0 of claude, 2 of codex).

No point disagreements.
