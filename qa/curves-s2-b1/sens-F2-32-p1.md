# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b1\rederived\claude\F2-32\points-p1-native.csv` (claude), `<repository>\qa\curves-s2-b1\rederived\codex\F2-32\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 96 | 80 |
| x per px | 0.0048 | 0.0048 |
| y per px | 0.0484 | 0.0484 |
| RMS residual x, y | 0.009, 0.079 | 0.010, 0.074 |

Corners of claude's box [520, 1395, 2010, 3710] mapped by both calibrations (tolerance 0.02 in x, 0.20 in y):

- (11.1, 71.1) vs (11.1, 71.0)
- (11.1, -1.1) vs (11.1, -1.1)
- (-0.1, 71.2) vs (-0.1, 71.2)
- (-0.1, -0.9) vs (-0.1, -0.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.19 | 0.47 | 0.41 | 21 | 1.08 | 1.13 | agree |
| x | 1 | 0.11 | 0.53 | 0.44 | 21 | 0.95 | 0.95 | agree |
| x | 2 | 0.57 | 0.36 | 0.26 | 23 | 1.31 | 0.50 | agree |
| x | 3 | 0.17 | 0.16 | 0.18 | 21 | 0.98 | 0.81 | agree |
| x | 4 | 0.23 | 0.40 | 0.32 | 19 | 0.96 | 0.74 | agree |
| x | 5 | 0.21 | 0.38 | 0.43 | 20 | 1.29 | 1.42 | agree |
| x | 6 | 0.31 | 0.36 | 0.30 | 21 | 0.76 | 0.61 | agree |
| x | 7 | 0.30 | 0.30 | 0.42 | 21 | 0.89 | 0.88 | agree |
| x | 8 | 0.04 | 0.40 | 0.41 | 21 | 0.78 | 0.72 | agree |
| x | 9 | 0.72 | 0.94 | 0.84 | 11 | 1.28 | 0.92 | agree |
| x | 10 | | | | | 0.72 | | only in claude |
| x | 11 | | | | | 0.87 | | only in claude |
| y | 0 | 0.56 | 0.37 | 0.35 | 20 | 0.66 | 0.54 | agree |
| y | 10 | 0.54 | 0.33 | 0.35 | 20 | 0.55 | 0.50 | agree |
| y | 20 | 0.59 | 0.32 | 0.30 | 20 | 0.70 | 0.61 | agree |
| y | 30 | 1.10 | 0.76 | 0.51 | 20 | 1.02 | 0.72 | agree |
| y | 40 | 0.57 | 0.48 | 0.35 | 19 | 2.42 | 0.50 | agree |
| y | 50 | 1.98 | 1.02 | 0.27 | 20 | 2.32 | 0.62 | agree; claude off the ink |
| y | 60 | 0.32 | 0.42 | 0.29 | 20 | 0.50 | 0.64 | agree |
| y | 70 | 0.43 | 0.44 | 0.51 | 20 | 0.60 | 0.67 | agree |

Both maps along every verified line and every interval midline (452 places): largest difference 0.01896 in x (tolerance 0.008645, claude 11), 0.1429 in y (tolerance 0.1482, claude 50); 10 beyond the two maps' line errors.

Canonical reading: claude (claude's lines include all of codex's and more, as close to the ink; 18 shared lines checked against the ink, mean of the median distances 0.47 px (claude: x 0.43, y 0.52), 0.39 px (codex: x 0.40, y 0.37)); points are evaluated at claude's samples.

## Series

4 series in claude, 4 in codex.


## Points

Matched: 97; agreed 88; disagreed 9; unmatched 12 (kept as one-sided: 5 of claude, 7 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| fit | trace | 3/interp | 7.0, 49.7 (0.0, 0.2) | 7.0, 48.9 (0.0, 0.2) | slope +5.5 | +0.8 (tol 0.5) | **disagree** |
| lpt52 | feature | 3/- | 1.2, 6.8 | (none) | | | unmatched in codex |
| lpt52 | feature | 4/5 | 1.5, 13.9 (0.0, 0.2) | 1.5, 14.3 (0.0, 0.1) | -0.0 | -0.3 | **disagree** |
| lpt52 | trace | 13/interp | 3.3, 25.9 (0.0, 0.1) | 3.3, 25.4 (0.0, 0.2) | slope +6.0 | +0.5 (tol 0.5) | **disagree** |
| lpt52 | trace | 14/interp | 3.5, 27.4 (0.0, 0.1) | 3.5, 26.9 (0.0, 0.2) | slope +5.9 | +0.5 (tol 0.5) | **disagree** |
| lpt52 | trace | 15/interp | 3.8, 28.9 (0.0, 0.1) | 3.8, 28.3 (0.0, 0.2) | slope +8.3 | +0.6 (tol 0.5) | **disagree** |
| lpt52 | trace | 29/- | 7.1, 49.7 (0.0, 0.1) | (no trace at this x) | | | unmatched in codex |
| lpt53 | feature | 1/1 | 2.0, 2.5 (0.0, 1.1) | 2.0, 0.0 (0.0, 0.1) | +0.0 | +2.5 | **disagree** |
| lpt53 | feature | 3/4 | 2.0, 4.4 (0.0, 0.2) | 2.3, 14.5 (0.0, 0.1) | -0.3 | -10.1 | **disagree** |
| lpt53 | feature | -/7 | (none) | 2.8, 21.4 | | | unmatched in claude |
| lpt53 | trace | 24/- | 7.1, 48.9 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| lpt93 | feature | 3/- | 0.2, 4.3 | (none) | | | unmatched in codex |
| lpt93 | feature | 1/1 | 0.0, 1.2 (0.0, 0.4) | -0.0, 0.6 (0.0, 0.1) | +0.1 | +0.6 | **disagree** |
| lpt93 | feature | -/4 | (none) | 0.3, 6.3 | | | unmatched in claude |
| lpt93 | feature | -/8 | (none) | 1.2, 14.0 | | | unmatched in claude |
| lpt93 | trace | 5/interp | 0.5, 8.1 (0.0, 0.1) | 0.5, 7.5 (0.0, 0.2) | slope +7.0 | +0.6 (tol 0.5) | **disagree** |
| lpt93 | trace | 31/- | 6.8, 52.2 (0.0, 0.1) | (no trace at this x) | | | unmatched in codex |
