# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b6\rederived\claude\FC-5A\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b6\rederived\codex\FC-5A\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 36 | 42 |
| x per px | 3.4072 | 3.4070 |
| y per px | 3.3930 | 3.4012 |
| RMS residual x, y | 4.974, 4.299 | 4.970, 7.583 |

Corners of claude's box [790, 1500, 2310, 3060] mapped by both calibrations (tolerance 13.35 in x, 15.28 in y):

- (-73.8, 5193.7) vs (-73.1, 5202.4)
- (5105.0, 5182.3) vs (5105.5, 5190.5)
- (-106.3, -99.4) vs (-106.6, -103.5)
- (5072.5, -110.8) vs (5072.0, -115.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.09 | 0.33 | 0.41 | 15 | 0.65 | 0.71 | agree |
| x | 1000 | 0.44 | 0.22 | 0.32 | 15 | 0.50 | 0.63 | agree |
| x | 2000 | 0.47 | 0.34 | 0.25 | 15 | 0.73 | 0.50 | agree |
| x | 3000 | 0.13 | 0.17 | 0.18 | 15 | 0.63 | 0.79 | agree |
| x | 4000 | 0.21 | 0.39 | 0.30 | 15 | 0.89 | 0.61 | agree |
| x | 5000 | 0.28 | 0.21 | 0.21 | 15 | 0.64 | 0.50 | agree |
| y | 0 | 0.10 | 0.19 | 0.16 | 15 | 0.50 | 0.50 | agree |
| y | 1000 | 0.23 | 0.59 | 0.49 | 15 | 0.86 | 0.66 | agree |
| y | 2000 | 0.11 | 0.37 | 0.34 | 15 | 1.06 | 1.03 | agree |
| y | 3000 | 0.15 | 0.25 | 0.29 | 15 | 0.50 | 0.53 | agree |
| y | 4000 | 0.48 | 0.25 | 0.23 | 15 | 0.69 | 0.50 | agree |
| y | 5000 | 0.20 | 0.51 | 0.44 | 15 | 0.68 | 0.77 | agree |
| y | 6000 | 0.88 | 0.58 | 0.23 | 23 | 1.47 | 0.61 | agree |

Both maps along every verified line and every interval midline (268 places): largest difference 1.581 in x (tolerance 4.368, claude 1000), 1.798 in y (tolerance 4.118, claude 4000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 13 shared lines checked against the ink, mean of the median distances 0.34 px (claude: x 0.28, y 0.39), 0.30 px (codex: x 0.28, y 0.31), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

4 series in claude, 5 in codex.
Only in codex: FC-5A/1/


## Points

Matched: 85; agreed 81; disagreed 4; unmatched 9 (kept as one-sided: 0 of claude, 9 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
|  | marker | -/1 | (none) | 310.7, 237.3 | | | unmatched in claude |
| dr30 | marker | 2/2 | 1325.7, 862.6 (4.4, 4.8) | 1327.0, 847.7 (7.9, 7.9) | -1.3 | +14.9 | **disagree** |
| dr30 | marker | 3/3 | 1804.4, 1107.8 (4.6, 6.6) | 1809.5, 1087.9 (6.1, 6.3) | -5.0 | +19.9 | **disagree** |
| dr30 | marker | 5/5 | 4063.4, 2659.4 (5.0, 4.6) | 4063.4, 2647.8 (6.2, 6.3) | -0.0 | +11.6 | **disagree** |
| dr48 | marker | 5/5 | 3680.7, 2667.0 (4.8, 11.4) | 3706.0, 2668.9 (6.2, 11.4) | -25.3 | -1.9 | **disagree** |
