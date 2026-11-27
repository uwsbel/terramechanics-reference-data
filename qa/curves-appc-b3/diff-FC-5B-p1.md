# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b3\rederived\claude\FC-5B\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b3\rederived\codex\FC-5B\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 36 | 36 |
| x per px | 0.1689 | 0.1689 |
| y per px | 3.3998 | 3.3999 |
| RMS residual x, y | 0.952, 3.586 | 0.955, 3.525 |

Corners of claude's box [645, 955, 2180, 2475] mapped by both calibrations (tolerance 2.08 in x, 10.51 in y):

- (-4.7, 5096.0) vs (-4.8, 5095.7)
- (254.4, 5086.1) vs (254.5, 5086.3)
- (-6.0, -71.7) vs (-6.0, -72.1)
- (253.2, -81.5) vs (253.2, -81.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.05 | 0.33 | 0.30 | 15 | 0.53 | 0.50 | agree |
| x | 50 | 0.19 | 0.37 | 0.30 | 15 | 1.28 | 1.07 | agree |
| x | 100 | 0.17 | 0.14 | 0.22 | 14 | 0.54 | 0.50 | agree |
| x | 150 | 0.12 | 0.22 | 0.23 | 15 | 0.50 | 0.50 | agree |
| x | 200 | 0.05 | 0.18 | 0.18 | 15 | 0.50 | 0.50 | agree |
| x | 250 | 0.34 | 0.25 | 0.26 | 15 | 0.50 | 0.61 | agree |
| y | 1000 | | | | | | | claude's line not a knot: misplaced: 2.60 px from the ink's line at an end of the line |
| y | 1000 | | | | | | | codex's line not a knot: misplaced: 2.63 px from the ink's line at an end of the line |
| y | 0 | 0.15 | 0.40 | 0.34 | 15 | 0.71 | 0.57 | agree |
| y | 2000 | 0.26 | 0.41 | 0.31 | 15 | 1.25 | 1.07 | agree |
| y | 3000 | 0.00 | 0.37 | 0.37 | 15 | 0.86 | 0.86 | agree |
| y | 4000 | 0.22 | 0.53 | 0.60 | 15 | 0.89 | 0.77 | agree |
| y | 5000 | 0.09 | 0.30 | 0.32 | 15 | 0.72 | 0.81 | agree |

Both maps along every verified line and every interval midline (251 places): largest difference 0.06261 in x (tolerance 0.1874, claude 250), 0.9548 in y (tolerance 7.944, claude 2000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.32 px (claude: x 0.25, y 0.40), 0.31 px (codex: x 0.25, y 0.39), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 396; agreed 395; disagreed 1; unmatched 32 (kept as one-sided: 2 of claude, 30 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n4695 | marker | 11/11 | 197.3, 2632.8 (0.4, 10.2) | 198.2, 2634.4 (0.4, 10.0) | -0.9 | -1.7 | **disagree** |
| n4695 | trace | 13/- | 44.2, 2435.0 (0.4, 24.1) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 30/- | 123.4, 2639.0 (0.3, 20.4) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 3 trace samples excluded

Overrides of hand decisions (1), for review:

- claude n3815 trace 1: hand decision one-sided-verified (on the ink of the drawn line, verified on the page by codex's adjudicator; blind adjudication item 0)
