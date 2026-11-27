# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b1\rederived\claude\F2-33\points-p1-native.csv` (claude), `<repository>\qa\curves-s2-b1\rederived\codex\F2-33\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 36 | 36 |
| x per px | 0.0032 | 0.0032 |
| y per px | 1.2866 | 1.2866 |
| RMS residual x, y | 0.009, 3.545 | 0.010, 3.532 |

Corners of claude's box [330, 2040, 2345, 3650] mapped by both calibrations (tolerance 0.02 in x, 8.36 in y):

- (5.1, 2543.0) vs (5.1, 2542.9)
- (5.1, -49.4) vs (5.1, -49.6)
- (-0.1, 2556.0) vs (-0.1, 2556.0)
- (-0.1, -36.3) vs (-0.1, -36.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.39 | 0.65 | 0.39 | 15 | 1.20 | 0.84 | agree |
| x | 1 | 0.33 | 0.62 | 0.57 | 14 | 1.04 | 0.66 | agree |
| x | 2 | 0.78 | 0.58 | 0.81 | 14 | 1.83 | 1.53 | agree |
| x | 3 | 0.79 | 0.41 | 0.46 | 13 | 1.36 | 0.86 | agree |
| x | 4 | 0.06 | 0.37 | 0.42 | 13 | 2.10 | 2.06 | agree |
| x | 5 | 0.63 | 0.45 | 0.37 | 14 | 1.20 | 0.63 | agree |
| y | 0 | 0.30 | 0.21 | 0.17 | 15 | 0.55 | 0.50 | agree |
| y | 500 | 0.28 | 0.31 | 0.32 | 15 | 0.58 | 0.62 | agree |
| y | 1000 | 0.31 | 0.37 | 0.24 | 15 | 0.65 | 0.52 | agree |
| y | 1500 | 0.39 | 0.32 | 0.24 | 14 | 0.83 | 0.54 | agree |
| y | 2000 | 0.22 | 0.34 | 0.39 | 15 | 0.50 | 0.77 | agree |
| y | 2500 | 0.09 | 0.17 | 0.22 | 15 | 0.52 | 0.50 | agree |

Both maps along every verified line and every interval midline (260 places): largest difference 0.002981 in x (tolerance 0.01106, claude 3), 0.4548 in y (tolerance 1.784, claude 1500); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 12 shared lines checked against the ink, mean of the median distances 0.40 px (claude: x 0.52, y 0.29), 0.38 px (codex: x 0.51, y 0.26), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

4 series in claude, 4 in codex.


## Points

Matched: 55; agreed 50; disagreed 5; unmatched 14 (kept as one-sided: 6 of claude, 8 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| lpt74 | feature | 21/- | 0.5, 857.7 | (none) | | | unmatched in codex |
| lpt74 | feature | 22/- | 1.0, 721.5 | (none) | | | unmatched in codex |
| lpt74 | feature | 20/1 | 0.0, 32.5 (0.0, 6.8) | 0.0, 60.5 (0.0, 3.6) | -0.0 | -28.0 | **disagree** |
| lpt74 | feature | 25/- | 4.2, 1696.7 | (none) | | | unmatched in codex |
| lpt74 | feature | 23/21 | 3.5, 1377.2 (0.0, 7.0) | 3.5, 1392.6 (0.0, 2.3) | -0.0 | -15.4 | **disagree** |
| lpt74 | feature | 24/24 | 4.0, 1553.4 (0.0, 7.0) | 4.2, 1679.9 (0.0, 2.4) | -0.2 | -126.5 | **disagree** |
| lpt74 | feature | -/4 | (none) | 0.5, 865.1 | | | unmatched in claude |
| lpt74 | feature | -/8 | (none) | 1.1, 719.5 | | | unmatched in claude |
| lpt74 | feature | -/10 | (none) | 1.3, 747.4 | | | unmatched in claude |
| lpt74 | feature | -/15 | (none) | 2.3, 1050.1 | | | unmatched in claude |
| lpt74 | trace | 19/- | 4.5, 1770.3 (0.0, 2.1) | (no trace at this x) | | | unmatched in codex |
| lpt75 | feature | 12/1 | 2.0, 10.8 (0.0, 3.6) | 2.0, 0.2 (0.0, 3.6) | +0.0 | +10.6 | **disagree** |
| lpt75 | feature | 13/8 | 2.9, 1631.1 (0.0, 7.0) | 2.8, 1602.8 (0.0, 6.2) | +0.1 | +28.4 | **disagree** |
| lpt75 | feature | -/3 | (none) | 2.1, 533.7 | | | unmatched in claude |
| lpt75 | feature | -/6 | (none) | 2.5, 1396.3 | | | unmatched in claude |
| lpt75 | feature | -/10 | (none) | 3.2, 1734.8 | | | unmatched in claude |
| lpt75 | feature | 14/- | 3.3, 1741.2 | (none) | | | unmatched in codex |
| lpt75 | trace | 11/- | 4.5, 1801.9 (0.0, 2.4) | (no trace at this x) | | | unmatched in codex |
