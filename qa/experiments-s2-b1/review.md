# Review: Section II experiment index, batch experiments-s2-b1

Two blind experiment inventories of AM-68-1 Vol. I Section II:
`extractions/claude/experiments-s2-b1/experiments-claude.csv` (139 rows) and
`extractions/codex/experiments-s2-b1/experiments-codex.csv` (180 rows; gpt-6-astra, high,
read-only, 15.3 min, thread 01a1178d-f9f0-7f42-90ba-e048ce99bef3). Both agents had the agreed
figures index and both agents' inventory notes in the repository as hints; both state they read
the pages themselves. Claude's index was written outside the repository before Codex ran.

Alignment: `id-aliases.json` (26 Claude ids renamed to the documented scheme, which Codex had
followed more closely), then `tools/diff_tables.py` on 17 columns (`diff-report.md`), then
`tools/build_experiments.py` with `row-decisions.csv` (one-sided rows) and `resolutions.csv`.
Result: `data/experiments/index.csv`, 175 rows, no cell pending. Written 2026-10-07.

## 1. What agreed without discussion

Test type and soil family agree on every matched row. Every printed number (unit weight, Gp, rate,
bin size, normal stress) agrees after spelling normalization except the five listed in section 2.
Both agents found the same two state conflicts (LPT 26 and LPT 27) independently.

## 2. Factual disagreements, resolved by re-reading the page

| row | column | claude | codex | resolution |
|---|---|---|---|---|
| LPT 93 (Figure 2-32) | identity | LPT 63 | LPT 93 | Codex right; the label reads "LPT No. 93" at 300 dpi (PDF 88). |
| LPT 52, LPT 53 | start depth | 2 and 1 | 1 and 2 | Codex right; LPT 52 (dotted) starts at 1 inch, LPT 53 (solid) at 2 inches (PDF 88). |
| SSD 5-1, 5-6, 5-15, 5-23 (Figure 2-58) | min and max density | shifted by one inset row | as printed | Codex right; Claude's notes had the inset right and the CSV filing shifted it (PDF 122). |
| F2-17 fifth line (LSM) | min density | approx 68 | not printed | Codex right; the minimum endpoint has no label (PDF 61); Claude read a value off the axis. |
| LPT 24 | Dr and setup | none; incomplete | about 0.96; complete | Codex right; text 2-74 gives the group Dr and Figure 2-44 the bin. |
| F2-40 B, C, D | setup | incomplete | complete | Codex right; Dr 0.15 and the 36 by 18 bin are in text 2-74. |

Four of six went against Claude's filing, two of them clerical (a swapped pair, a shifted row).
That is the kind of error the two-reading protocol exists to catch, and it argues for keeping the
5 to 10 percent audit of agreed cells.

## 3. Granularity and vocabulary (settled by convention, recorded in row-decisions and resolutions)

1. Codex's finer rows adopted: one row per marker group in Figure 2-51 (5), per series in Figure
   2-60 (4), per soil for the sonic modulus (12), the unused-range bands of Figures 2-57 and 2-58,
   Table 2-3 values not covered by any figure (soils 10 and 11 friction, soil 12 gradation), the
   52.6 degree dense RS shear series, and twelve text-only bed preparation summaries (achieved Dr
   by placement method and by roller passes per soil).
2. Codex's rows rejected: the six bearing capacity factor curves of Figure 2-31 and the analytical
   line on Figure 2-33 are computed, not experiments; they stay in the figures index as trace class
   `computed`.
3. Claude's rows kept that Codex lacked: the unlabeled tenth line of Figure 2-49 and the DPT record
   54074 cited in the Figure 2-29 inset.
4. `kind`: the pressure-parameter curves of Figures 2-37, 2-49 and 2-50 are `derived-series` (the
   report does not say whether they are single tests or averages); Figures 2-36, 2-38, 2-39 are
   `averaged-series` (text 2-69 says so); the friction-versus-density curves of Figure 2-23 are
   `derived-series` (from Appendix C tests), not `correlation`; the min/max density lines of
   Figure 2-17 are `averaged-series`.
5. `soil_no`: Codex withheld nominal soil numbers for beds whose Dr is not the Table 2-3 state
   (dense RS at Dr 0.94 to 0.97 is not soil 4 at Dr 0.80) and for family-level series. Adopted as
   a rule: a soil number both agents did not assign is not assigned; every row without a soil
   number has status `unknown`.
6. `*_printed` discipline: Codex applied the "as printed" rule more strictly (no state for series
   whose caption gives none, no Dr for an axis range). Adopted; `state_printed` is taken from
   Codex's submission, Claude's wording kept in the sidecar.
7. Setup facts one agent found in the text and the other left empty (DPT geometry, tamping foot,
   shear rate on derived series) stand with status `one-sided-cell` and are listed for the audit.

## 4. Priority and MCC under the rules of 2026-10-07

Codex moved LPT 28 and 29 to priority 2 (no Dr or Gp printed; rate series) and the failure
envelope to 1; both adopted. Claude kept the triaxial text values and the DPT bed statistics at 2
(not reproducible, interpretation only). The Figure 2-17 lines are MCC `yes` (state maps,
consistent with the figures index) and priority 2. The screeding dip in Figure 2-36 and the 108 by
36 bin intermediate curves of Figure 2-37 are MCC `maybe`.

## 5. What the index says about the data

| count | what |
|---|---|
| 44 | single physical tests: 30 LPT, 7 direct shear, 4 DPT records, 3 compaction tests |
| 27 | LPT records with a printed bed state or Gp |
| 4 | tests with a complete printed setup (LPT 24; F2-40 curves B, C, D) |
| 71 | derived or averaged series whose underlying tests are not identified |
| 5 | rows carrying a conflict (LPT 26, LPT 27, two DPT records tied to them, soil 10/11 numbering) |

Every single LPT record lacks at least one of rate, bin or start depth on its own figure; the
transcription of the text pages and Volume II are expected to fill most of these.

## 6. Audit sample of agreed cells (student)

Rows agreed on every reconciled cell: LPT 22, 23, 25, 75, 76, 79, 85, 88, 89, 91, 95, 98, 101
and the seven direct shear tests. Suggested audit: LPT 25 (gamma 51.6, Gp 130), LPT 85 (Gp 46),
LPT 101 (Gp 63.9), direct shear at 1172 psf (gamma 46.8), SSD 4-18 (63.6 to 76.6), plus two
one-sided cells (DPT geometry on record 53958; shear rate on the Figure 2-23 series).

## 7. Credit

Codex: LPT 93, the LPT 52/53 start depths, the Figure 2-58 inset rows, the unlabeled minimum of
the LSM line, LPT 24 and F2-40 setups, stricter as-printed discipline, finer rows for Figures
2-51 and 2-60 and the sonic moduli, the bed preparation summaries, the soil 10/11 numbering slip
on printed 2-110. Claude: the LPT 26 DPT record conflict (found independently by both), the
tenth line of Figure 2-49, exclusion of computed curves, the priority reading for text-only values.
