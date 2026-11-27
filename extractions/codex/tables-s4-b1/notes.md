# Figure 4-6a transcription notes

## Caption and column headings

The caption appears below the table on `p0193.png` (printed page 4-8).

> Figure 4-6a. Subscale Drag Test Results - Soil No. 1 - RS Loose

The 14 printed columns match the requested order. Underscores represent subscripts and the slash in each derived heading represents a stacked fraction. The `note` field is the fifteenth CSV column.

| Column | Printed heading | Printed unit |
| --- | --- | --- |
| 1 | Run Number | |
| 2 | `D` | Inch |
| 3 | `d` | Inch |
| 4 | `V_H` | fps |
| 5 | `ḡ_p` | |
| 6 | `D_r` | |
| 7 | `γ` | Lb./Ft.³ |
| 8 | `F_D` | Lb. |
| 9 | `F_V` | Lb. |
| 10 | `F_D / (d γ A_ft)` | |
| 11 | `V_H / √(dg)` | |
| 12 | `F_D / A_ft` | |
| 13 | `F_V / A_pt` | |
| 14 | `α` | Deg. |

## Definitions on the supplied context pages

| Symbol | Printed wording and location |
| --- | --- |
| `A_ft` | “Total Horizontal Frontal Area - A_ft” (`p0191.png`, printed page 4-6, Figure 4-4, left callout). |
| `A_pt` | “Vertical Frontal Area - A_pt” (same figure, upper callout). |
| `d` | “Vertical Displacement - d” (`p0191.png`, Figure 4-5, trace C in the legend below the record). Figure 4-4 puts `d` on the vertical dimension from the soil surface to the dashed footpad reference. |
| `F_D` | “Drag Load - F_D” (`p0191.png`, Figure 4-5, trace H). Figure 4-4 labels the horizontal force arrow “F_D or F_ap.” |
| `F_V` | “Vertical Load - F_V” (`p0191.png`, Figure 4-5, trace F). Figure 4-4 labels the vertical force arrow “F_V or F_np.” |
| `V_H` | “Horizontal Velocity - V_H” (`p0191.png`, Figure 4-5, trace I). Figure 4-4 labels the velocity arrow “V_H or V_ap.” |
| `γ` | Neither context page explicitly defines `γ`. The paragraph above section 4.3 on `p0192.png` (printed page 4-7) says, “Soil relative and bulk density data were determined from dynamic penetrometer tests (ḡ_p) of the soil bed.” |
| `g` | Neither context page defines the standalone `g` in `√(dg)`. Figure 4-5, trace B, uses `g` in the sensitivity unit `g/inch` for “Horizontal Acceleration.” |
| `α` | “Footpad Pitch Angle, α” (`p0191.png`, Figure 4-5, below the trace legend). Figure 4-4 marks `α` between the horizontal and inclined lines. |

## Damaged characters and marks

All data characters were readable. The most damaged digits were the first `1` in run 1-21 `gamma_pcf`, the `8` in run 1-22 `alpha_deg`, and the `2` in run 1-33 `FD_over_Aft`. Their remaining strokes support the readings below. Positions `(u, v)` are approximate pixels in the original, unrotated `p0193.png`, measured right and down from its upper-left corner. Positions point to the affected character or mark.

| Run | CSV field | Scan position `(u, v)` | Reading or mark |
| --- | --- | --- | --- |
| 1-1 | `VH_over_sqrt_dg` | (574, 1695) | `2.4`. The `4` has a chipped foot and a clear crossbar. |
| 1-1 | `FD_over_Aft` | (574, 1500) | `0.57`. The `5` retains its top bar and lower curve. |
| 1-1 | `FV_over_Apt` | (574, 1309) | `0.43`. The `4` retains its crossbar and detached foot. |
| 1-2 | `gp_bar` | (637, 3062) | `10.8`. The leading `1` has a chipped top serif. |
| 1-3 | `run_number` | (696, 3912) | The leading `1` has a split stem. |
| 1-7 | `VH_over_sqrt_dg` | (931, 1695) | `1.1`. The final `1` has a split stem. |
| 1-10 | `run_number` | (1052, 3826) | The final `0` has a nick in the right side of its oval. |
| 1-10 | `D_in` | (1052, 3602) | `6`. The rough upper stroke and lower loop are visible. |
| 1-10 | `FD_over_Aft` | (1048, 1477) | `0.75`. The `5` retains its top bar and lower curve. |
| 1-11 | `VH_over_sqrt_dg` | (1119, 1717) | `4.7`. The decimal point is chipped. |
| 1-12 | `alpha_deg` | (1164, 1120) | `28.8`. The final `8` has a chipped lower-left curve. |
| 1-13 | `run_number` | (1227, 3857) | The `1` before the `3` has a detached foot. |
| 1-13 | `VH_fps` | (1225, 3120) | `5.45`. The last `5` has a chipped stroke and visible top bar and lower curve. |
| 1-14 | `gamma_pcf` | (1284, 2608) | `41.1`. The first `1` has a detached foot. |
| 1-15 | `VH_fps` | (1342, 3122) | `5.17`. The `7` has a gap near the top right. |
| 1-16 and 1-17 | `FV_lb` | (1427, 2182) | A short stroke extends between the leading `2`s of `25.2` and `20.9`. |
| 1-17 | `FD_over_d_gamma_Aft` | (1455, 1953) | `111.0`. The third `1` has a split stem. |
| 1-18 | `d_in` | (1520, 3401) | `1 1/2`. The numerator `1` has a split stem. |
| 1-21 | `gamma_pcf` | (1693, 2638), (1693, 2608) | `41.1`. The `4` retains its crossbar. The first `1` has lost much of its stem, but the top and foot are visible. |
| 1-21 | `FD_over_Aft` | (1704, 1538) | `2.27`. The point touches the foot of the following `2`. |
| 1-21 | `alpha_deg` | (1690, 1120) | `28.4`. The `4` has a chipped foot and a clear crossbar. |
| 1-22 | `alpha_deg` | (1747, 1164) | `28.4`. The `8` has an intact upper loop, with the lower-left arc interrupted and the lower return stroke visible. |
| 1-24 | `FD_over_d_gamma_Aft` | (1844, 1989) | Short stray stroke above the leading `6` of `61.6`. |
| 1-25 | `gp_bar` | (1928, 2984) | `12.0`. The `0` has a break at the upper left. |
| 1-26 | `d_in` | (1962, 3454) | Fleck above the `2`. |
| 1-26 | `gp_bar` | (1988, 3034) | `12.4`. The `2` has a split foot. |
| 1-27 | `gp_bar` | (2047, 2984) | `12.1`. The final `1` is split near the foot. |
| 1-27 | `gamma_pcf` | (2047, 2557) | `41.1`. The final `1` is split below the top serif. |
| 1-28 and 1-29 | `FV_lb` | (2086, 2181), (2135, 2182) | Stray marks near the `4` of `48.2` and above the first `2` of `21.6`. |
| 1-29 | `D_in` | (2166, 3606) | `6`. The lower loop is chipped but visible. |
| 1-31 | `FD_over_d_gamma_Aft` | (2279, 1981), (2279, 1902) | `59.7`. The `5` has a detached top bar and the `7` has a nick in its diagonal. |
| 1-32 | `Dr` | (2344, 2831) | `0`. Its oval is broken at the lower right. |
| 1-33 | `Dr` | (2402, 2831) | `0`. Its oval is broken at the upper left. |
| 1-33 | `FD_over_d_gamma_Aft` | (2397, 1980) | `47.1`. The `4` retains its crossbar and detached foot. |
| 1-33 | `FD_over_Aft` | (2397, 1508) | `3.27`. The `2` has a missing middle stroke. Its curved top and flat base with an upturned right tip are visible. |
| 1-33 | `FV_over_Apt` | (2395, 1307) | `1.77`. The first `7` has a split diagonal. |

The table is upright after turning the scan 90 degrees clockwise. It contains 32 runs, beginning at `1-1` and ending at `1-33`. The printed list goes directly from `1-8` to `1-10`. There are small breaks in some ruling lines, scattered specks, and a dark scan border outside the table. The CSV includes the printed precision and fractions, including `0.84` in `FV_over_Apt` for run `1-28`.
