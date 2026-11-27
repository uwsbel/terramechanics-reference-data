# Review of batch pages-vol2-ab-b1: Volume II Appendix A, PDF 2 to 24 (printed A-1 to A-23)

Date: 2026-10-08. Reviewer: Claude (page re-reads and glyph measurements on the scan). No human
audit yet.

## What was transcribed

The opening page of Appendix A and the specifications of soils No. 1 (RS loose), No. 2 (PS loose)
and No. 3 (RS intermediate): numbered specification items, chemical analysis tables, normative
mineral tables, photomicrographs, grain size curves with their parameter tables, density charts
and friction angle charts. Codex (gpt-6-astra, high) and Claude worked blind from the same images.

## Diff results (`diff.md`)

| result | pages |
|---|---|
| agreed | 12 |
| resolved | 11 |
| pending | 0 |

Every number agreed: the chemical analyses (the Volcalite column sums to the printed 99.25), the
mineral percentages, the grain size parameters (D50, D10, Cu, D95 with ranges), the density chart
end labels (40.1 to 54.0 pcf for RS, 23.3 to 31.1 pcf for PS) and the friction angle, modulus and
relative density statements. What differed was transcription form.

## Decisions (`decisions.csv`)

1. **Chemical formulas keep the typewriter digits.** On the scan the character in "Ca0", "Mg0",
   "Si02" is 24 px wide, the width of the digit zero in the values, against 36 px for the capital
   O of "Oxide" on the same line; "A1203" is printed with the digit 1 (19 px) rather than the
   letter l (16 px). Rule 10 keeps them as printed. Codex had normalized to letters (SiO2), Claude
   had kept the zeros but typed Al with a letter l; the canonical uses `$A1_20_3$`. A search for an
   oxide should use its name. Codex's `[sic]` on "Na0" (sodium oxide is Na2O) and on "S_i0_2" (a
   subscript i) is kept.
2. **Codex was right** on the starred line under each chemical table as a footnote (rule 7), on
   the normative mineral tables having no printed column heads (Claude added "Mineral, Percent"),
   on the `[sic]` after "ilmenite" given as an example of an iron hydroxide on printed A-3 (soil
   No. 3's page prints limonite there), and on the dot before "4 psi" on printed A-5, kept as
   ".4 [?]" because Table 2-3 and the other soils say 4 psi.
3. **Claude was right** on "tend to from iron hydroxides" on printed A-18 (Codex normalized it to
   "form"), the space in "230° F" on printed A-5, and underline remnants Codex typed as underscores.
4. **Numbered specification items stay list paragraphs**, not section headings: Codex wrote "5.
   Chemical Analysis:" as a heading with `sections: [5]`, which would repeat sections 1 to 14 on
   every soil. `tools/build_indexes.py` lists each sheet by its title instead ("SPECIFICATION FOR
   SOIL NO. n", section `A/soil n`).
5. The footer of PDF 23 prints a mark like an equals sign in "A=22"; the header keeps the page
   label A-22.

## Findings about the tool

`tools/diff_pages.py` compared header lists literally, so `[A]` and `["A"]` differed (the Codex
prompt asked for unquoted header values). Lists are now compared item by item without quotes and
written in one form; the only effect on earlier canonical pages is the `transcribers` line, now
`["claude", "codex"]` everywhere.

## Things worth carrying to the data

The soil No. 2 chemical table prints 11.0% for sodium oxide, potassium oxide and moisture alike,
under the line "Alkalies not tested for:"; the three values cannot all be right and the record
should say so. The friction angles stated in the text (41°, 43°, 43.9°) and the modulus values
(5500, 4500, 8600 psi at 4 psi confinement) match Table 2-3 of Volume I except soil No. 1, where
Table 2-3 gives 40°.

## Suggested audit sample (not yet recorded in `qa/audits.csv`)

The three chemical tables against the scan; the ".4 psi" on printed A-5; the 11.0% values on A-10.

## Corrections (2026-10-08, from the batch 2 review)

1. Decision 3 above was wrong on "230° F". Measured in batch 2, the gap after the degree sign is
   the width of the glyph, not a typed space. Decision `p0006-d2` now takes Codex's "230°F", and
   PDF 6 was regenerated. Credit Codex.
2. The friction angle of soil No. 3 does not match Table 2-3 either: the text gives about 43.9°,
   the table 44.5°. The list of disagreements with Table 2-3 is in
   `qa/pages-vol2-ab-b2/review.md`.
3. The density and grain size chart pages (PDF 7, 8, 14, 15, 22, 23) are now written from Codex's
   reading, which follows rule 9 (end labels and the classification strip as body text). See
   `qa/pages-vol2-ab-b3/review.md`, decision 4. Credit Codex.
