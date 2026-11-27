# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-2C\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-2C\points-p2-native.csv` (codex).

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

Matched: 42; agreed 37; disagreed 5; unmatched 7 (kept as one-sided: 2 of claude, 3 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1468 | marker | 6/- | 90.8, 17.4 | (none) | | | unmatched in codex |
| n2200 | marker | 6/6 | 70.9, 5.2 (0.7, 1.2) | 71.4, 10.7 (1.5, 3.0) | -0.4 | -5.5 | **disagree** |
| n2200 | marker | -/8 | (none) | 92.1, 18.8 | | | unmatched in claude |
| n2200 | marker | -/9 | (none) | 101.3, 22.0 | | | unmatched in claude |
| n2200 | marker | -/10 | (none) | 111.4, 24.8 | | | unmatched in claude |
| n2200 | marker | -/12 | (none) | 130.3, 31.5 | | | unmatched in claude |
| n2995 | marker | 5/5 | 60.6, 16.2 (0.5, 0.9) | 60.9, 18.5 (0.4, 0.9) | -0.3 | -2.3 | **disagree** |
| n2995 | marker | 6/6 | 70.8, 11.7 (0.7, 1.2) | 71.2, 19.3 (1.3, 2.6) | -0.4 | -7.6 | **disagree** |
| n3660 | marker | 6/7 | 140.5, 24.4 (0.5, 0.9) | 141.8, 26.8 (0.4, 0.9) | -1.3 | -2.4 | **disagree** |
| n4400 | marker | 7/7 | 140.4, 15.2 (0.5, 0.9) | 141.8, 15.9 (0.4, 0.9) | -1.5 | -0.7 | **disagree** |
| n734 | marker | 1/- | 5.1, 3.9 | (none) | | | unmatched in codex |
| n734 | marker | 2/- | 10.0, 6.3 | (none) | | | unmatched in codex |
| n1468 | marker | 6 (claude) | 90.8, 17.4 | codex: n3660 (x), n2200 (triangle-up) | | | **identity conflict** |
| n2200 | marker | 8 (codex) | 92.1, 18.8 | claude: n1468 (circle) | | | **identity conflict** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
