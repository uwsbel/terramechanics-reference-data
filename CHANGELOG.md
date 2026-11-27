# Changelog

Each release is a fixed snapshot. Values can change between releases (a re-reading, an adjudication
or an audit can correct a point); every change is listed here with the decision or review that made
it, and `docs/decisions.csv` holds the decisions themselves.

## 1.0.0 (2026-11-27, first public release)

The first public release, DOI 10.5281/zenodo.24477009. It is a first step and not a finished product
(`docs/OPEN-QUESTIONS.md`). The preview 0.1.0 planned earlier was not published (D-052); data and review
status were frozen on the morning of 2026-11-27 (D-058).

1. **Source:** the Bendix "Lunar Module (LM) Soil Mechanics Study" (NASA, 1968, AM-68-1). Volume I
   Section II and Volume II Appendices A to C are transcribed page by page; figures and tables of Volume I
   Sections III to V are read for the records that use them.
2. **Records:** 348 experiment records (199 from Volume I, 149 from Volume II), each with the pages it
   comes from and the setup details the report gives (complete for few of them; each record says what is
   missing). 192 records have digitized observations, 11,688 rows in all (symbols, curve samples and
   features read off the figures):
   - Volume II, Appendices A to C, all 149 records: direct shear (124), density (7), grain size (7) and
     sonic moduli (11);
   - Volume I, 43 records: load-penetration (22), direct shear (13), dynamic penetrometer (3), impact (3)
     and model drop (2).
   Three more Volume I records are printed tables of runs (`runs.csv`): the drag tests of Fig. 4-6a and
   the model drop tests of Table 5-3, in two soils.
3. **Method:** each figure read twice by independent AI readers (in some early batches both readers
   saw shared notes; each batch review says where), the readings compared mechanically, and
   disagreements settled by a re-reading of the scan where one was made. Each observation carries its
   reading bound and its status. At the freeze: 8,718 `agreed` (the two readings matched within their
   bounds), 143 `resolved` (a re-reading settled a disagreement), 981 `one-sided-verified` (held by one
   reading and checked on the scan by the other reader), 821 `one-sided` (held by one reading, not
   verified), 26 `pending-review`, and 999 answered `ok` by two student reviewers: 743 `audited` (the
   two readings had agreed) and 256 `confirmed` (the point rested on a rule, a re-reading or one
   reading).
4. **Human checks:** four student reviewers gave 3,360 answers on sampled points: 2,834 ok, 219
   problem, 298 cannot tell, 9 unreadable (`qa/audits.csv`).
5. **Known gaps:** 153 Volume I records have no measured data yet, among them 64 of the 86
   load-penetration records and 12 of the 13 drag records. The WES M-71-10 reports and the Apollo 15
   and 16 penetrometer tables are acquired (the Apollo files are under `nasa-reports/`) but not turned
   into records in this release.
