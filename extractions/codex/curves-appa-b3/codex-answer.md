Completed **314 points: 231 trace and 83 feature points**, using only this packet.

Every series has **11 trace samples**. Feature counts below are mean/upper/lower. Calibration RMS residuals are percentages of the axis spans; y uses the reciprocal span.

| Figure | Features M/U/L | RMS x / y (%) | Pcf labels checked by eye |
|---|---:|---:|---|
| FA-3 | 4/4/4 | 0.134 / 0.156 | 25, 45, 65 |
| FA-7 | 4/4/4 | 0.139 / 0.163 | 25, 45, 65 |
| FA-19 | 4/4/4 | 0.131 / 0.104 | 55, 85, 115 |
| FA-23 | 4/4/4 | 0.204 / 0.049 | 55, 75, 100 |
| FA-27 | 4/3/4 | 0.132 / 0.094 | 55, 85, 115 |
| FA-39 | 4/4/4 | 0.083 / 0.072 | 55, 85, 115 |
| FA-47 | 4/4/4 | 0.085 / 0.075 | 55, 85, 115 |

Dr labels **0, 0.5 and 1.0** were checked on every figure. All calibration knots passed ink verification. Maximum affine x residuals exceed 0.5% for FA-19, FA-23 and FA-27; these are documented, and native values use verified piecewise maps.

Ambiguities recorded: FA-27 lacks an upper left-end label; FA-47 has one shared **89.4** annotation with uncertain individual leader association and merged end ink. Frame-overlap uncertainty and the prompt’s scale discrepancies are also documented.

Under each figure directory in [out](<local path>), I wrote `cal-p1/`, `calibration-eye-checks.csv`, both point CSVs, `overlay-p1.png`, and `notes.md`, plus review crops and validation records.