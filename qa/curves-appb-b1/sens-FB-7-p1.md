# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appb-b1\rederived\claude\FB-7\points-p1-native.csv` (claude), `<repository>\qa\curves-appb-b1\rederived\codex\FB-7\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 59 | 685 |
| x per px | 0.0071 | 0.0071 |
| y per px | 0.0036 | 0.0036 |
| RMS residual x, y | 0.009, 0.006 | 0.010, 0.007 |

Corners of claude's box [470, 830, 2775, 3960] mapped by both calibrations (tolerance 0.03 in x, 0.02 in y):

- (-0.2, 11.1) vs (-0.2, 11.1)
- (16.3, 11.1) vs (16.3, 11.1)
- (-0.3, -0.1) vs (-0.3, -0.1)
- (16.2, -0.1) vs (16.2, -0.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.26 | 0.56 | 0.58 | 23 | 1.33 | 0.99 | agree |
| x | 2 | 0.03 | 0.16 | 0.15 | 11 | 0.50 | 0.50 | agree |
| x | 4 | 0.04 | 0.10 | 0.08 | 11 | 0.50 | 0.50 | agree |
| x | 6 | 0.09 | 0.06 | 0.14 | 11 | 0.50 | 0.50 | agree |
| x | 8 | 0.01 | 0.17 | 0.17 | 11 | 0.64 | 0.50 | agree |
| x | 10 | 0.02 | 0.07 | 0.08 | 11 | 0.50 | 0.50 | agree |
| x | 12 | 0.14 | 0.35 | 0.23 | 11 | 0.59 | 0.50 | agree |
| x | 14 | 0.02 | 0.08 | 0.08 | 11 | 0.50 | 0.50 | agree |
| x | 16 | 0.14 | 0.37 | 0.36 | 23 | 0.89 | 0.75 | agree |
| y | 1 | | | | | | | codex's line not a knot: insufficient ink: tick found at 0 of 0 stub positions |
| y | 2 | | | | | | | codex's line not a knot: insufficient ink: tick found at 0 of 0 stub positions |
| y | 0 | 0.06 | 0.31 | 0.33 | 23 | 0.73 | 0.54 | agree |
| y | 3 | 0.22 | 0.45 | 0.66 | 5 | 0.56 | 0.50 | agree |
| y | 4 | 0.13 | 0.04 | 0.14 | 11 | 0.95 | 0.50 | agree |
| y | 5 | 0.31 | 0.18 | 0.33 | 10 | 0.67 | 0.50 | agree |
| y | 6 | 0.11 | 0.06 | 0.07 | 11 | 0.50 | 0.50 | agree |
| y | 7 | 0.14 | 0.67 | 0.53 | 11 | 1.08 | 0.52 | agree |
| y | 8 | 0.06 | 0.15 | 0.15 | 10 | 0.50 | 0.50 | agree |
| y | 9 | 0.21 | 0.16 | 0.09 | 10 | 0.50 | 0.50 | agree |
| y | 10 | 0.37 | 0.29 | 0.14 | 11 | 0.63 | 0.50 | agree |
| y | 11 | 0.21 | 0.67 | 0.77 | 23 | 1.39 | 1.18 | agree |
| y | 1 | | | | | 1.11 | | only in claude |
| y | 2 | | | | | 1.71 | | only in claude |

Both maps along every verified line and every interval midline (426 places): largest difference 0.009053 in x (tolerance 0.007179, claude 2), 0.008539 in y (tolerance 0.008107, claude 2); 18 beyond the two maps' line errors.

Canonical reading: claude (claude's lines include all of codex's and more, as close to the ink; 19 shared lines checked against the ink, mean of the median distances 0.26 px (claude: x 0.21, y 0.30), 0.27 px (codex: x 0.21, y 0.32)); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 55; agreed 50; disagreed 5; unmatched 3 (kept as one-sided: 1 of claude, 2 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| dr104 | marker | 8/8 | 9.3, 7.5 (0.0, 0.0) | 9.3, 7.5 (0.0, 0.0) | -0.0 | +0.0 | **disagree** |
| dr77 | marker | 1/3 | -0.0, 1.6 (0.0, 0.0) | -0.0, 1.6 (0.0, 0.0) | -0.0 | -0.0 | **disagree** |
| dr77 | marker | 3/2 | -0.0, 1.6 (0.0, 0.0) | -0.0, 1.7 (0.0, 0.0) | -0.0 | -0.0 | **disagree** |
| dr77 | marker | 5/5 | 2.0, 5.9 (0.0, 0.0) | 2.0, 5.9 (0.0, 0.0) | -0.0 | +0.0 | **disagree** |
| dr77 | trace | 1/- | -0.0, 0.9 (0.0, 0.0) | (no trace at this x) | | | unmatched in codex |
| dr99p5 | marker | 7/7 | 10.3, 8.1 (0.0, 0.0) | 10.3, 8.1 (0.0, 0.0) | -0.0 | -0.0 | **disagree** |
