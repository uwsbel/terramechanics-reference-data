# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s5-b1\rederived\claude\F5-25\points-p2-native.csv` (claude), `<repository>\qa\curves-s5-b1\rederived\codex\F5-25\points-p2-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 477 | 517 |
| x per px | 0.0001 | 0.0001 |
| y per px | 0.2356 | 0.2355 |
| RMS residual x, y | 0.000, 0.186 | 0.000, 0.198 |

Corners of claude's box [1405, 1810, 1690, 3540] mapped by both calibrations (tolerance 0.00 in x, 0.62 in y):

- (0.1, 63.9) vs (0.1, 63.9)
- (0.1, -3.2) vs (0.1, -3.2)
- (-0.0, 63.0) vs (-0.0, 63.0)
- (-0.0, -4.2) vs (-0.0, -4.2)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.30 | 0.12 | 0.15 | 4 | 0.50 | 1.12 | agree |
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
| y | 0 | 0.06 | 0.29 | 0.29 | 25 | 0.50 | 0.50 | agree |
| y | 20 | 0.03 | 0.16 | 0.16 | 24 | 0.50 | 0.50 | agree |
| y | 40 | 0.02 | 0.27 | 0.28 | 22 | 0.72 | 0.63 | agree |
| y | 60 | 0.18 | 0.23 | 0.17 | 24 | 0.57 | 0.50 | agree |

Both maps along every verified line and every interval midline (340 places): largest difference 0.000102 in x (tolerance 8.683e-05, codex 0.01), 0.05057 in y (tolerance 0.3252, codex 60); 4 beyond the two maps' line errors.

Canonical reading: claude (same lines; 15 shared lines checked against the ink, mean of the median distances 0.24 px (claude: x 0.23, y 0.24), 0.31 px (codex: x 0.34, y 0.22), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 45; agreed 45; disagreed 0; unmatched 3 (kept as one-sided: 2 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| strut2 | feature | 1/- | 0.0, 1.0 | (none) | | | unmatched in codex |
| strut2 | feature | -/40 | (none) | 0.1, 34.4 | | | unmatched in claude |
| strut2 | trace | 1/- | 0.0, 1.0 (0.0, 0.8) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
