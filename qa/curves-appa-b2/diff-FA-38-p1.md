# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appa-b2\rederived\claude\FA-38\points-p1-native.csv` (claude), `<repository>\qa\curves-appa-b2\rederived\codex\FA-38\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 112 | 973 |
| x per px | 0.0010 | 0.0010 |
| y per px | 0.0686 | 0.0686 |
| RMS residual x, y | 0.002, 0.069 | 0.002, 0.064 |

Corners of claude's box [672, 1157, 2185, 3762] mapped by both calibrations (tolerance 0.01 in x, 0.20 in y (in the plotting coordinates of log10 x, linear y)):

- (9.4, 101.3) vs (9.4, 101.3)
- (9.3, -2.5) vs (9.3, -2.5)
- (0.0, 102.5) vs (0.0, 102.5)
- (0.0, -1.4) vs (0.0, -1.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0.02 | 0.19 | 0.25 | 0.22 | 23 | 0.63 | 0.70 | agree |
| x | 0.05 | 0.10 | 0.47 | 0.53 | 23 | 0.66 | 0.72 | agree |
| x | 0.1 | 0.20 | 0.36 | 0.35 | 23 | 0.68 | 0.62 | agree |
| x | 0.2 | 0.07 | 0.36 | 0.34 | 23 | 0.56 | 0.69 | agree |
| x | 0.5 | 0.07 | 0.32 | 0.35 | 21 | 0.64 | 0.68 | agree |
| x | 1 | 0.33 | 0.40 | 0.47 | 23 | 1.25 | 1.08 | agree |
| x | 1.5 | 0.07 | 0.21 | 0.20 | 22 | 0.50 | 0.56 | agree |
| x | 2 | 0.27 | 0.47 | 0.38 | 23 | 0.75 | 0.68 | agree |
| x | 3 | 0.14 | 0.48 | 0.48 | 23 | 0.56 | 0.58 | agree |
| x | 4 | 0.09 | 0.37 | 0.38 | 21 | 0.73 | 0.89 | agree |
| x | 5 | 0.10 | 0.29 | 0.26 | 23 | 0.64 | 0.57 | agree |
| x | 9 | 0.11 | 0.47 | 0.49 | 23 | 0.68 | 0.81 | agree |
| y | 0 | 0.13 | 0.35 | 0.33 | 23 | 0.70 | 0.64 | agree |
| y | 10 | 0.15 | 0.29 | 0.20 | 23 | 0.93 | 0.79 | agree |
| y | 20 | 0.40 | 0.40 | 0.38 | 22 | 0.66 | 0.50 | agree |
| y | 30 | 0.38 | 0.43 | 0.45 | 22 | 0.65 | 0.74 | agree |
| y | 40 | 0.40 | 0.40 | 0.35 | 23 | 0.52 | 0.56 | agree |
| y | 50 | 0.08 | 0.30 | 0.23 | 23 | 0.78 | 0.52 | agree |
| y | 60 | 0.30 | 0.41 | 0.56 | 23 | 1.27 | 1.09 | agree |
| y | 70 | 0.01 | 0.21 | 0.22 | 23 | 0.55 | 0.50 | agree |
| y | 80 | 0.05 | 0.24 | 0.24 | 23 | 0.50 | 0.68 | agree |
| y | 90 | 0.05 | 0.35 | 0.31 | 23 | 0.50 | 0.50 | agree |
| y | 100 | 0.06 | 0.24 | 0.24 | 23 | 0.60 | 0.50 | agree |

(In the plotting coordinates: log10 x, linear y.) Both maps along every verified line and every interval midline (489 places): largest difference 0.0002598 in x (tolerance 0.002409, codex 1), 0.02241 in y (tolerance 0.09534, claude 40); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 23 shared lines checked against the ink, mean of the median distances 0.35 px (claude: x 0.37, y 0.33), 0.35 px (codex: x 0.37, y 0.32), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

3 series in claude, 3 in codex.


## Points

Matched: 115; agreed 113; disagreed 2; unmatched 40 (kept as one-sided: 4 of claude, 36 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| average | feature | -/3 | (none) | 1.5, 79.0 | | | unmatched in claude |
| average | marker | -/2 | (none) | 4.7, 97.0 | | | unmatched in claude |
| average | marker | -/3 | (none) | 3.4, 91.5 | | | unmatched in claude |
| average | marker | -/4 | (none) | 2.4, 85.2 | | | unmatched in claude |
| average | marker | -/6 | (none) | 1.7, 80.4 | | | unmatched in claude |
| average | marker | -/7 | (none) | 1.2, 76.8 | | | unmatched in claude |
| average | marker | -/9 | (none) | 0.6, 71.6 | | | unmatched in claude |
| average | marker | -/10 | (none) | 0.4, 69.5 | | | unmatched in claude |
| average | marker | -/11 | (none) | 0.3, 66.5 | | | unmatched in claude |
| average | marker | -/15 | (none) | 0.1, 58.6 | | | unmatched in claude |
| average | marker | -/16 | (none) | 0.1, 56.5 | | | unmatched in claude |
| average | trace | 1/- | 0.1, 49.8 (0.0, 0.4) | (no trace at this x) | | | unmatched in codex |
| average | trace | 11/interp | 0.2, 63.9 (0.0, 0.5) | 0.2, 62.9 (0.0, 0.5) | slope -1.2 | +1.1 (tol 1.0) | **disagree** |
| average | trace | 30/- | 2.0, 82.2 (0.0, 0.5) | (no trace at this x) | | | unmatched in codex |
| lower | feature | -/3 | (none) | 1.5, 78.2 | | | unmatched in claude |
| lower | marker | -/1 | (none) | 2.4, 84.5 | | | unmatched in claude |
| lower | marker | -/3 | (none) | 1.7, 79.7 | | | unmatched in claude |
| lower | marker | -/4 | (none) | 0.8, 73.6 | | | unmatched in claude |
| lower | marker | -/7 | (none) | 0.3, 65.7 | | | unmatched in claude |
| lower | marker | -/10 | (none) | 0.1, 58.2 | | | unmatched in claude |
| lower | marker | -/11 | (none) | 0.1, 56.2 | | | unmatched in claude |
| upper | feature | 1/1 | 0.1, 53.0 (0.0, 0.3) | 0.1, 54.0 (0.0, 0.3) | -0.0 | -0.9 | **disagree** |
| upper | feature | -/3 | (none) | 1.5, 79.8 | | | unmatched in claude |
| upper | marker | -/1 | (none) | 2.4, 85.7 | | | unmatched in claude |
| upper | marker | -/4 | (none) | 0.6, 72.4 | | | unmatched in claude |
| upper | marker | -/6 | (none) | 0.3, 65.7 | | | unmatched in claude |
| upper | marker | -/7 | (none) | 0.2, 63.9 | | | unmatched in claude |
| upper | trace | 1/- | 0.1, 53.0 (0.0, 0.3) | (no trace at this x) | | | unmatched in codex |
| upper | trace | 30/- | 2.0, 83.1 (0.0, 0.5) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 15 trace samples excluded

Overrides of hand decisions (1), for review:

- claude upper trace 41: hand decision one-sided-verified (on the ink of the drawn line, verified on the page by codex's adjudicator; blind adjudication item 2)
