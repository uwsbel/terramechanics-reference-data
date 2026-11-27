# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b2\rederived\claude\FC-4B\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b2\rederived\codex\FC-4B\points-p2-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 30 | 12 |
| x per px | 0.1721 | 0.1721 |
| y per px | 0.3418 | 0.3416 |
| RMS residual x, y | 0.218, 0.158 | 0.235, 0.038 |

Corners of claude's box [770, 2780, 2290, 3420] mapped by both calibrations (tolerance 0.62 in x, 0.54 in y):

- (-5.4, 58.5) vs (-5.4, 58.3)
- (256.2, 60.3) vs (256.2, 60.1)
- (-5.6, -160.3) vs (-5.7, -160.3)
- (256.0, -158.5) vs (256.0, -158.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.39 | 0.33 | 0.30 | 12 | 0.74 | 1.69 | agree |
| x | 50 | 1.63 | 0.42 | 0.19 | 12 | 2.20 | 1.18 | agree |
| x | 100 | 0.29 | 0.26 | 0.30 | 22 | 1.71 | 0.92 | agree |
| x | 150 | 0.19 | 0.30 | 0.26 | 12 | 0.69 | 0.77 | agree |
| x | 200 | 0.86 | 0.20 | 0.19 | 20 | 0.61 | 0.75 | agree |
| x | 250 | 0.27 | 0.36 | 0.24 | 12 | 1.62 | 1.70 | agree |
| y | -150 | 0.05 | 0.29 | 0.27 | 15 | 0.74 | 0.71 | agree |
| y | 0 | 0.77 | 0.29 | 0.52 | 23 | 0.50 | 1.06 | agree |
| y | 50 | 0.12 | 0.34 | 0.30 | 15 | 0.64 | 0.59 | agree |

Both maps along every verified line and every interval midline (220 places): largest difference 0.3267 in x (tolerance 0.6681, claude 50), 0.272 in y (tolerance 0.6138, codex 0); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.31 px (claude: x 0.31, y 0.31), 0.28 px (codex: x 0.25, y 0.36), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 64; agreed 64; disagreed 0; unmatched 0 (kept as one-sided: 0 of claude, 0 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
