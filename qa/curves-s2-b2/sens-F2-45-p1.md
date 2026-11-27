# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s2-b2\rederived\claude\F2-45\points-p1-native.csv` (claude), `<repository>\qa\curves-s2-b2\rederived\codex\F2-45\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 104 | 88 |
| x per px | 0.0032 | 0.0032 |
| y per px | 0.1612 | 0.1611 |
| RMS residual x, y | 0.002, 0.170 | 0.003, 0.175 |

Corners of claude's box [350, 1420, 2320, 3640] mapped by both calibrations (tolerance 0.01 in x, 0.51 in y):

- (7.1, 304.8) vs (7.1, 304.7)
- (7.0, -12.7) vs (7.0, -12.6)
- (-0.0, 311.5) vs (-0.0, 311.4)
- (-0.2, -6.0) vs (-0.1, -5.9)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.32 | 0.34 | 0.33 | 19 | 0.90 | 0.62 | agree |
| x | 1 | 0.30 | 0.26 | 0.30 | 21 | 0.84 | 0.53 | agree |
| x | 2 | 0.36 | 0.27 | 0.24 | 21 | 0.68 | 0.52 | agree |
| x | 3 | 0.38 | 0.29 | 0.35 | 21 | 0.62 | 0.99 | agree |
| x | 4 | 0.35 | 0.38 | 0.44 | 20 | 1.05 | 0.81 | agree |
| x | 5 | 0.30 | 0.34 | 0.44 | 18 | 0.79 | 0.54 | agree |
| x | 6 | 0.29 | 0.50 | 0.52 | 20 | 0.78 | 0.60 | agree |
| x | 7 | 0.60 | 0.32 | 0.29 | 21 | 0.78 | 0.68 | agree |
| y | 0 | 0.17 | 0.34 | 0.31 | 21 | 0.56 | 0.50 | agree |
| y | 25 | 0.20 | 0.18 | 0.15 | 21 | 0.78 | 0.50 | agree |
| y | 50 | 0.23 | 0.34 | 0.28 | 21 | 0.70 | 0.55 | agree |
| y | 75 | 0.09 | 0.25 | 0.19 | 21 | 0.67 | 0.54 | agree |
| y | 100 | 0.08 | 0.30 | 0.35 | 21 | 0.53 | 0.50 | agree |
| y | 125 | 0.65 | 0.42 | 0.31 | 19 | 0.80 | 0.74 | agree |
| y | 150 | 0.38 | 0.45 | 0.30 | 19 | 0.95 | 0.61 | agree |
| y | 175 | 0.20 | 0.27 | 0.33 | 20 | 0.50 | 0.66 | agree |
| y | 200 | 0.16 | 0.19 | 0.16 | 19 | 0.64 | 0.56 | agree |
| y | 225 | 0.11 | 0.61 | 0.53 | 21 | 0.78 | 0.72 | agree |
| y | 250 | 0.44 | 0.38 | 0.21 | 21 | 0.54 | 0.76 | agree |
| y | 275 | | | | | 0.78 | | only in claude |
| y | 300 | | | | | 0.85 | | only in claude |

Both maps along every verified line and every interval midline (400 places): largest difference 0.002086 in x (tolerance 0.004752, codex 7), 0.2996 in y (tolerance 0.2611, claude 300); 3 beyond the two maps' line errors.

Canonical reading: claude (claude's lines include all of codex's and more, as close to the ink; 19 shared lines checked against the ink, mean of the median distances 0.34 px (claude: x 0.34, y 0.34), 0.32 px (codex: x 0.36, y 0.28)); points are evaluated at claude's samples.

## Series

2 series in claude, 2 in codex.


## Points

Matched: 67; agreed 60; disagreed 7; unmatched 23 (kept as one-sided: 0 of claude, 23 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| lpt79 | feature | 1/2 | 0.1, 8.1 (0.0, 0.6) | 0.0, 0.9 (0.0, 0.9) | +0.1 | +7.2 | **disagree** |
| lpt79 | feature | -/6 | (none) | 0.8, 29.8 | | | unmatched in claude |
| lpt79 | feature | -/26 | (none) | 5.6, 157.2 | | | unmatched in claude |
| lpt95 | feature | 1/2 | 0.0, 4.2 (0.0, 0.6) | 0.0, 0.9 (0.0, 0.7) | +0.0 | +3.3 | **disagree** |
| lpt95 | feature | 9/54 | 7.0, 299.0 (0.0, 0.6) | 7.0, 299.0 (0.0, 1.0) | -0.0 | +0.0 | **disagree** |
| lpt95 | feature | 2/3 | 0.1, 12.2 (0.0, 0.9) | 0.1, 14.5 (0.0, 0.5) | -0.0 | -2.3 | **disagree** |
| lpt95 | feature | 4/23 | 2.8, 111.4 (0.0, 1.4) | 2.8, 113.8 (0.0, 0.4) | -0.0 | -2.3 | **disagree** |
| lpt95 | feature | 5/25 | 3.1, 124.2 (0.0, 1.2) | 3.1, 123.2 (0.0, 0.4) | +0.0 | +1.0 | **disagree** |
| lpt95 | feature | 7/47 | 6.4, 273.5 (0.0, 0.7) | 6.1, 253.2 (0.0, 0.4) | +0.3 | +20.3 | **disagree** |
| lpt95 | feature | -/5 | (none) | 0.4, 30.5 | | | unmatched in claude |
| lpt95 | feature | -/10 | (none) | 1.4, 62.5 | | | unmatched in claude |
| lpt95 | feature | -/14 | (none) | 1.8, 75.6 | | | unmatched in claude |
| lpt95 | feature | -/15 | (none) | 1.9, 78.2 | | | unmatched in claude |
| lpt95 | feature | -/18 | (none) | 2.4, 97.3 | | | unmatched in claude |
| lpt95 | feature | -/19 | (none) | 2.5, 99.7 | | | unmatched in claude |
| lpt95 | feature | -/21 | (none) | 2.7, 109.4 | | | unmatched in claude |
| lpt95 | feature | -/26 | (none) | 3.2, 127.4 | | | unmatched in claude |
| lpt95 | feature | -/30 | (none) | 3.9, 152.7 | | | unmatched in claude |
| lpt95 | feature | -/31 | (none) | 3.9, 155.7 | | | unmatched in claude |
| lpt95 | feature | -/36 | (none) | 4.8, 192.3 | | | unmatched in claude |
| lpt95 | feature | -/37 | (none) | 4.8, 195.5 | | | unmatched in claude |
| lpt95 | feature | -/39 | (none) | 5.3, 213.6 | | | unmatched in claude |
| lpt95 | feature | -/41 | (none) | 5.3, 217.4 | | | unmatched in claude |
| lpt95 | feature | -/43 | (none) | 5.6, 228.8 | | | unmatched in claude |
| lpt95 | feature | -/44 | (none) | 5.6, 231.9 | | | unmatched in claude |
