# Task: a broad hunt for public-domain granular soil test records usable for simulator validation

You are Codex, working with Claude as colleagues for Dan. Claude runs the same hunt
independently; the two registers are merged afterwards and every lead is graded by both. Use web
search (it is enabled for this run). Record dead ends as carefully as finds: a search that returned
nothing is information.

## Purpose

Dan is building a public, machine-readable collection of soil test records (load penetration,
direct shear, triaxial, cone and dynamic penetrometer, bevameter plate sinkage and shear ring,
footpad impact and drag, wheel and plate tests where setup is complete) with full provenance, in
SI, to validate continuum and discrete granular simulators (Project Chrono first). The pilot is the
1968 Bendix LM Soil Mechanics Study (NASA CR-92208 and CR-92215, already in
`sources/register.csv`; read it so you do not re-register what is there). The question now is
what else exists in the public domain or under a clear license, from the Apollo era to today.

## Scope and eligibility

1. Rights: US Government work, NASA or Army public-release reports, or an explicit open license
   (CC BY, CC0, or a journal's open data statement). Paywalled journal articles are leads only
   (grade rights `restricted`); their data may still be worth asking the authors for.
2. Data form: measurements, not only fitted parameters. Tables of readings or raw curves rank
   highest; curves in figures next; a paper that reports only phi and c is `parameters-only`.
3. Setup recoverability: can someone reproduce the test in a simulator from what is published
   (material gradation and density, specimen or bin geometry, tool geometry, loading rate or
   velocity, boundary conditions, gravity)? Grade `high`, `medium`, `low`, `unknown`.
4. Materials: lunar and planetary simulants (JSC-1, JSC-1A, GRC-1, GRC-3, LHS-1, LMS-1, MGS-1,
   FJS-1, NU-LHT, OB-1, CAS-1 and others), Apollo returned soil mechanics (penetrometer, oedometer,
   direct shear on returned samples), Surveyor and Luna in situ soil mechanics, terrestrial analog
   sands used in lander and rover footpad or wheel studies (Ottawa sand, Wedron silica, dune
   sands), and classic terramechanics datasets (WES mobility and bevameter series, Bekker-era
   plate sinkage) when the setup is recoverable.
5. Lineage of the Bendix work: Bendix MM-67-2 and AM-68-3, JPL TM 33-443, Berkeley lunar surface
   engineering reports (NASA CR-102963, CR-121047 and the Mitchell series), WES reports in the
   M-71-10 series, Grumman and Langley LM footpad drop tests, Apollo lunar module landing dynamics
   reports with soil data.

## Routes to search

NTRS (ntrs.nasa.gov, with the "Public Use Permitted" filter in mind), DTIC (apps.dtic.mil),
HathiTrust full view, USACE ERDC digital library, the Smithsonian archives (Bellcomm collection),
NASA Technical Reports by report number, Google Scholar for data statements, Zenodo and
Dataverse, the Journal of Terramechanics, ASCE Journal of Aerospace Engineering, Icarus and PSJ
open-data sections. Try both report numbers and natural phrases; record the exact query and the
archive for each search.

## What to produce

1. A fenced ```csv block `leads` with columns:
   `lead_id,title,authors,year,report_or_doi,archive,url,rights_assessment,rights_evidence,test_types,materials,data_form,setup_recoverability,gravity_condition,relation_to_bendix,priority,notes`
   where `rights_assessment` is `public_domain | open_license | restricted | unknown`,
   `data_form` is `tables | curves | raw | parameters-only | unknown`, `gravity_condition` is
   `1g | reduced-g | lunar in situ | not applicable`, `priority` is 1 to 3 for acquisition, and
   `lead_id` is a short slug (for example `mitchell-1972-cr-121047`). Aim for breadth: 25 to 60
   leads, each with a URL you actually visited or a report number you confirmed exists. Do not
   invent report numbers; if you cannot confirm one, say so in notes.
2. A fenced ```csv block `searches` with columns `archive,query,date,result_count,useful,notes`,
   one row per search, including the ones that found nothing.
3. A short section of observations: where the dense veins are, what does not seem to exist (for
   example machine-readable shear data on any simulant), and three leads you would acquire first
   and why. Cite URLs. No em-dashes or en-dashes.
