# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b3\rederived\claude\FA-23\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b3\rederived\codex\FA-23\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 473 | 110 |
| x per px | 0.0007 | 0.0007 |
| y per px | 0.0000 | 0.0000 |
| RMS residual x, y | 0.002, 0.000 | 0.002, 0.000 |

Corners of claude's box [815, 1440, 2265, 3752] mapped by both calibrations (tolerance 0.00 in x, 0.00 in y (in the plotting coordinates of linear x, reciprocal y)):

- (-0.0, 54.4) vs (-0.0, 54.4)
- (1.0, 54.6) vs (1.0, 54.6)
- (-0.0, 101.0) vs (-0.0, 100.9)
- (1.0, 101.6) vs (1.0, 101.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.27 | 0.41 | 0.30 | 25 | 0.95 | 0.55 | agree |
| x | 0.1 | 0.16 | 0.15 | 0.12 | 25 | 0.50 | 0.50 | agree |
| x | 0.2 | 0.15 | 0.26 | 0.21 | 25 | 0.65 | 0.50 | agree |
| x | 0.3 | 0.23 | 0.35 | 0.26 | 25 | 0.66 | 0.50 | agree |
| x | 0.4 | 0.09 | 0.31 | 0.25 | 25 | 0.59 | 0.60 | agree |
| x | 0.5 | 0.28 | 0.29 | 0.19 | 25 | 0.55 | 0.62 | agree |
| x | 0.6 | 0.30 | 0.30 | 0.21 | 25 | 0.59 | 0.50 | agree |
| x | 0.7 | 0.10 | 0.22 | 0.20 | 25 | 0.56 | 0.50 | agree |
| x | 0.8 | 0.13 | 0.18 | 0.19 | 25 | 0.56 | 0.50 | agree |
| x | 0.9 | 0.70 | 0.42 | 0.29 | 25 | 1.16 | 0.50 | agree |
| x | 1 | 0.13 | 0.37 | 0.34 | 25 | 0.89 | 0.76 | agree |
| y | 100 | | | | | | | claude's line not a knot: insufficient ink: found at 1 of 25 positions over 0% of the line's length |
| y | 100 | | | | | | | codex's line not a knot: insufficient ink: found at 2 of 25 positions over 2% of the line's length |
| y | 55 | 0.24 | 0.28 | 0.25 | 25 | 0.58 | 0.50 | agree |
| y | 60 | 0.04 | 0.37 | 0.37 | 25 | 0.73 | 0.74 | agree |
| y | 65 | 0.08 | 0.23 | 0.27 | 25 | 0.50 | 0.50 | agree |
| y | 70 | 0.24 | 0.52 | 0.54 | 25 | 0.71 | 0.72 | agree |
| y | 75 | 0.57 | 0.36 | 0.35 | 25 | 1.04 | 0.50 | agree |
| y | 80 | 0.10 | 0.36 | 0.37 | 25 | 0.69 | 0.60 | agree |
| y | 85 | 0.08 | 0.36 | 0.34 | 25 | 0.63 | 0.54 | agree |
| y | 90 | 0.21 | 0.45 | 0.35 | 25 | 0.71 | 0.73 | agree |
| y | 95 | 0.13 | 0.37 | 0.42 | 25 | 0.78 | 0.67 | agree |
| y | 56 | | | | | 0.81 | | only in claude |
| y | 57 | | | | | 0.87 | | only in claude |
| y | 58 | | | | | 1.02 | | only in claude |
| y | 59 | | | | | 0.83 | | only in claude |
| y | 61 | | | | | 0.55 | | only in claude |
| y | 62 | | | | | 0.75 | | only in claude |
| y | 63 | | | | | 0.69 | | only in claude |
| y | 64 | | | | | 0.69 | | only in claude |
| y | 66 | | | | | 0.72 | | only in claude |
| y | 67 | | | | | 0.85 | | only in claude |
| y | 68 | | | | | 0.70 | | only in claude |
| y | 69 | | | | | 0.50 | | only in claude |
| y | 71 | | | | | 0.96 | | only in claude |
| y | 72 | | | | | 0.77 | | only in claude |
| y | 73 | | | | | 0.62 | | only in claude |
| y | 74 | | | | | 0.74 | | only in claude |
| y | 76 | | | | | 0.91 | | only in claude |
| y | 77 | | | | | 0.65 | | only in claude |
| y | 78 | | | | | 0.85 | | only in claude |
| y | 79 | | | | | 0.80 | | only in claude |
| y | 81 | | | | | 0.75 | | only in claude |
| y | 82 | | | | | 0.68 | | only in claude |
| y | 83 | | | | | 0.82 | | only in claude |
| y | 84 | | | | | 0.63 | | only in claude |
| y | 86 | | | | | 0.82 | | only in claude |
| y | 87 | | | | | 0.81 | | only in claude |
| y | 88 | | | | | 0.82 | | only in claude |
| y | 89 | | | | | 1.06 | | only in claude |
| y | 91 | | | | | 0.86 | | only in claude |
| y | 92 | | | | | 1.01 | | only in claude |
| y | 93 | | | | | 1.14 | | only in claude |
| y | 94 | | | | | 0.77 | | only in claude |
| y | 96 | | | | | 0.61 | | only in claude |

(In the plotting coordinates: linear x, reciprocal y.) Both maps along every verified line and every interval midline (740 places): largest difference 0.0003889 in x (tolerance 0.001222, claude 0.9), 2.608e-05 in y (tolerance 6.562e-06, claude 88); 220 beyond the two maps' line errors.

Canonical reading: claude (claude's lines include all of codex's and more, as close to the ink; 20 shared lines checked against the ink, mean of the median distances 0.33 px (claude: x 0.30, y 0.37), 0.29 px (codex: x 0.23, y 0.36)); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 38; agreed 38; disagreed 0; unmatched 5 (kept as one-sided: 0 of claude, 5 of codex).

No point disagreements.

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
