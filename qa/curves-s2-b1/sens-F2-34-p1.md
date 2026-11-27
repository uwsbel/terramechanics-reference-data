# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b1\rederived\claude\F2-34\points-p1-native.csv` (claude), `<repository>\qa\curves-s2-b1\rederived\codex\F2-34\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 70 | 49 |
| x per px | 0.0038 | 0.0038 |
| y per px | 0.7640 | 0.7619 |
| RMS residual x, y | 0.012, 2.009 | 0.009, 1.481 |

Corners of claude's box [600, 1280, 2280, 3700] mapped by both calibrations (tolerance 0.03 in x, 4.25 in y):

- (9.1, 1225.8) vs (9.1, 1223.2)
- (9.1, -57.6) vs (9.1, -56.7)
- (-0.1, 1240.8) vs (-0.1, 1238.2)
- (-0.2, -42.6) vs (-0.2, -41.7)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.52 | 0.33 | 0.30 | 18 | 0.68 | 0.72 | agree |
| x | 1 | 0.39 | 0.46 | 0.35 | 18 | 1.08 | 0.71 | agree |
| x | 2 | 0.09 | 0.32 | 0.29 | 18 | 0.64 | 0.55 | agree |
| x | 3 | 0.35 | 0.60 | 0.46 | 18 | 1.06 | 0.74 | agree |
| x | 4 | 0.21 | 0.68 | 0.52 | 18 | 1.74 | 1.78 | agree |
| x | 5 | 0.21 | 0.44 | 0.38 | 18 | 0.91 | 0.75 | agree |
| x | 6 | 1.33 | 0.34 | 0.79 | 18 | 0.72 | 2.12 | agree |
| x | 7 | | | | | 1.10 | | only in claude |
| x | 8 | | | | | 0.80 | | only in claude |
| x | 9 | | | | | 2.65 | | only in claude |
| y | 0 | 0.65 | 0.41 | 0.22 | 17 | 1.59 | 0.50 | agree |
| y | 200 | 0.57 | 0.56 | 0.48 | 17 | 1.43 | 1.08 | agree |
| y | 400 | 0.34 | 0.42 | 0.33 | 17 | 0.79 | 0.59 | agree |
| y | 600 | 0.27 | 0.40 | 0.39 | 17 | 0.69 | 0.60 | agree |
| y | 800 | 0.48 | 0.25 | 0.28 | 17 | 0.93 | 0.53 | agree |
| y | 1000 | 0.59 | 0.36 | 0.28 | 18 | 0.83 | 0.50 | agree |
| y | 1200 | 0.11 | 0.29 | 0.28 | 17 | 0.50 | 0.54 | agree |

Both maps along every verified line and every interval midline (318 places): largest difference 0.08161 in x (tolerance 0.01839, claude 9), 0.8071 in y (tolerance 2.031, claude 0); 26 beyond the two maps' line errors.

Canonical reading: claude (claude's lines include all of codex's and more, as close to the ink; 14 shared lines checked against the ink, mean of the median distances 0.42 px (claude: x 0.45, y 0.38), 0.38 px (codex: x 0.44, y 0.32)); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 71; agreed 57; disagreed 14; unmatched 7 (kept as one-sided: 0 of claude, 7 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| fit | feature | 1/2 | -0.0, 139.1 (0.0, 2.1) | 0.0, 127.5 (0.0, 2.3) | -0.0 | +11.6 | **disagree** |
| fit | trace | 1/interp | 0.0, 140.2 (0.0, 2.1) | 0.0, 128.3 (0.0, 2.3) | slope +62.2 | +11.9 (tol 5.6) | **disagree** |
| fit | trace | 6/interp | 5.0, 401.3 (0.0, 2.2) | 5.0, 409.6 (0.0, 3.7) | slope +61.9 | -8.3 (tol 7.9) | **disagree** |
| lpt87 | feature | 1/1 | 0.0, 2.3 (0.0, 2.9) | 0.0, 8.2 (0.0, 2.1) | -0.0 | -5.9 | **disagree** |
| lpt87 | feature | 3/11 | 1.3, 173.0 (0.1, 3.8) | 1.6, 191.2 (0.0, 1.7) | -0.3 | -18.2 | **disagree** |
| lpt87 | feature | -/7 | (none) | 0.8, 151.8 | | | unmatched in claude |
| lpt87 | trace | 8/interp | 1.7, 202.8 (0.0, 2.5) | 1.7, 227.9 (0.0, 1.9) | slope +181.6 | -25.1 (tol 8.0) | **disagree** |
| lpt87 | trace | 9/interp | 2.0, 227.1 (0.0, 2.1) | 2.0, 241.4 (0.0, 2.3) | slope +52.2 | -14.3 (tol 5.4) | **disagree** |
| lpt87 | trace | 17/interp | 4.0, 431.1 (0.0, 2.2) | 4.0, 438.7 (0.0, 2.2) | slope +77.1 | -7.6 (tol 6.4) | **disagree** |
| lpt87 | trace | 20/interp | 4.8, 513.9 (0.0, 2.2) | 4.8, 529.9 (0.0, 2.2) | slope +52.8 | -16.0 (tol 5.6) | **disagree** |
| lpt88 | feature | 1/1 | 2.0, 7.3 (0.0, 3.7) | 2.0, 53.3 (0.0, 2.2) | -0.0 | -46.0 | **disagree** |
| lpt88 | feature | 4/32 | 8.1, 657.5 (0.0, 1.5) | 8.1, 658.6 (0.0, 1.0) | +0.0 | -1.1 | **disagree** |
| lpt88 | feature | 2/5 | 2.3, 252.8 (0.0, 4.3) | 2.3, 258.4 (0.0, 3.8) | -0.0 | -5.6 | **disagree** |
| lpt88 | feature | -/3 | (none) | 2.0, 53.3 | | | unmatched in claude |
| lpt88 | feature | -/7 | (none) | 2.7, 281.6 | | | unmatched in claude |
| lpt88 | feature | -/12 | (none) | 3.5, 312.0 | | | unmatched in claude |
| lpt88 | trace | 1/interp | 2.0, 7.3 (0.0, 3.7) | 2.0, 53.3 (0.0, 2.2) | slope +829.5 | -46.0 (tol 20.7) | **disagree** |
| lpt88 | trace | 24/interp | 7.7, 627.4 (0.0, 1.6) | 7.7, 632.9 (0.0, 1.1) | slope +93.5 | -5.5 (tol 5.1) | **disagree** |
