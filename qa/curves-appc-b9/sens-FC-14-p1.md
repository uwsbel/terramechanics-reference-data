# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b9\rederived\claude\FC-14\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b9\rederived\codex\FC-14\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4385 | 3.4385 |
| y per px | 3.4236 | 3.4240 |
| RMS residual x, y | 3.634, 10.505 | 3.441, 10.325 |

Corners of claude's box [615, 1375, 2700, 3795] mapped by both calibrations (tolerance 10.51 in x, 24.25 in y):

- (-104.2, 8085.0) vs (-104.0, 8085.4)
- (7065.1, 8154.1) vs (7065.3, 8155.0)
- (-72.0, -199.8) vs (-71.9, -200.4)
- (7097.2, -130.7) vs (7097.4, -130.7)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.32 | 0.40 | 0.33 | 24 | 0.71 | 0.67 | agree |
| x | 1000 | 0.32 | 0.22 | 0.26 | 24 | 0.63 | 0.80 | agree |
| x | 2000 | 0.14 | 0.55 | 0.55 | 24 | 0.81 | 0.89 | agree |
| x | 3000 | 0.21 | 0.29 | 0.35 | 24 | 0.59 | 0.58 | agree |
| x | 4000 | 0.11 | 0.37 | 0.38 | 24 | 0.84 | 0.63 | agree |
| x | 5000 | 0.33 | 0.45 | 0.39 | 24 | 0.82 | 0.66 | agree |
| x | 6000 | 0.30 | 0.36 | 0.39 | 24 | 0.65 | 0.99 | agree |
| x | 7000 | 0.28 | 0.37 | 0.33 | 24 | 0.71 | 0.56 | agree |
| y | 0 | 0.34 | 0.26 | 0.19 | 21 | 1.07 | 0.73 | agree |
| y | 1000 | 0.54 | 0.33 | 0.20 | 21 | 0.82 | 0.60 | agree |
| y | 2000 | 0.25 | 0.27 | 0.29 | 21 | 0.84 | 0.86 | agree |
| y | 3000 | 0.36 | 0.57 | 0.68 | 21 | 1.04 | 0.87 | agree |
| y | 4000 | 0.40 | 0.35 | 0.37 | 21 | 0.75 | 0.61 | agree |
| y | 5000 | 0.45 | 0.35 | 0.22 | 21 | 0.95 | 0.75 | agree |
| y | 6000 | 0.12 | 0.35 | 0.37 | 21 | 0.70 | 0.61 | agree |
| y | 7000 | 0.24 | 0.32 | 0.45 | 21 | 0.64 | 0.70 | agree |
| y | 8000 | 0.33 | 0.60 | 0.78 | 21 | 1.29 | 1.19 | agree |

Both maps along every verified line and every interval midline (354 places): largest difference 1.21 in x (tolerance 5.144, codex 0), 1.582 in y (tolerance 5.269, codex 1000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.38 px (claude: x 0.38, y 0.38), 0.38 px (codex: x 0.37, y 0.40), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 22; agreed 22; disagreed 0; unmatched 1 (kept as one-sided: 0 of claude, 1 of codex).

No point disagreements.
