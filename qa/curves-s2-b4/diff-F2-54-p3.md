# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b4\rederived\claude\F2-54\points-p3-native.csv` (claude), `<repository>\qa\curves-s2-b4\rederived\codex\F2-54\points-p3-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 600 | 406 |
| x per px | 0.0644 | 0.0645 |
| y per px | 0.0881 | 0.0883 |
| RMS residual x, y | 0.407, 0.109 | 0.404, 0.225 |

Corners of claude's box [1385, 1300, 2450, 3050] mapped by both calibrations (tolerance 0.88 in x, 0.42 in y):

- (91.6, 83.3) vs (91.6, 83.3)
- (90.8, -10.5) vs (90.8, -10.7)
- (-21.2, 85.2) vs (-21.2, 85.2)
- (-22.0, -8.6) vs (-22.0, -8.8)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | -20 | 0.14 | 0.38 | 0.33 | 22 | 0.52 | 0.53 | agree |
| x | -10 | 0.18 | 0.32 | 0.34 | 22 | 0.51 | 0.58 | agree |
| x | 0 | 0.09 | 0.29 | 0.30 | 20 | 0.55 | 0.79 | agree |
| x | 10 | 0.09 | 0.28 | 0.29 | 23 | 0.50 | 0.61 | agree |
| x | 20 | 0.08 | 0.33 | 0.34 | 23 | 0.82 | 0.61 | agree |
| x | 30 | 0.13 | 0.39 | 0.38 | 23 | 0.63 | 0.52 | agree |
| x | 40 | 0.09 | 0.37 | 0.41 | 24 | 0.65 | 0.59 | agree |
| x | 50 | 0.28 | 0.34 | 0.30 | 22 | 0.51 | 0.69 | agree |
| x | 60 | 0.18 | 0.26 | 0.27 | 23 | 0.84 | 0.56 | agree |
| x | 70 | 0.16 | 0.35 | 0.40 | 22 | 0.79 | 0.83 | agree |
| x | 80 | 0.10 | 0.47 | 0.49 | 23 | 0.80 | 0.88 | agree |
| x | 90 | 0.17 | 0.33 | 0.35 | 24 | 0.51 | 0.67 | agree |
| y | 0 | 0.00 | 0.11 | 0.11 | 12 | 0.50 | 0.50 | agree |
| y | 2 | 0.08 | 0.13 | 0.14 | 11 | 0.50 | 0.50 | agree |
| y | 4 | 0.58 | 0.11 | 0.68 | 10 | 0.57 | 0.89 | agree |
| y | 6 | 0.10 | 0.15 | 0.07 | 10 | 0.50 | 0.50 | agree |
| y | 8 | 0.09 | 0.13 | 0.10 | 11 | 0.50 | 0.50 | agree |
| y | 10 | 0.36 | 0.25 | 0.17 | 11 | 0.50 | 0.50 | agree |
| y | 15 | 0.09 | 0.17 | 0.11 | 12 | 1.49 | 0.50 | agree |
| y | 20 | 0.15 | 0.10 | 0.22 | 11 | 0.50 | 0.50 | agree |
| y | 25 | 0.08 | 0.09 | 0.09 | 12 | 0.50 | 0.50 | agree |
| y | 30 | 0.35 | 0.25 | 0.22 | 12 | 0.50 | 0.50 | agree |
| y | 35 | 0.44 | 0.16 | 0.32 | 11 | 0.50 | 0.62 | agree |
| y | 40 | 0.22 | 0.19 | 0.18 | 11 | 0.50 | 0.50 | agree |
| y | 45 | 0.07 | 0.15 | 0.13 | 11 | 0.50 | 0.50 | agree |
| y | 50 | 0.06 | 0.35 | 0.30 | 11 | 0.50 | 0.53 | agree |
| y | 55 | 0.06 | 0.14 | 0.11 | 12 | 0.50 | 0.50 | agree |
| y | 60 | 0.34 | 0.24 | 0.19 | 11 | 0.50 | 0.50 | agree |
| y | 65 | 0.42 | 0.40 | 0.16 | 11 | 0.50 | 0.50 | agree |
| y | 70 | 0.67 | 0.48 | 0.19 | 11 | 0.50 | 0.50 | agree |
| y | 72 | 0.07 | 0.13 | 0.09 | 11 | 0.50 | 0.50 | agree |
| y | 74 | 0.60 | 0.11 | 0.55 | 11 | 0.51 | 0.63 | agree |
| y | 76 | 0.26 | 0.27 | 0.20 | 11 | 0.50 | 0.61 | agree |
| y | 78 | 0.08 | 0.34 | 0.42 | 10 | 0.50 | 0.74 | agree |
| y | 80 | 0.22 | 0.35 | 0.14 | 12 | 2.22 | 0.50 | agree |

Both maps along every verified line and every interval midline (738 places): largest difference 0.01627 in x (tolerance 0.09827, codex 50), 0.07899 in y (tolerance 0.1024, codex 74); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 35 shared lines checked against the ink, mean of the median distances 0.25 px (claude: x 0.34, y 0.21), 0.26 px (codex: x 0.35, y 0.21), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 102; agreed 102; disagreed 0; unmatched 7 (kept as one-sided: 0 of claude, 7 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
