# Transcription notes: pages-appc-b1

Read PDF pages 115-137 from the supplied PNG images. All 23 page files have been checked against their images. Enlarged crops and rotated reading copies are retained in `out/`. No OCR, outside report text, or other transcription was used. The supplied figure index was used for figure identifiers; the images govern the readings below.

## Page numbering and rotation

The visible numbers run from C-1 through C-23 and agree with every `inferred_label`. These visible numbers override the following `printed_label` entries in the supplied map:

| PDF page | Map printed_label | Number on image and in transcription |
| --- | --- | --- |
| 116 | unknown | C-2 |
| 117 | i | C-3 |
| 120 | i | C-6 |
| 123 | 1 | C-9 |
| 125 | i | C-11 |
| 131 | unknown | C-17 |
| 132 | unknown | C-18 |
| 133 | 0 | C-19 |
| 136 | i | C-22 |
| 137 | unknown | C-23 |

The figures on PDF 136 and 137 need a 90° clockwise turn for upright reading; their headers record `rotation: 90`, following the supplied figure-index convention. Their printed page numbers remain oriented with the portrait page. All other pages have `rotation: 0`.

## Doubt and misprint markers

Every `[?]` and `[sic]` in the page files is accounted for here. There are no `[illegible]` markers.

| Page | Location | Reading and reason |
| --- | --- | --- |
| p0117 / C-3 | Caption, between “Data” and “Shear” | `= [sic]`. Enlarging the mark shows a substantial upper stroke and a shorter separate lower stroke. Preserved as an equals sign rather than normalizing to the hyphen used on most sheets. The unequal stroke lengths made this a hesitation. See `crop-117dash.png`. |
| p0121 / C-7 | Lower panel vertical axis | `$γ_σ$ [sic]`, with gamma rather than delta. The glyph has the open, forked top of gamma. |
| p0122 / C-8 | Legend's second column header | `τ [sic] (PCF)`, not gamma. Enlarged in `crop-122legend.png`. |
| p0124 / C-10 | Legend's first column header | `τ [sic] (PSF)`, not sigma. Preserved the printed tau. |
| p0130 / C-16 | Caption, between “Data” and “Shear” | `= [sic]`. A short second stroke is visible below the main stroke; it is not a clean conventional equals sign. Preserved that two-stroke reading rather than replacing it with a hyphen. See `crop-130dash.png`. |
| p0130 / C-16 | Lower panel vertical axis | `$δ_τ$ [sic]`, not `$δ_σ$`. The subscript is visibly tau. |
| p0131 / C-17 | Second legend entry, relative-density symbol | `$D_r$ [?]`. The capital's right side is damaged/open and can resemble C; the left stem and surviving upper and lower portions support D. This remains flagged. See `crop-131heading.png`. |

## Other hesitations and image-based decisions

- p0115 / C-1: The first paragraph reads “was obtained,” and the second reads “series of tests were performed.” These grammatical forms are retained. The reference is “Figures C-1A through C-7B,” even though a C-7C sheet occurs later in this packet. The paragraph's quoted letters contain the commas inside the quotation marks: `"A," "B," "C,"`.
- p0116 / C-2: The axis labels visibly contain only `(PSF)` horizontally and `max (PSF)` vertically. No sigma or tau was supplied in the blanks. Enlargements `crop-116x.png` and `crop-116axes.png` confirm this. The legend uses an upright open triangle although the plotted triangles point downward; the legend's upright triangle is retained.
- p0117 / C-3: Both displacement labels print `10^3`, with no minus sign. The 2935 test's unit weight reads `46.8`. The heading begins `46.7`, and the relative-density lower bound is `.5`, not `.50`.
- p0118 / C-4: The horizontal label prints `10^-3`, but the lower panel's vertical label prints `10^3`. This difference is preserved.
- p0121 and p0122 / C-7 and C-8: Both third legend rows read `2935`, not the `2995` in the supplied index. The 3 is clear at full resolution. See `crop-121legend.png` and `crop-122legend.png`.
- p0125 / C-11: All five legend unit weights print `75.0`; the heading prints `75`. Retained the trailing decimal zeros rather than using the index's shortened values.
- p0127 / C-13: The first legend-column symbol is a damaged sigma, not pi; retained `σ (PSF)`. See `crop-127cols.png`.
- p0128 / C-14: The last normal-stress entry is `741`, not `734`. The marker order differs from neighboring sheets and was read from this page.
- p0129 / C-15: The printed angle is `36.9°`, not `36.8°`. Enlargement clearly shows the descending stroke on the 9 (`crop-129angle.png`). The attribution reads `MM-65-2`, not `MM-66-2` (`crop-129report.png`). The brace associates the attribution with the last three density entries. No outside source was consulted to “correct” the report number.
- p0130 / C-16: The heading reads `95.2 to 97.3`, while the third legend row prints `97.6`. Both are preserved without reconciling the discrepancy.
- p0131-p0134 / C-17-C-20: Short horizontal remnants after “LSM Soil” and many other words were treated as scan streaks/underline remnants. On C-17 the isolated remnant could look like a trailing hyphen; comparison with the page's many baseline streaks led to omitting it as an artifact, not punctuation.
- p0132-p0134 / C-18-C-20: Displacement-unit labels read `(in)` without a full stop, unlike the earlier `(in.)` labels.
- p0133 / C-19: The legend prints `1961` and `714`. Neither was changed to the more common values on adjacent sheets. Its caption begins “LSM Soil Dense,” not “Direct Shear Test Data.”
- p0134 / C-20: There is no visible gamma before the heading's equals sign; the transcription starts that line with `=`. No missing symbol was invented, and the blank is not marked illegible. The legend headers contain `σ` and `γ` without units. The second normal-stress entry is `3814`, and the last is `147`. The word “Rebound” is included. See `crop-134heading.png` for the blank before `=`.
- p0135 / C-21: The caption says “Normal Shear Stress.” This wording is retained without changing it to “Normal Stress.” The legend uses `Lb/ft³`, with lowercase ft and without the periods used on the earlier sheets.
- p0136 / C-22: The lowest normal-stress entry initially resembled `2.4`. The enlarged lower part of its first digit supports a damaged 3, so the final reading is `3.4`, without a doubt marker. See `crop-136legend.png`.
- p0136 and p0137 / C-22 and C-23: The legend column headers contain only `(PSI)` and `(PCF)`; no sigma or gamma is visible. These were not supplied from the index. The highest-load symbol is a hollow curved wedge/quarter-circle and is described as “open quarter-circle”; the remaining symbols are represented by Unicode outlines. Neither page prints the soil name or density range in a separate heading.

## Protocol applications

- The unnumbered Appendix C title is represented by two Markdown headings, with `sections: ["C"]`. No numbered subsection heading occurs elsewhere in this packet.
- Figure identifiers follow the supplied `FC-...` index. Captions also retain their printed `Figure C-...` labels. Legend-table rows are pairs in printed top-to-bottom order under `legend:`, with the printed column headers and associated marker shapes. These embedded legend tables do not have separately printed table numbers, so `tables: []` is used.
- Displacement symbols are the printed lowercase delta `δ`, not the uppercase delta in the protocol's illustrative example. Subscripts use the prescribed dollar-delimited Unicode notation. Superscript 3 in cubic units is represented as `³`; axis powers use `10^3` or `10^-3`.
- In addition to the four prescribed figure fields, printed headings and notes are transcribed as body text. Printed angle labels and the two construction-line labels `3680` and `3820` on C-17 are also retained as body text after the figure block. These are explicitly printed annotations, not values estimated or sampled from curves. No curve coordinates or axis tick inventories were extracted.
- The figure blocks keep a one-line description; captions printed across two lines are joined without inventing punctuation. “Same Notation As Above” is retained on each sheet where it is printed.
- All page files remain `review_status: single-reading`; checking this transcription against its own images is not an independent second transcription.
