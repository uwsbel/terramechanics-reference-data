# Blind transcription of five report pages, pilot batch pages-pilot-b1

You are one of two independent transcribers of pages from a 1968 NASA report (Bendix, LM Soil
Mechanics Study, AM-68-1 Vol. I, NASA CR-92208). The other transcriber works elsewhere; do not
look for or use any other transcription, OCR text or summary of these pages. Work only from the
page images in this workspace and the protocol they come with. Your files will be compared word
by word with the other transcription; differences are settled from the page image, with credit
to whichever reading was right, so type exactly what is printed and mark what you cannot read.

## Evidence packet (folder `packet/`)

1. `p0065.png`, `p0072.png`, `p0081.png`, `p0115.png`, `p0128.png`: five pages rendered at
   300 dpi, unrotated (each with a `.json` sidecar naming the render settings).
2. `page-map-rows.csv`: the page-map rows of these pages (`pdf_page`, `printed_label`,
   `inferred_label`); the printed page number is the `inferred_label` where `printed_label` is
   `unknown`. Check it against the number printed at the bottom of the page.
3. `PAGE-TRANSCRIPTION.md`: the protocol. Section 2 defines the header, section 3 the body
   rules. Follow it exactly; the comparison tool assumes it.

Source id for the header: `bendix-1968-vol1`. Image paths in the header:
`corpus/1968/images/pNNNN.png`. Set `transcriber: codex` and `review_status: single-reading`.

## Tools

Python with Pillow and NumPy: `<local path>`. Use it to crop
and enlarge parts of a page when a word, a number or a symbol is hard to read (write crops under
`out/`). Read the page yourself; do not run an OCR engine or any model-based text recognizer,
and do not fetch anything from the network.

## What to produce (write everything under `out/`)

1. `out/p0065.md`, `out/p0072.md`, `out/p0081.md`, `out/p0115.md`, `out/p0128.md`: one file per
   page in the protocol's format, complete (every printed word, heading, list label, footnote,
   equation and equation number; nothing paraphrased, nothing summarized, nothing added).
2. `out/notes.md`: the places where you hesitated (word, number, symbol; where on the page; what
   you decided and why), misprints you transcribed with `[sic]`, and anything in the protocol
   that was unclear or did not fit these pages.

Definition of done: the five page files exist, each passes a read-through against its image, and
`notes.md` lists every `[?]`, `[illegible]` and `[sic]` you used. Finish with a short summary
message naming the files.
