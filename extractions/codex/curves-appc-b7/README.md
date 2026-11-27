Independent blind reading: curves-appc-b7

All required outputs are under the corresponding figure directory. Pixel coordinates refer to the original unrotated 300 dpi packet image; numerical axes and bounds are in psf.

| Figure | Series | Markers | Traces | Features | Affine RMS x/y (psf) |
|---|---|---:|---:|---:|---|
| [FC-8](FC-8/notes.md) | rs-loose | 6 | 11 | 3 | 4.008 / 10.432 |
| [FC-9A](FC-9A/notes.md) | rs-dense | 6 | 9 | 3 | 3.627 / 10.222 |
| [FC-9B](FC-9B/notes.md) | rs-dense | 4 | 8 | 3 | 4.145 / 10.990 |
| [FC-9C](FC-9C/notes.md) | rs-dense | 11 | 9 | 3 | 3.966 / 10.271 |
| [FC-10A](FC-10A/notes.md) | ps-loose | 6 | 10 | 3 | 3.457 / 10.235 |

Each directory contains `cal-p1/` (calibration, anchors, verified knots and affine diagnostic), `calibration-eye-checks.csv`, `points-p1.csv`, `points-p1-native.csv`, `overlay-p1.png`, and `notes.md`. The two point CSVs carry identical final piecewise psf values; pixel readings remain in both. Supporting vertex records and inspection crops are included.

By-eye printed labels for every figure: x zero (00 or 00.), 300.00, 700.00; y zero (00 or 00.), 400.00, 800.00. The multiplier is ten. All 17 detected lines per figure pass ink verification; no predicted/rejected lines are used.

Ambiguities: C-8 endpoint merges into the 400.00 grid; C-9A has grid-obscured marker sides and a cap sample adjacent to a marker gap; C-9B omits the 1000 and 2000 psf requested trace samples in white gaps and has a concealed terminal locus with broad bounds; C-9C omits the 1000 psf gap, retains a distinct triangle slightly left of zero within its bound, and has 11 visible triangles; C-10A terminal cap touches the last triangle, whose centroid has a half-symbol bound. Full per-point details and the printed-box comparisons are in each notes.md.

Validation: all submitted trace centres lie on dark page ink; target abscissae agree with the piecewise map within 0.002 psf after CSV rounding; marker centroids and apex-direction bounds were checked against their reconstructed vertices; final overlays were inspected. The pixel-darkness check is supplemental: grid and symbol ink can also be dark, so the page inspection settles attribution. No other reading or earlier extraction was consulted.
