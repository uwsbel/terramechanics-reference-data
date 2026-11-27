# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b3\rederived\claude\FC-6C\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b3\rederived\codex\FC-6C\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 36 | 36 |
| x per px | 0.1712 | 0.1712 |
| y per px | 3.4033 | 3.4031 |
| RMS residual x, y | 0.639, 9.299 | 0.640, 9.750 |

Corners of claude's box [625, 925, 2150, 2435] mapped by both calibrations (tolerance 1.45 in x, 22.45 in y):

- (-3.1, 5086.9) vs (-3.1, 5087.2)
- (258.0, 5042.2) vs (258.0, 5041.1)
- (-6.0, -51.9) vs (-6.0, -51.2)
- (255.2, -96.6) vs (255.2, -97.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.15 | 0.31 | 0.33 | 15 | 0.51 | 0.59 | agree |
| x | 50 | 0.31 | 0.48 | 0.42 | 13 | 0.77 | 1.16 | agree |
| x | 100 | 0.02 | 0.27 | 0.27 | 12 | 0.63 | 0.58 | agree |
| x | 150 | 0.08 | 0.17 | 0.18 | 11 | 0.50 | 0.50 | agree |
| x | 200 | 0.07 | 0.28 | 0.29 | 13 | 0.82 | 0.73 | agree |
| x | 250 | 0.38 | 0.19 | 0.25 | 15 | 0.50 | 0.58 | agree |
| y | 0 | 0.07 | 0.19 | 0.20 | 15 | 0.56 | 0.55 | agree |
| y | 1000 | 0.28 | 0.25 | 0.26 | 15 | 0.74 | 0.50 | agree |
| y | 2000 | 0.06 | 0.57 | 0.53 | 15 | 1.11 | 1.05 | agree |
| y | 3000 | 3.32 | 0.65 | 0.69 | 23 | 2.43 | 2.37 | agree |
| y | 4000 | 0.36 | 0.49 | 0.60 | 15 | 1.44 | 1.25 | agree |
| y | 5000 | 0.12 | 0.35 | 0.32 | 15 | 0.51 | 0.57 | agree |

Both maps along every verified line and every interval midline (246 places): largest difference 0.07291 in x (tolerance 0.2712, claude 250), 9.907 in y (tolerance 16.36, codex 3000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 12 shared lines checked against the ink, mean of the median distances 0.35 px (claude: x 0.28, y 0.42), 0.36 px (codex: x 0.29, y 0.43), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 373; agreed 366; disagreed 7; unmatched 17 (kept as one-sided: 6 of claude, 11 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1961 | feature | 3/90 | 247.5, 1326.2 (0.5, 23.1) | 246.3, 1324.0 (0.5, 19.1) | +1.2 | +2.2 | **disagree** |
| n1961 | marker | 9/9 | 168.0, 1399.4 (0.4, 9.8) | 169.7, 1395.6 (1.1, 22.8) | -1.7 | +3.8 | **disagree** |
| n1961 | trace | 24/- | 101.5, 1333.3 (0.3, 26.5) | (no trace at this x) | | | unmatched in codex |
| n1961 | trace | 40/- | 163.9, 1366.4 (0.3, 18.1) | (no trace at this x) | | | unmatched in codex |
| n1961 | trace | 41/- | 171.2, 1392.2 (0.3, 18.1) | (no trace at this x) | | | unmatched in codex |
| n1961 | trace | 54/- | 222.1, 1331.3 (0.3, 14.7) | (no trace at this x) | | | unmatched in codex |
| n1961 | trace | 62/- | 247.5, 1326.2 (0.5, 23.1) | (no trace at this x) | | | unmatched in codex |
| n2934 | feature | 3/84 | 253.4, 2856.5 (0.5, 21.3) | 245.0, 2889.0 (0.5, 24.9) | +8.3 | -32.5 | **disagree** |
| n3815 | marker | 8/8 | 147.0, 3012.5 (0.4, 15.1) | 149.2, 3026.3 (0.4, 14.7) | -2.2 | -13.8 | **disagree** |
| n4695 | marker | 8/8 | 168.1, 3996.5 (0.5, 15.4) | 167.2, 3997.4 (0.4, 11.3) | +0.9 | -1.0 | **disagree** |
| n4695 | marker | 10/10 | 217.7, 4038.4 (0.5, 15.5) | 216.5, 4023.5 (0.5, 11.4) | +1.2 | +14.9 | **disagree** |
| n714 | feature | 3/82 | 247.3, 731.5 (0.5, 22.9) | 245.8, 732.8 (0.5, 18.8) | +1.5 | -1.3 | **disagree** |
| n714 | trace | 61/- | 247.3, 731.5 (0.5, 22.9) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 8 trace samples excluded

No hand decision overridden.
