# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b2\rederived\claude\F2-48\points-p1-native.csv` (claude), `<repository>\qa\curves-s2-b2\rederived\codex\F2-48\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 63 | 63 |
| x per px | 0.0033 | 0.0033 |
| y per px | 0.6480 | 0.6480 |
| RMS residual x, y | 0.062, 0.960 | 0.063, 0.944 |

Corners of claude's box [380, 1200, 2320, 3820] mapped by both calibrations (tolerance 0.13 in x, 2.55 in y):

- (8.5, 1228.4) vs (8.5, 1228.5)
- (8.6, -28.8) vs (8.6, -28.7)
- (-0.1, 1223.4) vs (-0.1, 1223.3)
- (-0.0, -33.8) vs (-0.0, -33.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.12 | 0.28 | 0.24 | 18 | 0.50 | 0.55 | agree |
| x | 1 | 0.06 | 0.64 | 0.66 | 18 | 0.77 | 0.82 | agree |
| x | 2 | 0.12 | 0.50 | 0.53 | 18 | 0.86 | 0.98 | agree |
| x | 3 | 0.11 | 0.60 | 0.66 | 18 | 0.99 | 0.93 | agree |
| x | 4 | 0.18 | 0.40 | 0.36 | 18 | 0.63 | 0.50 | agree |
| x | 5 | 0.10 | 0.40 | 0.44 | 18 | 0.78 | 0.65 | agree |
| x | 6 | 0.27 | 0.41 | 0.42 | 18 | 0.69 | 0.50 | agree |
| x | 7 | 0.26 | 0.32 | 0.32 | 17 | 0.67 | 0.50 | agree |
| x | 8 | 0.09 | 0.47 | 0.41 | 17 | 0.83 | 0.76 | agree |
| y | 0 | 0.16 | 0.18 | 0.22 | 24 | 0.50 | 0.50 | agree |
| y | 200 | 0.16 | 0.39 | 0.36 | 24 | 0.62 | 0.54 | agree |
| y | 400 | 0.03 | 0.27 | 0.26 | 24 | 0.50 | 0.50 | agree |
| y | 600 | 0.32 | 0.23 | 0.25 | 23 | 0.63 | 0.50 | agree |
| y | 800 | 0.31 | 0.30 | 0.31 | 24 | 0.54 | 0.54 | agree |
| y | 1000 | 0.31 | 0.27 | 0.27 | 24 | 0.80 | 0.55 | agree |
| y | 1200 | 0.24 | 0.29 | 0.26 | 24 | 0.54 | 0.50 | agree |

Both maps along every verified line and every interval midline (343 places): largest difference 0.0007382 in x (tolerance 0.004204, claude 6), 0.2192 in y (tolerance 0.7636, claude 800); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 16 shared lines checked against the ink, mean of the median distances 0.37 px (claude: x 0.45, y 0.27), 0.37 px (codex: x 0.45, y 0.27), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

2 series in claude, 2 in codex.


## Points

Matched: 78; agreed 74; disagreed 4; unmatched 11 (kept as one-sided: 2 of claude, 9 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| lpt85 | feature | 9/8 | 1.3, 95.5 (0.0, 4.3) | 1.2, 92.1 (0.0, 3.7) | +0.1 | +3.4 | **disagree** |
| lpt85 | trace | 2/- | 0.1, 10.5 (0.0, 5.5) | (no trace at this x) | | | unmatched in codex |
| lpt87 | feature | 1/2 | 0.0, 15.1 (0.0, 3.6) | 0.0, 0.2 (0.0, 5.5) | +0.0 | +14.9 | **disagree** |
| lpt87 | feature | 3/3 | 0.1, 32.6 (0.0, 3.6) | 0.2, 81.8 (0.0, 3.1) | -0.1 | -49.2 | **disagree** |
| lpt87 | feature | 5/7 | 0.4, 153.7 (0.0, 4.3) | 0.7, 153.6 (0.0, 2.0) | -0.3 | +0.1 | **disagree** |
| lpt87 | feature | -/12 | (none) | 1.4, 153.6 | | | unmatched in claude |
| lpt87 | feature | -/21 | (none) | 2.8, 285.9 | | | unmatched in claude |
| lpt87 | feature | -/22 | (none) | 2.9, 297.9 | | | unmatched in claude |
| lpt87 | feature | -/30 | (none) | 4.6, 474.2 | | | unmatched in claude |
| lpt87 | feature | -/31 | (none) | 4.7, 484.5 | | | unmatched in claude |
| lpt87 | feature | -/36 | (none) | 5.7, 601.7 | | | unmatched in claude |
| lpt87 | trace | 2/- | 0.0, 15.1 (0.0, 3.6) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
