# Blind transcription of report pages, batch pages-s2-b2 (PDF 48 to 70)

You are one of two independent transcribers of pages from a 1968 NASA report (Bendix, LM Soil
Mechanics Study, Final Report AM-68-1, Vol. I, NASA CR-92208, Section II: the soil test program).
The other transcriber works elsewhere; do not look for or use any other transcription, OCR text or
summary of these pages. Work only from the page images in this workspace and the protocol they come
with. Your files will be compared word by word with the other transcription; differences are settled
from the page image, with credit to whichever reading was right, so type exactly what is printed and
mark what you cannot read.

## Evidence packet (folder `packet/`)

1. 22 page images `pNNNN.png` (PDF 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68, 69, 70), rendered at 300 dpi, unrotated, each with a
   `.json` sidecar. The pages mix running text, section headings, numbered equations, footnotes,
   tables and full-page figures (photographs, schematics, plots). Some tables and figures are
   printed rotated on the page: transcribe them upright and record `rotation` in the header (90
   when the page must be turned a quarter turn clockwise to read).
2. `page-map-rows.csv`: the page-map rows (`pdf_page`, `printed_label`, `inferred_label`). The
   printed page number is usually the `inferred_label`; the number printed on the page wins, and
   say so in your notes when it differs from the map.
3. `figures-rows.csv`: the agreed figures index rows for figures and tables printed on these pages
   (ids `F2-n`, `T2-n`, title as printed, printed page, PDF page). Use these ids in the header lists
   and in figure blocks. What you transcribe is what is printed.
4. `PAGE-TRANSCRIPTION.md`: the protocol. Section 2 is the header, section 3 the body rules: rule 3
   (paragraphs joined, line-end hyphens joined, `[cont.]` and `[cont. next page]` markers), rule 4
   (numbers, units and symbols as printed; math between single dollars with Unicode inside,
   multi-letter subscripts in braces), rule 5 (display equations in `$$...$$` followed by the
   printed number), rule 7 (footnotes), rule 8 (tables as Markdown tables), rule 9 (figure blocks:
   exact layout; headings and annotations outside the plot frame are body text; no curve values
   ever), rule 10 (scan artifacts; odd typewriter marks transcribed as they stand, never
   normalized).

Source id for the header: `bendix-1968-vol1`. Image paths in the header:
`corpus/1968/images/pNNNN.png`. Set `transcriber: codex` and `review_status: single-reading`.

## Tools

Python with Pillow and NumPy: `<local path>`. Crop, enlarge and rotate for reading as needed; write
crops under `out/`. Read the pages yourself; no OCR engine, no model-based text recognizer, no
network.

## What to produce (write everything under `out/`)

1. One file per page, `out/pNNNN.md` for each image in the packet, in the protocol's format,
   complete: every printed word, heading, list label, footnote, equation and equation number,
   table cell, and figure caption, axis label and legend; nothing paraphrased, nothing summarized,
   nothing added. A table's numbers are transcribed in full; a plot's curves are never read.
2. `out/notes.md`: hesitations (word, number, symbol; where; what you decided and why), every `[?]`,
   `[illegible]` and `[sic]`, pages whose printed number differs from the page map, and anything in
   the protocol that did not fit these pages.

Definition of done: 22 page files, each read through against its image, and `notes.md`. Finish
with a short summary message naming the files.
