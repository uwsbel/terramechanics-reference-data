# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-2B\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-2B\points-p1-native.csv` (codex).

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

Matched: 384; agreed 377; disagreed 7; unmatched 151 (kept as one-sided: 99 of claude, 52 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1468 | trace | 1/- | 12.7, 481.1 (0.3, 30.6) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 4/- | 23.7, 756.0 (0.3, 28.0) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 5/- | 24.5, 776.6 (0.3, 28.1) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 8/- | 35.0, 977.4 (0.3, 33.9) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 9/- | 38.5, 1017.0 (0.3, 32.2) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 10/- | 44.0, 1105.2 (0.3, 16.5) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 11/- | 45.4, 1122.5 (0.3, 23.4) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 22/- | 83.5, 1444.0 (0.3, 11.9) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 24/- | 88.9, 1483.8 (0.3, 20.5) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 28/- | 105.8, 1620.5 (0.3, 21.8) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 29/- | 107.7, 1639.5 (0.3, 20.0) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 30/- | 113.8, 1688.0 (0.3, 23.4) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 43/- | 156.1, 1894.1 (0.3, 24.5) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 46/- | 166.5, 1895.8 (0.3, 22.7) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 49/- | 176.8, 1874.9 (0.3, 22.8) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 51/- | 184.2, 1850.5 (0.3, 19.4) | (no trace at this x) | | | unmatched in codex |
| n2200 | feature | 3/3 | 247.8, 2659.3 (0.8, 17.6) | 249.9, 2659.3 (1.0, 19.5) | -2.0 | +0.0 | **disagree** |
| n2200 | trace | 4/- | 19.0, 1050.4 (0.3, 30.5) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 10/- | 44.1, 1579.7 (0.3, 18.5) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 14/- | 55.9, 1756.2 (0.3, 21.4) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 16/- | 62.9, 1849.7 (0.3, 21.1) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 17/- | 66.3, 1884.3 (0.3, 24.4) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 18/- | 73.3, 1977.8 (0.3, 34.6) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 20/- | 78.6, 2010.6 (0.3, 25.6) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 21/- | 83.7, 2077.2 (0.3, 20.2) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 22/- | 87.1, 2108.0 (0.3, 27.0) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 24/- | 94.0, 2172.9 (0.3, 23.5) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 31/- | 118.3, 2362.5 (0.3, 18.1) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 32/- | 123.8, 2405.2 (0.3, 19.7) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 33/- | 125.2, 2415.5 (0.3, 19.7) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 35/- | 132.1, 2463.3 (0.3, 12.8) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 41/- | 153.3, 2543.6 (0.3, 9.2) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 61/- | 224.8, 2705.6 (0.3, 22.7) | (no trace at this x) | | | unmatched in codex |
| n2995 | feature | 1/1 | 10.3, 1028.1 (0.8, 23.7) | 11.4, 1078.0 (1.0, 19.4) | -1.1 | -49.9 | **disagree** |
| n2995 | trace | 4/- | 23.8, 1557.4 (0.3, 30.7) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 6/- | 29.2, 1713.2 (0.3, 30.2) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 7/- | 34.3, 1849.9 (0.3, 28.0) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 12/- | 48.6, 2152.6 (0.3, 23.5) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 15/- | 58.5, 2311.5 (0.3, 18.1) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 18/- | 73.5, 2518.3 (0.3, 19.5) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 21/- | 83.9, 2636.2 (0.3, 10.8) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 24/- | 93.8, 2731.9 (0.3, 14.1) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 27/- | 103.7, 2819.0 (0.3, 15.7) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 29/- | 108.0, 2848.1 (0.3, 17.3) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 44/- | 164.9, 3229.4 (0.3, 8.7) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 60/- | 218.1, 3349.9 (0.3, 18.9) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 61/- | 224.5, 3351.5 (0.3, 17.2) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 66/- | 237.4, 3341.3 (0.3, 8.7) | (no trace at this x) | | | unmatched in codex |
| n3660 | feature | 1/1 | 10.0, 1080.0 (0.8, 23.5) | 10.4, 1178.5 (1.1, 23.1) | -0.4 | -98.5 | **disagree** |
| n3660 | feature | 3/3 | 246.6, 3927.9 (0.8, 12.5) | 250.0, 3922.9 (1.0, 19.4) | -3.4 | +5.0 | **disagree** |
| n3660 | trace | 1/- | 11.0, 1235.7 (1.3, 9.1) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 2/- | 10.6, 1322.3 (0.9, 8.9) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 3/- | 14.3, 1668.3 (0.9, 7.8) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 5/- | 14.3, 1657.9 (0.3, 44.2) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 6/- | 18.8, 1839.6 (0.3, 38.5) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 9/- | 27.2, 2050.1 (0.3, 13.4) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 10/- | 32.8, 2202.2 (0.3, 18.3) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 18/- | 63.2, 2788.5 (0.3, 15.7) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 21/- | 73.6, 2923.5 (0.3, 17.2) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 31/- | 108.1, 3277.4 (0.3, 17.2) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 40/- | 138.7, 3518.7 (0.3, 13.9) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 45/- | 157.6, 3641.0 (0.3, 8.9) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 46/- | 165.0, 3702.2 (0.3, 14.1) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 50/- | 176.2, 3763.3 (0.3, 9.0) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 55/- | 196.8, 3875.4 (0.3, 21.0) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 56/- | 204.3, 3906.0 (0.3, 21.0) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 63/- | 226.0, 3948.4 (0.3, 12.5) | (no trace at this x) | | | unmatched in codex |
| n4400 | feature | 1/1 | 9.0, 1062.7 (0.8, 23.6) | 9.5, 1799.1 (1.0, 20.6) | -0.5 | -736.4 | **disagree** |
| n4400 | trace | 4/interp | 12.0, 1512.6 (0.9, 8.2) | 12.0, 1912.7 (0.3, 53.8) | slope +23.9 | -400.1 (tol 89.5) | **disagree** |
| n4400 | trace | 13/- | 37.8, 2788.6 (0.3, 26.0) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 14/- | 42.8, 2908.3 (0.3, 22.4) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 19/- | 58.1, 3194.3 (0.3, 22.2) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 22/- | 68.5, 3376.2 (0.3, 24.1) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 25/- | 78.9, 3539.4 (0.3, 24.2) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 26/- | 84.0, 3602.3 (0.3, 22.5) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 27/- | 87.4, 3646.5 (0.3, 25.9) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 28/- | 93.0, 3717.9 (0.3, 15.8) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 31/- | 102.3, 3819.8 (0.3, 19.2) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 37/- | 123.1, 4005.1 (0.3, 17.9) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 39/- | 129.0, 4061.9 (0.3, 23.1) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 40/- | 134.0, 4108.3 (0.3, 17.9) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 42/- | 138.4, 4134.1 (0.3, 12.7) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 51/- | 176.8, 4376.7 (0.3, 18.0) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 59/- | 207.2, 4509.2 (0.3, 9.4) | (no trace at this x) | | | unmatched in codex |
| n734 | marker | 15/15 | 159.2, 979.6 (0.6, 20.0) | 161.1, 1012.1 (1.1, 22.8) | -1.9 | -32.6 | **disagree** |
| n734 | trace | 1/- | 12.1, 322.9 (0.3, 19.7) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 3/- | 16.5, 352.1 (0.3, 25.0) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 4/- | 21.0, 389.8 (0.3, 25.1) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 7/- | 33.0, 484.2 (0.3, 23.7) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 13/- | 52.8, 624.8 (0.3, 20.7) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 18/- | 69.0, 732.8 (0.3, 26.2) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 19/- | 73.5, 763.6 (0.3, 26.3) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 22/- | 83.4, 814.9 (0.3, 26.4) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 24/- | 92.4, 855.9 (0.3, 26.6) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 26/- | 97.2, 878.1 (0.3, 24.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 27/- | 102.8, 898.6 (0.3, 28.4) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 29/- | 107.6, 917.3 (0.3, 26.7) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 30/- | 112.6, 934.4 (0.3, 23.3) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 50/- | 178.5, 1046.5 (0.3, 23.7) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 51/- | 183.5, 1049.9 (0.3, 27.2) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 52/- | 187.0, 1049.8 (0.3, 27.2) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 56/- | 202.3, 1051.2 (0.3, 25.4) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 58/- | 207.6, 1049.3 (0.3, 27.2) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 59/- | 212.0, 1045.7 (0.3, 23.7) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 61/- | 217.3, 1038.6 (0.3, 27.2) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 62/- | 221.7, 1035.0 (0.3, 23.8) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 210 trace samples excluded

No hand decision overridden.
