# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b2\rederived\claude\F2-46\points-p1-native.csv` (claude), `<repository>\qa\curves-s2-b2\rederived\codex\F2-46\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 49 | 49 |
| x per px | 0.0033 | 0.0033 |
| y per px | 0.3200 | 0.3200 |
| RMS residual x, y | 0.006, 0.532 | 0.007, 0.512 |

Corners of claude's box [560, 1480, 2480, 3500] mapped by both calibrations (tolerance 0.02 in x, 1.36 in y):

- (-0.1, 625.8) vs (-0.1, 625.8)
- (6.1, 628.3) vs (6.1, 628.2)
- (-0.1, -20.5) vs (-0.1, -20.5)
- (6.1, -18.1) vs (6.1, -18.2)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.38 | 0.04 | 0.18 | 18 | 0.51 | 0.50 | agree |
| x | 1 | 0.38 | 0.25 | 0.26 | 18 | 0.76 | 0.50 | agree |
| x | 2 | 0.41 | 0.28 | 0.12 | 16 | 1.00 | 0.60 | agree |
| x | 3 | 0.36 | 0.23 | 0.16 | 17 | 0.57 | 0.50 | agree |
| x | 4 | 0.27 | 0.19 | 0.07 | 17 | 0.50 | 0.50 | agree |
| x | 5 | 0.50 | 0.34 | 0.23 | 17 | 1.07 | 0.57 | agree |
| x | 6 | 0.33 | 0.36 | 0.28 | 18 | 0.77 | 0.51 | agree |
| y | 0 | 0.36 | 0.33 | 0.41 | 18 | 0.74 | 0.50 | agree |
| y | 100 | 0.24 | 0.43 | 0.45 | 18 | 0.98 | 0.88 | agree |
| y | 200 | 0.28 | 0.32 | 0.29 | 18 | 0.50 | 0.71 | agree |
| y | 300 | 0.26 | 0.44 | 0.44 | 18 | 0.83 | 0.59 | agree |
| y | 400 | 0.29 | 0.38 | 0.39 | 17 | 0.77 | 0.50 | agree |
| y | 500 | 0.41 | 0.38 | 0.27 | 18 | 1.00 | 0.52 | agree |
| y | 600 | 0.41 | 0.47 | 0.40 | 17 | 0.75 | 1.00 | agree |

Both maps along every verified line and every interval midline (338 places): largest difference 0.00177 in x (tolerance 0.005409, codex 5), 0.15 in y (tolerance 0.6382, claude 600); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 14 shared lines checked against the ink, mean of the median distances 0.32 px (claude: x 0.24, y 0.39), 0.28 px (codex: x 0.19, y 0.38), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

2 series in claude, 2 in codex.


## Points

Matched: 65; agreed 60; disagreed 5; unmatched 16 (kept as one-sided: 1 of claude, 15 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| lpt89 | feature | 2/5 | 0.4, 47.6 (0.0, 1.7) | 0.6, 59.2 (0.0, 1.4) | -0.2 | -11.6 | **disagree** |
| lpt89 | feature | -/10 | (none) | 1.5, 101.3 | | | unmatched in claude |
| lpt89 | feature | -/13 | (none) | 2.1, 136.0 | | | unmatched in claude |
| lpt89 | feature | -/26 | (none) | 5.1, 377.4 | | | unmatched in claude |
| lpt98 | feature | 3/28 | 4.6, 467.6 (0.0, 0.8) | 4.4, 445.7 (0.0, 0.7) | +0.2 | +21.9 | **disagree** |
| lpt98 | feature | 5/37 | 5.0, 519.7 (0.0, 0.8) | 5.5, 568.7 (0.0, 0.5) | -0.5 | -49.0 | **disagree** |
| lpt98 | feature | 6/33 | 5.1, 520.7 (0.0, 0.8) | 5.1, 522.6 (0.0, 0.7) | -0.0 | -1.9 | **disagree** |
| lpt98 | feature | 7/34 | 5.1, 536.3 (0.0, 0.8) | 5.2, 535.3 (0.0, 0.7) | -0.0 | +1.0 | **disagree** |
| lpt98 | feature | -/3 | (none) | 0.1, 27.1 | | | unmatched in claude |
| lpt98 | feature | -/7 | (none) | 0.7, 122.8 | | | unmatched in claude |
| lpt98 | feature | -/11 | (none) | 1.4, 162.9 | | | unmatched in claude |
| lpt98 | feature | -/13 | (none) | 1.6, 179.5 | | | unmatched in claude |
| lpt98 | feature | -/21 | (none) | 3.3, 326.0 | | | unmatched in claude |
| lpt98 | feature | -/23 | (none) | 3.7, 365.0 | | | unmatched in claude |
| lpt98 | feature | -/26 | (none) | 4.2, 427.9 | | | unmatched in claude |
| lpt98 | feature | 8/- | 5.6, 575.2 | (none) | | | unmatched in codex |
