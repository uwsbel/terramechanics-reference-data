# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b2\rederived\claude\FA-46\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b2\rederived\codex\FA-46\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 132 | 1044 |
| x per px | 0.0010 | 0.0010 |
| y per px | 0.0686 | 0.0686 |
| RMS residual x, y | 0.003, 0.082 | 0.003, 0.066 |

Corners of claude's box [712, 1151, 2205, 3755] mapped by both calibrations (tolerance 0.01 in x, 0.22 in y (in the plotting coordinates of log10 x, linear y)):

- (9.4, 100.8) vs (9.4, 100.8)
- (9.3, -1.6) vs (9.3, -1.6)
- (0.0, 101.9) vs (0.0, 101.9)
- (0.0, -0.6) vs (0.0, -0.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0.1 | | | | | | | claude's line not a knot: misplaced: 4.69 px from the ink's line at an end of the line |
| x | 0.02 | 0.05 | 0.35 | 0.35 | 23 | 0.84 | 0.69 | agree |
| x | 0.05 | 0.43 | 0.16 | 0.18 | 20 | 0.94 | 0.64 | agree |
| x | 0.2 | 0.52 | 0.28 | 0.27 | 20 | 0.65 | 1.00 | agree |
| x | 0.5 | 0.58 | 0.44 | 0.35 | 20 | 1.27 | 0.57 | agree |
| x | 1 | 0.66 | 0.63 | 0.61 | 23 | 1.05 | 0.94 | agree |
| x | 1.5 | 0.07 | 0.34 | 0.32 | 22 | 0.50 | 0.50 | agree |
| x | 2 | 0.11 | 0.36 | 0.32 | 23 | 0.68 | 0.65 | agree |
| x | 3 | 0.09 | 0.32 | 0.35 | 23 | 0.74 | 0.82 | agree |
| x | 4 | 0.08 | 0.59 | 0.60 | 23 | 0.80 | 0.59 | agree |
| x | 5 | 0.18 | 0.57 | 0.52 | 23 | 0.84 | 0.73 | agree |
| x | 9 | 0.13 | 0.57 | 0.62 | 23 | 0.80 | 0.74 | agree |
| x | 0.1 | | | | | | 0.72 | only in codex |
| y | 60 | | | | | | | claude's line not a knot: misplaced: 5.70 px from the ink's line at an end of the line |
| y | 0 | 0.06 | 0.48 | 0.51 | 23 | 0.97 | 0.89 | agree |
| y | 10 | 0.45 | 0.35 | 0.43 | 23 | 0.91 | 0.70 | agree |
| y | 20 | 0.28 | 0.19 | 0.24 | 23 | 0.51 | 0.50 | agree |
| y | 30 | 0.47 | 0.32 | 0.36 | 23 | 0.65 | 0.50 | agree |
| y | 40 | 0.64 | 0.45 | 0.27 | 23 | 0.88 | 0.52 | agree |
| y | 50 | 0.52 | 0.52 | 0.33 | 20 | 2.08 | 0.62 | agree |
| y | 70 | 0.31 | 0.40 | 0.24 | 20 | 1.65 | 0.50 | agree |
| y | 80 | 0.29 | 0.27 | 0.27 | 20 | 0.89 | 0.50 | agree |
| y | 90 | 0.09 | 0.19 | 0.24 | 23 | 0.54 | 0.83 | agree |
| y | 100 | 0.33 | 0.25 | 0.36 | 23 | 1.15 | 0.59 | agree |
| y | 60 | | | | | | 1.28 | only in codex |

(In the plotting coordinates: log10 x, linear y.) Both maps along every verified line and every interval midline (474 places): largest difference 0.001185 in x (tolerance 0.001724, codex 0.1), 0.1201 in y (tolerance 0.23, codex 60); 0 beyond the two maps' line errors.

Canonical reading: codex (codex's lines include all of claude's and more, as close to the ink; 21 shared lines checked against the ink, mean of the median distances 0.38 px (claude: x 0.42, y 0.34), 0.37 px (codex: x 0.41, y 0.32)); points are evaluated at codex's samples.

## Series

3 series in codex, 3 in claude.


## Points

Matched: 158; agreed 128; disagreed 30; unmatched 34 (kept as one-sided: 26 of codex, 8 of claude).

| series | kind | seq (codex/claude) | codex x, y (bounds) | claude x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| average | feature | 1/1 | 0.1, 1.1 (0.0, 0.8) | 0.1, 1.3 (0.0, 0.2) | +0.0 | -0.2 | **disagree** |
| average | feature | 2/4 | 3.9, 99.7 (0.1, 0.5) | 4.1, 99.7 (0.0, 0.3) | -0.2 | -0.0 | **disagree** |
| average | feature | 3/3 | 2.5, 81.5 (0.0, 3.0) | 2.8, 95.8 (0.0, 0.3) | -0.4 | -14.3 | **disagree** |
| average | feature | 4/2 | 0.9, 3.2 (0.0, 0.4) | 0.8, 2.7 (0.0, 0.3) | +0.1 | +0.5 | **disagree** |
| average | marker | 1/- | 3.4, 99.1 | (none) | | | unmatched in claude |
| average | marker | 2/- | 2.4, 70.7 | (none) | | | unmatched in claude |
| average | marker | 3/- | 2.0, 40.5 | (none) | | | unmatched in claude |
| average | marker | 4/- | 1.7, 25.9 | (none) | | | unmatched in claude |
| average | marker | 5/- | 1.2, 8.9 | (none) | | | unmatched in claude |
| average | marker | 6/- | 0.8, 2.8 | (none) | | | unmatched in claude |
| average | marker | 7/- | 0.6, 2.0 | (none) | | | unmatched in claude |
| average | marker | 8/- | 0.4, 2.1 | (none) | | | unmatched in claude |
| average | marker | 9/- | 0.3, 2.0 | (none) | | | unmatched in claude |
| average | marker | 10/- | 0.3, 2.0 | (none) | | | unmatched in claude |
| average | marker | 11/- | 0.2, 1.9 | (none) | | | unmatched in claude |
| average | marker | 12/- | 0.2, 1.9 | (none) | | | unmatched in claude |
| average | marker | 13/- | 0.1, 2.0 | (none) | | | unmatched in claude |
| average | marker | 14/- | 0.1, 1.8 | (none) | | | unmatched in claude |
| average | marker | 15/- | 0.1, 1.4 | (none) | | | unmatched in claude |
| average | trace | 9/interp | 0.2, 3.0 (0.0, 1.2) | 0.2, 1.5 (0.0, 0.3) | slope -1.0 | +1.5 (tol 1.5) | **disagree** |
| average | trace | 29/interp | 1.8, 29.4 (0.0, 0.2) | 1.8, 27.0 (0.0, 0.3) | slope +34.2 | +2.4 (tol 1.5) | **disagree** |
| average | trace | 30/interp | 1.8, 29.6 (0.0, 0.3) | 1.8, 27.1 (0.0, 0.3) | slope +34.1 | +2.5 (tol 1.6) | **disagree** |
| average | trace | 31/interp | 1.9, 35.0 (0.0, 0.2) | 1.9, 31.9 (0.0, 0.3) | slope +46.3 | +3.1 (tol 1.9) | **disagree** |
| average | trace | 33/interp | 2.0, 41.5 (0.0, 0.2) | 2.0, 37.5 (0.0, 0.3) | slope +62.4 | +4.1 (tol 2.3) | **disagree** |
| lower | feature | 1/1 | 0.1, 1.1 (0.0, 0.8) | 0.1, 0.7 (0.0, 0.2) | +0.0 | +0.4 | **disagree** |
| lower | feature | 2/4 | 3.9, 99.7 (0.1, 0.5) | 3.6, 98.8 (0.0, 0.3) | +0.2 | +0.9 | **disagree** |
| lower | feature | 3/3 | 2.5, 81.5 (0.0, 3.0) | 2.8, 94.8 (0.0, 0.3) | -0.4 | -13.3 | **disagree** |
| lower | feature | 4/2 | 0.9, 3.0 (0.0, 0.4) | 0.8, 2.0 (0.0, 0.3) | +0.1 | +1.0 | **disagree** |
| lower | marker | 1/- | 2.4, 68.0 | (none) | | | unmatched in claude |
| lower | marker | 2/- | 2.0, 38.1 | (none) | | | unmatched in claude |
| lower | marker | 3/- | 1.7, 23.3 | (none) | | | unmatched in claude |
| lower | marker | 4/- | 1.2, 8.0 | (none) | | | unmatched in claude |
| lower | marker | 5/- | 0.8, 2.7 | (none) | | | unmatched in claude |
| lower | marker | 6/- | 0.6, 0.6 | (none) | | | unmatched in claude |
| lower | trace | 9/interp | 0.2, 3.0 (0.0, 1.2) | 0.2, 0.8 (0.0, 0.3) | slope -1.0 | +2.2 (tol 1.5) | **disagree** |
| lower | trace | 10/interp | 0.2, 2.5 (0.0, 0.9) | 0.2, 0.9 (0.0, 0.3) | slope +2.9 | +1.7 (tol 1.2) | **disagree** |
| lower | trace | 22/interp | 0.8, 2.6 (0.0, 0.2) | 0.8, 1.9 (0.0, 0.3) | slope +5.7 | +0.6 (tol 0.6) | **disagree** |
| lower | trace | 32/interp | 2.0, 41.8 (0.0, 0.4) | 2.0, 36.5 (0.0, 0.3) | slope +61.6 | +5.3 (tol 3.8) | **disagree** |
| lower | trace | 33/interp | 2.0, 41.8 (0.0, 0.4) | 2.0, 36.5 (0.0, 0.3) | slope +61.6 | +5.3 (tol 3.8) | **disagree** |
| lower | trace | 35/interp | 2.2, 50.7 (0.0, 0.4) | 2.2, 45.3 (0.0, 0.3) | slope +67.5 | +5.4 (tol 4.1) | **disagree** |
| lower | trace | 36/interp | 2.2, 55.0 (0.0, 0.4) | 2.2, 48.8 (0.0, 0.3) | slope +65.9 | +6.2 (tol 4.3) | **disagree** |
| lower | trace | 50/- | 3.9, 99.7 (0.1, 0.5) | (no trace at this x) | | | unmatched in claude |
| upper | feature | 1/1 | 0.1, 1.1 (0.0, 0.8) | 0.1, 1.9 (0.0, 0.2) | +0.0 | -0.8 | **disagree** |
| upper | feature | 2/4 | 3.9, 99.7 (0.1, 0.5) | 4.6, 100.6 (0.0, 0.3) | -0.7 | -0.9 | **disagree** |
| upper | feature | 3/3 | 2.5, 81.5 (0.0, 3.0) | 2.8, 96.9 (0.0, 0.3) | -0.4 | -15.4 | **disagree** |
| upper | feature | 4/2 | 0.9, 4.7 (0.0, 0.4) | 0.8, 3.7 (0.0, 0.3) | +0.1 | +1.0 | **disagree** |
| upper | marker | 1/- | 2.4, 76.4 | (none) | | | unmatched in claude |
| upper | marker | 2/- | 1.7, 27.3 | (none) | | | unmatched in claude |
| upper | marker | 3/- | 1.2, 11.2 | (none) | | | unmatched in claude |
| upper | marker | 4/- | 0.8, 4.1 | (none) | | | unmatched in claude |
| upper | trace | 27/interp | 1.4, 15.1 (0.0, 0.2) | 1.4, 17.2 (0.0, 0.3) | slope +34.2 | -2.0 (tol 1.3) | **disagree** |
| upper | trace | 32/interp | 1.9, 43.9 (0.0, 0.1) | 1.9, 37.0 (0.0, 0.3) | slope +51.4 | +6.9 (tol 1.8) | **disagree** |
| upper | trace | 33/interp | 2.1, 53.8 (0.0, 0.1) | 2.1, 48.4 (0.0, 0.3) | slope +50.3 | +5.4 (tol 1.9) | **disagree** |
| upper | trace | 34/interp | 2.1, 53.8 (0.0, 0.1) | 2.1, 48.4 (0.0, 0.3) | slope +50.3 | +5.4 (tol 1.9) | **disagree** |
| upper | trace | 35/interp | 2.3, 61.8 (0.0, 0.1) | 2.3, 65.8 (0.0, 0.3) | slope +104.4 | -4.0 (tol 3.7) | **disagree** |
| upper | trace | 44/interp | 2.8, 95.4 (0.0, 0.4) | 2.8, 96.9 (0.0, 0.3) | slope +6.6 | -1.6 (tol 1.1) | **disagree** |
