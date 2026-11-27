# Review of batch curves-s2-b3: Section II load-penetration records (rate series and bin sizes)

Figs. 2-42 and 2-44 (Volume I, printed 2-77 and 2-79; PDF 102 and 104): load against penetration for
the four-inch cylinder in dense RS, both printed upright. Fig. 2-42 holds the rate series, LPT 22, 23,
24 and 25 (curves A to D: dotted, solid, long dashes of about 110 px, shorter dashes of about 46 px).
Fig. 2-44 holds the bin-size series, LPT 24 and 73 (18 by 36 in), 74 (36 by 36 in), 69 and 64A (54 by
36 in). LPT 24 is printed on both figures.

## Readings

Both agents, blind, from the evidence packet written by `tools/make_reading_packet.py`
(`qa/curves-s2-b3/batch.json`), 2026-11-05. Codex: gpt-6.1-sol high, one run (944 s). Claude: one
subagent per figure (claude-opus-5-5), launched at the same time as the Codex run, before any Codex
output existed. **Hints available:** the orchestrating session read the Codex run's final summary while
the Claude readers were still working and passed nothing to them; the Claude reader of Fig. 2-42 was
told that the A/C identification matters because LPT 24 is the calibration test of a later simulation
study; both agents received the batch description, which named the dash lengths of Fig. 2-42 the wrong
way round (it called D the long dashes). Claude's notes describe the page (C long, D shorter); Codex's
notes keep the description's names. The series identities of the two readings agree
(`extractions/claude/curves-s2-b3/meta.json`, `extractions/codex/curves-s2-b3/F2-42/notes.md`).

## Calibration

The two maps agree closely on both figures: the largest difference along every verified line and
interval midline is 1.13 lb on Fig. 2-42 (tolerance 1.27 lb), where 2 of the 274 places lie beyond the
two maps' combined line errors, and 0.81 lb on Fig. 2-44 (tolerance 3.78 lb), with none beyond. Claude's
reading is canonical on both (the same lines, as close to the ink).

## Agreement and adjudication

First comparison: on Fig. 2-42, 66 of 74 matched points agreed, with 39 held by one reading only; on
Fig. 2-44, all 151 matched points agreed, with 13 held by Codex only. The off-ink check (D-031)
excluded nothing. Blind adjudication in `qa/adjudication-2026-11-07/`, two rounds.

Round 1 had 48 items. As first applied, it settled 41 and split 7, but the tool misread answers of
`some` (part of a run on the line, part off): it took every pixel named in the comment as off, including
the samples the comment called on the line. Codex found the defect when it reviewed this batch. With the
comments transcribed sample by sample (Claude and Codex independently, no disagreement) and the
decisions corrected (D-039), round 1 settles 40 items and leaves 8 with split samples. Round 2 was built
from round 1 as first applied: its 7 splits and 5 items (7 samples) left without a partner by round 1
exclusions; 6 items settled and 6 split, and one more sample was settled by the same correction.

Of the 4 pair items settled by naming a reading, 3 went to Claude's (the starts of LPT 23 and 25 and one
trace sample of LPT 25 near the origin) and 1 to Codex's (the knee of LPT 25 near 0.9 in, 997 lb, by the
tool's rule that `both` from one adjudicator is compatible with a named reading from the other); one
pair was settled as both, and one (the start of LPT 22) as neither.

**Where the Fig. 2-42 curves start.** All four curves rise next to the zero-penetration frame line in
one bundle. Codex placed the first point of every curve at the origin corner; both adjudicators found
those points inside the frame, beyond any ink that can be told apart from it, and excluded them
(convention 2). Telling the bundle apart by line style (dot pitch, dash length), the first
distinguishable ink of each curve is:

| Test | First distinguishable ink | Basis |
|---|---|---|
| LPT 22 (A, dotted) | about 30 lb, last dot in the dot rhythm near (850, 3304) px | neither reading's first point; both adjudicators placed it there. The record starts at its first trace sample, 0.03 in and 53 lb |
| LPT 23 (B, solid) | 0.05 in, 146 lb | the solid line stops there with white paper below (both adjudicators) |
| LPT 24 (C, long dashes) | 0.05 in, 2.5 lb | agreed by both readings; the point lies on the bottom frame line |
| LPT 25 (D, shorter dashes) | 0.02 in, 79 lb | its last dash outside the frame (both adjudicators) |

Only LPT 24 can be followed down to the zero-load line. Where the others begin below their first
distinguishable ink, the page does not show; these are starts of visible ink, not of the tests.

**Where the Fig. 2-44 curves start.** Below about 150 to 200 lb, Fig. 2-44 does not show separately
identifiable continuations of its five curves toward the origin: the lowest pieces merge with each other
and with the frame, and some dashed pieces end in white paper to the right of the frame (the lowest
LPT 24 dash ends near (776, 3130) px, about 2.3 mm right of the zero-penetration line at about 160 lb).
Whether the curves were drawn down the frame line or stop short of it, the page cannot say. The
adjudicators did not agree on assigning the first samples inside the merged band (LPT 24, 73, 74); they
stay one-sided.

**The two printings of LPT 24.** Interpolated along the canonical points of each printing:

| Penetration (in) | Fig. 2-42 (lb) | Fig. 2-44 (lb) | Difference (lb) |
|---|---|---|---|
| 0.1 | 118 | 222 | 104 |
| 0.2 | 346 | 393 | 47 |
| 0.3 | 519 | 545 | 25 |
| 0.5 | 745 | 755 | 11 |
| 1.0 | 898 | 906 | 7 |
| 1.5 | 856 | 860 | 4 |
| 2.0 | 990 | 976 | -14 |
| 2.5 | 1161 | 1133 | -28 |

At equal load on the initial rise, the Fig. 2-44 printing sits 0.2 to 1.3 mm to the left of the Fig.
2-42 printing (about 0.5 mm between 300 and 500 lb; 1.3 mm at 200 lb, 0.2 mm at 700 lb, 1.2 mm at
800 lb). The large load differences below 0.3 in come from this small horizontal mismatch along a steep
rise; it varies with load, so it is not a single shift of the penetration zero, and the later loads
agree too closely for a constant load offset of 150 lb or so. At 0.3 in the printings differ by
4.9 percent; from 0.5 in on, by at most 3.2 percent (at 0.55 in), and by 0.5 to 2.4 percent at the
tabulated penetrations. Which printing has
the right penetration zero, and why the low-load parts differ, the figures do not show.

What stays open (mandatory rows of the student audit), 10 points: the knee of LPT 23 near 0.8 to 0.9
in (the readers marked two different bends); the knee of LPT 24 near 1.5 to 1.7 in (one reader marked
the trough minimum, the other a point on the straight recovery beyond the bend); Codex's LPT 25 trace
sample at 1.8 in where D crosses B; Codex's LPT 22 sample at 2.5 in where the last A dot merges with a C
dash (one adjudicator on, one off) and Claude's LPT 22 sample at 2.3 in, which lost its counterpart
there; the first samples of LPT 24, 73 and 74 on Fig. 2-44 inside the merged band (5 points).

Final canonical points: 262 (209 agreed, 38 one-sided-verified, 5 resolved, 8 one-sided, 2 pending
review).

## Records

`tools/build_batch_records.py curves-s2-b3`: seven records, `b68-lpt-022`, `-023`, `-024`, `-025`
(Fig. 2-42), `-073`, `-069`, `-064a` (Fig. 2-44). LPT 24 on Fig. 2-44 is its second printing (the
record takes Fig. 2-42) and LPT 74 on Fig. 2-44 is its second printing (the record takes Fig. 2-33,
batch curves-s2-b1): both rows are left out of `series-map.csv`, so their points stay in
`canonical.csv` as cross-checks and enter no record.

## Suggested audit sample

The 10 open points above; every Fig. 2-44 point below 200 lb, including the agreed first points of
LPT 64A and 69, which both readers placed at the same spot in the merged band; the Fig. 2-42 samples
below 0.1 in, where the bundle was separated by line style; the crossings of A with C and of B with D.
