# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-1D\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-1D\points-p2-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 18 | 18 |
| x per px | 0.1707 | 0.1708 |
| y per px | 0.3507 | 0.3508 |
| RMS residual x, y | 0.353, 0.438 | 0.298, 0.529 |

Corners of claude's box [530, 2990, 2110, 3665] mapped by both calibrations (tolerance 0.82 in x, 1.32 in y):

- (-10.4, 124.3) vs (-10.3, 124.3)
- (259.3, 114.6) vs (259.5, 114.6)
- (-12.7, -112.4) vs (-12.9, -112.4)
- (257.0, -122.0) vs (256.9, -122.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.25 | 0.51 | 0.38 | 6 | 1.33 | 1.07 | agree |
| x | 50 | 0.17 | 0.44 | 0.35 | 6 | 0.99 | 0.79 | agree |
| x | 100 | 0.28 | 0.26 | 0.09 | 6 | 0.50 | 0.50 | agree |
| x | 150 | 0.36 | 0.48 | 0.36 | 6 | 0.68 | 0.83 | agree |
| x | 200 | 0.43 | 0.42 | 0.36 | 6 | 0.98 | 1.23 | agree |
| x | 250 | 0.34 | 0.25 | 0.39 | 21 | 0.51 | 1.46 | agree |
| y | -100 | 0.23 | 0.32 | 0.31 | 15 | 0.72 | 0.50 | agree |
| y | 0 | 1.15 | 0.28 | 0.52 | 15 | 0.54 | 1.82 | agree |
| y | 100 | 0.36 | 0.32 | 0.25 | 15 | 0.67 | 0.50 | agree |

Both maps along every verified line and every interval midline (182 places): largest difference 0.07843 in x (tolerance 0.4226, claude 250), 0.3536 in y (tolerance 0.8693, codex 0); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.36 px (claude: x 0.39, y 0.31), 0.33 px (codex: x 0.32, y 0.36), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

7 series in claude, 7 in codex.


## Points

Matched: 78; agreed 67; disagreed 11; unmatched 5 (kept as one-sided: 1 of claude, 2 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n0 | marker | 1/1 | 19.5, 16.7 (0.3, 0.5) | 18.3, 17.3 (0.3, 0.8) | +1.2 | -0.6 | **disagree** |
| n0 | marker | 2/2 | 40.3, 38.1 (0.3, 0.5) | 39.1, 38.5 (0.3, 0.8) | +1.2 | -0.4 | **disagree** |
| n0 | marker | 3/3 | 60.7, 61.2 (0.2, 0.5) | 59.5, 61.8 (0.3, 0.7) | +1.2 | -0.6 | **disagree** |
| n0 | marker | 4/4 | 69.0, 74.0 (0.2, 0.5) | 67.8, 74.6 (0.3, 0.7) | +1.2 | -0.6 | **disagree** |
| n0 | marker | 5/5 | 89.6, 94.3 (0.2, 0.5) | 88.3, 94.7 (0.3, 0.6) | +1.3 | -0.4 | **disagree** |
| n0 | marker | 6/6 | 109.7, 115.0 (0.2, 0.5) | 108.3, 115.6 (0.3, 0.7) | +1.4 | -0.6 | **disagree** |
| n0 | marker | 7/7 | 130.5, 131.3 (0.2, 0.5) | 129.1, 131.9 (0.3, 0.8) | +1.4 | -0.7 | **disagree** |
| n1468 | marker | -/2 | (none) | 8.9, -9.1 | | | unmatched in claude |
| n2935 | marker | 9/- | 179.7, 46.8 | (none) | | | unmatched in codex |
| n2935 | marker | 8/10 | 149.6, 38.5 (0.4, 0.6) | 149.9, 25.8 (0.5, 1.2) | -0.2 | +12.7 | **disagree** |
| n2935 | marker | -/1 | (none) | -0.5, -25.8 | | | unmatched in claude |
| n2935 | marker | -/5 | (none) | 49.8, -6.1 | | | unmatched in claude |
| n2935 | marker | -/11 | (none) | 169.4, 47.8 | | | unmatched in claude |
| n3520 | marker | 4/4 | 50.2, -4.7 (0.4, 0.6) | 50.0, -7.5 (0.7, 1.5) | +0.2 | +2.8 | **disagree** |
| n3520 | marker | 8/8 | 130.1, 18.5 (0.2, 0.5) | 129.4, 17.7 (0.4, 1.0) | +0.7 | +0.8 | **disagree** |
| n3520 | marker | 12/12 | 220.2, 45.7 (0.2, 0.5) | 219.6, 44.1 (0.5, 0.9) | +0.6 | +1.6 | **disagree** |
| n1468 | marker | 2 (codex) | 8.9, -9.1 | claude: n587 (triangle-up) | | | **identity conflict** |
| n2935 | marker | 5 (codex) | 49.8, -6.1 | claude: n3520 (x) | | | **identity conflict** |
