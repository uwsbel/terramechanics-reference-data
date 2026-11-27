# Curve diff: claude vs codex

Files: `<repository>\qa\curves-pilot-b1\rederived\claude\FC-1B\points-p1-native.csv` (claude), `<repository>\qa\curves-pilot-b1\rederived\codex\FC-1B\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 42 | 42 |
| x per px | 0.1705 | 0.1701 |
| y per px | 3.4804 | 3.4791 |
| RMS residual x, y | 0.594, 10.155 | 0.174, 9.239 |

Corners of claude's box [780, 1100, 2300, 2900] mapped by both calibrations (tolerance 0.94 in x, 22.88 in y):

- (1.9, 6100.8) vs (2.7, 6100.3)
- (261.0, 6011.6) vs (261.1, 6009.4)
- (-3.9, -163.0) vs (-3.7, -161.2)
- (255.2, -252.2) vs (254.8, -252.0)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.14 | 0.17 | 0.17 | 23 | 0.50 | 0.73 | agree |
| x | 50 | 0.15 | 0.24 | 0.31 | 24 | 0.50 | 0.73 | agree |
| x | 100 | 0.09 | 0.16 | 0.13 | 18 | 0.62 | 0.50 | agree |
| x | 150 | 0.10 | 0.17 | 0.16 | 18 | 0.64 | 0.56 | agree |
| x | 200 | 0.32 | 0.18 | 0.20 | 18 | 0.50 | 0.50 | agree |
| x | 250 | 0.74 | 0.48 | 0.60 | 18 | 0.92 | 1.02 | agree |
| y | 0 | 0.19 | 0.44 | 0.31 | 15 | 0.75 | 0.62 | agree |
| y | 1000 | 0.72 | 0.56 | 0.76 | 15 | 1.11 | 1.43 | agree |
| y | 2000 | 0.12 | 0.49 | 0.52 | 15 | 1.39 | 1.06 | agree |
| y | 3000 | 0.38 | 0.58 | 0.56 | 15 | 0.86 | 1.13 | agree |
| y | 4000 | 0.41 | 0.51 | 0.38 | 23 | 1.06 | 0.80 | agree |
| y | 6000 | 0.46 | 0.36 | 0.30 | 18 | 0.79 | 0.50 | agree |

Both maps along every verified line and every interval midline (233 places): largest difference 0.1072 in x (tolerance 0.3314, codex 250), 2.455 in y (tolerance 8.876, claude 1000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 12 shared lines checked against the ink, mean of the median distances 0.36 px (claude: x 0.23, y 0.49), 0.37 px (codex: x 0.26, y 0.47), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

7 series in claude, 7 in codex.


## Points

Matched: 276; agreed 263; disagreed 13; unmatched 138 (kept as one-sided: 13 of claude, 125 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1172 | feature | -/2 | (none) | 9.6, 738.5 | | | unmatched in claude |
| n1172 | feature | -/86 | (none) | 250.6, 1535.0 | | | unmatched in claude |
| n1172 | feature | -/38 | (none) | 114.9, 1745.2 | | | unmatched in claude |
| n1172 | marker | -/1 | (none) | 9.6, 738.5 | | | unmatched in claude |
| n1172 | marker | -/8 | (none) | 29.2, 1133.8 | | | unmatched in claude |
| n1172 | marker | -/15 | (none) | 50.1, 1453.7 | | | unmatched in claude |
| n1172 | marker | -/22 | (none) | 69.8, 1588.9 | | | unmatched in claude |
| n1172 | marker | -/29 | (none) | 90.5, 1690.0 | | | unmatched in claude |
| n1172 | marker | -/36 | (none) | 110.5, 1723.7 | | | unmatched in claude |
| n1172 | marker | -/43 | (none) | 129.5, 1718.7 | | | unmatched in claude |
| n1172 | marker | -/50 | (none) | 150.1, 1684.7 | | | unmatched in claude |
| n1172 | marker | -/57 | (none) | 169.7, 1677.6 | | | unmatched in claude |
| n1172 | marker | -/64 | (none) | 190.1, 1659.6 | | | unmatched in claude |
| n1172 | marker | -/68 | (none) | 200.0, 1627.5 | | | unmatched in claude |
| n1172 | marker | -/75 | (none) | 219.7, 1595.7 | | | unmatched in claude |
| n1172 | marker | -/85 | (none) | 250.6, 1535.0 | | | unmatched in claude |
| n1172 | trace | 10/- | 8.2, 725.9 (0.1, 12.0) | (no trace at this x) | | | unmatched in codex |
| n1172 | trace | 15/- | 13.3, 816.4 (0.1, 12.1) | (no trace at this x) | | | unmatched in codex |
| n1172 | trace | 30/interp | 29.1, 1177.1 (0.1, 7.5) | 29.1, 1108.4 (0.2, 36.4) | slope +20.7 | +68.8 (tol 50.2) | **disagree** |
| n1172 | trace | 90/interp | 89.0, 1740.1 (0.1, 7.7) | 89.0, 1699.6 (0.2, 28.8) | slope +4.0 | +40.5 (tol 37.8) | **disagree** |
| n1760 | feature | -/2 | (none) | 20.4, 1439.4 | | | unmatched in claude |
| n1760 | feature | -/85 | (none) | 248.8, 2098.3 | | | unmatched in claude |
| n1760 | feature | -/41 | (none) | 129.4, 2411.5 | | | unmatched in claude |
| n1760 | marker | -/1 | (none) | 20.4, 1439.4 | | | unmatched in claude |
| n1760 | marker | -/9 | (none) | 40.5, 1798.7 | | | unmatched in claude |
| n1760 | marker | -/16 | (none) | 59.7, 2064.1 | | | unmatched in claude |
| n1760 | marker | -/24 | (none) | 81.4, 2257.9 | | | unmatched in claude |
| n1760 | marker | -/31 | (none) | 102.5, 2361.7 | | | unmatched in claude |
| n1760 | marker | -/37 | (none) | 121.1, 2410.9 | | | unmatched in claude |
| n1760 | marker | -/45 | (none) | 140.5, 2341.6 | | | unmatched in claude |
| n1760 | marker | -/53 | (none) | 160.6, 2341.6 | | | unmatched in claude |
| n1760 | marker | -/60 | (none) | 181.9, 2254.0 | | | unmatched in claude |
| n1760 | marker | -/67 | (none) | 200.9, 2233.4 | | | unmatched in claude |
| n1760 | marker | -/74 | (none) | 220.3, 2195.3 | | | unmatched in claude |
| n1760 | marker | -/84 | (none) | 248.8, 2098.3 | | | unmatched in claude |
| n1760 | trace | 20/- | 19.2, 1441.0 (0.1, 9.4) | (no trace at this x) | | | unmatched in codex |
| n2345 | feature | -/2 | (none) | 9.9, 1083.7 | | | unmatched in claude |
| n2345 | feature | -/84 | (none) | 250.9, 2675.6 | | | unmatched in claude |
| n2345 | feature | -/68 | (none) | 200.6, 2748.5 | | | unmatched in claude |
| n2345 | feature | -/70 | (none) | 214.5, 2785.5 | | | unmatched in claude |
| n2345 | feature | -/53 | (none) | 159.1, 2848.0 | | | unmatched in claude |
| n2345 | marker | -/1 | (none) | 9.9, 1083.7 | | | unmatched in claude |
| n2345 | marker | -/9 | (none) | 31.4, 1617.0 | | | unmatched in claude |
| n2345 | marker | -/15 | (none) | 51.8, 2053.1 | | | unmatched in claude |
| n2345 | marker | -/25 | (none) | 81.1, 2522.0 | | | unmatched in claude |
| n2345 | marker | -/29 | (none) | 90.3, 2612.6 | | | unmatched in claude |
| n2345 | marker | -/36 | (none) | 111.1, 2709.7 | | | unmatched in claude |
| n2345 | marker | -/43 | (none) | 130.4, 2793.5 | | | unmatched in claude |
| n2345 | marker | -/49 | (none) | 151.3, 2821.1 | | | unmatched in claude |
| n2345 | marker | -/57 | (none) | 170.2, 2807.7 | | | unmatched in claude |
| n2345 | marker | -/64 | (none) | 190.7, 2814.5 | | | unmatched in claude |
| n2345 | marker | -/69 | (none) | 211.1, 2816.2 | | | unmatched in claude |
| n2345 | marker | -/79 | (none) | 240.3, 2729.7 | | | unmatched in claude |
| n2345 | marker | -/83 | (none) | 250.9, 2675.6 | | | unmatched in claude |
| n2345 | trace | 10/- | 8.5, 1115.0 (0.1, 10.1) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 30/interp | 29.5, 1667.2 (0.1, 8.6) | 29.5, 1596.6 (0.2, 45.0) | slope +23.2 | +70.6 (tol 61.0) | **disagree** |
| n2345 | trace | 45/interp | 45.0, 1936.1 (0.1, 15.8) | 45.0, 1864.9 (0.2, 44.8) | slope +15.2 | +71.2 (tol 65.6) | **disagree** |
| n2345 | trace | 130/interp | 129.9, 2842.7 (0.1, 6.0) | 129.9, 2799.9 (0.2, 28.0) | slope +3.0 | +42.7 (tol 35.0) | **disagree** |
| n2345 | trace | 170/interp | 169.9, 2764.4 (0.1, 7.0) | 169.9, 2838.4 (0.2, 28.0) | slope -1.0 | -74.0 (tol 35.3) | **disagree** |
| n2345 | trace | 180/interp | 179.9, 2760.9 (0.1, 7.0) | 179.9, 2822.6 (0.2, 43.7) | slope -2.4 | -61.7 (tol 51.4) | **disagree** |
| n2345 | trace | 210/- | 209.9, 2771.2 (0.1, 7.0) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 215/- | 214.9, 2797.3 (0.1, 8.7) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 240/interp | 239.9, 2773.0 (0.2, 6.1) | 239.9, 2712.4 (0.2, 28.1) | slope -5.1 | +60.6 (tol 36.0) | **disagree** |
| n2935 | feature | -/2 | (none) | 19.9, 1825.8 | | | unmatched in claude |
| n2935 | feature | -/86 | (none) | 252.6, 3333.5 | | | unmatched in claude |
| n2935 | feature | -/50 | (none) | 155.3, 3409.6 | | | unmatched in claude |
| n2935 | feature | -/77 | (none) | 229.5, 3315.2 | | | unmatched in claude |
| n2935 | marker | -/1 | (none) | 19.9, 1825.8 | | | unmatched in claude |
| n2935 | marker | -/9 | (none) | 41.5, 2339.6 | | | unmatched in claude |
| n2935 | marker | -/17 | (none) | 61.8, 2721.4 | | | unmatched in claude |
| n2935 | marker | -/23 | (none) | 80.7, 2994.5 | | | unmatched in claude |
| n2935 | marker | -/30 | (none) | 102.2, 3201.4 | | | unmatched in claude |
| n2935 | marker | -/37 | (none) | 121.0, 3307.4 | | | unmatched in claude |
| n2935 | marker | -/44 | (none) | 141.8, 3366.9 | | | unmatched in claude |
| n2935 | marker | -/53 | (none) | 161.7, 3407.3 | | | unmatched in claude |
| n2935 | marker | -/63 | (none) | 191.1, 3367.1 | | | unmatched in claude |
| n2935 | marker | -/70 | (none) | 209.9, 3334.2 | | | unmatched in claude |
| n2935 | marker | -/79 | (none) | 231.7, 3319.7 | | | unmatched in claude |
| n2935 | marker | -/85 | (none) | 252.6, 3333.5 | | | unmatched in claude |
| n2935 | trace | 20/- | 19.5, 1826.0 (0.1, 16.7) | (no trace at this x) | | | unmatched in codex |
| n294 | feature | -/2 | (none) | 9.3, 211.8 | | | unmatched in claude |
| n294 | feature | -/86 | (none) | 249.6, 532.5 | | | unmatched in claude |
| n294 | feature | -/32 | (none) | 97.6, 598.6 | | | unmatched in claude |
| n294 | marker | -/1 | (none) | 9.3, 211.8 | | | unmatched in claude |
| n294 | marker | -/8 | (none) | 30.1, 382.4 | | | unmatched in claude |
| n294 | marker | -/15 | (none) | 50.4, 488.3 | | | unmatched in claude |
| n294 | marker | -/22 | (none) | 69.9, 546.6 | | | unmatched in claude |
| n294 | marker | -/29 | (none) | 90.3, 575.5 | | | unmatched in claude |
| n294 | marker | -/37 | (none) | 109.7, 582.5 | | | unmatched in claude |
| n294 | marker | -/43 | (none) | 129.5, 572.3 | | | unmatched in claude |
| n294 | marker | -/51 | (none) | 149.4, 550.0 | | | unmatched in claude |
| n294 | marker | -/58 | (none) | 169.2, 536.3 | | | unmatched in claude |
| n294 | marker | -/65 | (none) | 189.2, 539.6 | | | unmatched in claude |
| n294 | marker | -/72 | (none) | 209.1, 539.6 | | | unmatched in claude |
| n294 | marker | -/79 | (none) | 229.1, 532.7 | | | unmatched in claude |
| n294 | marker | -/85 | (none) | 249.6, 532.5 | | | unmatched in claude |
| n294 | trace | 10/- | 7.6, 181.1 (0.1, 14.2) | (no trace at this x) | | | unmatched in codex |
| n294 | trace | 15/- | 12.7, 235.7 (0.1, 11.7) | (no trace at this x) | | | unmatched in codex |
| n3520 | feature | -/2 | (none) | 20.2, 2123.2 | | | unmatched in claude |
| n3520 | feature | -/80 | (none) | 250.6, 3917.5 | | | unmatched in claude |
| n3520 | feature | -/65 | (none) | 209.7, 4059.1 | | | unmatched in claude |
| n3520 | marker | -/1 | (none) | 20.2, 2123.2 | | | unmatched in claude |
| n3520 | marker | -/15 | (none) | 59.4, 3110.8 | | | unmatched in claude |
| n3520 | marker | -/22 | (none) | 81.0, 3453.2 | | | unmatched in claude |
| n3520 | marker | -/35 | (none) | 121.6, 3800.8 | | | unmatched in claude |
| n3520 | marker | -/49 | (none) | 161.6, 3981.3 | | | unmatched in claude |
| n3520 | marker | -/61 | (none) | 201.8, 4067.1 | | | unmatched in claude |
| n3520 | marker | -/70 | (none) | 221.8, 4046.2 | | | unmatched in claude |
| n3520 | marker | -/79 | (none) | 250.6, 3917.5 | | | unmatched in claude |
| n3520 | trace | 20/- | 19.8, 2118.7 (0.1, 12.8) | (no trace at this x) | | | unmatched in codex |
| n587 | feature | -/2 | (none) | 20.2, 775.9 | | | unmatched in claude |
| n587 | feature | -/85 | (none) | 249.6, 741.8 | | | unmatched in claude |
| n587 | feature | -/75 | (none) | 223.4, 754.1 | | | unmatched in claude |
| n587 | feature | -/26 | (none) | 91.7, 1113.3 | | | unmatched in claude |
| n587 | marker | -/1 | (none) | 20.2, 775.9 | | | unmatched in claude |
| n587 | marker | -/8 | (none) | 40.0, 988.1 | | | unmatched in claude |
| n587 | marker | -/15 | (none) | 59.9, 1074.8 | | | unmatched in claude |
| n587 | marker | -/22 | (none) | 79.5, 1091.0 | | | unmatched in claude |
| n587 | marker | -/30 | (none) | 100.0, 1082.0 | | | unmatched in claude |
| n587 | marker | -/36 | (none) | 119.2, 1073.5 | | | unmatched in claude |
| n587 | marker | -/43 | (none) | 139.8, 1059.1 | | | unmatched in claude |
| n587 | marker | -/51 | (none) | 160.0, 955.8 | | | unmatched in claude |
| n587 | marker | -/58 | (none) | 179.9, 889.0 | | | unmatched in claude |
| n587 | marker | -/66 | (none) | 200.0, 799.8 | | | unmatched in claude |
| n587 | marker | -/73 | (none) | 219.3, 789.8 | | | unmatched in claude |
| n587 | marker | -/84 | (none) | 249.6, 741.8 | | | unmatched in claude |
| n587 | trace | 10/- | 8.2, 784.0 (0.1, 6.9) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 20/- | 18.5, 761.6 (0.1, 23.2) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 25/- | 23.7, 833.3 (0.1, 12.1) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 60/interp | 59.0, 1105.7 (0.1, 14.6) | 59.0, 1050.8 (0.2, 29.2) | slope +5.0 | +54.9 (tol 45.3) | **disagree** |
| n587 | trace | 105/interp | 103.1, 1045.3 (0.1, 10.1) | 103.1, 1108.5 (0.2, 29.2) | slope -0.0 | -63.2 (tol 39.3) | **disagree** |
| n587 | trace | 160/interp | 157.9, 934.0 (0.2, 19.0) | 157.9, 984.7 (0.2, 29.0) | slope -4.6 | -50.7 (tol 49.5) | **disagree** |
| n587 | trace | 165/interp | 162.9, 916.9 (0.1, 7.9) | 162.9, 961.1 (0.2, 28.7) | slope -4.7 | -44.3 (tol 38.0) | **disagree** |
| n587 | trace | 180/interp | 177.9, 841.5 (0.1, 7.0) | 177.9, 895.9 (0.2, 28.1) | slope -5.1 | -54.4 (tol 36.6) | **disagree** |
