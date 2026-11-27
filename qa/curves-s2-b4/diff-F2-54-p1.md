# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b4\rederived\claude\F2-54\points-p1-native.csv` (claude), `<repository>\qa\curves-s2-b4\rederived\codex\F2-54\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 205 | 202 |
| x per px | 0.0643 | 0.0643 |
| y per px | 0.0975 | 0.0993 |
| RMS residual x, y | 0.439, 0.053 | 0.434, 0.198 |

Corners of claude's box [290, 1300, 945, 3050] mapped by both calibrations (tolerance 0.94 in x, 0.35 in y):

- (92.0, 53.9) vs (91.9, 54.8)  **disagree**
- (91.6, -9.9) vs (91.6, -10.2)
- (-20.5, 55.9) vs (-20.6, 56.6)  **disagree**
- (-20.9, -7.9) vs (-20.9, -8.4)  **disagree**

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | -20 | 0.14 | 0.18 | 0.11 | 11 | 0.50 | 0.50 | agree |
| x | -10 | 0.28 | 0.24 | 0.19 | 7 | 0.66 | 0.54 | agree |
| x | 0 | 0.42 | 0.67 | 0.51 | 5 | 0.50 | 0.71 | agree |
| x | 10 | 0.12 | 0.31 | 0.35 | 10 | 0.50 | 0.52 | agree |
| x | 20 | 0.24 | 0.22 | 0.28 | 9 | 0.50 | 0.50 | agree |
| x | 30 | 0.14 | 0.30 | 0.36 | 9 | 0.50 | 0.65 | agree |
| x | 40 | 0.23 | 0.41 | 0.32 | 10 | 0.66 | 0.50 | agree |
| x | 50 | 0.20 | 0.17 | 0.15 | 9 | 0.58 | 0.50 | agree |
| x | 60 | 0.65 | 0.18 | 0.25 | 10 | 0.72 | 0.57 | agree |
| x | 70 | 0.42 | 0.18 | 0.28 | 9 | 0.62 | 0.51 | agree |
| x | 80 | 0.13 | 0.20 | 0.22 | 10 | 0.67 | 0.50 | agree |
| x | 90 | 0.17 | 0.10 | 0.09 | 9 | 0.73 | 0.50 | agree |
| y | 0 | 0.02 | 0.84 | 0.85 | 12 | 1.32 | 1.32 | agree |
| y | 2 | 0.13 | 0.22 | 0.31 | 12 | 0.77 | 0.91 | agree |
| y | 4 | 1.08 | 0.28 | 0.90 | 12 | 1.02 | 1.11 | agree |
| y | 6 | 0.38 | 0.29 | 0.20 | 11 | 0.54 | 0.50 | agree |
| y | 8 | 0.12 | 0.68 | 0.60 | 11 | 0.76 | 0.75 | agree |
| y | 10 | 0.38 | 0.24 | 0.15 | 11 | 0.50 | 0.50 | agree |
| y | 12 | 0.06 | 0.38 | 0.34 | 12 | 0.50 | 0.50 | agree |
| y | 14 | 0.56 | 0.40 | 0.16 | 10 | 0.50 | 0.50 | agree |
| y | 16 | 0.04 | 0.68 | 0.65 | 10 | 0.86 | 0.84 | agree |
| y | 18 | 0.05 | 0.13 | 0.09 | 10 | 0.50 | 0.50 | agree |
| y | 20 | 0.66 | 0.39 | 0.27 | 12 | 1.16 | 0.50 | agree |

Both maps along every verified line and every interval midline (480 places): largest difference 0.07156 in x (tolerance 0.08211, claude 60), 0.1719 in y (tolerance 0.2184, claude 4); 20 beyond the two maps' line errors.

Canonical reading: claude (same lines; 23 shared lines checked against the ink, mean of the median distances 0.34 px (claude: x 0.26, y 0.41), 0.33 px (codex: x 0.26, y 0.41), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 84; agreed 83; disagreed 1; unmatched 3 (kept as one-sided: 0 of claude, 3 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| r53958 | feature | 68/70 | 59.2, 4.3 (0.7, 0.9) | 60.4, 4.0 (0.3, 0.5) | -1.2 | +0.3 | **disagree** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
