Completed **332 rows**, with **zero markers**. Counts below are **trace / feature**.

| Figure | Counts by series | Calibration RMS: in / lb | Labels checked by eye: penetration; load |
|---|---|---|---|
| F2-45 | lpt95: 30/25; lpt79: 26/5 | 0.00250 / 0.175 | 0,3,7; 0,100,250 |
| F2-46 | lpt98: 26/18; lpt89: 26/7 | 0.00658 / 0.512 | 0,3,6; 0,300,600 |
| F2-47 | lpt101: 26/7; lpt91: 30/14 | 0.00369 / 1.585 | 0,3,7; 0,1000,2000 |
| F2-48 | lpt87: 34/17; lpt85: 34/7 | 0.06255 / 0.944 | 0,1,2,8; 0,600,1200 |

All final calibration knots pass ink verification. Reported values use piecewise calibration.

The main ambiguities are documented: shared origin/frame junctions; extrapolation beyond labelled load lines on F2-45 and F2-46; F2-47’s clear crossing near 1.3 inches and indistinguishable dashed continuation beyond roughly 6 inches; and F2-48’s shortened 0–1-inch grid interval.

Each `out/<figure_id>/` contains `cal-p1/`, `calibration-eye-checks.csv`, both requested point CSVs, `overlay-p1.png`, and `notes.md`, plus QA crops and audits. Maximum residuals and calibration sensitivity are recorded there.

The D031 checker was absent from the packet; visual review and a supplemental ink-distance audit were completed. All points have dark ink within 2 pixels.