# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b3\rederived\claude\FC-5B\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b3\rederived\codex\FC-5B\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 36 | 36 |
| x per px | 0.1689 | 0.1689 |
| y per px | 3.3998 | 3.3999 |
| RMS residual x, y | 0.952, 3.586 | 0.955, 3.525 |

Corners of claude's box [645, 955, 2180, 2475] mapped by both calibrations (tolerance 2.08 in x, 10.51 in y):

- (-4.7, 5096.0) vs (-4.8, 5095.7)
- (254.4, 5086.1) vs (254.5, 5086.3)
- (-6.0, -71.7) vs (-6.0, -72.1)
- (253.2, -81.5) vs (253.2, -81.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.05 | 0.33 | 0.30 | 15 | 0.53 | 0.50 | agree |
| x | 50 | 0.19 | 0.37 | 0.30 | 15 | 1.28 | 1.07 | agree |
| x | 100 | 0.17 | 0.14 | 0.22 | 14 | 0.54 | 0.50 | agree |
| x | 150 | 0.12 | 0.22 | 0.23 | 15 | 0.50 | 0.50 | agree |
| x | 200 | 0.05 | 0.18 | 0.18 | 15 | 0.50 | 0.50 | agree |
| x | 250 | 0.34 | 0.25 | 0.26 | 15 | 0.50 | 0.61 | agree |
| y | 1000 | | | | | | | claude's line not a knot: misplaced: 2.60 px from the ink's line at an end of the line |
| y | 1000 | | | | | | | codex's line not a knot: misplaced: 2.63 px from the ink's line at an end of the line |
| y | 0 | 0.15 | 0.40 | 0.34 | 15 | 0.71 | 0.57 | agree |
| y | 2000 | 0.26 | 0.41 | 0.31 | 15 | 1.25 | 1.07 | agree |
| y | 3000 | 0.00 | 0.37 | 0.37 | 15 | 0.86 | 0.86 | agree |
| y | 4000 | 0.22 | 0.53 | 0.60 | 15 | 0.89 | 0.77 | agree |
| y | 5000 | 0.09 | 0.30 | 0.32 | 15 | 0.72 | 0.81 | agree |

Both maps along every verified line and every interval midline (251 places): largest difference 0.06261 in x (tolerance 0.1874, claude 250), 0.9548 in y (tolerance 7.944, claude 2000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.32 px (claude: x 0.25, y 0.40), 0.31 px (codex: x 0.25, y 0.39), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 394; agreed 364; disagreed 30; unmatched 35 (kept as one-sided: 8 of claude, 27 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1761 | feature | 1/79 | 9.5, 627.2 (0.1, 14.3) | 9.0, 636.8 (0.2, 9.8) | +0.5 | -9.6 | **disagree** |
| n1761 | feature | 2/80 | 189.6, 986.5 (7.8, 13.9) | 156.2, 960.3 (14.6, 10.4) | +33.4 | +26.2 | **disagree** |
| n1761 | marker | 10/10 | 167.8, 997.5 (0.2, 6.8) | 167.8, 977.0 (0.6, 11.7) | +0.0 | +20.5 | **disagree** |
| n1761 | marker | 11/11 | 188.0, 998.5 (0.2, 6.8) | 187.9, 979.8 (0.6, 11.7) | +0.1 | +18.7 | **disagree** |
| n1761 | marker | 13/13 | 249.9, 940.1 (0.3, 5.1) | 248.9, 940.5 (0.6, 13.3) | +1.0 | -0.4 | **disagree** |
| n1761 | trace | 56/- | 246.9, 945.3 (0.1, 11.9) | (no trace at this x) | | | unmatched in codex |
| n2934 | feature | 1/82 | 7.5, 842.5 (0.5, 3.3) | 8.4, 886.2 (0.2, 9.9) | -0.9 | -43.7 | **disagree** |
| n2934 | trace | 1/- | 7.5, 842.5 (0.5, 3.3) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 2/- | 7.8, 863.0 (0.5, 3.3) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 3/- | 8.2, 883.5 (0.5, 3.3) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 76/- | 246.6, 1593.5 (0.1, 13.9) | (no trace at this x) | | | unmatched in codex |
| n3815 | feature | 1/79 | 8.4, 1170.4 (0.6, 3.5) | 8.8, 1200.4 (0.2, 10.0) | -0.4 | -30.0 | **disagree** |
| n3815 | marker | 2/2 | 19.9, 1632.2 (0.2, 5.4) | 19.8, 1616.7 (0.2, 5.1) | +0.1 | +15.5 | **disagree** |
| n3815 | marker | 4/4 | 47.7, 1936.4 (0.3, 5.5) | 47.8, 1923.1 (0.2, 5.2) | -0.1 | +13.3 | **disagree** |
| n3815 | marker | 5/5 | 77.5, 2083.6 (0.2, 7.2) | 77.5, 2065.1 (0.2, 5.2) | +0.0 | +18.5 | **disagree** |
| n3815 | marker | 6/6 | 93.0, 2165.1 (0.2, 5.4) | 93.1, 2152.8 (0.2, 5.2) | -0.1 | +12.3 | **disagree** |
| n3815 | marker | 7/7 | 107.3, 2223.9 (0.2, 5.4) | 107.3, 2208.3 (0.2, 5.2) | -0.1 | +15.6 | **disagree** |
| n3815 | marker | 9/9 | 148.5, 2248.4 (0.3, 7.1) | 148.5, 2235.7 (0.2, 5.1) | +0.0 | +12.7 | **disagree** |
| n3815 | marker | 10/10 | 172.2, 2221.4 (0.2, 5.4) | 172.2, 2206.0 (0.2, 5.2) | +0.0 | +15.4 | **disagree** |
| n3815 | marker | 12/12 | 217.5, 2169.7 (0.2, 5.4) | 217.6, 2158.6 (0.2, 5.2) | -0.0 | +11.1 | **disagree** |
| n3815 | marker | 13/13 | 245.9, 2117.6 (0.2, 5.5) | 245.7, 2105.0 (0.2, 5.2) | +0.1 | +12.7 | **disagree** |
| n3815 | trace | 1/- | 8.4, 1170.4 (0.6, 3.5) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 66/- | 242.7, 2099.8 (0.1, 11.4) | (no trace at this x) | | | unmatched in codex |
| n4695 | marker | 4/4 | 48.1, 2458.6 (0.3, 5.2) | 48.6, 2463.3 (0.2, 5.1) | -0.6 | -4.7 | **disagree** |
| n4695 | marker | 8/8 | 127.2, 2640.5 (0.2, 5.1) | 127.8, 2643.8 (0.2, 5.0) | -0.6 | -3.3 | **disagree** |
| n4695 | marker | 11/11 | 197.3, 2632.8 (0.2, 5.1) | 198.2, 2634.4 (0.2, 5.0) | -0.9 | -1.7 | **disagree** |
| n734 | feature | 3/82 | 246.5, 795.3 (0.1, 11.8) | 246.1, 797.3 (0.2, 10.7) | +0.5 | -2.1 | **disagree** |
| n734 | feature | 2/81 | 218.5, 799.6 (13.6, 12.3) | 196.4, 774.9 (18.1, 10.3) | +22.0 | +24.7 | **disagree** |
| n734 | marker | 4/4 | 48.6, 736.9 (0.3, 5.0) | 48.5, 750.0 (0.2, 4.7) | +0.1 | -13.2 | **disagree** |
| n734 | marker | 5/5 | 68.7, 748.2 (0.3, 5.0) | 68.8, 761.4 (0.2, 4.7) | -0.1 | -13.3 | **disagree** |
| n734 | marker | 6/6 | 88.1, 767.0 (0.2, 5.0) | 88.0, 779.6 (0.2, 4.7) | +0.1 | -12.7 | **disagree** |
| n734 | marker | 7/7 | 107.8, 782.1 (0.2, 6.7) | 107.8, 797.9 (0.2, 4.7) | +0.0 | -15.8 | **disagree** |
| n734 | marker | 8/8 | 127.5, 794.0 (0.2, 5.0) | 127.6, 807.5 (0.2, 4.7) | -0.1 | -13.5 | **disagree** |
| n734 | marker | 9/9 | 148.2, 795.1 (0.3, 8.4) | 148.0, 817.2 (0.2, 4.7) | +0.2 | -22.1 | **disagree** |
| n734 | marker | 10/10 | 168.0, 791.0 (0.2, 6.7) | 168.0, 806.4 (0.2, 4.7) | +0.0 | -15.4 | **disagree** |
| n734 | marker | 11/11 | 188.3, 804.7 (0.2, 5.0) | 188.3, 816.0 (0.2, 4.7) | +0.0 | -11.4 | **disagree** |
| n734 | marker | 12/12 | 218.0, 809.2 (0.2, 5.0) | 218.1, 820.3 (0.2, 4.7) | -0.0 | -11.1 | **disagree** |
| n734 | trace | 66/- | 246.5, 795.3 (0.1, 11.8) | (no trace at this x) | | | unmatched in codex |
