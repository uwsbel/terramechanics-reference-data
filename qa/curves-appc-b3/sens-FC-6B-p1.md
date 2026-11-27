# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b3\rederived\claude\FC-6B\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b3\rederived\codex\FC-6B\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 25 | 30 |
| x per px | 0.1734 | 0.1709 |
| y per px | 3.4089 | 3.4078 |
| RMS residual x, y | 0.555, 8.045 | 1.463, 8.029 |

Corners of claude's box [900, 895, 2140, 2130] mapped by both calibrations (tolerance 2.19 in x, 19.48 in y):

- (40.7, 4100.7) vs (42.8, 4099.9)
- (255.8, 4102.6) vs (254.7, 4102.1)
- (40.1, -109.3) vs (42.1, -108.7)
- (255.1, -107.4) vs (254.0, -106.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.12 | 0.40 | 0.40 | 24 | 0.61 | 0.52 | agree |
| x | 50 | 0.00 | 0.37 | 0.37 | 12 | 0.96 | 0.95 | agree |
| x | 100 | 0.05 | 0.22 | 0.23 | 12 | 0.50 | 0.50 | agree |
| x | 150 | 0.09 | 0.33 | 0.34 | 12 | 0.92 | 0.94 | agree |
| x | 200 | 0.48 | 0.24 | 0.15 | 12 | 0.50 | 0.59 | agree |
| x | 250 | 0.29 | 0.27 | 0.36 | 12 | 1.17 | 1.00 | agree |
| y | 0 | 0.11 | 0.39 | 0.33 | 12 | 0.78 | 0.78 | agree |
| y | 1000 | 0.17 | 0.46 | 0.34 | 12 | 1.00 | 0.63 | agree |
| y | 2000 | 0.24 | 0.48 | 0.52 | 12 | 0.76 | 1.08 | agree |
| y | 3000 | 0.34 | 0.31 | 0.30 | 12 | 0.79 | 0.94 | agree |
| y | 4000 | 0.07 | 0.62 | 0.62 | 12 | 1.68 | 1.35 | agree |

Both maps along every verified line and every interval midline (250 places): largest difference 0.07457 in x (tolerance 0.3606, codex 200), 1.381 in y (tolerance 7.358, claude 3000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.37 px (claude: x 0.30, y 0.45), 0.36 px (codex: x 0.31, y 0.42), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 352; agreed 335; disagreed 17; unmatched 16 (kept as one-sided: 4 of claude, 12 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1761 | feature | 3/82 | 242.2, 1621.2 (0.2, 11.0) | 242.7, 1610.9 (0.3, 10.2) | -0.5 | +10.4 | **disagree** |
| n2934 | marker | 3/3 | 47.3, 1427.7 (0.3, 8.5) | 47.5, 1412.1 (0.2, 4.9) | -0.2 | +15.5 | **disagree** |
| n2934 | marker | 4/4 | 66.3, 1711.1 (0.2, 6.6) | 66.4, 1698.6 (0.2, 5.1) | -0.0 | +12.5 | **disagree** |
| n2934 | marker | 5/5 | 86.5, 1939.1 (0.2, 6.5) | 86.4, 1926.4 (0.2, 5.3) | +0.0 | +12.7 | **disagree** |
| n2934 | marker | 11/11 | 217.9, 2832.1 (0.2, 6.4) | 217.8, 2817.7 (0.2, 5.0) | +0.1 | +14.5 | **disagree** |
| n2934 | trace | 1/- | 14.2, 918.8 (0.1, 11.6) | (no trace at this x) | | | unmatched in codex |
| n3815 | feature | 1/81 | 13.3, 1324.2 (0.1, 25.8) | 12.5, 1301.3 (0.2, 10.0) | +0.8 | +22.9 | **disagree** |
| n4695 | feature | 1/80 | 10.8, 1135.2 (0.2, 12.1) | 11.4, 1139.2 (0.2, 9.8) | -0.5 | -4.0 | **disagree** |
| n4695 | marker | 3/3 | 46.1, 2366.2 (0.2, 6.4) | 46.1, 2378.7 (0.2, 5.1) | +0.0 | -12.6 | **disagree** |
| n4695 | marker | 4/4 | 65.8, 2727.8 (0.2, 6.4) | 65.6, 2743.9 (0.2, 5.0) | +0.2 | -16.1 | **disagree** |
| n4695 | marker | 5/5 | 85.1, 3005.0 (0.2, 8.3) | 85.2, 3030.3 (0.6, 12.0) | -0.1 | -25.3 | **disagree** |
| n4695 | marker | 6/6 | 116.1, 3426.7 (0.2, 7.2) | 116.0, 3440.4 (0.2, 5.4) | +0.1 | -13.7 | **disagree** |
| n4695 | marker | 8/8 | 157.3, 3801.5 (0.2, 7.8) | 157.1, 3815.4 (0.2, 5.7) | +0.2 | -13.9 | **disagree** |
| n4695 | trace | 1/- | 10.8, 1135.2 (0.2, 12.1) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 60/- | 243.1, 4243.8 (0.2, 15.4) | (no trace at this x) | | | unmatched in codex |
| n734 | feature | 3/82 | 240.7, 348.6 (0.2, 11.5) | 241.3, 351.9 (0.3, 9.6) | -0.7 | -3.3 | **disagree** |
| n734 | marker | 1/1 | 11.3, 405.1 (0.2, 4.8) | 10.7, 403.4 (0.2, 4.5) | +0.5 | +1.7 | **disagree** |
| n734 | marker | 5/5 | 86.4, 388.3 (0.2, 4.8) | 87.2, 384.6 (0.2, 4.6) | -0.8 | +3.6 | **disagree** |
| n734 | marker | 11/11 | 217.8, 348.3 (0.2, 4.8) | 218.9, 326.9 (0.2, 4.6) | -1.2 | +21.4 | **disagree** |
| n734 | marker | 12/12 | 247.9, 332.8 (0.3, 4.8) | 249.0, 309.9 (0.6, 11.3) | -1.1 | +22.8 | **disagree** |
| n734 | trace | 1/- | 13.4, 397.8 (0.1, 10.6) | (no trace at this x) | | | unmatched in codex |
