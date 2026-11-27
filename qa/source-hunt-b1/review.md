# Review: broadened source hunt, batch source-hunt-b1 (2026-10-07)

Two independent hunts for public-domain or clearly licensed granular soil test records usable
for simulator validation, Apollo era to today. Claude: 38 leads, 26 searches (web search from
the Claude Code session). Codex: 38 leads, 69 searches (gpt-6-astra, high, read-only with live
web search, 27 min, thread 01a117ad-461a-78e2-842a-1e237db8381a). Merged by
`tools/merge_leads.py` with the hand-made match list `matches.json` into `sources/leads.csv`
(64 leads) and `sources/searches-log.csv` (95 searches, 11 of Codex's and 4 of Claude's
recorded as finding nothing useful).

One filing error on Claude's side (an unquoted comma in a title) was corrected in the
submission file before merging; it was a CSV formatting slip, not a reading.

## Overlap and complementarity

Twelve leads were found by both: the Apollo 15 and 16 self-recording penetrometer bundles on
PDS, NASA TN D-4711 (Langley LM gear impacts on sand), the Langley penetrometer TNs, WES
M-70-2, TN D-6850, the JSC-1A LASP geotechnical report, Oravec 2010 (GRC-1), Dewoolkar 2018
(GRC-3), Zeng 2010 (JSC-1A), the reduced-gravity cone index paper (Daca 2022), and the 2026
open lunar regolith database (Gasteiner, Murdoch, D'Angelo). Agreement on the top items is a
good sign that the obvious veins are covered.

Claude alone found: the Berkeley CR-121047 volumes on NTRS, the Apollo S-200 final report
(CR-134306), Carrier's 1973 vacuum shear and oedometer tests on Apollo 12 soil, WES M-71-10
reports 1 and 2 (Boeing LRV wheels in a basalt simulant, with bevameter and cone index), the
Surveyor surface sampler report (Roberson and Scott 1969), Costes 1971 reduced-gravity cone
tests, USGS PP 1389 (Viking), the Exolith LHS-1 and LMS-1 open-access shear papers, EAC-1A,
the Kruger bevameter thesis at Pretoria, the USBM vacuum shear report RI 7814, the Lunar
Sourcebook crosswalk, and the Lunokhod summaries.

Codex alone found: the DesignSafe LEAP-2020 raw cyclic triaxial and direct simple shear tests
on Ottawa sand (open license, machine-readable), Joshi 2026 (CC BY static characterization of
several simulants, raw data offered on request), Dotson 2024 (open, cohesion and shear of
compacted simulants), Kim 2021 (open-access bevameter paper, data withheld), WES TR 3-652
(1964, strength-density relations of an air-dry sand, the classic Yuma sand series), WES
M-70-4 (summary of M-70-2), Kleinhenz 2012 (ISRU vacuum soil bin preparation), Rame 2009
(JSC-1A flowability TM), Costes 1972 TR R-401 (LRV mobility), the Luna 16 and Lunokhod 1 soil
mechanics TM, Spencer 1967 (Surveyor footpad penetration depth), ERDC 2022 automatic dynamic
cone penetrometer validation, a 2025 Zenodo granular intrusion dataset, three NASA Glenn
wheel-test TMs, the 2024 simulant user's guide, FJS-1, CAS-1 and KLS-1 papers.

## Grade disagreements on shared leads (nine, none about identity)

| lead | column | claude | codex | resolution for now |
|---|---|---|---|---|
| arslan-2007 (JSC-1A LASP report) | data_form; setup | tables; medium | curves; high | both kept in the row; settle when the PDF is screened |
| oravec-2010 (GRC-1) | setup; priority | high; 1 | medium; 2 | priority 1 kept (lower number wins until screened); note that the paper is paywalled and a NASA TM version is the target |
| daca-2022 (reduced-g cone) | setup; priority | high; 1 | medium; 2 | priority 1 kept; rare reduced-gravity data |
| gasteiner-2026 (open database) | setup; priority | n/a; 1 | low; 3 | priority 1 kept, but as a crosswalk and citation, not as a data source: it is parameters only |
| rogers-1972 (TN D-6850) | priority | 2 | 3 | 2 kept; lineage document |

Rule applied by the merge: the lower priority number and the stricter rights reading stand
until the source is screened; both agents' grades stay in the row.

## What both hunts say about the landscape

1. **Machine-readable measurements exist but are rare.** The Apollo 15 and 16 penetrometer
   bundles (PDS) and the DesignSafe LEAP-2020 sand tests are the counterexamples; everything
   else is PDF tables and curves. Neither agent found a publicly downloadable, clearly licensed
   collection of complete simulant shear or triaxial histories. That is a search outcome, not
   proof of absence, and it is the gap this project would fill.
2. **The dense public-domain veins are NASA and WES reports of 1964 to 1973** (Bendix, Langley,
   WES mobility series, Berkeley, JPL Surveyor, MSFC) and modern NASA TMs. Modern university
   simulant papers are mostly paywalled; a few are CC BY (Joshi 2026, Dotson 2024, the Exolith
   shear papers, EAC-1A).
3. **A parameters database already exists** (Gasteiner, Murdoch, D'Angelo 2026, CC BY, with a
   query interface). The raw-record collection planned here is complementary; it should cite
   and cross-link that database rather than duplicate it.
4. **Still unlocated:** Bendix MM-67-2 and AM-68-3 (Smithsonian Bellcomm collection remains the
   lead), Berkeley CR-102963, JPL TM 33-443.

## Acquire first (agreed by both where marked)

1. Apollo 16 and 15 LSRP bundles on PDS (both agents): machine-readable, public domain, with
   the original microfilm records and instrument documentation.
2. NASA TN D-4711 (both agents): the only other Apollo-era footpad impact data set, on two
   quartz sands with a full-scale pad; direct companion to the Bendix impact tests.
3. WES M-70-2, M-70-4 and M-71-10 reports 1 and 2 (Claude; Codex found M-70-2 and M-70-4):
   wheel tests with cone index and bevameter characterization of a basalt simulant and Yuma sand.
4. Joshi 2026 (Codex): CC BY, several simulants, explicit shear and compression methods; ask the
   authors for the raw records they offer.
5. Berkeley CR-121047 volumes and the S-200 final report (Claude): the Apollo-era soil mechanics
   synthesis with simulant test data.
6. The JSC-1A LASP report (both): the one NASA-hosted geotechnical report on a modern simulant.

## Next actions

Screen the priority-1 leads (23) one by one: open the document, confirm the rights statement,
record page ranges of data, and promote to `sources/register.csv` with status `located` or
`acquired`. Record dead ends in the register too.
