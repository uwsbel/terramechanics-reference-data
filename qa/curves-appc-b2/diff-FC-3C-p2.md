# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b2\rederived\claude\FC-3C\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b2\rederived\codex\FC-3C\points-p2-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 18 | 18 |
| x per px | 0.1718 | 0.1718 |
| y per px | 0.3430 | 0.3430 |
| RMS residual x, y | 0.306, 0.279 | 0.312, 0.287 |

Corners of claude's box [805, 2960, 2300, 3580] mapped by both calibrations (tolerance 0.79 in x, 0.91 in y):

- (-3.3, 108.2) vs (-3.3, 108.2)
- (253.6, 104.8) vs (253.6, 104.8)
- (-4.6, -104.5) vs (-4.6, -104.5)
- (252.3, -107.9) vs (252.3, -107.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.25 | 0.15 | 0.18 | 6 | 0.50 | 0.51 | agree |
| x | 50 | 0.25 | 0.21 | 0.13 | 6 | 0.53 | 0.50 | agree |
| x | 100 | 0.15 | 0.18 | 0.23 | 6 | 0.60 | 0.50 | agree |
| x | 150 | 0.25 | 0.36 | 0.41 | 6 | 0.58 | 0.65 | agree |
| x | 200 | 0.00 | 0.23 | 0.23 | 6 | 0.55 | 0.55 | agree |
| x | 250 | 0.25 | 0.22 | 0.18 | 6 | 0.95 | 0.65 | agree |
| y | -100 | 0.17 | 0.22 | 0.20 | 15 | 0.62 | 0.53 | agree |
| y | 0 | 0.10 | 0.36 | 0.32 | 15 | 0.60 | 0.55 | agree |
| y | 100 | 0.08 | 0.17 | 0.18 | 15 | 0.53 | 0.50 | agree |

Both maps along every verified line and every interval midline (186 places): largest difference 0.05646 in x (tolerance 0.1787, between claude 0 and codex 50), 0.06547 in y (tolerance 0.404, claude -100); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.23 px (claude: x 0.22, y 0.25), 0.23 px (codex: x 0.22, y 0.23), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 64; agreed 64; disagreed 0; unmatched 0 (kept as one-sided: 0 of claude, 0 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
