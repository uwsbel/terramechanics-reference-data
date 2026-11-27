# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b2\rederived\claude\FC-4B\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b2\rederived\codex\FC-4B\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 36 | 36 |
| x per px | 0.1720 | 0.1720 |
| y per px | 3.4304 | 3.4302 |
| RMS residual x, y | 0.306, 20.369 | 0.299, 20.588 |

Corners of claude's box [770, 1180, 2290, 2690] mapped by both calibrations (tolerance 0.78 in x, 44.39 in y):

- (-5.4, 5049.1) vs (-5.4, 5048.8)
- (256.1, 5066.5) vs (256.1, 5066.3)
- (-5.3, -130.9) vs (-5.3, -130.8)
- (256.1, -113.4) vs (256.1, -113.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.17 | 0.13 | 0.10 | 15 | 0.50 | 0.52 | agree |
| x | 50 | 0.44 | 0.31 | 0.23 | 14 | 1.94 | 1.56 | agree |
| x | 100 | 0.22 | 0.06 | 0.11 | 13 | 0.50 | 0.50 | agree |
| x | 150 | 0.10 | 0.14 | 0.10 | 15 | 0.73 | 0.63 | agree |
| x | 200 | 0.29 | 0.30 | 0.31 | 14 | 0.66 | 0.72 | agree |
| x | 250 | 0.35 | 0.45 | 0.71 | 15 | 1.07 | 1.11 | agree |
| y | 0 | 0.21 | 0.16 | 0.27 | 15 | 0.50 | 0.50 | agree |
| y | 1000 | 0.15 | 0.24 | 0.19 | 15 | 0.50 | 0.50 | agree |
| y | 2000 | 0.12 | 0.35 | 0.38 | 15 | 0.74 | 0.60 | agree |
| y | 3000 | 0.29 | 0.49 | 0.42 | 15 | 1.06 | 0.78 | agree |
| y | 4000 | 0.17 | 0.23 | 0.30 | 15 | 0.50 | 0.50 | agree |
| y | 5000 | 0.19 | 0.35 | 0.35 | 15 | 0.87 | 1.18 | agree |

Both maps along every verified line and every interval midline (295 places): largest difference 0.08158 in x (tolerance 0.6027, codex 50), 0.925 in y (tolerance 6.319, codex 3000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 12 shared lines checked against the ink, mean of the median distances 0.27 px (claude: x 0.23, y 0.30), 0.29 px (codex: x 0.26, y 0.32), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 249; agreed 238; disagreed 11; unmatched 56 (kept as one-sided: 39 of claude, 17 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1761 | feature | 3/4 | 248.3, 1733.7 (0.3, 6.3) | 245.8, 1776.0 (0.4, 7.8) | +2.5 | -42.3 | **disagree** |
| n1761 | feature | -/2 | (none) | 169.0, 1678.4 | | | unmatched in claude |
| n1761 | trace | 4/- | 26.8, 735.3 (0.2, 10.9) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 8/- | 46.1, 955.0 (0.2, 10.9) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 9/- | 53.0, 1014.5 (0.2, 14.5) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 20/- | 112.8, 1438.2 (0.1, 11.2) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 23/- | 126.1, 1502.0 (0.1, 11.3) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 27/- | 145.6, 1585.0 (0.1, 11.3) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 37/- | 196.1, 1910.2 (0.1, 13.2) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 38/- | 202.9, 1926.1 (0.1, 11.5) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 41/- | 215.6, 1860.7 (0.2, 6.3) | (no trace at this x) | | | unmatched in codex |
| n2934 | feature | 1/1 | 9.9, 791.3 (0.4, 7.6) | 11.3, 810.3 (0.3, 5.9) | -1.5 | -18.9 | **disagree** |
| n2934 | feature | 3/4 | 248.3, 2704.3 (0.3, 11.8) | 245.9, 2706.8 (0.4, 8.0) | +2.5 | -2.5 | **disagree** |
| n2934 | feature | -/2 | (none) | 168.2, 2461.6 | | | unmatched in claude |
| n2934 | trace | 12/- | 71.6, 1946.7 (0.2, 11.4) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 16/- | 85.6, 2110.6 (0.2, 8.1) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 20/- | 111.6, 2331.0 (0.1, 6.5) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 26/- | 145.2, 2435.0 (0.1, 11.7) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 34/- | 196.0, 2645.0 (0.1, 8.4) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 36/- | 199.5, 2655.4 (0.1, 13.5) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 39/- | 214.7, 2697.0 (0.2, 10.1) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 45/- | 247.1, 2705.9 (0.2, 11.8) | (no trace at this x) | | | unmatched in codex |
| n3815 | feature | 3/3 | 246.8, 3698.4 (0.3, 11.5) | 245.9, 3692.5 (0.4, 7.9) | +0.9 | +6.0 | **disagree** |
| n3815 | trace | 10/- | 73.0, 2443.5 (0.2, 13.4) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 13/- | 85.2, 2585.0 (0.2, 8.4) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 17/- | 105.8, 2811.7 (0.1, 8.5) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 20/- | 122.5, 2995.7 (0.1, 13.8) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 21/- | 125.6, 3019.9 (0.1, 17.3) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 25/- | 145.1, 3229.3 (0.1, 12.0) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 38/- | 219.2, 3677.8 (0.2, 11.5) | (no trace at this x) | | | unmatched in codex |
| n4695 | feature | 3/4 | 246.9, 4115.6 (0.4, 8.3) | 246.8, 4147.8 (0.4, 8.4) | +0.1 | -32.2 | **disagree** |
| n4695 | feature | -/3 | (none) | 233.7, 4401.3 | | | unmatched in claude |
| n4695 | marker | 4/4 | 89.1, 3208.6 (0.2, 5.1) | 89.4, 3218.5 (0.2, 4.7) | -0.2 | -9.9 | **disagree** |
| n4695 | marker | 8/8 | 167.2, 4171.9 (0.2, 4.7) | 167.8, 4171.7 (0.2, 4.8) | -0.6 | +0.2 | **disagree** |
| n4695 | marker | 9/9 | 196.7, 4387.9 (0.3, 6.6) | 197.3, 4384.2 (0.2, 5.0) | -0.6 | +3.7 | **disagree** |
| n4695 | trace | 1/- | 11.9, 1675.6 (0.2, 26.6) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 12/- | 71.6, 2997.6 (0.2, 12.1) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 15/- | 85.6, 3158.5 (0.2, 8.6) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 34/- | 201.3, 4428.1 (0.1, 8.5) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 38/- | 226.7, 4475.3 (0.2, 8.5) | (no trace at this x) | | | unmatched in codex |
| n734 | feature | 1/1 | 9.5, 228.3 (0.4, 7.6) | 11.2, 225.0 (0.3, 5.9) | -1.6 | +3.3 | **disagree** |
| n734 | feature | 3/3 | 248.3, 727.3 (0.3, 7.6) | 242.3, 696.6 (0.4, 7.6) | +5.9 | +30.7 | **disagree** |
| n734 | marker | 12/12 | 248.9, 703.8 (0.4, 7.6) | 247.0, 696.8 (0.6, 11.0) | +1.8 | +6.9 | **disagree** |
| n734 | trace | 1/- | 13.4, 226.9 (0.2, 10.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 4/- | 26.1, 338.6 (0.2, 10.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 15/- | 106.3, 676.4 (0.1, 10.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 16/- | 113.3, 688.6 (0.1, 5.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 19/- | 126.0, 709.5 (0.1, 10.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 20/- | 133.4, 718.4 (0.1, 10.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 23/- | 146.6, 739.4 (0.1, 10.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 28/- | 184.8, 743.5 (0.1, 7.6) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 29/- | 192.7, 744.0 (0.1, 10.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 37/- | 242.9, 698.4 (0.2, 10.9) | (no trace at this x) | | | unmatched in codex |
