# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b4\rederived\claude\F2-54\points-p2-native.csv` (claude), `<repository>\qa\curves-s2-b4\rederived\codex\F2-54\points-p2-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 267 | 198 |
| x per px | 0.0643 | 0.0644 |
| y per px | 0.0910 | 0.0915 |
| RMS residual x, y | 0.444, 0.134 | 0.434, 0.254 |

Corners of claude's box [945, 1300, 1385, 3050] mapped by both calibrations (tolerance 0.94 in x, 0.48 in y):

- (91.7, 33.9) vs (91.7, 34.2)
- (91.4, -6.1) vs (91.5, -6.1)
- (-20.9, 35.9) vs (-21.0, 35.9)
- (-21.2, -4.1) vs (-21.2, -4.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | -20 | 0.17 | 0.15 | 0.20 | 10 | 0.50 | 0.66 | agree |
| x | -10 | 0.08 | 0.15 | 0.17 | 15 | 0.50 | 0.50 | agree |
| x | 0 | 0.54 | 0.44 | 0.56 | 16 | 0.68 | 1.02 | agree |
| x | 10 | 0.27 | 0.33 | 0.27 | 15 | 0.71 | 0.50 | agree |
| x | 20 | 0.40 | 0.20 | 0.29 | 17 | 0.62 | 1.28 | agree |
| x | 30 | 0.17 | 0.20 | 0.23 | 15 | 0.52 | 0.50 | agree |
| x | 40 | 0.09 | 0.18 | 0.23 | 15 | 0.50 | 0.54 | agree |
| x | 50 | 0.29 | 0.30 | 0.29 | 15 | 0.50 | 0.69 | agree |
| x | 60 | 0.37 | 0.13 | 0.19 | 16 | 0.51 | 0.63 | agree |
| x | 70 | 0.34 | 0.23 | 0.22 | 16 | 0.50 | 0.50 | agree |
| x | 80 | 0.18 | 0.31 | 0.25 | 16 | 0.61 | 0.55 | agree |
| x | 90 | 0.33 | 0.13 | 0.25 | 16 | 0.50 | 0.50 | agree |
| y | 2 | | | | | | | claude's line not a knot: misplaced: tick 5.46 px from the ink (median of its stubs) |
| y | 11 | | | | | | | claude's line not a knot: misplaced: tick 5.79 px from the ink (median of its stubs) |
| y | 29 | | | | | | | claude's line not a knot: misplaced: tick 5.62 px from the ink (median of its stubs) |
| y | 2 | | | | | | | codex's line not a knot: misplaced: tick 5.56 px from the ink (median of its stubs) |
| y | 0 | 0.01 | 0.13 | 0.13 | 10 | 0.50 | 0.50 | agree |
| y | 3 | 0.13 | 0.19 | 0.11 | 6 | 0.50 | 0.50 | agree |
| y | 4 | 0.09 | 0.16 | 0.08 | 11 | 0.50 | 0.50 | agree |
| y | 5 | 0.12 | 0.28 | 0.29 | 4 | 0.50 | 0.59 | agree |
| y | 6 | 0.08 | 0.13 | 0.09 | 11 | 0.50 | 0.50 | agree |
| y | 7 | 0.08 | 0.11 | 0.05 | 5 | 0.50 | 0.50 | agree |
| y | 8 | 0.09 | 0.13 | 0.08 | 11 | 0.50 | 0.50 | agree |
| y | 9 | 0.14 | 0.18 | 0.06 | 4 | 0.50 | 0.50 | agree |
| y | 10 | 0.25 | 0.19 | 0.37 | 12 | 0.79 | 0.50 | agree |
| y | 12 | 0.07 | 0.16 | 0.09 | 12 | 0.79 | 0.50 | agree |
| y | 13 | 0.05 | 0.07 | 0.09 | 4 | 0.50 | 0.50 | agree |
| y | 14 | 0.07 | 0.14 | 0.10 | 11 | 0.50 | 0.50 | agree |
| y | 15 | 0.06 | 0.08 | 0.04 | 4 | 0.50 | 0.50 | agree |
| y | 16 | 0.05 | 0.56 | 0.57 | 10 | 0.70 | 0.72 | agree |
| y | 17 | 0.06 | 0.33 | 0.30 | 6 | 0.56 | 0.55 | agree |
| y | 18 | 0.05 | 0.08 | 0.09 | 10 | 0.78 | 0.50 | agree |
| y | 19 | 0.07 | 0.11 | 0.08 | 5 | 0.50 | 0.50 | agree |
| y | 20 | 0.36 | 0.25 | 0.09 | 11 | 0.50 | 0.50 | agree |
| y | 21 | 0.07 | 0.09 | 0.08 | 4 | 0.50 | 0.50 | agree |
| y | 22 | 0.07 | 0.37 | 0.34 | 11 | 0.50 | 0.56 | agree |
| y | 23 | 0.13 | 0.59 | 0.49 | 4 | 0.78 | 0.71 | agree |
| y | 24 | 0.06 | 0.13 | 0.08 | 10 | 0.50 | 0.50 | agree |
| y | 25 | 0.08 | 0.05 | 0.07 | 4 | 0.50 | 0.50 | agree |
| y | 26 | 0.06 | 0.13 | 0.10 | 10 | 0.50 | 0.50 | agree |
| y | 27 | 0.13 | 0.55 | 0.44 | 5 | 0.91 | 0.71 | agree |
| y | 28 | 0.07 | 0.23 | 0.16 | 10 | 0.50 | 0.50 | agree |
| y | 30 | 0.74 | 0.75 | 0.12 | 12 | 1.68 | 0.50 | agree |
| y | 11 | | | | | | 0.50 | only in codex |
| y | 29 | | | | | | 0.50 | only in codex |

Both maps along every verified line and every interval midline (873 places): largest difference 0.03866 in x (tolerance 0.1111, claude 0), 0.5195 in y (tolerance 0.2476, codex 29); 244 beyond the two maps' line errors.

Canonical reading: codex (codex's lines include all of claude's and more, as close to the ink; 39 shared lines checked against the ink, mean of the median distances 0.23 px (claude: x 0.23, y 0.23), 0.20 px (codex: x 0.26, y 0.17)); points are evaluated at codex's samples.

## Series

1 series in codex, 1 in claude.


## Points

Matched: 92; agreed 91; disagreed 1; unmatched 8 (kept as one-sided: 7 of codex, 1 of claude).

| series | kind | seq (codex/claude) | codex x, y (bounds) | claude x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| r54025 | feature | 54/- | 17.2, 14.9 | (none) | | | unmatched in claude |
| r54025 | feature | 20/17 | 8.9, 0.5 (0.6, 0.9) | 9.9, 1.0 (0.4, 0.6) | -1.1 | -0.5 | **disagree** |
| r54025 | feature | -/81 | (none) | 74.6, 0.2 | | | unmatched in codex |
| r54025 | feature | 71/- | 36.4, 6.2 | (none) | | | unmatched in claude |
| r54025 | trace | 13/- | 4.0, 0.0 (0.4, 0.7) | (no trace at this x) | | | unmatched in claude |
| r54025 | trace | 14/- | 6.0, 0.1 (0.4, 0.8) | (no trace at this x) | | | unmatched in claude |
| r54025 | trace | 15/- | 6.5, 0.0 (0.4, 0.8) | (no trace at this x) | | | unmatched in claude |
| r54025 | trace | 16/- | 7.0, 0.1 (0.4, 0.8) | (no trace at this x) | | | unmatched in claude |
| r54025 | trace | 17/- | 7.5, 0.1 (0.3, 0.5) | (no trace at this x) | | | unmatched in claude |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
