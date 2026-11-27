# Arithmetic check of Table 5-T3: touchdown velocity against |V_v| = g tau (batch tables-s5-b1)

Written by `tools/check_mdrop_table.py`; our arithmetic, not the report's. A drop fits when |V_v| (with half a unit of its last printed digit) meets the interval g tau takes over the rounding of the printed tau. Two values of g, since the verdicts depend on which is used at this precision.

## g = 32.2 ft/s^2, the report's value for Earth (glossary, printed 2-2, PDF 27) (386.4000 in./sec.^2)

| NASA test | V_h printed | tau printed | g tau (in./sec.) | interval | abs V_v printed | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | .298 | 115.147 | 114.954 to 115.340 | 114.9 | differs |
| 2 | 83.5 | .177 | 68.393 | 68.200 to 68.586 | 60.5 | differs |
| 3 | 84.0 | .156 | 60.278 | 60.085 to 60.472 | 60.0 | differs |
| 4 | 0 | .304 | 117.466 | 117.272 to 117.659 | 117.3 | consistent |
| 5 | 83.4 | .146 | 56.414 | 56.221 to 56.608 | 60.8 | differs |
| 6 | 0 | .303 | 117.079 | 116.886 to 117.272 | 117.1 | consistent |
| 7 | 84.0 | .154 | 59.506 | 59.312 to 59.699 | 60.0 | differs |
| 8 | 0 | .306 | 118.238 | 118.045 to 118.432 | 118.0 | consistent |

Vertical drops (V_h 0): 3 of 4 are consistent with |V_v| = g tau within both printed roundings. Drops with a horizontal velocity: 0 of 4.

## g = standard gravity, 9.80665 m/s^2 (386.0886 in./sec.^2)

| NASA test | V_h printed | tau printed | g tau (in./sec.) | interval | abs V_v printed | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | .298 | 115.054 | 114.861 to 115.247 | 114.9 | consistent |
| 2 | 83.5 | .177 | 68.338 | 68.145 to 68.531 | 60.5 | differs |
| 3 | 84.0 | .156 | 60.230 | 60.037 to 60.423 | 60.0 | consistent |
| 4 | 0 | .304 | 117.371 | 117.178 to 117.564 | 117.3 | consistent |
| 5 | 83.4 | .146 | 56.369 | 56.176 to 56.562 | 60.8 | differs |
| 6 | 0 | .303 | 116.985 | 116.792 to 117.178 | 117.1 | consistent |
| 7 | 84.0 | .154 | 59.458 | 59.265 to 59.651 | 60.0 | differs |
| 8 | 0 | .306 | 118.143 | 117.950 to 118.336 | 118.0 | consistent |

Vertical drops (V_h 0): 4 of 4 are consistent with |V_v| = g tau within both printed roundings. Drops with a horizontal velocity: 1 of 4 (NASA Test No. 3).

Consistency is not the method: the report says the velocities were calculated using the measured interval tau and prints no formula.
