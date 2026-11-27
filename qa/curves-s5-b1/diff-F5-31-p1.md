# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s5-b1\rederived\claude\F5-31\points-p1-native.csv` (claude), `<repository>\qa\curves-s5-b1\rederived\codex\F5-31\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 77 | 88 |
| x per px | 0.0000 | 0.0000 |
| y per px | 0.0041 | 0.0041 |
| RMS residual x, y | 0.000, 0.007 | 0.000, 0.006 |

Corners of claude's box [670, 1040, 2235, 3545] mapped by both calibrations (tolerance 0.00 in x, 0.02 in y):

- (0.1, 5.2) vs (0.1, 5.2)
- (0.1, -1.2) vs (0.1, -1.2)
- (-0.0, 5.3) vs (-0.0, 5.3)
- (-0.0, -1.1) vs (-0.0, -1.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.43 | 0.33 | 0.29 | 18 | 0.76 | 0.51 | agree |
| x | 0.01 | 0.00 | 0.23 | 0.23 | 18 | 0.58 | 0.55 | agree |
| x | 0.02 | 0.19 | 0.35 | 0.33 | 18 | 0.50 | 0.60 | agree |
| x | 0.03 | 0.48 | 0.23 | 0.23 | 18 | 0.52 | 0.65 | agree |
| x | 0.04 | 0.11 | 0.37 | 0.40 | 18 | 0.67 | 0.75 | agree |
| x | 0.05 | 0.34 | 0.34 | 0.34 | 18 | 0.60 | 0.51 | agree |
| x | 0.06 | 0.13 | 0.36 | 0.31 | 18 | 0.75 | 0.50 | agree |
| x | 0.07 | 0.52 | 0.37 | 0.32 | 18 | 0.66 | 0.69 | agree |
| x | 0.08 | 0.06 | 0.29 | 0.29 | 18 | 0.64 | 0.65 | agree |
| x | 0.09 | 0.21 | 0.33 | 0.37 | 18 | 0.85 | 0.65 | agree |
| x | 0.1 | 0.32 | 0.31 | 0.29 | 18 | 0.58 | 0.69 | agree |
| y | -1 | 0.30 | 0.27 | 0.26 | 25 | 0.55 | 0.61 | agree |
| y | 0 | 0.35 | 0.24 | 0.23 | 25 | 0.91 | 0.68 | agree |
| y | 1 | 0.25 | 0.25 | 0.27 | 25 | 0.50 | 0.87 | agree |
| y | 2 | 0.65 | 0.29 | 0.28 | 25 | 0.71 | 0.55 | agree |
| y | 3 | 0.30 | 0.22 | 0.28 | 25 | 0.58 | 0.70 | agree |
| y | 4 | 0.75 | 0.39 | 0.24 | 25 | 1.13 | 0.52 | agree |
| y | 5 | 0.72 | 0.22 | 0.26 | 25 | 0.93 | 0.51 | agree |
| y | 5.5 | | | | | | 0.55 | only in codex |

Both maps along every verified line and every interval midline (368 places): largest difference 1.863e-05 in x (tolerance 5.481e-05, codex 0.07), 0.003192 in y (tolerance 0.006752, codex 5); 0 beyond the two maps' line errors.

Canonical reading: codex (codex's lines include all of claude's and more, as close to the ink; 18 shared lines checked against the ink, mean of the median distances 0.30 px (claude: x 0.32, y 0.27), 0.29 px (codex: x 0.31, y 0.26)); points are evaluated at codex's samples.

## Series

1 series in codex, 1 in claude.


## Points

Matched: 36; agreed 35; disagreed 1; unmatched 4 (kept as one-sided: 1 of codex, 3 of claude).

| series | kind | seq (codex/claude) | codex x, y (bounds) | claude x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| pen | feature | 36/- | 0.1, 4.0 | (none) | | | unmatched in claude |
| pen | feature | 18/2 | 0.0, 2.0 (0.0, 0.0) | 0.0, 1.9 (0.0, 0.0) | +0.0 | +0.1 | **disagree** |
| pen | feature | -/4 | (none) | 0.1, 4.2 | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
