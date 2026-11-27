Written **1,937 point records**, with calibrations, overlays, and ambiguity notes.

[Download all deliverables](<local path>) · [Detailed counts and file manifest](<local path>)

Counts below follow the listed series order. Upper totals include markers, traces, and three features per curve; lower totals are markers only.

| Figure | Series order (`n` prefix) | Upper totals | Lower totals |
|---|---|---|---|
| FC-5B | 4695, 3815, 2934, 1761, 734 | 84, 81, 84, 81, 82 | 13, 13, 13, 13, 13 |
| FC-6B | 4695, 3815, 2934, 1761, 734 | 82, 83, 84, 82, 82 | 13, 0, 13, 13, 13 |
| FC-6C | 4695, 3815, 2934, 1961, 714 | 82, 83, 84, 90, 82 | 12, 13, 13, 13, 13 |
| FC-6D | 4695, 3814, 2934, 1761, 147 | 89, 83, 82, 81, 83 | 17, 18, 16, 16, 25 |

Calibration RMS residuals: x and lower y in thousandths inch; upper y in psf.

| Figure | Upper RMS x / y | Lower RMS x / y |
|---|---:|---:|
| FC-5B | 0.955 / 3.525 | 0.916 / 0.131 |
| FC-6B | 1.463 / 8.029 | 1.345 / 0.243 |
| FC-6C | 0.640 / 9.750 | 0.581 / 0.072 |
| FC-6D | 1.079 / 8.624 | 1.142 / 0.068 |

Principal limitations:

- **FC-5B:** touching lower triangles and grid/frame overlaps; heading gamma differs from the legend.
- **FC-6B:** lower square series could not be identified. Horizontal calibration exceeds the 0.5% threshold because of the nonuniform printed grid; this remains flagged for review.
- **FC-6C:** upper plateaus share grid ink; lower circles touch zero. Only two lower ordinate numerals are visible. Legend confirms **1961 and 714**.
- **FC-6D:** touching plus/triangle stacks; three outside-range rebound symbols retained with interpretation notes. Some potential markers remain unidentifiable. Legend confirms **3814 and 147**.

Sampling gaps around symbols and dashes are preserved under rule 7. All delivered trace and feature coordinates passed the dark-pixel audit.

Each figure folder contains both calibration directories, eye checks, pixel/native CSVs for both panels, both overlays, `notes.md`, and `counts.csv`.