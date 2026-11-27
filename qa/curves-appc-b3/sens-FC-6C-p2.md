# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b3\rederived\claude\FC-6C\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b3\rederived\codex\FC-6C\points-p2-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 18 | 18 |
| x per px | 0.1712 | 0.1712 |
| y per px | 0.3395 | 0.3394 |
| RMS residual x, y | 0.585, 0.080 | 0.581, 0.072 |

Corners of claude's box [638, 2540, 2160, 3170] mapped by both calibrations (tolerance 1.34 in x, 0.49 in y):

- (-3.9, 109.6) vs (-3.9, 109.6)
- (256.6, 105.7) vs (256.6, 105.5)
- (-5.3, -104.2) vs (-5.3, -104.2)
- (255.2, -108.2) vs (255.3, -108.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.15 | 0.40 | 0.45 | 6 | 0.55 | 0.76 | agree |
| x | 50 | 0.25 | 0.28 | 0.24 | 6 | 0.50 | 0.54 | agree |
| x | 100 | 0.10 | 0.22 | 0.17 | 6 | 0.51 | 0.53 | agree |
| x | 150 | 0.08 | 0.29 | 0.28 | 6 | 0.56 | 0.50 | agree |
| x | 200 | 0.25 | 0.34 | 0.22 | 6 | 0.92 | 0.62 | agree |
| x | 250 | 0.17 | 0.30 | 0.22 | 6 | 0.53 | 0.50 | agree |
| y | -100 | 0.09 | 0.38 | 0.37 | 15 | 0.62 | 0.63 | agree |
| y | 0 | 0.39 | 0.23 | 0.13 | 15 | 0.59 | 0.50 | agree |
| y | 100 | 0.39 | 0.31 | 0.32 | 15 | 0.74 | 0.50 | agree |

Both maps along every verified line and every interval midline (184 places): largest difference 0.04253 in x (tolerance 0.183, claude 50), 0.1423 in y (tolerance 0.4209, between codex 0 and claude 100); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.31 px (claude: x 0.31, y 0.31), 0.27 px (codex: x 0.26, y 0.27), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 64; agreed 51; disagreed 13; unmatched 0 (kept as one-sided: 0 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1961 | marker | 1/1 | -0.0, -19.2 (0.2, 0.6) | 1.1, -20.2 (0.6, 1.3) | -1.2 | +1.1 | **disagree** |
| n1961 | marker | 4/4 | 59.7, -13.0 (0.2, 0.4) | 60.8, -14.2 (0.4, 0.8) | -1.1 | +1.2 | **disagree** |
| n1961 | marker | 6/6 | 99.8, -13.6 (0.2, 0.4) | 98.9, -13.8 (0.6, 1.1) | +0.9 | +0.2 | **disagree** |
| n1961 | marker | 11/11 | 199.7, -10.8 (0.3, 0.6) | 198.8, -11.1 (0.6, 1.1) | +0.8 | +0.3 | **disagree** |
| n1961 | marker | 13/13 | 250.0, -9.5 (0.2, 0.6) | 248.9, -10.3 (0.7, 1.3) | +1.0 | +0.8 | **disagree** |
| n2934 | marker | 1/1 | 0.1, -33.6 (0.2, 0.4) | -1.0, -33.5 (0.7, 1.3) | +1.1 | -0.2 | **disagree** |
| n2934 | marker | 6/6 | 99.6, -37.2 (0.2, 0.4) | 98.8, -37.1 (0.6, 1.1) | +0.8 | -0.1 | **disagree** |
| n2934 | marker | 7/7 | 119.2, -34.8 (0.2, 0.4) | 120.1, -35.9 (0.6, 1.1) | -0.9 | +1.1 | **disagree** |
| n2934 | marker | 11/11 | 199.5, -30.7 (0.3, 0.4) | 198.5, -31.0 (0.6, 1.1) | +1.0 | +0.2 | **disagree** |
| n2934 | marker | 13/13 | 250.2, -27.7 (0.2, 0.4) | 251.2, -27.9 (0.7, 1.3) | -1.0 | +0.1 | **disagree** |
| n3815 | marker | 13/13 | 250.2, -54.8 (0.2, 0.6) | 251.1, -54.5 (0.7, 1.3) | -0.9 | -0.3 | **disagree** |
| n4695 | marker | 11/11 | 215.8, -29.8 (0.2, 0.4) | 217.9, -29.6 (0.5, 0.9) | -2.1 | -0.2 | **disagree** |
| n4695 | marker | 12/12 | 245.0, -29.2 (0.2, 0.4) | 246.9, -30.0 (0.5, 0.9) | -1.8 | +0.8 | **disagree** |
