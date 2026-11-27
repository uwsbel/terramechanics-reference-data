# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b3\rederived\claude\FC-6D\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b3\rederived\codex\FC-6D\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 25 | 30 |
| x per px | 0.1702 | 0.1683 |
| y per px | 3.4280 | 3.4281 |
| RMS residual x, y | 0.128, 8.607 | 1.079, 8.624 |

Corners of claude's box [800, 990, 2258, 2245] mapped by both calibrations (tolerance 1.38 in x, 20.66 in y):

- (8.3, 4196.7) vs (10.2, 4196.4)  **disagree**
- (256.4, 4139.7) vs (255.6, 4140.9)
- (5.1, -105.2) vs (7.0, -105.6)  **disagree**
- (253.2, -162.1) vs (252.4, -161.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.11 | 0.19 | 0.21 | 24 | 0.51 | 0.84 | agree |
| x | 50 | 0.26 | 0.10 | 0.20 | 12 | 0.50 | 0.50 | agree |
| x | 100 | 0.11 | 0.21 | 0.17 | 12 | 0.50 | 0.50 | agree |
| x | 150 | 0.09 | 0.28 | 0.25 | 12 | 0.56 | 0.63 | agree |
| x | 200 | 0.27 | 0.25 | 0.16 | 12 | 0.58 | 0.50 | agree |
| x | 250 | 0.14 | 0.11 | 0.14 | 12 | 0.50 | 0.50 | agree |
| y | 0 | 0.21 | 0.53 | 0.53 | 12 | 1.73 | 1.27 | agree |
| y | 1000 | 0.06 | 0.49 | 0.47 | 12 | 1.03 | 1.02 | agree |
| y | 2000 | 0.16 | 0.37 | 0.38 | 12 | 0.81 | 1.01 | agree |
| y | 3000 | 0.44 | 0.50 | 0.48 | 12 | 1.26 | 0.99 | agree |
| y | 4000 | 0.60 | 0.20 | 0.37 | 12 | 0.81 | 0.89 | agree |

Both maps along every verified line and every interval midline (205 places): largest difference 0.0427 in x (tolerance 0.2065, codex 200), 2.31 in y (tolerance 7.615, claude 4000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.30 px (claude: x 0.19, y 0.42), 0.30 px (codex: x 0.19, y 0.45), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 429; agreed 419; disagreed 10; unmatched 42 (kept as one-sided: 5 of claude, 37 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n147 | feature | 1/81 | 13.1, 11.6 (0.0, 11.9) | 14.2, 8.1 (0.2, 13.8) | -1.1 | +3.5 | **disagree** |
| n147 | feature | 3/83 | 242.3, 121.7 (0.0, 11.7) | 244.6, 106.2 (0.2, 13.6) | -2.2 | +15.6 | **disagree** |
| n147 | trace | 1/- | 13.1, 11.6 (0.0, 11.9) | (no trace at this x) | | | unmatched in codex |
| n1761 | feature | 1/79 | 13.0, 496.3 (0.0, 12.1) | 13.8, 492.9 (0.2, 10.8) | -0.8 | +3.5 | **disagree** |
| n1761 | feature | 3/81 | 246.1, 1606.2 (0.0, 10.0) | 245.7, 1608.4 (0.2, 10.3) | +0.3 | -2.2 | **disagree** |
| n1761 | trace | 1/- | 13.0, 496.3 (0.0, 12.1) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 71/- | 246.1, 1606.2 (0.0, 10.0) | (no trace at this x) | | | unmatched in codex |
| n2934 | feature | 1/80 | 14.8, 817.2 (0.1, 16.1) | 14.0, 807.1 (0.2, 10.7) | +0.8 | +10.1 | **disagree** |
| n2934 | trace | 75/- | 246.8, 2660.0 (0.1, 12.2) | (no trace at this x) | | | unmatched in codex |
| n3814 | feature | 1/81 | 14.0, 1361.1 (0.1, 17.0) | 13.3, 1332.4 (0.2, 10.3) | +0.6 | +28.7 | **disagree** |
| n4695 | feature | 3/89 | 246.6, 4558.4 (0.1, 14.4) | 246.9, 4567.6 (0.2, 11.9) | -0.3 | -9.2 | **disagree** |
| n4695 | marker | 8/8 | 115.7, 3836.8 (0.3, 6.6) | 116.6, 3840.2 (0.2, 5.0) | -0.9 | -3.4 | **disagree** |
| n4695 | marker | 14/14 | 237.8, 4619.6 (0.2, 7.0) | 237.3, 4618.7 (0.2, 6.9) | +0.5 | +0.9 | **disagree** |
| n4695 | marker | 15/15 | 248.8, 4586.7 (0.3, 8.6) | 251.3, 4590.4 (0.6, 15.5) | -2.5 | -3.7 | **disagree** |
| n4695 | trace | 1/- | 13.6, 1657.5 (0.1, 16.8) | (no trace at this x) | | | unmatched in codex |
