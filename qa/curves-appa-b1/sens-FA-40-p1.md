# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b1\rederived\claude\FA-40\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b1\rederived\codex\FA-40\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 30 | 30 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0130 | 0.0130 |
| RMS residual x, y | 0.003, 0.019 | 0.003, 0.018 |

Corners of claude's box [770, 1450, 2400, 3400] mapped by both calibrations (tolerance 0.01 in x, 0.05 in y):

- (-0.0, 52.7) vs (-0.0, 52.7)
- (1.0, 52.5) vs (1.0, 52.5)
- (-0.0, 27.3) vs (-0.0, 27.3)
- (1.0, 27.1) vs (1.0, 27.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.21 | 0.20 | 0.23 | 12 | 0.50 | 0.62 | agree |
| x | 0.2 | 0.38 | 0.27 | 0.21 | 12 | 0.53 | 0.56 | agree |
| x | 0.4 | 0.11 | 0.29 | 0.25 | 12 | 0.86 | 1.00 | agree |
| x | 0.6 | 0.10 | 0.19 | 0.22 | 12 | 0.79 | 0.84 | agree |
| x | 0.8 | 0.45 | 0.28 | 0.45 | 12 | 0.68 | 0.77 | agree |
| x | 1 | 0.27 | 0.29 | 0.31 | 12 | 0.82 | 0.73 | agree |
| y | 30 | 0.37 | 0.25 | 0.25 | 15 | 0.61 | 0.64 | agree |
| y | 35 | 0.14 | 0.31 | 0.36 | 15 | 0.74 | 0.79 | agree |
| y | 40 | 0.30 | 0.48 | 0.26 | 15 | 1.27 | 0.99 | agree |
| y | 45 | 0.00 | 0.37 | 0.37 | 15 | 0.67 | 0.67 | agree |
| y | 50 | 0.07 | 0.32 | 0.32 | 15 | 0.55 | 0.57 | agree |

Both maps along every verified line and every interval midline (222 places): largest difference 0.0002728 in x (tolerance 0.001048, claude 0.8), 0.004613 in y (tolerance 0.02006, claude 30); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.30 px (claude: x 0.25, y 0.35), 0.29 px (codex: x 0.28, y 0.31), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

2 series in claude, 2 in codex.


## Points

Matched: 46; agreed 44; disagreed 2; unmatched 4 (kept as one-sided: 0 of claude, 4 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| band-bottom | feature | 1/1 | 0.0, 40.0 (0.0, 0.0) | 0.0, 40.0 (0.0, 0.0) | +0.0 | +0.0 | **disagree** |
| band-top | feature | 1/1 | 0.0, 45.0 (0.0, 0.0) | -0.0, 45.0 (0.0, 0.0) | +0.0 | -0.0 | **disagree** |
