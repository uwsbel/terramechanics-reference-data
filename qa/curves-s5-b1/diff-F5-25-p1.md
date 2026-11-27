# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s5-b1\rederived\claude\F5-25\points-p1-native.csv` (claude), `<repository>\qa\curves-s5-b1\rederived\codex\F5-25\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 379 | 386 |
| x per px | 0.0001 | 0.0001 |
| y per px | 0.2337 | 0.2337 |
| RMS residual x, y | 0.000, 0.116 | 0.000, 0.140 |

Corners of claude's box [975, 1810, 1265, 3540] mapped by both calibrations (tolerance 0.00 in x, 0.49 in y):

- (0.1, 65.2) vs (0.1, 65.2)
- (0.1, -2.6) vs (0.1, -2.6)
- (-0.0, 63.9) vs (-0.0, 63.9)
- (-0.0, -3.8) vs (-0.0, -3.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.74 | 0.25 | 0.95 | 3 | 0.50 | 1.12 | agree |
| x | 0.01 | 2.76 | 0.40 | 0.64 | 23 | 0.95 | 0.51 | **disagree** |
| x | 0.02 | 1.52 | 0.10 | 0.12 | 22 | 0.50 | 0.50 | **disagree** |
| x | 0.03 | 0.24 | 0.24 | 0.04 | 21 | 0.50 | 0.50 | agree |
| x | 0.04 | 0.35 | 0.31 | 0.17 | 25 | 0.50 | 0.50 | agree |
| x | 0.05 | 0.15 | 0.12 | 0.14 | 13 | 0.50 | 0.50 | agree |
| x | 0.06 | 1.08 | 0.35 | 0.50 | 23 | 0.50 | 0.50 | **disagree** |
| x | 0.07 | 0.57 | 0.17 | 0.44 | 27 | 0.50 | 0.50 | agree |
| x | 0.08 | 1.25 | 0.26 | 0.31 | 21 | 0.50 | 0.50 | **disagree** |
| x | 0.09 | 1.17 | 0.17 | 0.04 | 15 | 0.50 | 0.50 | **disagree** |
| x | 0.1 | 2.61 | 0.34 | 1.16 | 15 | 1.50 | 0.50 | **disagree**; codex off the ink |
| y | 0 | 0.26 | 0.33 | 0.25 | 22 | 0.78 | 0.52 | agree |
| y | 20 | 0.44 | 0.36 | 0.51 | 13 | 0.83 | 0.50 | agree |
| y | 40 | 0.06 | 0.33 | 0.36 | 16 | 0.55 | 0.50 | agree |
| y | 60 | 0.28 | 0.65 | 0.52 | 6 | 0.66 | 0.74 | agree |

Both maps along every verified line and every interval midline (340 places): largest difference 0.0001394 in x (tolerance 8.677e-05, codex 0.01), 0.1065 in y (tolerance 0.313, codex 20); 59 beyond the two maps' line errors.

Canonical reading: claude (same lines; 15 shared lines checked against the ink, mean of the median distances 0.29 px (claude: x 0.25, y 0.42), 0.41 px (codex: x 0.41, y 0.41), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 48; agreed 47; disagreed 1; unmatched 1 (kept as one-sided: 0 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| strut3 | feature | 2/4 | 0.0, 1.1 (0.0, 0.9) | 0.0, 3.8 (0.0, 0.7) | -0.0 | -2.7 | **disagree** |
| strut3 | feature | -/42 | (none) | 0.1, 43.1 | | | unmatched in claude |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
