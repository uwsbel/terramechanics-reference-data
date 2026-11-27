Completed under [out/](<local path>), using only the packet.

| Figure | Series | Markers / traces / features | Calibration RMS x / y (psf) |
|---|---|---:|---:|
| FC-8 | rs-loose | 6 / 11 / 3 | 4.008 / 10.432 |
| FC-9A | rs-dense | 6 / 9 / 3 | 3.627 / 10.222 |
| FC-9B | rs-dense | 4 / 8 / 3 | 4.145 / 10.990 |
| FC-9C | rs-dense | 11 / 9 / 3 | 3.966 / 10.271 |
| FC-10A | ps-loose | 6 / 10 / 3 | 3.457 / 10.235 |

Every figure has by-eye checks of printed x labels zero, `300.00`, `700.00`, and y labels zero, `400.00`, `800.00`, with the ×10 conversion. All grid lines passed ink verification.

Ambiguities are documented: C-8’s endpoint merges with a grid line; C-9A has grid-obscured triangles; C-9B’s terminal tip is concealed and has broad bounds; C-9C includes a distinct zero-axis triangle; C-10A’s cap touches its last triangle. Rule 7 required omitting gap samples at C-9B’s 1000/2000 psf and C-9C’s 1000 psf.

Each figure directory contains `cal-p1/`, both point CSVs, `calibration-eye-checks.csv`, `overlay-p1.png`, and `notes.md`, including printed-box transcriptions and numerical comparisons.