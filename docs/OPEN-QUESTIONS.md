# Open questions

This data set is a first step in a longer journey, not a finished product. The numbers come from
scanned reports more than half a century old, read twice by independent agents, reconciled by
rule, and sampled by student auditors. That process leaves questions we could not settle, and a
few we chose not to spend more time on yet. They are listed here so that a user knows where the
soft spots are, and so that anyone who wants to help can pick one up. If you can answer one, open
an issue or a pull request in the repository, or write to the maintainers; a better scan, a
printed copy of a report, or an hour with a figure on your screen is enough to close several of
them.

A reading uncertainty on this site is the uncertainty of our reading of the printed figure, not
the uncertainty of the experiment. Nothing below changes that distinction.

## Reading the figures

1. **Trace samples in gaps.** A sampled point on a plotted curve should sit on the line's own ink,
   not on a symbol or in the white gap between a dash and a symbol. A mechanical check now removes
   samples that fail this (it was validated blind on 400 samples: 98 percent of what it removes is
   rightly removed), but it finds only about half of the failures. The misses are at curve ends on
   the frame or a grid line, and at junctions where a symbol's outline fuses with the line. About
   300 samples it could not decide are kept and marked for review. See
   `qa/adjudication-2026-10-28-inkrule/review.md` and `tools/check_trace_ink.py`.
2. **Symbols merged with grid lines or with each other.** For 22 points of the first audit wave,
   two rounds of blind re-reading could not say where the symbol's center is (8 undecided, 14
   still split within a pixel). They are in the data with widened bounds and the status
   `pending-review`. See `qa/adjudication-2026-10-27/review.md`.
3. **Which point of a triangle the 1968 plotter registered.** A plotted triangle has two defensible
   centers, its centroid and the middle of its bounding box, about one sixth of its height apart.
   We accept both and carry the difference in the bound (`docs/CURVE-READING.md`, rule 8). A page
   of the report or of the plotter's manual that states the convention would tighten every marker.
4. **Grain-size bands that merge.** On the Appendix A grain-size charts the average curve and the
   two range curves run together over parts of their length, and neither reader could tell them
   apart there. See `insights/1968-vol2-appendix-a-grain-size-curves-against-their-tables.md`.
5. **Residual labels on log and reciprocal axes.** One item of the axis transform work (D-027)
   remains: the site labels residuals in printed units rather than in the transformed coordinate.
   Values and verdicts are unaffected. The other two items are done (2026-11-18): the canonical
   files now record where the other reading lies on the page, and audit packets draw it there,
   instead of placing it with a map fitted to the kept reading.

## The printed sources themselves

6. **Seven cells of Table 2-2 (Volume I, printed 2-14).** The page is a 200 dpi bilevel scan on
   which 5, 6 and 8 print alike. The cells carry both readings. A better scan or a printed copy of
   AM-68-1 Volume I would settle them. See `qa/pages-s2-b1/review.md`.
7. **Table 2-3 against the Appendix A specifications.** The summary table of Volume I and the
   per-soil specification sheets of Volume II disagree on six friction angles (soils 1, 3, 4, 7,
   11, 12) and on the gradations of four soils; 26 cells differ in all. Both Volcalite reprints are
   misprinted and the first printing is right. We record both values and do not know which the
   authors used downstream. See `qa/specifications/table23-vs-appendix-a.md`.
8. **The Table 2-3 modulus.** It appears to be IITRI's small-strain wave modulus, interpolated in
   relative density from two tested densities. This is an inference from the Appendix B plots, not
   a statement in the report.
9. **Computer plots against their printed fits.** On the Appendix C computer plots (Figs. C-8 to
   C-15) the drawn least-squares lines depart from the fit parameters printed on the same plot by
   up to 96 psf, while the printed parameters reproduce from the data sheets. We do not know why
   the plotter drew the lines where it did. See
   `insights/1968-vol2-appendix-c-computer-plots-against-printed-fits.md`.
10. **Relations between records that could not be resolved.** Five items of the Volume II figure
    index carry the relation `unresolved` (the Soil No. 10 specification table, printed A-71, PDF
    72, and Figs. C-12 to C-15): each appears to repeat material printed elsewhere, but the evidence
    does not say whether it is the same item or a derived one (for example Fig. C-12 against data
    sheet C-4B). They are counted once, on the side
    of caution. (Corrected 2026-11-05: this item said 31 rows of the experiment index; that index has
    no unresolved relation, only `same-as` and `derived-from`.)
11. **Setup fields.** Many records do not yet carry a complete setup (apparatus, rate, sample
    preparation) because the report prints it once for a family and the index has not been
    completed with those fields (`setup_status` on each record).
12. **The load axis of Figure 2-34.** Its title reads `Load - Lbs. x 100` while the printed slope
    (54 lb per inch) and intercept (140 lb) of the fit drawn on it, and the same test LPT 87 on
    Figure 2-48 (plain `Lbs.`), only make sense in plain pounds. The data record the axis numbers
    as pounds and note the title; a reader who knows what the `x 100` meant is welcome. The fit
    line's intercept read on the axis numbers is 139 lb, beside the printed 140 lb
    (`qa/curves-s2-b1/review.md`).
13. **The authors' straight lines.** The fit lines (`Slope = ...`) and the bearing-capacity line
    on Figures 2-32 to 2-34 are read like any curve but have no experiment record yet, so they sit
    in the batch files, not in `data/`, until the index gains derived-series records for them.
14. **The first inch of Figure 2-48 (Volume I, printed 2-83).** Its 0 to 1 in interval is drawn
    about 233 px tall against 304 to 316 px for every other inch. Both readings take the grid as
    drawn (the bottom frame is 0 in). If the zero line was meant to sit at the regular spacing,
    every value below 1 in shifts by up to about 0.25 in. The same test, LPT 87, is printed on
    Figure 2-34 with a regular first inch, which a comparison of the two printings could use
    (`qa/curves-s2-b2/review.md`).
15. **Grid lines beyond the last printed label.** On Figures 2-32, 2-34 and 2-45 the frame runs
    past the last labelled line, and the unlabelled lines there (penetration 10 and 11 in, 7 to 9 in;
    load 275 and 300 lb) are valued by the even grid spacing. The two readings differ there by at
    most 0.08 in, because one anchored those lines and the other extrapolated; the record values
    rest on the anchored lines.

## The audit

16. **Points checked by one reviewer only.** Every sampled point is meant to be checked by two
    students. Where one of the pair has not returned a chunk, the point stands as checked by one
    person, and its row in `qa/audits.csv` says so. Nothing in the pipeline waits for the second
    return; a later wave can re-deal such points if a user needs two signatures on a figure.
17. **Scan of the sample, not the population.** The audits cover every disputed point and a
    sample of the agreed ones, sized by the square root of the points in a figure. An agreed point
    outside the sample rests on the agreement of two readings made separately and on the rules, not on
    a person.

## Scope

18. **Not yet read.** Most Volume I curves. In Section II, the eight load-penetration figures 2-29,
    2-32 to 2-34 and 2-45 to 2-48 and the three DPT signatures of Fig. 2-54 (the dynamic penetrometer) are
    read; the other load-penetration figures, the pressure parameter plots, the DPT correlation, rate
    series and density control are not, nor Tables 1-1, 2-1 and 2-2. Of Sections III to V, three
    impact tests, two model drop tests and the run tables of Fig. 4-6a (drag) and Table 5-3 (model
    drop) are read; the other impact and drag records are indexed only.
19. **Not yet extracted sources.** The Apollo 15 and 16 penetrometer tables and the WES M-71-10
    reports are acquired and registered but not yet turned into records; 13 further leads are
    acquired-with-caveat and await a rights decision each.
20. **Later simulants.** Whether data on GRC-1, JSC-1A and their successors enter the first release
    is undecided (D-015).

## Points counted twice

21. **A curve's end recorded by both readings.** Where the other reading's last (or first) sample lies just beyond the
    canonical end of a trace, within both readings' bounds of that end, the comparison keeps it as a point of its own,
    so the end is recorded twice, a fraction of a pixel apart. Applied to the batches read before 2026-11-19, the rule
    that drops such a duplicate would remove 193 points (159 verified on the page by the other agent, 34 one-sided)
    from the records; the values are not wrong, only counted twice. The rule is used from the dynamic penetrometer
    batch on (`tools/diff_curves.py --end-dedup`); whether to apply it to the earlier records, some of whose points
    the students have audited, is open.

## Two printed values for one quantity

22. **The touchdown velocities of NASA Tests No. 1 and 2.** Table 5-T3 (Volume I, printed 5-45, PDF 325) is in the
    records `b68-mdrop-t5-3-rs` and `b68-mdrop-t5-3-ss` since 2026-11-20, every bed's relative density, unit weight and
    friction angle with it, and the record pages of the two tests give its values. Its velocities "were calculated
    based on the exact time interval between the instant of model release to the instant of ground contact" (printed
    5-44, PDF 324). The insets of the strut-load figures print others: -114.93 in./sec. for Test No. 1 (Fig. 5-25,
    printed 5-50, PDF 330; the table gives -114.9) and, on a degraded scan, -60.55 and 83.75 in./sec. for Test No. 2
    (Fig. 5-32, printed 5-57, PDF 337; the table gives -60.5 and 83.5, and 83.75 does not round to 83.5). Our
    arithmetic, against |V_v| = g tau (the speed of a free fall from rest over tau) within the rounding of both printed
    numbers: with the report's g for Earth, 32.2 ft/s^2 (glossary, printed 2-2, PDF 27), three of the four vertical
    drops are consistent with it and none of the four with a horizontal velocity; with standard gravity, all four
    vertical drops and one angled drop (Test No. 3). The two values of g differ by 0.08 percent, about the rounding
    of a printed tau, so at this precision the verdicts depend on the g used. That shows consistency, not the method, which the report does not state
    (`qa/tables-s5-b1/arithmetic.md`). Both values are in the records with their sources; which one a simulation starts
    from is a study's choice. How the inset values were obtained, and the method behind the angled drops' velocities,
    are open.

## How to help

a. Pick an item, say which, and send what you found with the page, figure and pixel or printed
   value, so it can enter the record with a citation like every other number here.
b. If you own or can scan a printed copy of AM-68-1 (Bendix, 1968, both volumes) at 300 dpi or
   better, items 6 and 7 close almost by themselves.
c. If you ran, or know who ran, these tests or their plotter, items 3 and 9 are yours.

Every item above names its evidence file in the repository; the decision log (`docs/decisions.csv`)
records what was decided about it and when.
