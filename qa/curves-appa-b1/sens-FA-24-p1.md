# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b1\rederived\claude\FA-24\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b1\rederived\codex\FA-24\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 30 | 30 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0130 | 0.0130 |
| RMS residual x, y | 0.002, 0.027 | 0.002, 0.027 |

Corners of claude's box [760, 1450, 2360, 3330] mapped by both calibrations (tolerance 0.00 in x, 0.07 in y):

- (-0.0, 52.0) vs (-0.0, 52.0)
- (1.0, 52.1) vs (1.0, 52.1)
- (-0.0, 27.6) vs (-0.0, 27.6)
- (1.0, 27.7) vs (1.0, 27.7)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.17 | 0.37 | 0.26 | 12 | 0.89 | 0.71 | agree |
| x | 0.2 | 0.16 | 0.21 | 0.20 | 12 | 0.54 | 0.50 | agree |
| x | 0.4 | 0.00 | 0.25 | 0.25 | 12 | 0.55 | 0.55 | agree |
| x | 0.6 | 0.34 | 0.28 | 0.16 | 12 | 0.82 | 0.50 | agree |
| x | 0.8 | 0.37 | 0.12 | 0.08 | 12 | 0.50 | 0.50 | agree |
| x | 1 | 0.22 | 0.42 | 0.38 | 12 | 1.26 | 1.02 | agree |
| y | 30 | 0.10 | 0.39 | 0.32 | 15 | 0.65 | 0.57 | agree |
| y | 35 | 0.27 | 0.35 | 0.28 | 15 | 0.50 | 0.64 | agree |
| y | 40 | 0.07 | 0.16 | 0.14 | 15 | 0.50 | 0.50 | agree |
| y | 45 | 0.26 | 0.31 | 0.39 | 15 | 1.03 | 0.95 | agree |
| y | 50 | 0.27 | 0.41 | 0.38 | 15 | 0.91 | 0.64 | agree |

Both maps along every verified line and every interval midline (272 places): largest difference 0.0003001 in x (tolerance 0.0008925, codex 0.6), 0.003836 in y (tolerance 0.01687, claude 35); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.30 px (claude: x 0.27, y 0.32), 0.26 px (codex: x 0.22, y 0.30), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 24; agreed 24; disagreed 0; unmatched 3 (kept as one-sided: 1 of claude, 2 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| curve | feature | 3/- | 0.9, 51.9 | (none) | | | unmatched in codex |
