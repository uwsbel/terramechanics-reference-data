# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b3\rederived\claude\FA-7\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b3\rederived\codex\FA-7\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 440 | 99 |
| x per px | 0.0007 | 0.0007 |
| y per px | 0.0000 | 0.0000 |
| RMS residual x, y | 0.001, 0.000 | 0.001, 0.000 |

Corners of claude's box [600, 1710, 2200, 3520] mapped by both calibrations (tolerance 0.00 in x, 0.00 in y (in the plotting coordinates of linear x, reciprocal y)):

- (-0.0, 22.5) vs (-0.0, 22.5)
- (1.0, 22.3) vs (1.0, 22.3)
- (-0.0, 67.7) vs (-0.0, 67.6)
- (1.0, 66.1) vs (1.0, 66.0)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.71 | 0.97 | 0.80 | 23 | 1.83 | 1.81 | agree |
| x | 0.1 | 0.22 | 0.54 | 0.50 | 23 | 0.91 | 1.04 | agree |
| x | 0.2 | 0.05 | 0.43 | 0.40 | 23 | 0.89 | 1.12 | agree |
| x | 0.3 | 0.16 | 0.42 | 0.39 | 23 | 1.26 | 1.37 | agree |
| x | 0.4 | 0.32 | 0.62 | 0.53 | 23 | 0.83 | 1.16 | agree |
| x | 0.5 | 0.25 | 0.52 | 0.62 | 23 | 1.69 | 1.49 | agree |
| x | 0.6 | 0.47 | 0.75 | 0.58 | 23 | 1.20 | 1.45 | agree |
| x | 0.7 | 0.39 | 0.57 | 0.49 | 23 | 1.59 | 1.18 | agree |
| x | 0.8 | 0.38 | 0.67 | 0.48 | 23 | 1.41 | 1.30 | agree |
| x | 0.9 | 0.17 | 0.47 | 0.37 | 23 | 0.88 | 0.90 | agree |
| x | 1 | 0.35 | 0.51 | 0.48 | 23 | 1.49 | 1.46 | agree |
| y | 25 | 0.34 | 0.47 | 0.43 | 25 | 0.88 | 0.79 | agree |
| y | 30 | 0.22 | 0.49 | 0.44 | 25 | 0.94 | 0.68 | agree |
| y | 35 | 0.20 | 0.39 | 0.38 | 25 | 0.85 | 0.64 | agree |
| y | 40 | 0.46 | 0.42 | 0.29 | 25 | 0.99 | 0.52 | agree |
| y | 45 | 0.49 | 0.44 | 0.40 | 25 | 1.04 | 0.53 | agree |
| y | 50 | 0.39 | 0.40 | 0.41 | 25 | 0.79 | 0.61 | agree |
| y | 55 | 0.14 | 0.20 | 0.24 | 25 | 0.52 | 0.50 | agree |
| y | 60 | 0.13 | 0.42 | 0.41 | 25 | 0.53 | 0.61 | agree |
| y | 65 | 0.28 | 0.23 | 0.26 | 25 | 0.55 | 0.50 | agree |
| y | 23 | | | | | 0.73 | | only in claude |
| y | 24 | | | | | 1.43 | | only in claude |
| y | 26 | | | | | 0.50 | | only in claude |
| y | 27 | | | | | 0.67 | | only in claude |
| y | 28 | | | | | 0.83 | | only in claude |
| y | 29 | | | | | 1.36 | | only in claude |
| y | 31 | | | | | 1.17 | | only in claude |
| y | 32 | | | | | 0.67 | | only in claude |
| y | 33 | | | | | 0.58 | | only in claude |
| y | 34 | | | | | 0.98 | | only in claude |
| y | 36 | | | | | 0.72 | | only in claude |
| y | 37 | | | | | 0.63 | | only in claude |
| y | 38 | | | | | 1.32 | | only in claude |
| y | 39 | | | | | 0.52 | | only in claude |
| y | 41 | | | | | 0.74 | | only in claude |
| y | 42 | | | | | 0.92 | | only in claude |
| y | 43 | | | | | 0.67 | | only in claude |
| y | 44 | | | | | 0.87 | | only in claude |
| y | 46 | | | | | 0.95 | | only in claude |
| y | 47 | | | | | 1.24 | | only in claude |
| y | 48 | | | | | 0.62 | | only in claude |
| y | 49 | | | | | 0.80 | | only in claude |
| y | 51 | | | | | 0.75 | | only in claude |
| y | 52 | | | | | 0.85 | | only in claude |
| y | 53 | | | | | 0.72 | | only in claude |
| y | 54 | | | | | 0.68 | | only in claude |
| y | 56 | | | | | 0.77 | | only in claude |
| y | 57 | | | | | 0.50 | | only in claude |
| y | 58 | | | | | 0.98 | | only in claude |
| y | 59 | | | | | 0.81 | | only in claude |
| y | 61 | | | | | 0.96 | | only in claude |

(In the plotting coordinates: linear x, reciprocal y.) Both maps along every verified line and every interval midline (725 places): largest difference 0.0005345 in x (tolerance 0.002358, codex 0), 0.0001125 in y (tolerance 2.896e-05, claude 47); 182 beyond the two maps' line errors.

Canonical reading: claude (claude's lines include all of codex's and more, as close to the ink; 20 shared lines checked against the ink, mean of the median distances 0.50 px (claude: x 0.59, y 0.38), 0.45 px (codex: x 0.51, y 0.36)); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 45; agreed 43; disagreed 2; unmatched 1 (kept as one-sided: 0 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| lower | feature | 1/1 | -0.0, 24.3 (0.0, 0.0) | 0.0, 24.4 (0.0, 0.0) | -0.0 | -0.1 | **disagree** |
| upper | feature | 1/1 | 0.0, 23.2 (0.0, 0.0) | 0.0, 23.2 (0.0, 0.0) | -0.0 | -0.1 | **disagree** |
