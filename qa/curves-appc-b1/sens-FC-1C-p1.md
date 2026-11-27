# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-1C\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-1C\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 42 | 42 |
| x per px | 0.1705 | 0.1705 |
| y per px | 3.4555 | 3.4563 |
| RMS residual x, y | 0.415, 7.231 | 0.409, 7.910 |

Corners of claude's box [595, 1085, 2115, 2870] mapped by both calibrations (tolerance 0.99 in x, 18.60 in y):

- (-4.4, 6089.6) vs (-4.4, 6091.9)
- (254.7, 6081.8) vs (254.7, 6082.5)
- (-5.7, -78.5) vs (-5.8, -77.6)
- (253.4, -86.3) vs (253.4, -86.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.16 | 0.38 | 0.41 | 18 | 0.58 | 0.60 | agree |
| x | 50 | 0.19 | 0.31 | 0.31 | 17 | 0.52 | 0.50 | agree |
| x | 100 | 0.07 | 0.38 | 0.37 | 17 | 0.52 | 0.52 | agree |
| x | 150 | 0.18 | 0.34 | 0.40 | 17 | 0.59 | 0.63 | agree |
| x | 200 | 0.00 | 0.35 | 0.35 | 18 | 0.62 | 0.62 | agree |
| x | 250 | 0.08 | 0.25 | 0.26 | 18 | 0.76 | 0.57 | agree |
| y | 0 | 0.05 | 0.30 | 0.32 | 15 | 0.50 | 0.50 | agree |
| y | 1000 | 0.08 | 0.36 | 0.35 | 15 | 0.52 | 0.50 | agree |
| y | 2000 | 0.11 | 0.42 | 0.39 | 15 | 0.73 | 0.82 | agree |
| y | 3000 | 0.17 | 0.42 | 0.46 | 15 | 0.68 | 0.83 | agree |
| y | 4000 | 0.67 | 0.46 | 0.64 | 23 | 0.84 | 1.05 | agree |
| y | 6000 | 0.07 | 0.29 | 0.32 | 15 | 0.50 | 0.50 | agree |

Both maps along every verified line and every interval midline (280 places): largest difference 0.02816 in x (tolerance 0.1997, claude 50), 2.549 in y (tolerance 6.494, codex 4000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 12 shared lines checked against the ink, mean of the median distances 0.36 px (claude: x 0.34, y 0.37), 0.38 px (codex: x 0.35, y 0.41), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

7 series in claude, 7 in codex.


## Points

Matched: 403; agreed 379; disagreed 24; unmatched 37 (kept as one-sided: 0 of claude, 37 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1172 | feature | 3/3 | 248.4, 1446.8 (0.4, 11.5) | 249.8, 1450.2 (0.5, 9.8) | -1.4 | -3.4 | **disagree** |
| n1172 | marker | -/10 | (none) | 200.7, 1532.0 | | | unmatched in claude |
| n2345 | feature | -/4 | (none) | 111.3, 3083.4 | | | unmatched in claude |
| n2345 | feature | 3/3 | 251.5, 2741.3 (0.3, 6.5) | 250.6, 2748.0 (0.5, 10.2) | +0.9 | -6.7 | **disagree** |
| n2345 | feature | -/5 | (none) | 140.5, 3061.2 | | | unmatched in claude |
| n2345 | marker | 12/13 | 251.5, 2741.3 (0.3, 6.5) | 250.6, 2748.0 (0.5, 10.2) | +0.9 | -6.7 | **disagree** |
| n2345 | marker | -/11 | (none) | 202.4, 2971.1 | | | unmatched in claude |
| n2935 | feature | 1/1 | 62.7, 3498.7 (0.3, 6.5) | 58.6, 3451.2 (0.5, 12.0) | +4.1 | +47.5 | **disagree** |
| n2935 | marker | 2/2 | 81.3, 3735.2 (0.2, 4.8) | 81.9, 3736.0 (0.4, 8.6) | -0.7 | -0.8 | **disagree** |
| n2935 | marker | 3/3 | 100.7, 3930.4 (0.3, 6.6) | 102.0, 3924.7 (0.4, 8.7) | -1.4 | +5.7 | **disagree** |
| n2935 | marker | 7/7 | 180.1, 3906.4 (0.2, 4.9) | 180.8, 3908.1 (0.4, 8.7) | -0.7 | -1.7 | **disagree** |
| n2935 | marker | 8/8 | 198.4, 3871.2 (0.3, 6.6) | 200.2, 3866.0 (0.5, 10.4) | -1.7 | +5.2 | **disagree** |
| n2935 | marker | 9/9 | 220.0, 3873.8 (0.2, 4.9) | 220.7, 3875.6 (0.4, 8.7) | -0.7 | -1.9 | **disagree** |
| n294 | marker | 1/1 | 19.5, 441.2 (0.2, 4.3) | 18.8, 441.2 (0.4, 7.8) | +0.7 | -0.0 | **disagree** |
| n294 | marker | 3/3 | 60.7, 691.2 (0.2, 4.3) | 60.0, 691.2 (0.4, 7.7) | +0.7 | -0.0 | **disagree** |
| n3520 | marker | 9/9 | 132.1, 4275.7 (0.2, 4.8) | 133.6, 4277.0 (0.4, 8.5) | -1.6 | -1.3 | **disagree** |
| n587 | feature | 1/1 | 10.2, 537.7 (0.3, 6.0) | 10.5, 517.1 (0.5, 9.5) | -0.3 | +20.6 | **disagree** |
| n587 | feature | 3/3 | 248.3, 1030.3 (0.4, 11.4) | 249.7, 1033.4 (0.5, 9.6) | -1.4 | -3.1 | **disagree** |
| n587 | marker | 1/1 | 10.2, 537.7 (0.2, 4.3) | 10.5, 517.1 (0.4, 7.8) | -0.3 | +20.6 | **disagree** |
| n587 | marker | 2/2 | 32.0, 936.2 (0.3, 6.1) | 32.3, 919.0 (0.4, 7.8) | -0.3 | +17.2 | **disagree** |
| n587 | marker | 5/5 | 90.0, 1372.6 (0.2, 4.5) | 90.4, 1358.6 (0.4, 8.1) | -0.3 | +13.9 | **disagree** |
| n587 | marker | 6/6 | 109.6, 1351.0 (0.2, 4.5) | 109.9, 1330.1 (0.4, 8.0) | -0.3 | +20.9 | **disagree** |
| n587 | marker | 7/7 | 140.0, 1356.9 (0.2, 4.5) | 140.3, 1339.4 (0.4, 8.0) | -0.3 | +17.4 | **disagree** |
| n587 | marker | 8/8 | 150.8, 1363.4 (0.3, 6.3) | 151.2, 1346.0 (0.5, 9.8) | -0.3 | +17.4 | **disagree** |
| n587 | marker | 9/9 | 169.8, 1303.7 (0.2, 4.5) | 170.1, 1282.7 (0.4, 8.0) | -0.3 | +20.9 | **disagree** |
| n587 | marker | 10/10 | 190.6, 1181.3 (0.2, 4.5) | 190.9, 1160.3 (0.4, 7.9) | -0.3 | +21.0 | **disagree** |
| n587 | marker | 11/11 | 210.5, 1125.1 (0.2, 4.4) | 210.9, 1107.5 (0.4, 7.9) | -0.3 | +17.6 | **disagree** |
| n587 | marker | 12/12 | 230.4, 1114.1 (0.2, 4.4) | 230.5, 1086.1 (0.4, 7.9) | -0.2 | +28.0 | **disagree** |
