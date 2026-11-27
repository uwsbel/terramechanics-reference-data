# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b2\rederived\claude\FA-26\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b2\rederived\codex\FA-26\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 164 | 1083 |
| x per px | 0.0010 | 0.0010 |
| y per px | 0.0686 | 0.0686 |
| RMS residual x, y | 0.002, 0.053 | 0.002, 0.069 |

Corners of claude's box [565, 1207, 2042, 3810] mapped by both calibrations (tolerance 0.01 in x, 0.19 in y (in the plotting coordinates of log10 x, linear y)):

- (9.3, 100.6) vs (9.3, 100.6)
- (9.4, -0.8) vs (9.4, -0.8)
- (0.0, 100.7) vs (0.0, 100.6)
- (0.0, -0.6) vs (0.0, -0.7)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0.02 | 0.26 | 0.42 | 0.27 | 23 | 0.81 | 0.61 | agree |
| x | 0.05 | 0.08 | 0.34 | 0.31 | 20 | 0.50 | 0.55 | agree |
| x | 0.1 | 0.36 | 0.35 | 0.30 | 21 | 0.54 | 1.29 | agree |
| x | 0.2 | 0.19 | 0.14 | 0.15 | 21 | 0.67 | 0.50 | agree |
| x | 0.5 | 1.12 | 0.75 | 0.55 | 23 | 1.62 | 0.77 | agree |
| x | 1 | 0.18 | 0.59 | 0.58 | 23 | 1.34 | 1.06 | agree |
| x | 1.5 | 0.05 | 0.27 | 0.23 | 23 | 0.75 | 0.53 | agree |
| x | 2 | 0.20 | 0.42 | 0.41 | 23 | 0.71 | 0.81 | agree |
| x | 3 | 0.13 | 0.36 | 0.41 | 23 | 0.60 | 0.52 | agree |
| x | 4 | 0.05 | 0.34 | 0.36 | 23 | 0.69 | 0.67 | agree |
| x | 5 | 0.27 | 0.41 | 0.44 | 23 | 0.96 | 0.81 | agree |
| x | 9 | 0.10 | 0.69 | 0.71 | 23 | 1.12 | 1.03 | agree |
| y | 0 | 0.31 | 0.60 | 0.45 | 23 | 0.95 | 0.80 | agree |
| y | 10 | 0.32 | 0.32 | 0.49 | 23 | 0.82 | 0.78 | agree |
| y | 20 | 0.06 | 0.14 | 0.17 | 23 | 0.50 | 0.57 | agree |
| y | 30 | 0.24 | 0.26 | 0.19 | 23 | 0.50 | 0.56 | agree |
| y | 40 | 0.07 | 0.17 | 0.17 | 23 | 0.60 | 0.50 | agree |
| y | 50 | 0.44 | 0.43 | 0.47 | 23 | 1.11 | 0.62 | agree |
| y | 60 | 0.36 | 0.48 | 0.60 | 22 | 1.31 | 1.93 | agree |
| y | 70 | 0.16 | 0.16 | 0.09 | 23 | 0.60 | 0.50 | agree |
| y | 80 | 0.00 | 0.03 | 0.03 | 22 | 0.50 | 0.50 | agree |
| y | 90 | 0.04 | 0.06 | 0.09 | 22 | 0.50 | 0.54 | agree |
| y | 100 | 0.36 | 0.39 | 0.33 | 22 | 0.92 | 0.95 | agree |

(In the plotting coordinates: log10 x, linear y.) Both maps along every verified line and every interval midline (580 places): largest difference 0.0009859 in x (tolerance 0.00248, claude 0.5), 0.04668 in y (tolerance 0.2199, codex 60); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 23 shared lines checked against the ink, mean of the median distances 0.35 px (claude: x 0.42, y 0.28), 0.34 px (codex: x 0.39, y 0.28), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 75; agreed 61; disagreed 14; unmatched 67 (kept as one-sided: 20 of claude, 47 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| average | feature | 1/1 | 0.1, 0.4 (0.0, 0.3) | 0.1, 0.5 (0.0, 0.6) | -0.0 | -0.1 | **disagree** |
| average | feature | 2/2 | 0.8, 100.6 (0.0, 0.3) | 0.8, 100.2 (0.0, 0.5) | -0.0 | +0.4 | **disagree** |
| average | feature | -/3 | (none) | 0.5, 87.6 | | | unmatched in claude |
| average | feature | -/4 | (none) | 0.2, 5.2 | | | unmatched in claude |
| average | marker | -/1 | (none) | 0.6, 94.4 | | | unmatched in claude |
| average | marker | -/2 | (none) | 0.4, 49.4 | | | unmatched in claude |
| average | marker | -/3 | (none) | 0.3, 15.5 | | | unmatched in claude |
| average | marker | -/4 | (none) | 0.3, 7.2 | | | unmatched in claude |
| average | marker | -/5 | (none) | 0.2, 3.5 | | | unmatched in claude |
| average | marker | -/6 | (none) | 0.2, 1.8 | | | unmatched in claude |
| average | marker | -/7 | (none) | 0.1, 0.4 | | | unmatched in claude |
| average | trace | 1/- | 0.1, 0.4 (0.0, 0.3) | (no trace at this x) | | | unmatched in codex |
| average | trace | 4/- | 0.2, 1.9 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| average | trace | 5/- | 0.2, 3.3 (0.0, 0.3) | (no trace at this x) | | | unmatched in codex |
| average | trace | 7/- | 0.3, 7.3 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| average | trace | 8/- | 0.3, 10.7 (0.0, 0.3) | (no trace at this x) | | | unmatched in codex |
| average | trace | 9/- | 0.3, 16.3 (0.0, 0.3) | (no trace at this x) | | | unmatched in codex |
| average | trace | 10/interp | 0.4, 24.1 (0.0, 0.2) | 0.4, 27.6 (0.0, 0.5) | slope +266.3 | -3.5 (tol 3.0) | **disagree** |
| average | trace | 11/interp | 0.4, 25.0 (0.0, 0.2) | 0.4, 28.5 (0.0, 0.3) | slope +223.9 | -3.5 (tol 2.0) | **disagree** |
| average | trace | 15/interp | 0.4, 40.0 (0.0, 0.2) | 0.4, 45.2 (0.0, 2.5) | slope +177.2 | -5.1 (tol 4.4) | **disagree** |
| average | trace | 29/- | 0.6, 96.8 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| average | trace | 31/interp | 0.8, 100.6 (0.0, 0.3) | 0.8, 99.4 (0.0, 0.5) | slope +15.5 | +1.2 (tol 1.1) | **disagree** |
| lower | feature | 1/1 | 0.1, 0.4 (0.0, 0.3) | 0.1, 0.5 (0.0, 0.6) | -0.0 | -0.1 | **disagree** |
| lower | feature | 2/2 | 0.8, 100.6 (0.0, 0.3) | 0.8, 100.2 (0.0, 0.5) | +0.0 | +0.4 | **disagree** |
| lower | feature | -/3 | (none) | 0.5, 87.6 | | | unmatched in claude |
| lower | feature | -/4 | (none) | 0.2, 4.4 | | | unmatched in claude |
| lower | marker | -/1 | (none) | 0.6, 93.4 | | | unmatched in claude |
| lower | marker | -/2 | (none) | 0.4, 47.5 | | | unmatched in claude |
| lower | marker | -/3 | (none) | 0.3, 13.7 | | | unmatched in claude |
| lower | marker | -/4 | (none) | 0.2, 0.6 | | | unmatched in claude |
| lower | trace | 1/- | 0.1, 0.4 (0.0, 0.3) | (no trace at this x) | | | unmatched in codex |
| lower | trace | 4/- | 0.2, 1.3 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| lower | trace | 7/- | 0.3, 6.6 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| lower | trace | 8/- | 0.3, 9.5 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| lower | trace | 9/- | 0.3, 14.8 (0.0, 0.3) | (no trace at this x) | | | unmatched in codex |
| lower | trace | 11/interp | 0.4, 31.5 (0.0, 0.2) | 0.4, 39.9 (0.0, 2.1) | slope +162.7 | -8.5 (tol 4.0) | **disagree** |
| lower | trace | 12/interp | 0.4, 35.0 (0.0, 0.2) | 0.4, 43.1 (0.0, 2.5) | slope +379.5 | -8.1 (tol 5.3) | **disagree** |
| lower | trace | 13/interp | 0.4, 39.7 (0.0, 0.2) | 0.4, 46.6 (0.0, 2.5) | slope +173.6 | -6.9 (tol 4.3) | **disagree** |
| lower | trace | 28/- | 0.8, 100.6 (0.0, 0.3) | (no trace at this x) | | | unmatched in codex |
| upper | feature | 1/1 | 0.1, 0.4 (0.0, 0.3) | 0.1, 0.5 (0.0, 0.6) | -0.0 | -0.1 | **disagree** |
| upper | feature | 2/2 | 0.8, 101.6 (0.0, 0.2) | 0.8, 100.2 (0.0, 0.5) | +0.0 | +1.4 | **disagree** |
| upper | feature | -/3 | (none) | 0.5, 87.6 | | | unmatched in claude |
| upper | feature | -/4 | (none) | 0.2, 5.9 | | | unmatched in claude |
| upper | marker | -/1 | (none) | 0.6, 94.9 | | | unmatched in claude |
| upper | marker | -/2 | (none) | 0.4, 53.4 | | | unmatched in claude |
| upper | marker | -/3 | (none) | 0.3, 17.5 | | | unmatched in claude |
| upper | marker | -/4 | (none) | 0.3, 8.6 | | | unmatched in claude |
| upper | marker | -/5 | (none) | 0.2, 2.2 | | | unmatched in claude |
| upper | trace | 1/- | 0.1, 0.4 (0.0, 0.3) | (no trace at this x) | | | unmatched in codex |
| upper | trace | 4/- | 0.2, 2.6 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| upper | trace | 5/- | 0.2, 4.1 (0.0, 0.3) | (no trace at this x) | | | unmatched in codex |
| upper | trace | 6/- | 0.2, 5.7 (0.0, 0.3) | (no trace at this x) | | | unmatched in codex |
| upper | trace | 7/- | 0.3, 8.5 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| upper | trace | 9/- | 0.3, 18.5 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| upper | trace | 27/- | 0.6, 97.6 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| upper | trace | 28/interp | 0.7, 99.9 (0.0, 0.3) | 0.7, 98.7 (0.0, 0.5) | slope +16.5 | +1.2 (tol 1.1) | **disagree** |
