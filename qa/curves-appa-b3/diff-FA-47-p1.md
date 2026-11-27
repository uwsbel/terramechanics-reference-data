# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b3\rederived\claude\FA-47\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b3\rederived\codex\FA-47\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 671 | 143 |
| x per px | 0.0007 | 0.0007 |
| y per px | 0.0000 | 0.0000 |
| RMS residual x, y | 0.001, 0.000 | 0.001, 0.000 |

Corners of claude's box [840, 1030, 2290, 3700] mapped by both calibrations (tolerance 0.00 in x, 0.00 in y (in the plotting coordinates of linear x, reciprocal y)):

- (-0.0, 54.4) vs (-0.0, 54.5)
- (1.0, 54.8) vs (1.0, 54.8)
- (-0.1, 115.9) vs (-0.1, 115.8)
- (1.0, 117.5) vs (1.0, 117.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 1 | | | | | | | claude's line not a knot: misplaced: 2.40 px from the ink's line at an end of the line |
| x | 0 | 0.21 | 0.37 | 0.35 | 25 | 0.81 | 0.55 | agree |
| x | 0.1 | 0.18 | 0.31 | 0.24 | 25 | 0.61 | 0.50 | agree |
| x | 0.2 | 0.63 | 0.29 | 0.28 | 25 | 1.04 | 0.50 | agree |
| x | 0.3 | 0.40 | 0.45 | 0.35 | 25 | 1.07 | 0.59 | agree |
| x | 0.4 | 0.66 | 0.36 | 0.24 | 25 | 0.97 | 0.53 | agree |
| x | 0.5 | 0.17 | 0.25 | 0.20 | 25 | 0.84 | 0.71 | agree |
| x | 0.6 | 0.38 | 0.42 | 0.37 | 25 | 0.96 | 0.66 | agree |
| x | 0.7 | 0.28 | 0.47 | 0.38 | 25 | 0.79 | 0.56 | agree |
| x | 0.8 | 0.28 | 0.29 | 0.25 | 25 | 0.80 | 0.62 | agree |
| x | 0.9 | 0.55 | 0.40 | 0.15 | 25 | 0.95 | 0.50 | agree |
| x | 1 | | | | | | 0.63 | only in codex |
| y | 55 | 0.70 | 0.46 | 0.22 | 25 | 1.16 | 0.63 | agree |
| y | 60 | 0.47 | 0.35 | 0.29 | 25 | 0.86 | 0.57 | agree |
| y | 65 | 0.66 | 0.29 | 0.35 | 25 | 0.92 | 0.59 | agree |
| y | 70 | 0.38 | 0.38 | 0.37 | 25 | 0.85 | 0.57 | agree |
| y | 75 | 0.49 | 0.34 | 0.35 | 25 | 0.60 | 0.67 | agree |
| y | 80 | 0.35 | 0.35 | 0.22 | 25 | 0.78 | 0.77 | agree |
| y | 85 | 0.17 | 0.32 | 0.32 | 25 | 0.93 | 0.75 | agree |
| y | 90 | 0.44 | 0.34 | 0.31 | 25 | 0.70 | 0.57 | agree |
| y | 95 | 0.19 | 0.18 | 0.24 | 25 | 0.50 | 0.50 | agree |
| y | 100 | 0.16 | 0.28 | 0.23 | 25 | 0.50 | 0.50 | agree |
| y | 105 | 0.15 | 0.24 | 0.22 | 25 | 0.50 | 0.50 | agree |
| y | 110 | 0.22 | 0.28 | 0.24 | 25 | 0.62 | 0.50 | agree |
| y | 115 | 0.55 | 0.29 | 0.18 | 16 | 0.56 | 0.50 | agree |
| y | 56 | | | | | 1.09 | | only in claude |
| y | 57 | | | | | 1.37 | | only in claude |
| y | 58 | | | | | 0.64 | | only in claude |
| y | 59 | | | | | 0.56 | | only in claude |
| y | 61 | | | | | 0.85 | | only in claude |
| y | 62 | | | | | 0.56 | | only in claude |
| y | 63 | | | | | 0.57 | | only in claude |
| y | 64 | | | | | 0.61 | | only in claude |
| y | 66 | | | | | 0.77 | | only in claude |
| y | 67 | | | | | 1.11 | | only in claude |
| y | 68 | | | | | 1.13 | | only in claude |
| y | 69 | | | | | 0.83 | | only in claude |
| y | 71 | | | | | 0.65 | | only in claude |
| y | 72 | | | | | 0.87 | | only in claude |
| y | 73 | | | | | 0.91 | | only in claude |
| y | 74 | | | | | 0.60 | | only in claude |
| y | 76 | | | | | 0.80 | | only in claude |
| y | 77 | | | | | 0.98 | | only in claude |
| y | 78 | | | | | 0.50 | | only in claude |
| y | 79 | | | | | 0.90 | | only in claude |
| y | 81 | | | | | 0.61 | | only in claude |
| y | 82 | | | | | 0.63 | | only in claude |
| y | 83 | | | | | 0.70 | | only in claude |
| y | 84 | | | | | 0.72 | | only in claude |
| y | 86 | | | | | 1.04 | | only in claude |
| y | 87 | | | | | 1.43 | | only in claude |
| y | 88 | | | | | 1.18 | | only in claude |
| y | 89 | | | | | 0.83 | | only in claude |
| y | 91 | | | | | 0.89 | | only in claude |
| y | 92 | | | | | 0.50 | | only in claude |
| y | 93 | | | | | 0.50 | | only in claude |
| y | 94 | | | | | 0.84 | | only in claude |
| y | 96 | | | | | 0.56 | | only in claude |
| y | 97 | | | | | 0.73 | | only in claude |
| y | 98 | | | | | 0.87 | | only in claude |
| y | 99 | | | | | 0.78 | | only in claude |
| y | 101 | | | | | 0.75 | | only in claude |
| y | 102 | | | | | 0.61 | | only in claude |
| y | 103 | | | | | 0.86 | | only in claude |
| y | 107 | | | | | 0.63 | | only in claude |
| y | 108 | | | | | 0.57 | | only in claude |
| y | 109 | | | | | 0.86 | | only in claude |

(In the plotting coordinates: linear x, reciprocal y.) Both maps along every verified line and every interval midline (892 places): largest difference 0.001781 in x (tolerance 0.001127, codex 1), 2.365e-05 in y (tolerance 6.141e-06, claude 56); 217 beyond the two maps' line errors.

Canonical reading: claude (**coverage cannot be ranked** (lines claude: x [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], y [55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0, 100.0, 101.0, 102.0, 103.0, 105.0, 107.0, 108.0, 109.0, 110.0, 115.0]; codex: x [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], y [55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0, 115.0]): recover the missing lines or name the canonical reading in overlays.csv; meanwhile first submission by the ink; 23 shared lines checked against the ink, mean of the median distances 0.34 px (claude: x 0.36, y 0.32), 0.28 px (codex: x 0.28, y 0.27)); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 39; agreed 39; disagreed 0; unmatched 7 (kept as one-sided: 3 of claude, 4 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| mean | trace | 11/- | 1.0, 89.5 (0.0, 0.1) | (no trace at this x) | | | unmatched in codex |
| upper | trace | 2/- | 0.1, 74.9 (0.0, 0.1) | (no trace at this x) | | | unmatched in codex |
| upper | trace | 3/- | 0.2, 76.4 (0.0, 0.1) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
