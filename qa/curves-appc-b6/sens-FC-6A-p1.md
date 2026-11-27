# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b6\rederived\claude\FC-6A\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b6\rederived\codex\FC-6A\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 42 | 42 |
| x per px | 3.4100 | 3.4094 |
| y per px | 3.3999 | 3.3996 |
| RMS residual x, y | 3.396, 6.092 | 3.040, 6.328 |

Corners of claude's box [895, 1215, 2425, 3025] mapped by both calibrations (tolerance 9.85 in x, 15.82 in y):

- (-65.7, 6092.1) vs (-63.9, 6091.7)
- (5151.3, 6048.8) vs (5152.1, 6047.7)
- (-135.0, -61.4) vs (-135.2, -61.3)
- (5082.0, -104.7) vs (5080.8, -105.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.55 | 0.40 | 0.34 | 18 | 0.72 | 0.93 | agree |
| x | 1000 | 1.02 | 0.51 | 0.19 | 16 | 0.99 | 0.83 | agree |
| x | 2000 | 0.85 | 0.26 | 0.19 | 15 | 0.81 | 0.85 | agree |
| x | 3000 | 0.12 | 0.40 | 0.44 | 15 | 1.31 | 1.24 | agree |
| x | 4000 | 0.19 | 0.19 | 0.19 | 15 | 0.74 | 0.66 | agree |
| x | 5000 | 0.02 | 0.40 | 0.39 | 18 | 0.96 | 0.98 | agree |
| y | 0 | 0.48 | 0.26 | 0.35 | 15 | 0.95 | 0.50 | agree |
| y | 1000 | 0.35 | 0.59 | 0.72 | 15 | 0.93 | 1.26 | agree |
| y | 2000 | 0.53 | 0.40 | 0.41 | 15 | 1.02 | 0.59 | agree |
| y | 3000 | 0.58 | 0.51 | 0.36 | 15 | 0.95 | 0.79 | agree |
| y | 4000 | 0.38 | 0.22 | 0.33 | 15 | 0.72 | 0.58 | agree |
| y | 5000 | 0.03 | 0.57 | 0.54 | 19 | 0.82 | 0.96 | agree |
| y | 6000 | 0.28 | 0.38 | 0.48 | 15 | 0.86 | 0.89 | agree |

Both maps along every verified line and every interval midline (266 places): largest difference 3.036 in x (tolerance 6.252, claude 1000), 1.704 in y (tolerance 6.191, codex 3000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 13 shared lines checked against the ink, mean of the median distances 0.39 px (claude: x 0.36, y 0.42), 0.38 px (codex: x 0.29, y 0.46), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

3 series in claude, 4 in codex.
Only in codex: FC-6A/1/


## Points

Matched: 73; agreed 71; disagreed 2; unmatched 9 (kept as one-sided: 3 of claude, 4 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
|  | marker | -/1 | (none) | 2946.3, 2894.4 | | | unmatched in claude |
| dr103-107 | marker | 5/5 | 4663.3, 4068.9 (5.0, 4.6) | 4660.2, 4052.6 (4.9, 4.4) | +3.1 | +16.4 | **disagree** |
| dr103-107 | trace | 1/- | 43.0, 0.3 (8.1, 10.2) | (no trace at this x) | | | unmatched in codex |
| dr19-28 | marker | 3/- | 2930.7, 2877.8 | (none) | | | unmatched in codex |
| dr19-28 | marker | 6/- | -141.2, -156.5 | (none) | | | unmatched in codex |
| dr5-40 | marker | 5/5 | 4586.2, 4554.2 (6.7, 11.5) | 4570.6, 4553.2 (6.7, 13.2) | +15.6 | +1.0 | **disagree** |
| dr5-40 | trace | 1/- | 2.5, -9.9 (9.8, 10.2) | (no trace at this x) | | | unmatched in codex |
|  | marker | 1 (codex) | 2946.3, 2894.4 | claude: dr19-28 (circle) | | | **identity conflict** |
| dr19-28 | marker | 3 (claude) | 2930.7, 2877.8 | codex:  (triangle-down) | | | **identity conflict** |
