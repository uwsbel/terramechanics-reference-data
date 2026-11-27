# Review of batch pages-pilot-b1: five Section II pages transcribed by both agents

Date: 2026-10-08. Reviewer: Claude (page re-reads of both wording differences). No human audit yet.

## What was transcribed

Five text pages of AM-68-1 Vol. I chosen to exercise the protocol: PDF 65 (printed 2-40, the direct
shear procedure, a numbered equation and a footnote), PDF 72 (2-47, friction angle and apparent
cohesion, two footnotes, literature citations), PDF 81 (2-56, the load-penetration apparatus as a
lettered list with dimensions in inch marks and a printing slip), PDF 115 (2-90, the dynamic
penetrometer, symbols with subscripts, a confidence interval), PDF 128 (2-103, placement
procedures, inequalities with Unicode operators, two headings). No figure or table is printed on
these pages.

Evidence packet (source only): the five 300 dpi images with their render sidecars, the page-map rows
and `docs/PAGE-TRANSCRIPTION.md`. Codex (gpt-6-astra, high, workspace-write in a scratch
workspace, 240 s) transcribed first; Claude typed its transcription from the same images while
Codex ran and before opening anything Codex wrote. Neither saw the other's text or any OCR output.

## Diff results (`diff.md`)

| page | differences | class | status |
|---|---|---|---|
| p0065 | 0 | | agreed |
| p0072 | 0 | | agreed |
| p0081 | 2 | wording | resolved (both for Codex) |
| p0115 | 0 | | agreed |
| p0128 | 4 | markup | resolved (protocol clarified) |

About 2,100 words and some 60 numbers, references and symbols in all; no number, reference or
symbol was read differently by the two agents. Header fields agreed on every page, including the
printed page numbers (the page map's `printed_label` of 2-27 for PDF 81 is a body reference, as
Codex noted; the footer reads 2-56 and both used it).

## Decisions (`decisions.csv`)

1. **p0081 item C, "Hydraulic-Cylinder" (Codex) versus "Hydraulic Cylinder" (Claude): Codex.**
   The crop shows a hyphen of the same weight as the one before "Used"; Claude took it for an
   underline artifact. Transcribed as printed.
2. **p0081 item J, "x=y [sic]" (Codex) versus "x-y" (Claude): Codex.** The crop shows two
   strokes, a typewriter equals sign, unlike the single hyphen in the other plotter references.
   Claude normalized it to the expected form, which the protocol forbids.
3. **p0128, the two inequalities in `$...$` (Codex) versus plain text (Claude): Codex.** Not a
   reading difference. Dan ruled for math in dollars so the rendered pages show real subscripts and
   relations; a text search still finds `D_r` inside `$D_r$`. Rule 4 now requires `$...$` with
   Unicode inside and no LaTeX macros, and the canonical build wraps bare symbols a transcriber left
   plain (both transcribers had left `G_p` and `D_r` plain on p0115 and p0128).

## Findings about the protocol and the tool

1. The depth example in rule 2 (`##` for a four-part number) contradicted the depth rule; Codex
   followed the rule and said so. Example corrected.
2. Rule 5 was ambiguous about inline math (decision 3). Rule 4 now settles it: math in dollars,
   Unicode inside.
3. `tools/diff_pages.py` matched `prompt.md` as a page (glob `p*.md`) and reported it as a
   one-sided page; glob narrowed. It also classified a `$`-only difference as `number`; a
   `markup` class was added, non-blocking.
4. Claude's two errors were both normalizations of odd typewriter marks toward the expected
   form. Codex's notes show a better habit: enlarge every odd mark and transcribe what is there.
   Worth a sentence in rule 10, and a reason to keep both transcribers on every page.
5. Time: Codex 4 minutes for five pages; Claude about the same. The diff and the review took
   longer than the transcription. At this rate the 230 remaining pages are a day of agent time
   plus review, below the roadmap's estimate.

## Credit

Codex: both resolved differences, the depth-rule contradiction, the page-map note on PDF 81.
Claude: the markup clarification and the tool fixes. Agreement on everything else is agreement
between two agents, not confirmation; the pages carry `review_status: agreed` or `resolved` and
no human audit.

## Suggested audit sample (not yet recorded in `qa/audits.csv`)

One agreed page re-read in full against the image (p0115, the densest in numbers), plus the two
resolved spots on p0081.
