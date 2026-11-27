# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b2\rederived\claude\FC-3B\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b2\rederived\codex\FC-3B\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 36 | 36 |
| x per px | 0.1712 | 0.1712 |
| y per px | 3.4231 | 3.4228 |
| RMS residual x, y | 0.302, 8.733 | 0.297, 7.936 |

Corners of claude's box [660, 1250, 2170, 2760] mapped by both calibrations (tolerance 0.77 in x, 20.09 in y):

- (-4.6, 5064.9) vs (-4.6, 5065.5)
- (253.9, 5089.5) vs (253.9, 5087.4)
- (-4.3, -103.9) vs (-4.3, -102.9)
- (254.3, -79.3) vs (254.3, -81.0)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.11 | 0.32 | 0.28 | 15 | 0.50 | 0.50 | agree |
| x | 50 | 0.08 | 0.15 | 0.14 | 13 | 0.53 | 0.50 | agree |
| x | 100 | 0.27 | 0.14 | 0.14 | 11 | 1.38 | 1.08 | agree |
| x | 150 | 0.10 | 0.35 | 0.31 | 13 | 2.22 | 2.11 | agree |
| x | 200 | 0.12 | 0.39 | 0.42 | 12 | 1.10 | 1.33 | agree |
| x | 250 | 0.04 | 0.15 | 0.14 | 15 | 0.50 | 0.50 | agree |
| y | 0 | 0.17 | 0.25 | 0.15 | 15 | 0.58 | 0.54 | agree |
| y | 1000 | 0.08 | 0.38 | 0.38 | 15 | 1.07 | 1.02 | agree |
| y | 2000 | 0.06 | 0.44 | 0.43 | 15 | 0.95 | 0.93 | agree |
| y | 3000 | 0.08 | 0.35 | 0.33 | 23 | 1.47 | 1.58 | agree |
| y | 4000 | 0.16 | 0.23 | 0.22 | 15 | 0.53 | 0.51 | agree |
| y | 5000 | 0.12 | 0.39 | 0.34 | 15 | 0.64 | 0.69 | agree |

Both maps along every verified line and every interval midline (284 places): largest difference 0.05053 in x (tolerance 0.4202, claude 100), 0.6464 in y (tolerance 7.035, claude 0); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 12 shared lines checked against the ink, mean of the median distances 0.29 px (claude: x 0.25, y 0.34), 0.27 px (codex: x 0.24, y 0.31), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 246; agreed 242; disagreed 4; unmatched 63 (kept as one-sided: 55 of claude, 8 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1761 | feature | 1/1 | 13.7, 784.6 (0.4, 18.6) | 10.2, 740.2 (0.6, 13.2) | +3.4 | +44.4 | **disagree** |
| n1761 | trace | 5/- | 33.7, 991.0 (0.3, 23.9) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 6/- | 35.3, 1001.2 (0.3, 23.9) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 12/- | 65.1, 1198.2 (0.3, 15.4) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 13/- | 73.1, 1254.6 (0.3, 17.1) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 20/- | 104.0, 1389.1 (0.4, 17.0) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 29/- | 151.8, 1584.1 (0.6, 18.6) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 33/- | 172.9, 1656.8 (0.5, 18.6) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 36/- | 184.6, 1700.1 (0.4, 16.9) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 43/- | 221.9, 1813.1 (0.3, 18.5) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 48/- | 245.5, 1826.8 (0.3, 20.2) | (no trace at this x) | | | unmatched in codex |
| n2934 | feature | 1/1 | 12.4, 1055.4 (0.4, 29.0) | 9.7, 946.6 (1.1, 23.8) | +2.7 | +108.8 | **disagree** |
| n2934 | trace | 5/- | 27.6, 1428.8 (0.3, 15.3) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 6/- | 35.2, 1600.4 (0.3, 13.5) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 9/- | 47.0, 1775.6 (0.3, 21.9) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 12/- | 65.0, 1990.3 (0.3, 22.2) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 15/- | 84.3, 2148.4 (0.4, 26.3) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 16/- | 91.7, 2217.0 (0.4, 17.7) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 22/- | 124.7, 2437.8 (0.5, 12.9) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 25/- | 144.0, 2546.0 (0.5, 14.8) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 26/- | 152.0, 2586.9 (0.6, 16.6) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 30/- | 172.1, 2669.0 (0.5, 20.3) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 34/- | 193.3, 2706.0 (0.4, 16.9) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 39/- | 215.1, 2697.6 (0.3, 16.9) | (no trace at this x) | | | unmatched in codex |
| n3815 | feature | 1/1 | 12.6, 1429.4 (0.4, 33.9) | 9.7, 1342.7 (0.6, 13.6) | +2.9 | +86.7 | **disagree** |
| n3815 | trace | 5/- | 33.4, 1881.2 (0.3, 27.0) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 8/- | 44.7, 2061.5 (0.3, 26.1) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 9/- | 51.4, 2156.1 (0.3, 15.8) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 13/- | 72.4, 2391.3 (0.3, 16.2) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 16/- | 85.0, 2498.7 (0.4, 14.7) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 17/- | 92.0, 2562.0 (0.4, 14.8) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 20/- | 105.0, 2653.9 (0.4, 25.5) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 21/- | 111.3, 2691.1 (0.4, 20.3) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 25/- | 131.9, 2796.0 (0.5, 25.7) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 28/- | 144.6, 2842.6 (0.5, 29.3) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 32/- | 164.3, 2910.9 (0.5, 26.0) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 33/- | 171.1, 2932.5 (0.5, 26.0) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 36/- | 184.8, 2968.8 (0.4, 26.1) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 42/- | 214.7, 2989.3 (0.3, 26.0) | (no trace at this x) | | | unmatched in codex |
| n4695 | feature | 2/- | 240.3, 3829.1 | (none) | | | unmatched in codex |
| n4695 | trace | 13/- | 72.7, 2988.7 (0.3, 26.0) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 14/- | 74.9, 2999.4 (0.3, 26.0) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 21/- | 110.2, 3307.9 (0.4, 16.0) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 24/- | 124.3, 3385.9 (0.5, 17.5) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 29/- | 152.2, 3522.8 (0.5, 18.7) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 33/- | 170.3, 3573.7 (0.5, 16.8) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 37/- | 193.1, 3664.0 (0.4, 23.4) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 43/- | 218.6, 3783.3 (0.3, 17.9) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 44/- | 228.5, 3812.9 (0.3, 16.1) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 48/- | 244.7, 3826.0 (0.3, 17.7) | (no trace at this x) | | | unmatched in codex |
| n734 | feature | 1/1 | 12.7, 391.8 (0.4, 11.1) | 9.7, 354.5 (0.6, 12.6) | +2.9 | +37.2 | **disagree** |
| n734 | trace | 8/- | 48.4, 587.9 (0.3, 11.4) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 9/- | 58.0, 632.7 (0.3, 18.3) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 12/- | 72.8, 677.9 (0.3, 18.3) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 16/- | 94.9, 735.5 (0.4, 13.3) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 19/- | 113.0, 774.2 (0.4, 23.5) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 32/- | 183.7, 825.4 (0.4, 18.5) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 33/- | 192.2, 822.7 (0.4, 11.8) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 38/- | 212.9, 812.6 (0.3, 23.5) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 1 trace samples excluded

Overrides of hand decisions (1), for review:

- claude n3815 trace 48: hand decision one-sided-verified (on the ink of the drawn line, verified on the page by codex's adjudicator; blind adjudication item 1)
