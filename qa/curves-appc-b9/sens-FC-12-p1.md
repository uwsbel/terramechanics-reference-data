# Curve diff: claude vs codex

Files: `<repository>\qa\curves-appc-b9\rederived\claude\FC-12\points-p1-native.csv` (claude), `<repository>\qa\curves-appc-b9\rederived\codex\FC-12\points-p1-native.csv` (codex).

Sensitivity run: every reading bound multiplied by 0.5 before comparing.

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 72 | 72 |
| x per px | 3.4302 | 3.4301 |
| y per px | 3.4187 | 3.4189 |
| RMS residual x, y | 3.891, 9.999 | 3.886, 10.147 |

Corners of claude's box [560, 1365, 2650, 3770] mapped by both calibrations (tolerance 11.21 in x, 23.56 in y):

- (-76.2, 8080.2) vs (-75.8, 8080.4)
- (7093.0, 8115.7) vs (7093.1, 8116.2)
- (-83.0, -141.7) vs (-83.0, -142.0)
- (7086.2, -106.2) vs (7085.9, -106.1)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0 | 0.18 | 0.44 | 0.48 | 24 | 0.63 | 0.73 | agree |
| x | 1000 | 0.11 | 0.24 | 0.26 | 24 | 0.56 | 0.69 | agree |
| x | 2000 | 0.00 | 0.38 | 0.38 | 24 | 0.81 | 0.86 | agree |
| x | 3000 | 0.07 | 0.32 | 0.34 | 24 | 0.54 | 0.62 | agree |
| x | 4000 | 0.26 | 0.36 | 0.47 | 24 | 0.75 | 0.73 | agree |
| x | 5000 | 0.37 | 0.45 | 0.33 | 24 | 0.85 | 0.62 | agree |
| x | 6000 | 0.18 | 0.12 | 0.19 | 24 | 0.56 | 0.72 | agree |
| x | 7000 | 0.36 | 0.47 | 0.41 | 24 | 0.75 | 0.62 | agree |
| y | 0 | 0.12 | 0.30 | 0.28 | 21 | 0.59 | 0.57 | agree |
| y | 1000 | 0.11 | 0.35 | 0.30 | 21 | 0.68 | 0.60 | agree |
| y | 2000 | 0.25 | 0.34 | 0.31 | 21 | 0.71 | 0.53 | agree |
| y | 3000 | 0.21 | 0.33 | 0.31 | 21 | 0.63 | 0.77 | agree |
| y | 4000 | 0.37 | 0.35 | 0.36 | 21 | 0.70 | 0.61 | agree |
| y | 5000 | 0.02 | 0.33 | 0.33 | 21 | 0.65 | 0.63 | agree |
| y | 6000 | 0.19 | 0.31 | 0.34 | 21 | 0.85 | 0.66 | agree |
| y | 7000 | 0.21 | 0.26 | 0.25 | 21 | 0.75 | 0.59 | agree |
| y | 8000 | 0.29 | 0.54 | 0.56 | 21 | 0.72 | 0.94 | agree |

Both maps along every verified line and every interval midline (406 places): largest difference 1.34 in x (tolerance 5.417, claude 5000), 0.9925 in y (tolerance 4.607, codex 4000); 0 beyond the two maps' line errors.

Canonical reading: claude (same lines; 17 shared lines checked against the ink, mean of the median distances 0.35 px (claude: x 0.35, y 0.35), 0.35 px (codex: x 0.36, y 0.34), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 22; agreed 22; disagreed 0; unmatched 1 (kept as one-sided: 0 of claude, 1 of codex).

No point disagreements.
