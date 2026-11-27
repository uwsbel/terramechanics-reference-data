# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b2\rederived\claude\FC-4B\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b2\rederived\codex\FC-4B\points-p2-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 30 | 12 |
| x per px | 0.1721 | 0.1721 |
| y per px | 0.3418 | 0.3416 |
| RMS residual x, y | 0.218, 0.158 | 0.235, 0.038 |

Corners of claude's box [770, 2780, 2290, 3420] mapped by both calibrations (tolerance 0.62 in x, 0.54 in y):

- (-5.4, 58.5) vs (-5.4, 58.3)
- (256.2, 60.3) vs (256.2, 60.1)
- (-5.6, -160.3) vs (-5.7, -160.3)
- (256.0, -158.5) vs (256.0, -158.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.39 | 0.33 | 0.30 | 12 | 0.74 | 1.69 | agree |
| x | 50 | 1.63 | 0.42 | 0.19 | 12 | 2.20 | 1.18 | agree |
| x | 100 | 0.29 | 0.26 | 0.30 | 22 | 1.71 | 0.92 | agree |
| x | 150 | 0.19 | 0.30 | 0.26 | 12 | 0.69 | 0.77 | agree |
| x | 200 | 0.86 | 0.20 | 0.19 | 20 | 0.61 | 0.75 | agree |
| x | 250 | 0.27 | 0.36 | 0.24 | 12 | 1.62 | 1.70 | agree |
| y | -150 | 0.05 | 0.29 | 0.27 | 15 | 0.74 | 0.71 | agree |
| y | 0 | 0.77 | 0.29 | 0.52 | 23 | 0.50 | 1.06 | agree |
| y | 50 | 0.12 | 0.34 | 0.30 | 15 | 0.64 | 0.59 | agree |

Both maps along every verified line and every interval midline (220 places): largest difference 0.3267 in x (tolerance 0.6681, claude 50), 0.272 in y (tolerance 0.6138, codex 0); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.31 px (claude: x 0.31, y 0.31), 0.28 px (codex: x 0.25, y 0.36), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 64; agreed 56; disagreed 8; unmatched 1 (kept as one-sided: 0 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1761 | marker | 10/10 | 180.0, -101.3 (0.2, 0.5) | 179.1, -101.8 (0.5, 1.0) | +0.9 | +0.5 | **disagree** |
| n2934 | marker | 13/13 | 249.0, -121.3 (0.5, 0.8) | 249.6, -118.1 (1.0, 1.9) | -0.6 | -3.3 | **disagree** |
| n3815 | marker | 11/12 | 201.1, -129.0 (0.4, 0.8) | 202.5, -129.0 (0.9, 1.7) | -1.4 | -0.0 | **disagree** |
| n3815 | marker | 12/13 | 225.9, -126.5 (0.3, 0.5) | 227.6, -125.8 (0.7, 1.3) | -1.7 | -0.7 | **disagree** |
| n3815 | marker | -/11 | (none) | 180.2, -127.1 | | | unmatched in claude |
| n4695 | marker | 9/9 | 170.7, -131.0 (0.2, 0.5) | 170.2, -130.6 (0.2, 0.5) | +0.5 | -0.4 | **disagree** |
| n4695 | marker | 11/11 | 220.5, -129.6 (0.4, 0.8) | 222.4, -125.8 (0.8, 1.5) | -1.9 | -3.8 | **disagree** |
| n734 | marker | 11/11 | 200.1, -44.5 (0.3, 0.6) | 199.8, -42.0 (0.8, 1.7) | +0.3 | -2.5 | **disagree** |
| n734 | marker | 13/13 | 249.1, -40.3 (0.5, 0.8) | 250.8, -39.2 (1.0, 1.9) | -1.7 | -1.1 | **disagree** |
