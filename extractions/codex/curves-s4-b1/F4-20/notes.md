# Figure 4-20 · Force versus displacement

Read from `packet/p0209.png`, printed page 4-24. The page turns clockwise to read the figure. The saved pixels are in the original image coordinates. Displacement increases toward smaller page `v` and force toward smaller page `u`. Printed page 4-22 identifies these as the same vertical tests as Figure 4-19. The caption gives the footpad diameter as 6.17 in.

| Series ID | Printed legend | Trace |
| --- | --- | --- |
| `run4` | Run No. 4, Dᵣ = 0 | Solid |
| `run10` | Run No. 10, Dᵣ = 0.45 | Dotted |
| `run12` | Run No. 12, Dᵣ = 0.65 | Alternating long and short dashes |

The series IDs agree with the printed legend. The Run 12 sample includes both long and short dashes. No plotted point symbols were visible.

## Calibration

I checked all ten printed displacement labels from 0 to 4.5 in and all seven printed force labels from 0 to 600 lb against their grid lines. The six intervening unnumbered force lines are 50 lb half-steps. The baseline has a gap near 1.7–1.9 in and supports a fit on either side. The piecewise calibration uses 10 verified displacement lines and 13 verified force lines. The affine RMS residual is 0.00228 in and 0.356 lb, with maxima of 0.00548 in and 0.948 lb. Near the origin, a native row can carry an extrapolation flag when its pixel bound reaches past the frame.

## Traces and ambiguity

- The left edge is crowded. Near zero displacement the ascending strokes and the axis share ink. Bounds on the first points and nearby force stations include that overlap.
- The falling Run 12 stroke crosses Run 10 near 0.69 in and 207 lb and crosses Run 4 near 0.75 in and 83 lb. Run 10 crosses Run 4 near 1.4 in and 82 lb. The nearby rows carry wider bounds.
- Run 10 has a wide blank strip from roughly 1.61 to 1.92 in, where adjacent grid ink is also interrupted. Samples stop at the last visible dot before the break and resume at the first visible dot on the other side. Run 4 has a smaller interruption near 1.8 in. Its samples likewise follow the visible margins.
- Run 4 turns near 4.15 in, descends steeply, and bends to smaller displacement. The dark left limb of its pointed tip is consistent with a short return stroke from about 21 to 44 lb and is included in drawing order. Figure 4-19 also shows a force recovery at about this displacement. The two limbs crowd each other near the tip.
- Run 10 ends near 2.01 in and 26 lb at the final dot distinguishable from the 2 in grid. Run 12 ends in a falling dash near 1.25 in and 22 lb. Bounds on the dotted and dashed samples include half of the adjacent gap along the stroke.
