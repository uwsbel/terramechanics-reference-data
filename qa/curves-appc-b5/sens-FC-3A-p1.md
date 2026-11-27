# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b5\rederived\claude\FC-3A\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b5\rederived\codex\FC-3A\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 12 | 13 |
| x per px | 3.4309 | 3.4275 |
| y per px | 3.4285 | 3.4258 |
| RMS residual x, y | 5.056, 13.080 | 3.404, 12.825 |

Corners of claude's box [910, 1450, 2385, 3215] mapped by both calibrations (tolerance 11.89 in x, 29.33 in y):

- (-19.9, 5998.8) vs (-21.6, 5997.2)
- (5040.7, 6031.0) vs (5033.9, 6028.2)
- (-34.1, -52.4) vs (-33.8, -49.3)
- (5026.5, -20.1) vs (5021.7, -18.2)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.40 | 0.28 | 0.25 | 18 | 1.01 | 0.72 | agree |
| x | 1000 | 0.01 | 0.54 | 0.55 | 12 | 0.99 | 0.98 | agree |
| x | 2000 | 0.00 | 0.08 | 0.08 | 12 | 0.50 | 0.50 | agree |
| x | 3000 | 0.01 | 0.08 | 0.07 | 12 | 0.50 | 0.50 | agree |
| x | 4000 | 0.01 | 0.08 | 0.08 | 10 | 0.50 | 0.50 | agree |
| x | 5000 | 3.00 | 1.11 | 1.89 | 12 | 2.99 | 2.94 | agree; claude off the ink; codex off the ink |
| y | 0 | 0.87 | 0.97 | 0.52 | 15 | 1.94 | 1.01 | agree |
| y | 1000 | 0.00 | 0.10 | 0.09 | 12 | 0.50 | 0.50 | agree |
| y | 2000 | 0.01 | 0.09 | 0.09 | 12 | 0.50 | 0.50 | agree |
| y | 3000 | 0.01 | 0.10 | 0.10 | 12 | 0.50 | 0.50 | agree |
| y | 4000 | 0.50 | 0.27 | 0.24 | 12 | 0.50 | 0.50 | agree |
| y | 5000 | 0.01 | 0.29 | 0.29 | 12 | 0.50 | 0.50 | agree |
| y | 6000 | 0.01 | 0.96 | 0.96 | 12 | 2.37 | 2.27 | agree |

Both maps along every verified line and every interval midline (287 places): largest difference 12.24 in x (tolerance 20.71, codex 5000), 3.176 in y (tolerance 10.08, codex 0); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 13 shared lines checked against the ink, mean of the median distances 0.38 px (claude: x 0.36, y 0.40), 0.40 px (codex: x 0.49, y 0.33), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

2 series in claude, 2 in codex.


## Points

Matched: 54; agreed 54; disagreed 0; unmatched 4 (kept as one-sided: 2 of claude, 2 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| dr0-15 | trace | 21/- | 4977.5, 4218.6 (15.9, 11.0) | (no trace at this x) | | | unmatched in codex |
| dr100-130 | trace | 21/- | 4930.4, 5952.2 (14.7, 14.1) | (no trace at this x) | | | unmatched in codex |
