# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b2\rederived\claude\FA-18\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b2\rederived\codex\FA-18\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 132 | 981 |
| x per px | 0.0010 | 0.0010 |
| y per px | 0.0685 | 0.0685 |
| RMS residual x, y | 0.003, 0.050 | 0.003, 0.049 |

Corners of claude's box [565, 1100, 2125, 3755] mapped by both calibrations (tolerance 0.01 in x, 0.17 in y (in the plotting coordinates of log10 x, linear y)):

- (10.6, 101.4) vs (10.6, 101.4)
- (9.9, -5.5) vs (9.9, -5.5)
- (0.0, 105.3) vs (0.0, 105.3)
- (0.0, -1.6) vs (0.0, -1.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0.02 | 0.08 | 0.39 | 0.38 | 24 | 0.76 | 0.64 | agree |
| x | 0.05 | 0.11 | 0.28 | 0.27 | 21 | 0.81 | 0.78 | agree |
| x | 0.1 | 0.10 | 0.38 | 0.36 | 21 | 0.57 | 0.50 | agree |
| x | 0.2 | 0.10 | 0.15 | 0.19 | 21 | 0.61 | 0.50 | agree |
| x | 0.5 | 0.20 | 0.35 | 0.35 | 22 | 1.09 | 0.54 | agree |
| x | 1 | 0.43 | 0.63 | 0.49 | 24 | 1.23 | 1.04 | agree |
| x | 1.5 | 0.42 | 0.33 | 0.37 | 23 | 0.50 | 0.74 | agree |
| x | 2 | 0.19 | 0.43 | 0.34 | 23 | 0.89 | 0.57 | agree |
| x | 3 | 0.21 | 0.43 | 0.41 | 24 | 0.82 | 0.78 | agree |
| x | 4 | 0.15 | 0.33 | 0.24 | 24 | 0.50 | 0.94 | agree |
| x | 5 | 0.30 | 0.38 | 0.35 | 24 | 0.74 | 0.59 | agree |
| x | 9 | 0.13 | 0.36 | 0.40 | 24 | 0.57 | 0.72 | agree |
| y | 0 | 0.32 | 0.43 | 0.30 | 23 | 0.91 | 0.89 | agree |
| y | 10 | 0.14 | 0.31 | 0.34 | 24 | 0.70 | 0.77 | agree |
| y | 20 | 0.11 | 0.52 | 0.51 | 24 | 0.82 | 0.64 | agree |
| y | 30 | 0.11 | 0.22 | 0.23 | 24 | 0.60 | 0.50 | agree |
| y | 40 | 0.50 | 0.27 | 0.31 | 23 | 0.60 | 0.50 | agree |
| y | 50 | 0.18 | 0.34 | 0.44 | 23 | 0.70 | 0.64 | agree |
| y | 60 | 0.18 | 0.63 | 0.81 | 22 | 2.27 | 1.45 | agree |
| y | 70 | 0.32 | 0.21 | 0.28 | 21 | 1.69 | 0.68 | agree |
| y | 80 | 0.12 | 0.34 | 0.30 | 20 | 0.50 | 0.63 | agree |
| y | 90 | 0.08 | 0.32 | 0.27 | 24 | 0.61 | 0.50 | agree |
| y | 100 | 0.19 | 0.30 | 0.28 | 23 | 0.66 | 0.72 | agree |

(In the plotting coordinates: log10 x, linear y.) Both maps along every verified line and every interval midline (462 places): largest difference 0.0003551 in x (tolerance 0.001986, codex 1.5), 0.02852 in y (tolerance 0.08554, claude 40); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 23 shared lines checked against the ink, mean of the median distances 0.36 px (claude: x 0.37, y 0.35), 0.36 px (codex: x 0.35, y 0.37), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 163; agreed 135; disagreed 28; unmatched 29 (kept as one-sided: 3 of claude, 26 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| average | feature | 1/1 | 0.1, 0.4 (0.0, 0.2) | 0.1, 0.6 (0.0, 0.5) | -0.0 | -0.1 | **disagree** |
| average | feature | 2/4 | 2.0, 24.5 (0.0, 0.2) | 0.9, 2.0 (0.0, 0.6) | +1.1 | +22.5 | **disagree** |
| average | feature | 3/3 | 2.8, 95.0 (0.0, 0.2) | 2.5, 81.4 (0.1, 4.7) | +0.3 | +13.6 | **disagree** |
| average | marker | -/2 | (none) | 3.4, 99.0 | | | unmatched in claude |
| average | marker | -/3 | (none) | 2.4, 64.6 | | | unmatched in claude |
| average | marker | -/4 | (none) | 2.0, 25.6 | | | unmatched in claude |
| average | marker | -/5 | (none) | 1.7, 14.0 | | | unmatched in claude |
| average | marker | -/6 | (none) | 1.2, 3.9 | | | unmatched in claude |
| average | marker | -/7 | (none) | 0.8, 1.9 | | | unmatched in claude |
| average | marker | -/8 | (none) | 0.6, 1.2 | | | unmatched in claude |
| average | marker | -/9 | (none) | 0.4, 0.8 | | | unmatched in claude |
| average | marker | -/10 | (none) | 0.3, 0.7 | | | unmatched in claude |
| average | marker | -/11 | (none) | 0.3, 0.6 | | | unmatched in claude |
| average | marker | -/12 | (none) | 0.2, 0.4 | | | unmatched in claude |
| average | marker | -/13 | (none) | 0.2, 0.4 | | | unmatched in claude |
| average | marker | -/14 | (none) | 0.1, 0.5 | | | unmatched in claude |
| average | marker | -/15 | (none) | 0.1, 0.5 | | | unmatched in claude |
| average | trace | 1/- | 0.1, 0.4 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| average | trace | 11/interp | 0.2, 1.2 (0.0, 0.2) | 0.2, 0.0 (0.0, 0.7) | slope -43.4 | +1.2 (tol 1.2) | **disagree** |
| average | trace | 12/interp | 0.3, 1.2 (0.0, 0.2) | 0.3, 0.0 (0.0, 0.7) | slope -0.0 | +1.2 (tol 0.9) | **disagree** |
| average | trace | 15/interp | 0.4, 1.4 (0.0, 0.2) | 0.4, 0.0 (0.0, 1.0) | slope -17.1 | +1.4 (tol 1.3) | **disagree** |
| lower | feature | 1/1 | 0.1, 0.3 (0.0, 0.2) | 0.1, 0.6 (0.0, 0.5) | -0.0 | -0.3 | **disagree** |
| lower | feature | 2/4 | 2.0, 20.8 (0.0, 0.2) | 1.0, 1.3 (0.0, 0.4) | +1.0 | +19.4 | **disagree** |
| lower | feature | 3/3 | 2.8, 95.0 (0.0, 0.2) | 2.5, 81.4 (0.1, 4.7) | +0.3 | +13.6 | **disagree** |
| lower | marker | -/1 | (none) | 2.4, 60.1 | | | unmatched in claude |
| lower | marker | -/2 | (none) | 2.0, 22.5 | | | unmatched in claude |
| lower | marker | -/3 | (none) | 1.7, 12.2 | | | unmatched in claude |
| lower | marker | -/4 | (none) | 1.2, 2.6 | | | unmatched in claude |
| lower | marker | -/5 | (none) | 0.8, 0.5 | | | unmatched in claude |
| lower | marker | -/6 | (none) | 0.6, 0.5 | | | unmatched in claude |
| lower | trace | 1/- | 0.1, 0.3 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| upper | feature | 1/1 | 0.1, 1.1 (0.0, 0.2) | 0.1, 0.6 (0.0, 0.5) | -0.0 | +0.5 | **disagree** |
| upper | feature | 2/4 | 2.0, 28.0 (0.0, 0.2) | 0.9, 3.1 (0.0, 0.4) | +1.1 | +25.0 | **disagree** |
| upper | feature | 3/3 | 2.7, 95.0 (0.0, 0.2) | 2.5, 81.4 (0.1, 4.7) | +0.2 | +13.6 | **disagree** |
| upper | marker | -/1 | (none) | 2.4, 74.4 | | | unmatched in claude |
| upper | marker | -/2 | (none) | 2.0, 30.2 | | | unmatched in claude |
| upper | marker | -/3 | (none) | 1.7, 15.7 | | | unmatched in claude |
| upper | marker | -/4 | (none) | 1.2, 5.7 | | | unmatched in claude |
| upper | marker | -/5 | (none) | 0.8, 2.8 | | | unmatched in claude |
| upper | marker | -/6 | (none) | 0.6, 2.1 | | | unmatched in claude |
| upper | trace | 1/- | 0.1, 1.1 (0.0, 0.2) | (no trace at this x) | | | unmatched in codex |
| upper | trace | 4/interp | 0.1, 1.4 (0.0, 0.2) | 0.1, -0.0 (0.0, 0.7) | slope +35.3 | +1.4 (tol 1.0) | **disagree** |
| upper | trace | 5/interp | 0.1, 1.4 (0.0, 0.2) | 0.1, 0.4 (0.0, 0.6) | slope +40.9 | +1.0 (tol 0.9) | **disagree** |
| upper | trace | 7/interp | 0.1, 1.7 (0.0, 0.2) | 0.1, 0.8 (0.0, 0.6) | slope +2.0 | +1.0 (tol 0.8) | **disagree** |
| upper | trace | 8/interp | 0.2, 1.7 (0.0, 0.2) | 0.2, 0.8 (0.0, 0.6) | slope +0.0 | +0.9 (tol 0.8) | **disagree** |
| upper | trace | 9/interp | 0.2, 1.8 (0.0, 0.2) | 0.2, 0.8 (0.0, 0.6) | slope +0.0 | +1.0 (tol 0.8) | **disagree** |
| upper | trace | 12/interp | 0.3, 1.9 (0.0, 0.2) | 0.3, 0.2 (0.0, 0.7) | slope -21.3 | +1.7 (tol 1.1) | **disagree** |
| upper | trace | 13/interp | 0.3, 2.0 (0.0, 0.2) | 0.3, 0.8 (0.0, 0.6) | slope -2.2 | +1.2 (tol 0.8) | **disagree** |
| upper | trace | 14/interp | 0.3, 2.1 (0.0, 0.2) | 0.3, 0.7 (0.0, 1.0) | slope -18.4 | +1.5 (tol 1.3) | **disagree** |
| upper | trace | 15/interp | 0.4, 2.0 (0.0, 0.2) | 0.4, 0.0 (0.0, 1.0) | slope -16.5 | +2.0 (tol 1.3) | **disagree** |
| upper | trace | 16/interp | 0.4, 2.1 (0.0, 0.2) | 0.4, 1.0 (0.0, 0.7) | slope +2.2 | +1.2 (tol 0.9) | **disagree** |
| upper | trace | 17/interp | 0.4, 2.1 (0.0, 0.2) | 0.4, 1.1 (0.0, 0.7) | slope +0.2 | +1.1 (tol 1.0) | **disagree** |
| upper | trace | 18/interp | 0.5, 2.3 (0.0, 0.2) | 0.5, 1.1 (0.0, 0.7) | slope +9.0 | +1.1 (tol 1.1) | **disagree** |
| upper | trace | 19/interp | 0.6, 2.4 (0.0, 0.2) | 0.6, 1.7 (0.0, 0.4) | slope +5.0 | +0.7 (tol 0.7) | **disagree** |
| upper | trace | 24/interp | 1.0, 3.5 (0.0, 0.2) | 1.0, 2.9 (0.0, 0.2) | slope -3.3 | +0.7 (tol 0.4) | **disagree** |
| upper | trace | 30/interp | 2.0, 28.0 (0.0, 0.2) | 2.0, 23.8 (0.0, 0.5) | slope +21.3 | +4.2 (tol 1.9) | **disagree** |
| upper | trace | 31/interp | 2.0, 30.0 (0.0, 0.2) | 2.0, 25.4 (0.0, 0.5) | slope +62.7 | +4.6 (tol 4.2) | **disagree** |
