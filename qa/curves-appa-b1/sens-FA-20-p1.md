# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b1\rederived\claude\FA-20\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b1\rederived\codex\FA-20\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 30 | 30 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0130 | 0.0130 |
| RMS residual x, y | 0.002, 0.023 | 0.002, 0.023 |

Corners of claude's box [790, 1470, 2380, 3220] mapped by both calibrations (tolerance 0.00 in x, 0.06 in y):

- (-0.0, 50.3) vs (-0.0, 50.3)
- (1.0, 50.3) vs (1.0, 50.3)
- (-0.0, 27.5) vs (-0.0, 27.5)
- (1.0, 27.6) vs (1.0, 27.6)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.44 | 0.34 | 0.21 | 12 | 0.70 | 0.50 | agree |
| x | 0.2 | 0.45 | 0.39 | 0.28 | 12 | 0.77 | 0.51 | agree |
| x | 0.4 | 0.42 | 0.34 | 0.23 | 12 | 0.91 | 0.50 | agree |
| x | 0.6 | 0.29 | 0.23 | 0.23 | 12 | 0.50 | 0.53 | agree |
| x | 0.8 | 0.29 | 0.10 | 0.18 | 12 | 0.86 | 0.54 | agree |
| x | 1 | 0.84 | 0.77 | 0.57 | 12 | 1.58 | 0.65 | agree |
| y | 30 | 0.08 | 0.36 | 0.35 | 15 | 0.51 | 0.56 | agree |
| y | 35 | 0.13 | 0.26 | 0.24 | 15 | 0.50 | 0.64 | agree |
| y | 40 | 0.29 | 0.25 | 0.24 | 15 | 0.50 | 0.60 | agree |
| y | 45 | 0.22 | 0.37 | 0.32 | 15 | 0.86 | 0.63 | agree |
| y | 50 | 0.04 | 0.17 | 0.19 | 15 | 0.50 | 0.50 | agree |

Both maps along every verified line and every interval midline (286 places): largest difference 0.0007012 in x (tolerance 0.001446, claude 1), 0.004146 in y (tolerance 0.01502, codex 40); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.33 px (claude: x 0.36, y 0.28), 0.28 px (codex: x 0.28, y 0.27), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 23; agreed 23; disagreed 0; unmatched 4 (kept as one-sided: 1 of claude, 3 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| curve | feature | -/2 | (none) | 0.5, 42.2 | | | unmatched in claude |
| curve | feature | 2/- | 0.5, 42.1 | (none) | | | unmatched in codex |
