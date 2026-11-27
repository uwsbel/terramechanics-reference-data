# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b6\rederived\claude\FC-7A\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b6\rederived\codex\FC-7A\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 56 | 56 |
| x per px | 0.0160 | 0.0160 |
| y per px | 0.0160 | 0.0160 |
| RMS residual x, y | 0.022, 0.030 | 0.026, 0.031 |

Corners of claude's box [600, 920, 2600, 3200] mapped by both calibrations (tolerance 0.06 in x, 0.08 in y):

- (-0.7, 35.8) vs (-0.7, 35.8)
- (31.3, 35.5) vs (31.3, 35.5)
- (-1.1, -0.6) vs (-1.1, -0.6)
- (30.9, -0.9) vs (30.9, -0.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.51 | 0.42 | 0.45 | 21 | 1.07 | 1.50 | agree |
| x | 5 | 0.95 | 0.56 | 0.70 | 20 | 1.26 | 1.88 | agree |
| x | 10 | 0.32 | 0.22 | 0.26 | 19 | 0.73 | 1.08 | agree |
| x | 15 | 0.87 | 0.42 | 0.49 | 19 | 0.67 | 1.46 | agree |
| x | 20 | 0.29 | 0.48 | 0.41 | 21 | 1.00 | 0.70 | agree |
| x | 25 | 0.11 | 0.33 | 0.30 | 21 | 0.76 | 0.78 | agree |
| x | 30 | 0.29 | 0.45 | 0.35 | 21 | 0.99 | 0.70 | agree |
| y | 0 | 0.32 | 0.35 | 0.28 | 17 | 0.50 | 0.59 | agree |
| y | 5 | 0.07 | 0.46 | 0.45 | 18 | 0.85 | 0.97 | agree |
| y | 10 | 0.37 | 0.38 | 0.48 | 18 | 1.13 | 0.84 | agree |
| y | 15 | 0.10 | 0.41 | 0.36 | 18 | 0.77 | 0.67 | agree |
| y | 20 | 0.30 | 0.50 | 0.28 | 18 | 0.80 | 0.63 | agree |
| y | 25 | 0.39 | 0.24 | 0.39 | 18 | 0.86 | 1.25 | agree |
| y | 30 | 1.31 | 1.30 | 0.69 | 15 | 2.46 | 1.92 | agree; claude off the ink |
| y | 35 | 0.21 | 0.51 | 0.42 | 14 | 1.52 | 1.51 | agree |

Both maps along every verified line and every interval midline (304 places): largest difference 0.01391 in x (tolerance 0.04981, codex 5), 0.0177 in y (tolerance 0.07034, codex 30); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 15 shared lines checked against the ink, mean of the median distances 0.47 px (claude: x 0.41, y 0.52), 0.42 px (codex: x 0.42, y 0.42), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

2 series in claude, 2 in codex.


## Points

Matched: 45; agreed 44; disagreed 1; unmatched 4 (kept as one-sided: 1 of claude, 3 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| dr100 | trace | 15/- | 26.7, 35.0 (0.1, 0.1) | (no trace at this x) | | | unmatched in codex |
| dr53 | marker | 6/6 | 26.4, 27.8 (0.0, 0.0) | 26.4, 27.7 (0.0, 0.0) | -0.0 | +0.1 | **disagree** |
