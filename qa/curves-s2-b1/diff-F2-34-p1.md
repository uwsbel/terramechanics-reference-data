# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b1\rederived\claude\F2-34\points-p1-native.csv` (claude), `<repository>\qa\curves-s2-b1\rederived\codex\F2-34\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 70 | 49 |
| x per px | 0.0038 | 0.0038 |
| y per px | 0.7640 | 0.7619 |
| RMS residual x, y | 0.012, 2.009 | 0.009, 1.481 |

Corners of claude's box [600, 1280, 2280, 3700] mapped by both calibrations (tolerance 0.03 in x, 4.25 in y):

- (9.1, 1225.8) vs (9.1, 1223.2)
- (9.1, -57.6) vs (9.1, -56.7)
- (-0.1, 1240.8) vs (-0.1, 1238.2)
- (-0.2, -42.6) vs (-0.2, -41.7)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.52 | 0.33 | 0.30 | 18 | 0.68 | 0.72 | agree |
| x | 1 | 0.39 | 0.46 | 0.35 | 18 | 1.08 | 0.71 | agree |
| x | 2 | 0.09 | 0.32 | 0.29 | 18 | 0.64 | 0.55 | agree |
| x | 3 | 0.35 | 0.60 | 0.46 | 18 | 1.06 | 0.74 | agree |
| x | 4 | 0.21 | 0.68 | 0.52 | 18 | 1.74 | 1.78 | agree |
| x | 5 | 0.21 | 0.44 | 0.38 | 18 | 0.91 | 0.75 | agree |
| x | 6 | 1.33 | 0.34 | 0.79 | 18 | 0.72 | 2.12 | agree |
| x | 7 | | | | | 1.10 | | only in claude |
| x | 8 | | | | | 0.80 | | only in claude |
| x | 9 | | | | | 2.65 | | only in claude |
| y | 0 | 0.65 | 0.41 | 0.22 | 17 | 1.59 | 0.50 | agree |
| y | 200 | 0.57 | 0.56 | 0.48 | 17 | 1.43 | 1.08 | agree |
| y | 400 | 0.34 | 0.42 | 0.33 | 17 | 0.79 | 0.59 | agree |
| y | 600 | 0.27 | 0.40 | 0.39 | 17 | 0.69 | 0.60 | agree |
| y | 800 | 0.48 | 0.25 | 0.28 | 17 | 0.93 | 0.53 | agree |
| y | 1000 | 0.59 | 0.36 | 0.28 | 18 | 0.83 | 0.50 | agree |
| y | 1200 | 0.11 | 0.29 | 0.28 | 17 | 0.50 | 0.54 | agree |

Both maps along every verified line and every interval midline (318 places): largest difference 0.08161 in x (tolerance 0.01839, claude 9), 0.8071 in y (tolerance 2.031, claude 0); 26 beyond the two maps' line errors.

Canonical reading: claude (claude's lines include all of codex's and more, as close to the ink; 14 shared lines checked against the ink, mean of the median distances 0.42 px (claude: x 0.45, y 0.38), 0.38 px (codex: x 0.44, y 0.32)); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 70; agreed 63; disagreed 7; unmatched 4 (kept as one-sided: 1 of claude, 3 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| fit | feature | 1/2 | -0.0, 139.1 (0.0, 4.2) | 0.0, 127.5 (0.0, 4.5) | -0.0 | +11.6 | **disagree** |
| fit | trace | 1/- | 0.0, 140.2 (0.0, 4.2) | (no trace at this x) | | | unmatched in codex |
| lpt87 | feature | 3/11 | 1.3, 173.0 (0.2, 7.5) | 1.6, 191.2 (0.0, 3.3) | -0.3 | -18.2 | **disagree** |
| lpt87 | trace | 8/interp | 1.7, 202.8 (0.0, 4.9) | 1.7, 227.9 (0.0, 3.9) | slope +181.6 | -25.1 (tol 16.0) | **disagree** |
| lpt87 | trace | 9/interp | 2.0, 227.1 (0.0, 4.1) | 2.0, 241.4 (0.0, 4.6) | slope +52.2 | -14.3 (tol 10.8) | **disagree** |
| lpt87 | trace | 20/interp | 4.8, 513.9 (0.0, 4.5) | 4.8, 529.9 (0.0, 4.4) | slope +52.8 | -16.0 (tol 11.2) | **disagree** |
| lpt88 | feature | 1/1 | 2.0, 7.3 (0.0, 7.3) | 2.0, 53.3 (0.0, 4.4) | -0.0 | -46.0 | **disagree** |
| lpt88 | feature | -/12 | (none) | 3.5, 312.0 | | | unmatched in claude |
| lpt88 | trace | 1/interp | 2.0, 7.3 (0.0, 7.3) | 2.0, 53.3 (0.0, 4.4) | slope +829.5 | -46.0 (tol 41.3) | **disagree** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
