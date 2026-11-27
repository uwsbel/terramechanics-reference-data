# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b2\rederived\claude\FC-4C\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b2\rederived\codex\FC-4C\points-p2-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 18 | 18 |
| x per px | 0.1718 | 0.1718 |
| y per px | 0.3476 | 0.3476 |
| RMS residual x, y | 0.460, 0.154 | 0.453, 0.110 |

Corners of claude's box [750, 2750, 2260, 3380] mapped by both calibrations (tolerance 1.09 in x, 0.61 in y):

- (-4.0, 110.6) vs (-4.0, 110.5)
- (255.4, 109.1) vs (255.4, 109.1)
- (-5.0, -108.4) vs (-5.0, -108.5)
- (254.4, -109.9) vs (254.4, -109.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.15 | 0.19 | 0.20 | 6 | 0.50 | 0.50 | agree |
| x | 50 | 0.07 | 0.37 | 0.39 | 6 | 0.72 | 0.75 | agree |
| x | 100 | 0.17 | 0.30 | 0.31 | 6 | 0.64 | 0.75 | agree |
| x | 150 | 0.17 | 0.30 | 0.38 | 6 | 0.50 | 0.70 | agree |
| x | 200 | 0.00 | 0.35 | 0.35 | 6 | 0.59 | 0.59 | agree |
| x | 250 | 0.18 | 0.29 | 0.25 | 6 | 1.25 | 1.10 | agree |
| y | -100 | 0.26 | 0.32 | 0.39 | 15 | 0.60 | 0.80 | agree |
| y | 0 | 0.74 | 0.70 | 0.35 | 15 | 1.53 | 0.78 | agree |
| y | 100 | 0.20 | 0.23 | 0.18 | 15 | 0.61 | 0.75 | agree |

Both maps along every verified line and every interval midline (200 places): largest difference 0.03763 in x (tolerance 0.2525, codex 0), 0.2845 in y (tolerance 0.8122, claude 0); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.34 px (claude: x 0.30, y 0.41), 0.31 px (codex: x 0.31, y 0.31), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 68; agreed 67; disagreed 1; unmatched 1 (kept as one-sided: 1 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n3815 | marker | 9/- | 118.8, 24.6 | (none) | | | unmatched in codex |
| n741 | marker | 3/3 | 30.0, -1.6 (0.8, 1.9) | 20.2, -2.9 (1.8, 3.8) | +9.8 | +1.2 | **disagree** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
