# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b3\rederived\claude\F2-42\points-p1-native.csv` (claude), `<repository>\qa\curves-s2-b3\rederived\codex\F2-42\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 26 | 28 |
| x per px | 0.0032 | 0.0032 |
| y per px | 0.6438 | 0.6437 |
| RMS residual x, y | 0.006, 0.611 | 0.007, 1.042 |

Corners of claude's box [800, 1420, 1800, 3380] mapped by both calibrations (tolerance 0.02 in x, 2.30 in y):

- (-0.1, 1243.9) vs (-0.1, 1243.7)
- (3.1, 1244.9) vs (3.1, 1245.4)
- (-0.1, -18.0) vs (-0.1, -17.8)
- (3.1, -17.0) vs (3.1, -16.2)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.78 | 0.43 | 0.24 | 18 | 1.03 | 1.11 | agree |
| x | 1 | 0.19 | 0.35 | 0.34 | 18 | 0.50 | 0.50 | agree |
| x | 2 | 0.26 | 0.26 | 0.29 | 14 | 0.50 | 0.67 | agree |
| x | 3 | 0.12 | 0.18 | 0.18 | 16 | 0.50 | 0.99 | agree |
| y | 0 | 0.13 | 0.26 | 0.23 | 9 | 0.50 | 0.50 | agree |
| y | 200 | 0.37 | 0.48 | 0.51 | 9 | 0.99 | 0.92 | agree |
| y | 400 | 0.32 | 0.22 | 0.32 | 23 | 0.74 | 0.56 | agree |
| y | 600 | 0.43 | 0.40 | 0.16 | 9 | 0.70 | 0.58 | agree |
| y | 800 | 0.28 | 0.53 | 0.58 | 9 | 1.21 | 0.93 | agree |
| y | 1000 | 0.07 | 0.82 | 0.89 | 9 | 1.45 | 1.34 | agree |
| y | 1200 | 0.22 | 0.64 | 0.43 | 9 | 1.01 | 1.10 | agree |

Both maps along every verified line and every interval midline (274 places): largest difference 0.002745 in x (tolerance 0.006924, claude 0), 1.126 in y (tolerance 1.265, claude 400); 2 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.42 px (claude: x 0.30, y 0.48), 0.38 px (codex: x 0.26, y 0.44), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

4 series in claude, 4 in codex.


## Points

Matched: 69; agreed 64; disagreed 5; unmatched 33 (kept as one-sided: 16 of claude, 17 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| lpt22 | feature | -/16 | (none) | 1.4, 843.6 | | | unmatched in claude |
| lpt22 | feature | 16/- | 1.4, 843.6 | (none) | | | unmatched in codex |
| lpt22 | trace | 2/- | 0.0, 53.5 (0.0, 3.6) | (no trace at this x) | | | unmatched in codex |
| lpt22 | trace | 3/- | 0.1, 98.3 (0.0, 5.0) | (no trace at this x) | | | unmatched in codex |
| lpt22 | trace | 20/- | 2.3, 1100.4 (0.0, 4.0) | (no trace at this x) | | | unmatched in codex |
| lpt23 | feature | 1/2 | 0.0, 146.2 (0.0, 5.7) | 0.0, 1.3 (0.1, 11.7) | +0.0 | +144.9 | **disagree** |
| lpt23 | feature | 14/15 | 0.9, 1061.5 (0.0, 6.0) | 0.8, 1031.8 (0.0, 4.2) | +0.1 | +29.8 | **disagree** |
| lpt23 | trace | 2/- | 0.1, 190.9 (0.0, 5.1) | (no trace at this x) | | | unmatched in codex |
| lpt23 | trace | 13/- | 0.8, 1018.5 (0.0, 4.1) | (no trace at this x) | | | unmatched in codex |
| lpt23 | trace | 15/- | 1.0, 1073.4 (0.0, 4.0) | (no trace at this x) | | | unmatched in codex |
| lpt23 | trace | 16/- | 1.3, 1086.0 (0.0, 4.0) | (no trace at this x) | | | unmatched in codex |
| lpt23 | trace | 17/- | 1.5, 1085.8 (0.0, 4.0) | (no trace at this x) | | | unmatched in codex |
| lpt24 | feature | -/19 | (none) | 1.5, 855.6 | | | unmatched in claude |
| lpt24 | feature | 17/20 | 1.5, 855.2 (0.0, 4.7) | 1.7, 885.5 (0.0, 6.6) | -0.2 | -30.4 | **disagree** |
| lpt25 | feature | 1/2 | 0.0, 79.1 (0.0, 5.6) | -0.0, 1.9 (0.0, 12.7) | +0.0 | +77.2 | **disagree** |
| lpt25 | feature | 13/15 | 0.7, 958.6 (0.0, 6.1) | 0.9, 996.6 (0.0, 6.3) | -0.2 | -38.0 | **disagree** |
| lpt25 | trace | 2/- | 0.0, 91.3 (0.0, 4.3) | (no trace at this x) | | | unmatched in codex |
| lpt25 | trace | 3/- | 0.0, 190.9 (0.0, 5.1) | (no trace at this x) | | | unmatched in codex |
| lpt25 | trace | 4/- | 0.1, 291.8 (0.0, 5.1) | (no trace at this x) | | | unmatched in codex |
| lpt25 | trace | 14/- | 0.8, 963.1 (0.0, 4.8) | (no trace at this x) | | | unmatched in codex |
| lpt25 | trace | 15/- | 1.0, 1008.0 (0.0, 4.8) | (no trace at this x) | | | unmatched in codex |
| lpt25 | trace | 19/- | 2.0, 1162.0 (0.0, 4.6) | (no trace at this x) | | | unmatched in codex |
| lpt25 | trace | 20/- | 2.2, 1219.2 (0.0, 4.7) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
