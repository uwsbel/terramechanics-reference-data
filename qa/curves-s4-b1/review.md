# Review of batch curves-s4-b1: vertical footpad impact runs (pilot of the dynamic families, D-050)

Figs. 4-19 and 4-20 (Volume I, printed 4-23 and 4-24; PDF 208 and 209): three vertical impacts of the 6.17 in
instrumented 1/6-scale footpad on RS soil at about six ft/s, Run No. 4 (Dr 0, solid line), Run No. 10 (Dr 0.45,
dotted) and Run No. 12 (Dr 0.65, long dashes with short dashes between). Fig. 4-19, printed upright, has two
panels sharing a time axis in milliseconds: vertical force in pounds (panel 1) and footpad displacement into the
soil in inches (panel 2). Fig. 4-20, printed sideways, plots force against displacement for the same runs; the
figures index records it as derived from Fig. 4-19. The first batch with time on an axis.

## Readings

Both agents, blind, from the evidence packet written by `tools/make_reading_packet.py`
(`qa/curves-s4-b1/batch.json`), 2026-11-19. Codex: gpt-6.2-sol high, one run for both figures (653 s). Claude: one
subagent per figure (claude-opus-5-5), writing outside the repository until Codex had finished. **Hints
available:** the orchestrating session read the Codex run's final summary while the Claude reader of Fig. 4-19 was
still working and passed nothing to it. The Claude reader of Fig. 4-19 did not have `p0209.png` (Fig. 4-20) in its
workspace although its brief listed it, so unlike Codex it could not use Fig. 4-20 as a check on the time axis; it
reported this. Both received the same batch description; its line styles and labels match the page.

Points submitted (trace and feature rows): Claude 159 and 114 on Fig. 4-19 panels 1 and 2, 137 on Fig. 4-20; Codex
206, 138 and 158. No plotted symbols on either figure.

## The time axis past 100 ms

The time grid of Fig. 4-19 is evenly spaced (119 to 124 px per line on both panels, no break mark), but its labels
read 0, 10, ..., 90, 100, then **120, 130, 140** under the next three lines, and the right frame is unlabeled: 110 is
missing. Read as a uniform axis, which is how an oscillograph trace is plotted, those lines are 110, 120 and 130 ms
and the frame 140 ms. Codex anchored them so. Claude's reader judged the same assignment more likely but anchored
nothing past 100 and extrapolated the 90 to 100 interval (up to 1.1 ms different on panel 2). For a comparison on
one footing, the four lines past 100 were measured on the page for Claude's calibration from its own grid with
`tools/calibrate_axes.py recover` (`knots.csv`, 8 lines, straight-line residuals 0.24 to 0.43 px); they lie within
half a pixel of the lines Codex measured independently (Codex's review fitted them within 0.09 px). Taken as
printed, a time between the 100 ms line and the next would be up to 10 ms later (the difference grows across that
interval) and every later time 10 ms later. Nothing on the page tests the scale: Fig. 4-20 cannot, because the same
rescaling of both time axes of Fig. 4-19 leaves force against displacement unchanged. The record panels carry this
as a note (`panel-map.csv`, `note`), shown on the record pages beside the data.

## Calibration

Fig. 4-19 panel 1: the 500 lb line is not a knot in either reading (the legend box interrupts it; ink at 4 to 5 of 25
positions) and Claude's 550 lb line was off the ink at one end; the maps interpolate between 450 and 600 lb there,
which at the run 12 peak (588 lb) changes the value by less than 0.5 lb. Largest difference between the two maps
along every line and interval midline: 0.028 ms and 0.60 lb, none beyond the line errors. Codex's reading is
canonical (its lines include Claude's).

Fig. 4-19 panel 2: Codex also anchored the top frame as 4.5 in. That frame tilts -0.0063 against about +0.0006 for
the grid lines (about 5 px, 0.02 in, at the panel's ends), so it is not a reliable 4.5 in line; Claude's reader left
it out for that reason and extrapolates the even 3.5 to 4.0 in spacing. Claude's reading is named canonical for this
panel (`overlays.csv`, `canonical`); only run 4's displacement above 4.0 in uses that interval. The right frame (140
ms) also tilts a little (0.002 to 0.003); only run 12's last sample, past 130 ms, lies in that interval (about 0.1 ms).

Fig. 4-20: the same 10 displacement and 13 force lines in both readings, affine residuals 0.0023 in and 0.36 lb; the
maps differ by at most 0.0003 in and 0.044 lb. Claude's reading is canonical (the first submission, the readings'
lines being equally close to the ink). The scan has a blank strip near 1.6 to 1.9 in where the dotted run 10 and the
grid are missing; both readings stop at the last dot before it and resume after it.

## Comparison rule for features (tool change)

`tools/diff_curves.py` paired features by the first role word anywhere in a reader's note, a rule made for curves with
one first point, one peak and one last point. These histories have several maxima, minima and knees per run, and the
rule read "knee, minimum after the first peak" as a first point and "knee, minimum after impact peak" as a peak, so
matching minima could never pair and leftover features paired across 90 ms. The batch sets `feature_roles=leading`
in `overlays.csv` (from 2026-11-19, `--feature-roles leading`): the note's opening word gives the role, knees and
minima pair in one group, a role with several features per run pairs only within 40 px on the page, and a minimum is
compared like a peak (its depth, not its time). The earlier batches keep the earlier rule and regenerate unchanged.
This removed most of the first comparison's disagreements, which were mispairings, not readings that differ.

## Agreement and adjudication

Before adjudication, 435 of 440 matched points agreed within the sum of their bounds; every one of the 795 trace
samples of both readings passed the ink check (D-031). Blind adjudication in `qa/adjudication-2026-11-19/`, two
rounds (60 and 15 items). The three trace disagreements were sampling, not reading: run 12's sharp apex lies between
Claude's samples (both readings give 588 lb at the apex), and at run 4's end hook on Fig. 4-20 the comparison by
displacement fails on a vertical stroke that both readings followed; both adjudicators answered `both` for all three.
Both adjudicators excluded the two first samples placed inside the frame at the origin corner of Fig. 4-19 panel 2,
one trace sample past the end of its line's ink, and 11 one-sided features that do not sit on a bend of the line within 8 px.

Final canonical points: 507 (430 agreed, 52 one-sided-verified, 4 resolved, 20 one-sided, 1 pending review). What
stays open (mandatory rows of the student audit), 21 points:
1. the starts of the three runs inside the merged ink at the origins of both figures, where line style cannot tell
   them apart;
2. run 12's start on Fig. 4-19 panel 2 (pending review): Codex's reading starts it at 0.3 ms inside the bundle,
   Claude's at 9.0 ms where its own dash first appears; one adjudicator follows its dash rhythm into the bundle to
   about (758, 3268) px, the other cannot tell;
3. the late band of Fig. 4-19 panel 1, 95 to 117 ms, where the three runs touch and cross (run 10's weak late crest,
   two of Codex's run 12 samples).

## Fig. 4-20 against Fig. 4-19

Fig. 4-19's force and displacement, paired at equal times, give Fig. 4-20's force within 0 to 3 lb at most
displacements (run 4 at 0.5, 1.0, 1.5, 2.0, 3.0 and 4.0 in: 105/105, 72/72, 86/86, 101/104, 121/123, 142/139 lb). The
larger differences lie on steep falling branches, where a shift of 0.02 in explains them: run 10 at 1.0 in 153/143 lb,
run 12 at 0.5 in 521/547 lb. The impact peaks lie 0.02 to 0.04 in further along on Fig. 4-20 (run 4 0.22/0.24 in,
run 10 0.30/0.31 in, run 12 0.36/0.40 in), which at the impact rate of about 0.08 in/ms is 0.25 to 0.5 ms, within the
time reading bound (median 0.6 ms). Fig. 4-20 is consistent with a cross-plot of Fig. 4-19 to the precision of the
readings. This checks that the two panels of Fig. 4-19 agree with each other; it does not test the time scale, which
a common rescaling of both panels would leave unchanged (Codex's review).

## Records

`tools/build_batch_records.py curves-s4-b1`: three records, `b68-imp-4`, `-10`, `-12`, each with three panels
(record panels 1 and 2 from Fig. 4-19, 3 from Fig. 4-20, marked `relation: derived-from F4-19`), the first records
read from two figures (`docs/DATA-ORGANIZATION.md`, records from several figures). SI: time in s (factor 0.001),
force in N, displacement in m. The setup is incomplete for all three (`data/experiments/index.csv`, batch
experiments-s3s5-b1): the impact velocity is printed only as about six ft/s for every run, the moving weights of
runs 10 and 12 are not printed, and no bed density is printed for these runs.

## Afterwards: the breaks in the comparison (2026-11-19, batch curves-s5-b1)

Codex's reviews of batch curves-s5-b1 found that a documented break in a drawn line (`breaks.csv`) stopped the plot's
line but not the comparison, which still interpolated the other reading across it within the gap rule. The comparison
now refuses that (`tools/diff_curves.py --break-a`, `--break-b`, passed by `tools/reconcile_curves.py`), and a sample
beside a break is compared directly with the other reading's nearest sample on an intact stretch, within both bounds.
`breaks.csv` here gains the two edges of each dropout measured on the page (`gap_u1` to `gap_v2`: run 10 about 190 px,
run 4 about 30 px), mapped on each reading's own calibration. With those spans nothing in this batch changes (a first
version of the rule, which took the span between the two samples named, was wider than run 4's dropout and would have
made three agreed samples one-sided; Codex's third review found it).
