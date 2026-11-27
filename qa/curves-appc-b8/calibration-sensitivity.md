# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| FC-10B | 1 | ps-loose | 17 | 3.644 | 15.16 | -1.5% | -0.2% |
| FC-10C | 1 | ps-loose | 23 | 8.237 | 16.29 | +0.1% | +0.0% |
| FC-11A | 1 | rsm-loose | 19 | 6.703 | 15.24 | -0.7% | -0.3% |
| FC-11B | 1 | rsm-loose | 18 | 6.941 | 15.98 | +0.2% | +0.2% |
| FC-11C | 1 | rsm-loose | 24 | 14.69 | 15.32 | +1.9% | +0.2% |
