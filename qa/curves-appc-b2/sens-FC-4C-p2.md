# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b2\rederived\claude\FC-4C\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b2\rederived\codex\FC-4C\points-p2-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 18 | 18 |
| x per px | 0.1718 | 0.1718 |
| y per px | 0.3476 | 0.3476 |
| RMS residual x, y | 0.460, 0.154 | 0.453, 0.110 |

Corners of claude's box [750, 2750, 2260, 3380] mapped by both calibrations (tolerance 1.09 in x, 0.61 in y):

- (-4.0, 110.6) vs (-4.0, 110.5)
- (255.4, 109.1) vs (255.4, 109.1)
- (-5.0, -108.4) vs (-5.0, -108.5)
- (254.4, -109.9) vs (254.4, -109.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.15 | 0.19 | 0.20 | 6 | 0.50 | 0.50 | agree |
| x | 50 | 0.07 | 0.37 | 0.39 | 6 | 0.72 | 0.75 | agree |
| x | 100 | 0.17 | 0.30 | 0.31 | 6 | 0.64 | 0.75 | agree |
| x | 150 | 0.17 | 0.30 | 0.38 | 6 | 0.50 | 0.70 | agree |
| x | 200 | 0.00 | 0.35 | 0.35 | 6 | 0.59 | 0.59 | agree |
| x | 250 | 0.18 | 0.29 | 0.25 | 6 | 1.25 | 1.10 | agree |
| y | -100 | 0.26 | 0.32 | 0.39 | 15 | 0.60 | 0.80 | agree |
| y | 0 | 0.74 | 0.70 | 0.35 | 15 | 1.53 | 0.78 | agree |
| y | 100 | 0.20 | 0.23 | 0.18 | 15 | 0.61 | 0.75 | agree |

Both maps along every verified line and every interval midline (200 places): largest difference 0.03763 in x (tolerance 0.2525, codex 0), 0.2845 in y (tolerance 0.8122, claude 0); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.34 px (claude: x 0.30, y 0.41), 0.31 px (codex: x 0.31, y 0.31), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 68; agreed 57; disagreed 11; unmatched 4 (kept as one-sided: 1 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1761 | marker | 2/- | 20.2, -1.2 | (none) | | | unmatched in codex |
| n1761 | marker | 12/11 | 198.5, 60.2 (0.3, 0.7) | 200.0, 59.0 (0.9, 1.9) | -1.4 | +1.2 | **disagree** |
| n1761 | marker | 13/12 | 219.1, 58.1 (0.3, 0.5) | 220.7, 57.1 (1.0, 1.9) | -1.6 | +0.9 | **disagree** |
| n2934 | marker | 1/- | -1.2, -20.9 | (none) | | | unmatched in codex |
| n3815 | marker | 9/- | 118.8, 24.6 | (none) | | | unmatched in codex |
| n3815 | marker | 11/11 | 148.4, 24.4 (0.3, 0.8) | 149.5, 23.9 (0.8, 1.7) | -1.2 | +0.5 | **disagree** |
| n3815 | marker | 14/14 | 198.6, 26.0 (0.3, 0.7) | 199.8, 26.1 (0.8, 1.7) | -1.2 | -0.0 | **disagree** |
| n3815 | marker | 15/15 | 218.9, 24.6 (0.3, 0.6) | 220.4, 24.6 (0.8, 1.5) | -1.5 | +0.1 | **disagree** |
| n3815 | marker | -/2 | (none) | -1.6, -21.2 | | | unmatched in claude |
| n4695 | marker | 7/7 | 89.6, 6.5 (0.2, 0.6) | 89.2, 6.2 (0.2, 0.5) | +0.5 | +0.3 | **disagree** |
| n4695 | marker | 8/8 | 108.8, 12.2 (0.2, 0.6) | 108.3, 12.0 (0.2, 0.5) | +0.5 | +0.2 | **disagree** |
| n4695 | marker | 9/9 | 130.1, 13.1 (0.2, 0.6) | 129.6, 12.9 (0.2, 0.5) | +0.5 | +0.2 | **disagree** |
| n4695 | marker | 14/14 | 220.3, 19.8 (0.3, 0.6) | 221.6, 19.7 (0.7, 1.3) | -1.3 | +0.1 | **disagree** |
| n741 | marker | 3/3 | 30.0, -1.6 (0.4, 1.0) | 20.2, -2.9 (0.9, 1.9) | +9.8 | +1.2 | **disagree** |
| n741 | marker | 10/10 | 148.3, 55.5 (0.3, 0.7) | 149.7, 54.8 (0.9, 1.9) | -1.4 | +0.7 | **disagree** |
| n1761 | marker | 2 (claude) | 20.2, -1.2 | codex: n741 (triangle-down) | | | **identity conflict** |
| n2934 | marker | 1 (claude) | -1.2, -20.9 | codex: n3815 (circle) | | | **identity conflict** |
| n3815 | marker | 2 (codex) | -1.6, -21.2 | claude: n4695 (plus), n2934 (triangle-up) | | | **identity conflict** |
