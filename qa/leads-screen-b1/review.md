# Review: screening of the 23 priority-1 leads (batch leads-screen-b1)

Date 2026-10-07. Screener: Codex (gpt-6-astra, high, read-only, live web search), 869 s. Submission:
`extractions/codex/leads-screen-b1/` (prompt, answer, `screened.csv`, `visited.csv`, meta). This was a
single-agent step, not a blind pair: the screen reads archive records and PDF text layers, and
Claude's role was to verify a sample of the identity corrections against the archive, then promote the
rows into `sources/register.csv` with `tools/promote_leads.py`.

## Verdicts

| verdict | count | leads |
|---|---:|---|
| acquire | 2 | wes-m71-10-rpt1, wes-m71-10-rpt2 |
| acquire-with-caveat | 13 | wes-1970-m70-4, apollo15-pds-lsrp, apollo16-pds-lsrp, berkeley-cr-121047-vols, apollo-s200-final-1974, arslan-2007-lasp105525, rame-2009-jsc1a, kleinhenz-2012-vacuum, kim-2021-bevameter, leap2020-gwu-sand, dotson-2024-shear, gasteiner-2026-database, joshi-2026-static |
| lead-only | 8 | wes-1964-3-652, mccarty-1968-d4711, surveyor-smss-1969, wes-1970-m70-2, costes-1971-cone-gravity, oravec-2010-grc1, berney-2022-dcp, daca-2022-reducedg |

`lead-only` means the screen could not open the document (fetch size limit, 403, timeout), not that
the document lacks data; Codex says so in its header. These nine need a download by other means
(a browser session, interlibrary loan) before they can be graded.

## Identity corrections Codex made, and Claude's check

1. `wes-m71-10-rpt2`: the lead pointed at NTRS 19720007590, which is C. H. Mullis, "A study and analysis
   of the MSFC lunar roving vehicle dust profile test program" (CR-121075). The WES Report 2 is NTRS
   19730004536 (M-71-10 Report 2, CR-129612, Melzer, Dec 1971). Verified on both NTRS records. Credit Codex.
2. `surveyor-smss-1969`: NTRS 19690074497 is "Surveyor 3 Preliminary Science Results" (JPL-PD-125,
   CR-106136, May 1967), not a 1969 report. Verified. Credit Codex.
3. `berkeley-cr-121047-vols`: NTRS 19720006172 is Volume 4 (CR-121044, fluid conductivity), not part of
   CR-121047, which is Volume 1 at 19720006162. Verified. Credit Codex.
4. `costes-1971-cone-gravity`: the lead title was a paraphrase; the publication title is "Cone penetration
   resistance test: an approach to evaluating in-place strength and packing characteristics of lunar
   soils". Not independently verified (NTRS record has no download).
5. `apollo15-pds-lsrp`: Codex reported six TAB files in the data directory; Claude listed the directory
   and found the same six (stations 011 to 016). Verified.

## What was promoted

All 23 rows entered `sources/register.csv` with status `located` (identity confirmed, file not in hand).
The screening verdict, setup recoverability and text-layer assessment are in the `notes` column, the
rights statement as quoted plus Codex's assessment in `rights_evidence`, and the measured quantities,
data form and data pages in `holds`. Status moves to `acquired` only when a file is downloaded and
checksummed; the two `acquire` verdicts and the PDS bundles are the obvious first downloads.

## Caveats carried forward

1. Rights: NTRS "Work of the US Gov. Public Use Permitted" was quoted for the government reports; the
   JSC-hosted LASP report, the Elsevier and Concordia items and the French data repository (Etalab 2.0)
   need a rights decision before any number from them is redistributed.
2. Codex could not render page images, so every figure reference in `screened.csv` is a locator, not a
   visual confirmation that the curve exists as described.
3. The Apollo 15 and 16 PDS tables are hand transcriptions from microfilm with corrections documented in
   the archive; the in situ density and operator-controlled rate are uncertain (Codex's caveat, carried
   into the register notes).
