# Notes on the reading of Figure 4-6a (AM-68-1 Vol. I, printed 4-8, PDF 193)

Reader: Claude, blind transcription, batch tables-s4-b1. Evidence: `packet/p0193.png` (3263 x 4508 px, 300 dpi),
context pages `packet/p0191.png` and `packet/p0192.png`. Pixel positions are on the unrotated scan, (u, v) with u to
the right and v downward from the top-left corner, as in `tools/plot_grid.py`.

## 1. Caption and header as printed

The table is printed sideways: the scan must be turned 90 degrees clockwise to read it (the run numbers then sit at
the left and the caption below the table). The page number "4-8" is printed in portrait orientation at the lower
left of the scan (u 318-401, v 4078-4116).

Caption (below the table when upright; scan u 2562-2627, v 1624-3333):

"Figure 4-6a.  Subscale Drag Test Results - Soil No. 1 - RS Loose"

(The "o" of "Soil" is printed partly broken and looks like "Scil"; there is a stray dot between "Soil" and "No.".)

Header, left to right as read upright (14 columns, same order as the TASK list; the page does not differ). Column
boundaries are the printed rules at the given v on the scan; the header band runs from u 301 (top rule) to u 507
(rule under the header), the body from u 507 to u 2502 (bottom rule).

| # | Header as printed | Scan v range | CSV column |
|---|---|---|---|
| 1 | Run / Number | 3710-3998 | run_number |
| 2 | D / Inch | 3500-3710 | D_in |
| 3 | d / Inch | 3308-3500 | d_in |
| 4 | V subscript H / fps | 3096-3308 | VH_fps |
| 5 | g subscript p with a bar over the g (no units) | 2931-3096 | gp_bar |
| 6 | D subscript r (no units) | 2743-2931 | Dr |
| 7 | gamma (Greek) / Lb./Ft. superscript 3 | 2448-2743 | gamma_pcf |
| 8 | F subscript D / Lb. | 2250-2448 | FD_lb |
| 9 | F subscript V / Lb. | 2045-2250 | FV_lb |
| 10 | F subscript D over (d gamma A subscript ft), a fraction, no units | 1801-2045 | FD_over_d_gamma_Aft |
| 11 | V subscript H over (radical sign over "dg"), a fraction, no units | 1617-1801 | VH_over_sqrt_dg |
| 12 | F subscript D over A subscript ft, a fraction, no units | 1435-1617 | FD_over_Aft |
| 13 | F subscript V over A subscript pt, a fraction, no units | 1246-1435 | FV_over_Apt |
| 14 | alpha (Greek) / Deg. | 1071-1246 | alpha_deg |

No units are printed for columns 5, 6 and 10 to 13. Fractions in the CSV follow the printed form with a space
between whole number and fraction ("1 1/2", "3 3/4").

Body: 32 printed rows, 1-1 to 1-8 and 1-10 to 1-33. Run 1-9 is not printed: the row pitch is a constant 58 to 60 px
in u across the 1-8 / 1-10 boundary (1-8 at u 973-1011, 1-10 at u 1032-1071), so no row was left blank or lost. Row
ink bands in u (Run Number column): 1-1 559-596, 1-2 618-656, 1-3 678-716, 1-4 736-774, 1-5 798-834, 1-6 855-893,
1-7 915-951, 1-8 973-1011, 1-10 1032-1071, 1-11 1091-1128, 1-12 1148-1186, 1-13 1208-1246, 1-14 1265-1305,
1-15 1325-1362, 1-16 1384-1422, 1-17 1442-1480, 1-18 1501-1539, 1-19 1559-1597, 1-20 1618-1656, 1-21 1676-1714,
1-22 1735-1773, 1-23 1793-1833, 1-24 1852-1891, 1-25 1912-1950, 1-26 1970-2010, 1-27 2029-2067, 1-28 2089-2127,
1-29 2147-2186, 1-30 2207-2246, 1-31 2265-2305, 1-32 2325-2365, 1-33 2385-2425.

Constant columns: D is "6" in every row, D_r is "0" (the digit zero) in every row, gamma is "41.1" in every row.
Each was read in every row, not filled down.

## 2. Definitions of A_ft, A_pt and the symbols in the derived columns

The words "A_ft" and "A_pt" are defined only as labels on a drawing; there is no definition in running text on PDF
191 or 192.

1. AM-68-1 Vol. I, Fig. 4-4 "Nomenclature for Constant Penetration Drag Tests", printed 4-6, PDF 191 (scan u about
   1050-1475, v about 875-1000): "Vertical Frontal Area - A_pt" (A with subscript "pt"). The arrow points to a
   hatched circle drawn above the footpad and joined to it by vertical projection lines (the pad outline seen from
   above).
2. Same figure (scan u about 550-1040, v about 1075-1215): "Total Horizontal Frontal Area - A_ft" (A with subscript
   "ft"). The arrow points to a hatched ellipse drawn to the left of the footpad and joined to it by horizontal
   projection lines from the top and bottom of the tilted pad (the pad outline seen along the direction of travel).
3. Same figure, other symbols, as labels only: "alpha" marks the angle between the inclined footpad and a horizontal
   line; "V_H or V_ap" labels a horizontal arrow (the horizontal velocity); "d" is dimensioned from the soil surface
   (the cross-hatched line) down to the horizontal line through the F_D arrow; "F_D or F_ap" labels a horizontal
   force arrow; "F_V or F_np" labels a vertical force arrow.
4. Fig. 4-5 "Drag Test Record Run No. 2-20", printed 4-6, PDF 191, legend "Definition of Measured Functions"
   (scan u about 250-2950, v about 3430-3900; very poor small type, quoted with that caveat): traces "Horizontal
   Displacement", "Horizontal Acceleration", "Vertical Displacement - d", "Angle Function - hs", "Side Load - Fs",
   "Vertical Load - Fv", "Angle Function - hp", "Drag Load - FD", "Horizontal Velocity - VH", and "Footpad Pitch
   Angle, alpha = Sin^-1 (.200 hp + .23? hs)" and "Footpad Roll Angle, beta = Sin^-1 (.200 hp - .23? hs)", where
   the last digit of ".23?" reads as 8 but could be 6 in this type. This is how the record gives alpha.
5. Printed 4-7, PDF 192, second paragraph: "Soil relative and bulk density data were determined from dynamic
   penetrometer tests (g_p bar) of the soil bed." This is the only place on these pages that names g_p bar; it
   implies, but does not state, that D_r is the relative density and gamma the bulk density.
6. "g" in V_H / sqrt(d g) is not defined on PDF 191 or 192 (Fig. 4-5 uses "g/inch" only as the sensitivity unit of
   the acceleration trace). "d" and "gamma" in the derived columns are the table's own columns 3 and 7; no units are
   printed for the derived columns.

PDF 192 (printed 4-7) also says the functions "were generally read from the records at three positions of
horizontal displacement covering a total displacement of 40 inches" and that "the mid-point reading was used in the
development of the force equations", and that Figures 4-6a through 4-16 "are tables showing all of the pertinent
readings obtained during constant penetration drag tests".

## 3. Cells I was unsure of, or that are damaged (all written as read, none with "?")

No cell needed a "?". These cells have broken or marked type; each was read on a 3x to 6x crop and the digit is
written with confidence. Positions are the glyph's ink extent on the scan.

1. 1-21 gamma "41.1": second digit (1) badly broken, only the top with its flag serif and bits of the foot serif are
   printed; u 1673-1713, v 2599-2617. The 4 is also broken. The surviving strokes fit only a 1.
2. 1-22 alpha "28.4": second digit has a broken lower-left stroke; u 1728-1767, v 1160-1183. Its upper bowl is
   closed down to the waist (a 3 in this font has an open upper left with a ball terminal), so 8, not 3. This is the
   cell most likely to be read differently (as "23.4").
3. 1-33 FD/Aft "3.27": middle digit heavily broken, only the top arc and the base bar with its right upturn are
   printed; u 2378-2416, v 1491-1515. Only a 2 has that flat base with the upturn.
4. 1-31 FD/(d gamma A_ft) "59.7": top bar of the 5 printed detached from the body; u 2258-2311, v 1966-1988; a stray
   dot below the value.
5. 1-14 gamma "41.1": second digit has a break in its stem; u 1264-1302, v 2597-2617.
6. 1-17 FD/(d gamma A_ft) "111.0": third digit (1) has a white gap in its stem; u 1437-1476, v 1938-1958.
7. 1-25 g_p "12.0": left side of the 0 broken; u 1909-1948, v 2973-2999.
8. 1-27 g_p "12.1": top of the last 1 partly broken; u 2027-2065, v 2975-2995.
9. 1-33 D_r "0": gap in the left side of the 0; u 2382-2419, v 2819-2845. 1-33 FV/A_pt "1.77": small gap in the last
   7 (u about 2385-2425, v 1268-1289).

## 4. Other things a careful reader should know

1. Scan quality: the image is bilevel (black and white, no gray), 300 dpi, clean in the table. Type is sharp in most
   cells; breaks are listed above. Dark scan-edge bands run along the right edge (u above about 3100) and the bottom
   edge (v above about 4400), with a short mark at the top-left corner; none touch the table.
2. Stray marks inside the table, none part of a value: a short vertical stroke at u 1408-1442, v about 2181, left of
   the F_V values between rows 1-16 and 1-17; a tick above the 6 of 1-24 FD/(d gamma A_ft) at u about 1835-1852, v
   about 1986-1991; a tick between rows 1-31 and 1-32 left of the 4 of 1-32 FD/(d gamma A_ft) at u about 2306-2320, v about
   1984; a dot above the 2 of 1-26 d at u about 1961, v about 3454; a dot at the upper left of 1-28 F_V at u about
   2084, v about 2182; a hook-shaped mark above the 2 of 1-29 F_V at u about 2128-2144, v about 2182.
3. Reading procedure: pass 1 on upright crops of 8 rows by 4 or 5 columns at 1.5x; pass 2 on upright strips of 16
   rows by 2 or 3 columns at 1.4x (different grouping, so a row-alignment slip would show); the two passes agreed in
   every cell. Damaged cells were then read at 3x to 6x without interpolation. Crops are in `out/crops/`, the crop
   scripts in `out/scripts/`.
4. Arithmetic cross-check (used only to choose cells to look at again; it did not set or change any value; the unit
   interpretation is my inference, not printed): (a) in all 32 rows FD/(d gamma A_ft) equals (FD/A_ft x 144) / (d/12
   x gamma) times a nearly constant 1.021 to 1.029, so columns 3, 7, 10 and 12 are mutually consistent and FD/A_ft
   behaves like lb/in^2; (b) V_H / sqrt(dg) matches V_H / sqrt(d/12 x 32.2) within the rounding of its one printed
   decimal; (c) F_V divided by FV/A_pt gives 26.6 to 29.1 (in^2, near the 28.3 in^2 of a 6 in circle) in most rows,
   but 30.4 in 1-26, 57.4 in 1-28 and 21.7 to 23.5 in 1-29 to 1-32. Those F_V and FV/A_pt cells were re-read at 2.5x
   and are clean and as transcribed ("40.4", "1.33"; "48.2", "0.84"; "21.6", "0.98"; "26.2", "1.21"; "33.4", "1.47";
   "36.5", "1.55"). The inconsistency is in the printed table, not in the reading.
