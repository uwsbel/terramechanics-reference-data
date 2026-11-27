# Figure 4-19 · Force and displacement versus time

Read from `packet/p0208.png`, printed page 4-23. Panel 1 is vertical force in pounds. Panel 2 is displacement into the soil in inches. Both use milliseconds. The context on printed pages 4-7, 4-21 and 4-22 describes the subscale impact program and identifies these as vertical impacts at about 6 ft/s. The figure gives the footpad diameter as 6.17 in.

| Series ID | Printed legend | Trace |
| --- | --- | --- |
| `run4` | Run No. 4, Dᵣ = 0 | Solid |
| `run10` | Run No. 10, Dᵣ = 0.45 | Dotted |
| `run12` | Run No. 12, Dᵣ = 0.65 | Alternating long and short dashes |

The series IDs agree with the printed legend. The Run 12 sample in the legend includes a short dash between long ones. No plotted point symbols were visible.

## Calibration and time labels

The eye-check CSV records every numbered time line in both panels and the unnumbered right frame. The numerals 0 through 100 run in 10 ms increments. The next three numerals are literally **120, 130 and 140**, each beneath one of the next three consecutive grid lines. There is one further line at the right frame with no numeral. The same layout appears in both panels. I assigned 110, 120, 130 and 140 ms to those four physical lines by extending the 0–100 cadence. The last three printed numerals would shift the calibration by one division if taken literally. The assigned values are used in the native files. The CSV also records the eye checks for the force and displacement scales.

The grid fits use measured ink profiles. The 500 lb line can be tied to its numeral at the left edge, and the short visible segment is represented in the affine diagnostic. It failed the longitudinal ink-coverage check for use as a piecewise knot. The 450 and 550 lb lines bracket its position in the piecewise conversion.

| Panel | Verified time × ordinate lines | Affine RMS (time, ordinate) | Affine max (time, ordinate) |
| --- | ---: | --- | --- |
| 1 | 15 × 12 | 0.100 ms, 0.332 lb | 0.321 ms, 0.964 lb |
| 2 | 15 × 10 | 0.114 ms, 0.00561 in | 0.375 ms, 0.0220 in |

The native bounds include the local knot-location uncertainty. Near an outer frame, a row may be flagged `extrapolated` because part of its pixel bound reaches past the outer knot.

## Traces and ambiguity

- The first few milliseconds are crowded. In panel 1, the first force rise shares ink with the left frame and the other rises. In panel 2, the Run 4 and Run 12 strokes touch or cross in the early rise and the Run 10 dots pass through the same band. The first points mark visible ink at the crowded starts, with widened bounds. The starts of the individual strokes within shared ink are uncertain.
- In panel 1, the descending Run 12 pulse passes Run 10 at about 15 ms and Run 4 at about 17 ms. Run 4 and Run 10 cross near 23 ms. Run 12 touches the baseline around 36 ms.
- The falling Run 4 branch crosses both of the lower runs near 96–100 ms and passes back through their band around 110–115 ms. The late dotted Run 10 and dashed Run 12 strokes are close or joined. Some apparent late extrema can only be located within those overlaps. The row notes identify these readings.
- The dotted displacement record ends at about 78 ms, at about 1.99 in. Its force record continues to about 130 ms. The last Run 4 and Run 12 displacement readings are about 4.13 in and 1.23 in, respectively.
- For patterned strokes, scheduled stations move onto the nearest identifiable ink within the local reading window. Bounds project the measured half-width of the stroke and half of its adjacent gap onto the page axes, with additional allowance in crowded regions.

## Cross-check against Figure 4-20

I paired the force-peak times with the displacement read from panel 2. The three impact peaks gave approximately 0.21 in / 125 lb, 0.27 in / 284 lb and 0.36 in / 588 lb for Runs 4, 10 and 12. The corresponding peaks read directly on Figure 4-20 were about 0.24 in / 123 lb, 0.31 in / 283 lb and 0.40 in / 592 lb. Run 4's later crest was about 4.04 in / 143 lb versus 4.05 in / 139 lb, and its unloading minimum was about 4.11 in / 22 lb versus 4.11 in / 21 lb. The figures broadly agree on the branches and levels, with visible drawing differences. The paired values do not distinguish common relabelings of the two time panels. The late time assignments therefore come from the printed grid cadence.
