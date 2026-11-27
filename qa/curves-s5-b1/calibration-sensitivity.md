# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| F5-24 | 1 | pen | 43 | 0.000115 | 0.008483 | -0.4% | -0.2% |
| F5-25 | 1 | strut3 | 49 | 9.037e-05 | 0.2258 | -0.8% | -8.1% |
| F5-25 | 2 | strut2 | 48 | 7.984e-05 | 0.2682 | -0.8% | -1.3% |
| F5-25 | 3 | strut1 | 67 | 6.909e-05 | 0.2052 | -0.1% | +2.4% |
| F5-31 | 1 | pen | 40 | 0.0001012 | 0.01153 | -1.1% | +0.0% |
| F5-32 | 1 | strut3 | 43 | 0.0001251 | 0.107 | +44.0% | -0.0% |
| F5-32 | 2 | strut2 | 43 | 0.0003133 | 0.1011 | +0.5% | -0.1% |
| F5-32 | 3 | strut1 | 44 | 0.0001514 | 0.1511 | -0.9% | -0.3% |
