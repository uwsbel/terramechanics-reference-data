# Inventory s6-b1, Claude blind reading: notes

Source: AM-68-1 Volume I (NASA CR-92208), PDF 345 to 440 (printed 5-65 to 6-82). Every page image was looked at;
sideways and multi-panel pages were cropped and zoomed. `inventory.csv` has 83 rows: 8 Section V figures (F5-40 to
F5-47) and 75 Section VI rows (F6-1 to F6-27, with the four-sheet figures F6-11 to F6-26 as one row per sheet,
`<id>-pNNN` for sheets 2 to 4). Helper scripts and raw reading notes are in `out/scratch/` (`build_inventory.py`
holds every reading that went into the CSV).

Pages with no figure or table (text only): PDF 345 to 349 (5-65 to 5-69), 353, 354, 357, 358, 359 (6-1), 361
(6-3), 364 (6-6), 369 (6-11), 372 (6-14), 374 (6-16), 379 (6-21). There are no numbered tables in this range; the
four tables of Section VI are numbered as figures (F6-4, F6-6, F6-8, F6-10), so they are kind `figure`, data_form
`table`.

## Counts

### Detail correlation drops, NASA 1 to 8

Conditions from F6-10 (PDF 373, printed 6-15, printed sideways): all at 45 deg yaw on level ground, all Stable.

| NASA drop | Bendix drop, date | soil, state | VV, VH (fps) | measured histories (Section VI) | computed-only figure |
|---|---|---|---|---|---|
| 1 | 10, 7-18-67 | RS loose, Dr 0, 46.9 pcf | 10, 0 | F6-13, PDF 384 to 387 (6-26 to 6-29) | F6-20, PDF 412 to 415 |
| 2 | 11, 7-19-67 | RS loose, Dr 0, 46.9 pcf | 5, 7 | F6-11, PDF 375 to 378 (6-17 to 6-20) | F6-12, PDF 380 to 383 |
| 3 | 12, 7-20-67 | RS loose, Dr 0, 47.1 pcf | 5, 7 | F6-14, PDF 388 to 391 (6-30 to 6-33) | F6-21, PDF 416 to 419 |
| 4 | 13, 7-20-67 | RS loose, Dr 0, 47.1 pcf | 10, 0 | F6-15, PDF 392 to 395 (6-34 to 6-37) | F6-22, PDF 420 to 423 |
| 5 | 16, 7-25-67 | RS intermediate, Dr printed "3", 53.0 pcf | 5, 7 | F6-16, PDF 396 to 399 (6-38 to 6-41) | F6-23, PDF 424 to 427 |
| 6 | 17, 7-25-67 | RS intermediate, Dr 0.3, 53.0 pcf | 10, 0 | F6-17, PDF 400 to 403 (6-42 to 6-45) | F6-24, PDF 428 to 431 |
| 7 | 20, 7-28-67 | SS loose, Dr 0, 96.0 pcf | 5, 7 | F6-18, PDF 404 to 407 (6-46 to 6-49) | F6-25, PDF 432 to 435 |
| 8 | 21, 7-28-67 | SS loose, Dr 0, 96.0 pcf | 10, 0 | F6-19, PDF 408 to 411 (6-50 to 6-53) | F6-26, PDF 436 to 439 |

Every drop has both a measured-history figure (experimental and computed curves, original strut damping 10 Sdot)
and a computed-only figure (higher strut damping, 10 Sdot^1/2 primary and 30 Sdot^1/2 secondary, Sdot the stroking
velocity in ft/s; prose 6-11, PDF 369, and 6-21, PDF 379). Section V also prints measured histories for NASA Tests
1 and 2 only (F5-22 to F5-39, agreed index); drops 3 to 8 are printed only in Section VI.

Measured-history figures (F6-11, F6-13 to F6-19), four sheets each, x "Elapsed Time, Second" 0 to 0.1 s:

1. Sheet 1, 4 panels: a) Footpad Velocity Vap (Inches Second), b) Footpad Velocity Angle theta (Degrees),
   c) Footpad Penetration d (Inches), d) Vehicle Pitch Acceleration (Degrees Second^2 on F6-11; printed "Degrees
   Second" without the square on F6-13 to F6-18).
2. Sheet 2, 4 panels: e) Vehicle Pitch Rate (Degrees Second), f) Vehicle Pitch Angle (Degrees), g) Vehicle c.g.
   Vertical Position X (Inches), h) Vehicle c.g. Horizontal Position Y (Inches).
3. Sheet 3, 4 panels: i) c.g. Vertical Velocity Xdot (Inches Second), j) c.g. Horizontal Velocity Ydot (Inches
   Second), k) c.g. Vertical Acceleration Xddot (Inches Second^2), l) c.g. Horizontal Acceleration Yddot (Inches
   Second^2).
4. Sheet 4, 2 panels: m) Footpad Pitch Angle alpha (Degrees), n) Footpad Roll Angle beta (Degrees).

Each panel of sheets 1 to 3 has two curves, labeled "Experimental" and "Computer" with arrows (8 curves per sheet).
Sheet 4 has 3 curves (panel n experimental only; the program does not compute roll, prose 6-16), except F6-13 (drop
1), where panel n also has a computer line at zero labeled "Computer" (4 curves). Total measured panels: 14 per drop,
112 in all.

Computed-only figures (F6-12, F6-20 to F6-26), four sheets each, x "Time Seconds" or "Time/Seconds" 0 to 0.12 s,
one computed curve per panel, panels a to m only: sheet 1 a to d (a Vap, b theta, c d, d pitch angle; see quirks),
sheet 2 e to h (e pitch acceleration, f pitch rate, g X, h Y), sheet 3 i to l (i horizontal velocity Ydot, j
vertical velocity Xdot, k Xddot, l Yddot; note i and j are in the opposite order from the measured-history
figures), sheet 4 m alone (alpha). 13 panels per drop.

### Other figures with measured data

1. F5-40 (PDF 350, 5-70): stability profile, RS dense, 45 deg yaw, 15 deg downhill slope; drops 22 to 34 as markers
   (stable, unstable, unstable but close to balancing) with a hatched transition band; VV versus VH in ft/s.
   Values agree with F6-6 except drop 25 (see below).
2. F5-41 (PDF 351, 5-71): same for RSM-b, drops 64 to 67 and 69 to 77 (63 and 68 not plotted); values agree with F6-8.
3. F5-42 (PDF 352, 5-72): RS dense, 22.5 deg yaw, drops 35 to 44, all stable, no band; one marker unnumbered.
   No Section VI table lists these drops.
4. F6-4 (PDF 365, 6-7): table of rigid surface drops 45 to 62 (plywood blocks, 10 deg slope, 22.5 deg yaw): VV, VH,
   Stable, remarks.
5. F6-5 (PDF 366, 6-8): rigid surface stability profile, drops 45 to 62 as markers, experimental band and a
   calculated (rigid surface program) band.
6. F6-6 (PDF 367, 6-9): table of RS dense drops 22 to 34: VV, VH, slope, yaw, Dr, density, phi, Stable, remarks.
7. F6-7 (PDF 368, 6-10): the F5-40 markers and experimental band with four computed profiles (rigid surface,
   original soil equations, modified soil equations, increased strut damping).
8. F6-8 (PDF 370, 6-12): table of RSM-b drops 63 to 77, same columns as F6-6.
9. F6-9 (PDF 371, 6-13): the F5-41 markers and band with the same four computed profiles.
10. F6-10 (PDF 373, 6-15): table of the eight detail correlation drops (conditions above).
11. F6-27 (PDF 440, 6-82): computed minus experimental footpad penetration versus time for drops 1 to 8 in stacked
    strips at 0.25 inch per division, with the measured maximum depth Dmax of each drop in the legend (4.3, 4.2,
    4.2, 5.3, 3.4, 3.0, 3.3, 3.7 in.); Dmax agrees by eye with the experimental maxima in panels c. The damping used
    for the computed depths is not stated.

The photographs F5-43 to F5-47 (PDF 355, 356) show the five exploratory drops of Section 5.7 (RS dense, 3 1/2 deg
slope); their conditions are in the prose (5-74, PDF 354), not in a figure.

## Statements in the prose that disagree with the figures or tables

1. Repeat pairs. Printed 6-21 (PDF 379): "these results show the degree of repeatability obtained (Drop No. 3 same
   as No. 1, No. 4 same as No. 2)". F6-10 (6-15, PDF 373) gives drops 1 and 4 VV 10, VH 0 and drops 2 and 3 VV 5,
   VH 7, so the repeats are 3 of 2 and 4 of 1. The figures agree with the table: F6-14 (drop 3) has a horizontal
   velocity starting at 85 in/s like F6-11 (drop 2), and the computed traces of F6-21 (drop 3) nearly coincide with
   F6-12 (drop 2), F6-22 sheet 1 a to c with F6-20 (drop 1). F6-14 is not a reprint of F6-11: the computed traces
   are nearly identical but the experimental traces differ (panel d compared side by side).
2. Variable list. Printed 6-14 (PDF 372) defines the plain Xi as "vehicle pitch acceleration - deg./sec.2", Xi with
   one dot as pitch rate and Xi with two dots as "vehicle pitch angle - degrees" (dots inverted), and uses Z, Zdot,
   Zddot for the c.g. vertical position, velocity and acceleration (6-14 and 6-16), where every figure uses X, Xdot,
   Xddot (and the figure captions put two dots on pitch acceleration).
3. Rolling. F6-6 (6-9, PDF 367), drop 22 remark: "RS Dense soil- 10 rolls per two-inch layer"; F6-8 prints "RSM 10
   Rolls". Printed 5-68 (PDF 348) describes the gross correlation beds as "layers about four inches thick, followed
   by rolling 20 times (10 back and forth cycles) for every 24-inch width of the soil bed".
4. Third group yaw. Printed 5-69 (PDF 349): "The third group of tests (numbers 63 through 77) were made on RSM-b dense
   soil with the same initial conditions as that of the first group" (45 deg yaw). F6-8 lists drop 63 at 22.5 deg
   yaw and drop 68 on unrolled soil at Dr 0.10; neither is plotted in F5-41 or F6-9.
5. Drop 25. F6-6 prints drop 25 at VV 12, VH 5, No; F5-40 and F6-7 both plot drop 25 as unstable at VH about 6
   (next to drop 24 at VH 5).
6. F5-41 inset reads "RS Dense Soil, 45 deg Yaw" while its caption and F6-8 say RSM-b.
7. F6-7 legend says "Dr (From DPT Tests) as Marked" but no Dr value is printed on the plot.
8. Prose 6-16 (PDF 374) says the experimental footpad roll angle of drop 2 stays below eight degrees: F6-11 panel n
   peaks just under 8 deg. Agrees.
9. Prose 6-21 (PDF 379) cites "Figures 6-12(a) through 6-12(m)" for drop 2 at higher damping; F6-12 indeed has
   panels a to m. Agrees.
10. Prose 5-66 (PDF 346) says F5-25 applies to drop No. 10 and F5-32 to drop No. 11: these are Bendix numbers, and
    F6-10 maps Bendix 10 and 11 to NASA 1 and 2. Agrees.
11. Prose 5-73 (PDF 353) calls the exploratory drops "drops Nos. 2 through 6 in Paragraph 5.3"; the photographs are
    captioned "Exploratory Model Drop No. 2" to "No. 6". This numbering collides with NASA detail correlation drops 2
    to 6, which are different tests.

## Printing quirks in the figures

1. F6-10 drop 5 relative density printed "3" with no decimal point (drop 6 prints "0.3").
2. F6-12 sheet 1 (PDF 380): panel d captioned "Vehicle Pitch Acceleration" but its axis is Degrees 0 to 3.75 and the
   curve is a pitch angle (the acceleration is panel e on sheet 2). F6-12 sheet 2 panel f has a tick printed 15 where
   25 belongs.
3. F6-20 sheet 1 (PDF 412): fourth panel lettered "e) Vehicle Pitch Acceleration" (no panel d), axis "Vehicle Pitch
   Degrees" with every tick printed 0.
4. F6-15 sheet 3 (PDF 394): panels i, j, k show other quantities than captioned (i acceleration-like with unit
   Inches Second^2, j vertical velocity, k horizontal velocity).
5. F6-16 sheet 2 (PDF 397): captions e (Pitch Rate) and f (Pitch Angle) do not match their axes (Degrees and
   Degrees Second) or curves.
6. F6-19 sheet 1 (PDF 408): panel d captioned "Vehicle Pitch Angle" but axis Degrees/Second^2, acceleration-like.
7. F6-21 sheet 2 (PDF 417): pitch acceleration axis labeled "Inches".
8. F6-25: sheet 1 panel d axis labeled "Pitch"; sheet 2 panel e has no visible axis label.
9. Computed-only figures for drops 1, 4, 6, 8 (VH 0) plot near-zero quantities whose tick labels are truncated and
   unreadable: F6-20 sheet 3 i; F6-22 sheet 1 d (all "0"), sheet 2 f and h (all "0.0020"), sheet 3 i; F6-24 sheet 1
   d (all "0"), sheet 2 e (signs dropped on some ticks), f and sheet 3 i; F6-26 sheet 1 d and sheet 2 h (ticks
   repeated). Values on these panels cannot be scaled from the axes.
10. F6-24 sheet 2 panel g: time ticks printed 0.2, 0.4, 0.6, 0.8 for 0.02 to 0.08. F6-26 sheet 1 panel a: a time
    tick printed 0.00 where 0.04 belongs.
11. F6-4 drop 49 yaw reads like 22.3 (the other 17 rows print 22.5). F6-6 drop 32 row partly illegible (number "3'",
    date "8-1 -67", Stable "N)").
12. F6-8 density column: the digits 6 and 8 are hard to tell apart in this scan (drop 63 reads 86.0 or 88.0).
13. F5-42: one marker (near VH 8, VV 3.9) has no drop number; 43 is the number in 35 to 44 that is not printed.
14. F5-40: drop 27 drawn with a partly filled mark (F6-6 lists 27 stable, borderline); F5-40 markers sit about 0.1
    ft/s left of the F6-6 VH values.
15. List of illustrations (PDF 14): Figures 6-20 to 6-26 are titled "Computer Program For LM Model Drop No. N" where
    the captions say "Computer Results For ..."; 6-10 is "LM Model Drops For Detail Correlation Studies" (caption
    "LM Model Drop Tests ..."); 6-12 "Computer Results For LM Model Drop No. 2". Page numbers in the list match the
    folios.

## Page map

The page map's `printed_label` is an OCR misread on several pages; the images show the inferred labels: PDF 350
(5-70), 365 (6-7), 368 (6-10, map "2-2"), 372 (6-14), 385 (6-27), 408 (6-50), 409 (6-51), 413 (6-55), 416 (6-58),
418 (6-60), 423 (6-65), 428 (6-70), 431 (6-73), 435 (6-77), 438 (6-80). PDF 374: the folio is printed with a filled
loop and reads like "6-18"; the sequence gives 6-16. PDF 363 has the folio 6-5 printed (map: unknown).

## Conventions I applied

1. Curve counts: each legend marker class present on a stability profile is one series, and each banded or patterned
   profile line (hatched transition band, computed profiles) is one trace, as the agreed F5-20 row counts it (3
   marker classes plus a band = 4).
2. First-panel axes go in the axis columns; every panel's quantity, printed unit and range is in `notes`. Pitch
   acceleration in degrees per second squared has no vocabulary token; I wrote `deg_s2` (by analogy with `in_s2`).
   A unit printed wrongly is recorded as printed (F6-21 sheet 2, "Inches" -> `inch`), with the problem in `notes`.
3. `test_type`: `model drop` for anything carrying measured drop results, `soil model` for the program flow charts
   and for the computed-only figures F6-12 and F6-20 to F6-26.
4. `in_scope`: measured histories, tables and the Section V profiles `yes`, priority 1; the Section VI profiles
   (F6-5, F6-7, F6-9) and F6-27 `maybe`, priority 2, because their measured content is already in a table or a
   Section V profile and the rest is computed; computed-only figures `maybe`, priority 3 (the report's own
   simulation, not measurement); photographs and flow charts `no`, priority 3.
5. Relations: `same-as` links a figure to the table row of the same drop (F6-10, T5-3, T5-2) and, for drops 1 and 2,
   to the Section V figures of the same quantity (traces not compared; Section V pages are not in the packet).
   `derived-from` links profiles to the tables they plot and F6-27 to the measured-history figures; computed-only
   figures point at F6-10 for their input conditions. T5-2 page targets: F6-4 uses T5-2-p310 and p311 as the agreed
   F5-20 row does, F6-8 the two RSM pages of T5-2 by the agreed index soils column; for the others the T5-2 page was
   not identified and the target is `T5-2`. No `mcc_relevant` evidence in this range (each bed was re-raked and
   rolled before every drop, 5-69).

## What I could not read

1. Tick labels of the near-zero computed panels listed under quirk 9.
2. F6-16 sheet 1 panel d lowest tick (range read as up to 12500; bottom value unclear).
3. F6-6 drop 32 number and date (partly), F6-8 densities where 6 and 8 are ambiguous, F6-4 drop 49 yaw.
4. Which markers in the F6-5 cluster at VH 4.7, VV 8 (drops 45, 46, 50) carry which symbol.
