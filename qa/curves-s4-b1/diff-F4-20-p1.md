# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s4-b1\rederived\claude\F4-20\points-p1-native.csv` (claude), `<repository>\qa\curves-s4-b1\rederived\codex\F4-20\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 130 | 130 |
| x per px | 0.0016 | 0.0016 |
| y per px | 0.3237 | 0.3237 |
| RMS residual x, y | 0.002, 0.356 | 0.002, 0.356 |

Corners of claude's box [405, 995, 2305, 3835] mapped by both calibrations (tolerance 0.01 in x, 1.04 in y):

- (4.6, 595.7) vs (4.6, 595.7)
- (4.5, -19.3) vs (4.5, -19.3)
- (-0.0, 608.7) vs (-0.0, 608.7)
- (-0.1, -6.3) vs (-0.1, -6.3)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.09 | 0.33 | 0.33 | 25 | 1.09 | 1.01 | agree |
| x | 0.5 | 0.07 | 0.48 | 0.48 | 24 | 0.81 | 0.72 | agree |
| x | 1 | 0.09 | 0.35 | 0.38 | 25 | 1.00 | 0.61 | agree |
| x | 1.5 | 0.06 | 0.35 | 0.36 | 25 | 0.79 | 0.76 | agree |
| x | 2 | 0.17 | 0.44 | 0.47 | 25 | 0.93 | 1.08 | agree |
| x | 2.5 | 0.02 | 0.16 | 0.16 | 20 | 0.51 | 0.52 | agree |
| x | 3 | 0.27 | 0.28 | 0.31 | 21 | 0.56 | 0.69 | agree |
| x | 3.5 | 0.04 | 0.55 | 0.56 | 18 | 1.05 | 0.98 | agree |
| x | 4 | 0.20 | 0.60 | 0.62 | 20 | 0.93 | 1.07 | agree |
| x | 4.5 | 0.09 | 0.26 | 0.27 | 25 | 0.61 | 0.71 | agree |
| y | 0 | 0.03 | 0.41 | 0.41 | 25 | 0.64 | 0.57 | agree |
| y | 50 | 0.02 | 0.37 | 0.35 | 22 | 0.60 | 0.57 | agree |
| y | 100 | 0.06 | 0.28 | 0.24 | 25 | 0.58 | 0.50 | agree |
| y | 150 | 0.05 | 0.33 | 0.34 | 25 | 0.52 | 0.50 | agree |
| y | 200 | 0.05 | 0.20 | 0.20 | 25 | 0.62 | 0.56 | agree |
| y | 250 | 0.04 | 0.36 | 0.36 | 25 | 0.58 | 0.59 | agree |
| y | 300 | 0.05 | 0.17 | 0.15 | 25 | 0.52 | 0.50 | agree |
| y | 350 | 0.02 | 0.25 | 0.24 | 25 | 0.50 | 0.50 | agree |
| y | 400 | 0.02 | 0.19 | 0.17 | 25 | 0.50 | 0.50 | agree |
| y | 450 | 0.03 | 0.36 | 0.37 | 21 | 0.50 | 0.51 | agree |
| y | 500 | 0.16 | 0.27 | 0.31 | 20 | 1.28 | 1.45 | agree |
| y | 550 | 0.07 | 0.33 | 0.31 | 25 | 0.53 | 0.62 | agree |
| y | 600 | 0.03 | 0.40 | 0.41 | 25 | 0.60 | 0.58 | agree |

Both maps along every verified line and every interval midline (463 places): largest difference 0.0003492 in x (tolerance 0.0028, codex 3), 0.04369 in y (tolerance 0.8841, codex 500); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 23 shared lines checked against the ink, mean of the median distances 0.34 px (claude: x 0.38, y 0.30), 0.34 px (codex: x 0.39, y 0.30), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 128; agreed 125; disagreed 3; unmatched 28 (kept as one-sided: 9 of claude, 19 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| run10 | feature | -/4 | (none) | 0.9, 149.1 | | | unmatched in claude |
| run10 | trace | 22/- | 1.2, 116.9 (0.0, 2.0) | (no trace at this x) | | | unmatched in codex |
| run10 | trace | 23/- | 1.3, 98.8 (0.0, 2.3) | (no trace at this x) | | | unmatched in codex |
| run12 | feature | -/3 | (none) | 0.5, 544.3 | | | unmatched in claude |
| run12 | trace | 14/- | 0.2, 498.7 (0.0, 3.8) | (no trace at this x) | | | unmatched in codex |
| run12 | trace | 18/- | 0.4, 591.2 (0.0, 2.8) | (no trace at this x) | | | unmatched in codex |
| run12 | trace | 19/- | 0.5, 553.1 (0.0, 3.5) | (no trace at this x) | | | unmatched in codex |
| run12 | trace | 33/- | 0.8, 28.2 (0.0, 3.3) | (no trace at this x) | | | unmatched in codex |
| run12 | trace | 34/- | 0.8, 8.4 (0.0, 1.8) | (no trace at this x) | | | unmatched in codex |
| run12 | trace | 37/- | 1.0, 13.9 (0.0, 2.6) | (no trace at this x) | | | unmatched in codex |
| run12 | trace | 39/- | 1.1, 50.1 (0.0, 3.8) | (no trace at this x) | | | unmatched in codex |
| run4 | feature | 50/6 | 4.1, 135.4 (0.0, 1.8) | 4.1, 127.1 (0.0, 0.9) | -0.0 | +8.3 | **disagree** |
| run4 | trace | 56/interp | 4.1, 20.1 (0.0, 1.8) | 4.1, 134.4 (0.0, 1.8) | slope -245.4 | -114.3 (tol 8.5) | **disagree** |
| run4 | trace | 58/interp | 4.1, 45.3 (0.0, 1.5) | 4.1, 134.2 (0.0, 1.8) | slope -245.4 | -88.9 (tol 8.6) | **disagree** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
