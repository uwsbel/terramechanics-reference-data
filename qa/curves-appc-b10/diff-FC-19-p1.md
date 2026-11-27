# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b10\rederived\claude\FC-19\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b10\rederived\codex\FC-19\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 55 | 55 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0130 | 0.0130 |
| RMS residual x, y | 0.001, 0.016 | 0.001, 0.018 |

Corners of claude's box [860, 1450, 2600, 3400] mapped by both calibrations (tolerance 0.00 in x, 0.05 in y):

- (-0.1, 52.9) vs (-0.1, 52.9)
- (1.1, 52.7) vs (1.1, 52.8)
- (-0.1, 27.5) vs (-0.1, 27.5)
- (1.0, 27.3) vs (1.0, 27.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.00 | 0.17 | 0.17 | 12 | 0.50 | 0.50 | agree |
| x | 0.1 | 0.23 | 0.32 | 0.32 | 12 | 0.59 | 0.50 | agree |
| x | 0.2 | 0.44 | 0.24 | 0.18 | 12 | 0.60 | 0.50 | agree |
| x | 0.3 | 0.61 | 0.46 | 0.24 | 12 | 0.92 | 0.50 | agree |
| x | 0.4 | 0.56 | 0.51 | 0.54 | 12 | 1.31 | 1.11 | agree |
| x | 0.5 | 0.37 | 0.28 | 0.40 | 12 | 1.01 | 1.34 | agree |
| x | 0.6 | 0.22 | 0.26 | 0.27 | 12 | 0.56 | 0.50 | agree |
| x | 0.7 | 0.19 | 0.31 | 0.41 | 12 | 0.51 | 0.65 | agree |
| x | 0.8 | 0.52 | 0.21 | 0.52 | 12 | 0.62 | 0.91 | agree |
| x | 0.9 | 0.55 | 0.27 | 0.27 | 12 | 0.54 | 0.90 | agree |
| x | 1 | 0.20 | 0.22 | 0.21 | 12 | 0.53 | 0.50 | agree |
| y | 30 | 0.28 | 0.75 | 0.66 | 25 | 1.03 | 1.03 | agree |
| y | 35 | 0.08 | 0.41 | 0.49 | 25 | 0.92 | 0.85 | agree |
| y | 40 | 0.81 | 0.62 | 0.47 | 25 | 1.24 | 1.02 | agree |
| y | 45 | 0.14 | 0.75 | 0.69 | 25 | 1.25 | 1.10 | agree |
| y | 50 | 0.29 | 0.51 | 0.54 | 25 | 1.09 | 0.91 | agree |

Both maps along every verified line and every interval midline (323 places): largest difference 0.0004023 in x (tolerance 0.001314, claude 0.3), 0.008573 in y (tolerance 0.03057, codex 40); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 16 shared lines checked against the ink, mean of the median distances 0.39 px (claude: x 0.29, y 0.61), 0.40 px (codex: x 0.32, y 0.57), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

4 series in claude, 4 in codex.


## Points

Matched: 71; agreed 71; disagreed 0; unmatched 4 (kept as one-sided: 1 of claude, 3 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| mean | trace | 21/- | 1.0, 52.9 (0.0, 0.1) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
