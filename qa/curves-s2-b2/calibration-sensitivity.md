# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| F2-45 | 1 | lpt79 | 29 | 0.00453 | 0.2239 | +2.4% | +0.2% |
| F2-45 | 1 | lpt95 | 50 | 0.004553 | 0.3202 | +1.0% | +0.1% |
| F2-46 | 1 | lpt89 | 32 | 0.01005 | 0.6555 | -0.5% | -0.1% |
| F2-46 | 1 | lpt98 | 41 | 0.01141 | 0.6708 | -0.4% | -0.1% |
| F2-47 | 1 | lpt101 | 32 | 0.005098 | 2.358 | +0.4% | -0.1% |
| F2-47 | 1 | lpt91 | 44 | 0.005357 | 2.271 | +0.4% | -0.0% |
| F2-48 | 1 | lpt85 | 41 | 0.1334 | 1.823 | -21.8% | -1.2% |
| F2-48 | 1 | lpt87 | 48 | 0.1395 | 1.616 | -23.4% | -1.2% |
