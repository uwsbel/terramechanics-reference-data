Completed the blind reading from the supplied packet. The eight panels yielded **324 trace samples and 72 features**. The figures contain no plotted symbols.

| Figure | Series | Trace | Feature | Affine RMS time (s) | Affine RMS load or depth |
|---|---|---:|---:|---:|---:|
| F5-24 | `pen` | 38 | 6 | 0.0000570 | 0.00584 in |
| F5-25 | `strut3` | 44 | 12 | 0.0000510 | 0.140 lb |
| F5-25 | `strut2` | 41 | 8 | 0.0000510 | 0.198 lb |
| F5-25 | `strut1` | 59 | 10 | 0.0000510 | 0.158 lb |
| F5-31 | `pen` | 36 | 6 | 0.0000620 | 0.00650 in |
| F5-32 | `strut3` | 35 | 11 | 0.0000657 | 0.150 lb |
| F5-32 | `strut2` | 37 | 12 | 0.0000657 | 0.132 lb |
| F5-32 | `strut1` | 34 | 7 | 0.0000657 | 0.140 lb |

I checked every printed axis label by eye. Both tension panels for `strut2` print `-60` above `+40`. The eye-check CSVs preserve `-60`, and the measured ruling anchors +60 lb. Both damaged `.09` labels have measurable tick remnants. F5-32’s `.10` label has too little ruling ink to anchor, so times beyond `.09` s are flagged as extrapolated. All three traces end near `.103` s.

The main ambiguities are the F5-25 `strut1` crest at −80 lb, the F5-32 `strut3` shoulder along zero, and the F5-32 `strut1` start within the left frame. The damaged F5-32 inset reads 83.75 in./s horizontally. Table 5-T3 gives 83.5 in./s.

Each figure folder contains `cal-p<n>/`, `calibration-eye-checks.csv`, both point CSVs per panel, `overlay-p<n>.png`, and `notes.md` with the label transcriptions, calibration details, and inset conditions. [F5-24](<<local path>>), [F5-25](<<local path>>), [F5-31](<<local path>>), [F5-32](<<local path>>).