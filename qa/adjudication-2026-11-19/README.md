# Blind adjudication of 2026-11-19

Curve batch `curves-s4-b1` (Figs. 4-19 and 4-20, the vertical footpad impact runs 4, 10 and 12; review
`qa/curves-s4-b1/review.md`). Each round: the brief, the items (`items.csv`: each item's question and the
pixels and values of the marks drawn; built by `scripts/make_disputes5.py` with `ADJ_SEED` 20261119 for round 1 and
20261120 for round 2 and `ADJ_FEATURE_ROLES=leading`; the crops are not kept), the answers of a Claude adjudicator (one subagent, claude-opus-5-5) and a Codex
adjudicator (gpt-6.2-sol high, workspace-write in its own copy of the packet), the key that maps the neutral labels
P and Q to the readers (kept out of the packets until the round was applied), the splits and the Codex run's meta.
Each adjudicator worked in its own copy of the packet outside the repository and reports opening nothing else.
Answers applied with `qa/adjudication-2026-10-15/scripts/apply_adjudication4.py`; the decisions are in the batch's
`decisions-*.csv` (round 1 rows first, round 2 rows appended by `qa/adjudication-2026-11-02/scripts/append_decisions.py`).

`items.csv` and `key.csv` are the record of each round: the key names every row an item drew (reader, series, kind,
sequence), whose pixels are in the batch's reading files. Rerunning the builder does not reproduce the rounds: it
reads the batch's current canonical and decision files, in which the rounds' own decisions have since been applied
(Codex's review found that a rerun gives 9 items, not 60 and 15). The crops of round 1 drew the other reader's
nearby samples sorted by pixel rather than in drawing order; on items 057 and 058 (run 4's end hook on Fig. 4-20)
that joined the samples of the hook's two strokes out of order. Both adjudicators answered `both` there (every
sample on the ink), which the drawing order does not change. The builder now draws them in order.

`scripts/make_disputes5.py` is version 4 with two changes (version 4 is left as the earlier rounds used it): the
other reader's samples drawn with a `trace-disagree` item are the nearest on the page (on Fig. 4-20,
printed sideways, the nearest in pixel u had taken samples from the far end of the curve and made the crop span the
page), and feature roles follow `tools/diff_curves.py --feature-roles leading`, as the batch does.

The brief is that of 2026-11-07 with the figure section rewritten for these two figures and convention 5 widened
to the several maxima and minima of a history; round 2 adds the second-round section.

Round 1: 60 items (17 one-sided features, 5 disagreements, 38 runs of trace samples only one reader took); 49
settled (65 decision rows), 11 split. Two of the 65 rows were not applied: Claude's last displacement samples of
runs 12 and 4 (sequences 34 and 44 of F4-19 panel 2) were one-sided when the items were built, and became agreed
when the canonical reading of that panel was changed to Claude's (the top frame Codex anchored as 4.5 in is not
parallel to the grid; `qa/curves-s4-b1/overlays.csv`), so a verification would have lowered their status. The two
exclusions of that panel (Claude's first samples of runs 10 and 4, inside the frame at the corner on both
adjudicators' word) were applied although those samples had become agreed: a judgment of the page outranks an
agreement with the other reading's samples in the same merged ink.

Round 2: the 11 splits and the 4 items left without a partner by round 1's exclusions or by the change of canonical
reading (15 items); 6 settled (9 rows), 9 split. Item 002 (Codex's run 12 samples 62 and 63 on F4-19 panel 1) has a
`some` answer from Claude's adjudicator and `all yes` from Codex's; its comment was not transcribed by two readers
(D-039) for two samples, so it stays split. The split points keep their status and are mandatory rows of the student
audit: chiefly the starts of the three runs inside the merged ink at the origins of both figures, run 12's start on
F4-19 panel 2 (pending review: one adjudicator places it in the bundle near (758, 3268) px, the other cannot tell),
and the late band of F4-19 panel 1 where the three runs cross between 95 and 117 ms.
