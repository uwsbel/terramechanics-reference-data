Completed from the packet only. Full details are in [summary.md](/<local path>).

Upper counts are **markers / traces / features**; lower counts are markers.

| Figure | Series | Upper | Lower |
|---|---|---:|---:|
| FC-1C | n3520 | 15 / 118 / 3 | 14 |
| FC-1C | n2935 | 10 / 93 / 3 | 13 |
| FC-1C | n2345 | 13 / 117 / 5 | 12 |
| FC-1C | n1760 | 10 / 113 / 3 | 14 |
| FC-1C | n1172 | 12 / 113 / 3 | 12 |
| FC-1C | n587 | 12 / 115 / 3 | 13 |
| FC-1C | n294 | 9 / 79 / 3 | 9 |
| FC-1D | n3520 | 12 / 118 / 3 | 13 |
| FC-1D | n2935 | 10 / 117 / 3 | 14 |
| FC-1D | n2345 | 12 / 112 / 3 | 15 |
| FC-1D | n1468 | 12 / 117 / 3 | 13 |
| FC-1D | n587 | 12 / 117 / 3 | 12 |
| FC-1D | n294 | 8 / 77 / 3 | 8 |
| FC-1D | n0 | 7 / 61 / 3 | 7 |
| FC-2B | n4400 | 15 / 118 / 3 | 24 |
| FC-2B | n3660 | 15 / 122 / 4 | 24 |
| FC-2B | n2995 | 17 / 117 / 3 | 24 |
| FC-2B | n2200 | 17 / 116 / 3 | 24 |
| FC-2B | n1468 | 16 / 88 / 3 | 20 |
| FC-2B | n734 | 24 / 117 / 3 | 16 |
| FC-2C | n4400 | 16 / 73 / 3 | 10 |
| FC-2C | n3660 | 17 / 77 / 3 | 9 |
| FC-2C | n2995 | 12 / 68 / 3 | 9 |
| FC-2C | n2200 | 11 / 62 / 3 | 12 |
| FC-2C | n1468 | 8 / 38 / 3 | 4 |
| FC-2C | n734 | 5 / 31 / 3 | 3 |

Calibration RMS residuals use printed units: displacement in thousandths of an inch and upper stress in psf.

| Figure | Upper RMS x / y | Lower RMS x / y |
|---|---:|---:|
| FC-1C | 0.409 / 7.910 | 0.370 / 0.223 |
| FC-1D | 0.343 / 5.705 | 0.298 / 0.529 |
| FC-2B | 0.351 / 3.920 | 0.377 / 0.830 |
| FC-2C | 0.465 / 2.678 | 0.366 / 0.637 |

All figures have 12 eye checks. Maximum neighboring trace spacing is **4.611 thousandths**. Shared-ink samples have wider bounds and explicit notes.

Material ambiguities:

- **FC-1C:** merging initial branches, doubled triangle ink, two square maxima, and crowded lower x/plus symbols.
- **FC-1D:** overlapping lower triangles, markers departing from fitted curves, dilation markers above +100, and one unresolved early lower x.
- **FC-2B:** initial n3660 reversal preserved; dense lower stacks; lower calibration maximum residual **1.298 thousandths**, flagged as 0.65% of span.
- **FC-2C:** several unresolved lower markers omitted with approximate locations. Both PS figures print **2935**, while the required ID remains `n2995`. FC-2C also prints “τ (PCF).”

Each figure folder contains both calibration directories, eye-check CSV, four point CSVs, two overlays, and `notes.md`. Review crops and helper records are also included. The [file manifest](/<local path>) lists every output.