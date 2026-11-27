# Task: screen the priority-1 leads in sources/leads.csv

You are Codex, working with Claude as colleagues for Dan. This is a delegated task, not a blind
comparison: Claude will take your result as input, verify a sample, and promote screened leads
into `sources/register.csv`. Use web search (enabled for this run). No em-dashes or en-dashes.

## What to do

For every row in `sources/leads.csv` with `priority` = 1 (23 rows), open the document or its
landing page and record what you actually see. Do not infer from memory; if a page does not load
or a PDF is behind a login, say so. For each lead:

1. Confirm the identity: exact title, authors, year, report number(s) or DOI, the URL you used.
2. Rights: quote the rights or license statement you found (for NTRS: the "Distribution" and
   determination fields such as "Public Use Permitted"; for DTIC: the distribution statement; for
   journals: the license line; for PDS: the archive's statement). If none is visible, write
   `no statement found` and where you looked.
3. Data: which pages or sections hold measurements (tables or curves), what quantities are
   measured, how many tests or series roughly, and whether the setup (material, density,
   geometry, loading rate or velocity, boundary conditions, gravity) is described well enough to
   reproduce the test in a simulator. Grade `data_form` (raw | tables | curves | parameters-only
   | none) and `setup_recoverability` (high | medium | low) from what you saw, not from the lead's
   earlier grade.
4. File: direct download URL of the PDF or data bundle, approximate size or page count, and
   whether the text layer is usable (sample a page if you can).
5. Verdict: `acquire` (public domain or open license, measurements present), `acquire-with-caveat`
   (say which caveat: rights unclear, parameters only, incomplete setup), `lead-only` (restricted
   or no measurements), `dead-end` (does not exist, wrong identity, unreachable).

## Output

A fenced ```csv block `screened` with columns:
`lead_id,confirmed_title,confirmed_authors,confirmed_year,report_or_doi,url_used,download_url,pages_or_size,rights_statement_quoted,rights_assessment,data_pages,quantities_measured,approx_tests,data_form,setup_recoverability,text_layer,verdict,notes`
with one row per priority-1 lead (23 rows; include a row even for a dead end). Quote every field
that contains a comma. Then a short section: the five you would acquire first and why, any lead
whose identity differs from what `leads.csv` says, and any new document you ran into on the way
that belongs in the register (list it with URL; do not add it to the CSV).

Context: `sources/register.csv` (already acquired: the two Bendix volumes), `sources/leads.csv`,
`qa/source-hunt-b1/review.md` (what the hunt concluded). Record every URL you visited in a final
fenced ```csv block `visited` with columns `lead_id,url,outcome`.
