# Independent reading — curves-appc-b8

The authoritative submissions are the five `FC-*/` folders: `points-p1.csv` holds measured pixels and pixel bounds; `points-p1-native.csv` adds verified piecewise-calibrated values and bounds in psf. Each folder has `cal-p1/`, six by-eye label checks, the full-page overlay and notes containing the printed parameters, measured comparisons and ambiguities.

`summary.csv` summarizes counts, residuals and comparisons. `verification.json` records final consistency checks. The final trace sheets/crops and triangle-fit sheets show the audited reading. All coordinates are original unrotated page pixels.

The helpers were written here, without modifying tools or reading another extraction. `read_images.py` creates inspection crops and validates grid knots; `marker_geometry.py` reconstructs triangle sides and includes the manual shared-ink correction; `trace_read.py` generates provisional ink candidates; `finish_reading.py` applies the visual audit (endpoints and the omitted C-11B 2500 psf target), writes CSVs/notes/overlays, and computes printed-value differences; `verify_reading.py` checks final files and regenerates final trace inspection sheets. `trace-candidates.json` is a provisional helper input, not a submission. The final CSVs supersede it.

C-11B's scheduled 2500 psf trace sample lies in a drawn gap and is omitted under protocol rules 6–7. The overlapping pair is retained as two distinguishable markers, with half-symbol bounds. C-10C's upper terminal line and triangle merge; the last distinct line ink is used and the unresolved pen termination is noted.
