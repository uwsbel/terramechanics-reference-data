Completed the blind reading: **100 rows for F2-42; 151 for F2-44**.

| Figure | Series | Trace | Feature |
|---|---|---:|---:|
| F2-42 | lpt22 | 19 | 5 |
| | lpt23 | 19 | 5 |
| | lpt24 | 22 | 5 |
| | lpt25 | 21 | 4 |
| F2-44 | lpt24 | 21 | 4 |
| | lpt73 | 20 | 5 |
| | lpt74 | 26 | 5 |
| | lpt69 | 31 | 6 |
| | lpt64a | 29 | 4 |

No markers were found.

Calibration RMS residuals `(penetration, load)` are **(0.00658 in, 1.042 lb)** and **(0.00258 in, 1.632 lb)** respectively. Maximum residuals are `(0.01110 in, 3.578 lb)` and `(0.00483 in, 2.740 lb)`. All intended grid knots passed ink verification. Every printed grid label was checked by eye; maximum position differences were **1.20 px** and **1.42 px**.

Ambiguities include overlapping initial rises, crossings, F2-42 A’s termination against C, and F2-44’s merged recovery strokes and visible starts above zero load. Bounds and notes retain these uncertainties.

Both output folders contain `cal-p1/`, calibration eye checks, both point CSVs, overlays, `notes.md`, and supporting audits/crops. Details: [F2-42 notes](out/F2-42/notes.md), [F2-44 notes](out/F2-44/notes.md).

The packet lacked `check_trace_ink.py`; local ink audits and visual overlay checks were completed.