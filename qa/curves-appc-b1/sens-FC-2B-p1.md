# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-2B\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-2B\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 42 | 42 |
| x per px | 0.1723 | 0.1722 |
| y per px | 3.4320 | 3.4321 |
| RMS residual x, y | 0.352, 4.200 | 0.351, 3.920 |

Corners of claude's box [730, 1060, 2240, 2860] mapped by both calibrations (tolerance 0.88 in x, 11.55 in y):

- (-3.9, 6090.8) vs (-3.9, 6090.6)
- (256.2, 6089.9) vs (256.2, 6090.5)
- (-5.1, -86.9) vs (-5.1, -87.2)
- (255.0, -87.7) vs (255.0, -87.2)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.19 | 0.27 | 0.26 | 18 | 0.60 | 0.50 | agree |
| x | 50 | 0.09 | 0.30 | 0.32 | 17 | 0.50 | 0.50 | agree |
| x | 100 | 0.04 | 0.35 | 0.35 | 17 | 0.52 | 0.57 | agree |
| x | 150 | 0.13 | 0.16 | 0.19 | 17 | 0.50 | 0.50 | agree |
| x | 200 | 0.10 | 0.30 | 0.36 | 17 | 0.91 | 0.80 | agree |
| x | 250 | 0.12 | 0.35 | 0.31 | 18 | 0.50 | 0.60 | agree |
| y | 0 | 0.03 | 0.18 | 0.15 | 15 | 0.93 | 0.88 | agree |
| y | 1000 | 1.03 | 0.64 | 0.05 | 15 | 1.84 | 0.56 | agree |
| y | 2000 | 0.12 | 0.35 | 0.40 | 15 | 0.93 | 1.03 | agree |
| y | 3000 | 0.05 | 0.14 | 0.11 | 15 | 0.50 | 0.50 | agree |
| y | 4000 | 0.02 | 0.30 | 0.32 | 15 | 0.69 | 0.71 | agree |
| y | 6000 | 0.19 | 0.44 | 0.41 | 15 | 0.84 | 0.67 | agree |

Both maps along every verified line and every interval midline (292 places): largest difference 0.02751 in x (tolerance 0.1909, claude 0), 4.026 in y (tolerance 9.881, claude 1000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 12 shared lines checked against the ink, mean of the median distances 0.32 px (claude: x 0.29, y 0.34), 0.27 px (codex: x 0.30, y 0.24), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

6 series in claude, 6 in codex.


## Points

Matched: 521; agreed 478; disagreed 43; unmatched 24 (kept as one-sided: 0 of claude, 23 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n2200 | feature | 3/3 | 247.8, 2659.3 (0.4, 8.8) | 249.9, 2659.3 (0.5, 9.7) | -2.0 | +0.0 | **disagree** |
| n2200 | marker | 1/1 | 9.8, 831.9 (0.2, 8.1) | 9.8, 813.0 (0.4, 7.9) | -0.0 | +18.9 | **disagree** |
| n2200 | marker | 2/2 | 21.3, 1124.7 (0.2, 8.2) | 21.5, 1102.3 (0.4, 8.0) | -0.2 | +22.5 | **disagree** |
| n2200 | marker | 3/3 | 31.6, 1332.3 (0.2, 7.9) | 31.4, 1313.7 (0.4, 8.2) | +0.2 | +18.5 | **disagree** |
| n2200 | marker | 5/5 | 60.6, 1809.8 (0.2, 7.1) | 60.3, 1788.5 (0.4, 8.6) | +0.4 | +21.3 | **disagree** |
| n2200 | marker | 6/6 | 70.7, 1913.7 (0.2, 7.0) | 71.0, 1892.5 (0.4, 8.7) | -0.3 | +21.2 | **disagree** |
| n2200 | marker | 8/8 | 90.7, 2150.7 (0.2, 6.6) | 90.9, 2129.8 (0.4, 8.5) | -0.2 | +20.9 | **disagree** |
| n2200 | marker | 9/9 | 110.1, 2321.6 (0.2, 6.5) | 110.5, 2304.2 (0.4, 8.3) | -0.3 | +17.4 | **disagree** |
| n2200 | marker | 12/12 | 139.9, 2536.8 (0.2, 6.3) | 140.0, 2512.7 (0.4, 8.2) | -0.2 | +24.1 | **disagree** |
| n2200 | marker | 14/14 | 160.8, 2625.6 (0.2, 6.3) | 161.1, 2604.9 (0.4, 8.1) | -0.3 | +20.6 | **disagree** |
| n2200 | marker | 15/15 | 191.3, 2714.3 (0.2, 6.2) | 191.3, 2693.7 (0.4, 8.0) | +0.0 | +20.6 | **disagree** |
| n2200 | marker | 16/16 | 221.1, 2714.1 (0.2, 6.2) | 220.9, 2693.6 (0.4, 8.0) | +0.2 | +20.5 | **disagree** |
| n2200 | marker | 17/17 | 249.9, 2662.7 (0.6, 8.0) | 250.5, 2642.2 (0.5, 9.8) | -0.7 | +20.5 | **disagree** |
| n2200 | trace | 41/interp | 153.3, 2543.6 (0.1, 4.6) | 153.3, 2581.5 (0.1, 28.7) | slope +7.4 | -37.9 (tol 35.3) | **disagree** |
| n2200 | trace | 44/interp | 163.2, 2591.4 (0.1, 4.6) | 163.2, 2631.1 (0.1, 28.6) | slope +2.2 | -39.8 (tol 33.8) | **disagree** |
| n2995 | feature | 1/1 | 10.3, 1028.1 (0.4, 11.8) | 11.4, 1078.0 (0.5, 9.7) | -1.1 | -49.9 | **disagree** |
| n2995 | feature | 3/3 | 248.6, 3332.7 (0.4, 11.2) | 250.3, 3344.7 (0.5, 9.5) | -1.7 | -12.1 | **disagree** |
| n2995 | marker | 3/3 | 31.8, 1772.0 (0.2, 5.4) | 31.3, 1757.4 (0.4, 8.5) | +0.5 | +14.6 | **disagree** |
| n2995 | marker | 6/6 | 60.9, 2362.8 (0.2, 4.7) | 60.4, 2345.4 (0.4, 8.3) | +0.5 | +17.4 | **disagree** |
| n2995 | marker | 8/8 | 80.8, 2602.1 (0.2, 4.6) | 80.5, 2588.2 (0.4, 8.1) | +0.3 | +13.9 | **disagree** |
| n2995 | marker | 11/11 | 111.4, 2868.6 (0.2, 4.4) | 110.8, 2865.1 (0.4, 7.8) | +0.7 | +3.5 | **disagree** |
| n2995 | marker | 13/13 | 160.9, 3215.9 (0.2, 4.3) | 160.9, 3202.3 (0.4, 7.7) | +0.0 | +13.5 | **disagree** |
| n2995 | marker | 15/15 | 221.5, 3351.6 (0.2, 4.4) | 220.7, 3348.3 (0.4, 7.8) | +0.8 | +3.3 | **disagree** |
| n3660 | feature | 1/1 | 10.0, 1080.0 (0.4, 11.8) | 10.4, 1178.5 (0.6, 11.5) | -0.4 | -98.5 | **disagree** |
| n3660 | feature | 3/3 | 246.6, 3927.9 (0.4, 6.3) | 250.0, 3922.9 (0.5, 9.7) | -3.4 | +5.0 | **disagree** |
| n3660 | feature | -/4 | (none) | 9.4, 1320.7 | | | unmatched in claude |
| n3660 | marker | 8/8 | 111.2, 3308.0 (0.2, 4.4) | 110.2, 3308.0 (0.4, 7.8) | +1.0 | -0.0 | **disagree** |
| n3660 | trace | 1/interp | 11.0, 1235.7 (0.7, 4.6) | 11.0, 1513.0 (0.4, 8.4) | slope +98.0 | -277.3 (tol 115.9) | **disagree** |
| n3660 | trace | 2/interp | 10.6, 1322.3 (0.4, 4.4) | 10.6, 1472.2 (0.4, 8.4) | slope +98.0 | -149.9 (tol 94.4) | **disagree** |
| n4400 | feature | 1/1 | 9.0, 1062.7 (0.4, 11.8) | 9.5, 1799.1 (0.5, 10.3) | -0.5 | -736.4 | **disagree** |
| n4400 | feature | 3/3 | 248.7, 4572.8 (0.4, 9.0) | 250.4, 4576.4 (0.5, 9.8) | -1.7 | -3.5 | **disagree** |
| n4400 | marker | 1/- | 10.9, 1176.9 | (none) | | | unmatched in codex |
| n4400 | trace | 1/interp | 10.8, 1253.0 (0.6, 4.5) | 10.8, 1862.3 (0.1, 29.4) | slope +48.0 | -609.3 (tol 67.9) | **disagree** |
| n4400 | trace | 2/interp | 10.6, 1339.6 (0.4, 4.4) | 10.6, 1850.7 (0.1, 29.4) | slope +48.0 | -511.1 (tol 61.5) | **disagree** |
| n4400 | trace | 3/interp | 11.1, 1426.1 (0.4, 4.3) | 11.1, 1876.5 (0.1, 29.4) | slope +48.0 | -450.4 (tol 61.3) | **disagree** |
| n4400 | trace | 4/interp | 12.0, 1512.6 (0.4, 4.1) | 12.0, 1912.7 (0.1, 26.9) | slope +23.9 | -400.1 (tol 44.8) | **disagree** |
| n4400 | trace | 5/interp | 13.5, 2005.7 (0.1, 20.7) | 13.5, 1948.2 (0.1, 15.6) | slope +41.0 | +57.5 (tol 47.5) | **disagree** |
| n4400 | trace | 6/interp | 14.9, 2077.5 (0.1, 20.4) | 14.9, 2010.5 (0.1, 23.9) | slope +67.5 | +67.0 (tol 62.8) | **disagree** |
| n734 | feature | 3/3 | 248.4, 1013.5 (0.4, 17.0) | 250.1, 1032.9 (0.5, 9.7) | -1.7 | -19.4 | **disagree** |
| n734 | feature | 2/2 | 227.3, 1061.0 (8.8, 8.6) | 181.5, 1032.9 (0.6, 11.4) | +45.8 | +28.1 | **disagree** |
| n734 | marker | 6/6 | 60.9, 672.8 (0.3, 7.8) | 60.0, 665.4 (0.6, 11.5) | +0.9 | +7.4 | **disagree** |
| n734 | marker | 13/13 | 131.1, 966.5 (0.3, 10.0) | 130.5, 988.0 (0.6, 11.3) | +0.5 | -21.5 | **disagree** |
| n734 | marker | 15/15 | 159.2, 979.6 (0.3, 10.0) | 161.1, 1012.1 (0.6, 11.4) | -1.9 | -32.6 | **disagree** |
| n734 | marker | 22/22 | 230.3, 1057.4 (0.3, 8.4) | 231.4, 1022.5 (0.6, 11.4) | -1.0 | +34.9 | **disagree** |
| n734 | marker | 23/23 | 241.0, 1053.7 (0.3, 8.4) | 240.2, 1022.5 (0.6, 11.4) | +0.8 | +31.2 | **disagree** |
| n4400 | marker | 1 (claude) | 10.9, 1176.9 | codex: n3660 (x) | | | **identity conflict** |
