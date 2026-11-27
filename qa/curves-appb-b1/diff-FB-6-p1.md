# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appb-b1\rederived\claude\FB-6\points-p1-native.csv` (claude), `<repository>\qa\curves-appb-b1\rederived\codex\FB-6\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 21 | 725 |
| x per px | 0.0075 | 0.0075 |
| y per px | 0.0075 | 0.0075 |
| RMS residual x, y | 0.008, 0.011 | 0.008, 0.012 |

Corners of claude's box [560, 740, 2680, 4110] mapped by both calibrations (tolerance 0.02 in x, 0.03 in y):

- (-0.5, 29.7) vs (-0.5, 29.7)
- (15.3, 29.3) vs (15.3, 29.3)
- (-1.3, 4.4) vs (-1.3, 4.4)
- (14.5, 4.0) vs (14.5, 4.0)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.06 | 0.35 | 0.35 | 23 | 0.98 | 0.70 | agree |
| x | 2 | 0.00 | 0.08 | 0.08 | 8 | 0.50 | 0.50 | agree |
| x | 4 | 0.07 | 0.31 | 0.25 | 8 | 0.50 | 0.50 | agree |
| x | 6 | 0.04 | 0.13 | 0.15 | 8 | 0.50 | 0.50 | agree |
| x | 8 | 0.05 | 0.12 | 0.11 | 8 | 0.50 | 0.50 | agree |
| x | 10 | 0.05 | 0.14 | 0.12 | 8 | 0.50 | 0.50 | agree |
| x | 12 | 0.04 | 0.18 | 0.16 | 8 | 0.50 | 0.50 | agree |
| x | 14 | 0.02 | 0.40 | 0.40 | 23 | 0.73 | 0.65 | agree |
| y | 5 | 0.10 | 0.36 | 0.36 | 23 | 0.61 | 0.55 | agree |
| y | 7 | 0.04 | 0.06 | 0.05 | 8 | 0.50 | 0.50 | agree |
| y | 9 | 0.02 | 0.09 | 0.10 | 8 | 0.50 | 0.50 | agree |
| y | 11 | 0.01 | 0.15 | 0.16 | 8 | 0.50 | 0.50 | agree |
| y | 13 | 0.02 | 0.11 | 0.12 | 8 | 0.50 | 0.50 | agree |
| y | 15 | 0.09 | 0.14 | 0.09 | 8 | 0.50 | 0.50 | agree |
| y | 17 | 0.03 | 0.12 | 0.12 | 8 | 0.50 | 0.50 | agree |
| y | 19 | 0.12 | 0.08 | 0.13 | 8 | 0.50 | 0.50 | agree |
| y | 21 | 0.01 | 0.14 | 0.13 | 8 | 0.50 | 0.50 | agree |
| y | 23 | 0.05 | 0.12 | 0.12 | 8 | 0.50 | 0.50 | agree |
| y | 25 | 0.08 | 0.08 | 0.06 | 8 | 0.51 | 0.50 | agree |
| y | 27 | 0.09 | 0.20 | 0.30 | 8 | 0.50 | 0.50 | agree |
| y | 29 | 0.11 | 0.41 | 0.42 | 23 | 0.66 | 0.68 | agree |

Both maps along every verified line and every interval midline (413 places): largest difference 0.01158 in x (tolerance 0.007455, claude 8), 0.009913 in y (tolerance 0.007542, codex 19); 91 beyond the two maps' line errors.

Canonical reading: claude (same lines; 21 shared lines checked against the ink, mean of the median distances 0.18 px (claude: x 0.21, y 0.16), 0.18 px (codex: x 0.20, y 0.17), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

2 series in claude, 2 in codex.


## Points

Matched: 40; agreed 40; disagreed 0; unmatched 5 (kept as one-sided: 0 of claude, 5 of codex).

No point disagreements.

## Ink check (D-031): 1 trace samples excluded

Overrides of hand decisions (1), for review:

- claude dr02 trace 1: hand decision one-sided-verified (on the ink of the drawn line, verified on the page by codex's adjudicator; blind adjudication item 0)
