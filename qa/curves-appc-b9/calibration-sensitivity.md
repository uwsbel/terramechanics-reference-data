# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| FC-12 | 1 | rc2-loose | 20 | 7.589 | 14.36 | -0.9% | -0.1% |
| FC-13 | 1 | ss-loose | 21 | 4.776 | 13.04 | -1.6% | -0.9% |
| FC-14 | 1 | lsm-loose | 22 | 4.876 | 16.68 | -1.3% | -0.2% |
| FC-15 | 1 | lsm-dense | 22 | 16.83 | 23.22 | -1.5% | -0.2% |
