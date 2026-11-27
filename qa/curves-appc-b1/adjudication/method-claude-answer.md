# Claude's answers (written before Codex ran)

1. **Gap rule.** Bridge, with an absolute limit in page pixels added to the relative one: the
   other reading's trace may be interpolated across a gap no wider than max(3 x its median sample
   spacing, 60 px on the page). The relative rule alone is scale-dependent: a reader who samples
   densely (about 2 thousandths, 12 px) gets a 36 px limit, narrower than the interruption a dashed
   line has around every symbol (about 40 to 55 px). 60 px is about three symbol widths: wide enough
   to bridge a symbol gap, narrow enough that a real feature of the drawn line (a kink, a fork such
   as n1760/n2345 on FC-1B, which developed over about 100 px) cannot hide inside it without one of
   the readers' neighbouring samples showing it. Bridged samples get status `agreed` and a note
   naming the bridged gap width, so they are traceable and still in the audit's agreed stratum.
   Change my mind: a bridged sample within 60 px that a page look shows off the ink.
2. **Features.** Keep them, but compare by meaning, not by position. Peak: compare y only
   (|dy| <= b_y + b_y'); x of a plateau peak is reported as the canonical reader's with the other
   reader's x in the note, and the x bound widened to cover both (an interval). First and last
   points: these are trace ends, not observations; compare them with the trace-end question (3).
   Features are never sampled for the audit and duplicate markers or trace samples, so they should
   not hold up a batch. Change my mind: a downstream use that needs the peak displacement itself.
3. **Non-canonical-only points.** Keep them. Markers are observations; losing one because the other
   reader had the smaller calibration residual is wrong. Write them to the canonical output with
   `source` = the reader who found them, status `one-sided`, values in that reader's calibration
   (the calibrations agree within tolerance at the frame corners on every panel), then verify each
   on the page like any one-sided point. Curve-end samples likewise: the longer of the two traces
   is kept at each end where the extra samples are on ink.
4. **Series ids.** `n2935`: the print says 2935 on both figures, the two page transcriptions agree,
   and the normal stresses of the PS series are multiples of 733.7 psf (4 x 733.7 = 2935). The
   inventory's 2995 is a transcription error. Rename at the canonical stage through a series map
   (submissions stay immutable), and correct the figures index forward: a decision row in the
   inventory's decisions file that `tools/build_figures.py` applies, so a rebuild produces 2935.
