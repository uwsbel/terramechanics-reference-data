# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b2\rederived\claude\FC-3B\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b2\rederived\codex\FC-3B\points-p2-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 30 | 12 |
| x per px | 0.1712 | 0.1712 |
| y per px | 0.3431 | 0.3436 |
| RMS residual x, y | 0.277, 0.040 | 0.288, 0.159 |

Corners of claude's box [660, 2850, 2170, 3485] mapped by both calibrations (tolerance 0.74 in x, 0.54 in y):

- (-4.4, 57.4) vs (-4.4, 57.6)
- (254.1, 60.0) vs (254.2, 59.9)
- (-4.3, -160.5) vs (-4.4, -160.6)
- (254.2, -157.9) vs (254.2, -158.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.45 | 0.30 | 0.48 | 12 | 0.84 | 1.52 | agree |
| x | 50 | 0.02 | 0.18 | 0.17 | 12 | 0.66 | 0.52 | agree |
| x | 100 | 0.45 | 0.19 | 0.05 | 12 | 0.52 | 0.50 | agree |
| x | 150 | 0.27 | 0.32 | 0.42 | 12 | 0.62 | 1.09 | agree |
| x | 200 | 0.29 | 0.25 | 0.10 | 12 | 0.52 | 1.12 | agree |
| x | 250 | 0.56 | 0.34 | 0.13 | 21 | 0.88 | 1.02 | agree |
| y | -150 | 1.77 | 0.32 | 0.81 | 15 | 0.50 | 2.22 | agree |
| y | 0 | 0.19 | 0.38 | 0.40 | 23 | 0.82 | 0.60 | agree |
| y | 50 | 0.11 | 0.14 | 0.22 | 15 | 0.50 | 0.50 | agree |

Both maps along every verified line and every interval midline (228 places): largest difference 0.1047 in x (tolerance 0.3435, claude 250), 0.6631 in y (tolerance 1.046, claude -150); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.27 px (claude: x 0.26, y 0.28), 0.31 px (codex: x 0.23, y 0.48), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 64; agreed 62; disagreed 2; unmatched 0 (kept as one-sided: 0 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n4695 | marker | 5/5 | 79.2, -127.4 (0.3, 0.6) | 79.0, -129.2 (0.2, 0.7) | +0.2 | +1.8 | **disagree** |
| n4695 | marker | 7/7 | 120.0, -132.5 (0.2, 0.4) | 119.5, -133.4 (0.2, 0.7) | +0.6 | +0.9 | **disagree** |
