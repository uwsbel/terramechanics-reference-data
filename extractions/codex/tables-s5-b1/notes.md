# Table 5-T3 transcription notes

AM-68-1 Vol. I, Table 5-T3, printed 5-45, PDF 325. The scan reads upright after a 90° clockwise rotation.

> TABLE 5-T3. DETAIL CORRELATION DROPS

The nine printed columns are in the requested order. The notation below represents subscripts with underscores and joins lines within each heading.

| Column | Printed heading |
| --- | --- |
| 1 | NASA Test No. |
| 2 | Bendix Drop No. |
| 3 | V_v (In./Sec.) |
| 4 | V_h (In./Sec.) |
| 5 | τ (Sec.) |
| 6 | Soil |
| 7 | D_r |
| 8 | γ (Lb./Ft.³) |
| 9 | φ (Deg.) |

The slash in the γ unit is almost lost in the scan. Two small marks remain between “Lb.” and “Ft.³” near (u 803, v 1446) on the unrotated page. The header above reads those marks as a slash.

### Printed legend

> V_v = Vertical velocity
>
> V_h = Horizontal velocity
>
> τ = Time interval between model release to touchdown
>
> D_r = Soil relative density
>
> γ = Soil density
>
> φ = Internal angle of friction

## Timing and velocities

> The velocities shown in Table 5-T3 were calculated based on the exact time interval between the instant of model release to the instant of ground contact. This time interval could be measured very precisely from the readings of the accelerometer in the x direction.

AM-68-1 Vol. I, §5.5.4, printed 5-44, PDF 324.

> At the instant of model release, a short pulse signal was injected into the output of the accelerometer at the CG in the X direction. The signal from this accelerometer was recorded simultaneously on all the four recording devices (2 tape recorders and 2 oscillographs) to provide a common time base for data reduction.

AM-68-1 Vol. I, §5.5.1, printed 5-39, PDF 319.

> The origin of the fixed coordinate is a point on the ground, which is the vertical projection from the model center of gravity at the instant the first footpad touches the ground.

AM-68-1 Vol. I, §5.2.3, printed 5-18, PDF 298.

Release is the model's separation from the launch mechanism shown in Fig. 5-12. The injected pulse marks that instant. Touchdown is first footpad contact with the landing surface. The measured interval between these events is τ. Section V says both tabulated velocities were calculated using that interval and leaves the contact-picking rule, component formulas, and any other inputs to the velocity calculation unspecified.

For the separate time-history reduction, §5.5.1 says “the three accelerometers provided data from which the CG displacement, velocity, and acceleration in the x-y plane, and the pitch displacement, velocity and acceleration of the model could be calculated at any instant.” Section 5.5.2 describes “the numerical integration used in the computation of the footpad and CG motions.” After filtering, the analog-to-digital machine “yielded thirteen digital signals every 1/1000 second of model drop time as the input for the computer program.” Fig. 5-21 is the program flow chart. AM-68-1 Vol. I, printed 5-39, PDF 319, and printed 5-41 to 5-43, PDF 321 to 323.

## Soil-bed preparation and characterization

> For detail correlation tests, the LM model was landed on RS and SS loose and RS intermediate soils, using a level landing surface (e.g., zero slope). Soil emplacement was accomplished by means of a large, specially designed hopper (or spreader) which is described in Section II (reference Figure 2-63).

> The spreader rolls horizontally on steel tracks along the edges of the soil pit, uniformly depositing the soil material in approximately four-inch layers across the surface of the bed with each pass. The soil is allowed to flow only when the spreader is moved in one direction. At the end of each pass, flow is stopped by a shutoff gate, the hopper is raised clear of the bed, returned to its starting position, and the process continued until the desired soil depth is reached.

> For the RS and SS loose soil beds, no further handling was required once the soil was placed by successive passes of the spreader.

AM-68-1 Vol. I, §5.5.3, printed 5-43, PDF 323.

> Preparation of the RS intermediate soil beds required compacting the soil after each pass of the spreader. This was accomplished using a 63-pound lawn roller which is 18 inches in diameter and 24 inches wide. The procedure for rolling the soil consisted of making eight straight back and forth passes of the roller (i.e., four cycles) for every 24-inch width of soil bed until the whole area had been traversed. The entire process of depositing and rolling one layer at a time was repeated until the desired soil depth (18 inches thick) was achieved.

> Dynamic penetrometer readings were taken across the soil bed (but [away] from the area disturbed by the model footpads) after each model drop was made. The soil was then completely removed from the bed before a new soil bed was prepared.

> Soil bed properties obtained for each of the detail correlation drop tests are given in Table 5-T3, and details of the methods of establishing the soil properties are described in Section II. In particular, the correlation between the relative density and the dynamic penetrometer readings is covered in Paragraph 2.7.1.

AM-68-1 Vol. I, §5.5.3, printed 5-44, PDF 324. Brackets mark the reading of “away,” where the scan loses part of the word.

The report ties each bed's D_r to post-drop dynamic penetrometer readings in undisturbed areas and points to §2.7.1 for the correlation. Section V does not give the individual readings, their aggregation or calibration, or the per-bed method for obtaining γ or φ. It refers to Section II for the property methods. The supplied Section II page, Table 2-3, lists soil designations and properties. The bed was rebuilt for each drop, including the repeat conditions. The text does not say whether the removed soil material was used to build later beds.

## Other printed values for these drops

Table 5-T2 prints the nominal velocities below. Section 5.5.4 identifies the nominal units as feet per second, whereas Table 5-T3 prints calculated values in In./Sec. The pairs below preserve the signs and digits from each source.

| NASA / Bendix | Table 5-T2 V_v, V_h (ft/s) | Table 5-T3 V_v, V_h (In./Sec.) | Table 5-T2 location |
| --- | --- | --- | --- |
| 1 / 10 | 10, 0 | -114.9, 0 | Printed 5-28, PDF 308 |
| 2 / 11 | 5, 7 | -60.5, 83.5 | Printed 5-28, PDF 308 |
| 3 / 12 | 5, 7 | -60.0, 84.0 | Printed 5-28, PDF 308 |
| 4 / 13 | 10, 0 | -117.3, 0 | Printed 5-28, PDF 308 |
| 5 / 16 | 5, 7 | -60.8, 83.4 | Printed 5-29, PDF 309 |
| 6 / 17 | 10, 0 | -117.1, 0 | Printed 5-29, PDF 309 |
| 7 / 20 | 5, 7 | -60.0, 84.0 | Printed 5-29, PDF 309 |
| 8 / 21 | 10, 0 | -118.0, 0 | Printed 5-29, PDF 309 |

- For NASA 5 and 6 (Bendix 16 and 17), Table 5-T2 prints D_r as `0.3`. Table 5-T3 prints `.3`. AM-68-1 Vol. I, Table 5-T2, printed 5-29, PDF 309.
- For NASA 1 (Bendix 10), the strut-load inset prints V_v `-114.93` in/s, versus `-114.9` in Table 5-T3. The inset also prints V_h `0`. AM-68-1 Vol. I, Fig. 5-25, printed 5-50, PDF 330.
- For NASA 2 (Bendix 11), the strut-load inset reads V_v `-60.55` and V_h `83.75` in/s, versus `-60.5` and `83.5` in Table 5-T3. The inset is degraded, but those digits are distinguishable in the enlarged scan. AM-68-1 Vol. I, Fig. 5-32, printed 5-57, PDF 337.
- Section 5.5.4 assigns the pure vertical condition to NASA 1, 4, 6, and 8 and prints “a nominal vertical velocity of teen feet per second.” The word reads “teen” on the scan. Table 5-T2 gives `10` for those tests. For NASA 2, 3, 5, and 7 the prose gives “a nominal vertical velocity of five feet per second and a nominal horizontal velocity of seven feet per second.” AM-68-1 Vol. I, §5.5.4, printed 5-44, PDF 324.
- Table 5-T2 marks all eight landings “Yes” under “Stable.” The detailed study covered Bendix drops 10 to 21 inclusive, and the report says “four of the drops had to be repeated.” In Table 5-T2 the other four drops have separate numbers and remarks: 14 “Bad tape recording.”, 15 “Poor recording.”, 18 “Bad recording.”, and 19 “Bad release.” Table 5-T3 lists the eight NASA-numbered runs. AM-68-1 Vol. I, Table 5-T2, printed 5-28 to 5-29, PDF 308 to 309, and §5.5.4, printed 5-46, PDF 326.

On printed 5-46, PDF 326, §5.5.4 says “test No. 4 was a duplicate of test No. 1, and test No. 3 was a duplicate of test No. 2.” It adds that “Tests Nos. 5 and 6 repeated the two test conditions on RS intermediate soil, and tests Nos. 7 and 8 on SS loose soil.” Section 5.5.5 says “Figures 5-22 to 5-39, inclusive, show the typical results of tests Nos. 1 and 2.” No response histories for NASA 3 through 8 appear in Section V. The curves for NASA 1 and 2 represent time histories, including absolute footpad speed and CG velocity, and the exact initial velocity annotations are in the two strut-load insets.

Table 2-3, outside Section V, identifies No. 1 as “RS Loose,” No. 3 as “RS Inter.” and No. 7 as “SS Loose.” Their general D_r, γ, and φ entries are `0 / 41.4 / 40°`, `.45 / 45.9 / 44.5°`, and `0 / 94.7 / 29°`, respectively. The index uses family and state to infer SS soil No. 7 and leaves the mixed-state RS row unnumbered. The drop properties are transcribed from Table 5-T3. AM-68-1 Vol. I, Table 2-3, printed 2-16, PDF 41.

## Scan condition and reading checks

All 72 data cells were readable. There were no blank cells, ditto marks, or unresolved digits. The coordinates below are approximate glyph centers or mark locations in the original unrotated `packet/pages/p0325.png`, with u measured from the left and v from the top. Small gaps and mottled edges occur in the lettering and rules.

| NASA / Bendix | Cell or mark | Approximate (u, v), px |
| --- | --- | --- |
| 1 / 10 | γ and φ, leading 4s with broken diagonals | (911, 1486), (905, 1138) |
| 2 / 11 | γ and φ, leading 4s with broken diagonals | (998, 1486), (993, 1138) |
| 3 / 12 | Soil, chipped R. γ, chipped 4 and 7. φ, chipped 4 | (1097, 2261), (1085, 1486), (1085, 1457), (1081, 1137) |
| 4 / 13 | Gap and fleck in rule beside Soil. γ, chipped 7 and final 1 | (1168, 2325), (1173, 1457), (1173, 1407) |
| 5 / 16 | γ and φ, broken upper strokes of 5 | (1260, 1485), (1254, 1057) |
| 6 / 17 | V_v, split second 1. γ, broken upper stroke of 5 | (1367, 3172), (1347, 1485) |
| 7 / 20 | V_h, 8 with chipped upper loop | (1449, 2834) |

There is a dark scan edge outside the table and small breaks in the outer rules. The defect in the γ header unit is described above.

## Setup

- **Model and rig.** The instrumented and modified Langley-Grumman 1/6-scale dynamic LM model was launched by a “six-degree-of-freedom drop test rig” suspended over the soil bed at the Bendix spacecraft model dynamic drop test laboratory. Fig. 5-12 labels the release mechanism and Fig. 5-13 shows the rig. The linked launch mechanism had adjustable drop-rig height, linkage angles, and linkage swing settings obtained by a digital computer program. The settings themselves are unspecified for these runs. AM-68-1 Vol. I, §5.2 and Fig. 5-1, printed 5-2 to 5-3, PDF 281 to 282, Fig. 5-2, printed 5-5, PDF 284 to 285, and §5.2.4 and Figs. 5-12 and 5-13, printed 5-22 to 5-25, PDF 302 to 305.
- **Weight and geometry.** “Total Model Weight” is `68.4 Lbs.` The physical-properties table also gives `23.90 Inches` for “Initial CG Height above a level ground” and `27.928 Inches` for “Initial footpad to body centerline radius.” The radius is a vehicle layout dimension. Fig. 5-9 shows the modified strut geometry and Fig. 5-10 the model load-stroke curves. AM-68-1 Vol. I, physical-properties table, printed 5-22, PDF 302, and Figs. 5-9 and 5-10, printed 5-15 to 5-16, PDF 295 to 296.
- **Footpads.** Section V calls them “Scaled LM footpads” and “round simulated LM footpads.” Under the normal touchdown setup the pads were against their stops, tilted two degrees from a plane normal to the vehicle centerline. The No. 1 pad was instrumented. AM-68-1 Vol. I, §5.2.1, printed 5-4, PDF 283, §5.2.1.3 and Fig. 5-6, printed 5-9 and 5-11, PDF 289 and 291, and §5.4.1, printed 5-33, PDF 313.
- **Bed.** The site description gives “18 feet long and 12 feet wide, with a maximum below ground depth of five feet” and says the soil depth was adjusted to the test conditions. Section 5.5.3 gives “18 inches thick” in its RS intermediate preparation instructions. It gives no test fill thickness for RS Loose or SS Loose. Table 5-T3 assigns D_r, γ and φ per drop. Fresh beds and no reported bed reloading support `mcc_relevant=no` for both families. AM-68-1 Vol. I, §5.2.4, printed 5-22, PDF 302, §5.5.3, printed 5-43 to 5-44, PDF 323 to 324, and Table 5-T3, printed 5-45, PDF 325.
- **Loading and rates.** The model made free-body landings on a level soil surface. “The initial drop conditions had zero angular rates, zero pitch and roll attitude, and all of the drops were released with 45-degree yaw angle (i.e., 2-2 landings).” Table 5-T2 gives slope `0` and yaw `45` in degrees for each of the eight runs. The calculated Table 5-T3 ranges, in `In./Sec.`, are RS V_v `-117.3 to -60.0`, SS V_v `-118.0 to -60.0`, and V_h `0 to 84.0` for both. Section V gives no run-specific release heights, measured touchdown attitudes, or starting penetration depth. AM-68-1 Vol. I, §5.5, printed 5-38, PDF 318, §5.5.3 and §5.5.4, printed 5-43 to 5-44, PDF 323 to 324, Table 5-T2, printed 5-28 to 5-29, PDF 308 to 309, and Table 5-T3, printed 5-45, PDF 325.
- **Remaining simulation inputs.** Both rows are `setup_incomplete`. The laboratory setting supports using ordinary Earth gravity as an assumption. Section V gives no numerical test gravity for the drop series. A recreation would also need the loose-bed fill thickness and, for a simulation starting at release, the run-specific release pose and velocity or the rig settings needed to recover them. A soil constitutive law, its parameters beyond the tabulated bed properties, and any exact footpad contact dimensions needed by that law must be supplied separately.
