# Table 5-T3, Detail Correlation Drops: blind reading notes (batch tables-s5-b1, Claude)

Source: Bendix AM-68-1 Vol. I (NASA CR-92208), Section V. Table 5-T3 is on PDF 325, printed 5-45, printed
sideways on the scan (text reads bottom to top). All pixel positions below are (u, v) on the unrotated scan
`packet/pages/p0325.png` (3213 by 4558 px, u to the right, v downward), unless another page is named.

## 1. How the table was read

1. The page was rotated 90 degrees clockwise (rotated x maps back to v = 4557 - x, rotated y = u) and every
   crop was labeled with the original scan coordinates.
2. Pass 1, grouped by column: each column (NASA and Bendix numbers together, then V_v, V_h, tau, Soil, D_r with
   gamma, phi) in two crops, rows 1 to 4 and rows 5 to 8, at zoom 2.4 to 3.
3. Pass 2, grouped by row: row pairs (1 and 2, 3 and 4, 5 and 6, 7 and 8) across three thirds of the table
   (NASA, Bendix, V_v; V_h, tau, Soil; D_r, gamma, phi) at zoom 1.3 to 1.7.
4. Damaged glyphs were then read at zoom 4 to 8 (V_v of row 6, the RS of row 3, the 4s and 5s of the gamma and
   phi columns, the gamma header unit).
5. The two passes agreed on all 72 cells (8 rows by 9 columns). No cell needed a `?`.

## 2. Caption and header as printed

Caption: `TABLE 5-T3.  DETAIL CORRELATION DROPS` (one line, capitals, above the table).

The page has the nine columns of the brief, in the same order:

| # | Header as printed | Notes |
|---|---|---|
| 1 | `NASA` / `Test` / `No.` | three lines |
| 2 | `Bendix` / `Drop` / `No.` | three lines |
| 3 | `V` with subscript `v` / `(In./Sec.)` | the closing parenthesis is broken and looks like `.;)` |
| 4 | `V` with subscript `h` / `(In./Sec.)` | |
| 5 | `tau` (Greek) / `(Sec.)` | |
| 6 | `Soil` | |
| 7 | `D` with subscript `r` | no unit |
| 8 | `gamma` (Greek) / `(Lb./Ft.` with superscript `3` `)` | the slash between `Lb.` and `Ft.` is mostly missing on the scan: only its upper end (about u 740 to 754, v 1435) and a speck at its lower end (about u 814, v 1452) print, so the unit can look like `(Lb., Ft.^3)`; read as Lb./Ft.^3 by the slash fragments and the legend `Soil density` |
| 9 | `phi` (Greek) / `(Deg.)` | |

## 3. Legend printed under the table (quoted line by line)

1. `V_v = Vertical velocity`
2. `V_h = Horizontal velocity`
3. `tau = Time interval between model release to touchdown` (printed "between ... to" as quoted; the b of
   "between" has a broken ascender and looks like "tetween" on the scan, about u 1880 to 1915, v 3195 to 3225)
4. `D_r = Soil relative density`
5. `gamma = Soil density`
6. `phi = Internal angle of friction` (the scan shows a gap that makes it look like "Internal a ngle")

No footnote, source line or other legend is printed on the page. The printed page label `5-45` is at the
lower right of the unrotated scan.

## 4. Transcribed values (also in `table.csv`)

| NASA Test No. | Bendix Drop No. | V_v (In./Sec.) | V_h (In./Sec.) | tau (Sec.) | Soil | D_r | gamma (Lb./Ft.^3) | phi (Deg.) |
|---|---|---|---|---|---|---|---|---|
| 1 | 10 | -114.9 | 0 | .298 | RS Loose | 0 | 46.9 | 41 |
| 2 | 11 | -60.5 | 83.5 | .177 | RS Loose | 0 | 46.9 | 41 |
| 3 | 12 | -60.0 | 84.0 | .156 | RS Loose | 0 | 47.1 | 41 |
| 4 | 13 | -117.3 | 0 | .304 | RS Loose | 0 | 47.1 | 41 |
| 5 | 16 | -60.8 | 83.4 | .146 | RS Intermediate | .3 | 53.0 | 42.5 |
| 6 | 17 | -117.1 | 0 | .303 | RS Intermediate | .3 | 53.0 | 42.5 |
| 7 | 20 | -60.0 | 84.0 | .154 | SS Loose | 0 | 96.0 | 30 |
| 8 | 21 | -118.0 | 0 | .306 | SS Loose | 0 | 96.0 | 30 |

No cell is blank and no ditto mark is used; every cell carries its own value.

## 5. What the text says about these drops

Citations are AM-68-1 Vol. I, printed page, PDF page.

### 5.1 How V_v, V_h and tau were obtained

1. Printed 5-44, PDF 324 (Para. 5.5.4): "The velocities shown in Table 5-T3 were calculated based on the exact
   time interval between the instant of model release to the instant of ground contact. This time interval
   could be measured very precisely from the readings of the accelerometer in the x direction."
2. Printed 5-39, PDF 319 (Para. 5.5.1): "At the instant of model release, a short pulse signal was injected into
   the output of the accelerometer at the CG in the X direction. The signal from this accelerometer was recorded
   simultaneously on all the four recording devices (2 tape recorders and 2 oscillographs) to provide a common
   time base for data reduction."
3. So tau is measured (from the x accelerometer record, with release marked by the injected pulse), and V_v and
   V_h are computed ("calculated") from tau. The text does not say how: no formula, no value of g, and nothing
   on how V_h follows from a time interval for the drops released from the swinging rig. It does not say that
   any velocity was measured directly (no velocity transducer, photo or film is mentioned for these drops).
4. Nominal conditions, printed 5-44, PDF 324: "It can be seen that among the eight drops only two different sets
   of initial conditions were used. The first condition (used for NASA Tests No. 1, 4, 6, and 8) was a pure
   vertical drop which had a nominal vertical velocity of teen feet per second. The second condition (used for
   the remaining tests) had a nominal vertical velocity of five feet per second and a nominal horizontal
   velocity of seven feet per second." ("teen" is printed so; checked at full resolution. It presumably means
   ten, which matches the 10 printed in Table 5-T2.)
5. Attitude, printed 5-44, PDF 324: "The initial drop conditions had zero angular rates, zero pitch and roll
   attitude, and all of the drops were released with 45-degree yaw angle (i.e., 2-2 landings)."
6. Sign convention, printed 5-18, PDF 298: "X_f axis - Normal to the horizon, positive in the direction away
   from the ground surface." and "Y_f axis - Normal to X_f, positive in the direction of the model horizontal
   velocity." Table 5-T3 does not state its sign convention; under this fixed system a negative V_v is downward
   and a positive V_h is along +Y_f (my reading of the definitions, not a statement attached to the table).

### 5.2 What "release" and "touchdown" mean

1. Legend of Table 5-T3 (printed 5-45, PDF 325): tau is the "Time interval between model release to
   touchdown".
2. Printed 5-44, PDF 324: "the instant of model release to the instant of ground contact".
3. Release is the instant the drop rig lets the model go: printed 5-22, PDF 302: "The LM model was launched by a
   six-degree-of-freedom drop test rig which is suspended above the soil bed"; Fig. 5-12 (printed 5-23, PDF 303)
   labels the "RELEASE MECHANISM" at the lower end of the rig links; printed 5-39, PDF 319, marks the release
   instant with the injected pulse.
4. Touchdown is "ground contact" (printed 5-44, PDF 324). The text does not define it further (for example
   first footpad contact, or contact of the two leading pads of a 2-2 landing). The nearest definition is the
   origin of the fixed system, printed 5-18, PDF 298: "a point on the ground, which is the vertical projection
   from the model center of gravity at the instant the first footpad touches the ground."
5. The time axes of Figs. 5-22 to 5-39 start at 0; the text does not say whether t = 0 there is the touchdown
   instant of Table 5-T3.

### 5.3 How the beds were prepared

1. Printed 5-43, PDF 323 (Para. 5.5.3): "For detail correlation tests, the LM model was landed on RS and SS
   loose and RS intermediate soils, using a level landing surface (e.g., zero slope). Soil emplacement was
   accomplished by means of a large, specially designed hopper (or spreader) which is described in Section II
   (reference Figure 2-63)."
2. Printed 5-43, PDF 323: "The spreader rolls horizontally on steel tracks along the edges of the soil pit,
   uniformly depositing the soil material in approximately four-inch layers across the surface of the bed with
   each pass. The soil is allowed to flow only when the spreader is moved in one direction. At the end of each
   pass, flow is stopped by a shutoff gate, the hopper is raised clear of the bed, returned to its starting
   position, and the process continued until the desired soil depth is reached."
3. Printed 5-43, PDF 323: "For the RS and SS loose soil beds, no further handling was required once the soil was
   placed by successive passes of the spreader. It was found that the soil beds thus prepared had very uniform
   and consistent soil properties."
4. Printed 5-44, PDF 324: "Preparation of the RS intermediate soil beds required compacting the soil after each
   pass of the spreader. This was accomplished using a 63-pound lawn roller which is 18 inches in diameter and
   24 inches wide. The procedure for rolling the soil consisted of making eight straight back and forth passes
   of the roller (i.e., four cycles) for every 24-inch width of soil bed until the whole area had been
   traversed. The entire process of depositing and rolling one layer at a time was repeated until the desired
   soil depth (18 inches thick) was achieved."
5. Printed 5-44, PDF 324: "Dynamic penetrometer readings were taken across the soil bed (but away from the area
   disturbed by the model footpads) after each model drop was made. The soil was then completely removed from
   the bed before a new soil bed was prepared."
6. Printed 5-46, PDF 326: "As noted earlier, three different kinds of soil beds were used for the eight detailed
   correlation tests. Of the four drops made in RS loose soil test No. 4 was a duplicate of test No. 1, and test
   No. 3 was a duplicate of test No. 2. These duplicate drops were made to check the repeatability of the test
   equipment and procedure with due allowance for the slight variation of individual RS loose soil beds. Tests
   Nos. 5 and 6 repeated the two test conditions on RS intermediate soil, and tests Nos. 7 and 8 on SS loose
   soil. The detailed test conditions for all the drops can be found in Paragraph 5.3 (Table 5-T2) in which
   Bendix drops Nos. 10 to 21, inclusive, applied to the detailed correlation study. It can be seen that some
   trouble was encountered in the laboratory so that four of the drops had to be repeated."
7. The depth of soil in the loose beds is not printed. The pit, printed 5-22, PDF 302: "The soil bed which forms
   the landing surface is 18 feet long and 12 feet wide, with a maximum below ground depth of five feet. The
   depth of soil used was adjusted to suit the varying test conditions."

### 5.4 How D_r, gamma and phi were obtained for each bed

1. Printed 5-44, PDF 324: "Soil bed properties obtained for each of the detail correlation drop tests are given
   in Table 5-T3, and details of the methods of establishing the soil properties are described in Section II.
   In particular, the correlation between the relative density and the dynamic penetrometer readings is covered
   in Paragraph 2.7.1."
2. Together with item 5 of 5.3 (penetrometer readings after each drop), this indicates that D_r of each bed
   came from dynamic penetrometer readings through the correlation of Para. 2.7.1. The text does not state it in
   one sentence, does not print the penetrometer readings, and does not say how gamma and phi were obtained for
   these beds (measured on the bed, or taken from the Section II correlations for the soil at that D_r).
   Section II is not in this packet.

### 5.5 Data reduction of these drops (context)

1. Printed 5-43, PDF 323: "The thirteen signals which form the input for the computer program were machine
   reduced from the two reels of magnetic tape on which they were recorded. ... The filtered signals were then
   fed into an analog-to-digital hybrid machine which yielded thirteen digital signals every 1/1000 second of
   model drop time as the input for the computer program. The processes of machine data reduction and
   computation of required output for each of the eight drops were accomplished by the McDonnell Automation
   Center of The McDonnell Douglas Corporation under subcontract to Bendix."
2. Printed 5-41, PDF 321: "For given model drop test initial conditions the computer program calls for the input
   of the 13 (tape recorded) signals every 1/1000 second, then calculates the instantaneous CG motion, the model
   attitude, the footpad velocity, the depth of footpad penetration into the soil, the forces acting on the
   footpad and other pertinent information required for detailed correlation study. A total of 17 output
   parameters result." The text does not say that the initial conditions given to the program were the
   Table 5-T3 velocities.
3. Printed 5-46, PDF 326 (Para. 5.5.5): "Figures 5-22 to 5-39, inclusive, show the typical results of tests Nos.
   1 and 2." Only these two of the eight drops have plotted results in Section V.

## 6. Numbers printed elsewhere in Section V for these drops that differ from Table 5-T3

1. Table 5-T2, List of Model Drop Tests (PDF 308, printed 5-28, Bendix drops 10 to 13; PDF 309, printed 5-29,
   drops 16, 17, 20, 21). Header `V_V`, `V_H` with no unit printed. It prints the nominal velocities, not the
   Table 5-T3 values: drops 10, 13, 17, 21: V_V 10, V_H 0; drops 11, 12, 16, 20: V_V 5, V_H 7. All eight:
   Test Type C ("Detail Correlation Tests" in the key, PDF 312, printed 5-32), Ground Slope 0, Yaw Angle 45,
   Stable Yes. Relative Density printed `0.3` for drops 16 and 17 (Table 5-T3 `.3`); `0` for the others.
   Density gamma (46.9, 46.9, 47.1, 47.1, 53.0, 53.0, 96.0, 96.0) and Friction Angle phi (41, 41, 41, 41, 42.5,
   42.5, 30, 30) are the same as in Table 5-T3. Remarks: drop 10 "NASA Drop No. 1. Tests No. 1-8 McDonnell
   reduced.", drops 11 to 21 "NASA Drop No. 2" to "NASA Drop No. 8" (Table 5-T2 says "Drop", Table 5-T3 says
   "Test"). Dates: 10: 7-18-67; 11: 7-19-67; 12: 7-20-67; 13: 7-20-67; 16: 7-25-67; 17: 7-25-67; 20: 7-28-67;
   21: 7-2?-67 (the day digit is broken, 6 or 8; on p0309, printed upright, about u 668 to 792, v 2238 to 2262).
2. The repeated drops on the same soils, Table 5-T2: drop 14 (RS Intermediate, 5, 7, "Bad tape recording.") and
   15 (RS Intermediate, 10, 0, "Poor recording."), D_r, gamma, phi printed `-`; drop 18 (SS Loose, 5, 7, "Bad
   recording.") and 19 (SS Loose, 10, 0, "Bad release."), D_r 0, gamma 95.2, phi 30. These are not in Table
   5-T3.
3. Fig. 5-25, Strut Axial Load versus Time (NASA Test No. 1), PDF 330, printed 5-50, inset text (about u 1445 to
   1485, v 1259 to 1689 on p0330): `V_v = -114.93 in. sec.   V_h = 0` / `RS Loose   Level Surface`. Table 5-T3
   prints -114.9. No slash is visible between "in." and "sec.".
4. Fig. 5-32, Strut Axial Load versus Time (NASA Test No. 2), PDF 337, printed 5-57, inset text:
   `V_v = -?0.55 In. Sec.   V_h = ?3.75 In. Sec.` / `RS Loose   Level Surface`. Table 5-T3 prints -60.5 and
   83.5. The inset print is faint and broken:
   - V_v (about u 1595 to 1635, v 1479 to 1589 on p0337): the first digit is 5 or 6 (top bar, middle bar and
     lower bowl print; the lower left side is missing); the second digit is 0 (both upper sides and the lower
     right side print, which rules out 2); then `.55`.
   - V_h (about u 1595 to 1635, v 1139 to 1244 on p0337): the first digit shows an upper right side, a wide
     middle bar, a lower left side and part of the lower right side, which fits 8 best (2 less well; not 6);
     then `3.75`, read with confidence.
   - Whatever the first digits, the decimals differ from Table 5-T3: `.55` against `.5`, and `3.75` against
     `3.5`. A value 83.75 would round to 83.8, not 83.5.
5. The CG vertical velocity curves start near the Table 5-T3 values (Fig. 5-27, PDF 332, near -115 at t = 0;
   Fig. 5-34, PDF 339, near -60), and the CG horizontal velocity curve of Fig. 5-36 (PDF 341) starts near 84. These
   are curve positions, not printed numbers, and were not digitized.
6. Section II Table 2-3 (PDF 41, printed 2-16), for comparison of the bed properties (not printed for these
   drops): No. 1 RS Loose: D_r 0, 41.4 pcf, 40 deg; No. 3 RS Inter.: .45, 45.9 pcf, 44.5 deg; No. 7 SS Loose: 0,
   94.7 pcf, 29 deg. Table 5-T3 prints 46.9 and 47.1 pcf with 41 deg for RS Loose, .3, 53.0 pcf and 42.5 deg for
   RS Intermediate, and 96.0 pcf with 30 deg for SS Loose. The RS Intermediate beds have a lower D_r but a
   higher unit weight than soil No. 3, and the RS Loose beds are 5.5 to 5.7 pcf heavier than soil No. 1 at the
   same D_r 0. The report does not comment on these differences in the pages read.

## 7. Cells to look at (all read with confidence; none left as `?`)

Positions are ink bounding boxes on p0325.

| Row | Column | Value | Position (u, v) | Why noted |
|---|---|---|---|---|
| 1 | gamma | 46.9 | u 890 to 928, v 1400 to 1500 (the 4 at v 1475 to 1497) | 4 printed without most of its diagonal |
| 2 | gamma | 46.9 | u 978 to 1016, v 1399 to 1501 | same |
| 3 | Soil | RS Loose | u 1077 to 1115, v 2037 to 2275 (the S at v 2215 to 2245) | S broken, lower stroke detached; can look like "RS" or "FS" at low zoom |
| 3 | gamma | 47.1 | u 1065 to 1103, v 1400 to 1500 | 4 broken |
| 4 | gamma | 47.1 | u 1154 to 1192, v 1399 to 1498 | 4 and 7 light and broken |
| 1 to 4 | phi | 41 | u 886 to 1187, v 1099 to 1153 | the 4s print with broken diagonals |
| 5, 6 | gamma | 53.0 | u 1241 to 1366, v 1394 to 1495 | the 5 has a detached top bar (typeface; can look like "33.0" at low zoom) |
| 6 | V_v | -117.1 | u 1352 to 1389, v 3083 to 3240 (the middle 1 at v 3160 to 3177) | the middle 1 has a break near u 1365 and a spur |

## 8. Other remarks on the page

1. The scan is clean apart from broken glyphs and rules; the dark band along the unrotated bottom edge
   (binding) does not reach the table.
2. The left table border has a gap at about u 1484 to 1490, v 3910. The bottom border is missing from the left
   corner (v about 3923) to about v 3725, at u about 1658.
3. The column rule between tau and Soil has a gap from about u 1105 to 1165 (v about 2327), beside rows 3 and 4;
   a short broken piece of it beside row 4 (about u 1160 to 1180) looks like a stray mark in front of "RS Loose".
4. A small speck below "relative" in the legend (about u 2036, v 3454) is not a character.
5. A check made by the reader, not printed in the report: with standard gravity (386.09 in./sec.^2) and the
   printed tau, g times tau gives 115.05, 117.37, 116.98 and 118.14 in./sec. for the four pure vertical drops
   (Tests 1, 4, 6, 8), against |V_v| 114.9, 117.3, 117.1, 118.0. The differences (-0.15, -0.07, +0.12, -0.14) are
   within the 0.19 in./sec. that the third decimal of tau allows, so those V_v values agree with free fall from
   rest over tau. For the four drops with V_h (Tests 2, 3, 5, 7), g times tau is 68.34, 60.23, 56.37 and
   59.46 in./sec. against |V_v| 60.5, 60.0, 60.8, 60.0, so their V_v is not free fall from rest over tau; the
   report does not say how V_v and V_h were calculated for these drops (the rig gives the model a velocity at
   release through its swinging links, printed 5-22, PDF 302: "linkage swing settings").
6. Rows 1 and 2, 3 and 4, 5 and 6, 7 and 8 print identical D_r, gamma and phi in pairs. Table 5-T2 dates drops 12
   and 13, 16 and 17, and 20 and 21 on the same day, while drops 10 and 11 are on different days. The text says
   the soil was removed after each drop and a new bed prepared (printed 5-44, PDF 324) and speaks of "the slight
   variation of individual RS loose soil beds" (printed 5-46, PDF 326). It does not say whether the paired
   values are separate measurements that came out equal or one value assigned to both beds.

## 9. Index rows written (`experiments.csv`)

1. `b68-mdrop-t5-3-rs`: 6 drops (NASA Tests 1 to 6, Bendix drops 10, 11, 12, 13, 16, 17), RS Loose and RS
   Intermediate, so `soil_no` empty and `unknown`; `same-as` `b68-mdrop-10;b68-mdrop-11` because Tests 1 and 2
   already have their own records; `setup_incomplete`.
2. `b68-mdrop-t5-3-ss`: 2 drops (NASA Tests 7 and 8, Bendix drops 20 and 21), SS Loose, `soil_no` 7 `inferred`
   (by family and state; the report does not print a soil number for these drops); no relation;
   `setup_incomplete`.

## Setup

Where each setup fact is printed, and what a simulator user would still have to assume.

### Printed

1. Model: "The LM Model used in this drop test program was obtained from Langley Research Center ... one of
   several identical 1/6-scale models built by Grumman for NASA"; after modification it "has the correct LM pad
   radius, center of gravity height, model weight, and footpad size, and is also very close to the present LM
   gear geometry"; energy absorbing media "crushable aluminum honeycomb capsules mounted inside the telescopic
   shock absorbers". AM-68-1 Vol. I, text, printed 5-2, PDF 281; Figs. 5-1 to 5-3, PDF 282 to 286.
2. Scale factors (full scale / model): length 6, time 6, angular velocity 1/6, linear velocity 1.0, linear
   acceleration 1/6, mass 6^3, mass density 1.0, mass moment of inertia 6^5, force 6^2, spring rate 6.0,
   coefficient of friction 1.0. AM-68-1 Vol. I, Table 5-T1, printed 5-2, PDF 281.
3. Mass and geometry: moments of inertia about X_b, Y_b, Z_b 1.6022, 1.2880, 1.3402 Slug ft.^2; about Y_s, Z_s
   0.09917, 0.09914 Slug ft.^2; initial CG height above a level ground 23.90 Inches; primary strut assembly CG
   14.66 Inches from the upper hinge point; total model weight 68.4 Lbs.; primary strut assembly weight (include
   footpad) 1.82 Lbs.; initial footpad to body centerline radius 27.928 Inches. AM-68-1 Vol. I, unnumbered table,
   printed 5-22, PDF 302; leg geometry in Fig. 5-9, printed 5-15, PDF 295 (inches, full scale in parentheses).
4. Struts: honeycomb with 1/8-inch cells, foil 0.0007 and 0.001 inch; crush load variation +-10 percent; primary
   strut 151 to 183 pounds (low crush load compression stroke) and 300 to 366 pounds (high); secondary struts 125
   to 153 pounds compression, 38 to 46 pounds low tension, 151 to 183 pounds high tension; measured dynamic
   primary strut load "usually around 200 to 225 pounds". AM-68-1 Vol. I, text, printed 5-17 and 5-18, PDF 297
   and 298; load-stroke steps in Fig. 5-10, printed 5-16, PDF 296.
5. Footpads: "Scaled LM footpads were added to each leg" (text, printed 5-4, PDF 283); ball joints on primary
   struts 4, 7, 10, a non-yawing universal joint on strut 1; angular displacement limited to 24 degrees; "In a
   normal touchdown position, the footpads were set against the stop surfaces so they tilted up two degrees
   from a plane normal to the vehicle centerline" (text, printed 5-9, PDF 289; Fig. 5-6, PDF 291); "round
   simulated LM footpads" (text, printed 5-33, PDF 313).
6. Drop rig and pit: "The soil bed which forms the landing surface is 18 feet long and 12 feet wide, with a
   maximum below ground depth of five feet. The depth of soil used was adjusted to suit the varying test
   conditions. The LM model was launched by a six-degree-of-freedom drop test rig which is suspended above the
   soil bed." AM-68-1 Vol. I, text, printed 5-22, PDF 302; Figs. 5-12 and 5-13, PDF 303 and 304. Rig settings
   from a computer program; full description "in Section IV of Reference 1" (text, printed 5-25, PDF 305).
7. Signal wires: "very fine and were suspended above the model such that their presence would not greatly
   influence the free-body motion of the model." AM-68-1 Vol. I, text, printed 5-38, PDF 318.
8. Beds: spreader in four-inch layers; loose beds not compacted; RS intermediate rolled (63-pound roller, 18 in.
   diameter, 24 in. wide, eight passes per 24-inch width per layer) to 18 inches thick; new bed after each drop.
   AM-68-1 Vol. I, text, printed 5-43 and 5-44, PDF 323 and 324.
9. Bed properties per drop: D_r, gamma, phi. AM-68-1 Vol. I, Table 5-T3, printed 5-45, PDF 325 (same values in
   Table 5-T2, printed 5-28 and 5-29, PDF 308 and 309).
10. Touchdown state per drop: V_v, V_h (calculated from tau) and tau. AM-68-1 Vol. I, Table 5-T3, printed 5-45,
    PDF 325. Attitude: zero angular rates, zero pitch and roll, 45-degree yaw (2-2 landing), level surface.
    AM-68-1 Vol. I, text, printed 5-43 and 5-44, PDF 323 and 324; Table 5-T2 ground slope 0, yaw 45.
11. Axes and signs: AM-68-1 Vol. I, text, printed 5-18 to 5-21, PDF 298 to 301; Fig. 5-11, PDF 299.

### Still to be assumed by a simulator user

1. Footpad geometry and mass: Section V does not print the footpad diameter, profile or mass ("Scaled LM
   footpads", "round simulated LM footpads" only).
2. Gravity: not stated for these drops. The scale factors (linear velocity 1.0, linear acceleration 1/6) imply
   the 1/6-scale model was dropped in Earth gravity to represent lunar landing at full scale, but the text read
   does not say so.
3. Bed depth for the RS and SS loose beds (only the RS intermediate depth, 18 inches, is printed); the drop
   location on the 18 by 12 ft bed and the distance to the walls.
4. Soil properties beyond D_r, gamma, phi: grain size and other properties only by soil family in Table 2-3,
   whose unit weights and friction angles differ from the Table 5-T3 beds; no cohesion or stiffness is printed
   for these beds; how gamma and phi were obtained for each bed is not stated.
5. How V_v and V_h were calculated from tau (formula, g, and the rig's release velocity for the drops with
   V_h), and therefore the uncertainty of the touchdown velocities.
6. Strut behavior beyond the printed crush-load ranges and step curves (friction in the struts is named as the
   cause of the higher measured dynamic loads but not quantified); strut stroke limits per Fig. 5-10.
7. The full mass distribution beyond the printed weight, CG height and moments of inertia (inertias printed in
   Slug ft.^2, lengths in inches, weights in Lbs.).
8. Footpad-soil friction and the footpad's initial orientation beyond the stated 2-degree tilt against the stop.
