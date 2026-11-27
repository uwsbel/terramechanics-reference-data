# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b2\rederived\claude\FC-4C\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b2\rederived\codex\FC-4C\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 30 | 30 |
| x per px | 0.1719 | 0.1719 |
| y per px | 6.8590 | 6.8594 |
| RMS residual x, y | 0.462, 12.097 | 0.462, 13.245 |

Corners of claude's box [740, 1317, 2250, 2520] mapped by both calibrations (tolerance 1.10 in x, 32.20 in y):

- (-3.6, 8046.8) vs (-3.6, 8048.6)
- (255.9, 8008.6) vs (255.9, 8008.9)
- (-5.4, -204.5) vs (-5.4, -203.2)
- (254.1, -242.7) vs (254.1, -242.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.15 | 0.27 | 0.31 | 12 | 1.11 | 1.14 | agree |
| x | 50 | 0.09 | 0.38 | 0.35 | 11 | 0.62 | 0.75 | agree |
| x | 100 | 0.17 | 0.24 | 0.27 | 12 | 0.69 | 0.70 | agree |
| x | 150 | 0.25 | 0.49 | 0.46 | 12 | 0.86 | 0.59 | agree |
| x | 200 | 0.18 | 0.20 | 0.21 | 12 | 0.50 | 0.50 | agree |
| x | 250 | 0.27 | 0.28 | 0.24 | 12 | 0.74 | 0.66 | agree |
| y | 0 | 0.11 | 0.34 | 0.34 | 15 | 0.63 | 0.55 | agree |
| y | 2000 | 0.00 | 0.22 | 0.22 | 15 | 0.61 | 0.61 | agree |
| y | 4000 | 0.49 | 0.78 | 0.64 | 15 | 1.34 | 1.26 | agree |
| y | 6000 | 0.17 | 0.49 | 0.42 | 15 | 0.90 | 0.91 | agree |
| y | 8000 | 0.63 | 0.95 | 0.85 | 15 | 1.75 | 1.51 | agree |

Both maps along every verified line and every interval midline (234 places): largest difference 0.05479 in x (tolerance 0.2466, codex 250), 3.604 in y (tolerance 22.46, claude 8000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 11 shared lines checked against the ink, mean of the median distances 0.42 px (claude: x 0.31, y 0.56), 0.39 px (codex: x 0.31, y 0.49), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

5 series in claude, 5 in codex.


## Points

Matched: 244; agreed 232; disagreed 12; unmatched 91 (kept as one-sided: 59 of claude, 32 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1761 | feature | 1/1 | 14.2, 2849.1 (0.3, 45.3) | 9.1, 2161.9 (0.4, 12.9) | +5.1 | +687.2 | **disagree** |
| n1761 | feature | 3/4 | 245.7, 2186.3 (0.3, 12.9) | 246.7, 2168.9 (0.5, 19.9) | -1.0 | +17.4 | **disagree** |
| n1761 | feature | -/3 | (none) | 211.6, 2174.0 | | | unmatched in claude |
| n1761 | trace | 3/- | 26.0, 3626.4 (0.3, 32.3) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 5/- | 36.0, 3977.7 (0.2, 53.5) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 7/- | 45.6, 4234.0 (0.2, 24.7) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 9/- | 55.2, 4381.4 (0.2, 21.2) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 11/- | 65.4, 4352.8 (0.2, 24.6) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 13/- | 75.2, 4016.5 (0.2, 56.7) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 17/- | 95.3, 3371.3 (0.2, 24.9) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 21/- | 115.3, 2928.2 (0.2, 20.9) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 27/- | 144.7, 2515.3 (0.3, 23.8) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 31/- | 165.8, 2281.7 (0.2, 13.0) | (no trace at this x) | | | unmatched in codex |
| n1761 | trace | 37/- | 202.2, 2213.5 (0.2, 12.9) | (no trace at this x) | | | unmatched in codex |
| n2934 | feature | 1/1 | 11.4, 3660.1 (0.4, 56.8) | 8.6, 3253.9 (0.4, 14.1) | +2.8 | +406.2 | **disagree** |
| n2934 | feature | 3/3 | 245.7, 3003.1 (0.3, 24.5) | 246.9, 3000.8 (0.7, 27.9) | -1.2 | +2.3 | **disagree** |
| n2934 | trace | 3/- | 22.8, 4616.3 (0.3, 34.6) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 7/- | 45.6, 5593.6 (0.2, 23.7) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 8/- | 52.6, 5693.9 (0.2, 23.6) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 9/- | 57.5, 5639.0 (0.2, 30.4) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 11/- | 65.1, 5610.8 (0.2, 23.7) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 18/- | 104.6, 4590.3 (0.2, 24.4) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 22/- | 129.5, 4187.6 (0.2, 11.2) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 25/- | 142.1, 4003.1 (0.3, 39.5) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 30/- | 177.2, 3551.0 (0.2, 67.2) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 34/- | 195.1, 3398.1 (0.2, 28.5) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 38/- | 217.5, 3206.2 (0.2, 21.2) | (no trace at this x) | | | unmatched in codex |
| n2934 | trace | 42/- | 240.4, 3014.4 (0.2, 21.0) | (no trace at this x) | | | unmatched in codex |
| n3815 | feature | 1/1 | 12.4, 5169.2 (0.4, 64.7) | 8.9, 4454.9 (0.4, 14.2) | +3.6 | +714.2 | **disagree** |
| n3815 | feature | 3/4 | 245.0, 3226.6 (0.3, 24.7) | 248.7, 3245.2 (0.7, 28.2) | -3.7 | -18.5 | **disagree** |
| n3815 | feature | -/3 | (none) | 51.5, 6214.6 | | | unmatched in claude |
| n3815 | feature | 2/2 | 37.0, 7188.4 (0.6, 25.6) | 38.5, 7126.5 (1.8, 28.8) | -1.5 | +61.9 | **disagree** |
| n3815 | trace | 4/- | 25.4, 6621.6 (0.3, 35.1) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 6/- | 39.4, 7124.8 (0.2, 35.8) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 8/- | 49.7, 6566.1 (0.2, 62.6) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 11/- | 69.8, 5048.7 (0.2, 27.5) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 13/- | 79.3, 4621.2 (0.2, 21.0) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 15/- | 85.1, 4437.7 (0.2, 27.9) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 19/- | 106.9, 3980.7 (0.2, 46.5) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 27/- | 154.8, 3592.8 (0.2, 28.7) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 34/- | 194.8, 3387.7 (0.2, 38.9) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 38/- | 215.1, 3220.6 (0.2, 35.2) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 39/- | 222.6, 3278.8 (0.2, 38.8) | (no trace at this x) | | | unmatched in codex |
| n3815 | trace | 42/- | 237.9, 3245.1 (0.2, 28.3) | (no trace at this x) | | | unmatched in codex |
| n4695 | feature | 1/1 | 19.9, 5800.5 (0.3, 43.9) | 7.6, 4914.1 (0.4, 13.9) | +12.3 | +886.4 | **disagree** |
| n4695 | feature | -/3 | (none) | 184.4, 5042.5 | | | unmatched in claude |
| n4695 | trace | 13/- | 92.4, 5941.3 (0.2, 9.9) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 17/- | 114.6, 5511.8 (0.2, 20.4) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 23/- | 152.2, 5124.0 (0.2, 24.0) | (no trace at this x) | | | unmatched in codex |
| n4695 | trace | 29/- | 185.5, 5051.3 (0.2, 27.5) | (no trace at this x) | | | unmatched in codex |
| n741 | feature | 1/1 | 10.9, 1319.8 (0.3, 32.8) | 8.2, 1225.2 (0.4, 12.2) | +2.8 | +94.6 | **disagree** |
| n741 | feature | 3/3 | 243.1, 757.5 (0.3, 15.7) | 244.6, 736.8 (0.5, 19.0) | -1.5 | +20.6 | **disagree** |
| n741 | marker | 16/16 | 187.6, 781.8 (0.2, 8.9) | 187.6, 761.5 (0.2, 8.8) | +0.0 | +20.3 | **disagree** |
| n741 | marker | 17/17 | 217.8, 742.4 (0.2, 8.9) | 217.9, 723.4 (0.2, 8.8) | -0.1 | +19.0 | **disagree** |
| n741 | trace | 2/- | 23.1, 2082.7 (0.3, 30.3) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 3/- | 25.4, 2166.2 (0.2, 19.9) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 5/- | 35.7, 2514.0 (0.2, 27.3) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 10/- | 66.0, 1955.3 (0.2, 57.6) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 12/- | 75.9, 1617.0 (0.2, 25.9) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 13/- | 82.2, 1449.4 (0.2, 22.5) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 14/- | 86.1, 1380.8 (0.2, 25.9) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 15/- | 92.0, 1277.9 (0.2, 25.9) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 16/- | 95.6, 1253.6 (0.2, 8.9) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 17/- | 101.9, 1181.2 (0.2, 22.5) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 18/- | 105.2, 1170.6 (0.2, 19.1) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 20/- | 114.9, 1077.4 (0.2, 22.5) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 21/- | 122.0, 1022.0 (0.2, 22.5) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 22/- | 125.0, 1008.0 (0.2, 15.7) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 23/- | 132.4, 956.0 (0.2, 12.3) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 26/- | 144.7, 899.9 (0.2, 8.9) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 27/- | 152.1, 868.2 (0.2, 22.5) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 30/- | 165.1, 818.9 (0.2, 15.7) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 38/- | 212.5, 737.7 (0.2, 22.5) | (no trace at this x) | | | unmatched in codex |
| n741 | trace | 43/- | 243.1, 757.5 (0.2, 15.7) | (no trace at this x) | | | unmatched in codex |
