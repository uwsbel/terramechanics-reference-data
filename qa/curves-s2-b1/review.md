# Review of batch curves-s2-b1: Section II load-penetration records (cylinders)

Figs. 2-29, 2-32, 2-33, 2-34 (Volume I, printed 2-52, 2-61, 2-62, 2-65; PDF 80, 88, 89, 90): load on a
cylindrical penetrator against its penetration into the soil bed, printed sideways, one panel each.
Recorded traces LPT 27, 52, 53, 93 (RS loose), 74, 75 (RS dense), 87, 88 (SS), and the authors'
straight lines: the fits labelled `Slope = ... lbs./in.` on 2-32 to 2-34 (series `fit`) and the
bearing-capacity line on 2-33 (series `bce`).

## Readings

Both agents, blind, from the evidence packet written by `tools/make_reading_packet.py`
(`qa/curves-s2-b1/batch.json`). Claude: one subagent per figure (claude-fable-5-1), 2026-10-30,
before any Codex reading existed. Codex: gpt-6.1-sol high, the run of 2026-10-31 02:54 (through the
session relay of the Codex runner; three attempts on 2026-10-30 failed before running any command).
A second complete Codex run from the byte-identical prompt and packet was made by mistake on
2026-11-02; it is kept outside the repository as a replicate and plays no part here, a rule fixed
before either run was compared with anything (`extractions/codex/curves-s2-b1/meta.json`).

Both readers gave the printed numbers of the Figure 2-34 load axis (`Load - Lbs. x 100`, 0 to 1200)
and did not multiply, as instructed; the question stays open (`docs/OPEN-QUESTIONS.md`, item 12).

## Calibration

Where both readings hold a verified grid line, the two maps agree within their line errors on every
figure. They part only beyond the last printed label of the penetration axis: the lines there carry no
label (7, 8 and 9 in on 2-34; 10 and 11 in on 2-32). Claude's readers anchored them on their ink with
the values the even spacing gives them; Codex's reading stopped its map at the last labelled line and
flagged the points beyond it as extrapolated. The largest difference is 0.082 in at 9 in on 2-34 and
0.019 in at 11 in on 2-32. By the canonical rule (`docs/CURVE-READING.md`, section 4, step 4) the
reading with more verified lines, as close to the ink, is canonical: Claude's on all four figures.
The records' values beyond the last printed label therefore rest on unlabelled lines valued by the
grid spacing, and their notes say so.

## Agreement and adjudication

First comparison: 249 of 263 matched points agreed (F2-29 37 of 39, F2-32 97 of 98, F2-33 52 of 55,
F2-34 63 of 71); 51 points were held by one reading only. The off-ink check (D-031) excluded nothing
(these figures plot no symbols) and sent 5 samples to review.

Blind adjudication (`qa/adjudication-2026-11-02/`, two rounds, one Claude and one Codex adjudicator per
round, neutral labels, batches s2-b1 and s2-b2 in one packet). Findings on this batch:

1. On 2-34, where LPT 87 runs beside the fit line, two of Codex's LPT 87 samples sat on the fit
   line's ink and one on the printed `LPT No. 87`; both adjudicators chose Claude's samples on the
   trace (round 1, items 056 to 058). The fit line's intercept: both chose Claude's mark at 139 lb,
   beside the printed intercept of 140 lb (item 051), which supports reading this axis in plain pounds
   (`docs/OPEN-QUESTIONS.md`, item 12).
2. The start of LPT 88 (it starts two inches below the surface, on the 2 in grid line) was the hardest
   item: the thin trace cannot be told from the grid line near the frame. Its first point stays split
   after two rounds.
3. An early trace sample of Codex's LPT 27 and LPT 75, and the first sample of the fit lines on 2-32
   and 2-34, sat inside the frame line or on the axis beyond the last visible ink; both adjudicators
   excluded them under the frame rule, and Claude's first samples, left without a partner, were
   verified in round 2.
4. On 2-33 the knees where LPT 74 and LPT 75 meet the fit line are judgment on a junction, not a bend,
   and three of them stay open.

Final canonical points: 300 (246 agreed, 35 one-sided-verified, 9 resolved, 5 one-sided, 5 pending
review). The 10 open points stay in the records with their status and are mandatory rows of the
student audit. With every bound halved, 230 of 262 matched points agree.

## Records

`tools/build_batch_records.py curves-s2-b1`: eight records, `b68-lpt-027`, `-052`, `-053`, `-093`,
`-074`, `-075`, `-087`, `-088` (260 points). `b68-lpt-087` is also printed on Fig. 2-48 (batch
curves-s2-b2); its record takes this figure, the first printing (the convention of
`docs/DATA-ORGANIZATION.md`: the first printing holds the numbers). The 36 points of the `fit` and
`bce` lines are in `canonical.csv` and in no record until the experiment index gains derived-series
records for them (`docs/OPEN-QUESTIONS.md`, item 13).

## Suggested audit sample

The 10 open points, the samples near the crossings of the fit line on 2-33 and 2-34, and the points
beyond the last printed penetration label on 2-32 and 2-34.
