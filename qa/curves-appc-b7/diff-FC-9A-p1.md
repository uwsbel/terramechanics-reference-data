# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b7\rederived\claude\FC-9A\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b7\rederived\codex\FC-9A\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4374 | 3.4374 |
| y per px | 3.4238 | 3.4240 |
| RMS residual x, y | 3.746, 10.363 | 3.627, 10.222 |

Corners of claude's box [630, 1395, 2715, 3775] mapped by both calibrations (tolerance 10.81 in x, 24.01 in y):

- (-54.8, 8049.6) vs (-54.2, 8049.7)
- (7112.3, 8067.5) vs (7112.8, 8068.1)
- (-76.1, -99.0) vs (-76.4, -99.5)
- (7090.9, -81.0) vs (7090.6, -81.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.27 | 0.42 | 0.49 | 24 | 0.77 | 0.81 | agree |
| x | 1000 | 0.07 | 0.18 | 0.18 | 24 | 0.59 | 0.51 | agree |
| x | 2000 | 0.07 | 0.55 | 0.53 | 24 | 0.81 | 0.86 | agree |
| x | 3000 | 0.10 | 0.26 | 0.26 | 24 | 0.71 | 0.80 | agree |
| x | 4000 | 0.20 | 0.39 | 0.36 | 24 | 0.84 | 0.75 | agree |
| x | 5000 | 0.45 | 0.41 | 0.39 | 22 | 0.83 | 0.70 | agree |
| x | 6000 | 0.32 | 0.38 | 0.41 | 24 | 0.68 | 0.67 | agree |
| x | 7000 | 0.33 | 0.25 | 0.23 | 24 | 0.50 | 0.52 | agree |
| y | 0 | 0.17 | 0.44 | 0.48 | 21 | 0.76 | 0.68 | agree |
| y | 1000 | 0.17 | 0.60 | 0.55 | 21 | 1.03 | 0.99 | agree |
| y | 2000 | 0.19 | 0.17 | 0.18 | 21 | 0.50 | 0.60 | agree |
| y | 3000 | 0.08 | 0.44 | 0.37 | 21 | 0.70 | 0.69 | agree |
| y | 4000 | 0.36 | 0.37 | 0.42 | 19 | 0.81 | 0.70 | agree |
| y | 5000 | 0.17 | 0.27 | 0.30 | 21 | 0.72 | 0.60 | agree |
| y | 6000 | 0.16 | 0.46 | 0.33 | 21 | 0.80 | 0.65 | agree |
| y | 7000 | 0.09 | 0.37 | 0.29 | 21 | 0.85 | 0.79 | agree |
| y | 8000 | 0.89 | 0.50 | 0.64 | 21 | 1.07 | 1.40 | agree |

Both maps along every verified line and every interval midline (378 places): largest difference 1.283 in x (tolerance 5.26, claude 5000), 2.682 in y (tolerance 8.34, claude 8000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.38 px (claude: x 0.35, y 0.40), 0.38 px (codex: x 0.36, y 0.40), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 16; agreed 16; disagreed 0; unmatched 2 (kept as one-sided: 0 of claude, 2 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
