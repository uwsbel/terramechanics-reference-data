Completed the blind reading of Figure 2-54. All three record labels match the index.

| Panel / series | Trace | Feature | Markers | Affine time RMS / max (ms) | Affine G RMS / max (g) |
|---|---:|---:|---:|---:|---:|
| 1 / `r53958` | 78 | 9 | 0 | 0.434 / 0.667 | 0.199 / 0.538 |
| 2 / `r54025` | 90 | 11 | 0 | 0.434 / 0.684 | 0.254 / 1.177 |
| 3 / `r5465` | 100 | 8 | 0 | 0.404 / 0.626 | 0.225 / 0.895 |

By eye, the `.01 sec.` arrows meet the adjacent +30 and +40 ms lines. I checked all 12 timing lines in each panel and matched each printed G label to its ruler tick. The native CSVs use the verified piecewise calibrations.

The dashed zero datums sit 9–11 px above the solid ruler zeros. I used the dashed datums for 0 g, which makes the near-zero readings sensitive to that choice. The printed zero hides the +2 ms sample in all three panels, and the panel 2 dash obscures the expected 1 g tick. The notes document the panel 1 onset gap and the widened bounds where traces merge with the grid, dashes, or frame.

The [output folder](/<local path>) contains six point CSVs, three overlays, three calibration folders, the eye-check CSV, and `notes.md`.