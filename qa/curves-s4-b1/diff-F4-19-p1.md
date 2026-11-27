# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s4-b1\rederived\claude\F4-19\points-p1-native.csv` (claude), `<repository>\qa\curves-s4-b1\rederived\codex\F4-19\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 143 | 195 |
| x per px | 0.0821 | 0.0820 |
| y per px | 0.4101 | 0.4099 |
| RMS residual x, y | 0.095, 0.357 | 0.100, 0.332 |

Corners of claude's box [705, 508, 2462, 2002] mapped by both calibrations (tolerance 0.28 in x, 1.10 in y):

- (-1.2, 607.8) vs (-1.1, 607.7)
- (143.0, 603.9) vs (142.9, 603.7)
- (-2.2, -4.9) vs (-2.2, -4.7)
- (142.0, -8.8) vs (141.8, -8.7)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.39 | 1.09 | 0.90 | 25 | 2.53 | 2.34 | agree; claude off the ink |
| x | 10 | 0.02 | 0.40 | 0.41 | 25 | 0.63 | 0.68 | agree |
| x | 20 | 0.08 | 0.33 | 0.36 | 25 | 0.79 | 0.75 | agree |
| x | 30 | 0.07 | 0.15 | 0.16 | 25 | 0.51 | 0.57 | agree |
| x | 40 | 0.07 | 0.13 | 0.15 | 25 | 0.50 | 0.50 | agree |
| x | 50 | 0.06 | 0.17 | 0.19 | 19 | 0.50 | 0.54 | agree |
| x | 60 | 0.02 | 0.15 | 0.15 | 19 | 0.66 | 0.66 | agree |
| x | 70 | 0.06 | 0.36 | 0.37 | 19 | 0.75 | 0.76 | agree |
| x | 80 | 0.31 | 0.18 | 0.24 | 21 | 0.80 | 0.59 | agree |
| x | 90 | 0.07 | 0.38 | 0.38 | 21 | 1.34 | 1.35 | agree |
| x | 100 | 0.16 | 0.33 | 0.38 | 21 | 1.56 | 1.35 | agree |
| x | 110 | 0.28 | 0.31 | 0.33 | 21 | 0.69 | 0.50 | agree |
| x | 120 | 0.10 | 0.18 | 0.21 | 20 | 0.89 | 0.53 | agree |
| x | 130 | 0.13 | 0.34 | 0.37 | 23 | 0.50 | 0.57 | agree |
| x | 140 | 0.14 | 0.22 | 0.20 | 23 | 0.50 | 0.54 | agree |
| y | 500 | | | | | | | claude's line not a knot: insufficient ink: found at 5 of 25 positions over 15% of the line's length |
| y | 550 | | | | | | | claude's line not a knot: misplaced: 3.29 px from the ink's line at an end of the line |
| y | 500 | | | | | | | codex's line not a knot: insufficient ink: found at 4 of 25 positions over 11% of the line's length |
| y | 0 | 0.03 | 0.27 | 0.26 | 18 | 0.59 | 0.50 | agree |
| y | 50 | 0.05 | 0.31 | 0.30 | 18 | 0.81 | 0.50 | agree |
| y | 100 | 0.10 | 0.13 | 0.15 | 18 | 0.56 | 0.79 | agree |
| y | 150 | 0.11 | 0.40 | 0.41 | 18 | 0.88 | 0.76 | agree |
| y | 200 | 0.14 | 0.48 | 0.52 | 18 | 0.83 | 0.70 | agree |
| y | 250 | 0.05 | 0.57 | 0.57 | 17 | 0.95 | 0.71 | agree |
| y | 300 | 0.09 | 0.58 | 0.57 | 9 | 0.81 | 1.07 | agree |
| y | 350 | 0.06 | 0.54 | 0.49 | 5 | 1.38 | 0.95 | agree |
| y | 400 | 0.01 | 0.48 | 0.49 | 6 | 0.99 | 0.75 | agree |
| y | 450 | 0.04 | 0.26 | 0.25 | 7 | 1.01 | 0.61 | agree |
| y | 600 | 0.05 | 0.31 | 0.31 | 18 | 0.61 | 0.54 | agree |
| y | 550 | | | | | | 2.43 | only in codex |

Both maps along every verified line and every interval midline (560 places): largest difference 0.02809 in x (tolerance 0.4129, claude 0), 0.5956 in y (tolerance 1.425, codex 550); 0 beyond the two maps' line errors.

Canonical reading: codex (codex's lines include all of claude's and more, as close to the ink; 26 shared lines checked against the ink, mean of the median distances 0.35 px (claude: x 0.31, y 0.39), 0.35 px (codex: x 0.32, y 0.39)); points are evaluated at codex's samples.

## Series

3 series in codex, 3 in claude.


## Points

Matched: 195; agreed 194; disagreed 1; unmatched 27 (kept as one-sided: 9 of codex, 18 of claude).

| series | kind | seq (codex/claude) | codex x, y (bounds) | claude x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| run10 | feature | 6/- | 112.7, 31.7 | (none) | | | unmatched in claude |
| run12 | feature | 3/- | 19.9, 49.8 | (none) | | | unmatched in claude |
| run12 | trace | 17/interp | 4.3, 588.0 (0.7, 2.8) | 4.3, 581.4 (0.7, 3.6) | slope -0.2 | +6.7 (tol 6.7) | **disagree** |
| run12 | trace | 62/- | 95.0, 30.1 (1.3, 5.3) | (no trace at this x) | | | unmatched in claude |
| run12 | trace | 63/- | 99.9, 31.1 (1.3, 7.0) | (no trace at this x) | | | unmatched in claude |
| run12 | trace | 64/- | 105.0, 32.7 (0.9, 5.5) | (no trace at this x) | | | unmatched in claude |
| run12 | trace | 65/- | 109.7, 33.2 (1.0, 4.3) | (no trace at this x) | | | unmatched in claude |
| run12 | trace | 66/- | 115.0, 27.8 (1.8, 5.3) | (no trace at this x) | | | unmatched in claude |
| run4 | feature | 4/- | 23.4, 95.4 | (none) | | | unmatched in claude |
| run4 | feature | 9/- | 120.6, 44.8 | (none) | | | unmatched in claude |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
