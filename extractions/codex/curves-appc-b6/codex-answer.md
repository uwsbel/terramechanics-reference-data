Completed under `out/FC-5A/`, `out/FC-6A/`, and `out/FC-7A/`.

| Figure | Series | Markers | Traces | Features |
|---|---|---:|---:|---:|
| FC-5A | dr2-13 | 5 | 21 | 2 |
| | dr30 | 5 | 20 | 2 |
| | dr48 | 5 | 17 | 2 |
| | dr77 | 5 | 13 | 2 |
| FC-6A | dr5-40 | 5 | 21 | 1 |
| | dr19-28 | 4 | 20 | 1 |
| | dr103-107 | 5 | 20 | 1 |
| FC-7A | dr53 | 6 | 15 | 2 |
| | dr100 | 6 | 15 | 2 |

FC-5A and FC-6A each also contain **one unassigned marker**, with wide bounds and an ambiguity note.

| Figure | Calibration RMS x / y | Printed labels checked x; y |
|---|---|---|
| FC-5A | 4.970 / 7.583 psf | 0, 2000, 5000; 1000, 3000, 5000 |
| FC-6A | 3.040 / 6.328 psf | 1000, 3000, 5000; 1000, 4000, 6000 |
| FC-7A | 0.02601 / 0.03129 psi | 0, 15, 30; 0, 20, 35 |

All by-eye checks pass within eye bounds plus calibration RMS. No calibration lines are predicted.

Ambiguities are documented: C-5A’s obscured origin symbol; C-6A’s unlisted downward triangle and obscured square-fit left join. **C-6A prints no angle labels**, so those features are omitted. C-7A’s labels read **45° and 50.5°**.

Each folder contains `cal-p1/`, `calibration-eye-checks.csv`, both point CSVs, `overlay-p1.png`, `notes.md`, and supporting check images. Counts and verification results are also saved in [batch-summary.json](<local path>).