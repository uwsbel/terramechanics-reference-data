# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b2\rederived\claude\FC-3C\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b2\rederived\codex\FC-3C\points-p2-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 18 | 18 |
| x per px | 0.1718 | 0.1718 |
| y per px | 0.3430 | 0.3430 |
| RMS residual x, y | 0.306, 0.279 | 0.312, 0.287 |

Corners of claude's box [805, 2960, 2300, 3580] mapped by both calibrations (tolerance 0.79 in x, 0.91 in y):

- (-3.3, 108.2) vs (-3.3, 108.2)
- (253.6, 104.8) vs (253.6, 104.8)
- (-4.6, -104.5) vs (-4.6, -104.5)
- (252.3, -107.9) vs (252.3, -107.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.25 | 0.15 | 0.18 | 6 | 0.50 | 0.51 | agree |
| x | 50 | 0.25 | 0.21 | 0.13 | 6 | 0.53 | 0.50 | agree |
| x | 100 | 0.15 | 0.18 | 0.23 | 6 | 0.60 | 0.50 | agree |
| x | 150 | 0.25 | 0.36 | 0.41 | 6 | 0.58 | 0.65 | agree |
| x | 200 | 0.00 | 0.23 | 0.23 | 6 | 0.55 | 0.55 | agree |
| x | 250 | 0.25 | 0.22 | 0.18 | 6 | 0.95 | 0.65 | agree |
| y | -100 | 0.17 | 0.22 | 0.20 | 15 | 0.62 | 0.53 | agree |
| y | 0 | 0.10 | 0.36 | 0.32 | 15 | 0.60 | 0.55 | agree |
| y | 100 | 0.08 | 0.17 | 0.18 | 15 | 0.53 | 0.50 | agree |

Both maps along every verified line and every interval midline (186 places): largest difference 0.05646 in x (tolerance 0.1787, between claude 0 and codex 50), 0.06547 in y (tolerance 0.404, claude -100); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.23 px (claude: x 0.22, y 0.25), 0.23 px (codex: x 0.22, y 0.23), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 64; agreed 58; disagreed 6; unmatched 0 (kept as one-sided: 0 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n2934 | marker | 1/1 | 4.6, -17.8 (0.2, 0.5) | 5.6, -18.2 (0.7, 1.5) | -1.0 | +0.4 | **disagree** |
| n3815 | marker | 12/12 | 199.9, 37.7 (0.3, 0.6) | 201.2, 37.4 (0.8, 1.6) | -1.3 | +0.4 | **disagree** |
| n4695 | marker | 5/5 | 79.2, -0.2 (0.2, 0.6) | 80.1, -0.9 (0.6, 1.3) | -0.9 | +0.7 | **disagree** |
| n4695 | marker | 11/11 | 199.8, 28.3 (0.3, 0.6) | 201.1, 27.8 (0.8, 1.6) | -1.3 | +0.5 | **disagree** |
| n734 | marker | 1/1 | -0.1, -7.6 (0.3, 0.5) | 0.3, -10.5 (0.9, 1.8) | -0.3 | +3.0 | **disagree** |
| n734 | marker | 2/2 | 30.9, 0.5 (0.2, 0.6) | 30.8, -2.0 (0.7, 1.5) | +0.1 | +2.4 | **disagree** |
