Written using only the supplied packet. [Download all files](<local path>) or open the [full summary and file list](<local path>).

Counts follow series order **n4695, n3815, n2934, n1761, lowest**—n734 except FC-4C’s n741. Upper totals include markers, traces, and features; lower panels contain markers only. Separate counts by kind are in the summary.

| Figure | Upper totals per series | Lower markers per series |
|---|---|---|
| FC-3B | 104, 105, 100, 101, 98 | 13, 12, 13, 13, 13 |
| FC-3C | 107, 106, 104, 110, 104 | 13, 14, 12, 13, 12 |
| FC-4B | 105, 110, 104, 110, 101 | 12, 14, 13, 13, 13 |
| FC-4C | 111, 95, 96, 107, 93 | 15, 16, 11, 13, 14 |

Calibration RMS residuals `(x, y)` use thousandths of an inch for x, psf for upper y, and thousandths for lower y.

| Figure | Upper RMS | Lower RMS |
|---|---|---|
| FC-3B | (0.297, 7.936) | (0.288, 0.159) |
| FC-3C | (0.364, 9.666) | (0.312, 0.287) |
| FC-4B | (0.299, 20.588) | (0.235, 0.038) |
| FC-4C | (0.462, 13.245) | (0.453, 0.110) |

Principal ambiguities:

- **FC-3B:** grid-sharing circle plateau and possible missing symbols.
- **FC-3C:** heading obscures the top grid; missing upper square and crowded lower symbols.
- **FC-4B:** tiny overlapping circles, an out-of-frame circle, and uneven upper grid spacing. Maximum y calibration residual is **35.687 psf**, above 0.5% of the span.
- **FC-4C:** triangle identities differ; curves share ink; lower frame/zero clusters are crowded.

Trace gaps exceeding five thousandths are explicitly documented rather than interpolated.

Each figure folder contains `cal-p1/` and `cal-p2/` with `anchors.csv` and `calibration.json`; `calibration-eye-checks.csv`; both `points-p1.csv` and `points-p2.csv` with their `-native.csv` counterparts; `overlay-p1.png`, `overlay-p2.png`, and `notes.md`. Supporting specs, crops, center audits, and gap audits are included. Schema, sequence, ink-sample, and archive checks passed.