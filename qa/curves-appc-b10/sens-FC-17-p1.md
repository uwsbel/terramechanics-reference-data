# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b10\rederived\claude\FC-17\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b10\rederived\codex\FC-17\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 55 | 55 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0130 | 0.0130 |
| RMS residual x, y | 0.001, 0.013 | 0.001, 0.014 |

Corners of claude's box [775, 1300, 2560, 3555] mapped by both calibrations (tolerance 0.00 in x, 0.04 in y):

- (-0.1, 54.9) vs (-0.1, 54.9)
- (1.1, 54.6) vs (1.1, 54.6)
- (-0.1, 25.5) vs (-0.1, 25.5)
- (1.1, 25.2) vs (1.1, 25.2)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.11 | 0.37 | 0.39 | 12 | 0.75 | 1.03 | agree |
| x | 0.1 | 0.15 | 0.30 | 0.28 | 12 | 0.50 | 0.50 | agree |
| x | 0.2 | 0.32 | 0.24 | 0.20 | 12 | 0.79 | 0.72 | agree |
| x | 0.3 | 0.20 | 0.37 | 0.37 | 12 | 0.75 | 0.59 | agree |
| x | 0.4 | 1.34 | 0.65 | 0.29 | 12 | 1.65 | 0.60 | agree |
| x | 0.5 | 0.32 | 0.32 | 0.28 | 12 | 0.55 | 0.50 | agree |
| x | 0.6 | 0.16 | 0.39 | 0.35 | 12 | 0.80 | 0.65 | agree |
| x | 0.7 | 0.44 | 0.26 | 0.25 | 12 | 0.69 | 0.53 | agree |
| x | 0.8 | 0.27 | 0.61 | 0.52 | 12 | 0.80 | 0.92 | agree |
| x | 0.9 | 0.58 | 0.56 | 0.35 | 12 | 1.49 | 0.88 | agree |
| x | 1 | 0.09 | 0.24 | 0.28 | 12 | 0.53 | 0.61 | agree |
| y | 30 | 0.20 | 0.29 | 0.42 | 25 | 0.93 | 0.72 | agree |
| y | 35 | 0.30 | 0.39 | 0.40 | 25 | 0.78 | 0.78 | agree |
| y | 40 | 0.26 | 0.46 | 0.36 | 25 | 0.73 | 0.77 | agree |
| y | 45 | 0.49 | 0.38 | 0.34 | 25 | 1.05 | 0.77 | agree |
| y | 50 | 0.30 | 0.48 | 0.38 | 25 | 0.79 | 0.85 | agree |

Both maps along every verified line and every interval midline (316 places): largest difference 0.0009763 in x (tolerance 0.00146, codex 0.4), 0.005257 in y (tolerance 0.02369, codex 45); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 16 shared lines checked against the ink, mean of the median distances 0.39 px (claude: x 0.39, y 0.40), 0.34 px (codex: x 0.32, y 0.38), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

4 series in claude, 4 in codex.
- marker symbol disagreement in FC-17/1/data: claude ['circle', 'circle-dot'], codex ['circle']


## Points

Matched: 84; agreed 83; disagreed 1; unmatched 2 (kept as one-sided: 0 of claude, 2 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| upper | feature | 1/1 | 0.0, 44.8 (0.0, 0.0) | -0.0, 44.8 (0.0, 0.0) | +0.0 | +0.0 | **disagree** |
