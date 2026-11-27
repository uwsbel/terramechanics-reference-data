# Review of batch pages-vol2-ab-b5: Volume II PDF 98 to 114 (end of Appendix A, Appendix B)

Date: 2026-10-08. Reviewer: Claude (page re-reads and glyph measurements on the scan). No human
audit yet.

## What was transcribed

The last page of soil No. 12 (printed A-97/A-98) and Appendix B: a one-paragraph note that the
sonic modulus work was subcontracted to the IIT Research Institute, followed by the IITRI final
report M6175 (J. D. Nelson, January 1967): cover, title page, foreword, table of contents, three
pages of text with equations (1) to (3), two apparatus photographs and six charts (E against
confining pressure for RS, PS, SS, RC and LSM, and the Poisson factor f(ν)). Codex (gpt-6-astra,
high) and Claude worked blind from the same images.

Hints available to each agent: Claude's helpers carried the forms settled in the reviews of
batches 1 to 4. Codex's prompt predates those reviews. Neither agent saw the other's reading of
these pages.

## Diff results (`diff.md`)

| result | pages |
|---|---|
| agreed | 7 |
| resolved | 10 |
| pending | 0 |

Every printed number agreed: report and purchase order numbers, dates, the footnote citation
(Selig and Vey 1965, Vol. 91, SM3, Paper 4332, pp. 19-49), the equation numbers, and the relative
densities on the charts (RS 0.99 and 0.30, PS 0.86 and 0.22, SS 0.84 and 0.26, RC 0.82 and 0.02,
LSM 1.04, 0.995 and 0.77).

## Decisions (`decisions.csv`)

1. **Codex was right** on six points:
   - "IIT RESEARCH INSTITUTE" at the foot of each IITRI page is the report's running footer, and
     rule 1 omits footers. Claude kept it on five pages.
   - Claude wrote "[signature]" for the two handwritten signatures on the foreword. That is
     invented text, and rule 10 ignores handwriting.
   - "South, Bend, Indiana" has a misprinted comma and takes `[sic]`. Claude missed it.
   - FOREWORD, TABLE OF CONTENTS and the report title at the start of the body are headings.
   - The second letter of "scils" on the Appendix B note is an open c shape on a page where many
     letters are broken ("dctermination", "complcte"). Codex's `[?]` fits a damaged o better than
     Claude's `[sic]`, which claims a misprint.
   - The Figure 7 legend marker is a square with one falling diagonal (⧅), not Claude's ⊠. The
     figure diff does not compare legend symbols, so this was found by eye. A page decision
     corrects it.
2. **Claude was right** on the dot after "Special" on PDF 98 (6 x 5 px, a speck) and on the mark
   between "modulus" and "of" on PDF 99 (a baseline underline remnant).
3. **Forms kept from the corpus:**
   - Display equations write Greek as LaTeX macros (`\rho`, `\nu`), as every Volume I display
     equation does.
   - The superscript in "E=ρc²" uses the Unicode sign, as units like "kips/in.²" do throughout.
   - Footnote markers sit against the text with no space.
   - The report title on the cover and title page is part of the title block, not a heading.
4. **Pages with no printed number** (PDF 99 to 101) have `printed_page` empty. Codex wrote
   `unknown`, but the absence is known. The page map's "i" for PDF 101 came from OCR of the
   page top. The rule is now in `docs/PAGE-TRANSCRIPTION.md`.

## Findings about the tools

`tools/build_indexes.py` gave the IITRI sections A to D an empty section id, and would have
confused them with appendix letters. A lettered heading inside an appendix is now `B/A` to `B/D`.
The where-list on printed 2 ("E is the initial tangent modulus") is a sentence form the symbol
index missed; it now gives three rows. Volume I indexes are unchanged by both fixes.

## Things worth carrying to the data (feeds roadmap steps 3b and 3d)

1. **The Table 2-3 modulus is a small-strain wave modulus.** IITRI writes that static triaxial
   values "will generally differ by an order of magnitude" and dynamic stress-strain values "by
   as much as a factor of 4" (printed 1). The wave peaked below 2 psi (printed 2).
2. **Table 2-3 looks interpolated in Dr from the IITRI curves.** IITRI measured RS only at Dr
   0.30 and 0.99. By Claude's eye reading at 4 psi, a straight line in Dr through the two curves
   gives 5.6, 8.7 and 11.2 kips/in.² at Dr 0, 0.45 and 0.80. Table 2-3 gives 5,500, 8,600 and
   10,900 psi. To be confirmed when the curves are read in step 3b.
3. **Two print slips matter for curve reading.** Figure 3's y tick between 9 and 7 is printed
   "3" where 8 belongs. Figure 5's dense label prints "o.84" with a lowercase o. Both are kept as
   printed and described on the pages.
4. **Figure 7 includes an LSM specimen at Dr = 1.04**, above the maximum-density test.

## Suggested audit sample (not yet recorded in `qa/audits.csv`)

The "3" tick on printed 6; the Figure 7 legend marker; the "scils" on the Appendix B note; one
footer omission.

## Addendum: header decisions were not applied (found after this batch, 2026-10-08)

`tools/diff_pages.py` built each canonical header from one reading and ignored header decisions
that chose the other one. Two pages carried a wrong header as a result: PDF 115 (Appendix C
title) had `sections: []` although decision `p0115-h0` chose Codex's `["C"]`, and PDF 23 had
`printed_page: "A=22"` although decision `p0023-h0` chose "A-22" (the batch 3 page decision to
write PDF 23 from Codex's reading brought Codex's header with it). The tool now applies header
decisions. Every batch was regenerated into a scratch folder: those two pages changed and no
other page did. Both are corrected in `corpus/1968-vol2/pages`.
