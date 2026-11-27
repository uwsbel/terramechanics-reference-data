# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b5\rederived\claude\FC-1A\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b5\rederived\codex\FC-1A\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 35 | 35 |
| x per px | 3.3975 | 3.3972 |
| y per px | 3.4730 | 3.4729 |
| RMS residual x, y | 23.870, 10.176 | 23.927, 9.974 |

Corners of claude's box [905, 1567, 2125, 3325] mapped by both calibrations (tolerance 51.19 in x, 23.62 in y):

- (-42.4, 6050.0) vs (-41.6, 6050.0)
- (4102.5, 6055.9) vs (4103.0, 6055.4)
- (-52.8, -55.6) vs (-53.0, -55.3)
- (4092.2, -49.7) vs (4091.6, -49.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.00 | 0.49 | 0.49 | 17 | 0.89 | 0.91 | agree |
| x | 1000 | 0.55 | 0.23 | 0.21 | 18 | 1.18 | 0.79 | agree |
| x | 2000 | 0.23 | 0.46 | 0.32 | 18 | 0.84 | 0.67 | agree |
| x | 3000 | 0.31 | 0.30 | 0.33 | 18 | 0.66 | 0.50 | agree |
| x | 4000 | 0.12 | 0.35 | 0.35 | 18 | 0.56 | 0.52 | agree |
| y | 0 | 0.00 | 0.10 | 0.10 | 12 | 0.50 | 0.50 | agree |
| y | 1000 | 0.04 | 0.20 | 0.20 | 12 | 0.50 | 0.50 | agree |
| y | 2000 | 0.52 | 0.42 | 0.33 | 12 | 1.10 | 0.70 | agree |
| y | 3000 | 0.24 | 0.30 | 0.26 | 12 | 0.50 | 0.69 | agree |
| y | 4000 | 0.12 | 0.23 | 0.15 | 12 | 0.79 | 0.68 | agree |
| y | 5000 | 0.65 | 0.35 | 0.26 | 12 | 0.72 | 0.72 | agree |
| y | 6000 | 0.51 | 0.36 | 0.26 | 12 | 0.79 | 0.84 | agree |

Both maps along every verified line and every interval midline (306 places): largest difference 2.117 in x (tolerance 6.922, claude 1000), 2.48 in y (tolerance 5.182, between claude 5000 and codex 5000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 12 shared lines checked against the ink, mean of the median distances 0.32 px (claude: x 0.37, y 0.28), 0.27 px (codex: x 0.34, y 0.22), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.
- marker symbol disagreement in FC-1A/1/dr100-116: claude ['triangle-down'], codex ['filled circle', 'triangle-down']
- marker symbol disagreement in FC-1A/1/dr50-57: claude ['circle'], codex ['circle', 'filled circle', 'triangle-down']


## Points

Matched: 66; agreed 64; disagreed 2; unmatched 12 (kept as one-sided: 4 of claude, 2 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| dr100-116 | feature | 1/1 | 0.0, 772.1 (10.9, 10.3) | -0.1, 804.6 (11.2, 10.6) | +0.1 | -32.6 | **disagree** |
| dr100-116 | marker | 1/- | 3.6, 481.3 | (none) | | | unmatched in codex |
| dr100-116 | marker | -/4 | (none) | 1794.0, 2882.5 | | | unmatched in claude |
| dr100-116 | trace | 1/- | 0.0, 772.1 (10.9, 10.3) | (no trace at this x) | | | unmatched in codex |
| dr50-57 | marker | -/1 | (none) | 3.6, 481.3 | | | unmatched in claude |
| dr50-57 | marker | -/3 | (none) | 299.4, 767.0 | | | unmatched in claude |
| dr50-57 | trace | 15/- | 3462.4, 4035.4 (9.5, 10.6) | (no trace at this x) | | | unmatched in codex |
| dr73-88 | feature | 1/1 | 0.0, 665.7 (10.0, 9.4) | -0.1, 685.2 (10.4, 9.8) | +0.1 | -19.5 | **disagree** |
| dr73-88 | marker | 1/- | 299.0, 771.9 | (none) | | | unmatched in codex |
| dr73-88 | marker | 3/- | 1791.8, 2877.0 | (none) | | | unmatched in codex |
| dr73-88 | trace | 1/- | 0.0, 665.7 (10.0, 9.4) | (no trace at this x) | | | unmatched in codex |
| dr73-88 | trace | 16/- | 3530.6, 4518.5 (8.7, 9.7) | (no trace at this x) | | | unmatched in codex |
| dr100-116 | marker | 1 (claude) | 3.6, 481.3 | codex: dr50-57 (triangle-down) | | | **identity conflict** |
| dr100-116 | marker | 4 (codex) | 1794.0, 2882.5 | claude: dr73-88 (filled circle) | | | **identity conflict** |
| dr50-57 | marker | 1 (codex) | 3.6, 481.3 | claude: dr100-116 (triangle-down) | | | **identity conflict** |
| dr50-57 | marker | 3 (codex) | 299.4, 767.0 | claude: dr73-88 (filled circle) | | | **identity conflict** |
| dr73-88 | marker | 1 (claude) | 299.0, 771.9 | codex: dr50-57 (filled circle) | | | **identity conflict** |
| dr73-88 | marker | 3 (claude) | 1791.8, 2877.0 | codex: dr100-116 (filled circle) | | | **identity conflict** |
