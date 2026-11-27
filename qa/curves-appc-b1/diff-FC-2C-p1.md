# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-2C\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-2C\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 42 | 42 |
| x per px | 0.1713 | 0.1713 |
| y per px | 3.4462 | 3.4460 |
| RMS residual x, y | 0.471, 2.770 | 0.465, 2.678 |

Corners of claude's box [670, 1050, 2175, 2835] mapped by both calibrations (tolerance 1.11 in x, 8.89 in y):

- (-3.7, 6057.9) vs (-3.7, 6056.8)
- (254.1, 6078.6) vs (254.1, 6078.8)
- (-3.5, -93.5) vs (-3.5, -94.3)
- (254.4, -72.8) vs (254.4, -72.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.03 | 0.16 | 0.16 | 18 | 0.50 | 0.50 | agree |
| x | 50 | 0.01 | 0.16 | 0.15 | 18 | 0.50 | 0.50 | agree |
| x | 100 | 0.36 | 0.25 | 0.37 | 17 | 1.01 | 0.62 | agree |
| x | 150 | 0.07 | 0.31 | 0.32 | 16 | 0.52 | 0.60 | agree |
| x | 200 | 0.15 | 0.37 | 0.33 | 18 | 0.62 | 0.62 | agree |
| x | 250 | 0.04 | 0.33 | 0.34 | 18 | 0.50 | 0.50 | agree |
| y | 0 | 0.05 | 0.18 | 0.18 | 15 | 0.50 | 0.50 | agree |
| y | 1000 | 0.14 | 0.16 | 0.22 | 15 | 0.50 | 0.65 | agree |
| y | 2000 | 0.05 | 0.40 | 0.37 | 15 | 0.50 | 0.53 | agree |
| y | 3000 | 0.21 | 0.23 | 0.27 | 15 | 0.50 | 0.64 | agree |
| y | 4000 | 1.09 | 0.45 | 0.46 | 13 | 1.28 | 1.05 | agree |
| y | 5000 | 0.22 | 0.59 | 0.53 | 14 | 0.98 | 0.78 | agree |
| y | 6000 | 0.22 | 0.37 | 0.34 | 15 | 0.63 | 0.50 | agree |

Both maps along every verified line and every interval midline (312 places): largest difference 0.06605 in x (tolerance 0.2753, claude 100), 3.234 in y (tolerance 8.049, claude 4000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 13 shared lines checked against the ink, mean of the median distances 0.30 px (claude: x 0.26, y 0.34), 0.31 px (codex: x 0.28, y 0.34), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

6 series in claude, 6 in codex.


## Points

Matched: 156; agreed 156; disagreed 0; unmatched 136 (kept as one-sided: 41 of claude, 95 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1468 | trace | 2/- | 7.7, 1124.4 (0.4, 15.6) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 3/- | 13.0, 1352.0 (0.4, 15.6) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 4/- | 18.1, 1502.5 (0.4, 19.0) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 5/- | 23.5, 1614.4 (0.4, 19.0) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 7/- | 33.1, 1777.1 (0.4, 8.7) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 3/- | 17.8, 1668.5 (0.4, 15.6) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 4/- | 22.9, 1823.6 (0.4, 19.0) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 6/- | 33.6, 2107.5 (0.4, 15.5) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 11/- | 58.8, 2591.9 (0.4, 18.9) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 16/- | 83.5, 2856.0 (0.5, 25.8) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 17/- | 88.6, 2921.6 (0.5, 12.0) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 19/- | 98.6, 2960.0 (0.5, 15.5) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 20/- | 103.5, 3005.1 (0.5, 19.2) | (no trace at this x) | | | unmatched in codex |
| n2200 | trace | 22/- | 113.4, 3030.2 (0.5, 15.8) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 2/- | 18.0, 2852.4 (0.4, 18.9) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 10/- | 58.6, 3710.5 (0.4, 21.1) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 13/- | 73.3, 3862.3 (0.5, 28.5) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 14/- | 78.7, 3892.6 (0.5, 11.2) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 15/- | 84.3, 3945.9 (0.5, 11.3) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 24/- | 127.7, 4088.6 (0.5, 25.0) | (no trace at this x) | | | unmatched in codex |
| n2995 | trace | 28/- | 146.7, 4054.7 (0.6, 18.1) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 4/- | 23.3, 3265.4 (0.4, 16.4) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 6/- | 33.2, 3537.2 (0.4, 10.2) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 7/- | 38.1, 3657.2 (0.4, 24.5) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 11/- | 57.9, 4003.3 (0.6, 18.3) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 23/- | 118.1, 4457.7 (0.5, 24.6) | (no trace at this x) | | | unmatched in codex |
| n3660 | trace | 24/- | 123.4, 4469.8 (0.5, 10.8) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 5/- | 43.6, 4168.1 (0.4, 21.4) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 6/- | 48.5, 4303.4 (0.4, 17.9) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 14/- | 88.6, 4963.7 (0.5, 20.6) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 18/- | 108.6, 5119.6 (0.5, 23.9) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 20/- | 118.3, 5186.4 (0.5, 23.8) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 22/- | 127.8, 5224.3 (0.5, 23.8) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 25/- | 143.3, 5246.5 (0.6, 16.9) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 27/- | 153.4, 5240.4 (0.6, 16.9) | (no trace at this x) | | | unmatched in codex |
| n4400 | trace | 30/- | 167.2, 5161.3 (0.4, 10.1) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 2/- | 12.9, 1032.0 (0.4, 22.5) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 4/- | 23.3, 1242.7 (0.4, 12.1) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 7/- | 38.4, 1346.4 (0.4, 8.7) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 8/- | 43.4, 1349.9 (0.4, 12.1) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 13/- | 68.3, 1277.4 (0.5, 19.0) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 124 trace samples excluded

Overrides of hand decisions (3), for review:

- claude n4400 trace 7: hand decision resolved use codex (the other reading is on the line's ink and the kept one is not; credit codex (audit re-check 2026-10)
- claude n3660 trace 8: hand decision resolved use codex (the other reading is on the line's ink and the kept one is not; credit codex (audit re-check 2026-10)
- claude n2995 trace 9: hand decision resolved use codex (the other reading is on the line's ink and the kept one is not; credit codex (audit re-check 2026-10)
