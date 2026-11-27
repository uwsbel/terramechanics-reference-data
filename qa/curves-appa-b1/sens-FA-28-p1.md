# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b1\rederived\claude\FA-28\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b1\rederived\codex\FA-28\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 36 | 36 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0130 | 0.0130 |
| RMS residual x, y | 0.003, 0.022 | 0.003, 0.022 |

Corners of claude's box [735, 1420, 2335, 3550] mapped by both calibrations (tolerance 0.01 in x, 0.06 in y):

- (-0.0, 52.4) vs (-0.0, 52.4)
- (1.0, 52.4) vs (1.0, 52.4)
- (-0.0, 24.6) vs (-0.0, 24.6)
- (1.0, 24.7) vs (1.0, 24.7)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.12 | 0.30 | 0.36 | 15 | 0.66 | 0.71 | agree |
| x | 0.2 | 0.10 | 0.21 | 0.26 | 15 | 0.62 | 0.62 | agree |
| x | 0.4 | 0.36 | 0.19 | 0.15 | 14 | 0.67 | 0.50 | agree |
| x | 0.6 | 0.12 | 0.41 | 0.33 | 15 | 0.91 | 0.79 | agree |
| x | 0.8 | 0.13 | 0.32 | 0.31 | 15 | 0.59 | 0.50 | agree |
| x | 1 | 0.00 | 0.34 | 0.34 | 15 | 0.65 | 0.65 | agree |
| y | 25 | 0.17 | 0.40 | 0.37 | 15 | 0.66 | 0.70 | agree |
| y | 30 | 0.17 | 0.32 | 0.32 | 15 | 0.62 | 0.50 | agree |
| y | 35 | 0.13 | 0.14 | 0.17 | 15 | 0.52 | 0.50 | agree |
| y | 40 | 0.10 | 0.16 | 0.17 | 15 | 0.55 | 0.50 | agree |
| y | 45 | 0.08 | 0.20 | 0.19 | 15 | 0.50 | 0.50 | agree |
| y | 50 | 0.11 | 0.23 | 0.22 | 15 | 0.50 | 0.50 | agree |

Both maps along every verified line and every interval midline (277 places): largest difference 0.0002148 in x (tolerance 0.0009469, claude 0.4), 0.002448 in y (tolerance 0.01782, claude 25); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 12 shared lines checked against the ink, mean of the median distances 0.27 px (claude: x 0.30, y 0.24), 0.27 px (codex: x 0.29, y 0.24), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 23; agreed 23; disagreed 0; unmatched 4 (kept as one-sided: 0 of claude, 4 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| curve | feature | -/2 | (none) | 0.3, 31.4 | | | unmatched in claude |
| curve | feature | -/3 | (none) | 0.7, 38.4 | | | unmatched in claude |
