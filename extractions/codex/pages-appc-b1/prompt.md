# Blind transcription of Appendix C pages, batch pages-appc-b1 (PDF 115 to 137)

You are one of two independent transcribers of pages from a 1968 NASA report (Bendix, LM Soil
Mechanics Study, AM-68-1 Vol. II, NASA CR-92215, Appendix C: the direct shear test program). The
other transcriber works elsewhere; do not look for or use any other transcription, OCR text or
summary of these pages. Work only from the page images in this workspace and the protocol they
come with. Your files will be compared word by word with the other transcription; differences
are settled from the page image, with credit to whichever reading was right.

## Evidence packet (folder `packet/`)

1. `p0115.png` to `p0137.png`: 23 pages rendered at 300 dpi, unrotated (each with a `.json`
   sidecar). PDF 115 is the appendix's text page; the rest are figure pages: failure envelopes,
   data sheets (shear stress and dilation against shear displacement for several normal stresses,
   with a legend table of normal stress and unit weight) and friction-angle charts. Some pages are
   printed rotated; transcribe them upright and record `rotation` in the header.
2. `page-map-rows.csv`: the page-map rows (`pdf_page`, `printed_label`, `inferred_label`); the
   printed page number is the `inferred_label` where `printed_label` is `unknown` or wrong (this
   binding is scrambled in places; the number printed on the page wins, and say so in your notes
   when it differs from the map).
3. `figures-rows.csv`: the agreed figures index of Appendix C (id, title as printed, printed page,
   PDF page, soil, states, panels, curves, axes, units). Use these ids (`FC-1A`, `FC-1B`, ...) in
   the header's `figures` list and in the figure blocks. The index tells you what to expect on a
   page; what you transcribe is what is printed.
4. `PAGE-TRANSCRIPTION.md`: the protocol. Section 2 defines the header, section 3 the body rules
   (rule 9 is the figure block: caption, axes with labels and units verbatim, legend entries
   including the legend table's values as printed, a one-line description; never a curve value).

Source id for the header: `bendix-1968-vol2`. Image paths: `corpus/1968-vol2/images/pNNNN.png`.
Set `transcriber: codex` and `review_status: single-reading`.

## Tools

Python with Pillow and NumPy: `<local path>`. Crop and enlarge
(and rotate for reading) as needed; write crops under `out/`. Read the pages yourself; no OCR
engine, no model-based text recognizer, no network.

## What to produce (write everything under `out/`)

1. `out/p0115.md` to `out/p0137.md`: one file per page in the protocol's format, complete. A
   figure page's body is its figure block(s) plus any text printed outside the figure (title
   lines, notes, "same notation as above", test numbers, dates). The legend table of a data
   sheet (normal stress with unit weight per test) goes in `legend:` as printed, in order.
2. `out/notes.md`: hesitations (word, number, symbol; where; what you decided and why), every
   `[?]`, `[illegible]` and `[sic]`, pages whose printed number differs from the page map, and
   anything in the protocol that did not fit these pages.

Definition of done: 23 page files, each read through against its image, and `notes.md`. Finish
with a short summary message naming the files.
