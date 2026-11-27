# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b1\rederived\claude\FA-48\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b1\rederived\codex\FA-48\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 30 | 30 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0131 | 0.0131 |
| RMS residual x, y | 0.003, 0.039 | 0.003, 0.039 |

Corners of claude's box [770, 1430, 2400, 3350] mapped by both calibrations (tolerance 0.01 in x, 0.09 in y):

- (-0.0, 52.6) vs (-0.0, 52.6)
- (1.0, 52.5) vs (1.0, 52.5)
- (-0.0, 27.5) vs (-0.0, 27.5)
- (1.0, 27.4) vs (1.0, 27.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.21 | 0.22 | 0.30 | 12 | 0.68 | 0.76 | agree |
| x | 0.2 | 0.22 | 0.29 | 0.27 | 12 | 0.54 | 0.50 | agree |
| x | 0.4 | 0.10 | 0.26 | 0.26 | 12 | 0.57 | 0.50 | agree |
| x | 0.6 | 0.02 | 0.16 | 0.16 | 12 | 0.50 | 0.50 | agree |
| x | 0.8 | 0.25 | 0.32 | 0.20 | 12 | 1.03 | 0.77 | agree |
| x | 1 | 0.38 | 0.39 | 0.37 | 12 | 0.97 | 0.84 | agree |
| y | 30 | 0.25 | 0.40 | 0.44 | 15 | 0.64 | 0.79 | agree |
| y | 35 | 0.19 | 0.32 | 0.28 | 15 | 0.67 | 0.78 | agree |
| y | 40 | 0.38 | 0.44 | 0.29 | 15 | 1.04 | 0.76 | agree |
| y | 45 | 0.21 | 0.28 | 0.22 | 15 | 0.66 | 0.61 | agree |
| y | 50 | 0.21 | 0.42 | 0.30 | 15 | 1.01 | 0.89 | agree |

Both maps along every verified line and every interval midline (224 places): largest difference 0.0002378 in x (tolerance 0.001183, codex 1), 0.004181 in y (tolerance 0.02403, claude 40); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.32 px (claude: x 0.27, y 0.37), 0.28 px (codex: x 0.26, y 0.31), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 21; agreed 21; disagreed 0; unmatched 3 (kept as one-sided: 2 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| curve | feature | -/2 | (none) | 0.8, 48.8 | | | unmatched in claude |
| curve | trace | 1/- | 0.0, 38.2 (0.0, 0.1) | (no trace at this x) | | | unmatched in codex |
| curve | trace | 21/- | 1.0, 50.6 (0.0, 0.1) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
