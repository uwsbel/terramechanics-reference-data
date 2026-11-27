# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| FC-20 | 1 | data | 7 | 0.002686 | 0.01308 |  |  |
| FC-20 | 1 | lower | 24 | 0.003634 | 0.01441 | -1.7% | +0.2% |
| FC-20 | 1 | mean | 23 | 0.003581 | 0.01301 | -1.7% | +0.2% |
| FC-20 | 1 | upper | 24 | 0.003484 | 0.01132 | -1.9% | +0.1% |
| FC-21 | 1 | band-bottom | 27 | 0.001572 | 0.01907 | -13.3% | -43.0% |
| FC-21 | 1 | band-top | 27 | 0.001576 | 0.01172 | +21.8% | -46.7% |
| FC-21 | 1 | data | 8 | 0.0009575 | 0.01588 |  |  |
| FC-22 | 1 | data | 2 | 0.0006504 | 0.01984 |  |  |
| FC-22 | 1 | lower | 24 | 0.002011 | 0.01826 | -0.1% | -0.1% |
| FC-22 | 1 | mean | 26 | 0.001927 | 0.02171 | -0.7% | -0.1% |
| FC-22 | 1 | upper | 23 | 0.001853 | 0.02443 | -1.2% | -0.2% |
| FC-23 | 1 | ps | 27 | 0.004133 | 0.06357 | -3.4% | +0.1% |
| FC-23 | 1 | rc2 | 27 | 0.004126 | 0.06339 | -3.5% | +0.3% |
| FC-23 | 1 | rs | 29 | 0.005295 | 0.06061 | -3.0% | -0.7% |
| FC-23 | 1 | rsm-a | 27 | 0.004421 | 0.06355 | -2.8% | -1.0% |
| FC-23 | 1 | rsm-b | 27 | 0.004301 | 0.06214 | -2.6% | -0.5% |
| FC-23 | 1 | ss | 27 | 0.00495 | 0.06756 | -0.2% | +0.2% |
