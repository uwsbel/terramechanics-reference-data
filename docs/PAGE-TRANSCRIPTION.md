# Page transcription protocol

How a page of a report becomes `corpus/<source>/pages/pNNNN.md`: one Markdown file per PDF page,
typed from the 300 dpi page image, by two agents independently, compared by
`tools/diff_pages.py`, and settled by a page re-read. The page files are the text an agent
searches when asked a question about the reports; the indexes (`contents.csv`, `symbols.csv`,
`equations.csv`, `glossary.csv`) are built from them. Numbers from figures never go in a page file;
they are read under `docs/CURVE-READING.md`.

## 1. Inputs

The page image `corpus/<source>/images/pNNNN.png` (300 dpi, unrotated, from
`tools/render_pages.py`), the page-map row (`corpus/<source>/page-map.csv`: PDF page, printed
label), and this protocol. Nothing else: not the OCR layer of the PDF (unusable for numbers), not
another agent's notes.

## 2. The file

```
---
source: bendix-1968-vol1
pdf_page: 65
printed_page: "2-40"
sections: ["2.5.2.3"]
figures: []
tables: []
equations: ["3-1"]
rotation: 0
image: corpus/1968/images/p0065.png
transcriber: claude
review_status: single-reading
---
<body>
```

Header fields: `sections` lists the section numbers whose headings are printed on the page;
`figures` and `tables` list the ids of figures and tables printed on the page (a caption is on
the page), not merely mentioned in the text; `equations` lists the printed equation numbers;
`printed_page` is the number printed on the page, and empty (`""`) when none is printed (a cover or title page). `rotation` is 0, 90, 180 or 270 as the page was scanned (the text of a rotated page is
transcribed upright, and the image path still points at the unrotated scan). `review_status` is
`single-reading` in a submission; the diff sets `agreed`, `resolved` or `pending` on the
canonical copy.

## 3. The body

1. **Everything printed, in reading order**: running text, headings, lists, tables, captions,
   footnotes, equation numbers. The printed page number is in the header and not repeated in
   the body. Headers and footers of the report (none in AM-68-1) would be omitted.
2. **Headings** become Markdown headings with the printed number and title verbatim:
   `### 2.5.2.3 Direct Shear Test`. Depth follows the numbering (two parts `2.5` is `#`, three
   `2.5.2` is `##`, four or more `###`). (The example once said `##`; Codex caught the
   contradiction in the pilot.)
3. **Paragraphs** are joined into one line each; line breaks inside a paragraph are not kept.
   A word hyphenated at a line end is joined (`Read-` / `ings` becomes `Readings`); a hyphen
   that is part of the word stays (`2-1/2-inch`, `load-penetration`, `x-y`). A paragraph that
   continues from the previous page starts with `[cont.]`; one that runs onto the next page ends
   with `[cont. next page]`.
4. **Numbers, units and symbols exactly as printed**: `0.50 to 0.57`, `11.76 ± 0.14 g's`,
   `230°F`, `18"` (the inch mark as printed), `2-3/4 inches`, `1.59 lbs`. Unicode for `±`, `°`,
   `≤`, `≈`. A symbol with a subscript, alone or in a relation, is written as math between single
   dollars with Unicode inside: `$D_r$`, `$G_p$`, `$σ_n$`, `$φ_{DS}$` (a subscript of more than one
   letter in braces), `$0 ≤ D_r ≤ 0.3$`, `$D_r ≈ 0$`. No LaTeX
   macros inside (`\le`, `\sigma`): the files are searched as text, and `D_r` must be found by
   a search for `D_r`; the dollars make the rendered page show real subscripts. The canonical
   build wraps a bare `D_r` in dollars if a transcriber forgot (decided with Dan 2026-10-08,
   after the pilot had the two transcribers split on this).
5. **Display equations** are their own paragraph in LaTeX between `$$`, followed on the same
   line by the printed number in parentheses: `$$S = C + \sigma_n 	an \phi$$ (3-1)`. Display
   equations may use LaTeX macros; their text is also indexed in `equations.csv`.
6. **Lists** keep the printed labels: `A. Soil Container - A wooden box ...`, one item per
   paragraph, indented continuation lines joined. A label printed twice or out of order is
   transcribed as printed with `[sic]` after it.
7. **Footnotes** go at the end of the body under a line `Footnotes:`, each starting with its
   printed marker (`*`, `**`) and the text verbatim. The marker stays in the running text where
   it is printed (`2-20*`, `tests**`).
8. **Tables** are Markdown tables, cells verbatim, the printed title above as `Table 2-3 ...`.
   A rotated table is transcribed upright.
9. **Figures on the page** get a block, values never. Text printed on the page outside the plot
   frame (a soil heading, "Same Notation As Above", "Rebound", angle labels on envelope lines,
   construction-line labels) is body text in reading order, before or after the block as
   printed; the block holds only the caption, the axis labels, the legend and one sentence of
   description:

   ```
   RS Soil

   $γ$ = 46.7 to 47.4 Lb./Ft.³ ($D_r$ = .5 to .57)

   ::: figure FC-1B
   caption: Figure C-1B. Direct Shear Test Data - Shear Stress vs. Shear Displacement Dilation Displacement vs. Shear Displacement
   axes: x $δ_τ$ x 10^3 (in.); y $τ$ (PSF); y2 $δ_σ$ x 10^3 (in.)
   legend: σ (PSF), γ (PCF); × 3520, 46.7; * 2935, 46.8; □ 2345, 46.7; + 1760, 46.7; ▽ 1172, 46.8; △ 587, 47.2; ○ 294, 47.4
   description: Two panels showing shear stress and dilation displacement against shear displacement, with 7 test series in each panel.
   :::

   Same Notation As Above
   ```

   `caption` is the printed caption verbatim (lines joined). `axes` lists each axis as `x`, `y`,
   `y2` with its printed label and unit, no tick ranges. `legend` lists the column heads as
   printed, then one entry per series as `symbol value, value` in printed order; a legend
   without symbols lists the values alone. The `description` is one sentence and is not compared
   between transcribers. The unnumbered title of an appendix is a heading and its letter goes in
   `sections` (`["C"]`). (Layout fixed 2026-10-08 after the first Appendix C batch, where one
   transcriber folded headings and tick ranges into the block; Codex's layout was adopted.)
   Labels printed beside an axis with leader lines (the end values of the Appendix A density
   charts) and a classification strip printed below the frame are body text too; `legend` is
   for series keys only, and `legend: none` when none is printed. The figure-page diff compares
   numbers and captions, not layout, so a reviewer checks the layout by eye (the Appendix A
   batch 3 review moved 18 chart pages to this form).
10. **Scan artifacts are not text**: underlines, strike-through marks, marginal pencil marks
    and bleed-through are ignored. A word that cannot be read is `[illegible]`; a word read with
    doubt gets `[?]` after it; a visible misprint is transcribed as printed with `[sic]`. An odd
    typewriter mark (a hyphen where none is expected, an equals sign for a hyphen) is enlarged
    and transcribed as it stands, never normalized to the expected form; the pilot's only two
    reading differences were normalizations of this kind. The same holds for typewriter digits
    standing for letters in chemical formulas ("Ca0", "A1203" printed with the digits zero and
    one): measure the glyph against a known letter on the same line and keep what is printed.
    Numbered items of a specification sheet ("5. Chemical Analysis:") are list paragraphs, not
    section headings.
11. **Quotation marks** are straight (`"`), apostrophes straight (`'`), and no em- or en-dashes
    are introduced: a printed dash between words is a spaced hyphen (` - `), a printed range
    keeps its hyphen (`354-356`).

## 4. Comparing two transcriptions (`tools/diff_pages.py`)

1. Header fields are compared one by one; any difference is reported.
2. Bodies are tokenized on whitespace after normalization (straight quotes, `[?]` removed,
   `[cont.]` markers removed, multiple spaces collapsed) and aligned with a sequence matcher.
   Every differing run is one difference with an id `pNNNN-dK`, classified as `markup` (the
   same words with and without `$` delimiters), `number` (either side contains a digit),
   `reference` (a figure, table, section, equation or citation reference), `symbol` (Greek
   letters, subscripts, math), or `wording` (anything else).
3. `number`, `reference` and `symbol` differences block the page (`pending`) until settled.
   `wording` and `markup` differences are listed but do not block: the canonical copy keeps reading A's words
   unless a decision says otherwise. A page with no difference is `agreed`.
4. Decisions (`qa/<batch>/decisions.csv`: `page, diff_id, use, note`, `use` in `a | b | text`;
   on a figure page a row `<page>,<page>-canonical,a|b` picks the reading the page is written
   from, and `replace: OLD => NEW` in its note records a substitution for a cell neither reading
   has right)
   settle differences after a page re-read; with `text`, the note's `text=` value is used. The
   tool applies them and writes the canonical page with `review_status` `agreed` (no
   differences), `resolved` (all differences decided) or `pending`. Credit goes to whichever
   reading was right, in the batch review.
5. The canonical page carries both transcribers in the header (`transcribers: [claude, codex]`)
   and the batch; the two submissions stay under `extractions/`.

## 5. What goes into `corpus/`

`corpus/<source>/pages/pNNNN.md` is the canonical page. A `pending` page is quoted with that
caveat (`AGENTS.md`, rule 2). The indexes are rebuilt from the pages by `tools/build_indexes.py`
(to be written in step 2d of the roadmap).
