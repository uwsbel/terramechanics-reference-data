# Re-derivation of every curve batch under D-025 and D-026

2026-10-14. Batches `curves-pilot-b1` and `curves-appc-b1` to `-b6` (22 figures, 35 panels), whose
values until now came from one affine map per panel and reading. Nothing under `extractions/` was
changed: each reading's pixels are re-derived by `tools/reconcile_curves.py` into
`qa/<batch>/rederived/<reader>/<figure>/` and reconciled again.

## What changed

1. **Values** come from a piecewise map between each reading's verified lines (D-025;
   `tools/calibrate_axes.py`, `docs/CURVE-READING.md` section 2 step 4). The difference from the
   affine values, per canonical series, is in each batch's `calibration-sensitivity.md`: at most 0.7
   thousandths of an inch and 16 psf on the data sheets, initial secant slopes within -3 to +3
   percent.
2. **Every reader's line is checked against the ink of the page.** 22 lines failed, 14 of Claude's and
   8 of Codex's, and were measured again on the page from that reading's own neighbouring lines
   (`calibrate_axes.py recover`, `qa/<batch>/knots.csv`, each straight within 0.7 px). Claude's: five
   in the pilot's calibration (x = 0, x = 50 and y = 4000 of the upper panel, x = 50 and x = 250 of the
   lower; the x = 50 line, found by the grid tool in 10 of 24 bands with the wrong tilt, is 13 px from
   the ink's line at the top of the plot), FC-1C y = 4000, FC-1D y = 1000, y = 5000 and lower x = 250,
   FC-3B y = 3000, FC-3C y = 3000, FC-5B y = 1000, FC-6A y = 5000, FC-7C y = 20 psi. Codex's: FC-3B
   lower x = 250, FC-4B lower x = 100 and x = 200, FC-5B y = 1000 and lower x = 150, FC-6A y = 5000,
   FC-6C y = 3000, FC-6D lower x = 100. Six lines a reader had left out were measured the same way
   (FC-1D y = 1000 and 5000 and the lower y = 0 of FC-3B and FC-4B in Codex's reading; FC-7C y = 30 psi
   and the top frame of FC-5A in Claude's), and four left frames (x = 0 on both panels of FC-6B and
   FC-6D, Claude's reading). The top frame of FC-3C, visible over 31 percent of its length beside the
   legend, is in neither map.
3. **Canonical reading** (D-026): with the same verified lines in both maps on every panel but FC-4A,
   the ink cannot separate the two (mean distances within 0.25 px), and the first submission
   (Claude) is canonical on 34 of 35 panels; on FC-4A, ticks without a grid, Codex stays canonical as
   the batch named it (D-024). Until now the affine residual had chosen Codex on 14 of the 32 earlier
   panels (6 of them by less than 3 percent) and the batch had named Codex on FC-4A; on the pilot
   the residual reflected Claude's misplaced lines, which the ink check now rejects and the
   recovery replaces.
4. **Corrections found by Codex's review** (`method/`), all applied: exclusions now act before the
   comparison (75 agreed trace samples had been supported by excluded samples); a swapped value takes
   the other reading's whole record (FC-4B n1761's last point was Codex's sequence 4 labelled 3);
   resolutions follow the physical symbol when the canonical reading changes (12 carried); the other
   reading's samples in gaps of the canonical trace are kept as one-sided; bounds move the bracketing
   lines exactly; the maps are compared along every line. The pilot's decision rows without a source
   (141, all made on Codex's points when Codex was canonical) now name it.
5. `before-after-first-run.txt` is the per-panel comparison of the first run (before Codex's review),
   kept because Codex's review cites it (its prompt names it under its former path
   `qa/curves-appc-b1/d025-before-after.txt`).

## Adjudication

Same blind procedure as batches b1 to b5 (`adjudication/`): one crop per item with both readings under
neutral labels P and Q, shuffled per item, the key outside the packet; a Claude and a Codex
adjudicator per item, three of each in round 1 (91 items apiece), one of each in later rounds.

1. **Round 1**, 273 items: runs of one reader's trace samples at curve starts (50) and ends (39) or
   inside gaps of the other trace (107), marker (36) and feature (16) disagreements under the tighter
   bounds, one-sided features (14) and markers (2), identity conflicts (7), trace disagreements (2).
   Most were new questions: Claude's samples at the ends of FC-1C to FC-2C, for example, used to agree
   with Codex samples an earlier adjudication had excluded. 241 settled, 32 split.
2. **Round 2**, the 32 splits with both first-round answers and comments: 19 settled, 13 still split.
3. **Rounds 3 and 4**, 13 and then 2 items: trace samples newly unsupported where rounds 1 and 2 had
   excluded a sample of the other reading (an exclusion leaves a break; D-026), and two features. All
   settled; nothing further was exposed.
4. **Outcome**: 398 decision rows added to the batches' decision files. Where the two readings
   disagreed (or filed one symbol under two tests) and one was right: Claude's reading 37 times,
   Codex's 6; both readings on the symbol or line 4 times. Trace samples excluded as off the line: 26 (on a symbol's outline, in a white gap, on
   another test's curve or a grid line). First, last or peak points neither reading had placed where
   the convention puts them (the line runs into its symbol, so the point is the symbol's centre): 9
   pairs, both readings' points excluded, the trace samples and markers keeping the curve.
5. **Rules settled during the rounds**, applied to every item alike: a reader's name from one
   adjudicator and `both` from the other on a marker resolve for the named, centred mark (the brief
   defines `both` as both inside the symbol; FC-1D's filled dots, one reading about 7 px left of
   centre each time); `neither` from both on a feature excludes both readings' features; and, for
   round 2 on, a sample within 2 px of the line's own ink beyond a dash end is on the line (the
   white-gap rule is for samples placed across a gap), and a line running into an axis continues
   into the axis stroke. The first two were written after the round-1 answers were seen.
6. **Left for the human audit** (`still-split.csv`, 13 items, 14 points): the FC-2B and FC-2C lower
   panel stacks (whether a square is printed between the triangle and the x; the round-2 Claude
   adjudicator reads triangle and x only, overturning both first-round readings, and gives a template
   fit), a sample at a circle's ring on FC-3B, four one-sided features (FC-1C, FC-4B) on which the two
   adjudicators of the other agent and of the author disagree, a knee on FC-4B that has no distinct
   onset, the possible hidden symbol on FC-5A, the start of FC-6A's dense-group line at the origin,
   and one trace disagreement and one feature on FC-1B. Plus one judgment by Claude to confirm: the
   circle printed outside FC-6A's frame, excluded from the data as not a test
   (`qa/curves-appc-b6/review.md`).
7. **Blindness**: every adjudicator worked in a copy of the packet. The round-1 Claude adjudicator of
   items 183 to 273 wrote one scratch file to `/tmp` before moving it into its workspace; it reports
   opening nothing outside the packet.

## Totals after the re-derivation

| batch | points | agreed | one-sided-verified | resolved | open |
|---|---|---|---|---|---|
| curves-pilot-b1 | 502 | 366 | 133 | 1 | 2 |
| curves-appc-b1 | 1886 | 1750 | 85 | 46 | 5 |
| curves-appc-b2 | 1753 | 1400 | 331 | 17 | 5 |
| curves-appc-b3 | 1925 | 1740 | 131 | 54 | 0 |
| curves-appc-b4 | 202 | 197 | 1 | 4 | 0 |
| curves-appc-b5 | 246 | 217 | 24 | 5 | 0 |
| curves-appc-b6 | 223 | 202 | 18 | 1 | 2 |

Totals now (2026-11-07, after the off-ink rule, D-032, and the correction of `some` answers, D-039, which
reached this re-derivation's rounds 1 to 3 and the older rounds of b1 and b3; see each `canonical.csv`):
curves-pilot-b1 540 (273 agreed, 128 one-sided-verified, 5 resolved, 134 one-sided), curves-appc-b1
2,007 (1,458 agreed, 105 one-sided-verified, 47 resolved, 386 one-sided, 11 pending review),
curves-appc-b2 1,764 (1,400 agreed, 310 one-sided-verified, 17 resolved, 37 one-sided), curves-appc-b3
1,924 (1,734 agreed, 128 one-sided-verified, 54 resolved, 8 one-sided).

`data/experiments/` regenerated with `tools/build_batch_records.py <batch>` for all seven batches:
103 records (9 new, the envelope groups of C-5A, C-6A and C-7A), 6721 points (7626 before: the
canonical reading is now Claude's on panels where Codex's denser sampling had been canonical). Peaks of
the shear-stress traces moved by a median of 6 psf and at most 22 psf. Agreement at the reading
bounds: 5909 of 6029 matched points (98 percent); with every bound halved and no decision applied
(`sens-*.md`), 5585 of 6098 (92 percent).
