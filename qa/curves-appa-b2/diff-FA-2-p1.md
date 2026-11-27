# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b2\rederived\claude\FA-2\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b2\rederived\codex\FA-2\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 112 | 995 |
| x per px | 0.0010 | 0.0010 |
| y per px | 0.0686 | 0.0686 |
| RMS residual x, y | 0.003, 0.070 | 0.003, 0.075 |

Corners of claude's box [675, 1123, 2195, 3735] mapped by both calibrations (tolerance 0.01 in x, 0.21 in y (in the plotting coordinates of log10 x, linear y)):

- (9.5, 100.9) vs (9.5, 100.9)
- (9.2, -3.3) vs (9.3, -3.3)
- (0.0, 102.8) vs (0.0, 102.7)
- (0.0, -1.4) vs (0.0, -1.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0.02 | 0.25 | 0.57 | 0.59 | 24 | 0.84 | 0.65 | agree |
| x | 0.05 | 0.16 | 0.38 | 0.36 | 22 | 0.66 | 0.62 | agree |
| x | 0.1 | 0.07 | 0.45 | 0.41 | 22 | 0.80 | 0.82 | agree |
| x | 0.2 | 0.14 | 0.26 | 0.24 | 22 | 0.72 | 0.63 | agree |
| x | 0.5 | 0.16 | 0.36 | 0.36 | 22 | 1.06 | 1.00 | agree |
| x | 1 | 0.28 | 0.56 | 0.50 | 23 | 0.75 | 0.89 | agree |
| x | 1.5 | 0.05 | 0.38 | 0.37 | 23 | 0.97 | 0.79 | agree |
| x | 2 | 0.27 | 0.50 | 0.56 | 22 | 0.82 | 0.73 | agree |
| x | 3 | 0.18 | 0.39 | 0.31 | 23 | 1.07 | 1.26 | agree |
| x | 4 | 0.16 | 0.36 | 0.38 | 23 | 0.77 | 0.87 | agree |
| x | 5 | 0.14 | 0.35 | 0.32 | 23 | 0.77 | 0.71 | agree |
| x | 9 | 0.27 | 0.46 | 0.52 | 23 | 1.03 | 0.95 | agree |
| y | 0 | 0.24 | 0.45 | 0.38 | 23 | 1.04 | 0.78 | agree |
| y | 10 | 0.22 | 0.44 | 0.34 | 23 | 0.84 | 0.56 | agree |
| y | 20 | 0.23 | 0.23 | 0.20 | 22 | 0.50 | 0.50 | agree |
| y | 30 | 0.28 | 0.28 | 0.23 | 23 | 0.62 | 0.50 | agree |
| y | 40 | 0.28 | 0.22 | 0.24 | 23 | 0.55 | 0.64 | agree |
| y | 50 | 0.11 | 0.38 | 0.40 | 20 | 0.83 | 0.62 | agree |
| y | 60 | 0.40 | 0.42 | 0.35 | 20 | 0.75 | 0.98 | agree |
| y | 70 | 0.20 | 0.27 | 0.26 | 19 | 0.61 | 0.53 | agree |
| y | 80 | 0.18 | 0.26 | 0.27 | 20 | 0.75 | 0.50 | agree |
| y | 90 | 0.28 | 0.34 | 0.31 | 19 | 0.63 | 0.50 | agree |
| y | 100 | 0.06 | 0.21 | 0.19 | 22 | 0.63 | 0.52 | agree |

(In the plotting coordinates: log10 x, linear y.) Both maps along every verified line and every interval midline (471 places): largest difference 0.0002984 in x (tolerance 0.002016, codex 9), 0.06564 in y (tolerance 0.1216, claude 60); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 23 shared lines checked against the ink, mean of the median distances 0.37 px (claude: x 0.42, y 0.32), 0.35 px (codex: x 0.41, y 0.29), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 138; agreed 134; disagreed 4; unmatched 55 (kept as one-sided: 2 of claude, 53 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| average | feature | -/3 | (none) | 2.6, 84.8 | | | unmatched in claude |
| average | feature | -/4 | (none) | 0.9, 3.2 | | | unmatched in claude |
| average | marker | -/1 | (none) | 4.7, 99.6 | | | unmatched in claude |
| average | marker | -/2 | (none) | 3.3, 96.8 | | | unmatched in claude |
| average | marker | -/3 | (none) | 2.4, 69.8 | | | unmatched in claude |
| average | marker | -/4 | (none) | 2.0, 43.8 | | | unmatched in claude |
| average | marker | -/6 | (none) | 1.2, 7.3 | | | unmatched in claude |
| average | marker | -/7 | (none) | 0.8, 2.4 | | | unmatched in claude |
| average | marker | -/8 | (none) | 0.6, 1.5 | | | unmatched in claude |
| average | marker | -/9 | (none) | 0.4, 0.7 | | | unmatched in claude |
| average | marker | -/10 | (none) | 0.3, 1.0 | | | unmatched in claude |
| average | marker | -/11 | (none) | 0.2, 0.7 | | | unmatched in claude |
| average | marker | -/12 | (none) | 0.2, 0.7 | | | unmatched in claude |
| average | marker | -/13 | (none) | 0.2, 0.5 | | | unmatched in claude |
| average | marker | -/15 | (none) | 0.1, 0.5 | | | unmatched in claude |
| average | trace | 1/- | 0.1, 0.6 (0.0, 0.4) | (no trace at this x) | | | unmatched in codex |
| average | trace | 31/interp | 1.9, 35.0 (0.0, 0.4) | 1.9, 40.7 (0.0, 0.5) | slope +18.8 | -5.7 (tol 2.1) | **disagree** |
| average | trace | 39/interp | 2.3, 65.0 (0.0, 0.4) | 2.3, 70.5 (0.1, 0.9) | slope +35.2 | -5.5 (tol 5.3) | **disagree** |
| lower | feature | 2/4 | 1.2, 4.3 (0.0, 0.5) | 0.9, 1.9 (0.0, 0.9) | +0.3 | +2.3 | **disagree** |
| lower | feature | -/3 | (none) | 2.5, 80.8 | | | unmatched in claude |
| lower | marker | -/1 | (none) | 2.3, 63.1 | | | unmatched in claude |
| lower | marker | -/2 | (none) | 2.0, 37.1 | | | unmatched in claude |
| lower | marker | -/3 | (none) | 1.7, 20.9 | | | unmatched in claude |
| lower | marker | -/4 | (none) | 1.2, 5.7 | | | unmatched in claude |
| lower | marker | -/5 | (none) | 0.8, 1.7 | | | unmatched in claude |
| lower | trace | 1/- | 0.1, 0.6 (0.0, 0.4) | (no trace at this x) | | | unmatched in codex |
| upper | feature | -/3 | (none) | 2.6, 87.9 | | | unmatched in claude |
| upper | feature | -/4 | (none) | 0.9, 4.2 | | | unmatched in claude |
| upper | marker | -/1 | (none) | 3.4, 98.6 | | | unmatched in claude |
| upper | marker | -/3 | (none) | 2.0, 52.3 | | | unmatched in claude |
| upper | marker | -/4 | (none) | 0.8, 3.5 | | | unmatched in claude |
| upper | trace | 46/interp | 3.5, 100.1 (0.0, 0.5) | 3.5, 97.9 (0.1, 1.1) | slope +2.6 | +2.2 (tol 2.1) | **disagree** |

## Ink check (D-031): 12 trace samples excluded

No hand decision overridden.
