# Review of batch curves-pilot-b1: Figure C-1B (RS direct shear, seven normal stresses)

Date: 2026-10-08. Reviewer: Claude (page re-reads of every disputed or one-sided location). No
human audit yet; `qa/audits.csv` has no row for this batch, so "agreed" below means the two agents
agreed, not that a person confirmed it.

## What was read

Figure C-1B, AM-68-1 Vol. II (CR-92215), printed C-3, PDF 117, 300 dpi rendering
`corpus/1968-vol2/images/p0117.png`. Upper panel: shear stress (psf) against shear displacement
(thousandths of an inch) for seven normal stresses, 294 to 3520 psf, drawn curves with plotted
symbols. Lower panel: dilation (thousandths of an inch) against shear displacement, symbols only.
The same tests are printed as Figure 2-21 in Volume I; the Volume I printing was in the packet as
context and is not read here (step 3e will add the cross-check).

Evidence packet (source only): the page image, the two preceding pages, `docs/CURVE-READING.md`,
the figures-index and experiment-index rows, `tools/plot_grid.py` and `tools/calibrate_axes.py`.
Neither agent saw the other's output or any earlier note. Claude's reading was written outside the
repository until Codex finished.

## The two readings

| | Claude | Codex (gpt-6-astra, high, 1181 s) |
|---|---|---|
| upper calibration | 42 anchors, RMS 0.594 / 10.2 psf (5000 line predicted) | 42 anchors, RMS 0.174 / 9.24 psf (5000 line predicted) |
| lower calibration | 18 anchors, RMS 0.366 / 0.356 | 18 anchors, RMS 0.269 / 0.375 |
| upper panel | 289 trace samples every 5 thousandths (column scan with a right-to-left tracker); no markers | 83 markers, 484 trace samples every 20 px (about 3.4 thousandths), 25 features |
| lower panel | 92 markers by eye on 4x crops | 93 markers (contact sheets, connected components as a check) |

The two calibrations agree: the corners of Claude's frame box map to the same values within 0.9
in x and 1.7 psf in y (upper), 0.6 and 0.1 (lower). Codex's are canonical on both panels by the
rule (smaller residual); nothing was averaged.

## Diff results

| panel | matched | agreed | disagreed | one-sided in the canonical reading |
|---|---|---|---|---|
| 1 | 462 | 462 | 0 | 130 (83 markers, 25 features, 22 trace samples) |
| 2 | 92 | 92 | 0 | 1 |

Sensitivity (`--bound-scale`): with every bound halved, 6 of 462 upper samples and 1 of 92 lower
markers would disagree; at a quarter of the bounds, 33 and 21. The readings are consistent to
roughly half the stated bounds.

## Decisions (`decisions-p1.csv`, `decisions-p2.csv`)

1. **Upper-panel markers (83): one-sided-verified, credit Codex.** Claude's reading omitted the
   upper-panel markers, which the protocol lists first; this is a protocol deviation on Claude's
   side. Every marker's symbol and center was checked by Claude on Codex's 4x contact sheets
   (`markers-p1-<series>.png`, each marker under a crosshair). All 83 are the right symbol on the
   right curve; centers on gridline or frame merges carry Codex's wider bounds.
2. **n2345 trace, x 168 to 198 (10 samples): resolved for Codex.** Two ink strokes run between
   u 1830 and 1965: a straight one at v about 2044 (about 2750 psf) that ends at the x = 200
   gridline, and a curved one through the squares at u 1784, 1906 and 2026. Claude's tracker
   followed the straight stroke; Codex followed the curved one. The page crop shows the squares sit
   on the curved stroke and the straight stroke is stray ink, so Codex was right. Codex's feature
   "end of the short lower stroke" (seq 68) is excluded as a feature of the stray ink.
3. **Codex's bridges across visible interruptions with no counterpart in Claude's trace (4 trace
   samples: n1760 seq 46; n294 seq 49, 50, 52): excluded.** Codex labeled them estimates of the
   drawn line's continuation, not readings of ink. Rule 4 of `AGENTS.md`: what could not be read
   is not guessed.
4. **The other 18 one-sided trace samples: one-sided-verified.** Series ends at x 244 to 248
   (Claude's column list stopped at 245; the ink reaches the end symbols at the frame) and the
   resumption of n1760 and n294 after marker interruptions (ink present on the crops).
5. **Features: first and last points one-sided-verified** (they coincide with verified end
   markers); **peaks one-sided-verified** (Claude's trace maximum lies within the sum of the bounds
   of every peak feature; largest offsets n587 dx 13 of 24 allowed, n294 dx 10 of 20); the two
   descriptive features (n587 rounded transition, n2935 shallow trough) stay `one-sided`.
6. **Lower-panel n1760 at x = 0: one-sided-verified.** A plus drawn about 25 px left of the frame
   on the zero line (Codex's `p2-origin.png`, confirmed), the n1760 point displaced by the
   draftsman to clear the origin cluster. Codex's x bound (5.1) covers x = 0; the fitted x of -4.7
   is not a measurement.
7. **Lower-panel n1172 at x = 0: missing in both readings.** Neither agent could separate a
   down-triangle from the circle on the frame line at (807, 3295). Recorded here, not in `data/`.

Result in `data/experiments/`: 680 points over seven records; agreed 544, resolved 10,
one-sided-verified 124, one-sided 2; 5 points excluded. (At this review. The batch now has 540 canonical
points, after the re-derivation of D-025, the off-ink rule of D-032 and the correction of `some` answers
of D-039: `qa/curves-rederivation-d025/review.md`, Totals.)

## Places where agreement rests on wide bounds

These agreed under the stated bounds and show up when the bounds are halved. A student audit
should start here.

1. n2345, x about 48 (u about 1070): the n2345 and n1760 rising lines share ink; readings differ
   by 84 psf.
2. n1760, x about 23: same merge region; 65 psf.
3. n587, x 140 to 160: the descending line runs along the 1000 psf gridline between two triangles;
   readings differ by up to 55 psf and the curve's center is genuinely uncertain to about 10 px.
4. n587, x about 102: the triangle at (1383, 2528) merges with the x = 100 gridline; Claude's
   column scan sits 56 psf below Codex's trace, which follows the plateau.

## Findings about the protocol (applied in `docs/CURVE-READING.md`, D-018)

1. **Trace samples are not matched by nearest x.** Each reader samples at displacements of their
   own choosing; the first diff reported 92 disagreements that were sampling offsets of 1.2 to 1.7
   thousandths on steep rises. The tool now interpolates the other reading at the canonical sample
   and propagates the x bounds through the local slope.
2. **A trace bound is half the line thickness.** Codex read the protocol's "the line thickness" as
   the half-width, which gave a median bound of 58 psf (about 1 percent of the axis span) and a
   weak agreement test. The protocol now says half the thickness; the submitted bounds were not
   changed (submissions are immutable), so the error bars in this batch are conservative.
3. **Both agents must read markers on every panel.** Claude read only traces on the upper panel;
   83 markers entered as one-sided-verified instead of agreed.
4. **The calibration check compared different pixels.** `tools/diff_curves.py` mapped each
   reading's own box corners; it now maps the same corners through both calibrations.
5. Codex's connected-components listing and contact sheets are a good verification aid; adding a
   contact-sheet step to the protocol would let the student check markers in minutes.

## Credit

Codex: the upper-panel markers and features, the n2345 stroke decision, the displaced origin
symbol, the end-of-trace samples, and the observation that the 5000 psf line is interrupted by the
heading (both detectors predicted it). Claude: the panel-2 marker reading that confirmed Codex's
92, the diff-tool corrections, and the bridge exclusions.

## Suggested audit sample (not yet recorded in `qa/audits.csv`)

The four wide-bound places above; ten upper-panel markers across the seven series (two on
gridline merges); the n2345 resolved segment; five lower-panel markers near the origin where
circles and down-triangles touch.

## Correction after the second dry run of audit packet 1 (2026-10-09)

Row 8 of the starter packet is a compare row on the 2345 psf curve at a displacement of about 48
thousandths of an inch, where the two readings differed by 84 psf. Re-reading the scan with both
agents' traces drawn on it showed why: the 2345 and 1760 curves share one drawn line up to the plus
symbol of the 1760 test at u about 1030, then fork. The upper branch runs to the 2345 square at
u 1093, the lower branch to the next 1760 plus at u 1140 (ink runs at u 1049: v 2294-2305 and
2311-2322). Codex's 2345 trace, the canonical reading on this panel, followed the lower branch on
top of its own 1760 trace for two samples; Claude's stayed on the upper branch. Decisions
`n2345 trace 13, 14` in `decisions-p1.csv` keep Claude's values (credit Claude); the series now has
12 resolved points.

The two points had "agreed" because this batch keeps wide bounds (about 93 psf here). That is the
case the audit exists for: two readings agreeing within generous bounds while one is on the wrong
line. Dan's pick on the row (the blue mark, then Codex's reading) was the wrong one, and the
close-up was the reason: it showed only 140 scan pixels, too little to see where each branch goes.
Compare close-ups now show 300.

Two tool fixes came with it: `tools/diff_curves.py` now gives a swapped value its own pixel
position and keeps the rejected value as the row's other reading (before, the canonical row kept
the evaluating reading's pixel, and the rejected value was lost).
