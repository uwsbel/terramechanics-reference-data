# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-2C\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-2C\points-p2-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 18 | 18 |
| x per px | 0.1715 | 0.1715 |
| y per px | 0.3471 | 0.3471 |
| RMS residual x, y | 0.344, 0.623 | 0.366, 0.637 |

Corners of claude's box [670, 2935, 2175, 3550] mapped by both calibrations (tolerance 0.88 in x, 1.61 in y):

- (-3.6, 105.4) vs (-3.5, 105.3)
- (254.5, 107.9) vs (254.5, 108.0)
- (-3.5, -108.1) vs (-3.5, -108.1)
- (254.6, -105.5) vs (254.6, -105.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.13 | 0.33 | 0.27 | 6 | 0.67 | 0.59 | agree |
| x | 50 | 0.24 | 0.44 | 0.26 | 6 | 0.81 | 0.58 | agree |
| x | 100 | 1.10 | 0.85 | 0.12 | 6 | 1.33 | 0.50 | agree |
| x | 150 | 0.23 | 0.18 | 0.06 | 6 | 0.50 | 0.50 | agree |
| x | 200 | 0.15 | 0.09 | 0.12 | 6 | 0.50 | 0.50 | agree |
| x | 250 | 0.36 | 0.30 | 0.16 | 6 | 0.85 | 0.50 | agree |
| y | -100 | 0.23 | 0.22 | 0.23 | 15 | 0.50 | 0.50 | agree |
| y | 0 | 0.26 | 0.21 | 0.30 | 15 | 0.62 | 0.69 | agree |
| y | 100 | 0.18 | 0.34 | 0.32 | 15 | 0.50 | 0.62 | agree |

Both maps along every verified line and every interval midline (230 places): largest difference 0.2058 in x (tolerance 0.3271, codex 100), 0.09798 in y (tolerance 0.4585, codex 0); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.33 px (claude: x 0.36, y 0.26), 0.20 px (codex: x 0.16, y 0.28), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

6 series in claude, 6 in codex.


## Points

Matched: 42; agreed 18; disagreed 24; unmatched 16 (kept as one-sided: 3 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1468 | marker | 4/- | 70.8, 17.5 | (none) | | | unmatched in codex |
| n1468 | marker | 6/- | 90.8, 17.4 | (none) | | | unmatched in codex |
| n1468 | marker | 7/- | 100.8, 19.9 | (none) | | | unmatched in codex |
| n1468 | marker | 8/- | 110.5, 22.7 | (none) | | | unmatched in codex |
| n1468 | marker | 9/- | 110.5, 18.6 | (none) | | | unmatched in codex |
| n1468 | marker | 10/- | 120.5, 22.2 | (none) | | | unmatched in codex |
| n1468 | marker | 11/- | 130.1, 29.4 | (none) | | | unmatched in codex |
| n1468 | marker | 5/4 | 79.6, 29.3 (0.3, 0.4) | 79.9, 31.0 (0.2, 0.5) | -0.4 | -1.7 | **disagree** |
| n2200 | marker | 5/5 | 60.5, 8.2 (0.2, 0.4) | 61.1, 8.6 (0.2, 0.5) | -0.6 | -0.4 | **disagree** |
| n2200 | marker | 6/6 | 70.9, 5.2 (0.3, 0.6) | 71.4, 10.7 (0.7, 1.5) | -0.4 | -5.5 | **disagree** |
| n2200 | marker | -/8 | (none) | 92.1, 18.8 | | | unmatched in claude |
| n2200 | marker | -/9 | (none) | 101.3, 22.0 | | | unmatched in claude |
| n2200 | marker | -/10 | (none) | 111.4, 24.8 | | | unmatched in claude |
| n2200 | marker | -/12 | (none) | 130.3, 31.5 | | | unmatched in claude |
| n2995 | marker | 10/- | 130.1, 25.0 | (none) | | | unmatched in codex |
| n2995 | marker | 2/2 | 8.1, 8.4 (0.3, 0.6) | 7.7, 10.1 (0.6, 1.1) | +0.3 | -1.8 | **disagree** |
| n2995 | marker | 5/5 | 60.6, 16.2 (0.2, 0.4) | 60.9, 18.5 (0.2, 0.5) | -0.3 | -2.3 | **disagree** |
| n2995 | marker | 6/6 | 70.8, 11.7 (0.3, 0.6) | 71.2, 19.3 (0.6, 1.3) | -0.4 | -7.6 | **disagree** |
| n2995 | marker | 7/7 | 80.7, 21.8 (0.4, 0.6) | 82.2, 23.9 (0.6, 1.3) | -1.5 | -2.1 | **disagree** |
| n2995 | marker | 8/8 | 90.7, 26.5 (0.3, 0.4) | 91.2, 27.7 (0.2, 0.5) | -0.6 | -1.2 | **disagree** |
| n2995 | marker | 9/9 | 100.8, 28.5 (0.4, 0.6) | 100.0, 30.5 (0.6, 1.3) | +0.9 | -2.1 | **disagree** |
| n3660 | marker | 1/2 | 90.9, 12.3 (0.4, 0.8) | 92.4, 16.1 (0.7, 1.5) | -1.5 | -3.8 | **disagree** |
| n3660 | marker | 3/4 | 110.5, 14.2 (0.4, 0.8) | 111.4, 15.6 (0.2, 0.5) | -1.0 | -1.4 | **disagree** |
| n3660 | marker | 4/5 | 120.3, 17.7 (0.4, 0.8) | 121.1, 20.5 (0.6, 1.3) | -0.8 | -2.8 | **disagree** |
| n3660 | marker | 6/7 | 140.5, 24.4 (0.2, 0.4) | 141.8, 26.8 (0.2, 0.5) | -1.3 | -2.4 | **disagree** |
| n3660 | marker | 7/8 | 150.1, 27.2 (0.3, 0.6) | 151.1, 28.6 (0.6, 1.3) | -1.0 | -1.4 | **disagree** |
| n3660 | marker | 8/9 | 159.8, 26.6 (0.2, 0.4) | 160.6, 28.0 (0.2, 0.5) | -0.8 | -1.4 | **disagree** |
| n3660 | marker | -/1 | (none) | 82.0, 19.4 | | | unmatched in claude |
| n4400 | marker | 1/1 | 80.8, 6.2 (0.3, 0.4) | 81.6, 7.8 (0.2, 0.5) | -0.8 | -1.6 | **disagree** |
| n4400 | marker | 2/2 | 91.1, 5.2 (0.3, 0.4) | 91.9, 5.8 (0.2, 0.5) | -0.8 | -0.6 | **disagree** |
| n4400 | marker | 4/4 | 110.7, 8.7 (0.3, 0.4) | 111.6, 9.4 (0.2, 0.5) | -0.9 | -0.7 | **disagree** |
| n4400 | marker | 5/5 | 120.8, 10.8 (0.3, 0.4) | 121.2, 9.9 (0.2, 0.5) | -0.4 | +1.0 | **disagree** |
| n4400 | marker | 6/6 | 130.2, 14.0 (0.2, 0.4) | 130.7, 15.8 (0.2, 0.5) | -0.5 | -1.7 | **disagree** |
| n4400 | marker | 7/7 | 140.4, 15.2 (0.2, 0.4) | 141.8, 15.9 (0.2, 0.5) | -1.5 | -0.7 | **disagree** |
| n4400 | marker | 8/8 | 149.6, 16.6 (0.3, 0.6) | 150.8, 18.7 (0.6, 1.1) | -1.2 | -2.1 | **disagree** |
| n4400 | marker | 9/9 | 159.8, 18.4 (0.2, 0.4) | 160.6, 19.8 (0.2, 0.5) | -0.8 | -1.4 | **disagree** |
| n4400 | marker | 10/10 | 170.1, 21.4 (0.2, 0.4) | 170.7, 23.0 (0.2, 0.5) | -0.6 | -1.6 | **disagree** |
| n734 | marker | 1/- | 5.1, 3.9 | (none) | | | unmatched in codex |
| n734 | marker | 2/- | 10.0, 6.3 | (none) | | | unmatched in codex |
| n734 | marker | 5/- | 50.1, 22.1 | (none) | | | unmatched in codex |
| n1468 | marker | 4 (claude) | 70.8, 17.5 | codex: n2995 (square) | | | **identity conflict** |
| n1468 | marker | 6 (claude) | 90.8, 17.4 | codex: n3660 (x), n2200 (triangle-up) | | | **identity conflict** |
| n1468 | marker | 7 (claude) | 100.8, 19.9 | codex: n2200 (triangle-up) | | | **identity conflict** |
| n1468 | marker | 8 (claude) | 110.5, 22.7 | codex: n2200 (triangle-up) | | | **identity conflict** |
| n1468 | marker | 10 (claude) | 120.5, 22.2 | codex: n3660 (x) | | | **identity conflict** |
| n1468 | marker | 11 (claude) | 130.1, 29.4 | codex: n2200 (triangle-up) | | | **identity conflict** |
| n2200 | marker | 8 (codex) | 92.1, 18.8 | claude: n1468 (circle) | | | **identity conflict** |
| n2200 | marker | 9 (codex) | 101.3, 22.0 | claude: n1468 (circle) | | | **identity conflict** |
| n2200 | marker | 10 (codex) | 111.4, 24.8 | claude: n1468 (circle) | | | **identity conflict** |
| n2200 | marker | 12 (codex) | 130.3, 31.5 | claude: n1468 (circle) | | | **identity conflict** |
| n2995 | marker | 10 (claude) | 130.1, 25.0 | codex: n3660 (x) | | | **identity conflict** |
| n3660 | marker | 1 (codex) | 82.0, 19.4 | claude: n2995 (square) | | | **identity conflict** |
| n734 | marker | 5 (claude) | 50.1, 22.1 | codex: n1468 (circle) | | | **identity conflict** |
