# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b3\rederived\claude\FC-5B\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b3\rederived\codex\FC-5B\points-p2-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 18 | 18 |
| x per px | 0.1690 | 0.1690 |
| y per px | 0.3381 | 0.3381 |
| RMS residual x, y | 0.905, 0.132 | 0.916, 0.131 |

Corners of claude's box [652, 2580, 2185, 3212] mapped by both calibrations (tolerance 1.99 in x, 0.60 in y):

- (-4.9, 106.7) vs (-4.9, 106.7)
- (254.1, 106.3) vs (254.1, 106.4)
- (-5.6, -106.9) vs (-5.6, -107.0)
- (253.4, -107.3) vs (253.5, -107.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.35 | 0.43 | 0.31 | 6 | 0.85 | 0.67 | agree |
| x | 50 | 0.18 | 0.30 | 0.22 | 6 | 0.79 | 0.80 | agree |
| x | 100 | 0.08 | 0.24 | 0.24 | 6 | 0.54 | 0.50 | agree |
| x | 150 | 0.45 | 0.21 | 0.26 | 21 | 1.71 | 1.73 | agree |
| x | 200 | 0.11 | 0.15 | 0.16 | 6 | 0.71 | 0.73 | agree |
| x | 250 | 0.35 | 0.84 | 0.94 | 5 | 1.58 | 1.95 | agree |
| y | -100 | 0.17 | 0.10 | 0.05 | 15 | 0.50 | 0.50 | agree |
| y | 0 | 0.12 | 0.25 | 0.24 | 15 | 0.83 | 0.66 | agree |
| y | 100 | 0.00 | 0.15 | 0.15 | 15 | 0.50 | 0.50 | agree |

Both maps along every verified line and every interval midline (200 places): largest difference 0.07334 in x (tolerance 0.5937, claude 250), 0.06116 in y (tolerance 0.507, claude -100); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.30 px (claude: x 0.36, y 0.17), 0.28 px (codex: x 0.35, y 0.15), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 65; agreed 43; disagreed 22; unmatched 0 (kept as one-sided: 0 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1761 | marker | 1/1 | -0.1, -16.0 (0.3, 0.6) | -1.1, -16.0 (0.5, 1.1) | +0.9 | +0.0 | **disagree** |
| n1761 | marker | 4/4 | 50.1, -23.9 (0.3, 0.6) | 51.1, -23.9 (0.6, 1.1) | -1.0 | +0.0 | **disagree** |
| n4695 | marker | 1/1 | -0.4, -50.8 (0.3, 0.6) | -0.4, -53.3 (0.6, 1.3) | +0.0 | +2.4 | **disagree** |
| n4695 | marker | 2/2 | 21.1, -51.0 (0.2, 0.5) | 21.1, -56.0 (0.2, 0.4) | +0.0 | +5.0 | **disagree** |
| n4695 | marker | 3/3 | 31.1, -51.9 (0.2, 0.5) | 30.8, -58.0 (0.2, 0.4) | +0.3 | +6.1 | **disagree** |
| n4695 | marker | 4/4 | 49.7, -52.9 (0.3, 0.6) | 49.7, -59.1 (0.6, 1.1) | +0.0 | +6.1 | **disagree** |
| n4695 | marker | 5/5 | 69.3, -51.0 (0.2, 0.5) | 68.6, -56.4 (0.2, 0.4) | +0.7 | +5.4 | **disagree** |
| n4695 | marker | 6/6 | 89.3, -53.0 (0.2, 0.4) | 89.2, -59.8 (0.2, 0.4) | +0.1 | +6.8 | **disagree** |
| n4695 | marker | 7/7 | 109.7, -51.9 (0.2, 0.4) | 109.4, -59.5 (0.2, 0.4) | +0.3 | +7.6 | **disagree** |
| n4695 | marker | 8/8 | 128.9, -51.9 (0.3, 0.4) | 128.7, -59.8 (0.3, 0.4) | +0.2 | +7.9 | **disagree** |
| n4695 | marker | 9/9 | 149.0, -50.9 (0.4, 0.6) | 149.2, -55.8 (0.7, 1.1) | -0.2 | +4.9 | **disagree** |
| n4695 | marker | 10/10 | 169.1, -51.3 (0.3, 0.4) | 168.1, -57.2 (0.3, 0.4) | +1.1 | +5.9 | **disagree** |
| n4695 | marker | 11/11 | 189.4, -51.0 (0.3, 0.4) | 188.5, -57.5 (0.3, 0.4) | +1.0 | +6.6 | **disagree** |
| n4695 | marker | 12/12 | 218.8, -50.7 (0.3, 0.4) | 218.0, -55.6 (0.3, 0.4) | +0.8 | +4.9 | **disagree** |
| n4695 | marker | 13/13 | 249.6, -50.1 (0.4, 0.6) | 249.6, -53.6 (0.8, 1.3) | +0.0 | +3.5 | **disagree** |
| n734 | marker | 2/2 | 21.2, -35.4 (0.2, 0.6) | 21.1, -38.7 (0.5, 0.9) | +0.1 | +3.3 | **disagree** |
| n734 | marker | 3/3 | 31.0, -36.4 (0.2, 0.6) | 30.9, -40.1 (0.5, 0.9) | +0.1 | +3.7 | **disagree** |
| n734 | marker | 4/4 | 49.8, -38.6 (0.3, 0.6) | 50.9, -38.4 (0.8, 1.5) | -1.1 | -0.2 | **disagree** |
| n734 | marker | 6/6 | 89.6, -36.7 (0.2, 0.6) | 89.2, -40.2 (0.5, 0.9) | +0.4 | +3.5 | **disagree** |
| n734 | marker | 8/8 | 128.9, -37.2 (0.3, 0.6) | 128.7, -40.9 (0.5, 0.9) | +0.1 | +3.7 | **disagree** |
| n734 | marker | 10/10 | 168.8, -35.7 (0.3, 0.6) | 168.1, -39.3 (0.6, 0.9) | +0.6 | +3.6 | **disagree** |
| n734 | marker | 11/11 | 189.1, -35.4 (0.3, 0.6) | 188.5, -39.4 (0.5, 0.9) | +0.6 | +3.9 | **disagree** |
