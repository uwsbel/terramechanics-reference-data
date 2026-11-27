# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-2B\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-2B\points-p2-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 18 | 18 |
| x per px | 0.1724 | 0.1725 |
| y per px | 0.3443 | 0.3443 |
| RMS residual x, y | 0.384, 0.831 | 0.377, 0.830 |

Corners of claude's box [735, 2960, 2240, 3590] mapped by both calibrations (tolerance 0.93 in x, 2.00 in y):

- (-4.2, 107.4) vs (-4.3, 107.5)
- (255.2, 107.5) vs (255.3, 107.5)
- (-4.8, -109.5) vs (-4.8, -109.4)
- (254.7, -109.4) vs (254.7, -109.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.17 | 0.30 | 0.28 | 6 | 0.80 | 0.64 | agree |
| x | 50 | 0.45 | 0.28 | 0.23 | 6 | 0.74 | 0.50 | agree |
| x | 100 | 0.07 | 0.15 | 0.16 | 6 | 0.91 | 0.94 | agree |
| x | 150 | 0.18 | 0.28 | 0.27 | 6 | 0.62 | 0.68 | agree |
| x | 200 | 0.07 | 0.23 | 0.26 | 6 | 0.61 | 0.52 | agree |
| x | 250 | 0.30 | 0.25 | 0.52 | 6 | 0.51 | 0.83 | agree |
| y | -100 | 0.21 | 0.31 | 0.38 | 15 | 0.89 | 0.78 | agree |
| y | 0 | 0.43 | 0.88 | 0.86 | 15 | 1.71 | 1.29 | agree |
| y | 100 | 0.12 | 0.67 | 0.71 | 15 | 0.83 | 0.90 | agree |

Both maps along every verified line and every interval midline (206 places): largest difference 0.07861 in x (tolerance 0.2519, claude 50), 0.1729 in y (tolerance 1.028, claude 0); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.37 px (claude: x 0.25, y 0.62), 0.41 px (codex: x 0.29, y 0.65), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

6 series in claude, 6 in codex.


## Points

Matched: 125; agreed 106; disagreed 19; unmatched 7 (kept as one-sided: 0 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1468 | marker | 2/2 | 18.7, -5.7 (0.4, 1.3) | 18.5, -2.9 (0.7, 1.4) | +0.2 | -2.8 | **disagree** |
| n1468 | marker | 3/3 | 29.1, -6.7 (0.4, 1.3) | 28.9, -3.9 (0.7, 1.4) | +0.2 | -2.8 | **disagree** |
| n1468 | marker | 4/4 | 38.7, -7.4 (0.4, 1.3) | 38.5, -4.2 (0.7, 1.4) | +0.2 | -3.1 | **disagree** |
| n1468 | marker | 5/5 | 48.8, -7.0 (0.4, 1.3) | 48.4, -4.2 (0.7, 1.4) | +0.4 | -2.8 | **disagree** |
| n1468 | marker | 6/6 | 59.4, -7.7 (0.4, 1.3) | 58.7, -3.9 (0.7, 1.4) | +0.7 | -3.8 | **disagree** |
| n1468 | marker | 7/7 | 69.4, -7.3 (0.4, 1.3) | 68.5, -3.8 (0.7, 1.4) | +0.9 | -3.5 | **disagree** |
| n1468 | marker | 9/9 | 89.0, -6.2 (0.4, 1.1) | 88.5, -3.5 (0.7, 1.4) | +0.5 | -2.8 | **disagree** |
| n1468 | marker | 10/10 | 99.0, -3.2 (0.4, 1.3) | 98.7, -7.5 (0.7, 1.4) | +0.4 | +4.4 | **disagree** |
| n1468 | marker | -/14 | (none) | 139.1, -0.0 | | | unmatched in claude |
| n2200 | marker | 19/19 | 198.5, 0.5 (0.4, 1.3) | 198.8, -3.7 (0.7, 1.6) | -0.3 | +4.2 | **disagree** |
| n2200 | marker | 20/20 | 209.2, 3.3 (0.4, 1.0) | 209.1, -0.3 (0.7, 1.6) | +0.2 | +3.6 | **disagree** |
| n2200 | marker | 21/21 | 219.0, 3.7 (0.4, 1.0) | 218.7, -0.3 (0.7, 1.6) | +0.3 | +3.9 | **disagree** |
| n2200 | marker | 22/22 | 229.1, 4.0 (0.4, 1.0) | 228.8, 0.4 (0.7, 1.6) | +0.3 | +3.6 | **disagree** |
| n2995 | marker | 5/5 | 59.4, -16.1 (0.4, 1.1) | 58.7, -12.3 (0.7, 1.6) | +0.7 | -3.8 | **disagree** |
| n2995 | marker | 6/6 | 69.4, -15.1 (0.4, 1.1) | 68.5, -12.0 (0.8, 1.6) | +0.9 | -3.1 | **disagree** |
| n2995 | marker | 22/22 | 229.1, -3.9 (0.3, 0.8) | 228.7, -6.4 (0.7, 1.6) | +0.3 | +2.5 | **disagree** |
| n3660 | marker | 10/16 | 169.0, -16.9 (0.4, 1.1) | 169.2, -14.2 (0.7, 1.6) | -0.2 | -2.7 | **disagree** |
| n3660 | marker | -/1 | (none) | 18.5, -12.4 | | | unmatched in claude |
| n3660 | marker | -/2 | (none) | 28.8, -13.4 | | | unmatched in claude |
| n3660 | marker | -/3 | (none) | 38.5, -14.0 | | | unmatched in claude |
| n3660 | marker | -/4 | (none) | 48.3, -15.7 | | | unmatched in claude |
| n3660 | marker | -/5 | (none) | 58.7, -15.0 | | | unmatched in claude |
| n3660 | marker | -/6 | (none) | 68.5, -16.0 | | | unmatched in claude |
| n4400 | marker | 22/22 | 229.4, -19.5 (0.3, 0.8) | 228.7, -22.3 (0.7, 1.6) | +0.7 | +2.8 | **disagree** |
| n4400 | marker | 23/23 | 238.6, -19.8 (0.3, 0.8) | 238.6, -23.3 (0.8, 1.6) | -0.0 | +3.5 | **disagree** |
| n4400 | marker | 24/24 | 248.7, -19.5 (0.5, 0.9) | 248.2, -23.6 (0.8, 1.6) | +0.5 | +4.2 | **disagree** |
| n3660 | marker | 1 (codex) | 18.5, -12.4 | claude: n2995 (square) | | | **identity conflict** |
| n3660 | marker | 2 (codex) | 28.8, -13.4 | claude: n2995 (square), n4400 (asterisk) | | | **identity conflict** |
| n3660 | marker | 3 (codex) | 38.5, -14.0 | claude: n2200 (triangle-up), n2995 (square) | | | **identity conflict** |
| n3660 | marker | 4 (codex) | 48.3, -15.7 | claude: n2995 (square), n4400 (asterisk) | | | **identity conflict** |
| n3660 | marker | 5 (codex) | 58.7, -15.0 | claude: n2200 (triangle-up), n2995 (square) | | | **identity conflict** |
| n3660 | marker | 6 (codex) | 68.5, -16.0 | claude: n2995 (square) | | | **identity conflict** |
