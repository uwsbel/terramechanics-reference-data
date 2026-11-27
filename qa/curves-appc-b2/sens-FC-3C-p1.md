# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b2\rederived\claude\FC-3C\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b2\rederived\codex\FC-3C\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 36 | 42 |
| x per px | 0.1717 | 0.1717 |
| y per px | 3.4264 | 3.4373 |
| RMS residual x, y | 0.366, 4.692 | 0.364, 9.666 |

Corners of claude's box [790, 1330, 2295, 2850] mapped by both calibrations (tolerance 0.90 in x, 17.80 in y):

- (-2.6, 5167.5) vs (-2.6, 5179.8)
- (255.8, 5130.7) vs (255.8, 5139.8)
- (-5.6, -40.6) vs (-5.5, -44.8)
- (252.9, -77.3) vs (252.9, -84.8)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.20 | 0.30 | 0.38 | 15 | 0.57 | 0.52 | agree |
| x | 50 | 0.26 | 0.25 | 0.26 | 15 | 0.52 | 0.70 | agree |
| x | 100 | 0.04 | 0.35 | 0.35 | 15 | 0.73 | 0.71 | agree |
| x | 150 | 0.23 | 0.43 | 0.31 | 15 | 1.09 | 0.63 | agree |
| x | 200 | 0.16 | 0.20 | 0.20 | 15 | 0.52 | 0.50 | agree |
| x | 250 | 0.27 | 0.39 | 0.31 | 15 | 0.69 | 0.65 | agree |
| y | 6000 | | | | | | | codex's line not a knot: misplaced: 6.63 px from the ink's line at an end of the line |
| y | 0 | 0.19 | 0.36 | 0.31 | 15 | 0.50 | 0.60 | agree |
| y | 1000 | 0.05 | 0.39 | 0.39 | 15 | 0.84 | 0.83 | agree |
| y | 2000 | 0.05 | 0.37 | 0.35 | 15 | 1.23 | 1.18 | agree |
| y | 3000 | 0.20 | 0.51 | 0.39 | 23 | 0.73 | 0.69 | agree |
| y | 4000 | 0.21 | 0.27 | 0.35 | 15 | 0.67 | 0.79 | agree |
| y | 5000 | 0.57 | 0.51 | 0.36 | 15 | 1.07 | 0.63 | agree |

Both maps along every verified line and every interval midline (247 places): largest difference 0.04651 in x (tolerance 0.2186, between codex 0 and claude 50), 2.182 in y (tolerance 6.416, codex 5000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 12 shared lines checked against the ink, mean of the median distances 0.36 px (claude: x 0.32, y 0.40), 0.33 px (codex: x 0.30, y 0.36), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 436; agreed 421; disagreed 15; unmatched 114 (kept as one-sided: 101 of claude, 13 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1761 | feature | 3/3 | 249.5, 1978.4 (0.4, 8.9) | 246.8, 2019.5 (0.4, 9.0) | +2.7 | -41.1 | **disagree** |
| n1761 | marker | 11/11 | 249.5, 1978.4 (0.3, 7.2) | 251.6, 1984.7 (0.9, 17.5) | -2.1 | -6.3 | **disagree** |
| n1761 | trace | 1/- | 10.6, 1823.1 (0.6, 5.4) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 2/- | 11.5, 1870.4 (0.7, 5.5) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 10/- | 25.9, 2243.3 (0.2, 14.0) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 11/- | 32.0, 2345.8 (0.2, 10.5) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 17/- | 45.3, 2433.4 (0.2, 17.3) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 18/- | 51.8, 2446.2 (0.2, 13.8) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 24/- | 63.9, 2449.4 (0.2, 11.2) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 25/- | 71.2, 2448.3 (0.2, 7.8) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 31/- | 90.1, 2431.6 (0.2, 9.5) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 38/- | 109.7, 2421.7 (0.2, 13.0) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 39/- | 110.6, 2406.1 (0.2, 10.4) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 60/- | 163.9, 2310.3 (0.3, 11.3) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 61/- | 169.4, 2280.2 (0.3, 17.4) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 71/- | 193.0, 2214.8 (0.2, 12.3) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 78/- | 214.8, 2127.4 (0.2, 13.2) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 79/- | 220.8, 2123.1 (0.2, 9.8) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 90/- | 246.8, 2040.3 (0.2, 8.1) | (no trace at this x) | | | unmatched in codex |
| n2934 | marker | 10/10 | 197.0, 2989.4 (0.2, 4.7) | 199.5, 2965.4 (0.7, 13.4) | -2.5 | +24.0 | **disagree** |
| n2934 | marker | 12/12 | 247.4, 2831.3 (0.2, 4.9) | 248.8, 2816.9 (0.6, 11.8) | -1.4 | +14.4 | **disagree** |
| n2934 | trace | 1/- | 9.0, 2678.5 (0.6, 5.1) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 2/- | 9.9, 2774.9 (0.5, 5.0) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 12/- | 26.0, 3279.2 (0.2, 15.0) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 13/- | 31.3, 3353.7 (0.2, 11.5) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 19/- | 44.6, 3430.4 (0.2, 8.1) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 27/- | 65.7, 3471.5 (0.2, 11.5) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 28/- | 70.6, 3465.5 (0.2, 8.9) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 29/- | 72.5, 3448.1 (0.2, 8.9) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 35/- | 84.1, 3444.4 (0.2, 8.1) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 36/- | 90.0, 3472.6 (0.2, 8.9) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 37/- | 90.9, 3443.3 (0.2, 8.1) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 43/- | 103.6, 3427.5 (0.2, 11.5) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 44/- | 105.0, 3449.5 (0.2, 14.1) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 45/- | 110.0, 3450.4 (0.2, 9.8) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 51/- | 123.8, 3381.4 (0.3, 12.4) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 52/- | 129.7, 3359.9 (0.3, 12.4) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 59/- | 144.9, 3280.3 (0.3, 13.2) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 60/- | 145.8, 3285.3 (0.3, 10.7) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 61/- | 151.8, 3239.8 (0.3, 14.1) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 67/- | 164.7, 3177.8 (0.3, 11.5) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 68/- | 169.8, 3178.7 (0.3, 10.7) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 77/- | 191.4, 3016.0 (0.2, 15.0) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 78/- | 193.8, 3010.5 (0.2, 12.4) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 79/- | 201.6, 2981.8 (0.2, 14.2) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 87/- | 219.4, 2917.1 (0.2, 9.1) | (no trace at this x) | | | unmatched in codex |
| n3815 | feature | 3/3 | 249.2, 3997.3 (0.4, 8.1) | 247.9, 3998.7 (0.6, 11.8) | +1.4 | -1.3 | **disagree** |
| n3815 | marker | 12/12 | 249.2, 3997.3 (0.3, 6.4) | 251.1, 3984.4 (0.8, 15.2) | -1.9 | +12.9 | **disagree** |
| n3815 | trace | 1/- | 9.7, 3283.6 (0.5, 4.7) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 2/- | 10.5, 3379.4 (0.6, 4.7) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 14/- | 26.4, 4071.5 (0.2, 15.0) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 15/- | 31.5, 4203.4 (0.2, 14.3) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 21/- | 45.5, 4404.7 (0.2, 12.7) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 28/- | 70.4, 4633.8 (0.2, 13.7) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 34/- | 82.1, 4683.7 (0.2, 13.8) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 35/- | 90.7, 4718.7 (0.2, 12.9) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 40/- | 102.6, 4737.6 (0.2, 12.9) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 41/- | 110.9, 4741.5 (0.2, 10.3) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 47/- | 123.2, 4724.1 (0.3, 12.9) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 48/- | 129.0, 4697.3 (0.3, 10.3) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 54/- | 143.4, 4629.4 (0.3, 12.0) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 61/- | 164.1, 4493.0 (0.3, 9.3) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 62/- | 169.6, 4440.2 (0.3, 14.5) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 72/- | 194.1, 4280.5 (0.2, 14.4) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 81/- | 219.7, 4123.9 (0.2, 14.3) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 82/- | 225.2, 4098.7 (0.2, 14.3) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 91/- | 246.8, 4011.9 (0.2, 14.2) | (no trace at this x) | | | unmatched in codex |
| n4695 | feature | 3/3 | 251.0, 4735.9 (0.4, 8.7) | 246.5, 4759.5 (0.4, 8.1) | +4.5 | -23.6 | **disagree** |
| n4695 | marker | 2/2 | 28.8, 4936.5 (0.2, 5.3) | 28.8, 4949.2 (0.2, 4.6) | +0.0 | -12.7 | **disagree** |
| n4695 | marker | 6/6 | 107.2, 5559.4 (0.2, 7.0) | 107.7, 5558.3 (0.2, 6.0) | -0.5 | +1.0 | **disagree** |
| n4695 | marker | 10/10 | 196.6, 4936.7 (0.2, 7.0) | 197.8, 4957.2 (0.7, 13.3) | -1.2 | -20.5 | **disagree** |
| n4695 | marker | 11/11 | 220.9, 4880.8 (0.2, 5.3) | 221.5, 4891.3 (0.2, 4.6) | -0.5 | -10.5 | **disagree** |
| n4695 | trace | 1/- | 9.8, 4089.8 (0.4, 4.7) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 2/- | 10.7, 4186.2 (0.4, 4.8) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 16/- | 31.3, 4990.0 (0.2, 18.3) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 38/- | 89.2, 5566.9 (0.2, 15.7) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 45/- | 103.8, 5566.7 (0.2, 11.4) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 46/- | 110.3, 5545.1 (0.2, 11.3) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 53/- | 124.8, 5505.2 (0.3, 13.0) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 54/- | 130.8, 5471.5 (0.3, 13.7) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 67/- | 168.8, 5215.5 (0.3, 15.6) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 68/- | 169.7, 5215.4 (0.3, 15.6) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 79/- | 201.6, 4998.0 (0.2, 12.3) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 87/- | 225.4, 4854.2 (0.2, 9.6) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 96/- | 247.0, 4752.2 (0.2, 13.9) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 97/- | 247.9, 4750.3 (0.2, 9.5) | (no trace at this x) | | | unmatched in codex |
| n734 | feature | 3/3 | 247.5, 827.5 (0.4, 8.3) | 246.1, 822.1 (0.4, 8.3) | +1.4 | +5.4 | **disagree** |
| n734 | marker | 3/3 | 49.2, 1328.4 (0.2, 5.1) | 50.8, 1316.2 (0.5, 10.1) | -1.6 | +12.2 | **disagree** |
| n734 | marker | 10/10 | 198.0, 897.3 (0.2, 4.9) | 199.5, 900.8 (0.7, 13.5) | -1.5 | -3.5 | **disagree** |
| n734 | marker | 12/12 | 247.5, 827.5 (0.2, 4.8) | 249.6, 825.0 (0.8, 15.2) | -2.1 | +2.4 | **disagree** |
| n734 | trace | 1/- | 12.3, 1098.3 (0.9, 5.0) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 5/- | 26.0, 1274.1 (0.2, 10.1) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 6/- | 31.3, 1275.0 (0.2, 9.3) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 7/- | 33.3, 1325.6 (0.2, 14.4) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 13/- | 46.7, 1313.5 (0.2, 14.4) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 14/- | 51.6, 1299.2 (0.2, 9.3) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 15/- | 52.5, 1304.2 (0.2, 11.8) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 21/- | 65.6, 1263.3 (0.2, 7.6) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 22/- | 70.5, 1233.8 (0.2, 11.8) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 29/- | 84.5, 1189.5 (0.2, 10.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 30/- | 90.3, 1164.9 (0.2, 9.2) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 36/- | 105.0, 1095.1 (0.2, 10.8) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 37/- | 110.0, 1091.0 (0.2, 9.1) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 38/- | 111.9, 1084.0 (0.2, 7.4) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 44/- | 124.6, 1048.3 (0.3, 9.1) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 45/- | 130.4, 1017.0 (0.3, 14.2) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 51/- | 145.3, 989.3 (0.3, 11.8) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 52/- | 146.2, 958.3 (0.3, 11.8) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 53/- | 152.6, 971.1 (0.3, 10.1) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 59/- | 166.1, 922.8 (0.3, 10.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 60/- | 171.1, 923.8 (0.3, 11.7) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 61/- | 172.0, 921.9 (0.2, 7.4) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 71/- | 201.6, 876.5 (0.2, 10.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 77/- | 215.6, 853.9 (0.2, 12.6) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 78/- | 216.5, 812.6 (0.2, 10.8) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 79/- | 221.5, 811.9 (0.2, 10.8) | (no trace at this x) | | | unmatched in codex |
