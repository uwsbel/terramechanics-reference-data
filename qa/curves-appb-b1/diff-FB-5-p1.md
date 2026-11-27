# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appb-b1\rederived\claude\FB-5\points-p1-native.csv` (claude), `<repository>\qa\curves-appb-b1\rederived\codex\FB-5\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 25 | 615 |
| x per px | 0.0056 | 0.0056 |
| y per px | 0.0112 | 0.0112 |
| RMS residual x, y | 0.008, 0.018 | 0.010, 0.018 |

Corners of claude's box [600, 800, 2900, 4050] mapped by both calibrations (tolerance 0.02 in x, 0.05 in y):

- (-0.3, 40.9) vs (-0.3, 40.9)
- (12.7, 40.6) vs (12.7, 40.5)
- (-0.6, 4.4) vs (-0.6, 4.5)
- (12.4, 4.1) vs (12.4, 4.0)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.26 | 0.50 | 0.44 | 23 | 0.94 | 0.76 | agree |
| x | 2 | 0.75 | 0.51 | 0.38 | 8 | 0.50 | 0.50 | agree |
| x | 4 | 0.12 | 0.14 | 0.06 | 8 | 0.50 | 0.50 | agree |
| x | 6 | 0.34 | 0.32 | 0.06 | 8 | 0.50 | 0.50 | agree |
| x | 8 | 0.34 | 0.29 | 0.07 | 9 | 2.55 | 0.50 | agree |
| x | 10 | 0.22 | 0.36 | 0.14 | 9 | 1.10 | 0.50 | agree |
| x | 12 | 0.08 | 0.42 | 0.41 | 23 | 0.89 | 0.84 | agree |
| y | 5 | 0.04 | 0.38 | 0.38 | 23 | 0.72 | 0.74 | agree |
| y | 10 | 0.37 | 0.29 | 0.04 | 8 | 0.50 | 0.50 | agree |
| y | 15 | 0.33 | 0.24 | 0.04 | 8 | 0.50 | 0.50 | agree |
| y | 20 | 0.32 | 0.25 | 0.36 | 8 | 0.50 | 0.61 | agree |
| y | 25 | 0.43 | 0.31 | 0.08 | 8 | 0.50 | 0.50 | agree |
| y | 30 | 0.67 | 0.54 | 0.17 | 8 | 0.50 | 0.50 | agree |
| y | 35 | 0.95 | 0.62 | 0.34 | 8 | 0.58 | 0.50 | agree |
| y | 40 | 0.02 | 0.23 | 0.21 | 23 | 0.77 | 0.57 | agree |

Both maps along every verified line and every interval midline (303 places): largest difference 0.008068 in x (tolerance 0.008124, codex 2), 0.03936 in y (tolerance 0.0125, codex 20); 73 beyond the two maps' line errors.

Canonical reading: claude (same lines; 15 shared lines checked against the ink, mean of the median distances 0.36 px (claude: x 0.36, y 0.36), 0.21 px (codex: x 0.22, y 0.20), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

2 series in claude, 2 in codex.


## Points

Matched: 35; agreed 35; disagreed 0; unmatched 6 (kept as one-sided: 0 of claude, 6 of codex).

No point disagreements.

## Ink check (D-031): 4 trace samples excluded

Overrides of hand decisions (3), for review:

- claude dr84 trace 1: hand decision one-sided-verified (on the ink of the drawn line, verified on the page by codex's adjudicator; blind adjudication item 0)
- claude dr26 trace 4: hand decision resolved (the claude reading is on the drawn line; credit claude (blind adjudication item 014 (Claude's adjudi)
- claude dr26 trace 5: hand decision resolved (the claude reading is on the drawn line; credit claude (blind adjudication item 015 (Claude's adjudi)
