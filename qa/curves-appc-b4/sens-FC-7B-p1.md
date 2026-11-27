# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b4\rederived\claude\FC-7B\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b4\rederived\codex\FC-7B\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 0.0002 | 0.0002 |
| y per px | 0.0204 | 0.0204 |
| RMS residual x, y | 0.000, 0.022 | 0.000, 0.023 |

Corners of claude's box [575, 1305, 2335, 3305] mapped by both calibrations (tolerance 0.00 in x, 0.07 in y):

- (0.3, 35.4) vs (0.3, 35.4)
- (0.3, -0.5) vs (0.3, -0.5)
- (-0.0, 35.6) vs (-0.0, 35.6)
- (-0.0, -0.3) vs (-0.0, -0.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.00 | 0.58 | 0.58 | 21 | 1.06 | 1.06 | agree |
| x | 0.04 | 0.04 | 0.44 | 0.42 | 21 | 0.72 | 0.71 | agree |
| x | 0.08 | 0.00 | 0.41 | 0.41 | 21 | 0.73 | 0.73 | agree |
| x | 0.12 | 0.04 | 0.34 | 0.34 | 21 | 0.83 | 0.82 | agree |
| x | 0.16 | 0.04 | 0.31 | 0.30 | 21 | 0.78 | 0.78 | agree |
| x | 0.2 | 0.12 | 0.37 | 0.35 | 21 | 0.58 | 0.64 | agree |
| x | 0.24 | 0.02 | 0.55 | 0.53 | 21 | 0.80 | 0.80 | agree |
| x | 0.28 | 0.04 | 0.36 | 0.33 | 21 | 1.18 | 1.17 | agree |
| x | 0.32 | 0.00 | 0.35 | 0.35 | 21 | 0.98 | 1.00 | agree |
| y | 0 | 0.03 | 0.31 | 0.32 | 24 | 0.62 | 0.58 | agree |
| y | 5 | 0.68 | 0.39 | 0.30 | 24 | 1.12 | 0.50 | agree |
| y | 10 | 0.04 | 0.36 | 0.35 | 24 | 0.80 | 0.75 | agree |
| y | 15 | 0.07 | 0.35 | 0.33 | 24 | 0.50 | 0.50 | agree |
| y | 20 | 0.03 | 0.38 | 0.37 | 24 | 0.76 | 0.75 | agree |
| y | 25 | 0.04 | 0.30 | 0.32 | 24 | 0.90 | 0.96 | agree |
| y | 30 | 0.09 | 0.36 | 0.38 | 24 | 0.78 | 0.71 | agree |
| y | 35 | 0.04 | 0.28 | 0.29 | 24 | 0.50 | 0.54 | agree |

Both maps along every verified line and every interval midline (366 places): largest difference 1.721e-05 in x (tolerance 0.0002566, claude 0.2), 0.01134 in y (tolerance 0.03824, codex 5); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.38 px (claude: x 0.41, y 0.34), 0.37 px (codex: x 0.40, y 0.33), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

6 series in claude, 6 in codex.


## Points

Matched: 107; agreed 99; disagreed 8; unmatched 0 (kept as one-sided: 0 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n10p2psi | marker | 5/5 | 0.0, 14.6 (0.0, 0.0) | 0.0, 14.4 (0.0, 0.0) | +0.0 | +0.2 | **disagree** |
| n10p2psi | marker | 9/9 | 0.1, 14.6 (0.0, 0.0) | 0.1, 14.5 (0.0, 0.0) | +0.0 | +0.1 | **disagree** |
| n10p2psi | marker | 14/14 | 0.2, 10.5 (0.0, 0.0) | 0.2, 10.4 (0.0, 0.1) | +0.0 | +0.1 | **disagree** |
| n13p8psi | marker | 6/6 | 0.0, 19.3 (0.0, 0.0) | 0.0, 19.3 (0.0, 0.0) | +0.0 | +0.1 | **disagree** |
| n13p8psi | marker | 14/14 | 0.2, 15.3 (0.0, 0.0) | 0.2, 15.4 (0.0, 0.1) | +0.0 | -0.1 | **disagree** |
| n3p4psi | marker | 5/5 | 0.0, 7.5 (0.0, 0.0) | 0.0, 7.6 (0.0, 0.0) | +0.0 | -0.1 | **disagree** |
| n6p6psi | marker | 3/3 | 0.0, 8.8 (0.0, 0.0) | 0.0, 8.7 (0.0, 0.0) | +0.0 | +0.1 | **disagree** |
| n6p6psi | marker | 16/16 | 0.2, 6.5 (0.0, 0.0) | 0.2, 6.4 (0.0, 0.0) | +0.0 | +0.1 | **disagree** |
