# Review of batch experiments-vol2c-b1: experiment rows for Volume II Appendix C

Date: 2026-10-13. Both agents read Appendix C (PDF 115 to 159) blind from the page images, the page
transcriptions, the figures index and the Volume I experiment index (for relations only); neither
opened `extractions/` or `qa/`. Codex: gpt-6.1-sol high, 808 s. Claude: one subagent, 1176 s,
written outside the repository until both had finished. Prompt: `extractions/*/experiments-vol2c-b1/prompt.md`.

## Result

Both inventories have 130 rows (85 single tests, the rest envelopes, friction-angle charts and
computer plots). 94 ids agreed as submitted; the other 36 differ only by naming convention and are
aliased to Claude's (`id-aliases.json`): envelopes by printed Dr range in hundredths
(`b68-ds-fc-1a-dr50-57`; Codex's `dense`, `intermediate`, `superdense` were ambiguous across the three
RS groups), psi stresses with `p` for the point (`b68-ds-fc-7b-n27p1psi`), and Figure C-23 under the
Volume I ids of Figure 2-23 (one derived series, one row). The same convention names the series of
the envelope curve batch `curves-appc-b5`.

`data/experiments/index.csv` now stacks the two batches (`tools/build_experiments.py --batch ...`):
292 rows, 104 agreed, 146 resolved, 42 one-sided (all from Section II), none pending. The seven tests
of Figure C-1B and the six series of Figure C-23 are the Volume I rows, with the Volume II figures
added to their evidence. The index gains `relation` and `relation_target` (empty for Section II).

## Resolutions (`resolutions.csv`, 34 cells)

1. **kind of the computer plots C-8 to C-15** (14): `derived-series` (Claude) over `correlation`
   (Codex): the plots draw the test points with the computed curve, and the vocabulary reserves
   `correlation` for a fit drawn without its points. Convention.
2. **mcc_relevant of the C-7B and C-7C tests** (12): `no` (Claude) over `maybe`: the `maybe` for
   direct shear rests on the dilation panel, which these psi sheets do not have. Rule.
3. **priority of the C-23 series** (6): 2 per the prompt; the rows merge into Volume I's, whose
   priority 1 stands.
4. **C-9A derived from all seven C-1D tests, the zero-stress test included** (credit Claude). C-9A
   prints tan 1.3059 and cohesion 634.20 psf. A least-squares line through the peaks of the seven
   C-1D tests as read in `curves-appc-b1` gives tan 1.3099 and 635.1 psf (0.3 and 0.1 percent off);
   without the zero-stress test, 1.2746 and 727.3. So the 1968 fit used the test C-9A does not plot.
   The check also validates the digitized C-1D peaks against an independent printed number.
5. **C-19 derived from C-4A and C-12** (credit Codex): in the five other friction-angle charts both
   inventories agree the points combine the hand-drawn envelope and the soil's computer plot; C-12's
   43.07 degrees and C-4A's 43 overlap at Dr 0 on C-19.

## Conflicts between figures both inventories reported

1. C-2A's legend symbols look swapped against the data sheets (its squares sit on the dense C-2C
   peaks); the envelope rows keep the printed legend and note the conflict.
2. C-1B prints gamma 46.8 for the 2935 psf test; the Volume I row has 46.5 (kept, noted on the row
   and in `index.json` `merged_rows`).
3. C-5B's header gamma upper bound reads 97.3 (or 97.8) against 97.6 in its legend and in C-5A.
4. C-6D prints 3814 (C-6A labels 3820); C-6C prints 1961 and 714; C-4C prints 741.
5. Captions of the computer plots disagree with the printed states ("PS Loose" for Dr .33 to .53,
   "RS Dense" for about Dr 1.1, "LSM Dense" for about Dr 1.03); their soil numbers are `conflict`.
