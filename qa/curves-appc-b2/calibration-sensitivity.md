# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| FC-3B | 1 | n1761 | 64 | 0.4046 | 15.19 | -0.5% | -1.5% |
| FC-3B | 1 | n2934 | 59 | 0.3967 | 14.14 | -0.7% | -0.1% |
| FC-3B | 1 | n3815 | 66 | 0.4463 | 13.8 | -0.7% | +0.7% |
| FC-3B | 1 | n4695 | 62 | 0.4721 | 12.61 | +1.6% | +0.4% |
| FC-3B | 1 | n734 | 58 | 0.3708 | 4.899 | -0.7% | -1.5% |
| FC-3B | 2 | n1761 | 13 | 0.3964 | 0.06956 |  |  |
| FC-3B | 2 | n2934 | 13 | 0.3965 | 0.04947 |  |  |
| FC-3B | 2 | n3815 | 12 | 0.342 | 0.04027 |  |  |
| FC-3B | 2 | n4695 | 13 | 0.3962 | 0.03339 |  |  |
| FC-3B | 2 | n734 | 13 | 0.3913 | 0.08675 |  |  |
| FC-3C | 1 | n1761 | 109 | 0.4926 | 7.921 | -0.3% | -1.4% |
| FC-3C | 1 | n2934 | 109 | 0.4947 | 8.373 | -0.9% | -2.7% |
| FC-3C | 1 | n3815 | 109 | 0.5096 | 9.839 | -0.0% | -0.8% |
| FC-3C | 1 | n4695 | 116 | 0.5186 | 10.11 | +0.4% | +0.3% |
| FC-3C | 1 | n734 | 101 | 0.5063 | 8.596 | -1.5% | -1.8% |
| FC-3C | 2 | n1761 | 13 | 0.4179 | 0.4309 |  |  |
| FC-3C | 2 | n2934 | 12 | 0.4193 | 0.3971 |  |  |
| FC-3C | 2 | n3815 | 14 | 0.419 | 0.4061 |  |  |
| FC-3C | 2 | n4695 | 13 | 0.4194 | 0.412 |  |  |
| FC-3C | 2 | n734 | 12 | 0.4186 | 0.4327 |  |  |
| FC-4B | 1 | n1761 | 66 | 0.4535 | 9.602 | -1.7% | -1.3% |
| FC-4B | 1 | n2934 | 66 | 0.4893 | 18.99 | -0.9% | -1.2% |
| FC-4B | 1 | n3815 | 59 | 0.5355 | 22.5 | -0.5% | -0.8% |
| FC-4B | 1 | n4695 | 58 | 0.5859 | 22.35 | -0.5% | -0.1% |
| FC-4B | 1 | n734 | 54 | 0.4554 | 15.18 | -1.8% | -2.2% |
| FC-4B | 2 | n1761 | 13 | 0.278 | 0.1469 |  |  |
| FC-4B | 2 | n2934 | 13 | 0.2591 | 0.1008 |  |  |
| FC-4B | 2 | n3815 | 13 | 0.2517 | 0.09344 |  |  |
| FC-4B | 2 | n4695 | 12 | 0.3191 | 0.09456 |  |  |
| FC-4B | 2 | n734 | 13 | 0.331 | 0.2466 |  |  |
| FC-4C | 1 | n1761 | 78 | 0.7144 | 22.97 | +2.6% | +1.2% |
| FC-4C | 1 | n2934 | 69 | 0.6684 | 21.31 | -0.2% | +1.8% |
| FC-4C | 1 | n3815 | 65 | 0.6745 | 21.14 | -0.1% | +0.0% |
| FC-4C | 1 | n4695 | 69 | 0.7244 | 9.193 | +0.1% | +0.4% |
| FC-4C | 1 | n741 | 66 | 0.6942 | 14.41 | +1.1% | -1.4% |
| FC-4C | 2 | n1761 | 13 | 0.6486 | 0.2595 |  |  |
| FC-4C | 2 | n2934 | 11 | 0.6525 | 0.255 |  |  |
| FC-4C | 2 | n3815 | 16 | 0.6146 | 0.2457 |  |  |
| FC-4C | 2 | n4695 | 15 | 0.6207 | 0.2339 |  |  |
| FC-4C | 2 | n741 | 14 | 0.6169 | 0.2487 |  |  |
