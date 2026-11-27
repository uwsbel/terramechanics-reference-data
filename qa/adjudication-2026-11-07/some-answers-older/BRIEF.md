# Transcribing "some" answers

`some-answers.csv` holds 103 answers given by adjudicators who checked runs of trace samples on scanned
plots. Each row names the run's samples (`subject_samples`, page pixels `(u,v)`) and the adjudicator's
answer was `some`: some of the samples are on the drawn line and some are off it. The adjudicators were
asked to list the off-line samples by pixel in the comment; many comments also say which samples are on.

Your job is a transcription, not a judgment of the plot: for every sample of every row, write what the
comment says about it.

1. `off`: the comment says the sample is off the line (inside a frame or grid line, in a gap, on a
   symbol, on another curve, and so on).
2. `on`: the comment says the sample is on the line, or the comment does not mention it (the
   adjudicators were asked to list only the off-line ones).
3. `unclear`: the comment mentions the sample but does not let you tell whether it calls it on or off.

Match a pixel in the comment to a sample when it is within 4 px of it. Write `transcription.csv` in this
folder with columns `round,item,adjudicator,sample_px,verdict`, one row per sample (sample_px exactly as
written in `subject_samples`), every sample of every row. Work only inside this folder. Write in US
English with no em-dashes or en-dashes. Finish with a one-paragraph report naming any rows you found
hard.
