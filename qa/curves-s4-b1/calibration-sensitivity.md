# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| F4-19 | 1 | run10 | 63 | 0.3102 | 0.3522 | -2.8% | -0.0% |
| F4-19 | 1 | run12 | 98 | 0.3168 | 0.6584 | -3.0% | -0.0% |
| F4-19 | 1 | run4 | 61 | 0.3122 | 0.3532 | -3.2% | -0.1% |
| F4-19 | 2 | run10 | 38 | 0.1015 | 0.007006 | -0.0% | -0.2% |
| F4-19 | 2 | run12 | 45 | 0.4061 | 0.005334 | -0.6% | -0.6% |
| F4-19 | 2 | run4 | 46 | 0.2202 | 0.00704 | -0.3% | -0.2% |
| F4-20 | 1 | run10 | 41 | 0.002271 | 0.3077 | -0.1% | +0.8% |
| F4-20 | 1 | run12 | 55 | 0.00176 | 0.5623 | -0.2% | +0.6% |
| F4-20 | 1 | run4 | 60 | 0.002377 | 0.6595 | -0.3% | +1.1% |
