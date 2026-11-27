# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b11\rederived\claude\FC-21\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b11\rederived\codex\FC-21\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 55 | 55 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0130 | 0.0130 |
| RMS residual x, y | 0.001, 0.009 | 0.001, 0.011 |

Corners of claude's box [640, 1200, 2420, 3440] mapped by both calibrations (tolerance 0.00 in x, 0.03 in y):

- (-0.1, 54.8) vs (-0.1, 54.8)
- (1.1, 54.4) vs (1.1, 54.4)
- (-0.1, 25.6) vs (-0.1, 25.6)
- (1.1, 25.2) vs (1.1, 25.2)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.07 | 0.31 | 0.31 | 12 | 0.71 | 0.67 | agree |
| x | 0.1 | 0.16 | 0.40 | 0.31 | 12 | 0.61 | 0.59 | agree |
| x | 0.2 | 0.26 | 0.23 | 0.26 | 12 | 0.75 | 0.50 | agree |
| x | 0.3 | 0.17 | 0.29 | 0.26 | 12 | 0.50 | 0.50 | agree |
| x | 0.4 | 0.17 | 0.27 | 0.32 | 12 | 1.01 | 0.87 | agree |
| x | 0.5 | 0.62 | 0.53 | 0.19 | 12 | 1.30 | 0.59 | agree |
| x | 0.6 | 0.11 | 0.19 | 0.22 | 12 | 0.50 | 0.50 | agree |
| x | 0.7 | 0.17 | 0.30 | 0.27 | 12 | 0.65 | 0.50 | agree |
| x | 0.8 | 0.15 | 0.34 | 0.33 | 12 | 0.69 | 0.84 | agree |
| x | 0.9 | 0.34 | 0.23 | 0.17 | 12 | 0.65 | 0.50 | agree |
| x | 1 | 0.27 | 0.19 | 0.22 | 12 | 0.50 | 0.50 | agree |
| y | 30 | 0.28 | 0.39 | 0.42 | 25 | 1.00 | 1.28 | agree |
| y | 35 | 0.12 | 0.36 | 0.38 | 25 | 1.05 | 1.04 | agree |
| y | 40 | 0.32 | 0.37 | 0.42 | 25 | 0.72 | 1.04 | agree |
| y | 45 | 0.67 | 0.58 | 0.64 | 25 | 1.14 | 1.59 | agree |
| y | 50 | 0.35 | 0.44 | 0.43 | 25 | 0.75 | 0.97 | agree |

Both maps along every verified line and every interval midline (313 places): largest difference 0.0004375 in x (tolerance 0.001396, codex 0.5), 0.007405 in y (tolerance 0.03548, codex 45); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 16 shared lines checked against the ink, mean of the median distances 0.34 px (claude: x 0.30, y 0.43), 0.32 px (codex: x 0.26, y 0.46), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 62; agreed 60; disagreed 2; unmatched 4 (kept as one-sided: 0 of claude, 4 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| band-bottom | feature | 2/2 | 1.1, 40.0 (0.0, 0.0) | 1.1, 40.0 (0.0, 0.0) | -0.0 | +0.0 | **disagree** |
| band-top | feature | 2/2 | 1.1, 45.0 (0.0, 0.0) | 1.1, 45.0 (0.0, 0.0) | -0.0 | +0.0 | **disagree** |
