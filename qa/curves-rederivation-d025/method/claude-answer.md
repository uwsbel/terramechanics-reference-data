# Claude's answer, written before Codex runs

1. **Tie-break: keep (c), first submission, as written.** In a tie the two maps are equivalent for
   the values (the means differ by under 0.16 px, about 0.5 psf), so no choice is more accurate; what
   matters is that the result is reproducible from the submissions alone. "Keep the existing
   canonical" makes the outcome depend on the history of the tool (the superseded residual rule), which
   a reader of the protocol cannot reproduce; reinstating the residual as a secondary key reintroduces
   a criterion D-025 retired, and its differences are 1 to 3 percent noise. Denser sampling is a
   property of the reading, not of its accuracy, and would systematically favour one agent. The cost,
   about 160 items to adjudicate, is a few hours of agent time with the existing blind two-round
   machinery, and buys a canonical choice that anyone can recompute. The density loss is real but the
   protocol's sampling step was chosen to represent the curves; if denser canonical traces are wanted,
   that is a sampling rule for future readings, not a tie-break.
2. **Re-adjudicate blind; do not translate.** A decision on a point says which reading was right at
   that point; for a marker it would carry over to its paired point, but for a trace the new canonical
   sample sits at a different x and is compared with an interpolation, so a mechanical translation
   would claim a verdict nobody gave. Old decisions stay valid where their point is still written (the
   other reader's one-sided points keep their source and sequence). The 18 pending items near an old
   decision will mostly be settled the same way, and the adjudication record will show that.
3. **Line rules: keep, with two notes.** The 2 px threshold sits in a clean gap (coinciding lines up
   to 1.8 px, misplaced ones from 2.9 px). Coverage-first is right: a map lacking a verified line
   interpolates over a wider interval or extrapolates. The per-line mean weights each line once, which
   matches the share of the plot each line governs. Note one: the tie threshold of 0.25 px is a
   judgment, not derived; a test of how often the means differ by 0.1 to 0.25 px would show whether it
   matters (here the largest tie difference is 0.16 px). Note two: a line can pass the check at 1.8 px
   and still carry that distance into the bounds through the 80th-percentile error, which is the
   intended behaviour.
4. Implementation risks Claude sees: the ink centre near a crossing curve or symbol is biased, which
   the median absorbs; `compare_knots` evaluates the other reading's line in the first reading's frame,
   fine for the near-identical gradients here but untested for strongly different ones.
