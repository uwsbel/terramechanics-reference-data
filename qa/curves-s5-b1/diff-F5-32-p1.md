# Curve diff: claude vs codex

Files: `<repository>\qa\curves-s5-b1\rederived\claude\F5-32\points-p1-native.csv` (claude), `<repository>\qa\curves-s5-b1\rederived\codex\F5-32\points-p1-native.csv` (codex).

## Calibration

| | claude | codex |
|---|---|---|
| anchors | 44 | 438 |
| x per px | 0.0001 | 0.0001 |
| y per px | 0.2345 | 0.2345 |
| RMS residual x, y | 0.000, 0.072 | 0.000, 0.150 |

Corners of claude's box [1072, 1784, 1368, 3517] mapped by both calibrations (tolerance 0.00 in x, 0.46 in y):

- (0.1, -62.9) vs (0.1, -62.9)
- (0.1, 6.5) vs (0.1, 6.5)
- (-0.0, -66.7) vs (-0.0, -66.7)
- (-0.0, 2.7) vs (-0.0, 2.7)

Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the affine fit, a diagnostic of the drafting.

| axis | value | lines apart (px) | claude from ink, median (px) | codex from ink, median (px) | positions | claude line error (px) | codex line error (px) | verdict |
|---|---|---|---|---|---|---|---|---|
| x | 0.1 | | | | | | | claude's line not a knot: insufficient ink: tick found at 0 of 6 stub positions |
| x | 0 | 0.07 | 0.23 | 0.30 | 5 | 0.93 | 0.67 | agree |
| x | 0.01 | 0.26 | 0.21 | 0.14 | 11 | 0.50 | 0.50 | agree |
| x | 0.02 | 0.27 | 0.11 | 0.10 | 11 | 0.50 | 0.50 | agree |
| x | 0.03 | 0.04 | 0.08 | 0.11 | 11 | 0.50 | 0.50 | agree |
| x | 0.04 | 0.05 | 0.33 | 0.38 | 11 | 0.50 | 0.50 | agree |
| x | 0.05 | 0.06 | 0.14 | 0.10 | 11 | 0.50 | 0.50 | agree |
| x | 0.06 | 0.11 | 0.54 | 0.47 | 11 | 0.58 | 0.58 | agree |
| x | 0.07 | 0.02 | 0.14 | 0.16 | 11 | 0.50 | 0.50 | agree |
| x | 0.08 | 0.21 | 0.03 | 0.23 | 10 | 0.50 | 0.50 | agree |
| x | 0.09 | 0.09 | 0.06 | 0.14 | 5 | 0.50 | 0.50 | agree |
| y | -60 | 0.03 | 0.41 | 0.41 | 10 | 1.35 | 0.74 | agree |
| y | -40 | 0.12 | 0.47 | 0.46 | 16 | 1.05 | 0.64 | agree |
| y | -20 | 0.04 | 0.41 | 0.40 | 18 | 1.05 | 0.67 | agree |
| y | 0 | 0.17 | 0.46 | 0.43 | 18 | 1.14 | 1.46 | agree |

Both maps along every verified line and every interval midline (307 places): largest difference 0.0005385 in x (tolerance 5.735e-05, codex 0.02), 0.04103 in y (tolerance 0.6122, codex 0); 42 beyond the two maps' line errors.

Canonical reading: claude (named by the batch: Claude's map, on evidence: both readings anchor the 0.02 s line only on its tick at the right frame (about 80 px); Claude's line takes the panel's common tilt, Codex's its own fit to the tick. The line's surviving dots, in panel 2 (u 1718 px) and panel 3 (u 1853 and 2022 to 2091 px), read 0.01999 to 0.02004 s on Claude's map and 0.01974 to 0.01996 s on Codex's, Codex's departing further from 0.0200 s the farther the dot lies from the tick. At Claude's trace samples the two maps differ by up to 0.419 ms in panel 1 and 0.271 ms in panel 2, at 0.02 s; same lines; 14 shared lines checked against the ink, mean of the median distances 0.26 px (claude: x 0.19, y 0.44), 0.27 px (codex: x 0.21, y 0.42), within 0.25 px of each other, so the first submission); points are evaluated at claude's samples.

## Series

1 series in claude, 1 in codex.


## Points

Matched: 41; agreed 41; disagreed 0; unmatched 2 (kept as one-sided: 2 of claude, 0 of codex).

| series | kind | seq (claude/codex) | claude x, y (bounds) | codex x, y (bounds) | dx | dy | verdict |
|---|---|---|---|---|---|---|---|
| strut3 | feature | 1/- | 0.0, 0.2 | (none) | | | unmatched in codex |
| strut3 | trace | 1/- | 0.0, 0.2 (0.0, 1.1) | (no trace at this x) | | | unmatched in codex |

## Ink check (D-031): 0 trace samples excluded

No hand decision overridden.
