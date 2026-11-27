# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b2\rederived\claude\FA-6\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b2\rederived\codex\FA-6\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 132 | 987 |
| x per px | 0.0010 | 0.0010 |
| y per px | 0.0686 | 0.0686 |
| RMS residual x, y | 0.002, 0.060 | 0.002, 0.058 |

Corners of claude's box [778, 1162, 2275, 3762] mapped by both calibrations (tolerance 0.01 in x, 0.19 in y (in the plotting coordinates of log10 x, linear y)):

- (9.4, 100.7) vs (9.4, 100.7)
- (9.3, -1.9) vs (9.3, -1.9)
- (0.0, 101.6) vs (0.0, 101.6)
- (0.0, -1.1) vs (0.0, -1.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0.02 | 0.17 | 0.35 | 0.34 | 23 | 0.67 | 0.56 | agree |
| x | 0.05 | 0.04 | 0.41 | 0.39 | 20 | 1.07 | 0.60 | agree |
| x | 0.1 | 0.17 | 0.47 | 0.47 | 21 | 0.61 | 0.56 | agree |
| x | 0.2 | 0.04 | 0.29 | 0.29 | 20 | 0.87 | 0.50 | agree |
| x | 0.5 | 0.21 | 0.48 | 0.53 | 19 | 0.86 | 0.87 | agree |
| x | 1 | 0.21 | 0.47 | 0.34 | 23 | 1.45 | 0.75 | agree |
| x | 1.5 | 0.44 | 0.47 | 0.41 | 22 | 0.82 | 0.56 | agree |
| x | 2 | 0.09 | 0.48 | 0.46 | 23 | 0.74 | 0.95 | agree |
| x | 3 | 0.05 | 0.60 | 0.59 | 23 | 0.76 | 0.65 | agree |
| x | 4 | 0.19 | 0.57 | 0.49 | 23 | 0.82 | 0.87 | agree |
| x | 5 | 0.06 | 0.50 | 0.51 | 23 | 0.93 | 0.84 | agree |
| x | 9 | 0.34 | 0.58 | 0.60 | 23 | 1.27 | 0.86 | agree |
| y | 40 | | | | | | | claude's line not a knot: misplaced: 3.31 px from the ink's line at an end of the line |
| y | 80 | | | | | | | claude's line not a knot: misplaced: 2.51 px from the ink's line at an end of the line |
| y | 0 | 0.22 | 0.36 | 0.41 | 23 | 0.78 | 0.72 | agree |
| y | 10 | 0.13 | 0.45 | 0.57 | 23 | 1.02 | 0.77 | agree |
| y | 20 | 0.06 | 0.29 | 0.26 | 23 | 0.50 | 0.50 | agree |
| y | 30 | 0.14 | 0.22 | 0.26 | 22 | 0.50 | 0.55 | agree |
| y | 50 | 0.32 | 0.66 | 0.62 | 21 | 1.01 | 0.77 | agree |
| y | 60 | 0.53 | 0.19 | 0.52 | 20 | 0.78 | 1.21 | agree |
| y | 70 | 0.20 | 0.22 | 0.17 | 20 | 0.50 | 0.50 | agree |
| y | 90 | 0.04 | 0.20 | 0.21 | 23 | 0.61 | 0.52 | agree |
| y | 100 | 0.21 | 0.22 | 0.28 | 22 | 0.52 | 0.63 | agree |
| y | 40 | | | | | | 1.38 | only in codex |
| y | 80 | | | | | | 0.85 | only in codex |

(In the plotting coordinates: log10 x, linear y.) Both maps along every verified line and every interval midline (483 places): largest difference 0.0004047 in x (tolerance 0.002265, codex 1.5), 0.02793 in y (tolerance 0.1536, claude 60); 0 beyond the two maps' line errors.

Canonical reading: codex (codex's lines include all of claude's and more, as close to the ink; 21 shared lines checked against the ink, mean of the median distances 0.40 px (claude: x 0.47, y 0.31), 0.42 px (codex: x 0.45, y 0.37)); points are evaluated at codex's samples.

## Series

3 series in codex, 3 in claude.


## Points

Matched: 144; agreed 112; disagreed 32; unmatched 37 (kept as one-sided: 24 of codex, 12 of claude).

| series | kind | seq (codex/claude) | codex x, y (bounds) | claude x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| average | feature | 1/1 | 0.1, 0.8 (0.0, 0.6) | 0.1, 1.0 (0.0, 0.2) | +0.0 | -0.1 | **disagree** |
| average | feature | 3/3 | 2.4, 90.4 (0.0, 0.4) | 2.8, 98.1 (0.0, 0.4) | -0.4 | -7.7 | **disagree** |
| average | feature | 4/2 | 0.9, 3.6 (0.0, 0.4) | 1.1, 6.4 (0.0, 0.4) | -0.2 | -2.8 | **disagree** |
| average | marker | 1/- | 3.4, 99.7 | (none) | | | unmatched in claude |
| average | marker | 2/- | 2.4, 88.1 | (none) | | | unmatched in claude |
| average | marker | 3/- | 2.0, 62.2 | (none) | | | unmatched in claude |
| average | marker | 4/- | 1.7, 45.6 | (none) | | | unmatched in claude |
| average | marker | 5/- | 1.2, 9.9 | (none) | | | unmatched in claude |
| average | marker | 6/- | 0.8, 2.5 | (none) | | | unmatched in claude |
| average | marker | 7/- | 0.6, 1.6 | (none) | | | unmatched in claude |
| average | marker | 8/- | 0.4, 2.1 | (none) | | | unmatched in claude |
| average | marker | 9/- | 0.3, 1.4 | (none) | | | unmatched in claude |
| average | marker | 10/- | 0.2, 0.9 | (none) | | | unmatched in claude |
| average | marker | 11/- | 0.2, 0.7 | (none) | | | unmatched in claude |
| average | marker | 12/- | 0.2, 0.6 | (none) | | | unmatched in claude |
| average | marker | 13/- | 0.1, 1.3 | (none) | | | unmatched in claude |
| average | marker | 14/- | 0.1, 0.4 | (none) | | | unmatched in claude |
| average | trace | 18/interp | 1.0, 4.0 (0.0, 0.1) | 1.0, 5.5 (0.0, 0.3) | slope +25.5 | -1.5 (tol 0.9) | **disagree** |
| average | trace | 28/interp | 1.8, 49.3 (0.0, 0.4) | 1.8, 55.0 (0.0, 0.2) | slope +72.4 | -5.7 (tol 3.6) | **disagree** |
| average | trace | 31/interp | 2.0, 64.1 (0.0, 0.3) | 2.0, 71.7 (0.0, 0.2) | slope +64.6 | -7.7 (tol 2.7) | **disagree** |
| average | trace | 32/interp | 2.0, 64.6 (0.0, 0.3) | 2.0, 72.4 (0.0, 0.2) | slope +64.3 | -7.8 (tol 2.8) | **disagree** |
| average | trace | 40/interp | 3.2, 98.7 (0.1, 0.5) | 3.2, 99.8 (0.0, 0.3) | slope +0.5 | -1.1 (tol 0.8) | **disagree** |
| lower | feature | 1/1 | 0.1, 0.8 (0.0, 0.6) | 0.1, 1.0 (0.0, 0.2) | +0.0 | -0.1 | **disagree** |
| lower | feature | 2/4 | 3.9, 100.4 (0.1, 0.5) | 4.1, 100.7 (0.0, 0.3) | -0.1 | -0.2 | **disagree** |
| lower | feature | 3/3 | 2.3, 85.2 (0.0, 0.4) | 2.8, 97.8 (0.0, 0.4) | -0.5 | -12.6 | **disagree** |
| lower | feature | 4/2 | 0.9, 2.0 (0.0, 0.4) | 1.1, 6.1 (0.0, 0.4) | -0.2 | -4.1 | **disagree** |
| lower | marker | 1/- | 2.3, 86.3 | (none) | | | unmatched in claude |
| lower | marker | 2/- | 2.0, 58.7 | (none) | | | unmatched in claude |
| lower | marker | 6/- | 0.6, 1.0 | (none) | | | unmatched in claude |
| lower | marker | 7/- | 0.4, 0.4 | (none) | | | unmatched in claude |
| lower | marker | 3/2 | 1.7, 41.8 (0.0, 0.5) | 1.7, 36.8 (0.0, 0.2) | +0.0 | +5.0 | **disagree** |
| lower | marker | 4/1 | 1.2, 8.7 (0.0, 0.5) | 1.2, 6.1 (0.0, 0.2) | +0.0 | +2.6 | **disagree** |
| lower | trace | 26/interp | 1.6, 39.6 (0.0, 0.3) | 1.6, 34.8 (0.0, 0.2) | slope +74.5 | +4.8 (tol 2.7) | **disagree** |
| lower | trace | 30/interp | 1.9, 60.7 (0.0, 0.4) | 1.9, 55.2 (0.0, 0.2) | slope +69.1 | +5.5 (tol 3.6) | **disagree** |
| upper | feature | 1/1 | 0.1, 0.8 (0.0, 0.6) | 0.1, 1.0 (0.0, 0.2) | +0.0 | -0.1 | **disagree** |
| upper | feature | 2/4 | 3.9, 100.4 (0.1, 0.5) | 4.1, 100.7 (0.0, 0.2) | -0.1 | -0.2 | **disagree** |
| upper | feature | 3/3 | 2.4, 90.4 (0.0, 0.4) | 2.6, 96.3 (0.0, 0.4) | -0.2 | -5.8 | **disagree** |
| upper | feature | 4/2 | 0.9, 4.0 (0.0, 0.5) | 1.0, 6.7 (0.0, 0.4) | -0.1 | -2.7 | **disagree** |
| upper | marker | 1/- | 2.4, 89.2 | (none) | | | unmatched in claude |
| upper | marker | 2/- | 2.0, 66.4 | (none) | | | unmatched in claude |
| upper | marker | 4/- | 1.2, 12.2 | (none) | | | unmatched in claude |
| upper | marker | 5/- | 0.8, 3.7 | (none) | | | unmatched in claude |
| upper | marker | 6/- | 0.6, 2.8 | (none) | | | unmatched in claude |
| upper | marker | 7/- | 0.4, 2.8 | (none) | | | unmatched in claude |
| upper | marker | 8/- | 0.2, 1.4 | (none) | | | unmatched in claude |
| upper | marker | 3/1 | 1.7, 49.7 (0.0, 0.5) | 1.6, 47.3 (0.0, 0.2) | +0.1 | +2.5 | **disagree** |
| upper | trace | 11/interp | 0.4, 2.0 (0.0, 0.2) | 0.4, 2.8 (0.0, 0.2) | slope -2.9 | -0.8 (tol 0.5) | **disagree** |
| upper | trace | 15/interp | 0.7, 2.4 (0.0, 0.3) | 0.7, 3.5 (0.0, 0.2) | slope +4.0 | -1.2 (tol 0.6) | **disagree** |
| upper | trace | 24/interp | 1.4, 25.0 (0.0, 0.5) | 1.4, 30.3 (0.0, 0.2) | slope +106.8 | -5.3 (tol 4.7) | **disagree** |
| upper | trace | 30/interp | 1.8, 50.4 (0.0, 0.3) | 1.8, 59.5 (0.0, 0.2) | slope +66.1 | -9.1 (tol 2.6) | **disagree** |
| upper | trace | 34/interp | 1.9, 65.0 (0.0, 0.3) | 1.9, 70.8 (0.0, 0.2) | slope +59.7 | -5.7 (tol 2.9) | **disagree** |
| upper | trace | 35/interp | 2.0, 69.6 (0.0, 0.5) | 2.0, 73.4 (0.0, 0.2) | slope +58.3 | -3.8 (tol 3.8) | **disagree** |
| upper | trace | 36/interp | 2.1, 70.1 (0.0, 0.1) | 2.1, 80.8 (0.0, 0.2) | slope +60.1 | -10.8 (tol 2.0) | **disagree** |
| upper | trace | 38/interp | 2.2, 79.6 (0.0, 3.0) | 2.2, 85.8 (0.0, 0.2) | slope +57.8 | -6.2 (tol 6.1) | **disagree** |
| upper | trace | 39/interp | 2.2, 84.7 (0.0, 2.7) | 2.2, 89.4 (0.0, 0.2) | slope +23.6 | -4.7 (tol 4.4) | **disagree** |
| upper | trace | 40/interp | 2.5, 93.4 (0.0, 0.4) | 2.5, 95.5 (0.0, 0.2) | slope +11.7 | -2.1 (tol 1.3) | **disagree** |
| upper | trace | 42/interp | 3.2, 98.7 (0.1, 0.5) | 3.2, 99.8 (0.0, 0.3) | slope +1.6 | -1.1 (tol 0.9) | **disagree** |
| average | marker | 13 (codex) | 0.1, 1.3 | claude: upper (circle) | | | **identity conflict** |
