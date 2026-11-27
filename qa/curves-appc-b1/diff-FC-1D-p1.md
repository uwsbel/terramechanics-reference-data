# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-1D\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-1D\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 42 | 42 |
| x per px | 0.1708 | 0.1708 |
| y per px | 3.4551 | 3.4528 |
| RMS residual x, y | 0.345, 7.161 | 0.343, 5.705 |

Corners of claude's box [530, 1120, 2110, 2950] mapped by both calibrations (tolerance 0.86 in x, 16.32 in y):

- (-3.6, 6191.3) vs (-3.6, 6194.0)
- (266.2, 6101.5) vs (266.2, 6096.2)
- (-10.1, -130.7) vs (-10.1, -123.6)
- (259.7, -220.5) vs (259.6, -221.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.73 | 0.46 | 0.33 | 18 | 0.83 | 0.93 | agree |
| x | 50 | 1.36 | 0.10 | 0.38 | 17 | 2.00 | 0.83 | agree |
| x | 100 | 0.23 | 0.12 | 0.16 | 18 | 0.50 | 0.55 | agree |
| x | 150 | 0.20 | 0.15 | 0.17 | 18 | 1.22 | 1.11 | agree |
| x | 200 | 0.78 | 0.32 | 0.19 | 18 | 1.47 | 0.69 | agree |
| x | 250 | 0.89 | 0.28 | 0.49 | 18 | 0.98 | 0.96 | agree |
| y | 0 | 0.16 | 0.24 | 0.30 | 15 | 0.50 | 0.50 | agree |
| y | 1000 | 0.10 | 0.39 | 0.45 | 25 | 1.33 | 0.61 | agree |
| y | 2000 | 0.33 | 0.51 | 0.44 | 15 | 0.75 | 0.77 | agree |
| y | 3000 | 0.26 | 0.31 | 0.37 | 15 | 1.28 | 1.07 | agree |
| y | 4000 | 1.02 | 0.38 | 0.80 | 15 | 1.34 | 2.20 | agree |
| y | 5000 | 0.07 | 0.36 | 0.36 | 25 | 0.59 | 0.60 | agree |
| y | 6000 | 0.25 | 0.24 | 0.21 | 15 | 0.73 | 0.79 | agree |

Both maps along every verified line and every interval midline (262 places): largest difference 0.1986 in x (tolerance 0.4955, claude 50), 3.269 in y (tolerance 12.37, codex 4000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 13 shared lines checked against the ink, mean of the median distances 0.30 px (claude: x 0.24, y 0.35), 0.36 px (codex: x 0.28, y 0.42), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

7 series in claude, 7 in codex.


## Points

Matched: 327; agreed 319; disagreed 8; unmatched 84 (kept as one-sided: 20 of claude, 64 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n0 | trace | 4/- | 37.8, 419.5 (1.4, 23.9) | (no trace at this x) | | | unmatched in codex |
| n0 | trace | 7/- | 55.3, 457.2 (1.3, 24.0) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 5/- | 32.2, 2098.8 (1.3, 24.0) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 16/- | 87.6, 2645.3 (1.0, 21.5) | (no trace at this x) | | | unmatched in codex |
| n1468 | trace | 25/- | 142.8, 2614.0 (1.1, 21.4) | (no trace at this x) | | | unmatched in codex |
| n2345 | feature | 1/1 | 18.5, 2603.1 (0.9, 17.9) | 21.7, 2683.8 (1.0, 21.0) | -3.2 | -80.7 | **disagree** |
| n2345 | trace | 16/- | 94.6, 3841.0 (1.1, 25.9) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 19/- | 115.0, 3834.9 (1.2, 25.9) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 37/- | 217.6, 3211.3 (1.3, 25.8) | (no trace at this x) | | | unmatched in codex |
| n2345 | trace | 38/- | 224.8, 3144.1 (1.4, 29.3) | (no trace at this x) | | | unmatched in codex |
| n2935 | marker | 1/1 | 10.7, 2507.0 (0.5, 10.6) | 12.4, 2513.8 (0.9, 17.3) | -1.7 | -6.8 | **disagree** |
| n2935 | marker | 2/2 | 29.9, 3425.3 (0.6, 11.6) | 31.6, 3435.1 (0.9, 19.7) | -1.7 | -9.8 | **disagree** |
| n2935 | marker | 4/4 | 90.4, 4487.6 (0.5, 10.2) | 92.1, 4487.4 (0.8, 18.6) | -1.7 | +0.2 | **disagree** |
| n2935 | marker | 5/5 | 110.4, 4514.0 (0.5, 10.1) | 111.8, 4520.8 (0.8, 18.4) | -1.4 | -6.8 | **disagree** |
| n2935 | marker | 6/6 | 130.9, 4439.4 (0.5, 10.3) | 132.4, 4453.2 (0.9, 18.7) | -1.5 | -13.8 | **disagree** |
| n2935 | marker | 8/8 | 179.7, 4186.2 (0.6, 10.9) | 181.2, 4191.0 (0.8, 20.1) | -1.5 | -4.8 | **disagree** |
| n2935 | trace | 18/- | 94.5, 4492.5 (1.1, 23.9) | (no trace at this x) | | | unmatched in codex |
| n2935 | trace | 26/- | 135.3, 4425.4 (0.9, 17.2) | (no trace at this x) | | | unmatched in codex |
| n2935 | trace | 33/- | 175.2, 4191.5 (1.3, 24.6) | (no trace at this x) | | | unmatched in codex |
| n2935 | trace | 37/- | 194.8, 4094.2 (1.4, 28.3) | (no trace at this x) | | | unmatched in codex |
| n294 | marker | -/3 | (none) | 41.4, 929.5 | | | unmatched in claude |
| n294 | trace | 1/- | 7.3, 444.2 (0.9, 17.0) | (no trace at this x) | | | unmatched in codex |
| n3520 | trace | 9/- | 52.3, 4340.5 (1.0, 17.4) | (no trace at this x) | | | unmatched in codex |
| n3520 | trace | 13/- | 68.5, 4631.1 (0.9, 16.7) | (no trace at this x) | | | unmatched in codex |
| n3520 | trace | 17/- | 87.6, 4874.7 (1.0, 19.5) | (no trace at this x) | | | unmatched in codex |
| n587 | feature | 2/2 | 89.8, 1487.1 (1.0, 21.4) | 81.8, 1432.3 (1.1, 23.6) | +7.9 | +54.8 | **disagree** |
| n587 | trace | 1/- | 10.6, 802.4 (1.1, 21.5) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 9/- | 48.2, 1355.5 (1.0, 18.1) | (no trace at this x) | | | unmatched in codex |
| n587 | trace | 30/- | 165.1, 1125.7 (1.1, 22.1) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 129 trace samples excluded

Overrides of hand decisions (1), for review:

- claude n1468 trace 29: hand decision resolved use codex (the other reading is on the line's ink and the kept one is not; credit codex (audit re-check 2026-10)
