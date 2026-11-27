Completed under `out/<figure_id>/`. [Output index](out/README.md)

| Figure | Series | Markers | Trace | Features | Calibration RMS x/y, psf |
|---|---|---:|---:|---:|---:|
| FC-10B | ps-loose | 3 | 10 | 3 | 3.458 / 10.179 |
| FC-10C | ps-loose | 9 | 10 | 3 | 4.030 / 10.972 |
| FC-11A | rsm-loose | 5 | 11 | 3 | 3.841 / 10.016 |
| FC-11B | rsm-loose | 5 | 10 | 3 | 3.442 / 10.867 |
| FC-11C | rsm-loose | 10 | 11 | 3 | 5.599 / 10.825 |

Each calibration has 8 verified x lines and 9 verified y lines. Recorded by-eye checks per figure: x labels **100.00, 400.00, 700.00**; y labels **100.00, 400.00, 800.00**, with the ×10 conversion to psf.

Ambiguities are documented with widened bounds: touching ink in FC-10B, the terminal line/triangle merge in FC-10C, grid crossings in FC-11A and FC-11C, and overlapping triangle pairs in FC-11B/FC-11C. **FC-11B’s 2500 psf trace sample was omitted because it falls in a drawn gap.**

Every figure folder contains the requested calibration files, both point CSVs, eye-check CSV, overlay and notes. Notes include printed box transcriptions and numerical slope/intercept differences. Supporting crops, reconstructed vertices, thickness checks, [summary](out/summary.csv), and [verification results](out/verification.json) are also written.