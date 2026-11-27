# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b3\rederived\claude\FA-27\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b3\rederived\codex\FA-27\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 220 | 143 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0000 | 0.0000 |
| RMS residual x, y | 0.001, 0.000 | 0.001, 0.000 |

Corners of claude's box [650, 3122, 2235, 3680] mapped by both calibrations (tolerance 0.00 in x, 0.00 in y (in the plotting coordinates of linear x, reciprocal y)):

- (-0.0, 94.5) vs (-0.0, 94.5)
- (1.0, 94.7) vs (1.0, 94.7)
- (-0.0, 114.5) vs (-0.0, 114.2)  **disagree**
- (1.0, 114.7) vs (1.0, 114.4)  **disagree**

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.19 | 0.32 | 0.37 | 17 | 0.53 | 0.55 | agree |
| x | 0.1 | 0.22 | 0.31 | 0.22 | 17 | 0.60 | 0.50 | agree |
| x | 0.2 | 0.51 | 0.24 | 0.30 | 17 | 0.63 | 0.50 | agree |
| x | 0.3 | 0.44 | 0.24 | 0.50 | 17 | 0.50 | 0.58 | agree |
| x | 0.4 | 0.67 | 0.31 | 0.45 | 17 | 0.80 | 0.75 | agree |
| x | 0.5 | 1.37 | 0.30 | 0.73 | 17 | 0.58 | 1.28 | agree |
| x | 0.6 | 0.45 | 0.28 | 0.52 | 17 | 0.56 | 0.61 | agree |
| x | 0.7 | 0.35 | 0.28 | 0.31 | 17 | 0.50 | 0.60 | agree |
| x | 0.8 | 0.69 | 0.34 | 0.35 | 16 | 0.62 | 0.59 | agree |
| x | 0.9 | 0.34 | 0.19 | 0.21 | 16 | 0.62 | 0.76 | agree |
| x | 1 | 0.84 | 0.19 | 0.58 | 17 | 0.50 | 1.05 | agree |
| y | 115 | | | | | | | codex's line not a knot: insufficient ink: found at 2 of 25 positions over 5% of the line's length |
| y | 95 | 0.16 | 0.37 | 0.34 | 25 | 0.50 | 0.56 | agree |
| y | 100 | 0.11 | 0.29 | 0.23 | 25 | 0.56 | 0.52 | agree |
| y | 105 | 0.15 | 0.36 | 0.36 | 25 | 0.72 | 0.82 | agree |
| y | 110 | 0.23 | 0.22 | 0.18 | 25 | 0.69 | 0.53 | agree |
| y | 96 | | | | | 1.05 | | only in claude |
| y | 97 | | | | | 0.84 | | only in claude |
| y | 98 | | | | | 0.50 | | only in claude |
| y | 99 | | | | | 0.56 | | only in claude |
| y | 101 | | | | | 1.45 | | only in claude |
| y | 102 | | | | | 0.64 | | only in claude |
| y | 103 | | | | | 0.86 | | only in claude |
| y | 104 | | | | | 1.03 | | only in claude |
| y | 106 | | | | | 0.74 | | only in claude |
| y | 107 | | | | | 0.76 | | only in claude |
| y | 108 | | | | | 0.67 | | only in claude |
| y | 109 | | | | | 0.67 | | only in claude |
| y | 111 | | | | | 0.54 | | only in claude |
| y | 112 | | | | | 0.73 | | only in claude |
| y | 113 | | | | | 0.64 | | only in claude |
| y | 114 | | | | | 0.69 | | only in claude |
| y | 55 | | | | | | 0.50 | only in codex |
| y | 60 | | | | | | 0.82 | only in codex |
| y | 65 | | | | | | 0.50 | only in codex |
| y | 70 | | | | | | 0.50 | only in codex |
| y | 75 | | | | | | 0.50 | only in codex |
| y | 80 | | | | | | 0.55 | only in codex |
| y | 85 | | | | | | 0.55 | only in codex |
| y | 90 | | | | | | 0.56 | only in codex |

(In the plotting coordinates: linear x, reciprocal y.) Both maps along every verified line and every interval midline (558 places): largest difference 0.0008041 in x (tolerance 0.001345, codex 0.5), 3.992e-05 in y (tolerance 4.615e-06, claude 113); 114 beyond the two maps' line errors.

Canonical reading: claude (**coverage cannot be ranked** (lines claude: x [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], y [95.0, 96.0, 97.0, 98.0, 99.0, 100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0, 112.0, 113.0, 114.0]; codex: x [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], y [55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0]): recover the missing lines or name the canonical reading in overlays.csv; meanwhile first submission by the ink; 15 shared lines checked against the ink, mean of the median distances 0.28 px (claude: x 0.27, y 0.31), 0.38 px (codex: x 0.41, y 0.28)); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 44; agreed 36; disagreed 8; unmatched 3 (kept as one-sided: 0 of claude, 3 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| lower | feature | 1/1 | 0.0, 95.8 (0.0, 0.1) | -0.0, 95.9 (0.0, 0.1) | +0.0 | -0.2 | **disagree** |
| lower | trace | 10/interp | 0.9, 112.8 (0.0, 0.1) | 0.9, 112.3 (0.0, 0.1) | slope +20.3 | +0.6 (tol 0.3) | **disagree** |
| mean | feature | 2/2 | 1.0, 112.6 (0.0, 0.1) | 1.0, 112.2 (0.0, 0.1) | +0.0 | +0.4 | **disagree** |
| mean | trace | 11/interp | 1.0, 112.6 (0.0, 0.1) | 1.0, 112.2 (0.0, 0.1) | slope +18.8 | +0.4 (tol 0.3) | **disagree** |
| upper | feature | 1/1 | 0.0, 95.1 (0.0, 0.1) | -0.0, 95.3 (0.0, 0.1) | +0.0 | -0.2 | **disagree** |
| upper | feature | 2/2 | 1.0, 110.6 (0.0, 0.1) | 1.0, 110.2 (0.0, 0.1) | +0.0 | +0.4 | **disagree** |
| upper | trace | 3/interp | 0.2, 98.0 (0.0, 0.1) | 0.2, 97.7 (0.0, 0.1) | slope +13.2 | +0.2 (tol 0.2) | **disagree** |
| upper | trace | 11/interp | 1.0, 110.6 (0.0, 0.1) | 1.0, 110.2 (0.0, 0.1) | slope +15.1 | +0.4 (tol 0.3) | **disagree** |
