# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appb-b1\rederived\claude\FB-3\points-p1-native.csv` (claude), `<repository>\qa\curves-appb-b1\rederived\codex\FB-3\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 482 | 713 |
| x per px | 0.0071 | 0.0071 |
| y per px | 0.0036 | 0.0036 |
| RMS residual x, y | 0.006, 0.005 | 0.011, 0.007 |

Corners of claude's box [500, 780, 2580, 3980] mapped by both calibrations (tolerance 0.02 in x, 0.02 in y):

- (-0.4, 18.2) vs (-0.4, 18.2)
- (14.4, 18.2) vs (14.4, 18.2)
- (-0.3, 6.8) vs (-0.3, 6.8)
- (14.5, 6.8) vs (14.5, 6.8)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.08 | 0.34 | 0.38 | 25 | 0.60 | 0.62 | agree |
| x | 2 | 0.25 | 0.22 | 0.03 | 10 | 3.71 | 0.50 | agree |
| x | 4 | 0.26 | 0.27 | 0.02 | 8 | 0.50 | 0.50 | agree |
| x | 6 | 0.36 | 0.35 | 0.06 | 9 | 2.31 | 0.50 | agree |
| x | 8 | 0.28 | 0.47 | 0.19 | 11 | 1.84 | 0.50 | agree |
| x | 10 | 0.18 | 0.21 | 0.12 | 10 | 4.77 | 0.50 | agree |
| x | 12 | 0.38 | 0.36 | 0.13 | 11 | 2.94 | 0.50 | agree |
| x | 14 | 0.01 | 0.60 | 0.60 | 25 | 0.72 | 0.60 | agree |
| y | 7 | 0.11 | 0.51 | 0.56 | 25 | 0.78 | 0.81 | agree |
| y | 8 | 0.58 | 0.54 | 0.04 | 8 | 0.66 | 0.50 | agree |
| y | 9 | 0.68 | 0.42 | 0.31 | 8 | 0.56 | 0.50 | agree |
| y | 10 | 0.40 | 0.39 | 0.10 | 8 | 0.50 | 0.50 | agree |
| y | 11 | 0.75 | 0.59 | 0.16 | 8 | 0.66 | 0.50 | agree |
| y | 12 | 0.35 | 0.26 | 0.03 | 8 | 0.50 | 0.50 | agree |
| y | 13 | 0.44 | 0.52 | 0.13 | 8 | 0.50 | 0.50 | agree |
| y | 14 | 0.54 | 0.44 | 0.13 | 8 | 0.58 | 0.50 | agree |
| y | 15 | 0.05 | 0.12 | 0.09 | 8 | 0.50 | 0.50 | agree |
| y | 16 | 0.26 | 0.13 | 0.12 | 8 | 0.50 | 0.50 | agree |
| y | 17 | 0.53 | 0.43 | 0.06 | 9 | 2.00 | 0.50 | agree |
| y | 18 | 0.28 | 0.61 | 0.55 | 22 | 1.11 | 0.95 | agree |

Both maps along every verified line and every interval midline (419 places): largest difference 0.0222 in x (tolerance 0.0246, codex 12), 0.01606 in y (tolerance 0.003589, claude 13); 132 beyond the two maps' line errors.

Canonical reading: claude (same lines; 20 shared lines checked against the ink, mean of the median distances 0.39 px (claude: x 0.35, y 0.41), 0.19 px (codex: x 0.19, y 0.19), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

2 series in claude, 2 in codex.


## Points

Matched: 39; agreed 37; disagreed 2; unmatched 8 (kept as one-sided: 2 of claude, 6 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| dr30 | trace | 1/- | 3.9, 7.3 (0.0, 0.0) | (no trace at this x) | | | unmatched in codex |
| dr99 | marker | 4/- | 4.9, 13.9 | (none) | | | unmatched in codex |
| dr99 | trace | 4/interp | 4.9, 13.8 (0.0, 0.0) | 4.9, 13.5 (0.0, 0.0) | slope +1.1 | +0.3 (tol 0.1) | **disagree** |
| dr99 | trace | 5/interp | 5.0, 14.0 (0.0, 0.0) | 5.0, 13.7 (0.0, 0.0) | slope +1.1 | +0.3 (tol 0.1) | **disagree** |

## Ink check (D-031): 1 trace samples excluded

No hand decision overridden.
