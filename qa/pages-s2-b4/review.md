# Review of batches pages-s2-b3 and pages-s2-b4 (copy kept with batch 4): Volume I Section II, PDF 71 to 116

Date: 2026-10-08. Reviewer: Claude (page re-reads of the blocking differences; Codex's crops used
where it had enlarged a mark). No human audit yet. This review covers both batches; batch 4's
decisions are in `qa/pages-s2-b4/decisions.csv`.

## What was transcribed

Batch 3 (PDF 71 to 93, printed 2-46 to 2-68, without 2-47 and 2-56 from the pilot): the friction
angle relation and the apparent cohesion discussion, the load-penetration apparatus and procedure,
the bearing capacity equation (3-1 to 3-3) and its comparison with the LPT (Figures 2-29 to 2-35,
each with the bearing capacity arithmetic printed beside the plot). Batch 4 (PDF 94 to 116, without
2-90): pressure parameter against relative depth for RS, SS and PS (Figures 2-36 to 2-39), rate and
bin size effects (2-40 to 2-44), footpad against cylinder (2-45 to 2-51), the DPT correlation and
the soil bed control tests (2-52, 2-53).

## Diff results

| batch | agreed | resolved | pending |
|---|---|---|---|
| pages-s2-b3 (21 pages) | 14 | 7 | 0 |
| pages-s2-b4 (22 pages) | 13 | 9 | 0 |

Every number agreed: the bearing capacity computations on Figures 2-32 to 2-35 (slopes, N_q,
N_γ, the friction angles 38.5° to 55°), the LPT numbers and DPT values in the legends, the
footnote values (52.6°, 51°), the density scoop volume. The blocking differences were notation
(equations in LaTeX macros or Unicode, unit exponents as math or superscripts), printed marks, and
figure labels.

## Decisions

1. **Codex was right** on printed marks Claude normalized: "517=520" in a page reference (2-59),
   "compare-quite" (2-66), "LPT curve 5." (2-74, probably "curves" badly set), the spaced dashes
   in the lettered parts list of Figure 2-30 (rule 11), the illegible second digit of the
   Figure 2-47 number (2-83), and the bin-size labels of Figure 2-37 as body text (rule 9).
2. **Claude was right** on the extra tick label 627 printed on the load axes of Figures 2-41 to
   2-43 (left out by Codex), "Bin Size : 18" with its printed space, and a speck after "thus"
   (2-80).
3. Codex typed `$D_r ? 0.69$` for one approximately sign on Figure 2-37; fixed by a recorded
   substitution in the canonical page.

## Findings about the tool

`tools/diff_pages.py` compared header values literally, so Codex's quoted YAML in batch 4
(`source: "bendix-1968-vol1"`) made every header differ. Header values are now compared without
their quotes, and the canonical header is written in one form (scalars unquoted, `printed_page`
quoted). All earlier canonical pages regenerate byte for byte.

## Things worth carrying to the data

The bearing capacity arithmetic printed on Figures 2-32 to 2-35 (A, γ, N_q, N_γ and the
resulting friction angles) is a ready-made cross-check for the LPT records in step 3c, and
Figure 2-37's bin sizes (18, 54 and 108 by 36 inches) belong in the setup of those tests.

## Suggested audit sample (not yet recorded in `qa/audits.csv`)

The arithmetic blocks of Figures 2-33 and 2-35 read in full against the scans; the "517=520" and
"curve 5" marks.
