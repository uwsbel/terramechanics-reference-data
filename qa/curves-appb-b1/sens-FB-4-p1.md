# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appb-b1\rederived\claude\FB-4\points-p1-native.csv` (claude), `<repository>\qa\curves-appb-b1\rederived\codex\FB-4\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 49 | 690 |
| x per px | 0.0071 | 0.0071 |
| y per px | 0.0036 | 0.0036 |
| RMS residual x, y | 0.008, 0.005 | 0.009, 0.005 |

Corners of claude's box [560, 1060, 2610, 3950] mapped by both calibrations (tolerance 0.02 in x, 0.01 in y):

- (-0.3, 10.2) vs (-0.3, 10.2)
- (14.3, 10.2) vs (14.3, 10.2)
- (-0.2, -0.2) vs (-0.2, -0.2)
- (14.4, -0.1) vs (14.4, -0.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.06 | 0.20 | 0.20 | 23 | 0.50 | 0.77 | agree |
| x | 2 | 0.06 | 0.11 | 0.05 | 8 | 0.50 | 0.50 | agree |
| x | 4 | 0.09 | 0.18 | 0.09 | 10 | 4.39 | 0.50 | agree |
| x | 6 | 0.10 | 0.13 | 0.04 | 8 | 0.50 | 0.50 | agree |
| x | 8 | 0.19 | 0.23 | 0.12 | 8 | 0.50 | 0.50 | agree |
| x | 10 | 0.13 | 0.17 | 0.05 | 8 | 0.50 | 0.50 | agree |
| x | 12 | 0.19 | 0.39 | 0.31 | 9 | 0.52 | 0.50 | agree |
| x | 14 | 0.09 | 0.39 | 0.44 | 23 | 0.83 | 0.79 | agree |
| y | 0 | 0.08 | 0.26 | 0.33 | 23 | 0.50 | 0.59 | agree |
| y | 1 | 0.27 | 0.32 | 0.41 | 8 | 0.50 | 0.50 | agree |
| y | 2 | 0.01 | 0.11 | 0.11 | 8 | 0.50 | 0.50 | agree |
| y | 3 | 0.31 | 0.27 | 0.13 | 8 | 0.63 | 0.50 | agree |
| y | 4 | 0.03 | 0.12 | 0.09 | 8 | 0.50 | 0.50 | agree |
| y | 5 | 0.08 | 0.11 | 0.09 | 8 | 0.50 | 0.50 | agree |
| y | 6 | 0.21 | 0.07 | 0.26 | 8 | 0.50 | 0.50 | agree |
| y | 7 | 0.13 | 0.15 | 0.03 | 8 | 0.50 | 0.50 | agree |
| y | 8 | 0.18 | 0.15 | 0.19 | 8 | 0.50 | 0.50 | agree |
| y | 9 | 0.17 | 0.26 | 0.34 | 8 | 0.50 | 0.50 | agree |
| y | 10 | 0.13 | 0.45 | 0.53 | 23 | 0.80 | 1.25 | agree |

Both maps along every verified line and every interval midline (392 places): largest difference 0.005123 in x (tolerance 0.007318, codex 12), 0.003203 in y (tolerance 0.00358, claude 8); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 19 shared lines checked against the ink, mean of the median distances 0.21 px (claude: x 0.23, y 0.21), 0.20 px (codex: x 0.16, y 0.23), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

2 series in claude, 2 in codex.


## Points

Matched: 46; agreed 43; disagreed 3; unmatched 1 (kept as one-sided: 0 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| dr22 | trace | 3/interp | 2.4, 3.9 (0.0, 0.0) | 2.4, 3.8 (0.0, 0.0) | slope +0.9 | +0.1 (tol 0.1) | **disagree** |
| dr22 | trace | 4/interp | 2.6, 4.2 (0.0, 0.0) | 2.6, 4.0 (0.0, 0.0) | slope +0.9 | +0.1 (tol 0.1) | **disagree** |
| dr86 | feature | 1/1 | 2.6, 4.9 (0.0, 0.0) | 2.5, 4.8 (0.1, 0.0) | +0.1 | +0.1 | **disagree** |
