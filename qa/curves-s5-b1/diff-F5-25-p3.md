# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s5-b1\rederived\claude\F5-25\points-p3-native.csv` (claude), `<repository>\qa\curves-s5-b1\rederived\codex\F5-25\points-p3-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 654 | 699 |
| x per px | 0.0001 | 0.0001 |
| y per px | 0.2343 | 0.2344 |
| RMS residual x, y | 0.000, 0.120 | 0.000, 0.158 |

Corners of claude's box [1830, 1810, 2300, 3540] mapped by both calibrations (tolerance 0.00 in x, 0.51 in y):

- (0.1, -103.9) vs (0.1, -103.9)
- (0.1, 6.2) vs (0.1, 6.2)
- (-0.0, -103.1) vs (-0.0, -103.1)
- (-0.0, 7.1) vs (-0.0, 7.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.66 | 0.15 | 0.32 | 7 | 0.50 | 1.12 | agree |
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
| y | -100 | 0.04 | 0.17 | 0.18 | 24 | 0.50 | 0.50 | agree |
| y | -80 | 0.03 | 0.21 | 0.20 | 24 | 0.50 | 0.52 | agree |
| y | -60 | 0.04 | 0.32 | 0.31 | 23 | 0.66 | 0.50 | agree |
| y | -40 | 0.05 | 0.40 | 0.37 | 24 | 0.50 | 0.50 | agree |
| y | -20 | 0.06 | 0.37 | 0.36 | 23 | 0.60 | 0.66 | agree |
| y | 0 | 0.07 | 0.32 | 0.32 | 23 | 0.51 | 1.11 | agree |

Both maps along every verified line and every interval midline (397 places): largest difference 6.246e-05 in x (tolerance 0.0001185, claude 0.1), 0.01863 in y (tolerance 0.405, claude 0); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.26 px (claude: x 0.24, y 0.30), 0.33 px (codex: x 0.35, y 0.29), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 64; agreed 64; disagreed 0; unmatched 3 (kept as one-sided: 0 of claude, 3 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| strut1 | feature | -/38 | (none) | 0.0, -65.1 | | | unmatched in claude |
| strut1 | feature | -/51 | (none) | 0.1, -73.8 | | | unmatched in claude |
| strut1 | feature | -/61 | (none) | 0.1, -33.0 | | | unmatched in claude |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
