# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b3\rederived\claude\FA-3\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b3\rederived\codex\FA-3\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 418 | 99 |
| x per px | 0.0007 | 0.0007 |
| y per px | 0.0000 | 0.0000 |
| RMS residual x, y | 0.001, 0.000 | 0.001, 0.000 |

Corners of claude's box [875, 1835, 2458, 3388] mapped by both calibrations (tolerance 0.00 in x, 0.00 in y (in the plotting coordinates of linear x, reciprocal y)):

- (-0.0, 24.7) vs (-0.0, 24.7)
- (1.0, 24.7) vs (1.0, 24.8)
- (-0.0, 66.4) vs (-0.0, 66.2)
- (1.0, 66.9) vs (1.0, 66.7)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.33 | 0.90 | 0.72 | 25 | 1.38 | 1.98 | agree |
| x | 0.1 | 0.24 | 0.77 | 0.78 | 25 | 1.63 | 1.32 | agree |
| x | 0.2 | 0.23 | 0.57 | 0.52 | 25 | 1.12 | 1.21 | agree |
| x | 0.3 | 0.30 | 0.61 | 0.55 | 25 | 1.46 | 1.22 | agree |
| x | 0.4 | 0.59 | 0.58 | 0.50 | 25 | 1.05 | 1.01 | agree |
| x | 0.5 | 0.33 | 0.58 | 0.49 | 25 | 1.46 | 1.66 | agree |
| x | 0.6 | 0.14 | 0.43 | 0.37 | 25 | 0.67 | 1.13 | agree |
| x | 0.7 | 0.06 | 0.58 | 0.58 | 25 | 1.27 | 0.99 | agree |
| x | 0.8 | 0.34 | 0.47 | 0.48 | 25 | 1.10 | 1.10 | agree |
| x | 0.9 | 0.04 | 0.39 | 0.38 | 25 | 0.71 | 0.75 | agree |
| x | 1 | 0.15 | 0.35 | 0.38 | 25 | 1.34 | 0.83 | agree |
| y | 25 | 0.10 | 0.23 | 0.21 | 25 | 0.50 | 0.50 | agree |
| y | 30 | 0.22 | 0.27 | 0.23 | 25 | 0.74 | 0.56 | agree |
| y | 35 | 0.05 | 0.18 | 0.17 | 25 | 0.50 | 0.50 | agree |
| y | 40 | 0.20 | 0.25 | 0.20 | 25 | 0.66 | 0.50 | agree |
| y | 45 | 0.24 | 0.36 | 0.39 | 25 | 0.77 | 0.73 | agree |
| y | 50 | 0.33 | 0.47 | 0.47 | 25 | 0.65 | 0.96 | agree |
| y | 55 | 0.33 | 0.30 | 0.28 | 25 | 0.73 | 0.50 | agree |
| y | 60 | 0.19 | 0.26 | 0.27 | 25 | 0.50 | 0.50 | agree |
| y | 65 | 0.07 | 0.33 | 0.29 | 25 | 0.50 | 0.50 | agree |
| y | 26 | | | | | 0.58 | | only in claude |
| y | 27 | | | | | 0.50 | | only in claude |
| y | 28 | | | | | 0.50 | | only in claude |
| y | 29 | | | | | 0.78 | | only in claude |
| y | 31 | | | | | 0.73 | | only in claude |
| y | 32 | | | | | 0.50 | | only in claude |
| y | 33 | | | | | 0.50 | | only in claude |
| y | 34 | | | | | 0.50 | | only in claude |
| y | 36 | | | | | 0.82 | | only in claude |
| y | 37 | | | | | 0.64 | | only in claude |
| y | 38 | | | | | 0.87 | | only in claude |
| y | 39 | | | | | 0.80 | | only in claude |
| y | 41 | | | | | 0.62 | | only in claude |
| y | 42 | | | | | 0.54 | | only in claude |
| y | 43 | | | | | 0.91 | | only in claude |
| y | 44 | | | | | 0.50 | | only in claude |
| y | 46 | | | | | 0.69 | | only in claude |
| y | 47 | | | | | 0.55 | | only in claude |
| y | 48 | | | | | 0.77 | | only in claude |
| y | 49 | | | | | 1.14 | | only in claude |
| y | 51 | | | | | 1.36 | | only in claude |
| y | 52 | | | | | 1.20 | | only in claude |
| y | 53 | | | | | 1.01 | | only in claude |
| y | 54 | | | | | 0.84 | | only in claude |
| y | 56 | | | | | 0.56 | | only in claude |
| y | 57 | | | | | 0.62 | | only in claude |
| y | 58 | | | | | 0.75 | | only in claude |
| y | 59 | | | | | 0.68 | | only in claude |
| y | 61 | | | | | 0.55 | | only in claude |

(In the plotting coordinates: linear x, reciprocal y.) Both maps along every verified line and every interval midline (759 places): largest difference 0.0002962 in x (tolerance 0.002069, claude 0.4), 0.0001076 in y (tolerance 2.831e-05, claude 47); 203 beyond the two maps' line errors.

Canonical reading: claude (claude's lines include all of codex's and more, as close to the ink; 20 shared lines checked against the ink, mean of the median distances 0.44 px (claude: x 0.57, y 0.29), 0.41 px (codex: x 0.52, y 0.28)); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 45; agreed 41; disagreed 4; unmatched 0 (kept as one-sided: 0 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| lower | feature | 1/1 | 0.0, 42.6 (0.0, 0.1) | 0.0, 42.5 (0.0, 0.1) | -0.0 | +0.2 | **disagree** |
| mean | feature | 2/2 | 1.0, 52.8 (0.0, 0.1) | 1.0, 53.0 (0.0, 0.1) | +0.0 | -0.2 | **disagree** |
| mean | trace | 6/interp | 0.5, 46.6 (0.0, 0.1) | 0.5, 46.4 (0.0, 0.1) | slope +11.3 | +0.2 (tol 0.2) | **disagree** |
| upper | trace | 7/interp | 0.6, 46.4 (0.0, 0.1) | 0.6, 46.2 (0.0, 0.1) | slope +12.7 | +0.2 (tol 0.2) | **disagree** |
