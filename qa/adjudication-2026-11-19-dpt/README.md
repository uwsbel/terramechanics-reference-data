# Blind adjudication of 2026-11-19 (dynamic penetrometer)

Curve batch `curves-s2-b4` (Fig. 2-54, the three dynamic penetrometer records; review `qa/curves-s2-b4/review.md`). One
round: the brief (that of `qa/adjudication-2026-11-19/` with the figure section rewritten for Fig. 2-54 and
convention 5 for deceleration), the items (`items.csv`, built by `qa/adjudication-2026-11-19/scripts/make_disputes5.py`
with `ADJ_SEED` 20261121 and `ADJ_FEATURE_ROLES=leading`; crops not kept), the answers of a Claude adjudicator (one
subagent, claude-opus-5-5) and a Codex adjudicator (gpt-6.2-sol high, workspace-write in its own copy of the packet),
the key, the splits and the Codex run's meta. `items.csv` and `key.csv` are the record of the round. Answers applied
with `qa/adjudication-2026-10-15/scripts/apply_adjudication4.py`; the decisions are in the batch's `decisions-*.csv`.

12 items, 10 settled (22 decision rows), 2 split: two one-sided knees (one adjudicator places the corner about 9 px
from the mark, just over the 8 px rule; a turn of about 3 degrees the other judges too slight). They stay one-sided
and are mandatory rows of the student audit; no second round for two single points.

Afterwards (Codex's review): the three end samples the adjudicators excluded shared their place, within 0.6 px, with
the other reader's last sample or with both readers' `last` features, which the round did not ask about. Those seven
points were excluded by the same criterion (decision notes in the batch's `decisions-*.csv`). In panel 2, Codex's own
last sample and `last` feature also lie inside the frame line, 3.4 px from the trace's ink (Codex's second review;
3.8 px is their distance from Claude's), and were excluded too: nine points in all.
