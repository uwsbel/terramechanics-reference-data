# Review of batches curves-appb-b1, curves-appa-b1 and curves-appa-b3: Appendix B and Appendix A charts

Appendix B modulus plots Figs. B-3 to B-7 (`curves-appb-b1`); Appendix A friction-angle charts Figs.
A-4, 8, 20, 24, 28, 40, 48 (`curves-appa-b1`) and density charts Figs. A-3, 7, 19, 23, 27, 39, 47
(`curves-appa-b3`). The grain-size curves (`curves-appa-b2`) are reviewed separately.

## Readings

Both agents, blind, from evidence packets written by `tools/make_reading_packet.py` (as for Appendix
C). Codex: one run per batch, gpt-6.1-sol high. Claude: one subagent per modulus plot, two for the
seven friction-angle charts, two for the seven density charts; workspaces outside the repository,
filed after the Codex runs had finished. The density readers were stopped by the account's usage limit
on the evening of 2026-10-14 and resumed the next morning in the same workspaces (`meta.json`).

The density batch's instructions described the unit-weight axis as running from 25 to 65 pcf, which is
true of Fig. A-3 only; the other charts run from 55 to 100 or 115 pcf. Both readers followed the pages.

## Calibration

1. **Modulus plots**: ticks on two sides of a frame, no grid. Claude's readers wrote tick
   calibrations with their own helpers in the tool's layout; Codex anchored each tick at every pixel
   along it, which the ink check rejected as "0 of 0 positions" until the check learned to sample
   along such ticks, and once accepted the ticks' own tilts (measured over 19 px) moved them by up to
   1.3 psi across the plot. A line whose anchors span 60 px or less is now a tick taking the map's
   tilt (commit 0f551d2; no earlier batch changed). After that the maps agree to 0.005 to 0.04 units;
   several hundred places still differ by more than the very tight line errors of tick lines.
2. **Friction-angle charts**: grids found in full, maps within line errors everywhere.
3. **Density charts**: the first real use of the reciprocal axis (D-027). Both readers declared
   `--y-transform reciprocal --y-direction down` on all seven, and anchored every 1 pcf line (named by
   count between the labelled ones). The maps differ by at most about 0.1 pcf, beyond the line errors
   at many places (the line errors of 1 pcf lines are a fraction of a pixel). Values are in pcf; the
   records convert to N/m^3 (`series.json` records the transform).

## Agreement and adjudication

First comparison: 207 of 214 matched points agreed on the modulus plots, 185 of 185 on the
friction-angle charts, 278 of 281 on the density charts. The rest were curve ends and knees only one
reader recorded. Blind adjudication by a Claude and a Codex adjudicator (`qa/adjudication-2026-10-15/`)
under the conventions of `qa/curves-appc-b7/review.md` (curve ends at a frame's near edge; a trace
sample in a symbol's outline is off the line); seven Appendix B end samples in ink a polyline shares
with a circle, on which the first round split, were excluded by rule 7 of the protocol directly.

Final canonical points: modulus plots 242 (207 agreed, 27 one-sided-verified, 7 resolved, one open),
friction-angle charts 197 (166 agreed, 31 verified), density charts 301 (262 agreed, 20 verified, 19
open). Of the density batch's 19 open points, 3 are splits (Codex's last mean samples of FA-7, its first upper
sample of FA-23 and its first lower samples of FA-39, one pixel either side of the 2 px rule) and 16 are one reading's samples at Dr 0.1
or 0.9 whose twin in the other reading is in the data, agreed or verified, within the same bounds (the
comparison matches a canonical sample beyond the other trace's end, not yet the other reading's sample
beyond the canonical end; doing so would remove 65 verified rows from the earlier batches). Open points
stay in the records with status `one-sided` (unverified); for the 16 twins, a user who keeps only agreed,
verified and resolved points loses no sample. The modulus plots' open point (FB-4, Codex's first dense sample at a circle's outline)
goes to the human audit with the density splits. With every bound halved: 206 of 225, 183 of 185 and
289 of 313 matched points agree.

## Findings

1. **Fig. B-7** keys only the Dr 1.04 symbol (squares with an x); which circles are Dr 0.995 and which
   0.77 is inferred from the lines they lie on (open circles on the upper line, filled on the lower),
   identically by both readings and both inventories. A person should confirm.
2. **Fig. B-3** prints a y label "3" where 8 belongs (the tick spacing confirms 8), and its polyline
   segments do not pass through the symbol centres (6 to 21 px off; Claude's reader).
3. **Density charts**: the drawn lines' ends differ from their printed end values by up to 0.39 pcf on
   Fig. A-3 and 0.32 on Fig. A-23 (the leaders point at the drawn ends, so this is the drafting);
   Fig. A-47 prints a single right-end label, 89.4, for three lines that end at 89.3, 89.5 and 89.6.
4. **Fig. A-40** (and C-21): the LSM band's edges are the 45 and 40 degree grid lines; the text limits
   the band to Dr .40 to 1.00, the drawing spans Dr 0 to 1.0.

## Records

`b68-sonic-fb-*` (eleven density groups of Appendix B; modulus in ksi converted to Pa), `b68-ds-fa-*`
(seven friction-angle charts), `b68-dens-fa-*` (seven density charts), the ids of the experiment
inventory `experiments-vol2ab-b1`.
