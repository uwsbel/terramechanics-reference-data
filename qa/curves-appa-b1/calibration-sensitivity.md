# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| FA-20 | 1 | curve | 25 | 0.002632 | 0.04427 | -1.1% | -0.5% |
| FA-24 | 1 | curve | 25 | 0.004126 | 0.02014 | -2.1% | -0.3% |
| FA-28 | 1 | curve | 26 | 0.004619 | 0.04331 | -3.5% | +0.5% |
| FA-4 | 1 | curve | 25 | 0.00414 | 0.02353 | -2.0% | -0.4% |
| FA-40 | 1 | band-bottom | 23 | 0.00438 | 0.02875 | -19.7% | -34.5% |
| FA-40 | 1 | band-top | 23 | 0.004524 | 0.01314 | -13.2% | -681.4% |
| FA-48 | 1 | curve | 24 | 0.006013 | 0.06125 | -0.5% | -0.4% |
| FA-8 | 1 | curve | 26 | 0.005199 | 0.03278 | -5.2% | -0.4% |
