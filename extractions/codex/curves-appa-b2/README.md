# curves-appa-b2 blind reading

Read only the seven packet pages and their protocol; no other reader or earlier extraction was consulted. T/M/F denotes trace / marker / feature counts. RMS grain residuals are in log10 decades; percent residuals in percentage points. Native points use verified piecewise rulings.

| Figure | Average T/M/F | Upper T/M/F | Lower T/M/F | RMS decades / percentage points |
|---|---:|---:|---:|---:|
| [FA-2](FA-2/notes.md) | 51/15/4 | 51/4/4 | 49/6/4 | 0.002653 / 0.07505 |
| [FA-6](FA-6/notes.md) | 42/14/4 | 44/9/4 | 41/7/4 | 0.002426 / 0.05835 |
| [FA-18](FA-18/notes.md) | 50/15/4 | 52/6/4 | 51/6/4 | 0.002645 / 0.04927 |
| [FA-22](FA-22/notes.md) | 43/14/4 | 43/11/4 | 43/13/4 | 0.002491 / 0.04869 |
| [FA-26](FA-26/notes.md) | 30/7/4 | 30/5/4 | 31/4/4 | 0.002377 / 0.06895 |
| [FA-38](FA-38/notes.md) | 40/17/3 | 40/10/3 | 40/12/3 | 0.002431 / 0.06354 |
| [FA-46](FA-46/notes.md) | 50/15/4 | 47/4/4 | 50/6/4 | 0.002566 / 0.06578 |

Every figure directory contains `cal-p1/`, `calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`, and `notes.md`. Additional files retain crop evidence, calibration diagnostics, marker omissions, calibration sensitivity, helpers and delivery checks. Overlay colors are average red, upper green, lower blue.

All 12 printed grain labels and 11 percent labels were checked. The labelled fine frame is 0.02 mm; the coarse frame is beyond the interior 9.0 mm ruling and was excluded. Both percent frames carry 0/100 labels.

Ambiguities: FA-2, FA-6, FA-18 and FA-46 have merged near-zero tails and indistinguishable fine symbols; FA-26 approaches the zero frame with close range curves. FA-38 has close range curves and stacked coarse symbols. FA-22 has separated range curves over most of the plot, but coarse symbols and the end of line next to fine symbols remain uncertain. Bounds are widened at merges. Separately unidentified markers are omitted and located in each marker-omissions.csv; endpoint extent limits and remaining local order ambiguities are explicit in notes.md and delivery-check.json.
