# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| FC-16 | 1 | data | 11 | 0.001263 | 0.02262 |  |  |
| FC-16 | 1 | lower | 29 | 0.002638 | 0.004673 | -1.6% | -0.0% |
| FC-16 | 1 | mean | 29 | 0.002522 | 0.0188 | -1.6% | -0.2% |
| FC-16 | 1 | upper | 30 | 0.002473 | 0.03376 | -1.6% | -0.2% |
| FC-17 | 1 | data | 6 | 0.001622 | 0.02291 |  |  |
| FC-17 | 1 | lower | 27 | 0.001805 | 0.01383 | -0.7% | -0.2% |
| FC-17 | 1 | mean | 26 | 0.001769 | 0.01897 | -0.7% | -0.4% |
| FC-17 | 1 | upper | 26 | 0.00188 | 0.03381 | -1.7% | -0.6% |
| FC-18 | 1 | data | 6 | 0.001034 | 0.0142 |  |  |
| FC-18 | 1 | lower | 26 | 0.001951 | 0.01629 | +1.6% | +0.5% |
| FC-18 | 1 | mean | 25 | 0.001823 | 0.0122 | +1.3% | +0.2% |
| FC-18 | 1 | upper | 25 | 0.001689 | 0.01421 | +1.2% | +0.1% |
| FC-19 | 1 | data | 2 | 0.0004597 | 0.0487 |  |  |
| FC-19 | 1 | lower | 24 | 0.002362 | 0.03956 | +0.3% | -0.4% |
| FC-19 | 1 | mean | 23 | 0.002379 | 0.04969 | +0.4% | -0.5% |
| FC-19 | 1 | upper | 26 | 0.002391 | 0.06443 | +0.0% | -0.7% |
