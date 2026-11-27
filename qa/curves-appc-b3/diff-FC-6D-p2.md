# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b3\rederived\claude\FC-6D\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b3\rederived\codex\FC-6D\points-p2-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 20 | 12 |
| x per px | 0.1706 | 0.1685 |
| y per px | 0.3406 | 0.3407 |
| RMS residual x, y | 0.097, 0.065 | 1.142, 0.068 |

Corners of claude's box [800, 2320, 2266, 3255] mapped by both calibrations (tolerance 1.41 in x, 0.47 in y):

- (4.5, 11.5) vs (6.6, 11.5)  **disagree**
- (254.5, 5.7) vs (253.6, 5.7)
- (1.8, -307.0) vs (4.1, -307.0)  **disagree**
- (251.8, -312.7) vs (251.1, -312.8)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.40 | 0.32 | 0.31 | 21 | 0.74 | 0.54 | agree |
| x | 50 | 0.35 | 0.29 | 0.21 | 9 | 0.76 | 0.50 | agree |
| x | 100 | 0.02 | 0.16 | 0.18 | 23 | 0.50 | 0.50 | agree |
| x | 150 | 0.35 | 0.25 | 0.26 | 9 | 1.22 | 2.33 | agree |
| x | 200 | 0.17 | 0.19 | 0.20 | 9 | 0.80 | 1.69 | agree |
| x | 250 | 0.09 | 0.12 | 0.14 | 9 | 0.50 | 1.06 | agree |
| y | -300 | 0.19 | 0.37 | 0.40 | 12 | 0.64 | 0.70 | agree |
| y | 0 | 0.14 | 0.34 | 0.29 | 12 | 0.57 | 0.75 | agree |

Both maps along every verified line and every interval midline (145 places): largest difference 0.05612 in x (tolerance 0.2159, claude 50), 0.06575 in y (tolerance 0.4734, codex -300); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 8 shared lines checked against the ink, mean of the median distances 0.25 px (claude: x 0.22, y 0.35), 0.25 px (codex: x 0.21, y 0.34), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 92; agreed 90; disagreed 2; unmatched 0 (kept as one-sided: 0 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n3814 | marker | 9/9 | 97.2, -263.2 (0.6, 1.2) | 98.6, -268.5 (1.5, 3.0) | -1.4 | +5.3 | **disagree** |
| n4695 | marker | 13/13 | 175.1, -270.6 (0.5, 0.9) | 175.0, -274.5 (1.4, 2.3) | +0.1 | +3.9 | **disagree** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
