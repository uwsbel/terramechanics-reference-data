# Blind reading: curves-appc-b3

Evidence confined to the supplied packet. No other reading used.

## Counts

M = markers; T = trace samples; F = features. Lower panels contain markers only.

| Figure | Series | P1 M | P1 T | P1 F | P1 total | P2 M |
|---|---|---:|---:|---:|---:|---:|
| FC-5B | n4695 | 13 | 68 | 3 | 84 | 13 |
| FC-5B | n3815 | 13 | 65 | 3 | 81 | 13 |
| FC-5B | n2934 | 12 | 69 | 3 | 84 | 13 |
| FC-5B | n1761 | 13 | 65 | 3 | 81 | 13 |
| FC-5B | n734 | 13 | 66 | 3 | 82 | 13 |
| FC-6B | n4695 | 11 | 68 | 3 | 82 | 13 |
| FC-6B | n3815 | 12 | 68 | 3 | 83 | 0 |
| FC-6B | n2934 | 12 | 69 | 3 | 84 | 13 |
| FC-6B | n1761 | 12 | 67 | 3 | 82 | 13 |
| FC-6B | n734 | 12 | 67 | 3 | 82 | 13 |
| FC-6C | n4695 | 11 | 68 | 3 | 82 | 12 |
| FC-6C | n3815 | 12 | 68 | 3 | 83 | 13 |
| FC-6C | n2934 | 12 | 69 | 3 | 84 | 13 |
| FC-6C | n1961 | 12 | 75 | 3 | 90 | 13 |
| FC-6C | n714 | 14 | 65 | 3 | 82 | 13 |
| FC-6D | n4695 | 15 | 71 | 3 | 89 | 17 |
| FC-6D | n3814 | 13 | 67 | 3 | 83 | 18 |
| FC-6D | n2934 | 13 | 66 | 3 | 82 | 16 |
| FC-6D | n1761 | 13 | 65 | 3 | 81 | 16 |
| FC-6D | n147 | 24 | 56 | 3 | 83 | 25 |

## Calibration residuals

RMS x is in thousandths inch. RMS upper y is psf; lower y is thousandths inch.

| Figure | Panel | RMS x | RMS y |
|---|---:|---:|---:|
| FC-5B | 1 | 0.955 | 3.525 |
| FC-5B | 2 | 0.916 | 0.131 |
| FC-6B | 1 | 1.463 | 8.029 |
| FC-6B | 2 | 1.345 | 0.243 |
| FC-6C | 1 | 0.640 | 9.750 |
| FC-6C | 2 | 0.581 | 0.072 |
| FC-6D | 1 | 1.079 | 8.624 |
| FC-6D | 2 | 1.142 | 0.068 |

## Review limitations

- FC-5B: touching lower triangles; grid/frame markers; wider first displacement bay; heading gamma 97.3 differs from legend 97.6.
- FC-6B: lower square series not identifiable and omitted; x calibration RMS exceeds 0.5% in both panels despite correct grid detection and revised thresholds. Printed -100 lower label is displaced from nominal scale.
- FC-6C: upper plus/down-triangle traces share horizontal grid ink; lower circles touch zero; only two lower y numerals visible, so central zero line is checked as inferred/unlabelled. Legend confirms 1961 and 714.
- FC-6D: plus/down-triangle stacks; three rebound symbols beyond x=250, with their interpretation flagged; potential upper n147 marker at x~50 and lower plus/circle rebound markers cannot be separately found. Legend confirms 3814 and 147.
- Trace sampling nominally every 20 px (~3.4 thousandths) within visible ink, with explicit first/last ink endpoints. Gaps around marker outlines/dashes are preserved and can exceed 5 thousandths under protocol rule 7. No interpolation through these gaps. Shared grid/curve ink and initial n147 frame overlap carry wider bounds.
- Pixel audit confirms all delivered trace/feature coordinates lie on dark image pixels; this checks ink presence, not independently the curve identity. Overlay review is also recorded in per-figure notes.

## Files

In `out/FC-5B/`:
- `cal-p1/anchors.csv`
- `cal-p1/calibration.json`
- `cal-p2/anchors.csv`
- `cal-p2/calibration.json`
- `calibration-eye-checks.csv`
- `points-p1.csv`
- `points-p1-native.csv`
- `points-p2.csv`
- `points-p2-native.csv`
- `overlay-p1.png`
- `overlay-p2.png`
- `notes.md`
- `counts.csv`

In `out/FC-6B/`:
- `cal-p1/anchors.csv`
- `cal-p1/calibration.json`
- `cal-p2/anchors.csv`
- `cal-p2/calibration.json`
- `calibration-eye-checks.csv`
- `points-p1.csv`
- `points-p1-native.csv`
- `points-p2.csv`
- `points-p2-native.csv`
- `overlay-p1.png`
- `overlay-p2.png`
- `notes.md`
- `counts.csv`

In `out/FC-6C/`:
- `cal-p1/anchors.csv`
- `cal-p1/calibration.json`
- `cal-p2/anchors.csv`
- `cal-p2/calibration.json`
- `calibration-eye-checks.csv`
- `points-p1.csv`
- `points-p1-native.csv`
- `points-p2.csv`
- `points-p2-native.csv`
- `overlay-p1.png`
- `overlay-p2.png`
- `notes.md`
- `counts.csv`

In `out/FC-6D/`:
- `cal-p1/anchors.csv`
- `cal-p1/calibration.json`
- `cal-p2/anchors.csv`
- `cal-p2/calibration.json`
- `calibration-eye-checks.csv`
- `points-p1.csv`
- `points-p1-native.csv`
- `points-p2.csv`
- `points-p2-native.csv`
- `overlay-p1.png`
- `overlay-p2.png`
- `notes.md`
- `counts.csv`

Reading aids (readings.json, enlarged labeled crops, helper scripts) remain under out/. The ZIP contains the required deliverables and this summary, rather than temporary reading aids.