# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| FB-3 | 1 | dr30 | 24 | 0.03411 | 0.01962 | -0.9% | +0.4% |
| FB-3 | 1 | dr99 | 23 | 0.03413 | 0.02288 | -1.5% | +0.1% |
| FB-4 | 1 | dr22 | 26 | 0.02051 | 0.007716 | +0.6% | +0.2% |
| FB-4 | 1 | dr86 | 21 | 0.02051 | 0.008184 | -0.7% | +0.1% |
| FB-5 | 1 | dr26 | 19 | 0.02095 | 0.03237 | +0.9% | +0.9% |
| FB-5 | 1 | dr84 | 22 | 0.02276 | 0.04716 | -0.0% | +0.4% |
| FB-6 | 1 | dr02 | 22 | 0.01361 | 0.01491 | -1.0% | -0.3% |
| FB-6 | 1 | dr82 | 23 | 0.01362 | 0.02918 | -0.5% | -0.4% |
| FB-7 | 1 | dr104 | 10 | 0.02428 | 0.01391 |  |  |
| FB-7 | 1 | dr77 | 27 | 0.02438 | 0.01205 | +1.1% | +0.2% |
| FB-7 | 1 | dr99p5 | 22 | 0.02343 | 0.01506 | +0.6% | +0.0% |
