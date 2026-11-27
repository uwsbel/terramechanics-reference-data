# Terramechanics Reference Data

Measured soil tests for judging terramechanics simulations.

This collection provides laboratory soil tests as numbers: for example, the force needed to push a
cylinder into sand as it goes deeper, or the stress at which a soil sample fails in shear. Each test
comes with what one would need to set up the same test in a simulator (the soil, how its bed was
prepared, the tool and how it moved), and states what the original report leaves out. Every number
carries the page of the report it was read from.

The tests in this release come from a 1968 NASA study for the Apollo Lunar Module, the Bendix "Lunar
Module (LM) Soil Mechanics Study" (report AM-68-1), in which twelve soil conditions were tested on Earth
to predict how the lander's footpads would behave on the Moon. The collection will grow with further
tests, and contributions are welcome.

The website, https://uwsbel.github.io/terramechanics-reference-data/, presents each test with its setup,
its plot, its source pages, and a walkthrough of how to set up a virtual experiment of it in a simulator.
It is built from the `site/` folder of this repository.

## Getting the data

1. `data/experiments/index.csv`: one row per record, with its setup as printed in the report. Most
   records are single tests; the others are series the report averaged or derived from tests,
   correlations, numbers given only in the text, and soil samples (the `kind` column says which).
   Not every record has its points read yet.
2. `data/experiments/<record id>/observations.csv`: the measured points of a test, in SI units. Each
   point has a reading bound, a status that says how it was checked, and its position on the scanned
   page. `series.json` beside it gives the units, the conversion factors and how the points were read.
3. `data/materials/`: the test soils, from the report's soil table.

The measured points are in SI units, with the value as printed in the report kept beside each one; the
index keeps the setup fields as printed. The website's Glossary defines the codes, symbols and status
words; `docs/DATA-ORGANIZATION.md` describes every file and column.

## How the numbers were read and checked

Most numbers in the reports exist only as printed figures. Each figure whose numbers are in the data
was read twice, separately, by two readers (the AI systems Claude and Codex), each from the scanned page
and without seeing the other's reading. In some early batches both readers also saw notes from an earlier
step, so those readings were not fully independent; the review of each batch under `qa/` records where. A script compared the two readings point by point. Where they disagreed, a fresh
reading of the page, made without knowing which reading was whose, settled it, or the point was left
marked as unsettled. Then student reviewers compare a sample of the points with the scan, and every
check they make is recorded. Each point's status says which of these checks it passed.

## What the data can and cannot say

1. A reading bound is how precisely a point could be read from the printed figure. It is not the
   uncertainty of the experiment, which the reports rarely give.
2. Some setups are incomplete: the depth of a soil bed, or how it was placed, is often not printed.
   The record of each test lists what is missing.
3. `docs/OPEN-QUESTIONS.md` lists what could not be settled, with the evidence. Reading it before
   drawing conclusions from a single figure is recommended.

## Citing

Cite the release used, by its DOI: version 1.0.0 is https://doi.org/10.5281/zenodo.24477009
(`CITATION.cff` holds the full entry). For a single test, add its record id and the page of the
report, for example: record `b68-lpt-024`, AM-68-1 Vol. I, Fig. 2-42, printed page 2-77, PDF page 102.
Each release is a fixed snapshot; `CHANGELOG.md` lists what changed from one release to the next.

## The source reports

The public release does not copy the NASA reports; each is linked by its record on NASA's Technical Reports Server
(NTRS), as NASA asks (D-054). `sources/register.csv` gives, for each report, its NTRS link (column `url`), the file name the tools expect
(`local_file`) and the SHA-256 of the copy that was read (`sha256`). To render page images or check a reading against the
page, download the report from its NTRS record, save it under that name, and compare its SHA-256 with the register's. The
page images on the website come from those reports, courtesy of NASA.

## License

Data under CC BY 4.0 (`LICENSE-DATA.md`); code under the BSD 3-Clause license (`LICENSE`). The source
reports are public: NASA's technical reports server or the Planetary Data System lists each one for public
use (`sources/register.csv` gives the evidence for each).

## Contributing

Two kinds of contribution are welcome: data from new physical tests, and scripts that run virtual
experiments mirroring the tests hosted here. Corrections are welcome too: a point that looks wrong, a
better scan of a page, or an answer to an open question. Open an issue in this repository; the
website's Contribute page says what each kind of submission should contain. Every contribution enters
with its source, like every other number here.

## Where things are

| Folder | Holds |
|---|---|
| `data/` | The test records and the soils |
| `docs/` | How the data are organized, the reading rules, the open questions |
| `corpus/` | Page-by-page transcriptions of the source reports, with indexes of figures, symbols and terms |
| `nasa-reports/` | The Apollo 15 and 16 data from the Planetary Data System; the public release links the NASA reports instead of copying them (below) |
| `sources/` | The register of sources, with their rights |
| `insights/` | Findings about the reports themselves, for example where two printings disagree |
| `tools/` | The scripts that build the records and the website |
| `site/` | The website, generated from the data |
| `extractions/`, `qa/` | The two readings as submitted, and the record of how they were compared and checked |

## What the public release leaves out

Each public release is built from the maintainers' repository, without its history. It leaves out:

1. the student reviewers' names and e-mail addresses, and the e-mails sent to them; in the audit records each
   reviewer is a code, R1 to R4;
2. the audit program's working files: the answer keys, the sample of points still to be asked, who has which
   chunk, the returns as sent and the report on each return (the outcomes are in `qa/audits.csv`), and, while
   the audit runs, its manual and the tool that builds its packets;
3. the maintainers' roadmap, the guide for the AI agents, and the notes for the data paper in preparation.

The decision log keeps every decision under its number, with its options and outcome; decisions about the
people and the logistics of the review are summarized. The readers' briefs and the comparison records under
`extractions/` and `qa/` are kept as they were written, so some of them still name a file listed above. Local
file paths in them appear as `<repository>` (this repository) or `<local path>` (another folder on the machine
they were written on).

Maintained by the Simulation-Based Engineering Laboratory (SBEL), University of Wisconsin-Madison. Contact:
Dan Negrut, negrut@wisc.edu; corrections to the data through the repository's issues.
