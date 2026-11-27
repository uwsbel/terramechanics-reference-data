Completed the blind reading from the packet only.

| Figure | Data markers | Mean traces | Upper traces | Lower traces | RMS Dr | RMS φ (deg) |
|---|---:|---:|---:|---:|---:|---:|
| FC-16 | 11 | 25 | 26 | 25 | 0.001439 | 0.007557 |
| FC-17 | 6 | 23 | 23 | 25 | 0.001393 | 0.013624 |
| FC-18 | 6 | 22 | 23 | 23 | 0.001258 | 0.011222 |
| FC-19 | 2 | 21 | 22 | 22 | 0.001408 | 0.017705 |

Each curve has **2 feature points**: first and last/peak. No distinct knee was identified.

For every figure, eye-checks record **Dr: 0, 0.5, 1.0** and **φ: 30, 40, 50**. All 11 x lines and 5 y lines passed ink verification; native values use piecewise calibration.

Ambiguities documented with widened bounds:

- **FC-16:** frame-bisected circles and obscured terminals; mean sample at Dr=1.10 omitted.
- **FC-17:** overlaps and an interior circle speck; mean sample at Dr=0.15 omitted.
- **FC-18:** two touching circles and overlapping curves; mean sample at Dr=0.15 omitted.
- **FC-19:** mean’s left terminal merges with a circle.

Each `out/FC-16/` through `out/FC-19/` contains `cal-p1/`, `calibration-eye-checks.csv`, both point CSVs, `overlay-p1.png`, and `notes.md`, plus enlarged reading and ink-check crops.

[Reading summary](<local path>) includes counts and maximum residuals.