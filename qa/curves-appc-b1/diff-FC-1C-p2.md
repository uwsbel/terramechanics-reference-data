# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-1C\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-1C\points-p2-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 18 | 18 |
| x per px | 0.1707 | 0.1707 |
| y per px | 0.3501 | 0.3500 |
| RMS residual x, y | 0.370, 0.217 | 0.370, 0.223 |

Corners of claude's box [600, 2965, 2120, 3590] mapped by both calibrations (tolerance 0.91 in x, 0.79 in y):

- (-5.1, 109.1) vs (-5.1, 109.1)
- (254.3, 108.9) vs (254.4, 108.9)
- (-5.6, -109.7) vs (-5.7, -109.7)
- (253.8, -109.9) vs (253.8, -109.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.90 | 0.40 | 0.11 | 6 | 0.63 | 0.65 | agree |
| x | 50 | 0.10 | 0.30 | 0.27 | 6 | 0.56 | 0.50 | agree |
| x | 100 | 0.10 | 0.28 | 0.29 | 6 | 0.82 | 0.71 | agree |
| x | 150 | 0.25 | 0.35 | 0.26 | 6 | 0.85 | 0.56 | agree |
| x | 200 | 0.07 | 0.28 | 0.32 | 6 | 0.64 | 0.75 | agree |
| x | 250 | 0.35 | 0.23 | 0.22 | 6 | 0.50 | 0.50 | agree |
| y | -100 | 0.16 | 0.10 | 0.11 | 15 | 0.80 | 0.64 | agree |
| y | 0 | 0.00 | 0.10 | 0.10 | 15 | 0.91 | 0.91 | agree |
| y | 100 | 0.04 | 0.34 | 0.34 | 15 | 0.69 | 0.74 | agree |

Both maps along every verified line and every interval midline (206 places): largest difference 0.1543 in x (tolerance 0.2186, claude 0), 0.0597 in y (tolerance 0.6345, codex -100); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.26 px (claude: x 0.30, y 0.18), 0.23 px (codex: x 0.25, y 0.18), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

7 series in claude, 7 in codex.


## Points

Matched: 84; agreed 71; disagreed 13; unmatched 3 (kept as one-sided: 2 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1172 | marker | 5/- | 79.8, 6.2 | (none) | | | unmatched in codex |
| n1172 | marker | 10/9 | 180.6, 36.4 (0.5, 1.0) | 182.0, 37.4 (0.5, 1.0) | -1.4 | -1.1 | **disagree** |
| n1172 | marker | 11/10 | 200.0, 43.0 (0.6, 1.3) | 202.6, 45.1 (0.5, 1.0) | -2.6 | -2.1 | **disagree** |
| n1760 | marker | 10/11 | 180.2, 13.9 (0.6, 1.4) | 183.5, 14.9 (0.5, 1.0) | -3.2 | -1.1 | **disagree** |
| n1760 | marker | 11/12 | 200.1, 15.6 (0.6, 1.4) | 202.5, 16.7 (0.5, 1.0) | -2.4 | -1.1 | **disagree** |
| n2345 | marker | 4/- | 50.1, -8.9 | (none) | | | unmatched in codex |
| n2345 | marker | 2/2 | 30.0, -13.7 (0.4, 1.0) | 28.4, -14.4 (1.1, 2.4) | +1.6 | +0.7 | **disagree** |
| n2345 | marker | 6/5 | 90.7, -0.5 (0.6, 1.4) | 88.3, -1.5 (1.1, 2.4) | +2.4 | +1.0 | **disagree** |
| n2345 | marker | 8/7 | 140.7, 10.4 (0.7, 1.4) | 139.6, 10.7 (0.4, 1.0) | +1.2 | -0.4 | **disagree** |
| n2345 | marker | 10/9 | 180.1, 21.6 (0.6, 1.4) | 183.5, 21.3 (0.5, 1.0) | -3.4 | +0.4 | **disagree** |
| n2345 | marker | 11/10 | 200.0, 25.5 (0.6, 1.4) | 202.4, 26.2 (0.5, 1.0) | -2.4 | -0.7 | **disagree** |
| n2935 | marker | 9/8 | 142.5, 17.1 (0.7, 1.4) | 141.0, 16.4 (0.4, 1.0) | +1.5 | +0.7 | **disagree** |
| n2935 | marker | 11/10 | 184.0, 21.3 (0.6, 1.4) | 182.0, 21.3 (0.5, 1.0) | +2.0 | -0.0 | **disagree** |
| n3520 | marker | 5/7 | 110.8, -5.0 (0.7, 1.4) | 109.6, -5.0 (0.5, 1.0) | +1.2 | -0.0 | **disagree** |
| n3520 | marker | -/4 | (none) | 51.8, -16.2 | | | unmatched in claude |
| n587 | marker | 10/10 | 170.0, 72.9 (0.5, 1.0) | 170.0, 70.8 (0.4, 1.0) | -0.0 | +2.1 | **disagree** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
