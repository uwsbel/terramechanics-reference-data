# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b2\rederived\claude\FC-4B\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b2\rederived\codex\FC-4B\points-p1-native.csv` (codex).

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

Matched: 249; agreed 247; disagreed 2; unmatched 54 (kept as one-sided: 37 of claude, 17 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1761 | feature | 3/4 | 248.3, 1733.7 (0.5, 12.6) | 245.8, 1776.0 (0.9, 15.7) | +2.5 | -42.3 | **disagree** |
| n1761 | feature | -/2 | (none) | 169.0, 1678.4 | | | unmatched in claude |
| n1761 | trace | 4/- | 26.8, 735.3 (0.4, 21.9) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 8/- | 46.1, 955.0 (0.5, 21.9) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 9/- | 53.0, 1014.5 (0.5, 28.9) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 20/- | 112.8, 1438.2 (0.3, 22.5) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 23/- | 126.1, 1502.0 (0.3, 22.5) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 27/- | 145.6, 1585.0 (0.3, 22.6) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 37/- | 196.1, 1910.2 (0.3, 26.3) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 38/- | 202.9, 1926.1 (0.3, 22.9) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 41/- | 215.6, 1860.7 (0.3, 12.6) | (no trace at this x) | | | unmatched in codex |
| n2934 | feature | -/2 | (none) | 168.2, 2461.6 | | | unmatched in claude |
| n2934 | trace | 12/- | 71.6, 1946.7 (0.4, 22.9) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 16/- | 85.6, 2110.6 (0.3, 16.2) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 20/- | 111.6, 2331.0 (0.3, 13.1) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 26/- | 145.2, 2435.0 (0.3, 23.3) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 34/- | 196.0, 2645.0 (0.3, 16.8) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 36/- | 199.5, 2655.4 (0.3, 26.9) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 39/- | 214.7, 2697.0 (0.3, 20.2) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 45/- | 247.1, 2705.9 (0.4, 23.6) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 10/- | 73.0, 2443.5 (0.4, 26.8) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 13/- | 85.2, 2585.0 (0.3, 16.7) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 17/- | 105.8, 2811.7 (0.3, 17.0) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 20/- | 122.5, 2995.7 (0.3, 27.6) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 21/- | 125.6, 3019.9 (0.3, 34.5) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 25/- | 145.1, 3229.3 (0.3, 23.9) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 38/- | 219.2, 3677.8 (0.3, 23.0) | (no trace at this x) | | | unmatched in codex |
| n4695 | feature | -/3 | (none) | 233.7, 4401.3 | | | unmatched in claude |
| n4695 | trace | 12/- | 71.6, 2997.6 (0.4, 24.2) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 15/- | 85.6, 3158.5 (0.3, 17.1) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 34/- | 201.3, 4428.1 (0.3, 16.9) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 38/- | 226.7, 4475.3 (0.3, 17.0) | (no trace at this x) | | | unmatched in codex |
| n734 | feature | 3/3 | 248.3, 727.3 (0.5, 15.2) | 242.3, 696.6 (0.9, 15.2) | +5.9 | +30.7 | **disagree** |
| n734 | trace | 4/- | 26.1, 338.6 (0.4, 21.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 15/- | 106.3, 676.4 (0.3, 21.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 16/- | 113.3, 688.6 (0.3, 11.8) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 19/- | 126.0, 709.5 (0.3, 21.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 20/- | 133.4, 718.4 (0.3, 21.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 23/- | 146.6, 739.4 (0.3, 21.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 28/- | 184.8, 743.5 (0.3, 15.2) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 29/- | 192.7, 744.0 (0.3, 21.9) | (no trace at this x) | | | unmatched in codex |
| n734 | trace | 37/- | 242.9, 698.4 (0.4, 21.9) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
