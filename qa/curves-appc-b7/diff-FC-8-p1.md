# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b7\rederived\claude\FC-8\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b7\rederived\codex\FC-8\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4419 | 3.4415 |
| y per px | 3.4263 | 3.4254 |
| RMS residual x, y | 4.143, 10.364 | 4.008, 10.432 |

Corners of claude's box [715, 1052, 2810, 3445] mapped by both calibrations (tolerance 11.59 in x, 24.22 in y):

- (-129.8, 8053.9) vs (-129.1, 8052.8)
- (7080.8, 8128.2) vs (7080.8, 8128.3)
- (-89.0, -144.7) vs (-88.3, -143.8)
- (7121.6, -70.5) vs (7121.6, -68.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.20 | 0.75 | 0.83 | 20 | 1.42 | 1.65 | agree |
| x | 1000 | 0.41 | 0.33 | 0.30 | 24 | 0.88 | 0.61 | agree |
| x | 2000 | 0.29 | 0.46 | 0.46 | 24 | 0.78 | 0.80 | agree |
| x | 3000 | 0.22 | 0.28 | 0.41 | 24 | 0.74 | 0.98 | agree |
| x | 4000 | 0.08 | 0.36 | 0.36 | 24 | 0.64 | 0.66 | agree |
| x | 5000 | 0.10 | 0.44 | 0.42 | 24 | 0.73 | 0.83 | agree |
| x | 6000 | 0.10 | 0.53 | 0.57 | 24 | 1.02 | 1.11 | agree |
| x | 7000 | 0.18 | 0.49 | 0.58 | 24 | 0.80 | 0.89 | agree |
| y | 0 | 1.08 | 0.93 | 0.40 | 21 | 1.73 | 0.73 | agree |
| y | 1000 | 0.58 | 0.60 | 0.37 | 21 | 1.23 | 0.74 | agree |
| y | 2000 | 0.09 | 0.38 | 0.37 | 21 | 0.84 | 0.80 | agree |
| y | 3000 | 0.81 | 0.49 | 0.43 | 21 | 1.60 | 0.84 | agree |
| y | 4000 | 0.31 | 0.39 | 0.23 | 21 | 1.02 | 0.74 | agree |
| y | 5000 | 0.18 | 0.26 | 0.34 | 21 | 0.60 | 0.77 | agree |
| y | 6000 | 0.56 | 0.42 | 0.34 | 21 | 1.17 | 0.62 | agree |
| y | 7000 | 0.29 | 0.55 | 0.59 | 21 | 0.97 | 1.17 | agree |
| y | 8000 | 0.08 | 0.58 | 0.58 | 21 | 1.36 | 1.43 | agree |

Both maps along every verified line and every interval midline (352 places): largest difference 1.493 in x (tolerance 7.601, claude 1000), 3.846 in y (tolerance 8.301, codex 0); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.49 px (claude: x 0.45, y 0.51), 0.45 px (codex: x 0.49, y 0.41), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 18; agreed 18; disagreed 0; unmatched 1 (kept as one-sided: 1 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| rs-loose | trace | 11/- | 4670.8, 3987.8 (14.5, 29.7) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
