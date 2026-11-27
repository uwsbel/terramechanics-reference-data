# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s4-b1\rederived\claude\F4-19\points-p2-native.csv` (claude), `<repository>\qa\curves-s4-b1\rederived\codex\F4-19\points-p2-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 99 | 150 |
| x per px | 0.0819 | 0.0820 |
| y per px | 0.0041 | 0.0041 |
| RMS residual x, y | 0.078, 0.004 | 0.114, 0.006 |

Corners of claude's box [715, 2150, 2470, 3290] mapped by both calibrations (tolerance 0.27 in x, 0.01 in y):

- (-1.7, 4.6) vs (-1.8, 4.6)
- (142.1, 4.6) vs (142.2, 4.6)
- (-2.7, -0.1) vs (-2.7, -0.1)
- (141.0, -0.1) vs (141.2, -0.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.06 | 0.33 | 0.34 | 22 | 0.50 | 0.50 | agree |
| x | 10 | 0.12 | 0.26 | 0.23 | 22 | 0.50 | 0.50 | agree |
| x | 20 | 0.09 | 0.20 | 0.22 | 22 | 0.50 | 0.50 | agree |
| x | 30 | 0.08 | 0.27 | 0.28 | 22 | 0.50 | 0.50 | agree |
| x | 40 | 0.07 | 0.27 | 0.26 | 22 | 0.50 | 0.54 | agree |
| x | 50 | 0.04 | 0.31 | 0.29 | 22 | 0.50 | 0.50 | agree |
| x | 60 | 0.01 | 0.25 | 0.25 | 22 | 0.56 | 0.50 | agree |
| x | 70 | 0.05 | 0.26 | 0.25 | 22 | 0.50 | 0.50 | agree |
| x | 80 | 0.07 | 0.34 | 0.33 | 22 | 0.50 | 0.56 | agree |
| x | 90 | 0.01 | 0.31 | 0.31 | 22 | 0.50 | 0.50 | agree |
| x | 100 | 0.18 | 0.32 | 0.30 | 22 | 0.63 | 0.50 | agree |
| x | 110 | 0.15 | 0.17 | 0.17 | 23 | 0.50 | 0.50 | agree |
| x | 120 | 0.27 | 0.24 | 0.28 | 23 | 0.50 | 0.50 | agree |
| x | 130 | 0.15 | 0.14 | 0.15 | 23 | 0.50 | 0.50 | agree |
| x | 140 | 0.18 | 0.30 | 0.27 | 23 | 0.50 | 0.50 | agree |
| y | 0 | 0.08 | 0.40 | 0.38 | 18 | 0.72 | 0.57 | agree |
| y | 0.5 | 0.04 | 0.35 | 0.35 | 18 | 0.73 | 0.81 | agree |
| y | 1 | 0.09 | 0.36 | 0.36 | 18 | 0.82 | 1.13 | agree |
| y | 1.5 | 0.05 | 0.26 | 0.24 | 18 | 0.64 | 0.58 | agree |
| y | 2 | 0.17 | 0.44 | 0.50 | 18 | 0.92 | 1.01 | agree |
| y | 2.5 | 0.04 | 0.40 | 0.41 | 18 | 0.59 | 0.61 | agree |
| y | 3 | 0.04 | 0.29 | 0.28 | 18 | 0.88 | 0.51 | agree |
| y | 3.5 | 0.04 | 0.53 | 0.51 | 18 | 1.03 | 0.63 | agree |
| y | 4 | 0.02 | 0.38 | 0.39 | 18 | 0.77 | 0.53 | agree |
| y | 4.5 | | | | | | 0.97 | only in codex |

Both maps along every verified line and every interval midline (512 places): largest difference 0.02251 in x (tolerance 0.08297, claude 120), 0.02285 in y (tolerance 0.008123, codex 4.5); 6 beyond the two maps' line errors.

Canonical reading: claude (named by the batch: Codex's extra line, 4.5 in, is the panel's top frame, which tilts -0.0063 against about +0.0006 for the grid lines (about 5 px, 0.02 in, at the panel's ends); Claude left the frame out and extrapolates the even 3.5 to 4.0 in spacing. Only run 4's displacement above 4.0 in uses that interval; codex's lines include all of claude's and more, as close to the ink; 24 shared lines checked against the ink, mean of the median distances 0.31 px (claude: x 0.26, y 0.38), 0.31 px (codex: x 0.26, y 0.38)); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 112; agreed 111; disagreed 1; unmatched 17 (kept as one-sided: 0 of claude, 17 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| run12 | feature | 1/1 | 9.0, 0.6 (0.5, 0.0) | 0.3, 0.2 (1.4, 0.1) | +8.7 | +0.4 | **disagree** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
