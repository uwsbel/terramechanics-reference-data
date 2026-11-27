# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| FC-10A | 1 | ps-loose | 18 | 5.035 | 14.61 | +0.2% | +0.2% |
| FC-8 | 1 | rs-loose | 19 | 4.63 | 15.21 | -1.2% | -0.2% |
| FC-9A | 1 | rs-dense | 18 | 5.554 | 14.16 | +0.4% | +0.3% |
| FC-9B | 1 | rs-dense | 15 | 6.864 | 15.6 | -0.8% | +0.3% |
| FC-9C | 1 | rs-dense | 22 | 8.478 | 14.83 | -0.4% | +0.3% |
