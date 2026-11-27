# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b4\rederived\claude\FC-7C\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b4\rederived\codex\FC-7C\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 0.0002 | 0.0002 |
| y per px | 0.0204 | 0.0204 |
| RMS residual x, y | 0.000, 0.017 | 0.000, 0.015 |

Corners of claude's box [585, 1325, 2375, 3345] mapped by both calibrations (tolerance 0.00 in x, 0.05 in y):

- (0.3, 35.4) vs (0.3, 35.4)
- (0.3, -1.1) vs (0.3, -1.1)
- (-0.0, 36.1) vs (-0.0, 36.1)
- (-0.0, -0.4) vs (-0.0, -0.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.77 | 0.39 | 0.35 | 21 | 1.19 | 1.02 | agree |
| x | 0.04 | 0.79 | 0.44 | 0.32 | 21 | 1.03 | 0.90 | agree |
| x | 0.08 | 0.65 | 0.22 | 0.25 | 21 | 0.89 | 0.62 | agree |
| x | 0.12 | 1.15 | 0.36 | 0.39 | 21 | 0.96 | 1.27 | agree |
| x | 0.16 | 0.77 | 0.63 | 0.46 | 21 | 1.25 | 1.28 | agree |
| x | 0.2 | 0.38 | 0.36 | 0.30 | 21 | 0.91 | 0.55 | agree |
| x | 0.24 | 0.59 | 0.35 | 0.25 | 21 | 0.95 | 0.55 | agree |
| x | 0.32 | 0.58 | 0.45 | 0.57 | 21 | 0.98 | 1.13 | agree |
| y | 0 | 0.13 | 0.40 | 0.43 | 24 | 0.51 | 0.55 | agree |
| y | 5 | 0.35 | 0.43 | 0.53 | 24 | 0.86 | 1.16 | agree |
| y | 10 | 0.54 | 0.28 | 0.55 | 24 | 0.64 | 0.98 | agree |
| y | 15 | 0.81 | 0.39 | 0.38 | 24 | 0.95 | 0.79 | agree |
| y | 20 | 0.30 | 0.40 | 0.34 | 23 | 0.62 | 0.70 | agree |
| y | 25 | 0.29 | 0.37 | 0.44 | 24 | 0.61 | 0.90 | agree |
| y | 30 | 0.23 | 0.25 | 0.10 | 23 | 0.70 | 0.50 | agree |
| y | 35 | 0.83 | 0.24 | 0.42 | 24 | 0.78 | 1.06 | agree |

Both maps along every verified line and every interval midline (323 places): largest difference 0.000151 in x (tolerance 0.0004105, codex 0.12), 0.01389 in y (tolerance 0.03723, claude 35); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 16 shared lines checked against the ink, mean of the median distances 0.37 px (claude: x 0.40, y 0.34), 0.38 px (codex: x 0.36, y 0.40), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

6 series in claude, 7 in codex.
Only in codex: FC-7C/1/unidentified


## Points

Matched: 94; agreed 82; disagreed 12; unmatched 2 (kept as one-sided: 0 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n10p2psi | marker | 3/3 | 0.0, 8.9 (0.0, 0.0) | 0.0, 9.0 (0.0, 0.0) | +0.0 | -0.1 | **disagree** |
| n10p2psi | marker | 6/6 | 0.1, 11.5 (0.0, 0.0) | 0.1, 11.6 (0.0, 0.0) | +0.0 | -0.1 | **disagree** |
| n10p2psi | marker | 8/8 | 0.1, 11.7 (0.0, 0.0) | 0.1, 11.8 (0.0, 0.0) | +0.0 | -0.1 | **disagree** |
| n10p2psi | marker | 10/10 | 0.1, 11.0 (0.0, 0.0) | 0.1, 11.1 (0.0, 0.0) | -0.0 | -0.1 | **disagree** |
| n10p2psi | marker | 12/12 | 0.2, 10.2 (0.0, 0.1) | 0.2, 10.4 (0.0, 0.1) | -0.0 | -0.2 | **disagree** |
| n10p2psi | marker | 14/14 | 0.2, 9.3 (0.0, 0.0) | 0.2, 9.4 (0.0, 0.0) | +0.0 | -0.1 | **disagree** |
| n10p2psi | marker | 15/15 | 0.2, 9.1 (0.0, 0.0) | 0.2, 9.2 (0.0, 0.0) | +0.0 | -0.1 | **disagree** |
| n13p8psi | marker | 14/14 | 0.2, 13.2 (0.0, 0.0) | 0.2, 13.2 (0.0, 0.0) | +0.0 | +0.1 | **disagree** |
| n3p4psi | marker | 7/7 | 0.1, 4.8 (0.0, 0.0) | 0.1, 4.7 (0.0, 0.1) | +0.0 | +0.1 | **disagree** |
| n3p4psi | marker | 15/15 | 0.2, 3.9 (0.0, 0.0) | 0.2, 3.8 (0.0, 0.0) | +0.0 | +0.1 | **disagree** |
| n6p6psi | marker | 1/- | 0.0, 2.8 | (none) | | | unmatched in codex |
| n6p6psi | marker | 4/3 | 0.0, 5.8 (0.0, 0.0) | 0.0, 5.7 (0.0, 0.0) | +0.0 | +0.1 | **disagree** |
| n6p6psi | marker | 16/15 | 0.3, 6.5 (0.0, 0.0) | 0.3, 6.4 (0.0, 0.0) | +0.0 | +0.1 | **disagree** |
| unidentified | marker | -/1 | (none) | 0.0, 2.7 | | | unmatched in claude |
| n6p6psi | marker | 1 (claude) | 0.0, 2.8 | codex: unidentified (unidentified) | | | **identity conflict** |
| unidentified | marker | 1 (codex) | 0.0, 2.7 | claude: n6p6psi (diamond) | | | **identity conflict** |
