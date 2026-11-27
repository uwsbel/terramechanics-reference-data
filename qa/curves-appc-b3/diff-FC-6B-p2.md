# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b3\rederived\claude\FC-6B\points-p2-native.csv` (claude), `<repository>\qa\curves-appc-b3\rederived\codex\FC-6B\points-p2-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 40 | 18 |
| x per px | 0.1730 | 0.1708 |
| y per px | 0.3388 | 0.3389 |
| RMS residual x, y | 0.604, 0.165 | 1.345, 0.243 |

Corners of claude's box [900, 2225, 2145, 3300] mapped by both calibrations (tolerance 2.12 in x, 0.75 in y):

- (40.2, 56.7) vs (42.0, 56.6)
- (255.6, 56.8) vs (254.7, 56.8)
- (39.5, -307.6) vs (41.2, -307.8)
- (254.8, -307.4) vs (253.9, -307.5)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.35 | 0.33 | 0.27 | 24 | 0.77 | 0.62 | agree |
| x | 50 | 0.11 | 0.17 | 0.18 | 21 | 0.50 | 0.58 | agree |
| x | 100 | 0.05 | 0.30 | 0.30 | 21 | 0.50 | 0.61 | agree |
| x | 150 | 0.04 | 0.22 | 0.25 | 21 | 0.74 | 0.50 | agree |
| x | 200 | 0.05 | 0.33 | 0.31 | 21 | 0.50 | 0.90 | agree |
| x | 250 | 0.11 | 0.43 | 0.34 | 21 | 0.83 | 0.98 | agree |
| y | -300 | 0.41 | 0.10 | 0.27 | 12 | 0.50 | 0.65 | agree |
| y | 0 | 0.31 | 0.16 | 0.20 | 12 | 0.59 | 0.50 | agree |
| y | 50 | 0.02 | 0.10 | 0.09 | 12 | 0.50 | 0.50 | agree |

Both maps along every verified line and every interval midline (187 places): largest difference 0.02039 in x (tolerance 0.2261, claude 50), 0.1666 in y (tolerance 0.4177, claude -300); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 9 shared lines checked against the ink, mean of the median distances 0.24 px (claude: x 0.30, y 0.12), 0.25 px (codex: x 0.27, y 0.19), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

4 series in claude, 4 in codex.


## Points

Matched: 52; agreed 34; disagreed 18; unmatched 0 (kept as one-sided: 0 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| n2934 | marker | 4/4 | 48.1, -256.1 (0.6, 1.2) | 47.9, -262.8 (1.0, 2.2) | +0.3 | +6.6 | **disagree** |
| n2934 | marker | 5/5 | 67.8, -256.1 (0.4, 1.2) | 68.0, -262.7 (0.5, 0.9) | -0.2 | +6.6 | **disagree** |
| n2934 | marker | 6/6 | 88.6, -257.3 (0.4, 1.2) | 88.4, -265.0 (0.5, 0.9) | +0.1 | +7.7 | **disagree** |
| n2934 | marker | 7/7 | 108.4, -258.3 (0.5, 1.2) | 109.3, -265.3 (0.5, 0.9) | -0.9 | +7.0 | **disagree** |
| n2934 | marker | 8/8 | 128.3, -257.0 (0.5, 1.2) | 129.1, -262.6 (0.5, 0.9) | -0.8 | +5.5 | **disagree** |
| n2934 | marker | 9/9 | 149.7, -256.5 (0.7, 1.5) | 150.1, -263.2 (1.3, 2.6) | -0.5 | +6.7 | **disagree** |
| n2934 | marker | 10/10 | 169.1, -255.4 (0.5, 1.2) | 169.2, -262.5 (0.5, 0.9) | -0.0 | +7.1 | **disagree** |
| n2934 | marker | 11/11 | 189.0, -254.9 (0.4, 1.2) | 189.9, -262.8 (0.5, 0.9) | -1.0 | +7.8 | **disagree** |
| n2934 | marker | 12/12 | 218.6, -251.8 (0.4, 1.2) | 218.4, -259.0 (0.5, 0.9) | +0.2 | +7.1 | **disagree** |
| n4695 | marker | 3/3 | 28.5, -276.4 (0.4, 1.2) | 28.9, -279.4 (0.4, 0.9) | -0.4 | +3.0 | **disagree** |
| n4695 | marker | 5/5 | 66.8, -280.2 (0.4, 1.2) | 67.2, -284.0 (0.5, 0.9) | -0.5 | +3.8 | **disagree** |
| n4695 | marker | 6/6 | 86.6, -280.0 (0.4, 1.2) | 87.0, -283.7 (0.5, 0.9) | -0.5 | +3.7 | **disagree** |
| n4695 | marker | 7/7 | 107.6, -279.5 (0.5, 1.5) | 107.8, -283.9 (0.5, 0.9) | -0.2 | +4.4 | **disagree** |
| n4695 | marker | 8/8 | 127.3, -280.3 (0.5, 1.2) | 127.5, -283.2 (0.5, 0.9) | -0.1 | +2.9 | **disagree** |
| n4695 | marker | 9/9 | 148.7, -278.5 (0.7, 1.2) | 148.5, -282.8 (1.3, 2.6) | +0.2 | +4.4 | **disagree** |
| n4695 | marker | 10/10 | 167.2, -278.2 (0.5, 1.2) | 167.8, -283.1 (0.5, 0.9) | -0.6 | +4.9 | **disagree** |
| n4695 | marker | 11/11 | 187.8, -278.9 (0.4, 1.2) | 187.8, -283.1 (0.5, 0.9) | -0.1 | +4.2 | **disagree** |
| n4695 | marker | 12/12 | 216.9, -274.8 (0.4, 1.2) | 217.3, -277.9 (0.5, 0.9) | -0.4 | +3.2 | **disagree** |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
