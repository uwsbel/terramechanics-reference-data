# Blind transcription of report pages, batch pages-vol2-ab-b1 (PDF 2 to 24)

You are one of two independent transcribers of pages from a 1968 NASA report (Bendix, LM Soil
Mechanics Study, Final Report AM-68-1, Vol. II, NASA CR-92215). These pages are Appendix A, the specifications of the test soils: per soil, a chemical analysis table, a photomicrograph, a grain size curve with an inset table, a minimum-maximum density chart and a friction angle chart, repeated under each soil of a material. The other transcriber works
elsewhere; do not look for or use any other transcription, OCR text or summary of these pages.
Work only from the page images in this workspace and the protocol they come with. Your files will
be compared word by word and number by number with the other transcription; differences are
settled from the page image, with credit to whichever reading was right, so type exactly what is
printed and mark what you cannot read.

## Evidence packet (folder `packet/`)

1. 23 page images `pNNNN.png` (PDF 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24), rendered at 300 dpi from a 200 dpi bilevel scan,
   unrotated, each with a `.json` sidecar. Some tables and figures are printed rotated: transcribe
   them upright and record `rotation` in the header (90 when the page must be turned a quarter
   turn clockwise to read).
2. `page-map-rows.csv`: the page-map rows (`pdf_page`, `printed_label`, `inferred_label`). The
   number printed on the page wins; say so in your notes when it differs from the map.
3. `figures-rows.csv`: the agreed figures index rows for these pages (ids `FA-n`, `FB-n`, table
   locators `TA-pNNN`, title as printed, printed page, PDF page). Use these ids in the header lists
   and in figure blocks. What you transcribe is what is printed.
4. `PAGE-TRANSCRIPTION.md`: the protocol. Section 2 is the header, section 3 the body rules: rule 3
   (paragraphs, line-end hyphens, continuation markers), rule 4 (numbers, units and symbols as
   printed; math between single dollars with Unicode inside, multi-letter subscripts in braces),
   rule 5 (display equations), rule 7 (footnotes), rule 8 (tables as Markdown tables, every cell),
   rule 9 (figure blocks: exact layout; headings and annotations outside the plot frame are body
   text; no curve values ever), rule 10 (scan artifacts; odd typewriter marks transcribed as they
   stand, never normalized; `[?]` for doubt, `[illegible]` for what cannot be read).

Source id for the header: `bendix-1968-vol2`. Image paths in the header:
`corpus/1968-vol2/images/pNNNN.png`. Set `transcriber: codex` and `review_status: single-reading`.
Write header values without quotes except `printed_page`, which is quoted.

## Tools

Python with Pillow and NumPy: `<local path>`. Crop, enlarge and rotate for reading as needed; write
crops under `out/`. In tables of this scan the digits 3, 5, 6 and 8 can look alike: enlarge every
number you are not sure of, and mark it `[?]` if the enlargement does not settle it. Read the pages
yourself; no OCR engine, no model-based text recognizer, no network.

## What to produce (write everything under `out/`)

1. One file per page, `out/pNNNN.md` for each image in the packet, in the protocol's format,
   complete: every printed word, heading, table cell, footnote, caption, axis label and legend;
   nothing paraphrased, nothing summarized, nothing added. A table's numbers are transcribed in
   full; a plot's curves are never read. A blank or separator page gets a file with an empty body.
2. `out/notes.md`: hesitations (word, number, symbol; where; what you decided and why), every `[?]`,
   `[illegible]` and `[sic]`, pages whose printed number differs from the page map, and anything in
   the protocol that did not fit these pages.

Definition of done: 23 page files, each read through against its image, and `notes.md`. Finish
with a short summary message naming the files.
