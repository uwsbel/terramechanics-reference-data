# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b8\rederived\claude\FC-10B\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b8\rederived\codex\FC-10B\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4303 | 3.4302 |
| y per px | 3.4218 | 3.4220 |
| RMS residual x, y | 3.610, 10.171 | 3.458, 10.179 |

Corners of claude's box [545, 1395, 2640, 3790] mapped by both calibrations (tolerance 10.50 in x, 23.77 in y):

- (-84.4, 8071.8) vs (-84.1, 8071.7)
- (7102.0, 8093.8) vs (7102.1, 8094.2)
- (-101.3, -123.5) vs (-101.2, -123.9)
- (7085.1, -101.4) vs (7085.0, -101.4)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.27 | 0.50 | 0.41 | 24 | 0.73 | 0.94 | agree |
| x | 1000 | 0.19 | 0.35 | 0.35 | 24 | 0.51 | 0.55 | agree |
| x | 2000 | 0.26 | 0.49 | 0.50 | 24 | 0.80 | 1.26 | agree |
| x | 3000 | 0.18 | 0.28 | 0.33 | 24 | 0.74 | 0.72 | agree |
| x | 4000 | 0.10 | 0.46 | 0.38 | 24 | 0.87 | 0.81 | agree |
| x | 5000 | 0.10 | 0.26 | 0.31 | 24 | 0.58 | 0.62 | agree |
| x | 6000 | 0.11 | 0.60 | 0.58 | 24 | 1.20 | 1.08 | agree |
| x | 7000 | 0.34 | 0.29 | 0.27 | 24 | 0.52 | 0.77 | agree |
| y | 0 | 0.09 | 0.34 | 0.37 | 21 | 0.85 | 0.76 | agree |
| y | 1000 | 0.17 | 0.49 | 0.51 | 21 | 0.59 | 0.75 | agree |
| y | 2000 | 0.16 | 0.31 | 0.33 | 21 | 0.50 | 0.54 | agree |
| y | 3000 | 0.12 | 0.34 | 0.33 | 21 | 0.54 | 0.69 | agree |
| y | 4000 | 0.20 | 0.39 | 0.43 | 21 | 0.58 | 0.57 | agree |
| y | 5000 | 0.17 | 0.28 | 0.34 | 21 | 0.81 | 0.73 | agree |
| y | 6000 | 0.17 | 0.17 | 0.22 | 21 | 0.51 | 0.50 | agree |
| y | 7000 | 0.09 | 0.44 | 0.41 | 21 | 0.92 | 0.84 | agree |
| y | 8000 | 0.31 | 0.38 | 0.43 | 21 | 0.92 | 0.80 | agree |

Both maps along every verified line and every interval midline (382 places): largest difference 0.9849 in x (tolerance 5.738, codex 0), 0.8782 in y (tolerance 5.964, claude 8000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.38 px (claude: x 0.41, y 0.35), 0.38 px (codex: x 0.39, y 0.37), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 16; agreed 16; disagreed 0; unmatched 2 (kept as one-sided: 0 of claude, 2 of codex).

No point disagreements.
