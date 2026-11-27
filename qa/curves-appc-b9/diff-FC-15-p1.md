# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b9\rederived\claude\FC-15\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b9\rederived\codex\FC-15\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4332 | 3.4328 |
| y per px | 3.4185 | 3.4186 |
| RMS residual x, y | 6.027, 12.068 | 5.800, 12.014 |

Corners of claude's box [650, 1345, 2765, 3755] mapped by both calibrations (tolerance 15.26 in x, 27.50 in y):

- (-81.7, 8099.3) vs (-80.9, 8099.4)
- (7179.2, 8079.2) vs (7179.1, 8079.4)
- (-149.9, -139.3) vs (-149.7, -139.3)
- (7111.0, -159.4) vs (7110.4, -159.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.23 | 0.39 | 0.54 | 24 | 0.85 | 0.80 | agree |
| x | 1000 | 0.29 | 0.15 | 0.24 | 24 | 0.82 | 0.54 | agree |
| x | 2000 | 0.40 | 0.38 | 0.56 | 24 | 0.94 | 0.96 | agree |
| x | 3000 | 0.10 | 0.33 | 0.38 | 24 | 0.60 | 0.65 | agree |
| x | 4000 | 0.37 | 0.37 | 0.44 | 24 | 0.73 | 1.14 | agree |
| x | 5000 | 0.10 | 0.35 | 0.34 | 24 | 0.53 | 0.63 | agree |
| x | 6000 | 0.21 | 0.62 | 0.51 | 24 | 1.07 | 0.85 | agree |
| x | 7000 | 0.34 | 0.36 | 0.31 | 24 | 0.61 | 0.78 | agree |
| y | 0 | 0.10 | 0.34 | 0.32 | 21 | 0.52 | 0.50 | agree |
| y | 1000 | 0.16 | 0.23 | 0.22 | 21 | 0.68 | 0.50 | agree |
| y | 2000 | 0.18 | 0.40 | 0.34 | 21 | 0.75 | 0.65 | agree |
| y | 3000 | 0.19 | 0.47 | 0.50 | 21 | 0.85 | 0.68 | agree |
| y | 4000 | 0.20 | 0.20 | 0.18 | 21 | 0.54 | 0.50 | agree |
| y | 5000 | 0.10 | 0.27 | 0.22 | 21 | 0.71 | 0.60 | agree |
| y | 6000 | 0.23 | 0.28 | 0.35 | 21 | 0.50 | 0.66 | agree |
| y | 7000 | 0.07 | 0.46 | 0.46 | 21 | 0.84 | 0.78 | agree |
| y | 8000 | 0.10 | 0.47 | 0.50 | 21 | 0.80 | 0.86 | agree |

Both maps along every verified line and every interval midline (360 places): largest difference 1.108 in x (tolerance 6.539, claude 2000), 0.6953 in y (tolerance 5.118, claude 6000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.36 px (claude: x 0.37, y 0.35), 0.38 px (codex: x 0.42, y 0.34), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 21; agreed 21; disagreed 0; unmatched 1 (kept as one-sided: 0 of claude, 1 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
