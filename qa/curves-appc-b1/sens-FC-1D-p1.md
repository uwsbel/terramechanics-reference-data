# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-1D\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-1D\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

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

Matched: 364; agreed 342; disagreed 22; unmatched 34 (kept as one-sided: 4 of claude, 30 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n0 | feature | 3/3 | 145.7, 336.6 (0.5, 10.1) | 144.6, 338.1 (0.5, 9.6) | +1.1 | -1.6 | **disagree** |
| n0 | trace | 21/- | 145.2, 339.1 (0.6, 11.8) | (no trace at this x) | | | unmatched in codex |
| n1468 | feature | 1/1 | 10.5, 1325.6 (0.4, 9.1) | 10.5, 1346.6 (0.5, 10.0) | -0.0 | -21.0 | **disagree** |
| n1468 | feature | 3/3 | 248.4, 2117.2 (0.5, 10.2) | 249.9, 2111.3 (0.5, 10.2) | -1.5 | +6.0 | **disagree** |
| n2345 | feature | 1/1 | 18.5, 2603.1 (0.5, 8.9) | 21.7, 2683.8 (0.5, 10.5) | -3.2 | -80.7 | **disagree** |
| n2345 | feature | 3/3 | 249.3, 2929.9 (0.5, 11.0) | 250.8, 2945.6 (0.5, 10.6) | -1.5 | -15.8 | **disagree** |
| n2345 | trace | 1/- | 19.8, 2657.2 (0.6, 12.5) | (no trace at this x) | | | unmatched in codex |
| n2935 | marker | 1/1 | 10.7, 2507.0 (0.3, 5.3) | 12.4, 2513.8 (0.4, 8.7) | -1.7 | -6.8 | **disagree** |
| n2935 | marker | 2/2 | 29.9, 3425.3 (0.3, 5.8) | 31.6, 3435.1 (0.4, 9.9) | -1.7 | -9.8 | **disagree** |
| n2935 | marker | 3/3 | 70.3, 4287.8 (0.3, 5.3) | 71.7, 4289.4 (0.4, 9.8) | -1.4 | -1.7 | **disagree** |
| n2935 | marker | 4/4 | 90.4, 4487.6 (0.2, 5.1) | 92.1, 4487.4 (0.4, 9.3) | -1.7 | +0.2 | **disagree** |
| n2935 | marker | 5/5 | 110.4, 4514.0 (0.2, 5.0) | 111.8, 4520.8 (0.4, 9.2) | -1.4 | -6.8 | **disagree** |
| n2935 | marker | 6/6 | 130.9, 4439.4 (0.3, 5.1) | 132.4, 4453.2 (0.4, 9.4) | -1.5 | -13.8 | **disagree** |
| n2935 | marker | 7/7 | 150.4, 4341.6 (0.5, 7.0) | 151.6, 4345.8 (0.5, 11.4) | -1.2 | -4.2 | **disagree** |
| n2935 | marker | 8/8 | 179.7, 4186.2 (0.3, 5.5) | 181.2, 4191.0 (0.4, 10.1) | -1.5 | -4.8 | **disagree** |
| n2935 | marker | 9/9 | 199.9, 4071.2 (0.5, 7.3) | 201.4, 4086.7 (0.5, 12.0) | -1.5 | -15.5 | **disagree** |
| n2935 | marker | 10/10 | 250.6, 3898.3 (0.4, 9.4) | 252.1, 3901.1 (0.4, 10.8) | -1.5 | -2.8 | **disagree** |
| n2935 | trace | 1/- | 11.2, 2570.0 (0.4, 8.9) | (no trace at this x) | | | unmatched in codex |
| n2935 | trace | 2/interp | 15.0, 2770.3 (0.5, 10.9) | 15.0, 2712.0 (0.2, 28.6) | slope +22.5 | +58.4 (tol 56.1) | **disagree** |
| n294 | feature | 3/3 | 159.6, 686.1 (0.5, 10.6) | 162.0, 702.2 (0.5, 9.7) | -2.3 | -16.1 | **disagree** |
| n294 | marker | -/3 | (none) | 41.4, 929.5 | | | unmatched in claude |
| n3520 | feature | 3/3 | 251.6, 4136.3 (0.5, 10.7) | 252.0, 4113.1 (0.5, 12.0) | -0.4 | +23.1 | **disagree** |
| n3520 | trace | 27/interp | 148.0, 4948.3 (0.7, 13.1) | 148.0, 4995.8 (0.2, 29.0) | slope +2.8 | -47.5 (tol 44.7) | **disagree** |
| n587 | feature | 3/3 | 252.2, 893.1 (0.5, 10.9) | 248.7, 918.5 (0.5, 9.8) | +3.5 | -25.4 | **disagree** |
| n587 | feature | 2/2 | 89.8, 1487.1 (0.5, 10.7) | 81.8, 1432.3 (0.6, 11.8) | +7.9 | +54.8 | **disagree** |
| n587 | marker | 11/11 | 221.0, 914.6 (0.4, 7.4) | 221.0, 931.6 (0.4, 8.0) | -0.1 | -17.0 | **disagree** |
| n587 | trace | 43/- | 248.2, 933.6 (0.6, 12.7) | (no trace at this x) | | | unmatched in codex |
