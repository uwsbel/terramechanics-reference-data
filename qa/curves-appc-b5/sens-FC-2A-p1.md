# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b5\rederived\claude\FC-2A\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b5\rederived\codex\FC-2A\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 12 | 13 |
| x per px | 3.4377 | 3.4384 |
| y per px | 3.4140 | 3.4179 |
| RMS residual x, y | 14.165, 14.961 | 13.552, 15.668 |

Corners of claude's box [945, 1465, 2435, 3395] mapped by both calibrations (tolerance 31.16 in x, 34.05 in y):

- (-84.1, 6484.9) vs (-80.6, 6488.2)
- (5037.8, 6548.2) vs (5042.3, 6556.4)
- (-9.4, -103.6) vs (-11.0, -107.7)
- (5112.5, -40.3) vs (5112.0, -39.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 1.16 | 0.34 | 0.53 | 18 | 0.55 | 1.77 | agree |
| x | 1000 | 0.17 | 0.27 | 0.40 | 12 | 0.60 | 0.73 | agree |
| x | 2000 | 0.17 | 0.15 | 0.08 | 12 | 0.50 | 0.50 | agree |
| x | 3000 | 0.18 | 0.11 | 0.17 | 12 | 0.50 | 0.50 | agree |
| x | 4000 | 0.18 | 0.34 | 0.20 | 12 | 0.52 | 0.50 | agree |
| x | 5000 | 1.02 | 0.43 | 1.43 | 8 | 1.08 | 1.87 | agree; codex off the ink |
| y | 0 | 0.32 | 0.27 | 0.23 | 15 | 0.50 | 0.50 | agree |
| y | 1000 | 0.02 | 0.74 | 0.76 | 12 | 1.38 | 1.37 | agree |
| y | 2000 | 0.02 | 0.35 | 0.36 | 12 | 1.19 | 1.23 | agree |
| y | 3000 | 1.89 | 0.32 | 1.75 | 12 | 1.38 | 1.77 | agree; codex off the ink |
| y | 4000 | 0.02 | 0.13 | 0.14 | 12 | 0.50 | 0.50 | agree |
| y | 5000 | 0.02 | 0.20 | 0.19 | 12 | 0.70 | 0.69 | agree |
| y | 6000 | 0.03 | 0.76 | 0.74 | 12 | 0.89 | 0.95 | agree |

Both maps along every verified line and every interval midline (263 places): largest difference 4.923 in x (tolerance 4.796, codex 2000), 10.6 in y (tolerance 10.79, codex 3000); 19 beyond the two maps' line errors.

Canonical reading: claude (same lines; 13 shared lines checked against the ink, mean of the median distances 0.34 px (claude: x 0.27, y 0.40), 0.54 px (codex: x 0.47, y 0.59), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

2 series in claude, 2 in codex.


## Points

Matched: 50; agreed 49; disagreed 1; unmatched 4 (kept as one-sided: 3 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| dr115-130 | feature | 1/1 | 0.1, 186.5 (9.6, 10.6) | -0.2, 210.6 (11.4, 10.3) | +0.3 | -24.1 | **disagree** |
| dr115-130 | trace | 1/- | 0.1, 186.5 (9.6, 10.6) | (no trace at this x) | | | unmatched in codex |
| dr115-130 | trace | 19/- | 4850.2, 5305.6 (10.8, 10.7) | (no trace at this x) | | | unmatched in codex |
| dr33-53 | trace | 1/- | -0.1, 400.1 (9.1, 10.4) | (no trace at this x) | | | unmatched in codex |
