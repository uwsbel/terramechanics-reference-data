# Data organization and conventions

This is the data dictionary for the repository. It is updated in the same commit as any change to
the layout, file formats or vocabularies, so it never lags the data. Version 1, 2026-10-07.

## Purpose, in one paragraph

Physical soil-test data from Apollo-era NASA contractor reports is recovered from scanned pages
into machine-readable files (SI units), with the test setup, the provenance of every number and the
uncertainty of reading it from the page recorded (the experimental uncertainty is known only where
repeat tests show it), so that anyone with a simulator can set up these experiments as virtual
experiments, as far as the recorded setup allows, and judge the simulator against them (Project
Chrono's soil models are our own first use, in separate repositories since 2026-11-18, D-046). The same organized corpus lets an agent answer questions from the source material with page
citations.

### Calibration and validation are the user's choice, not a property of the data (D-028)

Almost any test can serve to calibrate a model or to validate it; which one is a choice made in a
particular study, for a particular claim, with a particular model, and others may choose otherwise.
The data therefore carries no such roles. It records, for every experiment, the facts any split
needs:

1. **What kind of test it is**: an element test, in which the soil is in a nearly uniform, known
   state (direct shear, density limits, grain size), or a boundary-value test, whose response mixes
   many properties (static load-penetration, dynamic penetrometer); a derived series (an envelope, a
   friction-angle chart) is a reduction of other tests, not an experiment of its own.
2. **What was measured and how well**: the setup and how complete it is (`setup_status`), the
   response, and its uncertainty (reading bounds; the scatter of repeat tests where they exist).
3. **How tests depend on each other**: same soil, same bed state, same laboratory, and the hard
   dependencies (`relation`: `same-as`, `derived-from`) that any split must respect so that no data
   is used on both sides of it.

Notes on what a given test can and cannot pin down for a given kind of model (for example, a direct
shear peak constrains a continuum model's friction coefficient, through a model-specific conversion,
but not its stiffness, while a push test mixes friction, density, stiffness and dilation) are documented beside the data, so whoever chooses a
split knows what each choice can show. Example splits, with their reasons, belong to studies and to
the benchmark's documentation, never to the data files.

## Folder layout

| Folder | Holds | Tracked |
|---|---|---|
| `AGENTS.md` | How an agent navigates, answers and cites from this repo | yes |
| `docs/` | This document, `KNOWN-LIMITATIONS.md`, release notes | yes |
| `sources/` | `register.csv` (acquired and screened sources, rights evidence, checksums); `leads.csv` (the broad hunt: every candidate source graded for rights, data form and setup recoverability, with both agents' grades and `found_by`); `searches-log.csv` (every search run, including the ones that found nothing) | yes |
| `nasa-reports/` | The source reports and data sets, each with its rights evidence in `sources/register.csv` (public use permitted), and the project lead's planning note; the public release keeps only the Planetary Data System bundles and links the NTRS reports by their records (D-054) | yes |
| `corpus/<source>/` | `page-map.csv`, `pages/pNNNN.md` transcriptions, `contents.csv`, `symbols.csv`, `figures.csv`, `equations.csv`, `glossary.csv`; `images/` rendered pages (regenerable) | yes, except `images/` |
| `insights/` | Short cited notes capturing judgment, caveats and recommendations found in the text | yes |
| `extractions/<agent>/<batch>/` | Immutable independent submissions from each agent, exactly as produced | yes |
| `data/materials/` | Soils: families, mixtures, batches, density states | yes |
| `data/experiments/<id>/` | One physical test: `setup.json`, `observations.csv`, `series.json`; `index.csv` at the folder root | yes |
| `data/derived/` | Reductions and conversions computed from `data/experiments` by scripts in `tools/` | yes |
| `qa/<batch>/` | Review packets: overlays, discrepancies, decisions, canonical points, `audit-meta.json` (what a reviewer is told about each figure) | yes, except images |
| `qa/audits/` | The reviewer audit program: `reviewers.csv`, `assignments.csv` (chunks, pairs, deadlines), `sample.csv`, `keys/` (answer keys, never sent), `table-controls.csv` (the controls `plan` chose for chunks of table cells, never sent), `returns/`, `returns-log.csv`, `voided.csv`, `withdrawn.csv`, `status.md`, `reports/`, `digests/`; the audit rows themselves are in `qa/audits.csv`. The public release keeps `qa/audits.csv` and `voided.csv` only | yes |
| `schemas/` | JSON Schema for every sidecar and the CSV column contracts | yes |
| `paper/notes/` | Findings written for the manuscripts, one topic per file, each paragraph cited | yes |
| `tools/` | All scripts; nothing in `data/` is produced by hand | yes |
| `.agent-related/` | Agent working records (plans, run folders, consultation records) | no |

## Source identifiers

`source_id` in `sources/register.csv` is a short slug: `bendix-1968-vol1`, `bendix-1968-vol2`,
`mdac-1970-cr66914`. The corpus folder for a source is named by year and volume where that is
unambiguous (`corpus/1968/` for Volume I; Volume II will be `corpus/1968-vol2/`).

Register statuses: `lead` (identified, not located), `located` (found, not in hand), `acquired`
(file in `nasa-reports/`, checksummed), `screened` (contents inspected and summarized),
`eligible` (holds data in scope), `extracted`. Dead ends are kept with status `not-located` and a
note of where was searched.

Leads move from `sources/leads.csv` into the register through a screening batch:
`tools/promote_leads.py <screened.csv> <leads.csv> <register.csv> --agent <who> --date <when>`
writes one `located` row per screened lead (identity fields as the screen confirmed or corrected
them against the archive record, the lead's relation to the Bendix study, and the screening verdict
`acquire | acquire-with-caveat | lead-only` with the setup and text-layer assessment in `notes`).
A row becomes `acquired` only when the file is downloaded and checksummed:
`tools/acquire_source.py <source_id> <url>... [--crawl] --date <when>` saves the files under
`nasa-reports/<source_id>/` (a PDS bundle is crawled from its directory listing and kept with its
relative paths), writes the SHA-256 digests, page counts and local path into the row and sets the
status; a re-run of `promote_leads.py` keeps those acquisition fields. A single file's digest goes
in the row; a bundle gets `nasa-reports/<source_id>/SHA256SUMS.txt` (one line per file) and the
row holds the digest of that manifest. Videos and high-resolution scans inside a bundle are not
tracked by git (`.gitignore`) but are in the manifest, so the acquisition is reproducible and
checkable. The screening submission
lives under `extractions/<agent>/leads-screen-b<n>/` with its review in
`qa/leads-screen-b<n>/review.md`.

## Page identity

Every page has two identities: `pdf_page` (1-based page in the file we hold) and `printed_label`
(the label printed on the page, for example `2-35`). Both are always given together. The map is
`corpus/<source>/page-map.csv` (`pdf_page, printed_label, label_source, inferred_label,
appendix_heading`); `inferred_label` is the authoritative printed label (OCR misreads are
outvoted by the per-section offset). A citation reads: `AM-68-1 Vol. I, Fig. 2-21, printed
2-43, PDF 68`.

## Units

SI is canonical. Every quantity in `data/` has an SI column; the value as printed is kept in a
`*_native` column with its unit named in the sidecar, for traceability only, and is never used
downstream. Conversions are done by `tools/to_si.py` from this table (exact or CODATA values):

| From | To | Factor |
|---|---|---|
| inch | m | 0.0254 |
| ft | m | 0.3048 |
| lbf | N | 4.4482216152605 |
| lb (mass) | kg | 0.45359237 |
| psi | Pa | 6894.757293168 |
| ksi (kips/in.^2) | Pa | 6894757.293168 |
| psf | Pa | 47.880258980336 |
| pcf (unit weight) | N/m^3 | 157.08746 |
| pcf (as mass density, dividing by g = 9.80665) | kg/m^3 | 16.018463 |
| in/min | m/s | 0.0254 / 60 |
| in/s | m/s | 0.0254 |
| ft/s | m/s | 0.3048 |
| in/s^2 | m/s^2 | 0.0254 |
| g (acceleration) | m/s^2 | 9.80665 |
| ms | s | 0.001 |
| s | s | 1 |
| mm | m | 0.001 |
| mil (thousandths of an inch) | m | 0.0000254 |
| deg (angle) | deg | 1 |
| deg/s (angular rate) | deg/s | 1 |
| none (dimensionless, e.g. relative density Dr) | none | 1 |
| percent (e.g. percent finer) | none (a fraction) | 0.01 |

Unit weight and mass density are distinct quantities and both are reported; the report's "unit
weight gamma, pcf" is converted to N/m^3 and, under standard gravity, to kg/m^3 with the column
name saying which. Normalized quantities (pressure parameter, relative depth) keep the report's
definition, recorded in `glossary.csv`, together with every quantity needed to undo the
normalization.

## Materials (`data/materials/`)

`materials.csv`: one row per soil number as the report defines it (a material in a density state).
Columns: `soil_no, bendix_designation, description_verbatim, family, state, relative_density,
unit_weight_native, unit_weight_unit, unit_weight_N_m3, bulk_density_kg_m3, friction_angle_deg,
elastic_modulus_native, elastic_modulus_unit, elastic_modulus_Pa, mean_grain_size_mm,
uniformity_coeff, percent_passing_200, d95_mm, read_flags, source_locator, status`.
Families are the report's: RS, PS, RSM (a and b are different mixtures and stay separate), RC2, SS,
LSM. `source_locator` names table, printed page, PDF page and row.

`specifications.csv`: the Appendix A soil specifications (Vol. II, PDF 2 to 98) in long form, one
row per soil and quantity, built by `tools/build_specifications.py` from the canonical page files.
Columns: `soil_no, quantity, qualifier, value_native, unit_native, value_si, unit_si, printed_text,
source_locator, status`. Quantities: `bendix_designation`, `relative_density`, `friction_angle`
(and `friction_angle_band_low/high` for LSM), `elastic_modulus` (qualifier `about`, `as printed` or
`estimated, not measured`), `modulus_confining_pressure`, `placement` (the printed sentence),
`roller_count` (qualifier `passes` or `rollings`, as printed), `mix_ratio_by_weight`,
`d50/d10/cu/d95_average` and `_range` (grain size chart inset), `gamma_min_label_k` and
`gamma_max_label_k` (density chart end labels, pcf and kg/m^3). Each soil's values come from its
own sheet. `qa/specifications/table23-vs-appendix-a.md` is generated with it and compares every
Table 2-3 cell; `--check` rebuilds both and compares.

## Experiments (`data/experiments/`)

`index.csv`: one row per physical test, test series or derived series. Columns: `experiment_id,
source_id, kind, test_type, test_label_printed, soil_family, soil_no, soil_no_status,
state_printed, dr_printed, unit_weight_printed_pcf, gp_printed_g, apparatus, penetrator_printed,
bin_printed_in, loading, rate_printed, start_depth_printed_in, measured_channels, evidence (figure
and table ids, semicolon separated, or `text <printed page> (PDF <n>)`), setup_status (complete |
setup_incomplete | pending), mcc_relevant, priority, relation, relation_target, status, notes`.
`bin_printed_in` is the bin or bed as printed, normalized for comparison to `A by B` in inches, or to
`A by B [by C] ft` when the report gives feet (the model-drop bed and the full-scale pit; until 2026-11-19
the unit was dropped and the site read 18 by 12 ft as inches).
`relation` is `same-as | derived-from` or empty and `relation_target` the semicolon-separated ids it
points to (from the Volume II batch on; Section II rows leave them empty). The index is built by
`tools/build_experiments.py` from one or more batches of two blind inventories, stacked in order
(Section II, `experiments-s2-b1`; Volume II Appendix C, `experiments-vol2c-b1`; Volume II Appendices A and B,
`experiments-vol2ab-b1`: grain-size and density charts, friction-angle charts and the sonic moduli; the
chemical analyses of Appendix A are material composition, not experiments, and belong in `data/materials/`;
Volume I Sections IV and V, `experiments-s3s5-b1`: the footpad impact runs with plotted histories and the two
model drops with histories, NASA Tests 1 and 2, D-050; Volume I Section IV, `experiments-drag-b1`: the 13
subscale drag tables, Figs. 4-6a to 4-16, kind `run-table`, D-050; Volume I Section V, `experiments-t5-3-b1`: Table
5-T3, the detail correlation drops of the LM model, kind `run-table`, read in the same blind pass as the table's cells,
2026-11-20); a later batch's row
with an id already in the index (a test or series printed again) merges into the earlier row: its
evidence is added, the earlier cells stand, and the printed facts that differ are noted on the row
and listed in `index.json` (`merged_rows`). Volume II rows keep the `b68` alias with `source_id`
`bendix-1968-vol2`; envelopes are named by their printed Dr range in hundredths
(`b68-ds-fc-1a-dr50-57`) and stresses in psi with `p` for the point (`b68-ds-fc-7b-n27p1psi`). The `*_printed` columns hold the
value exactly as printed beside the test (caption, legend, inset, or the paragraph describing the
figure) and are never inferred from another test; they are index fields for finding and matching
experiments, and `setup.json` is where the reconciled SI setup lives. `kind` is `single` (one
physical test), `averaged-series` (a curve the report says is averaged from several tests),
`derived-series` (a reduction the authors drew from identified tests, such as a failure envelope),
`correlation` (a fit drawn without the underlying points), `summary` (a number that exists only in
the text), `sample` (a bin sample analyzed for grain size and min/max density), `run-table` (a printed table of
separate runs of one test type, one physical test per row: the subscale drag tables of Figs. 4-6a to 4-16, one row
per printed table page, from 2026-11-19, D-050; Table 5-T3, the eight detail correlation drops, one row per soil family
of its beds, `b68-mdrop-t5-3-rs` and `b68-mdrop-t5-3-ss`, from 2026-11-20, because the index and the site group records
by soil family and the table mixes RS and SS beds; its runs are in `runs.csv`, below). A run-table whose runs include
a drop that has its own record (NASA Tests No. 1 and 2, `b68-mdrop-10`, `b68-mdrop-11`) carries `relation` `same-as`
with those ids, so a split keeps them together. The descriptive columns (`apparatus`, `loading`,
`measured_channels` from the first reading, `state_printed` and `test_label_printed` from the second) take a value
from `qa/<batch>/resolutions.csv` when one is recorded there, checked on the page (from 2026-11-20, batch
`experiments-t5-3-b1`). `soil_no_status` is
`reported | inferred | conflict | unknown`; `conflict` marks a test two figures label with
different states (LPT 26 and LPT 27 in Volume I).

`experiment_id` scheme: `<source alias>-<test_type>-<label>`, lower case, hyphens only. The
alias `b68` stands for `bendix-1968-vol1`. The label is the report's own test number when one is
printed (`b68-lpt-027`, `b68-lpt-064A`, `b68-dpt-r53958`, `b68-smp-ssd-4-18`), the normal stress
for a direct shear test (`b68-ds-f2-21-n3520`), or, for series without a printed number, the figure
id plus a sequence number in legend order or the legend label (`b68-lpt-f2-36-s01`,
`b68-dpt-f2-55-rs`). Test types: `gs` grain size, `dens` min/max, compaction and in-place
density, `ds` direct shear, `tx` triaxial, `lpt` static load-penetration, `spt` static
penetrometer, `dpt` dynamic penetrometer, `imp` footpad impact, `drag` footpad drag, `mdrop` 1/6-scale
LM model drop (Section V; id `b68-mdrop-<Bendix drop number>`, D-050; Table 5-T3's drops, a run-table, are
`b68-mdrop-t5-3-<soil family>`), `sonic` sonic
modulus, `smp` bin sample (`gs;dens`). Impact runs are `b68-imp-<run>` (subscale, `b68-imp-ii-1` for run
II-1) and `b68-imp-fs<n>` (full scale).

Per experiment folder:

- `setup.json`: material and state; preparation (placement method, compaction, waiting time, bed
  reuse); geometry (bin dimensions and fill depth, penetrator profile and dimensions, specimen
  dimensions); boundaries (wall and tool materials, applied loads); loading (control, rate history,
  impact velocity, moving mass, drop height, gravity level); measurement (sensor type and location,
  filtering, sampling, zero definition); data meaning per series (measurement markers, recorded
  trace, author fit, computed, derived). Every field is an object `{value, unit, status, source}`
  with `status` in `reported | derived | inferred | unknown` and `source` a page locator.
- `observations.csv`: the points, written by `tools/build_observations.py` from the canonical
  reading that `tools/diff_curves.py` selects (see `docs/CURVE-READING.md`). Columns
  `experiment_id, series_id, panel, point_kind, sequence, x_si, y_si, x_bound_si, y_bound_si,
  x_native, y_native, x_read_bound, y_read_bound, x_unit_native, y_unit_native, pixel_u, pixel_v,
  status, source, note`. `point_kind` in `marker | trace | gridline | feature`; `sequence` is the
  point's number in the reading named by `source` (its drawing order along the trace in that
  reading, never sorted by x); `pixel_u, pixel_v` locate the point on the
  unrotated 300 dpi page image; the bounds are reading bounds, not standard deviations: from
  2026-10-14 (D-025) the largest change of value over the point's pixel interval on the
  piecewise map plus the location error of the two lines around it (before: pixel bound times the
  local scale plus the calibration residual); `status` in `agreed` (the two readings
  matched within the sum of their bounds; for trace samples the other reading is interpolated at
  the canonical sample's displacement) `| resolved` (a page re-read settled a disagreement; the
  decision row says which reading was right) `| one-sided-verified` (only one reading holds the
  point and the other agent verified it on the page image) `| one-sided` (held by one reading,
  not verified by anyone) `| pending-review | confirmed | audited` (from 2026-10-30, roadmap 4c: two
  student reviewers answered `ok` on the point in `qa/audits.csv`, the pair outcome `confirmed` of
  `tools/ingest_review.py`; `audited` when the two readings had agreed on the point, `confirmed` when it
  rested on a rule, a re-read or one reading; the status the readings gave it is kept in the note after
  `audit:`; any other pair outcome is noted and changes nothing; a verdict on a reading a decision has
  since replaced at that sample is noted as superseded and not applied; `tools/build_observations.py
  --audits`); `source` names the reading
  whose value is kept (`<reader>-interp`: a value interpolated on that reader's trace at the
  displacement of the canonical sample numbered `sequence`, where a decision kept the other trace). Points of both readings can be in one series (a marker or a curve end only
  the non-canonical reader recorded), so rows keep the order of the canonical file within a panel
  and series, which is drawing order. The per-point decisions of a batch live in
  `qa/<batch>/decisions-<figure>-p<n>.csv` (the pilot's were renamed to this pattern on 2026-10-14; columns panel,
  series_id, point_kind, sequence, source, status, use, note; no `source` means the canonical
  reading); `use` names the reading whose value replaces the canonical one (`span` instead keeps
  the value and widens its read bounds to take in the other reading's value and bound, for a point
  neither reading could be shown right on, or a peak whose time is a locator on a flat top; 2026-10-27,
  D-030; the widened bound is rounded up, from 2026-11-19), and a row with
  status `excluded` drops the point (for example an interpolation across a visible gap in the
  drawn line, which is an estimate and not a reading). The decision note is appended to the
  point's `note` after ` | decision: `. Decisions from a blind adjudication are written by its apply script from
  the round's answers and key; for a run answered `some`, the off-line samples come from the round's
  `off-lists.csv` (columns item, adjudicator, sample_px, verdict off|on|unclear: the comment transcribed
  sample by sample by two independent readers, diffed), never from the comment text; an `unclear` sample
  stays undecided (D-039).
- `series.json`: the figure and panel the points came from, each panel's quantities with native
  and SI units and the conversion factor used, both readings' calibration residuals and anchor
  counts and, for piecewise maps, `map` (the lines used with their location errors, the lines not
  on the ink, the number of recovered lines), point counts by status and kind, the batch, the
  reading-rules version and the canonical-selection rule. Written per batch by
  `tools/build_batch_records.py <batch>`.
- `runs.csv` and `runs.json` (records of kind `run-table`, written by `tools/build_run_table.py <batch>` from the
  cells two transcriptions agreed on, `qa/<batch>/agreed.csv` of `tools/diff_tables.py`): one row per printed run,
  `experiment_id, run_number`, every printed column in SI (`D_m, d_m, VH_m_s, gp_bar_m_s2, Dr, unit_weight_N_m3,
  FD_N, FV_N, alpha_deg`, the derived `FD_over_d_gamma_Aft` and `VH_over_sqrt_dg` as printed, `FD_over_Aft_Pa`,
  `FV_over_Apt_Pa`, `bulk_density_kg_m3`) and as printed (`D_in, d_in, VH_fps, gp_bar, gamma_pcf, FD_lb, FV_lb,
  FD_over_Aft, FV_over_Apt`, named by their printed unit, an exception to the `*_native` names of
  `observations.csv`; a column kept as printed is not repeated), `status` (`agreed`; `pending-review` where a cell has
  no agreed value or an unreadable digit, kept as `?` in the printed column with its SI cell empty), `check`: the
  row's results outside the printed rounding and the heuristic area flags of the arithmetic check of the derived
  columns (`tools/check_drag_table.py`, `qa/<batch>/arithmetic.md`), and `audit` (from 2026-11-21): the run's cells the
  student reviewers checked, in printed order, as `<printed column> <pair outcome> by <reviewer> (<chunk>)`, empty
  until a cell of the run is audited; the run's `status` stays as the transcriptions left it, since a sample checks a
  few of its cells. `runs.json` `audit` counts the record's cells, the cells sampled and the cells two reviewers
  confirmed. A transcribed number carries the precision of its
  printing (half a unit of its last digit), not a reading bound; the diameters D and depths d are nominal set points,
  taken as exact. `d` is measured from the soil surface to the bottom of the pad at zero pitch (Fig. 4-4), held by
  locking the loading piston; whether the pad's pivot was free or clamped is not stated per run. The units of the two
  pressure columns are not printed (psi is inferred). `runs.json` names the figure, the method, the columns with their
  units and factors, the definitions of the derived columns as printed, and the arithmetic check's summary (the
  common factor between the two pressure columns, the runs flagged). These are the columns of the drag tables
  (`--family drag`, the default). Table 5-T3 (`--family mdrop --soil-family <RS|SS>`, from 2026-11-20) has its own:
  `experiment_id, run_number` (the printed NASA Test No.), `bendix_drop_no`, `same_test_as` (the record of the same
  drop's time histories, a `single` mdrop row labeled with that NASA Test No., or empty), in SI `VV_m_s, Vh_m_s`
  (touchdown velocities, sign as printed), `tau_s` (time from model release to touchdown), `Dr`, `unit_weight_N_m3`,
  `phi_deg`, `bulk_density_kg_m3`, then `soil_printed` and the printed `VV_in_s, Vh_in_s, gamma_pcf`, `status`,
  `check` and `audit`. A column kept as printed (`tau_s`, `Dr`, `phi_deg`) keeps the printed digits, a leading decimal point
  included (`.298`), and a `?` the readers could not read. A row without an agreed Soil stops the build rather than
  fall out of both family records.
- A record from several figures (from 2026-11-19, D-050: the vertical impact runs, whose force and
  displacement against time are Fig. 4-19 and whose force against displacement is Fig. 4-20) numbers
  its panels across the figures: `panel` in `observations.csv` is the record's panel, given per figure
  panel by the `record_panel` column of `qa/<batch>/panel-map.csv`. Its `series.json` adds `figures`
  (the list; `figure_id` is the first), and each panel entry gives its `figure_id` and `figure_panel`
  (the panel number on the printed figure, which audit objects and `qa/<batch>/` files use); the
  calibrations are keyed by figure and panel (`F4-20/cal-p1`). A record's figures are read in one batch. A
  one-figure record whose panel is renumbered names its figure and figure panel the same way (each dynamic
  penetrometer record of Fig. 2-54 is its own panel 1, from the figure's panel 1, 2 or 3).
  A panel entry may carry `relation` (a panel that re-plots another: Fig. 4-20 is derived from Fig. 4-19)
  and `note` (what a user of the panel's values must know, such as a misprinted axis label), both from
  the panel map. A note may hold several sentences, one per line (from batch curves-s5-b1); the record page
  joins the notes of all panels and gives a sentence that several panels share once.
- `series.json` `breaks` (from 2026-11-19, only on records that have one): a drawn line's explicit breaks,
  where the scan has no ink and both readers stopped (the dropout on Fig. 4-20), each with the record
  `panel`, `series_id`, the line samples `after` and `before` it (`source`, `sequence`) and the `reason`.
  Written from the hand-made `qa/<batch>/breaks.csv` (figure_id, figure panel, series_id, after and before
  as `source|sequence`, reason; both must be consecutive trace samples of the series in drawing order;
  optional `gap_u1`, `gap_v1`, `gap_u2`, `gap_v2`, from batch curves-s5-b1: the two ends of the gap, measured
  on the page in pixels). The plots do not draw the line across a break, and the record page names it (the
  reason up to its first semicolon; what follows, such as who found the break, stays on the review page). The
  comparison does not interpolate the other (non-canonical) reading across a break either (from 2026-11-19:
  `tools/reconcile_curves.py` maps the gap's ends on each reading's own calibration and passes the spans to
  `tools/diff_curves.py --break-a`, `--break-b`, or, for a break without pixels, the span between the two
  samples named, `--break`): a sample beside a break is compared directly with the other reading's nearest
  sample on an intact stretch, within both bounds, as at the end of a trace, never through the break. Rows of `observations.csv`
  are in drawing order within a series; `sequence` is each reading's own numbering, not an order. Two rows
  in drawing order may share an x value (two samples read at one time on a steep flank), so x is not strictly
  increasing.

Re-derivation and calibration files of a curve batch (D-025), written by
`tools/reconcile_curves.py <batch>` from the submissions, never edited:
`qa/<batch>/rederived/<reader>/<figure>/points-p<n>-native.csv` (the reader's pixels on its
piecewise map, with `cal_model`) and `cal-p<n>/` (`calibration.json` as submitted, `anchors.csv`
with any recovered line, `knots.json`: per axis the lines used, their tilt, location error and
distances from the ink, and the lines rejected with the reason); `qa/<batch>/calibration-sensitivity.md`
(affine against piecewise values per canonical series); `qa/<batch>/canonical-<figure>-p<n>.csv` and
`qa/<batch>/canonical.csv` (the canonical points: each point's own columns, then `status`, `source`,
`other_x_native`, `other_y_native`, `decision_note`, `other_pixel_u`, `other_pixel_v`; the last two,
added 2026-11-18, give the other reading's place on the page, which audit packets draw). Inputs written by hand:
`qa/<batch>/ink-checks.csv` (written by `tools/check_trace_ink.py`, D-031; columns figure_id, panel,
reader, series_id, point_kind, sequence, pixel_u, pixel_v, verdict `eligible | excluded | review`,
line_ink_px, symbol, reason, image_sha, params) is read by `tools/reconcile_curves.py` by default since
2026-10-30 (D-032): an `excluded` sample of either reading leaves the comparison as a hand exclusion
would, its note starts with `D-031 ink check`, and the diff report lists every hand decision it
overrides; `review` samples stay. Inputs written by hand:
`qa/<batch>/overlays.csv` (optional `cal_a`, `cal_b`: a reading's calibration directory when it is
not `cal-p<n>` next to its points file) and `qa/<batch>/knots.csv` (figure_id, panel, reader,
x_value, y_value, u, v, x_source, y_source, note: a line a reader left out, measured on the page), and
`qa/<batch>/feature-roles.csv` (figure_id, panel, reader, series_id, sequence, submitted_role, role,
reason; from batch curves-s5-b1, 2026-11-19): a feature whose note names its role by another convention
than the batch's (there: a compression panel's peaks and minima named by the curve as drawn instead of
the signed value). `tools/reconcile_curves.py` checks every row against the submissions before writing
anything (known figure, panel and reader; `role` and `submitted_role` two different words of `knee,
minimum`, `knee`, `peak`, `first`, `last`; one row per feature; the submitted note opening with exactly
`submitted_role`) and stops on any failure; it then writes the rederived note as `<role> (role renamed by
qa/<batch>/feature-roles.csv; submitted note: <the note verbatim>)`, so that the two readings pair by role.
The submission is not touched.
`qa/<batch>/panel-map.csv` may carry a `figure_id` column when a batch's figures differ in units.
A calibration of a log or reciprocal axis (D-027) records `x_transform` or `y_transform` (`log10`,
`reciprocal`; absent means linear) in `calibration.json` and `knots.json`; its anchors keep the printed
values, while `ax`, `ay`, the residuals and `x_per_px`, `y_per_px` are in the plotting coordinate
q = T(value). Points are always written in the printed unit; a read bound on such an axis is the larger
half of the interval mapped back from q (the tools count the values whose two halves differ by more
than 10 percent), and the SI conversion applies to the value, never to q.

## Figures index (`corpus/<source>/figures.csv`)

One row per figure or table, built by `tools/build_figures.py` from two blind inventories and a
resolutions file (`qa/<batch>/resolutions.csv`: id, column, value, status, note). Columns:
`id, kind, title_as_printed, printed_page, pdf_page, test_type, soils, states, apparatus,
rate_or_dynamics, data_form, panels, curves, trace_classes, x_quantity, x_unit, x_unit_as_printed,
x_axis_type, y_quantity, y_unit, y_unit_as_printed, y_axis_type, legend_entries, rotation,
in_scope, transcribe, priority, mcc_relevant, status, notes_claude, notes_codex`.

Ids are `F<section>-<n>` and `T<section>-<n>` in Volume I. In Volume II (`corpus/1968-vol2/`)
numbered figures keep the printed number with the appendix letter, `FA-12`, `FC-1B`, and `FB-3`
for the figures numbered 1 to 8 inside the reproduced IITRI report of Appendix B; unnumbered
tables are identified by page locator `TA-pNNN`, NNN the PDF page where the table starts (the
chemical analyses and normative mineral tables of the soil specifications). When the two
submissions used different id schemes, `qa/<batch>/id-aliases.json` maps the first submission's
ids to the canonical ones before the diff; the sidecar records the map.

Volume II adds three columns after `pdf_page` and before `status`: `appendix` (A, B, C) and
`relation`, `relation_target` with vocabulary `same-as | derived-from | reproduces | unresolved |
none` (a reproduction is the same content printed again, as the four figures repeated under each
soil of a material; derived-from points at the figure or table the data came from, across volumes:
F2-14, F2-17, F2-23 and Table 2-3 of Volume I derive from Appendix A and B figures; unresolved is a
plausible but unconfirmed link). One agent's `none` yields to the other's stated relation
(absence is not a reading), status `vocabulary-resolved`.

Volume I Sections III to V (batch `inventory-s3s5-b1`, 2026-11-19, D-050: Section III, Section IV to Fig.
4-22, Section V to Fig. 5-39) are appended to `corpus/1968/figures.csv` after the Section II rows. They add
`section` (III, IV, V) after `pdf_page`, and `relation`, `relation_target` as in Volume II; the Section II rows
leave all three empty. A printed item continued over several scanned pages has one row per page, the first
keeping the printed id and the others `-pNNN` (`T5-2-p309`, the continuation of Table 5-T2; `F5-2-p285`,
the second frame of a foldout); an alias of the form `<id>@<pdf_page>` in `qa/<batch>/id-aliases.json` maps a
submission that repeated an id on several pages. `TABLE 5-T2` is `T5-2`.

The rest of Section V and Section VI (batch `inventory-s6-b1`, 2026-11-20, D-050: Figs. 5-40 to 5-47 and 6-1 to
6-27, PDF 345 to 440) are appended after them, `section` V or VI. Section VI prints its four tables as
numbered figures (Figs. 6-4, 6-6, 6-8, 6-10: kind `figure`, data_form `table`). Each of the eight detail
correlation drops (NASA Drop No. 1 to 8) has a four-sheet figure of measured histories with the report's
computed curves (Figs. 6-11 and 6-13 to 6-19) and a four-sheet figure of computed curves alone at a higher
strut damping (Figs. 6-12 and 6-20 to 6-26), one row per sheet. A history sheet is `same-as` Fig. 6-10, the
table of the eight drops (its drop's NASA and Bendix numbers are in the row's notes), and, for NASA Drops 1 and 2,
the Section V figures of the same channels: `same-as` here means the same test and channel, not the same trace,
since the two printings have not been compared and can differ. The computed-only sheets are `derived-from` Fig.
6-10 and `in_scope` no; Figs. 6-4, 6-6 and 6-8 reprint rows of Table 5-T2 and are `reproduces`, `in_scope` no.
`qa/inventory-s6-b1/corrections.csv` changes cells both readers agreed on, each with its page evidence, as Volume
II's does. The brief of this batch asked for the controlled unit codes, so `*_unit_as_printed` is empty on its rows
(`--unit-codes`; the printed form is in the notes); in any batch a code with an underscore (`in_s`) is never taken
for a printed spelling. A row a correction changed has the status `resolved`.

Vocabularies: `axis_type` in `linear | log |
normalized | reciprocal | n/a` (normalized: a dimensionless quantity on a linear scale; reciprocal:
the 1/gamma scale of the unit weight charts); `unit` in `inch | lb | psf | psi | pcf | g | s | mm |
percent | deg | ksi | none | n/a`, with `ms | ft_s | in_s | in_s2 | deg_s | ustrain` since Sections III to V
(milliseconds, feet and inches per second, inches per second squared, degrees per second, microinches per
inch) and `deg_s2` since Section VI (degrees per second squared, the vehicle pitch acceleration), with the printed spelling kept in `*_as_printed` (an axis
multiplier such as "x 10^-3", "(x 10^1)" or a leading "1,000" belongs to the quantity and is stripped before the
unit is normalized); `test_type` in
`grain size | density | bed preparation | direct shear | triaxial | load penetration | dynamic
penetrometer | drag | impact | model drop | sonic | soil model | soil properties | apparatus | other`
(`model drop`: the 1/6-scale LM model landings of Section V);
`data_form` in `table | curve | schematic | photo | text | mixed`; `trace_classes` from
`measurement-markers | recorded-trace | author-fit | computed | schematic | setup-evidence`.

Three columns carry judgment and follow fixed rules (decided 2026-10-07):

- `in_scope` (`yes | maybe | no`): the item carries numbers to extract into `data/`. `transcribe`
  is `yes` for every page of a section in the transcription scope, so photographs and conceptual
  charts reach the corpus without being "in scope" for extraction.
- `priority`: 1 = needed for the first calibration and prediction protocols (shear family, LPT
  records with known bed state, DPT signatures and correlation, materials tables); 2 = needed to set
  up or interpret those tests (bed preparation, boundary and bin effects, rate series,
  degradation); 3 = context only.
- `mcc_relevant` (`yes | maybe | no`): yes only when the figure shows the same material after
  different loading or handling histories with a different response, plus the state maps needed
  to read those figures; the column answers one question, whether any test demands a
  history-dependent model.

Conventions fixed in the Volume II batch (2026-10-07) and applied from then on: a photograph has
0 panels and 0 curves and priority 3; a plot with an inset table of numbers or printed fit
parameters is `mixed`, a data sheet whose legend lists the test identities is `curve`; a figure or
table that reproduces another is `in_scope` no and priority 3 (the first printing holds the
numbers; the page is still transcribed); a chemical analysis is priority 2 (material identity, not
a simulation input); a normative mineral analysis of a reference rock is not soil data (`in_scope`
no, priority 3); a per-soil summary curve derived from primary figures is priority 2 when the
primaries are 1; a computed curve is `in_scope` no.

Curve-count convention: every drawn line is a trace, including each boundary of a shaded or
bracketed range; markers and the fitted line through them are one response series (range bars on
a marker are part of the marker); construction guides are not counted. Row `status`: `agreed`
(every reconciled cell agreed), `resolved` (some cells settled by a vocabulary rule, a page
re-read, a convention or a scope rule, each recorded in the sidecar), `provisional` (a count or
grade to be re-done at extraction or decided by Dan), `pending-review`, and `one-sided-verified`
for a row that only one submission listed and that entered through `qa/<batch>/row-decisions.csv`
(id, decision, status, note saying how the row was verified against the page image). The sidecar
`figures.json` lists the rules, per-cell statuses with their notes, and the other agent's text
for every descriptive cell that differs.

Known source quirks recorded here because the index is where an agent will meet them: "SS" in a
soil designation is silica sand, but "SS Drag Tests" (Figure 2-60) and the test numbers "SSD" mean
subscale drag; LPT 27 is captioned RS Dense in Figure 2-29 and RS Intermediate in Figure 2-43;
the ordinate of Figure 2-34 is printed "Lbs. x 100" although the ticks and the printed slope are in
pounds; Table 1-1 prints soil 4 at 50.5 pcf where Table 2-3 prints 50.6.

Volume II quirks: the Appendix C computer plots are bound out of order (PDF 147 = C-35, 148 = C-34,
149 = C-33) and Appendix B keeps the IITRI report's own page numbers, both handled by
`corpus/1968-vol2/page-map-corrections.csv`; Figure A-45, captioned "Photomicrograph RSM Soil"
under soil 12 (RSM-b), is the same photograph as A-17 (RSM-a); the Volcalite chemical analysis is
printed seven times with two different typesetting slips (A-72 drops the MgO line and prints 5.58
against CaO; A-81 prints MgO 1.61 and drops Na2O) and the clay analysis twice with iron oxide 1.1
(A-72) against 1.2 (A-81); the computer-fitted envelopes print "Angle of Friction", "Tan Theta" and
"Cohesion" with axes in tens of psf; Figure C-7A to C-7C (RSM-b) are in psi from a different
apparatus; the SS series at Dr .30, .48 and .77 in C-5A and C-20 are credited to Bendix report
MM-65-2 (as printed on C-15), not to this study; the sonic moduli of soils 5, 10 and 12 in Table 2-3 are estimates, not
measurements (A-41, A-79, A-93); the text gives phi for soil 11 as about 38.3 and for soil 12 as
about 37 degrees (A-84, A-93) where Table 2-3 prints 42 and 48; soil 12 was rolled "10 passes per
two inch layer" (A-93) where Volume I printed 2-113 says twenty-four rolls.

## Reading bounds and agreement

A reading bound is a half-width in native units built from: half the visible marker or trace
width; the axis-calibration residual; placement repeatability; extra ambiguity from overlap,
damage or uncertain centering. Bounds are bounds, not standard deviations. Two agents agree on a
matched point when |xA - xB| <= bxA + bxB and |yA - yB| <= byA + byB (in log coordinates on log
axes; on steep curves the x bound is propagated into y). Printed numbers (tables) must agree
exactly after typography normalization. Agreed objects take `status=agreed`; disagreements go to
review and come back `confirmed` or `interval`; a stratified 5 to 10 percent of agreed objects
is audited and marked `audited`. Readings are never averaged; the canonical trace is the one named
by the rule recorded in `series.json`.

### Reviewer audits (`qa/audits.csv` and `qa/audits/`)

`qa/audits.csv` holds one row per reviewer and point actually checked by a person: `batch`,
`object` (`<figure_id>/<panel>/<series_id>/<point_kind>/<source>/<sequence>`: `sequence` numbers the points of the reading named in `source`, so an audit stays with its point when a re-reconciliation changes the canonical reading), `column` (`position` for a
curve sample or compare row, `position+identity` for a symbol, `position` for a symbol whose identity
answer is listed in `qa/audits/voided.csv` for that chunk, `position+value` for a cell of a transcribed table,
whose object is `<table>/1/<column>/cell/agreed/<row key>`, since 2026-11-21, D-050), `auditor` (initials), `date`,
`outcome` (`ok | problem | cannot tell | unreadable`), `note` (starts with the chunk and the
reviewer's letter, `chunk W1-07 (R1-D)`, then the reviewer's comment). The file is append-only
and never holds the same object and auditor twice; a point's pair outcome (confirmed, flagged,
split for ok against problem, cannot-tell, a mix such as `ok + cannot tell` where the definite answers agree,
single) is computed from all its rows when a report is made, never stored (`tools/ingest_review.py`, `pair_outcome`).

The audit in brief. Each wave samples points of figures already read: every compare row (up to a cap), every
resolved or unverified one-sided point, some verified one-sided points, and agreed points in a number that grows with
the square root of the figure's point count. The sample is cut into chunks of about 60 rows, and each chunk is checked
against the scan by two reviewers, or by one in a second-review chunk that completes an earlier chunk; the first audit of
the grain-size curves and of the newest test families has one reviewer per chunk, their second reviews following in a
later release (D-050). Every chunk also
carries seeded attention checks whose answers are known; a return that misses one is not recorded unless the
maintainers accept it, and one they decline is never recorded, its points going to another reviewer. An answer a
reviewer could not give fairly (for example on a figure the packet showed upside down) is voided in
`qa/audits/voided.csv` and asked again. A point two reviewers answered ok becomes `audited` or `confirmed`; every other
outcome is noted on the point. The blind adjudication on the scan (D-023) takes every point with two or more reviews
that is not confirmed, and every point a single reviewer marked as a problem; a point with one review that is not a
problem waits for its second review.
The program's manual (`docs/audit/README.md`), its packet tool and its answer keys stay out of the public release while
the audit runs. In the maintainers' repository the
files under `qa/audits/` and their columns are listed in that manual, among them the reviewer's `left` date in
`reviewers.csv`, the `repeats` column of `assignments.csv` (a second-review chunk, one reviewer,
D-037) and the controls vocabulary of `returns-log.csv` (`passed | accepted | missed |
declined`). `qa/<batch>/audit-meta.json` carries, per figure, the
series labels and symbols, panel names and axis types, rotation, the legend hint and the notes a
reviewer sees in `about-the-figures.txt`; it is drafted by the packet tool from the batch's maps
and the figures index and then edited by hand. A table batch (one with `agreed.csv` and no `canonical.csv`) has a
hand-written `audit-meta.json` (kind `table`: the page image, its rotation, the key column, every printed column with
its heading, aliases by which the readers' notes name a column, and the arithmetic checks and verdicts that flag a
column, `check_columns` and `flag_verdicts`) and
`qa/<batch>/cell-layout.csv`, written by `tools/locate_table_cells.py`: one row per box (`figure_id`, `key`,
`column`, `role` cell, key or header, `x0 y0 x1 y1` in the upright, straightened frame, `u v` the center on the scan,
`bu bv` half its size there, `deskew_deg`), so a packet can show a reviewer the cell, its row key and its column
heading.

### Typography rule for text cells

When two readings of a text cell differ only by a hyphen or a space at a printed line break (for
example "Wedron 4040 narrowly graded" against "Wedron 4040-narrowly graded"), the canonical text
keeps the printed hyphen and drops the wrap space, the cell is marked `typography-resolved`, and
it is included in the audit sample so a person confirms the rule did the right thing. Any other
text difference is a disagreement for review.

### Cell and row status vocabulary

Cell statuses, recorded in the sidecar: `agreed` (identical after typography normalization),
`typography-resolved` (rule above), `uncertain` (identical readings, but both agents flagged the
glyph; goes to review), `pending-review` (readings differ; the cell is left empty in `data/`),
`confirmed` (a person settled it against the scan), `interval` (the scan does not support one
value; bounds given). Row status: `agreed` when every cell is agreed; `resolved-with-notes` when
some cells are typography-resolved or uncertain; `partial` when any cell is pending review.

## Corpus pages (`corpus/<source>/pages/pNNNN.md`)

Transcribed under `docs/PAGE-TRANSCRIPTION.md`: two agents type the page from its 300 dpi image,
`tools/diff_pages.py` compares the two, differences are settled by a page re-read recorded in
`qa/<batch>/decisions.csv` (page, diff_id, use, note), and the canonical page is written from the
first submission with the decisions applied. The header carries `review_status` (`agreed`,
`resolved`, `pending`), both `transcribers`, the `batch` and the number of `differences`.

YAML header: `source, pdf_page, printed_label, section, figures, tables, rotation,
review_status (agreed | confirmed | pending), image`. Body: the page text as Markdown with LaTeX
math; tables as Markdown tables; per figure a block with `caption`, `axes` (label and unit
verbatim per axis), `legend`, `description`. Curve values are never in page files.

### Corpus indexes (`corpus/<source>/{contents,equations,symbols,glossary}.csv`)

Built from the page files by `tools/build_indexes.py` (deterministic; `--check` compares a fresh
build with the committed files). Every row carries `source`, `pdf_page`, `printed_page` and the
page's `review_status`, so a row is as trustworthy as the page it came from.

- `contents.csv`: `section, title, level` per printed heading (section numbers as printed; an
  unnumbered appendix title carries its letter). Inside an appendix, a section lettered on the
  page is prefixed with the appendix letter (`B/C` is section C, RESULTS, of the IITRI report
  reproduced as Appendix B, not Appendix C), and each Appendix A soil sheet is `A/soil n`.
  A page with no printed number has `printed_page` empty (the cover and title pages of the IITRI
  report); `unknown` is not used, because the absence is known.
- `equations.csv`: `number, latex, context` per display equation; `number` is the printed number
  beside it or empty; `context` is the end of the sentence that introduces it. Printed duplicates
  stay (Vol. I Section II numbers two different equations 3-1, printed 2-40 and 2-60).
- `symbols.csv`: `symbol, meaning, units, equation` per entry of a printed "where" list
  (`X = meaning`, or `X is the meaning` as in Appendix B); `equation` is the numbered equation the
  list follows, when there is one.
- `glossary.csv`: `term, definition` from the report's own list of abbreviations (Vol. I 2.1.1);
  a definition printed without its term keeps `term` empty (the "Dense" entry on printed 2-2).

## Insights (`insights/`)

One Markdown file per theme (for example `soil-selection.md`, `bed-preparation.md`,
`dpt-as-density-proxy.md`). Each paragraph ends with its citation in the form above. These capture
judgment and recommendations, not numbers.

## Site (`site/`)

A Quarto website generated from the repository by `tools/build_site.py` (decided 2026-10-07,
D-012 to D-014 in `docs/decisions.csv`). Rules:

1. Every page is a generated view; no fact is typed into a page. Each page ends with a note naming
   its inputs and the regeneration command. The generated `.qmd` files are committed so that a
   change in what the site says appears in `git diff` beside the data change that caused it.
2. The generator is deterministic (sorted keys, fixed formatting, LF, UTF-8) and writes nothing
   time- or commit-dependent into a page body. `python tools/build_site.py --check` regenerates
   into a temporary directory and compares byte for byte with `site/`; any difference, or any
   `.qmd` under `site/` the script did not write, fails. Hand edits cannot survive a build.
3. `tools/render_site.py` regenerates, writes the render-time footer (`site/_footer.html`:
   repository revision, dirty flag, render date) and the recent-changes list (`site/_changes.md`
   from `git log`), both ignored by git, then runs `quarto render site` (or `--preview`).
   `site/_site/` and `site/.quarto/` are build outputs and are not tracked. Do not leave
   `--preview` running while `build_site.py` rewrites the sources: on 2026-11-19 it rendered
   changed pages beside their sources (193 stray files under `site/`); to look at the site, render
   and serve `site/_site/` as static files.

   After every change that affects pages, the rendered pages are visited before the work is called
   done (2026-11-19, Dan): `python tools/check_site_layout.py --shots` loads every page in headless
   Edge at 1280 px and 390 px and reports any table that crosses the "On this page" column, reaches
   past the text column, is wider than the column without a scrolling box, or squeezes a cell to
   six lines or more; it exits 1 on any of these, and its screenshots of one page of each kind
   (`work/site-check/shots/`) are looked at by eye. Every table goes in a box that scrolls sideways
   (`site/table-wrap.lua`, a Pandoc filter, so the pages copied from `docs/` are covered too; Quarto's
   listing tables scroll by `site/site.css`), and the same filter sets each table's column widths from
   its content, the same in every browser (from 2026-11-20, on Dan's look at the Materials page: left to
   the browser, a short column could be as wide as a text column and the last column squeezed): a
   column's share is its preferred width in characters (its longest cell, capped at 28 so long text
   wraps, never less than its longest unbreakable piece), and the table is as wide as the text column,
   or wider, scrolling in its box, when the columns do not fit side by side at their least widths (the
   longest unbreakable piece; on a phone also 20 characters for a column of longer text, so it scrolls
   rather than wrapping a text column to a word per line). Pandoc's
   equal widths from the dashes of a pipe table stay off (`tbl-colwidths: false`); the virtual
   experiment card keeps its own widths. A long code with no spaces gets line-break opportunities
   after `_`, `;` and `,` (`table()` in `tools/build_site.py`).
4. Every factual display carries its provenance and a status; missing values are written as
   `not reported`, `not yet extracted`, `unreadable`, `conflicting evidence` or `not applicable`,
   never as a blank or a zero; counts that measure different things (indexed records, single
   tests, complete setups, extracted series, recorded audits) are shown separately.
5. Record pages are written for a user of the data and carry only what that user needs: a
   descriptive title, a one-paragraph summary, one note on trust and completeness, the data (plot
   in SI units with the other tests of the figure in gray, downloads, a reading-bounds line, a link to the scan check on the
   figures page), the reproduce table (value, as printed, where; fields per test type; persistent
   ambiguities stated and labeled as our observation), the family, the source pages and the
   citation. From 2026-11-20 (Dan): the line says "reading bounds" (our reading of the figure, not
   the test's uncertainty), a dimensionless value is written without a unit (a percent stored as a
   fraction in percent), and gravity is the report's value for Earth, 32.2 ft/s^2 (9.81456 m/s^2; glossary, printed 2-2, PDF 27; until 2026-11-20 the pages said, wrongly, that the report does not state it). From 2026-11-21 (Dan): every record plot is drawn as the pilot's was
   (`tools/figures/plot_observations.py --readable`): values with an SI prefix that keeps the tick labels short (mm,
   kPa, MPa for a modulus, kN/m^3), a long axis title wrapped onto two lines, the title in words, and no caption baked
   into the image, since the page's caption says what the markers and error bars mean. Everything written for the maintainers (index-row reconciliation, point status counts,
   calibration residuals, the agents' notes, audit status) is on the record's provenance page
   `review/<record>.qmd`, linked from the record page (D-019, 2026-10-08).
6. `docs/decisions.csv` (id, date, question, options, decision, who, note) is the decision log;
   an empty `decision` means the question is open. Ids are stable (`D-001`, ...). The public release
   carries a curated log under the same ids, with the columns id, date, question, options and decision
   (D-052): `docs/decisions-public.csv` (id, publish, question, options, decision) holds one row per
   decision, `publish` either `as-is` (the other fields empty) or `edited`, and for an edited one every
   field given: its public text, or `=` to keep the original; `tools/make_public_release.py` builds the
   log from it and refuses a decision with no row, a doubled id, a row of the wrong width, or an edited
   row with an empty field. Edited decisions leave out the people and the logistics of
   the review.
7. Reader-facing pages (plan v3 Part A, approved 2026-11-05) are written for people at the level
   of a junior mechanical engineering undergraduate: impersonal and timeless wording, no internal
   words. Every code (soil, test, symbol) carries its definition: a span of class `term` with the
   definition as its title, shown on hover and, through `tabindex`, on tap or keyboard focus
   (`term()` in the generator). The build fails (`undefined_terms()`, A2.3) when a page of
   `PILOT_PAGES` has a definition span whose text is not a code of `TERMS` or whose title is not
   that code's definition, or uses a code whose first use, in reading order over the title, the
   subtitle and the body (link text and image descriptions included; code spans, link targets,
   attributes and comments left out), is neither a definition span nor written in parentheses
   after its plain name (`define()`: "red scoria (RS)").

Navigation (plan v3, A5.1): Find a test (`experiments/`), Soils (`materials/`), Simulate a test
(`simulate/`), Glossary (`glossary/`), Download (`downloads/`), About (`about/`), plus search. The
footer links About, Contribute (`contribute/`) and Project records (`records/`). Project records
holds the maintainers' material, public but off the reader's path: decisions, review, open
questions, methods, insights, figures and sources (and the roadmap on the maintainers' own build; the
public release leaves it out, D-052), with the coverage matrix, the five counts,
the open decisions and the recent changes that the first build's overview carried. The landing
page (`index.qmd`) carries the approved wording, a counts line generated from the data and the
soils by code and name.

The record pages are being moved to a template built around the virtual experiment card (below).
During the pilot only `PILOT_RECORD` (`b68-lpt-024`) uses it; the other record pages keep the
template of rule 5 until the pilot is approved, then all move.

### Virtual experiment card

The card of a test lists what one would need to set up the same test in a simulator (plan v3, A3).
It is organized in groups that fit a tool test and will also fit a vehicle on terrain, so a later
kind of test fills the same groups rather than starting a new format:

| Group | Shown as | Holds, for a tool test | For a vehicle test (later) |
|---|---|---|---|
| `terrain` | Soil | the soil, its state in the test, reference properties of the soil | the same |
| `domain` | Bed | container size, the container itself, how the bed was prepared | test course, its preparation |
| `body` | Tool | tool shape and size, how it is driven | chassis, mass properties, wheels or tracks, tires, suspension |
| `motion` | Motion | start depth, rate, extent of the record | speed, slip, steering, driver inputs |
| `environment` | Environment | gravity, laboratory or field | the same (Earth or Moon) |
| `measured` | Measured | what was recorded, with which instrument | the same |
| `choices` | Missing: choices left to the user | each input the report does not give, with what it says around it | the same |

Every entry is a triple (kind, text, where printed). `kind` is one of three, shown with a visible
tag: `test` (reported: given by the report for this test or its apparatus, or for the procedure of
these tests in general, which the text then says), `ref` (soil reference: a property of the soil
from another table of the report, for the soil's nominal state; Codex, 2026-11-05: a nominal density
at one relative density must not read as the measured state of a bed at another), `choice` (left to
the user: an input the report does not give, with what it says around it). An empty group is shown
as *not given*, never dropped. `where printed` gives the figure, table or section with the printed
and the PDF page, as a link to the page image (`page_link()`; the images come from
`tools/render_pages.py` into the thumbnail cache, and `copy_thumbs()` reports any that is missing).
A figure is cited for a value only when it prints that value for this test: `printed_in()` looks
first in the legend entry that names the test, then anywhere on the page, and leaves the citation
empty when no page prints it. The card is built by `card_lpt()` in `tools/build_site.py` from the
index row, the soil table, the figures index, the record's points, the page transcriptions and the
report's density chart of the soil (`DENSITY_CHART`); `setup.json` (Experiments, above) will carry
the same groups and kinds, as typed values with units, when it is written.

## Regeneration

`tools/render_pages.py <pdf> <out_dir> --dpi 300` renders pages (Ghostscript). `tools/page_map.py`
builds the page map, overlaying `page-map-corrections.csv` (pdf_page, printed_label, note: labels
read from the page image where OCR and inference both fail) when that file sits next to the
output. `tools/build_figures.py` rebuilds `figures.csv` from the two inventory submissions and
the resolutions file; Volume II adds `--aliases`, `--row-decisions`, `--batch inventory-vol2-b1`
and `--source`. Volume I is built in three steps, so no build reads its own output: Section II into
`qa/inventory-s2-b1/figures.csv` (the four positional arguments), then Sections III to V into
`qa/inventory-s3s5-b1/figures.csv` with `--base qa/inventory-s2-b1/figures.csv --aliases --row-decisions --batch
inventory-s3s5-b1 --codex-model "gpt-6.2-sol high" --source`, then the rest of Section V and Section VI into
`corpus/1968/figures.csv` with `--base qa/inventory-s3s5-b1/figures.csv --batch inventory-s6-b1 --codex-model
"gpt-6.2-sol high" --corrections qa/inventory-s6-b1/corrections.csv --unit-codes --source` (the exact arguments of each step are in its sidecar's `submissions`,
`resolutions` and `source`, the earlier steps nested under `base`). `tools/promote_leads.py` rebuilds the screened rows of `sources/register.csv`.
Each tool is deterministic: rebuilding from the same inputs reproduces the committed file byte
for byte, which is checked before a commit. `tools/build_indexes.py` rebuilds `contents.csv`,
`symbols.csv`, `equations.csv` and `glossary.csv` from the page files. Everything under `data/derived/` is rebuilt by the script
named in its sidecar.
