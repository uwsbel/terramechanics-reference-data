# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b3\rederived\claude\FC-6C\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b3\rederived\codex\FC-6C\points-p2-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 18 | 18 |
| x per px | 0.1712 | 0.1712 |
| y per px | 0.3395 | 0.3394 |
| RMS residual x, y | 0.585, 0.080 | 0.581, 0.072 |

Corners of claude's box [638, 2540, 2160, 3170] mapped by both calibrations (tolerance 1.34 in x, 0.49 in y):

- (-3.9, 109.6) vs (-3.9, 109.6)
- (256.6, 105.7) vs (256.6, 105.5)
- (-5.3, -104.2) vs (-5.3, -104.2)
- (255.2, -108.2) vs (255.3, -108.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.15 | 0.40 | 0.45 | 6 | 0.55 | 0.76 | agree |
| x | 50 | 0.25 | 0.28 | 0.24 | 6 | 0.50 | 0.54 | agree |
| x | 100 | 0.10 | 0.22 | 0.17 | 6 | 0.51 | 0.53 | agree |
| x | 150 | 0.08 | 0.29 | 0.28 | 6 | 0.56 | 0.50 | agree |
| x | 200 | 0.25 | 0.34 | 0.22 | 6 | 0.92 | 0.62 | agree |
| x | 250 | 0.17 | 0.30 | 0.22 | 6 | 0.53 | 0.50 | agree |
| y | -100 | 0.09 | 0.38 | 0.37 | 15 | 0.62 | 0.63 | agree |
| y | 0 | 0.39 | 0.23 | 0.13 | 15 | 0.59 | 0.50 | agree |
| y | 100 | 0.39 | 0.31 | 0.32 | 15 | 0.74 | 0.50 | agree |

Both maps along every verified line and every interval midline (184 places): largest difference 0.04253 in x (tolerance 0.183, claude 50), 0.1423 in y (tolerance 0.4209, between codex 0 and claude 100); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.31 px (claude: x 0.31, y 0.31), 0.27 px (codex: x 0.26, y 0.27), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 64; agreed 62; disagreed 2; unmatched 0 (kept as one-sided: 0 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n4695 | marker | 11/11 | 215.8, -29.8 (0.5, 0.9) | 217.9, -29.6 (1.0, 1.9) | -2.1 | -0.2 | **disagree** |
| n4695 | marker | 12/12 | 245.0, -29.2 (0.5, 0.9) | 246.9, -30.0 (1.0, 1.9) | -1.8 | +0.8 | **disagree** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
