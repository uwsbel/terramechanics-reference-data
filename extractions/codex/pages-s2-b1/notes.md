# Transcription notes: pages-s2-b1

All 22 pages, p0026–p0047, were visually read and checked against their supplied page images. Enlarged crops and rotated reading copies are retained in this folder. No OCR engine, text-recognition tool, or network source was used. Page files retain `review_status: single-reading` as required.

## Uncertain readings and printed anomalies

- **p0027, DST definition:** `in [sic] In-Place` is printed, rather than “an In-Place.” Enlargement confirms the first word is “in.”
- **p0027, gravitational constant:** the image has a short hyphen between the equals sign and `32.2`. Transcribed `earth =-32.2`, without correcting the sign. The enlargement `p0027-sign2.png` shows this mark distinctly.
- **p0027, ksi definition:** the two successive hyphens before `Kips` are retained as `--Kips`; confirmed in `p0027-detail.png`.
- **p0030, opening and boundary-condition discussion:** retained the printed “performance of the lunar surface” and “immediately comment on”; neither was rewritten to improve the wording.
- **p0032, first paragraph:** `behavior [?]` has missing portions of its first letters. The remaining letters and spacing support “behavior,” but the image does not preserve the whole word.
- **p0032, third paragraph:** `or [sic] individual grains` is clearly printed. The enlargement confirms “or,” not “of.”
- **p0033, Figure 2-4:** the horizontal axis is capital `E` with subscript `ij`, transcribed `$E_{ij}$`, rather than replacing it with epsilon.
- **p0034, Figure 2-5:** spacing is labeled with an uppercase subscript R, transcribed `$D_R$`.
- **p0035, first paragraph:** `quantitively [sic]` is printed; confirmed by enlargement. It was not expanded to “quantitatively.”
- **p0039, last column header:** `Final Select'n [?]` is the chosen reading of the very small abbreviation. The final characters remain unclear even enlarged.
- **p0039, first Silica Sand row:** `AASCO [?] #4, White`; the supplier name is pixelated. This is the closest visible reading, not a name supplied from outside evidence.
- **p0039, Air Floated Clay density:** enlargement resolves the cell as `80-100`.
- **p0039, Microballoons description:** `BJO-0930 [?]`; the first character and the zero/letter-O distinction are not fully secure. The rest of the description, including `.0002" to .005"`, is legible.
- **p0039, Dylite-Unexpanded description:** `"ISO-Fills" [?]`; the small commercial name and its letter case are not completely secure.
- **p0039, CAB-O-SIL grades:** enlargement supports `M-7,M-D-7`, without the extra “1” initially suspected between M and D. The densities in the three lines are `2-7`, `7`, and `6`.
- **p0039, Pelaspan:** this is the visible name in the material column; enlargement resolved the initial hesitation.
- **p0039, narrowly graded black volcanic cinders:** the density reads `40-65`, while the corresponding red row reads `40-55`. The black-row fraction is read as `1/8"`; the lower serif of the 1 is unusually long.
- **p0039, short trailing marks:** short typewriter-like hyphens after Charcoal, Pumice-Powdered, Dylite-Unexpanded, the Polylite description, and the Marble Chips text are retained. Long horizontal streaks, stray specks, and table-rule damage are treated as scan artifacts.
- **p0041, -200 column header:** `%** [?]` is the chosen reading. The upper loop and diagonal of the percent sign are damaged; the lower loop remains. Comparison with the similarly damaged percent signs in the cells supports a percent sign rather than a Greek letter.
- **p0041, row 1, -200 column:** `<3% [?]`; the middle of the 3 is partly missing, so the digit is flagged.
- **p0041, row 4 unit weight:** `50.6` is clearly printed.
- **p0041, row 12 description:** `Marbel [sic]` is printed, while the earlier row uses “Marble.” Confirmed in `p0041-marbel.png`.
- **p0042, flowchart:** the source labels `PS Inter` and `LSM Loose` are retained as printed.
- **p0042, upper right Effects box:** `$C_n$ [sic]` has a visibly lowercase n subscript, whereas the lower right box and central boxes use u. The differing subscript is preserved; see `p0042-right.png`.

Every `[?]` and `[sic]` in the page files is covered above. No `[illegible]` token was needed; uncertain partial readings have `[?]` instead.

## Printed page numbers versus the map

The visible printed labels are `2-1` through `2-22` for PDF pages 26 through 47, respectively. The printed numbers govern the headers.

| PDF page | Printed on image | Map printed_label | Map inferred_label |
| --- | --- | --- | --- |
| 26 | 2-1 | unknown | unknown |
| 27 | 2-2 | 1 | 1 |
| 28 | 2-3 | unknown | unknown |
| 30 | 2-5 | 11 | 2-5 |
| 31 | 2-6 | 1 | 2-6 |
| 32 | 2-7 | unknown | 2-7 |
| 35 | 2-10 | unknown | 2-10 |
| 36 | 2-11 | i | 2-11 |
| 37 | 2-12 | unknown | 2-12 |
| 39 | 2-14 | l | 2-14 |
| 41 | 2-16 | ii | 2-16 |
| 45 | 2-20 | unknown | 2-20 |

All remaining map labels agree with the image. Only pages 26–28 differ from the map's inferred labels.

## Layout and protocol decisions

- p0037 and p0042 require a clockwise quarter turn and have `rotation: 90`. The supplied p0041 image is already landscape and upright, so its header has `rotation: 0`, regardless of the sideways printed page number.
- The Section II banner and title on p0026 are preserved as headings; `sections` lists the numbered subsection headings `2.1` and `2.1.1`.
- Figure blocks use the prescribed caption/axes/legend/description fields. Schematics, equations, flowchart labels, and the photograph scale annotation are body text adjacent to their blocks because the block schema has no separate annotation field. Unplotted figures have `axes: none` and `legend: none`.
- Figure 2-2's three equations and the force-displacement relation on p0035 have no printed equation numbers. They are displayed without invented numbers, and `equations` remains empty.
- Table 2-2 uses printed braces to share cells. The three CAB-O-SIL lines and three sugar-bonded lines are grouped with `<br>` inside cells, retaining each printed entry once. The final comment applies to Aluminum Oxide Crust and the three sugar-bonded materials; it is placed in the first row of that group. Blank cells remain blank.
- Table 2-3's spanning “Grain Size Parameters” heading is preserved above “Mean Size” in the first of its four subordinate columns using `<br>`.
- No plotted curve values or axis tick values were transcribed. Incidental photographic equipment markings do not provide readable report annotations; the photographs are represented by their captions and figure blocks.
- No prose paragraph breaks mid-sentence across the supplied page boundaries. The definitions beginning “where,” on p0036 follow the standalone equation on p0035 as separate body paragraphs, so no paragraph continuation markers were added there.
