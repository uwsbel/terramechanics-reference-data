# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| F2-54 | 1 | r53958 | 87 | 0.6437 | 0.4023 | -8.2% | -8.4% |
| F2-54 | 2 | r54025 | 100 | 0.6463 | 0.3888 | +16.4% | +16.3% |
| F2-54 | 3 | r5465 | 109 | 0.5841 | 0.2314 | -4.0% | -4.8% |
