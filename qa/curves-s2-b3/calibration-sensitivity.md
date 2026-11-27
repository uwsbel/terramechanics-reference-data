# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| F2-42 | 1 | lpt22 | 24 | 0.0101 | 1.021 | -0.1% | +0.1% |
| F2-42 | 1 | lpt23 | 27 | 0.01057 | 0.9922 | +0.2% | +0.6% |
| F2-42 | 1 | lpt24 | 26 | 0.008617 | 0.9947 | -0.1% | -0.0% |
| F2-42 | 1 | lpt25 | 25 | 0.01069 | 0.9929 | -0.2% | +0.2% |
| F2-44 | 1 | lpt24 | 28 | 0.004246 | 2.369 | -1.1% | -0.3% |
| F2-44 | 1 | lpt64a | 34 | 0.002945 | 2.443 | -0.3% | +0.0% |
| F2-44 | 1 | lpt69 | 38 | 0.0029 | 2.419 | -0.2% | +0.0% |
| F2-44 | 1 | lpt73 | 27 | 0.004295 | 2.229 | -1.3% | -0.1% |
| F2-44 | 1 | lpt74 | 33 | 0.004295 | 2.351 | -0.9% | -0.1% |
