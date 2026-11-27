# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-1C\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-1C\points-p1-native.csv` (codex).

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

Matched: 346; agreed 342; disagreed 4; unmatched 79 (kept as one-sided: 55 of claude, 24 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1172 | marker | -/10 | (none) | 200.7, 1532.0 | | | unmatched in claude |
| n1172 | trace | 1/- | 23.2, 1054.1 (0.3, 19.3) | (no trace at this x) | | | unmatched in codex |
| n1172 | trace | 5/- | 44.1, 1391.6 (0.3, 23.1) | (no trace at this x) | | | unmatched in codex |
| n1172 | trace | 9/- | 63.8, 1603.5 (0.3, 23.2) | (no trace at this x) | | | unmatched in codex |
| n1172 | trace | 17/- | 102.8, 1807.3 (0.3, 23.3) | (no trace at this x) | | | unmatched in codex |
| n1172 | trace | 20/- | 116.9, 1803.2 (0.3, 16.4) | (no trace at this x) | | | unmatched in codex |
| n1172 | trace | 21/- | 123.8, 1785.5 (0.3, 16.3) | (no trace at this x) | | | unmatched in codex |
| n1172 | trace | 25/- | 144.4, 1725.5 (0.3, 23.2) | (no trace at this x) | | | unmatched in codex |
| n1172 | trace | 28/- | 157.1, 1711.0 (0.3, 23.2) | (no trace at this x) | | | unmatched in codex |
| n1172 | trace | 40/- | 216.7, 1475.7 (0.3, 19.6) | (no trace at this x) | | | unmatched in codex |
| n1172 | trace | 41/- | 224.2, 1454.6 (0.3, 19.5) | (no trace at this x) | | | unmatched in codex |
| n1172 | trace | 44/- | 235.3, 1443.8 (0.3, 16.1) | (no trace at this x) | | | unmatched in codex |
| n1172 | trace | 45/- | 243.0, 1436.6 (0.3, 12.6) | (no trace at this x) | | | unmatched in codex |
| n1760 | trace | 13/- | 84.2, 2448.4 (0.3, 16.5) | (no trace at this x) | | | unmatched in codex |
| n1760 | trace | 20/- | 116.5, 2699.2 (0.3, 23.5) | (no trace at this x) | | | unmatched in codex |
| n1760 | trace | 24/- | 137.1, 2810.3 (0.3, 20.0) | (no trace at this x) | | | unmatched in codex |
| n1760 | trace | 32/- | 176.5, 2825.7 (0.3, 23.5) | (no trace at this x) | | | unmatched in codex |
| n1760 | trace | 40/- | 216.9, 2627.4 (0.3, 20.0) | (no trace at this x) | | | unmatched in codex |
| n2345 | feature | -/4 | (none) | 111.3, 3083.4 | | | unmatched in claude |
| n2345 | feature | -/5 | (none) | 140.5, 3061.2 | | | unmatched in claude |
| n2345 | marker | -/11 | (none) | 202.4, 2971.1 | | | unmatched in claude |
| n2345 | trace | 1/- | 13.6, 1612.5 (0.3, 33.7) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 4/- | 27.5, 2065.6 (0.3, 27.1) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 13/- | 75.4, 2925.6 (0.3, 23.5) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 20/- | 106.5, 3083.7 (0.3, 19.6) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 21/- | 113.3, 3083.3 (0.3, 12.7) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 26/- | 135.8, 3058.1 (0.3, 16.2) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 32/- | 166.4, 3108.2 (0.3, 23.1) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 33/- | 173.2, 3114.8 (0.3, 23.1) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 36/- | 186.4, 3072.8 (0.3, 19.6) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 37/- | 193.7, 3031.1 (0.3, 16.2) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 43/- | 224.1, 2826.8 (0.3, 16.5) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 48/- | 247.5, 2745.0 (0.3, 16.5) | (no trace at this x) | | | unmatched in codex |
| n2935 | feature | 1/1 | 62.7, 3498.7 (0.6, 13.0) | 58.6, 3451.2 (1.1, 23.9) | +4.1 | +47.5 | **disagree** |
| n2935 | marker | 8/8 | 198.4, 3871.2 (0.6, 13.2) | 200.2, 3866.0 (1.0, 20.8) | -1.7 | +5.2 | **disagree** |
| n2935 | trace | 24/- | 185.0, 3892.5 (0.3, 13.2) | (no trace at this x) | | | unmatched in codex |
| n294 | trace | 4/- | 37.3, 578.3 (0.3, 22.4) | (no trace at this x) | | | unmatched in codex |
| n294 | trace | 5/- | 44.1, 619.4 (0.3, 22.4) | (no trace at this x) | | | unmatched in codex |
| n294 | trace | 9/- | 64.1, 708.3 (0.3, 22.4) | (no trace at this x) | | | unmatched in codex |
| n294 | trace | 12/- | 76.6, 728.6 (0.3, 19.0) | (no trace at this x) | | | unmatched in codex |
| n294 | trace | 13/- | 83.3, 742.1 (0.3, 19.0) | (no trace at this x) | | | unmatched in codex |
| n294 | trace | 20/- | 116.9, 730.9 (0.3, 19.0) | (no trace at this x) | | | unmatched in codex |
| n294 | trace | 24/- | 135.8, 699.4 (0.3, 19.0) | (no trace at this x) | | | unmatched in codex |
| n294 | trace | 28/- | 156.0, 664.5 (0.3, 19.0) | (no trace at this x) | | | unmatched in codex |
| n3520 | marker | 9/9 | 132.1, 4275.7 (0.4, 9.6) | 133.6, 4277.0 (0.8, 17.1) | -1.6 | -1.3 | **disagree** |
| n3520 | trace | 1/- | 13.9, 2171.5 (0.3, 34.1) | (no trace at this x) | | | unmatched in codex |
| n3520 | trace | 9/- | 54.6, 3416.5 (0.3, 30.1) | (no trace at this x) | | | unmatched in codex |
| n3520 | trace | 13/- | 73.4, 3783.7 (0.3, 26.9) | (no trace at this x) | | | unmatched in codex |
| n3520 | trace | 20/- | 106.9, 4184.1 (0.3, 23.4) | (no trace at this x) | | | unmatched in codex |
| n3520 | trace | 44/- | 227.7, 4169.0 (0.3, 23.4) | (no trace at this x) | | | unmatched in codex |
| n587 | marker | 12/12 | 230.4, 1114.1 (0.5, 8.9) | 230.5, 1086.1 (0.8, 15.8) | -0.2 | +28.0 | **disagree** |
| n587 | trace | 1/- | 13.6, 592.7 (0.3, 29.3) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 12/- | 66.1, 1310.7 (0.3, 23.0) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 16/- | 86.7, 1351.8 (0.3, 19.5) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 17/- | 93.4, 1358.5 (0.3, 23.0) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 21/- | 114.1, 1340.4 (0.3, 19.5) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 28/- | 147.4, 1342.7 (0.3, 19.5) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 32/- | 166.4, 1303.8 (0.3, 22.9) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 33/- | 173.7, 1268.8 (0.3, 19.4) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 36/- | 187.2, 1202.3 (0.3, 22.8) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 41/- | 214.5, 1090.3 (0.3, 15.8) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 44/- | 226.9, 1062.1 (0.3, 22.7) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 45/- | 234.4, 1041.1 (0.3, 12.3) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 147 trace samples excluded

No hand decision overridden.
