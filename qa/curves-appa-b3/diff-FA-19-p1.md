# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b3\rederived\claude\FA-19\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b3\rederived\codex\FA-19\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 638 | 143 |
| x per px | 0.0006 | 0.0006 |
| y per px | 0.0000 | 0.0000 |
| RMS residual x, y | 0.001, 0.000 | 0.001, 0.000 |

Corners of claude's box [738, 790, 2340, 3775] mapped by both calibrations (tolerance 0.00 in x, 0.00 in y (in the plotting coordinates of linear x, reciprocal y)):

- (-0.0, 54.5) vs (-0.0, 54.5)
- (1.0, 54.7) vs (1.0, 54.7)
- (-0.0, 116.5) vs (-0.0, 116.4)
- (1.0, 117.4) vs (1.0, 117.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.22 | 0.62 | 0.56 | 25 | 1.41 | 0.77 | agree |
| x | 0.1 | 0.36 | 0.39 | 0.34 | 25 | 1.18 | 0.67 | agree |
| x | 0.2 | 0.59 | 0.66 | 0.41 | 25 | 1.39 | 0.77 | agree |
| x | 0.3 | 0.41 | 0.70 | 0.68 | 25 | 1.37 | 0.84 | agree |
| x | 0.4 | 0.79 | 0.66 | 0.47 | 25 | 1.74 | 0.81 | agree |
| x | 0.5 | 0.17 | 0.42 | 0.41 | 25 | 1.05 | 0.81 | agree |
| x | 0.6 | 0.33 | 0.55 | 0.45 | 25 | 1.18 | 0.70 | agree |
| x | 0.7 | 0.08 | 0.28 | 0.31 | 25 | 0.50 | 0.50 | agree |
| x | 0.8 | 0.32 | 0.38 | 0.23 | 25 | 0.83 | 0.59 | agree |
| x | 0.9 | 0.09 | 0.19 | 0.25 | 25 | 0.55 | 0.50 | agree |
| x | 1 | 0.80 | 0.66 | 0.28 | 25 | 1.61 | 0.82 | agree |
| y | 115 | | | | | | | claude's line not a knot: insufficient ink: found at 0 of 25 positions over 0% of the line's length |
| y | 115 | | | | | | | codex's line not a knot: insufficient ink: found at 1 of 25 positions over 0% of the line's length |
| y | 55 | 0.16 | 0.29 | 0.27 | 25 | 0.62 | 0.50 | agree |
| y | 60 | 0.56 | 0.46 | 0.42 | 25 | 1.19 | 0.66 | agree |
| y | 65 | 0.04 | 0.35 | 0.38 | 25 | 0.69 | 0.71 | agree |
| y | 70 | 0.31 | 0.31 | 0.26 | 25 | 0.66 | 0.53 | agree |
| y | 75 | 0.53 | 0.35 | 0.22 | 25 | 0.88 | 0.50 | agree |
| y | 80 | 0.26 | 0.28 | 0.23 | 25 | 0.57 | 0.50 | agree |
| y | 85 | 0.23 | 0.27 | 0.25 | 25 | 0.56 | 0.50 | agree |
| y | 90 | 0.52 | 0.26 | 0.30 | 25 | 0.61 | 0.67 | agree |
| y | 95 | 0.11 | 0.30 | 0.30 | 25 | 0.50 | 0.52 | agree |
| y | 100 | 0.47 | 0.48 | 0.31 | 25 | 1.06 | 0.56 | agree |
| y | 105 | 0.22 | 0.45 | 0.44 | 25 | 0.98 | 0.73 | agree |
| y | 110 | 0.35 | 0.38 | 0.25 | 25 | 0.79 | 0.50 | agree |
| y | 56 | | | | | 0.50 | | only in claude |
| y | 57 | | | | | 0.92 | | only in claude |
| y | 58 | | | | | 0.96 | | only in claude |
| y | 59 | | | | | 0.91 | | only in claude |
| y | 61 | | | | | 0.59 | | only in claude |
| y | 62 | | | | | 0.50 | | only in claude |
| y | 63 | | | | | 0.52 | | only in claude |
| y | 64 | | | | | 0.85 | | only in claude |
| y | 66 | | | | | 0.87 | | only in claude |
| y | 67 | | | | | 0.67 | | only in claude |
| y | 68 | | | | | 0.68 | | only in claude |
| y | 69 | | | | | 0.68 | | only in claude |
| y | 71 | | | | | 0.91 | | only in claude |
| y | 72 | | | | | 0.96 | | only in claude |
| y | 73 | | | | | 1.07 | | only in claude |
| y | 74 | | | | | 1.06 | | only in claude |
| y | 76 | | | | | 0.92 | | only in claude |
| y | 77 | | | | | 0.96 | | only in claude |
| y | 78 | | | | | 0.64 | | only in claude |
| y | 79 | | | | | 0.66 | | only in claude |
| y | 81 | | | | | 0.78 | | only in claude |
| y | 82 | | | | | 0.93 | | only in claude |
| y | 83 | | | | | 0.65 | | only in claude |
| y | 84 | | | | | 0.59 | | only in claude |
| y | 86 | | | | | 1.27 | | only in claude |
| y | 87 | | | | | 0.67 | | only in claude |
| y | 88 | | | | | 0.84 | | only in claude |
| y | 89 | | | | | 0.69 | | only in claude |
| y | 91 | | | | | 0.93 | | only in claude |
| y | 92 | | | | | 0.57 | | only in claude |
| y | 93 | | | | | 0.65 | | only in claude |
| y | 94 | | | | | 0.63 | | only in claude |
| y | 96 | | | | | 1.01 | | only in claude |
| y | 97 | | | | | 1.02 | | only in claude |
| y | 98 | | | | | 0.63 | | only in claude |
| y | 99 | | | | | 0.87 | | only in claude |
| y | 101 | | | | | 1.05 | | only in claude |
| y | 102 | | | | | 0.67 | | only in claude |
| y | 103 | | | | | 0.76 | | only in claude |
| y | 104 | | | | | 0.70 | | only in claude |
| y | 106 | | | | | 0.60 | | only in claude |
| y | 107 | | | | | 0.63 | | only in claude |
| y | 108 | | | | | 0.60 | | only in claude |
| y | 109 | | | | | 0.82 | | only in claude |
| y | 111 | | | | | 0.85 | | only in claude |

(In the plotting coordinates: linear x, reciprocal y.) Both maps along every verified line and every interval midline (918 places): largest difference 0.0005593 in x (tolerance 0.001605, codex 1), 2.512e-05 in y (tolerance 3.964e-06, claude 56); 255 beyond the two maps' line errors.

Canonical reading: claude (claude's lines include all of codex's and more, as close to the ink; 23 shared lines checked against the ink, mean of the median distances 0.42 px (claude: x 0.50, y 0.35), 0.35 px (codex: x 0.40, y 0.30)); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 38; agreed 38; disagreed 0; unmatched 3 (kept as one-sided: 0 of claude, 3 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
