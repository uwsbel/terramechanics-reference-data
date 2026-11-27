# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b2\rederived\claude\FA-22\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b2\rederived\codex\FA-22\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 116 | 974 |
| x per px | 0.0010 | 0.0010 |
| y per px | 0.0686 | 0.0686 |
| RMS residual x, y | 0.002, 0.048 | 0.002, 0.049 |

Corners of claude's box [745, 1172, 2245, 3785] mapped by both calibrations (tolerance 0.01 in x, 0.17 in y (in the plotting coordinates of log10 x, linear y)):

- (9.4, 100.8) vs (9.4, 100.8)
- (9.3, -2.1) vs (9.3, -2.1)
- (0.0, 101.6) vs (0.0, 101.5)
- (0.0, -1.3) vs (0.0, -1.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0.02 | 0.39 | 0.87 | 0.81 | 20 | 0.88 | 0.89 | agree |
| x | 0.05 | 0.26 | 0.74 | 0.66 | 21 | 1.42 | 0.99 | agree |
| x | 0.1 | 0.12 | 0.68 | 0.66 | 21 | 1.13 | 0.97 | agree |
| x | 0.2 | 0.27 | 0.33 | 0.26 | 21 | 0.82 | 0.50 | agree |
| x | 0.5 | 0.13 | 0.49 | 0.51 | 20 | 0.90 | 0.68 | agree |
| x | 1 | 0.16 | 0.62 | 0.49 | 23 | 0.93 | 0.98 | agree |
| x | 1.5 | 0.09 | 0.39 | 0.41 | 23 | 0.67 | 0.64 | agree |
| x | 2 | 0.18 | 0.32 | 0.27 | 23 | 0.68 | 0.83 | agree |
| x | 3 | 0.08 | 0.50 | 0.47 | 22 | 0.67 | 1.20 | agree |
| x | 4 | 0.15 | 0.37 | 0.34 | 23 | 0.87 | 0.80 | agree |
| x | 5 | 0.25 | 0.56 | 0.64 | 23 | 1.03 | 1.29 | agree |
| x | 9 | 0.31 | 0.29 | 0.44 | 23 | 0.72 | 0.89 | agree |
| y | 0 | 0.08 | 0.44 | 0.41 | 23 | 0.52 | 0.67 | agree |
| y | 10 | 0.52 | 0.44 | 0.30 | 23 | 0.91 | 1.02 | agree |
| y | 20 | 0.21 | 0.39 | 0.29 | 23 | 0.60 | 0.59 | agree |
| y | 30 | 0.16 | 0.20 | 0.19 | 23 | 0.50 | 0.50 | agree |
| y | 40 | 0.08 | 0.23 | 0.24 | 22 | 0.66 | 0.61 | agree |
| y | 50 | 0.36 | 0.65 | 0.63 | 23 | 1.11 | 1.05 | agree |
| y | 60 | 0.54 | 0.66 | 0.75 | 22 | 1.36 | 1.16 | agree |
| y | 70 | 0.34 | 0.30 | 0.38 | 21 | 0.50 | 0.54 | agree |
| y | 80 | 0.18 | 0.26 | 0.28 | 21 | 0.67 | 0.72 | agree |
| y | 90 | 0.69 | 0.34 | 0.28 | 21 | 1.58 | 0.50 | agree |
| y | 100 | 0.39 | 0.27 | 0.24 | 19 | 0.76 | 0.50 | agree |

(In the plotting coordinates: log10 x, linear y.) Both maps along every verified line and every interval midline (524 places): largest difference 0.001121 in x (tolerance 0.002484, codex 0.02), 0.1459 in y (tolerance 0.1418, claude 90); 2 beyond the two maps' line errors.

Canonical reading: claude (same lines; 23 shared lines checked against the ink, mean of the median distances 0.45 px (claude: x 0.51, y 0.38), 0.43 px (codex: x 0.50, y 0.36), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.
- marker symbol disagreement in FA-22/1/upper: claude ['circle', 'x'], codex ['circle']


## Points

Matched: 159; agreed 159; disagreed 0; unmatched 15 (kept as one-sided: 2 of claude, 13 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| average | feature | -/3 | (none) | 4.6, 91.2 | | | unmatched in claude |
| average | feature | -/4 | (none) | 2.5, 68.5 | | | unmatched in claude |
| lower | feature | -/3 | (none) | 4.6, 89.0 | | | unmatched in claude |
| lower | feature | -/4 | (none) | 2.5, 60.3 | | | unmatched in claude |
| lower | marker | 9/- | 9.5, 99.8 | (none) | | | unmatched in codex |
| lower | marker | -/1 | (none) | 4.8, 91.1 | | | unmatched in claude |
| lower | marker | -/6 | (none) | 0.6, 30.6 | | | unmatched in claude |
| upper | feature | -/4 | (none) | 2.5, 82.7 | | | unmatched in claude |
| upper | marker | 10/- | 9.5, 99.8 | (none) | | | unmatched in codex |

## Ink check (D-031): 2 trace samples excluded

No hand decision overridden.
