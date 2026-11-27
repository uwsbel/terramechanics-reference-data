# Data license

The data in this repository are licensed under the Creative Commons Attribution 4.0 International
license (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/

That covers everything that is not code: the experiment records and indexes (`data/`), the page
transcriptions and their indexes (`corpus/`), the two readers' submissions (`extractions/`), the
reviews, decisions and audits (`qa/`), the insights (`insights/`), the documentation (`docs/`) and
the site content (`site/`). The code is licensed under BSD-3-Clause (`LICENSE`).

You may share and adapt the data for any purpose, including commercially, provided you give
appropriate credit: cite the release you used (`CITATION.cff`; each release is a fixed, versioned
snapshot) and say if you changed the data.

## The sources

The numbers come from reports that NASA's Technical Reports Server (NTRS) or the Planetary Data System
lists for public use: works of the United States Government, data sets the Planetary Data System holds
in the public domain, and reports written for NASA under contract whose NTRS record shows public
distribution, public use permitted and no third-party restrictions (the Bendix report AM-68-1, Volumes I
and II, is one of these). `sources/register.csv` records the evidence for each source and the date it
was checked. The public release does not copy the NASA reports: each is linked by its NTRS record
(D-054), and the page images on the website, rendered from them, are reproductions of single pages,
courtesy of NASA. The Apollo 15 and 16 data under `nasa-reports/` come from the Planetary Data System,
which holds them in the public domain. CC BY 4.0 applies to the work done here (the transcriptions,
readings, reconciliation, adjudication, audits and the records built from them), not to the original reports,
whose own terms, as their NTRS or Planetary Data System records state them, apply.

## What the data are, and are not

A reading bound on this site is the uncertainty of our reading of a printed figure, not the
uncertainty of the experiment. The data are provided as is, without warranty of any kind; each point
carries a status that says how it was checked. See `docs/OPEN-QUESTIONS.md` for the known soft spots.
