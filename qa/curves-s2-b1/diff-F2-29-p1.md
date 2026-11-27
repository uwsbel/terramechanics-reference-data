# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b1\rederived\claude\F2-29\points-p1-native.csv` (claude), `<repository>\qa\curves-s2-b1\rederived\codex\F2-29\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 63 | 63 |
| x per px | 0.0032 | 0.0032 |
| y per px | 0.6443 | 0.6444 |
| RMS residual x, y | 0.006, 0.883 | 0.006, 0.797 |

Corners of claude's box [440, 1100, 2370, 3830] mapped by both calibrations (tolerance 0.02 in x, 2.32 in y):

- (8.8, 1215.3) vs (8.8, 1215.3)
- (8.7, -28.1) vs (8.7, -28.3)
- (-0.1, 1239.8) vs (-0.1, 1240.2)
- (-0.1, -3.6) vs (-0.1, -3.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.15 | 0.26 | 0.36 | 18 | 0.74 | 0.86 | agree |
| x | 1 | 0.25 | 0.47 | 0.46 | 16 | 0.83 | 0.92 | agree |
| x | 2 | 0.12 | 0.38 | 0.41 | 16 | 1.09 | 1.25 | agree |
| x | 3 | 0.58 | 0.37 | 0.43 | 18 | 1.09 | 0.62 | agree |
| x | 4 | 0.08 | 0.36 | 0.37 | 18 | 0.63 | 0.55 | agree |
| x | 5 | 0.23 | 0.25 | 0.33 | 18 | 0.57 | 0.74 | agree |
| x | 6 | 0.23 | 0.44 | 0.49 | 18 | 0.78 | 0.98 | agree |
| x | 7 | 0.48 | 0.35 | 0.25 | 18 | 0.92 | 0.50 | agree |
| x | 8 | 0.26 | 0.40 | 0.33 | 18 | 0.86 | 0.60 | agree |
| y | 0 | 0.23 | 0.33 | 0.41 | 24 | 0.97 | 0.80 | agree |
| y | 200 | 0.40 | 0.37 | 0.44 | 24 | 1.05 | 1.05 | agree |
| y | 400 | 0.08 | 0.44 | 0.41 | 24 | 0.74 | 0.79 | agree |
| y | 600 | 0.43 | 0.31 | 0.42 | 24 | 0.85 | 0.50 | agree |
| y | 800 | 0.30 | 0.41 | 0.44 | 24 | 0.86 | 0.56 | agree |
| y | 1000 | 1.31 | 0.29 | 0.46 | 19 | 0.67 | 0.73 | agree |
| y | 1200 | 0.21 | 0.54 | 0.58 | 24 | 0.72 | 0.88 | agree |

Both maps along every verified line and every interval midline (319 places): largest difference 0.001658 in x (tolerance 0.005539, codex 3), 0.7347 in y (tolerance 1.12, claude 1000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 16 shared lines checked against the ink, mean of the median distances 0.37 px (claude: x 0.37, y 0.38), 0.41 px (codex: x 0.38, y 0.45), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 38; agreed 36; disagreed 2; unmatched 19 (kept as one-sided: 3 of claude, 16 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| lpt27 | feature | 4/17 | 2.5, 483.5 (0.0, 3.2) | 2.6, 485.3 (0.0, 4.3) | -0.1 | -1.8 | **disagree** |
| lpt27 | feature | 5/40 | 5.9, 975.9 (0.0, 3.0) | 6.0, 972.4 (0.0, 3.7) | -0.1 | +3.6 | **disagree** |
| lpt27 | feature | -/4 | (none) | 0.4, 216.5 | | | unmatched in claude |
| lpt27 | feature | -/7 | (none) | 1.0, 147.7 | | | unmatched in claude |
| lpt27 | feature | -/12 | (none) | 1.8, 282.4 | | | unmatched in claude |
| lpt27 | feature | -/15 | (none) | 2.3, 451.1 | | | unmatched in claude |
| lpt27 | feature | -/20 | (none) | 3.1, 574.2 | | | unmatched in claude |
| lpt27 | feature | -/22 | (none) | 3.3, 617.4 | | | unmatched in claude |
| lpt27 | feature | -/24 | (none) | 3.5, 648.7 | | | unmatched in claude |
| lpt27 | feature | -/26 | (none) | 3.8, 676.2 | | | unmatched in claude |
| lpt27 | feature | -/29 | (none) | 4.4, 758.6 | | | unmatched in claude |
| lpt27 | feature | -/31 | (none) | 4.7, 822.6 | | | unmatched in claude |
| lpt27 | feature | -/33 | (none) | 4.8, 825.5 | | | unmatched in claude |
| lpt27 | feature | -/35 | (none) | 5.0, 836.1 | | | unmatched in claude |
| lpt27 | feature | -/38 | (none) | 5.7, 954.7 | | | unmatched in claude |
| lpt27 | feature | -/43 | (none) | 6.3, 983.5 | | | unmatched in claude |
| lpt27 | feature | -/45 | (none) | 6.5, 999.6 | | | unmatched in claude |
| lpt27 | feature | 2/- | 0.4, 216.0 | (none) | | | unmatched in codex |
| lpt27 | feature | 3/- | 0.9, 144.7 | (none) | | | unmatched in codex |
| lpt27 | trace | 1/- | 0.0, 3.8 (0.0, 5.9) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
