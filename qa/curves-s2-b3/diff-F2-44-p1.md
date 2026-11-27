# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b3\rederived\claude\F2-44\points-p1-native.csv` (claude), `<repository>\qa\curves-s2-b3\rederived\codex\F2-44\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 28 | 30 |
| x per px | 0.0032 | 0.0032 |
| y per px | 1.2877 | 1.2879 |
| RMS residual x, y | 0.002, 1.658 | 0.003, 1.632 |

Corners of claude's box [725, 1675, 2300, 3270] mapped by both calibrations (tolerance 0.01 in x, 4.58 in y):

- (-0.0, 2034.6) vs (-0.0, 2035.4)
- (5.1, 2026.0) vs (5.1, 2026.1)
- (-0.1, -19.2) vs (-0.1, -18.8)
- (5.0, -27.8) vs (5.0, -28.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 1.31 | 0.36 | 0.39 | 12 | 1.08 | 0.99 | agree |
| x | 1 | 0.52 | 0.34 | 0.32 | 12 | 0.85 | 0.61 | agree |
| x | 2 | 0.21 | 0.29 | 0.35 | 9 | 1.07 | 0.83 | agree |
| x | 3 | 0.49 | 0.35 | 0.36 | 9 | 0.80 | 0.50 | agree |
| x | 4 | 0.30 | 0.27 | 0.18 | 12 | 1.04 | 0.61 | agree |
| x | 5 | 0.98 | 0.30 | 0.32 | 12 | 0.91 | 0.92 | agree |
| y | 0 | 0.31 | 0.31 | 0.41 | 15 | 0.64 | 0.65 | agree |
| y | 500 | 0.47 | 0.47 | 0.33 | 15 | 0.79 | 0.52 | agree |
| y | 1000 | 0.20 | 0.27 | 0.38 | 15 | 1.39 | 1.52 | agree |
| y | 1500 | 0.55 | 0.63 | 0.42 | 15 | 1.21 | 1.36 | agree |
| y | 2000 | 0.26 | 0.68 | 0.80 | 11 | 0.84 | 1.75 | agree |

Both maps along every verified line and every interval midline (232 places): largest difference 0.003519 in x (tolerance 0.006703, claude 0), 0.809 in y (tolerance 3.778, claude 1500); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.39 px (claude: x 0.32, y 0.47), 0.39 px (codex: x 0.32, y 0.47), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 151; agreed 151; disagreed 0; unmatched 9 (kept as one-sided: 0 of claude, 9 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
