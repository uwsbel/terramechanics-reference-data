# Validation of the off-ink check, D-031 v1 (2026-10-28)

`tools/check_trace_ink.py` (params b86a839e2446) classifies every trace sample of both readings as
eligible, excluded or review (CURVE-READING.md rule 7). It was developed on the 48 off-ink points of
`qa/adjudication-2026-10-27` (45 caught there, after tuning; not a test), then frozen, run on all 15
curve batches (14,856 trace samples: eligible 13,575, excluded 980, review 301) and validated here on a
stratified random sample of 400 samples outside the development set (`scripts/make_ink_validation.py`),
each answered blind by a Claude adjudicator (four subagents) and a Codex adjudicator (gpt-6.1-sol, high).
Truth is their agreement: both `yes`, both `no`; otherwise unsettled (69 of 400).

| stratum (population) | sampled | on the line | off | unsettled |
|---|---|---|---|---|
| excluded (920) | 120 | 2 | 106 | 12 |
| eligible within 20 px of a symbol (1,529) | 150 | 114 | 7 | 29 |
| eligible elsewhere (11,994) | 80 | 68 | 3 | 9 |
| review (296) | 50 | 10 | 21 | 19 |

- Exclusions: 106 of 108 settled are right (98 percent); 2 false exclusions, both line ink about 4 px
  before a symbol whose fitted template is slightly too large (a filled circle, a triangle's corner).
- Misses: 7 of 121 settled near symbols, 3 of 71 elsewhere. Weighted to the population: about 1,700
  off-ink samples, 903 caught (53 percent recall), about 17 good samples excluded. The recall estimate
  rests on 3 misses in the 12,000-sample stratum and is very uncertain.
- The 10 misses are two families: a curve ending at the frame or a grid line (convention 5, not
  implemented: 006, 022, 055, 211, 234, 350) and symbol junctions where the outline piece fused with the
  line or a speck in the gap counts as line ink (078, 087, 188, 238).
- Against the acceptance Codex proposed (all failures caught, no false exclusion, 95 percent recall),
  v1 fails. It is precise, not complete.

Adjudicators' shared ambiguities, for a v2 brief: the 2 px tolerance against ink shared with a symbol
(all four Claude adjudicators let the symbol rule win); filled symbols a line runs through (treated as
symbol ink); "upper" and "lower" on inverted density axes (page position used); merged grain-size bands
(cannot tell); pixel-center against edge distance near 2 px.

Process notes: Codex's run loaded a Windows font for its own review sheets (no evidence from outside the
packet); the Claude adjudicators shared one scratch folder, and one saw another's page overview with item
numbers of another range (no answers). Separate scratch folders per adjudicator next time.

## Dry run of applying v1 (reverted)

`tools/reconcile_curves.py <batch> --ink-checks` on all batches, then restored: the excluded samples leave
both readings; where a canonical sample goes, the other reading's samples in the break (eligible by the
same check) enter as one-sided: 615 new one-sided trace points (pilot 132, appc-b1 370, appa-b2 71, the
rest few), one-sided overall from about 160 to about 775. 40 hand decisions are overridden by the rule and
listed in the diff reports.
