# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b7\rederived\claude\FC-9C\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b7\rederived\codex\FC-9C\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4327 | 3.4331 |
| y per px | 3.4247 | 3.4249 |
| RMS residual x, y | 4.241, 10.166 | 3.966, 10.271 |

Corners of claude's box [530, 1402, 2615, 3782] mapped by both calibrations (tolerance 11.64 in x, 23.86 in y):

- (-65.1, 8072.2) vs (-64.4, 8072.5)
- (7091.9, 8069.8) vs (7093.4, 8070.5)
- (-109.4, -78.5) vs (-110.4, -78.8)
- (7047.6, -80.9) vs (7047.5, -80.7)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.36 | 0.43 | 0.28 | 23 | 1.30 | 0.95 | agree |
| x | 1000 | 0.41 | 0.24 | 0.29 | 24 | 0.55 | 0.69 | agree |
| x | 2000 | 0.35 | 0.46 | 0.48 | 24 | 0.95 | 0.94 | agree |
| x | 3000 | 0.18 | 0.23 | 0.25 | 24 | 0.72 | 0.53 | agree |
| x | 4000 | 0.75 | 0.36 | 0.34 | 24 | 0.93 | 0.85 | agree |
| x | 5000 | 0.31 | 0.34 | 0.36 | 24 | 0.81 | 0.85 | agree |
| x | 6000 | 0.69 | 0.40 | 0.50 | 24 | 0.63 | 1.08 | agree |
| x | 7000 | 0.39 | 0.44 | 0.37 | 24 | 1.02 | 0.67 | agree |
| y | 0 | 0.09 | 0.12 | 0.08 | 21 | 0.50 | 0.50 | agree |
| y | 1000 | 0.00 | 0.11 | 0.11 | 21 | 0.50 | 0.50 | agree |
| y | 2000 | 0.14 | 0.11 | 0.11 | 21 | 0.50 | 0.50 | agree |
| y | 3000 | 0.00 | 0.00 | 0.00 | 21 | 0.53 | 0.53 | agree |
| y | 4000 | 0.40 | 0.13 | 0.22 | 21 | 0.50 | 0.51 | agree |
| y | 5000 | 0.29 | 0.45 | 0.57 | 21 | 0.81 | 1.03 | agree |
| y | 6000 | 0.18 | 0.21 | 0.18 | 21 | 0.50 | 0.50 | agree |
| y | 7000 | 0.00 | 0.23 | 0.23 | 21 | 0.76 | 0.77 | agree |
| y | 8000 | 0.19 | 0.73 | 0.79 | 21 | 1.29 | 1.48 | agree |

Both maps along every verified line and every interval midline (414 places): largest difference 2.004 in x (tolerance 6.12, claude 4000), 1.496 in y (tolerance 5.388, claude 4000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.29 px (claude: x 0.36, y 0.23), 0.30 px (codex: x 0.36, y 0.25), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 23; agreed 21; disagreed 2; unmatched 1 (kept as one-sided: 0 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| rs-dense | marker | 7/7 | 2335.5, 3812.5 (5.0, 10.4) | 2324.7, 3809.6 (4.9, 9.5) | +10.8 | +2.9 | **disagree** |
| rs-dense | marker | 8/9 | 2941.7, 4498.3 (5.6, 10.7) | 2925.4, 4500.6 (9.7, 15.3) | +16.3 | -2.4 | **disagree** |
