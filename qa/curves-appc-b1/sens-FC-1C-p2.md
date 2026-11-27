# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b1\rederived\claude\FC-1C\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b1\rederived\codex\FC-1C\points-p2-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

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

Matched: 84; agreed 44; disagreed 40; unmatched 6 (kept as one-sided: 2 of claude, 1 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n1172 | marker | 5/- | 79.8, 6.2 | (none) | | | unmatched in codex |
| n1172 | marker | 6/5 | 100.2, 10.8 (0.3, 0.7) | 99.8, 13.2 (0.6, 1.2) | +0.3 | -2.5 | **disagree** |
| n1172 | marker | 7/6 | 120.5, 18.1 (0.2, 0.5) | 120.5, 19.5 (0.2, 0.5) | -0.0 | -1.4 | **disagree** |
| n1172 | marker | 8/7 | 140.6, 25.1 (0.2, 0.5) | 140.1, 26.9 (0.2, 0.5) | +0.5 | -1.8 | **disagree** |
| n1172 | marker | 9/8 | 160.4, 32.9 (0.2, 0.5) | 161.1, 34.3 (0.2, 0.5) | -0.7 | -1.4 | **disagree** |
| n1172 | marker | 10/9 | 180.6, 36.4 (0.2, 0.5) | 182.0, 37.4 (0.2, 0.5) | -1.4 | -1.1 | **disagree** |
| n1172 | marker | 11/10 | 200.0, 43.0 (0.3, 0.7) | 202.6, 45.1 (0.2, 0.5) | -2.6 | -2.1 | **disagree** |
| n1172 | marker | 12/11 | 220.5, 48.3 (0.2, 0.5) | 220.0, 49.7 (0.2, 0.5) | +0.5 | -1.4 | **disagree** |
| n1760 | marker | 2/2 | 19.9, -23.8 (0.3, 0.7) | 18.8, -24.2 (0.6, 1.2) | +1.1 | +0.3 | **disagree** |
| n1760 | marker | 10/11 | 180.2, 13.9 (0.3, 0.7) | 183.5, 14.9 (0.2, 0.5) | -3.2 | -1.1 | **disagree** |
| n1760 | marker | 11/12 | 200.1, 15.6 (0.3, 0.7) | 202.5, 16.7 (0.2, 0.5) | -2.4 | -1.1 | **disagree** |
| n1760 | marker | 12/13 | 220.8, 21.2 (0.3, 0.7) | 220.1, 20.9 (0.2, 0.5) | +0.7 | +0.4 | **disagree** |
| n1760 | marker | -/9 | (none) | 151.2, 7.2 | | | unmatched in claude |
| n2345 | marker | 4/- | 50.1, -8.9 | (none) | | | unmatched in codex |
| n2345 | marker | 2/2 | 30.0, -13.7 (0.2, 0.5) | 28.4, -14.4 (0.6, 1.2) | +1.6 | +0.7 | **disagree** |
| n2345 | marker | 5/4 | 70.8, -6.8 (0.3, 0.7) | 69.8, -7.5 (0.6, 1.2) | +1.0 | +0.7 | **disagree** |
| n2345 | marker | 6/5 | 90.7, -0.5 (0.3, 0.7) | 88.3, -1.5 (0.6, 1.2) | +2.4 | +1.0 | **disagree** |
| n2345 | marker | 7/6 | 110.6, 3.0 (0.3, 0.7) | 109.6, 2.3 (0.5, 1.0) | +1.0 | +0.7 | **disagree** |
| n2345 | marker | 8/7 | 140.7, 10.4 (0.3, 0.7) | 139.6, 10.7 (0.2, 0.5) | +1.2 | -0.4 | **disagree** |
| n2345 | marker | 10/9 | 180.1, 21.6 (0.3, 0.7) | 183.5, 21.3 (0.2, 0.5) | -3.4 | +0.4 | **disagree** |
| n2345 | marker | 11/10 | 200.0, 25.5 (0.3, 0.7) | 202.4, 26.2 (0.2, 0.5) | -2.4 | -0.7 | **disagree** |
| n2345 | marker | 13/12 | 250.1, 35.3 (0.3, 0.7) | 249.3, 35.3 (0.5, 1.0) | +0.8 | -0.0 | **disagree** |
| n2935 | marker | 4/- | 51.8, -16.2 | (none) | | | unmatched in codex |
| n2935 | marker | 5/4 | 63.6, -7.5 (0.3, 0.7) | 62.6, -7.8 (0.6, 1.2) | +1.0 | +0.3 | **disagree** |
| n2935 | marker | 8/7 | 119.6, 7.6 (0.2, 0.5) | 119.3, 8.6 (0.2, 0.5) | +0.3 | -1.1 | **disagree** |
| n2935 | marker | 9/8 | 142.5, 17.1 (0.3, 0.7) | 141.0, 16.4 (0.2, 0.5) | +1.5 | +0.7 | **disagree** |
| n2935 | marker | 10/9 | 160.7, 20.9 (0.3, 0.7) | 160.9, 22.3 (0.2, 0.5) | -0.2 | -1.4 | **disagree** |
| n2935 | marker | 11/10 | 184.0, 21.3 (0.3, 0.7) | 182.0, 21.3 (0.2, 0.5) | +2.0 | -0.0 | **disagree** |
| n2935 | marker | 13/12 | 217.2, 35.6 (0.3, 0.7) | 216.5, 36.0 (0.2, 0.5) | +0.7 | -0.4 | **disagree** |
| n294 | marker | 2/2 | 39.9, 9.0 (0.2, 0.5) | 39.2, 10.4 (0.2, 0.5) | +0.7 | -1.4 | **disagree** |
| n294 | marker | 3/3 | 59.6, 17.5 (0.2, 0.5) | 59.1, 15.7 (0.2, 0.5) | +0.5 | +1.8 | **disagree** |
| n294 | marker | 4/4 | 79.7, 28.0 (0.2, 0.5) | 79.2, 28.0 (0.2, 0.5) | +0.5 | -0.0 | **disagree** |
| n294 | marker | 6/6 | 120.0, 51.5 (0.2, 0.5) | 120.6, 51.9 (0.2, 0.5) | -0.5 | -0.4 | **disagree** |
| n3520 | marker | 3/5 | 70.8, -13.7 (0.3, 0.7) | 69.6, -10.6 (0.6, 1.2) | +1.2 | -3.1 | **disagree** |
| n3520 | marker | 4/6 | 90.7, -7.8 (0.3, 0.7) | 89.5, -9.6 (0.6, 1.2) | +1.2 | +1.7 | **disagree** |
| n3520 | marker | 5/7 | 110.8, -5.0 (0.3, 0.7) | 109.6, -5.0 (0.2, 0.5) | +1.2 | -0.0 | **disagree** |
| n3520 | marker | 7/9 | 150.5, 3.4 (0.3, 0.7) | 149.3, 3.7 (0.7, 1.6) | +1.2 | -0.4 | **disagree** |
| n3520 | marker | 8/10 | 170.7, 3.3 (0.3, 0.7) | 170.1, 4.8 (0.2, 0.5) | +0.7 | -1.4 | **disagree** |
| n3520 | marker | -/1 | (none) | 0.4, -4.0 | | | unmatched in claude |
| n3520 | marker | -/4 | (none) | 51.8, -16.2 | | | unmatched in claude |
| n587 | marker | 3/3 | 30.0, 4.8 (0.3, 0.7) | 29.5, 2.7 (0.5, 1.0) | +0.5 | +2.1 | **disagree** |
| n587 | marker | 5/5 | 69.9, 20.3 (0.2, 0.5) | 69.7, 18.5 (0.2, 0.5) | +0.2 | +1.8 | **disagree** |
| n587 | marker | 7/7 | 109.9, 39.6 (0.2, 0.5) | 109.9, 38.5 (0.2, 0.5) | +0.0 | +1.1 | **disagree** |
| n587 | marker | 10/10 | 170.0, 72.9 (0.2, 0.5) | 170.0, 70.8 (0.2, 0.5) | -0.0 | +2.1 | **disagree** |
| n587 | marker | 11/11 | 189.4, 81.3 (0.2, 0.5) | 189.0, 79.9 (0.2, 0.5) | +0.3 | +1.4 | **disagree** |
| n587 | marker | 13/13 | 230.8, 95.6 (0.3, 0.7) | 230.3, 93.5 (0.2, 0.5) | +0.5 | +2.1 | **disagree** |
| n2935 | marker | 4 (claude) | 51.8, -16.2 | codex: n3520 (x) | | | **identity conflict** |
| n3520 | marker | 1 (codex) | 0.4, -4.0 | claude: n587 (triangle-up) | | | **identity conflict** |
| n3520 | marker | 4 (codex) | 51.8, -16.2 | claude: n2935 (asterisk) | | | **identity conflict** |
