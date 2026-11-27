# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| F2-29 | 1 | lpt27 | 57 | 0.01365 | 0.975 | +0.6% | +0.1% |
| F2-32 | 1 | fit | 12 | 0.01525 | 0.1328 | -1.1% | +0.1% |
| F2-32 | 1 | lpt52 | 31 | 0.01508 | 0.1345 | -1.4% | -0.0% |
| F2-32 | 1 | lpt53 | 27 | 0.01312 | 0.134 | +1.9% | +0.5% |
| F2-32 | 1 | lpt93 | 34 | 0.0146 | 0.1208 | +2.2% | +0.2% |
| F2-33 | 1 | bce | 9 | 0.01566 | 1.474 | -1.6% | +0.0% |
| F2-33 | 1 | fit | 8 | 0.01765 | 4.907 | -1.6% | -0.2% |
| F2-33 | 1 | lpt74 | 30 | 0.01549 | 4.06 | -1.7% | +0.2% |
| F2-33 | 1 | lpt75 | 18 | 0.01385 | 4.169 | -1.1% | -0.3% |
| F2-34 | 1 | fit | 11 | 0.01675 | 2.033 | +1.5% | +0.0% |
| F2-34 | 1 | lpt87 | 32 | 0.01687 | 2.319 | +1.7% | +0.6% |
| F2-34 | 1 | lpt88 | 31 | 0.02661 | 2.131 | -0.8% | +0.7% |
