# Calibration sensitivity: piecewise against affine maps

Per canonical series: the largest difference between each point's piecewise value (D-025, the data) and the affine value of the same pixels on the same reading's submitted calibration; and, for traces, the change of the initial secant slope (first sample to the first sample beyond 10% of the trace's x extent) and of the overall secant (first to last sample), piecewise relative to affine. These are correlated calibration sensitivities, not reading bounds; a slope change at a grid line is drafting, not soil behaviour.

| figure | panel | series | points | max dx | max dy | initial secant | overall secant |
|---|---|---|---|---|---|---|---|
| FC-5B | 1 | n1761 | 72 | 1.44 | 1.588 | +6.4% | +1.0% |
| FC-5B | 1 | n2934 | 92 | 1.418 | 3.864 | +6.4% | +0.7% |
| FC-5B | 1 | n3815 | 86 | 1.413 | 5.55 | +6.5% | +0.6% |
| FC-5B | 1 | n4695 | 80 | 1.407 | 5.613 | +6.0% | +0.2% |
| FC-5B | 1 | n734 | 98 | 1.415 | 1.379 | +7.1% | +2.0% |
| FC-5B | 2 | n1761 | 13 | 1.503 | 0.1921 |  |  |
| FC-5B | 2 | n2934 | 13 | 1.524 | 0.03544 |  |  |
| FC-5B | 2 | n3815 | 13 | 1.516 | 0.07902 |  |  |
| FC-5B | 2 | n4695 | 13 | 1.537 | 0.03975 |  |  |
| FC-5B | 2 | n734 | 13 | 1.499 | 0.1181 |  |  |
| FC-6B | 1 | n1761 | 74 | 3.719 | 10.99 | -1.9% | +0.1% |
| FC-6B | 1 | n2934 | 71 | 3.732 | 11.02 | +10.8% | +1.4% |
| FC-6B | 1 | n3815 | 77 | 3.83 | 8.665 | +1.6% | +0.8% |
| FC-6B | 1 | n4695 | 73 | 3.788 | 15.87 | +11.4% | +2.5% |
| FC-6B | 1 | n734 | 71 | 3.654 | 2.838 | +5.5% | +7.5% |
| FC-6B | 2 | n1761 | 13 | 4.322 | 0.3264 |  |  |
| FC-6B | 2 | n2934 | 13 | 4.337 | 0.206 |  |  |
| FC-6B | 2 | n4695 | 13 | 4.342 | 0.1683 |  |  |
| FC-6B | 2 | n734 | 13 | 4.35 | 0.5011 |  |  |
| FC-6C | 1 | n1961 | 77 | 0.8428 | 3.793 | +2.9% | +0.5% |
| FC-6C | 1 | n2934 | 79 | 0.868 | 11.61 | +2.6% | -0.6% |
| FC-6C | 1 | n3815 | 78 | 0.8734 | 12.39 | +3.3% | -0.5% |
| FC-6C | 1 | n4695 | 77 | 0.8936 | 11.2 | +4.6% | -0.0% |
| FC-6C | 1 | n714 | 79 | 0.8285 | 8.234 | +3.9% | +8.1% |
| FC-6C | 2 | n1961 | 13 | 0.9153 | 0.1026 |  |  |
| FC-6C | 2 | n2934 | 13 | 0.9123 | 0.07233 |  |  |
| FC-6C | 2 | n3815 | 13 | 0.9179 | 0.02727 |  |  |
| FC-6C | 2 | n4695 | 12 | 0.7719 | 0.06957 |  |  |
| FC-6C | 2 | n714 | 13 | 0.927 | 0.1024 |  |  |
| FC-6D | 1 | n147 | 83 | 2.896 | 12.22 | +11.1% | +4.3% |
| FC-6D | 1 | n1761 | 96 | 2.867 | 11.54 | +10.4% | +1.8% |
| FC-6D | 1 | n2934 | 98 | 2.732 | 11.28 | +0.9% | +0.2% |
| FC-6D | 1 | n3814 | 94 | 2.886 | 9.472 | +6.9% | +0.4% |
| FC-6D | 1 | n4695 | 96 | 2.879 | 16.53 | +7.2% | +0.2% |
| FC-6D | 2 | n147 | 25 | 4.168 | 0.09169 |  |  |
| FC-6D | 2 | n1761 | 16 | 4.168 | 0.00825 |  |  |
| FC-6D | 2 | n2934 | 16 | 4.218 | 0.08536 |  |  |
| FC-6D | 2 | n3814 | 18 | 4.202 | 0.1351 |  |  |
| FC-6D | 2 | n4695 | 17 | 4.139 | 0.1493 |  |  |
