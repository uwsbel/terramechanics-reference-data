# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s5-b1\rederived\claude\F5-32\points-p3-native.csv` (claude), `<repository>\qa\curves-s5-b1\rederived\codex\F5-32\points-p3-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 55 | 632 |
| x per px | 0.0001 | 0.0001 |
| y per px | 0.2367 | 0.2368 |
| RMS residual x, y | 0.000, 0.108 | 0.000, 0.140 |

Corners of claude's box [1922, 1780, 2300, 3510] mapped by both calibrations (tolerance 0.00 in x, 0.49 in y):

- (0.1, -82.8) vs (0.1, -82.9)
- (0.1, 6.7) vs (0.1, 6.6)
- (-0.0, -86.9) vs (-0.0, -86.9)
- (-0.0, 2.6) vs (-0.0, 2.6)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0.1 | | | | | | | claude's line not a knot: insufficient ink: tick found at 0 of 6 stub positions |
| x | 0 | 0.10 | 0.38 | 0.39 | 5 | 1.28 | 0.67 | agree |
| x | 0.01 | 0.26 | 0.21 | 0.14 | 11 | 0.50 | 0.50 | agree |
| x | 0.02 | 0.27 | 0.11 | 0.10 | 11 | 0.50 | 0.50 | agree |
| x | 0.03 | 0.04 | 0.08 | 0.11 | 11 | 0.50 | 0.50 | agree |
| x | 0.04 | 0.05 | 0.33 | 0.38 | 11 | 0.50 | 0.50 | agree |
| x | 0.05 | 0.06 | 0.14 | 0.10 | 11 | 0.50 | 0.50 | agree |
| x | 0.06 | 0.11 | 0.54 | 0.47 | 11 | 0.58 | 0.58 | agree |
| x | 0.07 | 0.02 | 0.14 | 0.16 | 11 | 0.50 | 0.50 | agree |
| x | 0.08 | 0.21 | 0.03 | 0.23 | 10 | 0.50 | 0.50 | agree |
| x | 0.09 | 0.09 | 0.06 | 0.14 | 5 | 0.50 | 0.50 | agree |
| y | -80 | 0.03 | 0.36 | 0.36 | 21 | 0.73 | 0.50 | agree |
| y | -60 | 0.67 | 0.45 | 0.45 | 22 | 1.14 | 0.73 | agree |
| y | -40 | 0.06 | 0.42 | 0.38 | 22 | 0.77 | 0.61 | agree |
| y | -20 | 0.08 | 0.13 | 0.16 | 21 | 0.50 | 0.50 | agree |
| y | 0 | 0.04 | 0.34 | 0.31 | 22 | 0.50 | 0.50 | agree |

Both maps along every verified line and every interval midline (330 places): largest difference 0.0001506 in x (tolerance 5.843e-05, codex 0.02), 0.1654 in y (tolerance 0.4404, claude -60); 11 beyond the two maps' line errors.

Canonical reading: claude (same lines; 15 shared lines checked against the ink, mean of the median distances 0.25 px (claude: x 0.20, y 0.34), 0.26 px (codex: x 0.22, y 0.33), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 41; agreed 40; disagreed 1; unmatched 3 (kept as one-sided: 1 of claude, 2 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| strut1 | feature | 2/8 | 0.0, -39.1 (0.0, 1.1) | 0.0, -34.8 (0.0, 1.0) | +0.0 | -4.3 | **disagree** |
| strut1 | feature | -/24 | (none) | 0.0, -49.6 | | | unmatched in claude |
| strut1 | trace | 18/- | 0.0, -40.3 (0.0, 1.1) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
