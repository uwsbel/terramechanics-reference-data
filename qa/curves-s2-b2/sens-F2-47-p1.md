# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b2\rederived\claude\F2-47\points-p1-native.csv` (claude), `<repository>\qa\curves-s2-b2\rederived\codex\F2-47\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 40 | 40 |
| x per px | 0.0032 | 0.0032 |
| y per px | 1.2866 | 1.2865 |
| RMS residual x, y | 0.003, 1.690 | 0.004, 1.585 |

Corners of claude's box [470, 1660, 2670, 3255] mapped by both calibrations (tolerance 0.01 in x, 4.56 in y):

- (-0.0, 2043.1) vs (-0.0, 2043.2)
- (7.1, 2009.2) vs (7.1, 2009.3)
- (-0.1, -8.9) vs (-0.1, -8.7)
- (7.0, -42.8) vs (7.0, -42.6)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.23 | 0.26 | 0.27 | 12 | 0.72 | 0.88 | agree |
| x | 1 | 0.22 | 0.10 | 0.14 | 12 | 0.50 | 0.50 | agree |
| x | 2 | 0.33 | 0.47 | 0.26 | 11 | 0.83 | 0.63 | agree |
| x | 3 | 0.38 | 0.29 | 0.21 | 12 | 0.77 | 0.50 | agree |
| x | 4 | 0.16 | 0.24 | 0.25 | 10 | 0.50 | 0.50 | agree |
| x | 5 | 0.18 | 0.24 | 0.28 | 12 | 0.50 | 0.59 | agree |
| x | 6 | 1.26 | 0.34 | 0.76 | 12 | 0.62 | 1.96 | agree |
| x | 7 | 1.19 | 0.63 | 1.06 | 12 | 1.49 | 1.96 | agree; codex off the ink |
| y | 0 | 0.42 | 0.34 | 0.37 | 21 | 0.92 | 0.58 | agree |
| y | 500 | 0.09 | 0.51 | 0.59 | 21 | 0.87 | 0.83 | agree |
| y | 1000 | 0.25 | 0.58 | 0.54 | 19 | 1.22 | 0.94 | agree |
| y | 1500 | 0.47 | 0.30 | 0.31 | 21 | 1.12 | 0.61 | agree |
| y | 2000 | 0.33 | 0.27 | 0.46 | 21 | 0.61 | 0.58 | agree |

Both maps along every verified line and every interval midline (262 places): largest difference 0.003656 in x (tolerance 0.01125, claude 7), 0.5171 in y (tolerance 2.267, codex 0); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 13 shared lines checked against the ink, mean of the median distances 0.35 px (claude: x 0.32, y 0.40), 0.42 px (codex: x 0.40, y 0.45), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

2 series in claude, 2 in codex.


## Points

Matched: 71; agreed 65; disagreed 6; unmatched 9 (kept as one-sided: 0 of claude, 9 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| lpt101 | feature | 2/4 | 0.5, 365.5 (0.0, 5.8) | 0.4, 312.7 (0.0, 15.7) | +0.1 | +52.8 | **disagree** |
| lpt101 | feature | -/12 | (none) | 1.7, 371.1 | | | unmatched in claude |
| lpt91 | feature | 2/4 | 0.5, 289.1 (0.0, 3.9) | 0.4, 275.1 (0.0, 3.5) | +0.1 | +14.0 | **disagree** |
| lpt91 | feature | 4/25 | 4.0, 881.7 (0.0, 4.0) | 4.0, 889.2 (0.0, 3.8) | -0.1 | -7.5 | **disagree** |
| lpt91 | feature | 5/31 | 5.0, 1049.6 (0.0, 4.1) | 5.2, 1096.9 (0.0, 2.8) | -0.3 | -47.4 | **disagree** |
| lpt91 | feature | 6/30 | 5.1, 1071.8 (0.0, 4.1) | 5.1, 1075.5 (0.0, 3.5) | -0.1 | -3.7 | **disagree** |
| lpt91 | feature | 7/36 | 6.1, 1286.5 (0.0, 4.1) | 6.1, 1267.6 (0.0, 2.7) | +0.1 | +18.9 | **disagree** |
| lpt91 | feature | -/9 | (none) | 1.1, 321.3 | | | unmatched in claude |
| lpt91 | feature | -/13 | (none) | 2.0, 476.9 | | | unmatched in claude |
| lpt91 | feature | -/15 | (none) | 2.2, 512.8 | | | unmatched in claude |
| lpt91 | feature | -/22 | (none) | 3.7, 831.2 | | | unmatched in claude |
