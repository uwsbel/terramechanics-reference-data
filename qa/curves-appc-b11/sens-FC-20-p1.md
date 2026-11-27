# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b11\rederived\claude\FC-20\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b11\rederived\codex\FC-20\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 55 | 55 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0130 | 0.0130 |
| RMS residual x, y | 0.002, 0.010 | 0.002, 0.009 |

Corners of claude's box [700, 1590, 2420, 3400] mapped by both calibrations (tolerance 0.00 in x, 0.03 in y):

- (-0.0, 51.1) vs (-0.0, 51.1)
- (1.1, 50.7) vs (1.1, 50.7)
- (-0.1, 27.5) vs (-0.1, 27.5)
- (1.0, 27.1) vs (1.0, 27.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.46 | 0.36 | 0.24 | 12 | 0.79 | 0.51 | agree |
| x | 0.1 | 0.12 | 0.22 | 0.25 | 12 | 0.51 | 0.50 | agree |
| x | 0.2 | 0.21 | 0.12 | 0.16 | 12 | 0.55 | 0.50 | agree |
| x | 0.3 | 0.42 | 0.32 | 0.35 | 12 | 0.84 | 0.84 | agree |
| x | 0.4 | 0.51 | 0.51 | 0.30 | 12 | 1.46 | 0.83 | agree |
| x | 0.5 | 0.18 | 0.21 | 0.24 | 12 | 0.56 | 0.50 | agree |
| x | 0.6 | 0.27 | 0.30 | 0.23 | 12 | 0.50 | 0.60 | agree |
| x | 0.7 | 0.09 | 0.16 | 0.17 | 12 | 0.50 | 0.50 | agree |
| x | 0.8 | 0.12 | 0.27 | 0.31 | 12 | 0.54 | 0.57 | agree |
| x | 0.9 | 0.17 | 0.28 | 0.30 | 12 | 0.50 | 0.56 | agree |
| x | 1 | 0.31 | 0.19 | 0.20 | 12 | 0.50 | 0.58 | agree |
| y | 30 | 0.22 | 0.43 | 0.38 | 25 | 0.71 | 0.56 | agree |
| y | 35 | 0.06 | 0.42 | 0.39 | 25 | 0.66 | 0.68 | agree |
| y | 40 | 0.63 | 0.35 | 0.42 | 25 | 0.90 | 0.70 | agree |
| y | 45 | 0.26 | 0.50 | 0.54 | 25 | 1.17 | 0.91 | agree |
| y | 50 | 0.19 | 0.59 | 0.56 | 25 | 0.96 | 0.84 | agree |

Both maps along every verified line and every interval midline (319 places): largest difference 0.0003622 in x (tolerance 0.0008547, codex 0), 0.006565 in y (tolerance 0.02086, claude 40); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 16 shared lines checked against the ink, mean of the median distances 0.33 px (claude: x 0.27, y 0.46), 0.31 px (codex: x 0.25, y 0.46), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

4 series in claude, 4 in codex.


## Points

Matched: 79; agreed 78; disagreed 1; unmatched 3 (kept as one-sided: 0 of claude, 3 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| upper | feature | 1/1 | -0.0, 30.5 (0.0, 0.0) | -0.0, 30.4 (0.0, 0.0) | -0.0 | +0.1 | **disagree** |
