# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b11\rederived\claude\FC-23\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b11\rederived\codex\FC-23\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 55 | 55 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0131 | 0.0131 |
| RMS residual x, y | 0.002, 0.039 | 0.002, 0.039 |

Corners of claude's box [815, 1345, 2620, 3570] mapped by both calibrations (tolerance 0.01 in x, 0.09 in y):

- (-0.1, 54.7) vs (-0.1, 54.7)
- (1.1, 54.5) vs (1.1, 54.5)
- (-0.1, 25.6) vs (-0.1, 25.6)
- (1.1, 25.4) vs (1.1, 25.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.37 | 0.45 | 0.25 | 12 | 0.86 | 0.84 | agree |
| x | 0.1 | 0.34 | 0.18 | 0.19 | 12 | 0.68 | 0.50 | agree |
| x | 0.2 | 0.20 | 0.41 | 0.32 | 11 | 0.79 | 0.57 | agree |
| x | 0.3 | 0.32 | 0.22 | 0.23 | 12 | 0.50 | 0.52 | agree |
| x | 0.4 | 0.21 | 0.29 | 0.26 | 12 | 0.71 | 1.19 | agree |
| x | 0.5 | 0.69 | 0.61 | 0.42 | 12 | 1.63 | 1.12 | agree |
| x | 0.6 | 0.70 | 0.36 | 0.38 | 12 | 1.55 | 0.95 | agree |
| x | 0.7 | 0.38 | 0.30 | 0.21 | 12 | 0.83 | 0.50 | agree |
| x | 0.8 | 0.20 | 0.24 | 0.28 | 12 | 0.65 | 0.50 | agree |
| x | 0.9 | 0.53 | 0.46 | 0.38 | 12 | 0.83 | 0.63 | agree |
| x | 1 | 0.64 | 0.53 | 0.35 | 12 | 0.82 | 0.64 | agree |
| y | 30 | 0.47 | 0.35 | 0.32 | 25 | 0.97 | 0.59 | agree |
| y | 35 | 0.34 | 0.42 | 0.30 | 25 | 0.66 | 0.68 | agree |
| y | 40 | 0.32 | 0.29 | 0.33 | 25 | 1.01 | 0.80 | agree |
| y | 45 | 0.59 | 0.80 | 0.63 | 25 | 2.02 | 1.38 | agree |
| y | 50 | 1.00 | 0.57 | 0.51 | 22 | 0.96 | 1.22 | agree |

Both maps along every verified line and every interval midline (318 places): largest difference 0.0004984 in x (tolerance 0.001664, claude 0.6), 0.01183 in y (tolerance 0.04536, claude 50); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 16 shared lines checked against the ink, mean of the median distances 0.41 px (claude: x 0.37, y 0.49), 0.34 px (codex: x 0.30, y 0.42), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

6 series in claude, 6 in codex.


## Points

Matched: 160; agreed 156; disagreed 4; unmatched 4 (kept as one-sided: 0 of claude, 4 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| ps | trace | 6/interp | 0.2, 43.7 (0.0, 0.1) | 0.2, 44.0 (0.0, 0.1) | slope +0.4 | -0.3 (tol 0.2) | **disagree** |
| ps | trace | 19/interp | 0.8, 47.9 (0.0, 0.1) | 0.8, 47.6 (0.0, 0.1) | slope +0.7 | +0.3 (tol 0.2) | **disagree** |
| rs | trace | 18/interp | 0.8, 46.9 (0.0, 0.1) | 0.8, 47.3 (0.0, 0.1) | slope +7.0 | -0.4 (tol 0.2) | **disagree** |
| rs | trace | 19/interp | 0.8, 47.3 (0.0, 0.1) | 0.8, 47.6 (0.0, 0.1) | slope +0.8 | -0.3 (tol 0.2) | **disagree** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
