# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s5-b1\rederived\claude\F5-24\points-p1-native.csv` (claude), `<repository>\qa\curves-s5-b1\rederived\codex\F5-24\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 77 | 88 |
| x per px | 0.0000 | 0.0000 |
| y per px | 0.0041 | 0.0041 |
| RMS residual x, y | 0.000, 0.006 | 0.000, 0.006 |

Corners of claude's box [700, 1060, 2340, 3580] mapped by both calibrations (tolerance 0.00 in x, 0.02 in y):

- (0.1, 6.5) vs (0.1, 6.5)
- (0.1, -0.2) vs (0.1, -0.2)
- (-0.0, 6.6) vs (-0.0, 6.6)
- (-0.0, -0.1) vs (-0.0, -0.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.14 | 0.32 | 0.30 | 18 | 0.50 | 0.50 | agree |
| x | 0.01 | 0.17 | 0.25 | 0.33 | 18 | 0.50 | 0.67 | agree |
| x | 0.02 | 0.40 | 0.23 | 0.21 | 18 | 0.62 | 0.61 | agree |
| x | 0.03 | 0.04 | 0.36 | 0.33 | 18 | 0.65 | 0.71 | agree |
| x | 0.04 | 0.37 | 0.32 | 0.28 | 18 | 0.73 | 0.50 | agree |
| x | 0.05 | 0.08 | 0.17 | 0.16 | 18 | 0.50 | 0.50 | agree |
| x | 0.06 | 0.07 | 0.36 | 0.38 | 18 | 0.69 | 0.58 | agree |
| x | 0.07 | 0.46 | 0.41 | 0.22 | 18 | 1.00 | 0.50 | agree |
| x | 0.08 | 0.30 | 0.43 | 0.34 | 18 | 0.98 | 0.71 | agree |
| x | 0.09 | 0.21 | 0.26 | 0.37 | 18 | 0.94 | 0.72 | agree |
| x | 0.1 | 0.48 | 0.25 | 0.35 | 18 | 0.58 | 0.55 | agree |
| y | 0 | 0.34 | 0.27 | 0.24 | 25 | 0.65 | 0.50 | agree |
| y | 1 | 0.29 | 0.28 | 0.27 | 25 | 0.78 | 0.65 | agree |
| y | 2 | 0.18 | 0.19 | 0.18 | 25 | 0.50 | 0.60 | agree |
| y | 3 | 0.39 | 0.27 | 0.17 | 25 | 0.65 | 0.50 | agree |
| y | 4 | 0.03 | 0.18 | 0.17 | 25 | 0.50 | 0.50 | agree |
| y | 5 | 0.36 | 0.26 | 0.24 | 25 | 0.55 | 0.50 | agree |
| y | 6 | 0.30 | 0.24 | 0.17 | 25 | 0.64 | 0.50 | agree |
| y | 7 | | | | | | 0.89 | only in codex |

Both maps along every verified line and every interval midline (371 places): largest difference 2.132e-05 in x (tolerance 6.805e-05, codex 0.1), 0.009258 in y (tolerance 0.006293, between codex 6 and codex 7); 5 beyond the two maps' line errors.

Canonical reading: codex (codex's lines include all of claude's and more, as close to the ink; 18 shared lines checked against the ink, mean of the median distances 0.28 px (claude: x 0.31, y 0.24), 0.26 px (codex: x 0.30, y 0.21)); points are evaluated at codex's samples.

## Series

1 series in codex, 1 in claude.


## Points

Matched: 42; agreed 42; disagreed 0; unmatched 1 (kept as one-sided: 0 of codex, 1 of claude).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
