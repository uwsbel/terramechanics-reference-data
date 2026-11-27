# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b1\rederived\claude\FA-4\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b1\rederived\codex\FA-4\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 30 | 30 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0130 | 0.0130 |
| RMS residual x, y | 0.002, 0.023 | 0.002, 0.022 |

Corners of claude's box [805, 1365, 2405, 3100] mapped by both calibrations (tolerance 0.00 in x, 0.06 in y):

- (-0.0, 50.2) vs (-0.0, 50.2)
- (1.0, 50.4) vs (1.0, 50.4)
- (-0.0, 27.6) vs (-0.0, 27.6)
- (1.0, 27.7) vs (1.0, 27.7)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.11 | 0.12 | 0.19 | 12 | 0.65 | 0.74 | agree |
| x | 0.2 | 0.57 | 0.49 | 0.40 | 12 | 1.10 | 0.59 | agree |
| x | 0.4 | 0.37 | 0.40 | 0.29 | 12 | 0.74 | 0.61 | agree |
| x | 0.6 | 0.43 | 0.29 | 0.30 | 12 | 0.78 | 0.50 | agree |
| x | 0.8 | 0.12 | 0.37 | 0.37 | 12 | 0.63 | 0.65 | agree |
| x | 1 | 0.04 | 0.30 | 0.29 | 12 | 0.59 | 0.62 | agree |
| y | 30 | 0.21 | 0.28 | 0.41 | 15 | 0.64 | 0.81 | agree |
| y | 35 | 0.27 | 0.43 | 0.43 | 15 | 0.86 | 1.10 | agree |
| y | 40 | 0.08 | 0.29 | 0.31 | 15 | 0.56 | 0.51 | agree |
| y | 45 | 0.26 | 0.54 | 0.38 | 15 | 0.87 | 1.14 | agree |
| y | 50 | 0.17 | 0.28 | 0.35 | 15 | 0.76 | 0.64 | agree |

Both maps along every verified line and every interval midline (230 places): largest difference 0.000502 in x (tolerance 0.001197, codex 0.2), 0.003497 in y (tolerance 0.02578, claude 35); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.34 px (claude: x 0.33, y 0.36), 0.34 px (codex: x 0.31, y 0.38), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 21; agreed 21; disagreed 0; unmatched 4 (kept as one-sided: 3 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| curve | feature | -/2 | (none) | 0.5, 45.4 | | | unmatched in claude |
| curve | feature | 2/- | 0.5, 45.2 | (none) | | | unmatched in codex |
| curve | trace | 1/- | 0.0, 40.1 (0.0, 0.1) | (no trace at this x) | | | unmatched in codex |
| curve | trace | 21/- | 1.0, 48.6 (0.0, 0.1) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
