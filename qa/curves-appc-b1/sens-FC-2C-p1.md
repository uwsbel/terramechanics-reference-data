# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-2C\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-2C\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 42 | 42 |
| x per px | 0.1713 | 0.1713 |
| y per px | 3.4462 | 3.4460 |
| RMS residual x, y | 0.471, 2.770 | 0.465, 2.678 |

Corners of claude's box [670, 1050, 2175, 2835] mapped by both calibrations (tolerance 1.11 in x, 8.89 in y):

- (-3.7, 6057.9) vs (-3.7, 6056.8)
- (254.1, 6078.6) vs (254.1, 6078.8)
- (-3.5, -93.5) vs (-3.5, -94.3)
- (254.4, -72.8) vs (254.4, -72.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.03 | 0.16 | 0.16 | 18 | 0.50 | 0.50 | agree |
| x | 50 | 0.01 | 0.16 | 0.15 | 18 | 0.50 | 0.50 | agree |
| x | 100 | 0.36 | 0.25 | 0.37 | 17 | 1.01 | 0.62 | agree |
| x | 150 | 0.07 | 0.31 | 0.32 | 16 | 0.52 | 0.60 | agree |
| x | 200 | 0.15 | 0.37 | 0.33 | 18 | 0.62 | 0.62 | agree |
| x | 250 | 0.04 | 0.33 | 0.34 | 18 | 0.50 | 0.50 | agree |
| y | 0 | 0.05 | 0.18 | 0.18 | 15 | 0.50 | 0.50 | agree |
| y | 1000 | 0.14 | 0.16 | 0.22 | 15 | 0.50 | 0.65 | agree |
| y | 2000 | 0.05 | 0.40 | 0.37 | 15 | 0.50 | 0.53 | agree |
| y | 3000 | 0.21 | 0.23 | 0.27 | 15 | 0.50 | 0.64 | agree |
| y | 4000 | 1.09 | 0.45 | 0.46 | 13 | 1.28 | 1.05 | agree |
| y | 5000 | 0.22 | 0.59 | 0.53 | 14 | 0.98 | 0.78 | agree |
| y | 6000 | 0.22 | 0.37 | 0.34 | 15 | 0.63 | 0.50 | agree |

Both maps along every verified line and every interval midline (312 places): largest difference 0.06605 in x (tolerance 0.2753, claude 100), 3.234 in y (tolerance 8.049, claude 4000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 13 shared lines checked against the ink, mean of the median distances 0.30 px (claude: x 0.26, y 0.34), 0.31 px (codex: x 0.28, y 0.34), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

6 series in claude, 6 in codex.


## Points

Matched: 229; agreed 185; disagreed 44; unmatched 18 (kept as one-sided: 3 of claude, 15 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1468 | feature | 3/3 | 81.2, 2025.4 (0.5, 9.5) | 79.2, 2032.0 (0.5, 9.5) | +2.1 | -6.6 | **disagree** |
| n1468 | marker | 2/2 | 3.6, 853.3 (0.2, 4.3) | 3.8, 839.1 (0.4, 8.0) | -0.2 | +14.2 | **disagree** |
| n1468 | marker | 3/3 | 10.0, 1222.6 (0.2, 4.3) | 10.0, 1208.4 (0.4, 8.0) | -0.0 | +14.2 | **disagree** |
| n1468 | marker | 4/4 | 21.4, 1565.3 (0.2, 4.3) | 21.0, 1551.1 (0.4, 7.9) | +0.3 | +14.1 | **disagree** |
| n1468 | marker | 5/5 | 36.2, 1808.0 (0.2, 4.3) | 36.2, 1794.0 (0.4, 7.9) | -0.0 | +14.0 | **disagree** |
| n1468 | marker | 6/6 | 50.5, 1936.9 (0.3, 6.1) | 50.0, 1919.4 (0.5, 9.6) | +0.5 | +17.5 | **disagree** |
| n1468 | trace | 1/interp | 2.7, 454.7 (0.2, 11.2) | 2.7, 665.0 (0.1, 28.6) | slope +179.1 | -210.4 (tol 102.5) | **disagree** |
| n2200 | feature | 3/3 | 133.3, 3028.3 (0.4, 7.9) | 133.0, 2999.9 (0.5, 9.8) | +0.3 | +28.4 | **disagree** |
| n2200 | feature | 2/2 | 124.9, 3034.6 (0.4, 7.9) | 119.9, 3002.4 (0.5, 9.8) | +5.0 | +32.2 | **disagree** |
| n2200 | marker | 6/- | 47.4, 2386.5 | (none) | | | unmatched in codex |
| n2200 | marker | 1/1 | 7.4, 1294.9 (0.2, 4.3) | 6.9, 1308.3 (0.4, 8.0) | +0.5 | -13.4 | **disagree** |
| n2200 | marker | 2/2 | 16.8, 1592.5 (0.2, 4.3) | 16.1, 1602.5 (0.4, 7.9) | +0.7 | -10.0 | **disagree** |
| n2200 | marker | 3/3 | 22.2, 1741.4 (0.2, 4.3) | 21.4, 1754.9 (0.4, 7.9) | +0.9 | -13.5 | **disagree** |
| n2200 | marker | 5/5 | 42.0, 2307.2 (0.2, 4.3) | 41.3, 2317.1 (0.4, 7.9) | +0.7 | -9.9 | **disagree** |
| n2200 | marker | 8/7 | 82.1, 2828.4 (0.2, 4.3) | 81.4, 2841.6 (0.4, 8.0) | +0.7 | -13.2 | **disagree** |
| n2200 | trace | 3/interp | 17.8, 1668.5 (0.2, 7.8) | 17.8, 1616.3 (0.1, 28.6) | slope +32.7 | +52.3 (tol 47.9) | **disagree** |
| n2200 | trace | 4/interp | 22.9, 1823.6 (0.2, 9.5) | 22.9, 1766.3 (0.1, 28.6) | slope +45.9 | +57.3 (tol 54.2) | **disagree** |
| n2200 | trace | 7/interp | 38.3, 2190.2 (0.2, 6.0) | 38.3, 2220.1 (0.1, 13.8) | slope +23.8 | -29.9 (tol 28.2) | **disagree** |
| n2200 | trace | 23/interp | 117.6, 3030.5 (0.3, 7.9) | 117.6, 2997.0 (0.1, 15.0) | slope +0.1 | +33.5 (tol 23.0) | **disagree** |
| n2200 | trace | 25/interp | 128.0, 3031.4 (0.2, 7.9) | 128.0, 2998.4 (0.1, 15.0) | slope -0.8 | +33.0 (tol 23.2) | **disagree** |
| n2200 | trace | 26/- | 132.8, 3028.3 (0.2, 7.9) | (no trace at this x) | | | unmatched in codex |
| n2995 | marker | 5/5 | 51.3, 3606.3 (0.3, 7.0) | 51.7, 3586.9 (0.5, 10.3) | -0.3 | +19.4 | **disagree** |
| n2995 | marker | 12/12 | 150.0, 4041.2 (0.3, 7.4) | 149.7, 4019.7 (0.6, 12.2) | +0.3 | +21.5 | **disagree** |
| n2995 | trace | 11/interp | 63.6, 3730.0 (0.2, 12.3) | 63.6, 3777.8 (0.1, 29.5) | slope +3.0 | -47.8 (tol 42.9) | **disagree** |
| n3660 | marker | 2/2 | 11.0, 2826.5 (0.2, 4.3) | 10.9, 2839.6 (0.4, 8.0) | +0.2 | -13.1 | **disagree** |
| n3660 | marker | 4/4 | 31.6, 3486.6 (0.2, 5.0) | 31.1, 3501.9 (0.4, 8.4) | +0.5 | -15.3 | **disagree** |
| n3660 | marker | 6/6 | 51.2, 3902.0 (0.3, 7.4) | 50.6, 3940.8 (0.6, 12.3) | +0.5 | -38.8 | **disagree** |
| n4400 | feature | 3/3 | 170.4, 5141.9 (0.5, 10.2) | 168.8, 5142.3 (0.5, 9.9) | +1.5 | -0.4 | **disagree** |
| n4400 | marker | 1/1 | 20.8, 3426.7 (0.2, 5.0) | 19.8, 3428.1 (0.4, 8.4) | +1.0 | -1.4 | **disagree** |
| n4400 | marker | 2/2 | 32.1, 3848.4 (0.2, 5.5) | 31.3, 3845.3 (0.4, 8.7) | +0.9 | +3.1 | **disagree** |
| n4400 | marker | 3/3 | 41.4, 4098.2 (0.2, 5.6) | 40.5, 4112.6 (0.4, 8.7) | +0.9 | -14.3 | **disagree** |
| n4400 | marker | 4/4 | 51.7, 4363.4 (0.2, 5.5) | 50.8, 4361.6 (0.5, 10.3) | +0.9 | +1.9 | **disagree** |
| n4400 | marker | 5/5 | 62.3, 4570.3 (0.2, 5.4) | 61.5, 4572.6 (0.4, 8.5) | +0.9 | -2.4 | **disagree** |
| n4400 | marker | 6/6 | 72.8, 4763.4 (0.2, 5.3) | 72.1, 4759.5 (0.4, 8.4) | +0.7 | +3.9 | **disagree** |
| n4400 | marker | 7/7 | 82.1, 4870.5 (0.2, 5.2) | 80.9, 4873.8 (0.4, 8.3) | +1.2 | -3.3 | **disagree** |
| n4400 | marker | 8/8 | 90.5, 4977.6 (0.3, 6.9) | 89.7, 4971.0 (0.5, 10.0) | +0.9 | +6.6 | **disagree** |
| n4400 | marker | 9/9 | 102.3, 5074.8 (0.3, 6.8) | 101.3, 5071.6 (0.5, 9.9) | +1.0 | +3.2 | **disagree** |
| n4400 | marker | 10/10 | 112.2, 5140.9 (0.2, 5.1) | 111.3, 5144.5 (0.4, 8.2) | +0.8 | -3.7 | **disagree** |
| n4400 | marker | 11/11 | 121.7, 5196.6 (0.2, 5.0) | 120.7, 5200.3 (0.4, 8.2) | +1.0 | -3.7 | **disagree** |
| n4400 | marker | 12/12 | 131.1, 5224.9 (0.2, 5.0) | 130.2, 5232.0 (0.4, 8.1) | +0.8 | -7.1 | **disagree** |
| n4400 | marker | 13/13 | 140.2, 5246.2 (0.2, 5.0) | 139.4, 5260.2 (0.4, 8.1) | +0.8 | -14.0 | **disagree** |
| n4400 | marker | 14/14 | 150.1, 5243.6 (0.3, 6.7) | 149.3, 5250.7 (0.5, 9.9) | +0.8 | -7.2 | **disagree** |
| n4400 | marker | 15/15 | 159.7, 5220.2 (0.2, 5.0) | 158.7, 5224.0 (0.4, 8.1) | +1.0 | -3.8 | **disagree** |
| n4400 | marker | 16/16 | 170.4, 5141.9 (0.2, 5.1) | 169.3, 5149.2 (0.4, 8.2) | +1.0 | -7.3 | **disagree** |
| n734 | marker | 2/2 | 11.4, 988.1 (0.3, 6.0) | 10.4, 977.2 (0.5, 9.8) | +1.0 | +10.9 | **disagree** |
| n734 | trace | 1/interp | 7.7, 817.5 (0.2, 7.8) | 7.7, 769.7 (0.1, 2.8) | slope +76.2 | +47.8 (tol 37.2) | **disagree** |
| n734 | trace | 13/- | 68.3, 1277.4 (0.2, 9.5) | (no trace at this x) | | | unmatched in codex |
