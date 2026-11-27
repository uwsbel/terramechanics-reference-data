# Independent reading: curves-appc-b1

Only the supplied packet was used. No other reader or earlier extraction was accessed. All coordinates refer to the supplied unrotated 300-dpi page images.

In the count table, upper counts are marker / trace / feature; lower counts are markers only. Lower panels have no drawn connecting traces.

| Figure | Series | Upper M / T / F | Lower markers |
|---|---|---:|---:|
| FC-1C | n3520 | 15 / 118 / 3 | 14 |
| FC-1C | n2935 | 10 / 93 / 3 | 13 |
| FC-1C | n2345 | 13 / 117 / 5 | 12 |
| FC-1C | n1760 | 10 / 113 / 3 | 14 |
| FC-1C | n1172 | 12 / 113 / 3 | 12 |
| FC-1C | n587 | 12 / 115 / 3 | 13 |
| FC-1C | n294 | 9 / 79 / 3 | 9 |
| FC-1D | n3520 | 12 / 118 / 3 | 13 |
| FC-1D | n2935 | 10 / 117 / 3 | 14 |
| FC-1D | n2345 | 12 / 112 / 3 | 15 |
| FC-1D | n1468 | 12 / 117 / 3 | 13 |
| FC-1D | n587 | 12 / 117 / 3 | 12 |
| FC-1D | n294 | 8 / 77 / 3 | 8 |
| FC-1D | n0 | 7 / 61 / 3 | 7 |
| FC-2B | n4400 | 15 / 118 / 3 | 24 |
| FC-2B | n3660 | 15 / 122 / 4 | 24 |
| FC-2B | n2995 | 17 / 117 / 3 | 24 |
| FC-2B | n2200 | 17 / 116 / 3 | 24 |
| FC-2B | n1468 | 16 / 88 / 3 | 20 |
| FC-2B | n734 | 24 / 117 / 3 | 16 |
| FC-2C | n4400 | 16 / 73 / 3 | 10 |
| FC-2C | n3660 | 17 / 77 / 3 | 9 |
| FC-2C | n2995 | 12 / 68 / 3 | 9 |
| FC-2C | n2200 | 11 / 62 / 3 | 12 |
| FC-2C | n1468 | 8 / 38 / 3 | 4 |
| FC-2C | n734 | 5 / 31 / 3 | 3 |

Calibration RMS residuals are in printed native units: x and lower y are thousandths of an inch; upper y is psf.

| Figure | Upper RMS x / y | Lower RMS x / y |
|---|---:|---:|
| FC-1C | 0.409 / 7.910 | 0.370 / 0.223 |
| FC-1D | 0.343 / 5.705 | 0.298 / 0.529 |
| FC-2B | 0.351 / 3.920 | 0.377 / 0.830 |
| FC-2C | 0.465 / 2.678 | 0.366 / 0.637 |

Each calibration has three by-eye checks per axis per panel (12 per figure). All RMS residuals are below 0.5% of axis span. FC-2B lower y has a maximum affine residual of 1.298 thousandths, or 0.65% of its span: the zero grid is visibly off the midpoint of the frame. This is explicitly flagged in its notes.

The maximum neighboring trace displacement gap is 4.611 thousandths; all are below five. Clean trace bounds are half the visible run thickness. Samples sharing marker ink have a 16-px vertical bound; those sharing horizontal-grid ink have at least an 8-px bound and per-row notes. They do not assert a separately resolved author ordinate. No interpolated ordinate is presented as observed ink.

Material ambiguities:

- FC-1C: close initial 3520/2935 branches; doubled triangle ink; two square maxima; crowded lower origin and x/plus grid cluster; terminal symbols beside or beyond x=250. See [notes](FC-1C/notes.md).
- FC-1D: filled-circle zero-stress series; markers departing from author fits; overlapping lower triangles and origin/frame symbols; above-+100 dilation symbols; one possible early lower x omitted. See [notes](FC-1D/notes.md).
- FC-2B: short leftward initial n3660 bend preserved in drawing order; thick n734 stroke near the 1000 grid; tightly stacked lower symbols; lower zero-grid nonuniformity; printed square stress 2935 versus required n2995. See [notes](FC-2B/notes.md).
- FC-2C: short curves with distinct endpoints; lower symbols too small/merged to recover several early markers, which are explicitly omitted with approximate locations; printed square stress 2935 versus required n2995; tau (PCF) legend-header typo. See [notes](FC-2C/notes.md).

Requested files in each figure folder:

- cal-p1/anchors.csv and cal-p1/calibration.json
- cal-p2/anchors.csv and cal-p2/calibration.json
- calibration-eye-checks.csv
- points-p1.csv and points-p1-native.csv
- points-p2.csv and points-p2-native.csv
- overlay-p1.png and overlay-p2.png
- notes.md

Additional review/provenance files include labeled reading crops, cropped QA overlays, final reading.json, counts.json, center-check CSVs, and target-column gap JSONs. [manifest.csv](manifest.csv) lists every output file. Shared summaries: [counts.csv](counts.csv), [calibration-summary.csv](calibration-summary.csv), [trace-coverage.csv](trace-coverage.csv), [validation.txt](validation.txt).

Regeneration: run read_support.py with a figure ID using its final reading.json, then finalize_metadata.py for FC-1D/FC-2B/FC-2C, then audit_outputs.py and write_summary.py. build_*.py and finish_1c.py preserve the initial hand-reading stage and are not the final regeneration source; do not rerun them over the corrected reading.json.
