# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-2B\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-2B\points-p2-native.csv` (codex).

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

Matched: 125; agreed 125; disagreed 0; unmatched 4 (kept as one-sided: 0 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n3660 | marker | -/2 | (none) | 28.8, -13.4 | | | unmatched in claude |
| n3660 | marker | -/3 | (none) | 38.5, -14.0 | | | unmatched in claude |
| n3660 | marker | -/4 | (none) | 48.3, -15.7 | | | unmatched in claude |
| n3660 | marker | -/5 | (none) | 58.7, -15.0 | | | unmatched in claude |
| n3660 | marker | 2 (codex) | 28.8, -13.4 | claude: n2995 (square), n4400 (asterisk) | | | **identity conflict** |
| n3660 | marker | 3 (codex) | 38.5, -14.0 | claude: n2200 (triangle-up), n2995 (square) | | | **identity conflict** |
| n3660 | marker | 4 (codex) | 48.3, -15.7 | claude: n2995 (square), n4400 (asterisk) | | | **identity conflict** |
| n3660 | marker | 5 (codex) | 58.7, -15.0 | claude: n2200 (triangle-up), n2995 (square) | | | **identity conflict** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
