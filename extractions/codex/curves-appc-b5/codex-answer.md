Completed under `out/<figure_id>/`. Counts are **markers / traces / features**.

| Figure | Series | Counts | Printed angle |
|---|---|---:|---:|
| FC-1A | dr50-57 | 9 / 15 / 2 | 45.5° |
| FC-1A | dr73-88 | 4 / 16 / 2 | 47° |
| FC-1A | dr100-116 | 7 / 16 / 2 | 51° |
| FC-2A | dr33-53 | 6 / 20 / 2 | 49.5° |
| FC-2A | dr115-130 | 6 / 21 / 2 | 46.7° |
| FC-3A | dr0-15 | 5 / 21 / 2 | 38° |
| FC-3A | dr100-130 | 5 / 21 / 2 | 47° |
| FC-4A | dr95 | 5 / 22 / 2 | 53° |
| FC-4A | dr0 | 5 / 21 / 2 | 43° |

All three printed labels per axis were confirmed by eye:

| Figure | RMS residual x / y, psf | Checked x labels | Checked y labels |
|---|---:|---|---|
| FC-1A | 23.927 / 9.974 | 0, 2000, 4000 | 0, 3000, 6000 |
| FC-2A | 13.552 / 15.668 | 0, 2000, 5000 | 1000, 3000, 6000 |
| FC-3A | 3.404 / 12.825 | 1000, 3000, 5000 | 1000, 3000, 6000 |
| FC-4A | 6.727 / 2.267 | 1000, 3000, 5000 | 1000, 4000, 7000 |

C-1A’s uneven grid leaves its x RMS above the protocol’s 0.5% flag after detector adjustments. Symbol/fill mismatches, the obscured lower intercept, and the uncertain upper-fit filled-circle assignment are documented with wider bounds. C-2A–C-4A use measured tick anchors because they lack interior grids. C-4A’s line extension above the frame is included. Gap-related sampling shifts are noted; every recorded trace coordinate was checked on ink.

Each folder contains `cal-p1/`, `calibration-eye-checks.csv`, both points CSVs, `overlay-p1.png`, and `notes.md`, plus review crops.

Detailed notes: [FC-1A](<local path>), [FC-2A](<local path>), [FC-3A](<local path>), [FC-4A](<local path>).