# Curve diff: claude vs codex

Files: `<repository>\qa\curves-pilot-b1\rederived\claude\FC-1B\points-p2-native.csv` (claude), `<repository>\qa\curves-pilot-b1\rederived\codex\FC-1B\points-p2-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 18 | 18 |
| x per px | 0.1691 | 0.1697 |
| y per px | 0.3499 | 0.3502 |
| RMS residual x, y | 0.366, 0.356 | 0.269, 0.375 |

Corners of claude's box [780, 2960, 2300, 3600] mapped by both calibrations (tolerance 0.80 in x, 1.08 in y):

- (-3.5, 111.9) vs (-3.6, 112.0)
- (253.5, 102.6) vs (254.3, 102.7)
- (-5.2, -112.0) vs (-5.8, -112.0)
- (251.8, -121.3) vs (252.0, -121.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 1.05 | 0.36 | 0.61 | 6 | 0.85 | 1.55 | agree |
| x | 50 | 1.02 | 0.21 | 0.40 | 19 | 0.57 | 0.87 | agree |
| x | 100 | 0.17 | 0.39 | 0.45 | 6 | 1.87 | 1.82 | agree |
| x | 150 | 0.27 | 0.53 | 0.73 | 6 | 1.07 | 1.25 | agree |
| x | 200 | 0.47 | 0.15 | 0.37 | 6 | 0.50 | 0.58 | agree |
| x | 250 | 0.70 | 0.30 | 0.30 | 21 | 0.72 | 0.59 | agree |
| y | -100 | 0.14 | 0.34 | 0.25 | 15 | 0.79 | 0.76 | agree |
| y | 0 | 0.26 | 0.30 | 0.32 | 15 | 0.63 | 0.85 | agree |
| y | 100 | 0.48 | 0.25 | 0.32 | 15 | 0.52 | 1.00 | agree |

Both maps along every verified line and every interval midline (183 places): largest difference 0.1779 in x (tolerance 0.4021, codex 0), 0.1501 in y (tolerance 0.5756, claude 100); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.31 px (claude: x 0.32, y 0.30), 0.42 px (codex: x 0.48, y 0.30), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

7 series in claude, 7 in codex.


## Points

Matched: 92; agreed 91; disagreed 1; unmatched 1 (kept as one-sided: 0 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1172 | marker | 6/6 | 110.8, 18.5 (0.4, 0.6) | 111.0, 16.2 (0.4, 0.7) | -0.2 | +2.3 | **disagree** |
| n1760 | marker | -/1 | (none) | -4.3, -5.1 | | | unmatched in claude |
