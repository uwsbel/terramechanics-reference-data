# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b3\rederived\claude\FC-6C\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b3\rederived\codex\FC-6C\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 36 | 36 |
| x per px | 0.1712 | 0.1712 |
| y per px | 3.4033 | 3.4031 |
| RMS residual x, y | 0.639, 9.299 | 0.640, 9.750 |

Corners of claude's box [625, 925, 2150, 2435] mapped by both calibrations (tolerance 1.45 in x, 22.45 in y):

- (-3.1, 5086.9) vs (-3.1, 5087.2)
- (258.0, 5042.2) vs (258.0, 5041.1)
- (-6.0, -51.9) vs (-6.0, -51.2)
- (255.2, -96.6) vs (255.2, -97.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.15 | 0.31 | 0.33 | 15 | 0.51 | 0.59 | agree |
| x | 50 | 0.31 | 0.48 | 0.42 | 13 | 0.77 | 1.16 | agree |
| x | 100 | 0.02 | 0.27 | 0.27 | 12 | 0.63 | 0.58 | agree |
| x | 150 | 0.08 | 0.17 | 0.18 | 11 | 0.50 | 0.50 | agree |
| x | 200 | 0.07 | 0.28 | 0.29 | 13 | 0.82 | 0.73 | agree |
| x | 250 | 0.38 | 0.19 | 0.25 | 15 | 0.50 | 0.58 | agree |
| y | 0 | 0.07 | 0.19 | 0.20 | 15 | 0.56 | 0.55 | agree |
| y | 1000 | 0.28 | 0.25 | 0.26 | 15 | 0.74 | 0.50 | agree |
| y | 2000 | 0.06 | 0.57 | 0.53 | 15 | 1.11 | 1.05 | agree |
| y | 3000 | 3.32 | 0.65 | 0.69 | 23 | 2.43 | 2.37 | agree |
| y | 4000 | 0.36 | 0.49 | 0.60 | 15 | 1.44 | 1.25 | agree |
| y | 5000 | 0.12 | 0.35 | 0.32 | 15 | 0.51 | 0.57 | agree |

Both maps along every verified line and every interval midline (246 places): largest difference 0.07291 in x (tolerance 0.2712, claude 250), 9.907 in y (tolerance 16.36, codex 3000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 12 shared lines checked against the ink, mean of the median distances 0.35 px (claude: x 0.28, y 0.42), 0.36 px (codex: x 0.29, y 0.43), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 374; agreed 351; disagreed 23; unmatched 20 (kept as one-sided: 7 of claude, 13 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1961 | feature | 1/88 | 11.2, 873.9 (0.3, 6.4) | 10.4, 893.6 (0.2, 1.7) | +0.8 | -19.7 | **disagree** |
| n1961 | feature | 3/90 | 247.5, 1326.2 (0.2, 11.5) | 246.3, 1324.0 (0.2, 9.6) | +1.2 | +2.2 | **disagree** |
| n1961 | marker | 6/6 | 97.2, 1364.1 (0.3, 6.6) | 98.7, 1372.5 (0.6, 11.4) | -1.6 | -8.3 | **disagree** |
| n1961 | marker | 9/9 | 168.0, 1399.4 (0.2, 4.9) | 169.7, 1395.6 (0.6, 11.4) | -1.7 | +3.8 | **disagree** |
| n1961 | marker | 11/11 | 217.9, 1352.1 (0.2, 4.9) | 219.5, 1348.0 (0.6, 11.3) | -1.6 | +4.1 | **disagree** |
| n1961 | marker | 12/12 | 250.4, 1335.8 (0.3, 6.5) | 249.2, 1323.5 (0.7, 13.0) | +1.2 | +12.3 | **disagree** |
| n1961 | trace | 61/- | 246.6, 1328.0 (0.1, 10.7) | (no trace at this x) | | | unmatched in codex |
| n1961 | trace | 62/- | 247.5, 1326.2 (0.2, 11.5) | (no trace at this x) | | | unmatched in codex |
| n2934 | feature | 1/82 | 11.8, 1179.5 (0.3, 6.5) | 11.2, 1187.1 (0.2, 9.5) | +0.6 | -7.6 | **disagree** |
| n2934 | feature | 3/84 | 253.4, 2856.5 (0.2, 10.6) | 245.0, 2889.0 (0.2, 12.5) | +8.3 | -32.5 | **disagree** |
| n2934 | marker | 10/10 | 186.9, 2925.2 (0.2, 7.4) | 186.9, 2956.9 (0.6, 14.4) | -0.0 | -31.7 | **disagree** |
| n2934 | trace | 61/- | 245.2, 2876.9 (0.1, 9.0) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 62/- | 253.4, 2856.5 (0.2, 10.6) | (no trace at this x) | | | unmatched in codex |
| n3815 | feature | 3/83 | 245.4, 3019.1 (0.2, 12.7) | 244.9, 3022.2 (0.2, 12.4) | +0.5 | -3.1 | **disagree** |
| n3815 | marker | 8/8 | 147.0, 3012.5 (0.2, 7.5) | 149.2, 3026.3 (0.2, 7.4) | -2.2 | -13.8 | **disagree** |
| n3815 | marker | 9/9 | 167.0, 3007.9 (0.2, 9.2) | 167.0, 3025.0 (0.2, 7.4) | +0.0 | -17.0 | **disagree** |
| n3815 | marker | 10/10 | 187.5, 3003.2 (0.2, 9.2) | 187.4, 3030.0 (0.2, 7.3) | +0.1 | -26.7 | **disagree** |
| n3815 | marker | 11/11 | 217.6, 3016.8 (0.2, 9.3) | 217.4, 3036.8 (0.2, 7.3) | +0.2 | -20.0 | **disagree** |
| n3815 | trace | 60/- | 245.4, 3019.1 (0.2, 12.7) | (no trace at this x) | | | unmatched in codex |
| n4695 | feature | 1/80 | 10.3, 2059.9 (0.3, 7.3) | 10.4, 2080.3 (0.2, 10.6) | -0.1 | -20.4 | **disagree** |
| n4695 | marker | 2/2 | 19.9, 2564.1 (0.2, 6.7) | 19.9, 2549.2 (0.2, 6.5) | -0.0 | +14.8 | **disagree** |
| n4695 | marker | 5/5 | 98.3, 3846.1 (0.3, 6.1) | 98.9, 3844.2 (0.2, 5.8) | -0.6 | +1.9 | **disagree** |
| n4695 | marker | 8/8 | 168.1, 3996.5 (0.2, 7.7) | 167.2, 3997.4 (0.2, 5.7) | +0.9 | -1.0 | **disagree** |
| n4695 | marker | 9/9 | 187.4, 4019.2 (0.2, 6.0) | 186.6, 4025.3 (0.2, 5.7) | +0.8 | -6.1 | **disagree** |
| n4695 | marker | 10/10 | 217.7, 4038.4 (0.2, 7.7) | 216.5, 4023.5 (0.2, 5.7) | +1.2 | +14.9 | **disagree** |
| n4695 | marker | 11/11 | 248.0, 4031.5 (0.2, 6.0) | 249.1, 4000.3 (0.7, 14.5) | -1.1 | +31.2 | **disagree** |
| n4695 | trace | 1/- | 10.3, 2059.9 (0.3, 7.3) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 33/interp | 133.6, 3954.9 (0.1, 11.0) | 133.6, 3994.5 (0.1, 12.4) | slope +13.4 | -39.6 (tol 27.1) | **disagree** |
| n714 | feature | 3/82 | 247.3, 731.5 (0.2, 11.4) | 245.8, 732.8 (0.2, 9.4) | +1.5 | -1.3 | **disagree** |
| n714 | trace | 61/- | 247.3, 731.5 (0.2, 11.4) | (no trace at this x) | | | unmatched in codex |
