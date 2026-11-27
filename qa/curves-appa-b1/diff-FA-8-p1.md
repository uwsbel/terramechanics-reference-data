# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b1\rederived\claude\FA-8\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b1\rederived\codex\FA-8\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 30 | 30 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0130 | 0.0130 |
| RMS residual x, y | 0.003, 0.026 | 0.003, 0.026 |

Corners of claude's box [840, 1500, 2425, 3250] mapped by both calibrations (tolerance 0.01 in x, 0.06 in y):

- (-0.0, 50.3) vs (-0.0, 50.3)
- (1.0, 50.3) vs (1.0, 50.3)
- (-0.0, 27.5) vs (-0.0, 27.5)
- (1.0, 27.5) vs (1.0, 27.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.11 | 0.13 | 0.09 | 12 | 0.50 | 0.50 | agree |
| x | 0.2 | 0.18 | 0.28 | 0.25 | 12 | 0.50 | 0.50 | agree |
| x | 0.4 | 0.22 | 0.12 | 0.16 | 12 | 0.50 | 0.50 | agree |
| x | 0.6 | 0.09 | 0.17 | 0.16 | 12 | 0.50 | 0.50 | agree |
| x | 0.8 | 0.10 | 0.24 | 0.30 | 12 | 0.50 | 0.50 | agree |
| x | 1 | 0.33 | 0.37 | 0.28 | 12 | 0.64 | 0.50 | agree |
| y | 30 | 0.12 | 0.42 | 0.36 | 15 | 0.92 | 0.98 | agree |
| y | 35 | 0.00 | 0.00 | 0.00 | 15 | 0.50 | 0.50 | agree |
| y | 40 | 0.10 | 0.14 | 0.04 | 15 | 0.50 | 0.50 | agree |
| y | 45 | 0.06 | 0.15 | 0.17 | 15 | 0.50 | 0.50 | agree |
| y | 50 | 0.29 | 0.26 | 0.20 | 15 | 0.56 | 0.58 | agree |

Both maps along every verified line and every interval midline (294 places): largest difference 0.0003004 in x (tolerance 0.0007291, claude 1), 0.004162 in y (tolerance 0.01496, codex 50); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.21 px (claude: x 0.22, y 0.19), 0.18 px (codex: x 0.21, y 0.15), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 21; agreed 21; disagreed 0; unmatched 5 (kept as one-sided: 4 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| curve | feature | -/2 | (none) | 0.2, 43.7 | | | unmatched in claude |
| curve | feature | 2/- | 0.2, 43.6 | (none) | | | unmatched in codex |
| curve | feature | 3/- | 0.8, 47.3 | (none) | | | unmatched in codex |
| curve | trace | 1/- | 0.0, 43.0 (0.0, 0.1) | (no trace at this x) | | | unmatched in codex |
| curve | trace | 21/- | 1.0, 48.6 (0.0, 0.1) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
