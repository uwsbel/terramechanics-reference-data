# Figure 2-54 | Typical DPT Signatures

Independent reading of `packet/p0117.png`, printed page 2-92. The page reads upright after a clockwise quarter turn. All reported positions are `(u, v)` in the unrotated 300 dpi scan. Time increases toward smaller `v` and deceleration toward smaller `u`. The preceding text and apparatus schematic identify the drop-penetrometer measurement.

## Time and printed labels

- The opposing arrows marked `.01 sec.` in panel 3 meet two adjacent timing lines. The left tip meets the assigned +30 ms line at approximately (1776, 2256) and the right tip meets the +40 ms line at approximately (1774, 2105). There is no printed time origin. I assigned 0 ms to the column next to the three ruler zeros and counted both ways in 10 ms steps. The ruler labels interrupt that column locally, and the solid zero stubs start to its right in the upright view.
- I checked all 12 timing lines in each panel, from -20 ms at the first line right of the break marks to +90 ms at the right frame. The record boxes conceal parts of the -20 ms line. Both remaining stretches identify the same line. Each panel has its own ink-verified line fits. The visible pre-grid ink and the break marks are outside the timed reading.
- I checked the caption, the three record boxes, and the G ruler labels against the page. The records and soil labels agree with the index. Record No. 53958 is 2' Box, RS-Loose, 41.1 PCF. Record No. 54025 is 2' Box, RS-Intermediate, 44.1 PCF. Record No. 54-65 is LPT No. 26, RS-Dense, 52.0 PCF. The G's heading is printed above panel 1's ruler. The curves are solid and have no plotted symbols.
- I matched 0, 10, and 20 to their stubs in panel 1, 0, 10, 20, and 30 in panel 2, and 0 through 80 by tens in panel 3. Panel 1 has 2 g minor ticks. Panel 2 has 1 g subdivisions, with the expected 1 g stub inseparable from the dashed ink. Panel 3 has 2 g subdivisions from 0 to 10 and from 70 to 80, with 5 g subdivisions between 10 and 70. The position and outcome of each check are in `calibration-eye-checks.csv`.

## Calibration

The printed solid zero ticks sit **8.96, 9.35, and 11.38 px below** the dashed datums at their respective rulers. I measured both, used each dashed line as the 0 g knot as specified, and kept each verified positive ruler tick at its printed or counted value. The solid zero locations are in each calibration JSON and the eye checks. The lowest interval is consequently shorter than the typical ruler spacing, especially in panel 2. Negative native readings extend that interval and are sensitive to the datum. The recorded ink can lie visibly below the dashed line even before impact.

The global affine fit is a drafting diagnostic. Its largest residuals exceed 0.5% of at least one axis span in each panel. I rechecked the timing centers and ruler stubs before tracing. The timing intervals vary in the scan, and the solid-zero offset affects the lowest G interval. Native values use the verified piecewise lines and their position bounds. Ruler stubs are projected in the direction of the measured dashed datum. In panel 2, the 2 g stub has distinct ink in a tight cross-stub window. A wider search catches the stronger dashed line next to it.

| Panel | Affine time RMS / max (ms) | Affine G RMS / max (g) | Largest pointwise piecewise–affine difference (ms / g) |
|---|---:|---:|---:|
| 1 | 0.434 / 0.667 | 0.199 / 0.538 | 0.666 / 1.162 |
| 2 | 0.434 / 0.684 | 0.254 / 1.177 | 0.646 / 3.158 |
| 3 | 0.404 / 0.626 | 0.225 / 0.895 | 0.599 / 2.055 |

`cal_model` flags intervals that extend beyond an outside knot, including endpoint bounds extending beyond the timing frame and reads below the dashed datum.

## Trace reading

- I sampled every 2 ms on the earlier timed lead-in, then on the half-millisecond grid starting just at or before 2 ms ahead of the visually chosen onset. The 0.5 ms grid covers at least 5 ms after the main crest, then the 1 ms grid runs through 20 ms and the 2 ms grid continues to the end. Steep-flank points fill in where 2 g or 5 g spacing is finer. Trace and feature rows share drawing order.
- The printed zero numeral interrupts or hides the +2 ms trace position in all three panels. I omitted those three samples. The rest of the lead-in can be followed in the solid ink below the dashes. Near the ruler stubs, on timing-line crossings and where a tail coincides with the dashes, the point notes identify shared ink and the pixel bounds are widened. Each first point is the entry to the timed grid. Each last point is where the trace disappears into the right frame, estimated from the adjacent trace ink.
- **Panel 1.** At the +10 ms line, the low solid stroke and the rising stroke have a short visible gap. The +10 ms sample is on the low stroke. The onset feature is on the lowest separable rising ink. The main top is nearly flat. The saddle and secondary crest are broad, and the return to zero merges with the dashes.
- **Panel 2.** The rising stroke begins with a rounded bend and initially shares ink with the +10 ms timing line. The small trough and crest after the +30 ms crest are shallow, especially the third crest. The far tail interleaves with the dashes and small scan breaks. Its fine variations are ambiguous.
- **Panel 3.** The onset and lower falling flank cross the dashes near timing lines. I read the peak within the pointed ink cap. The post-peak trough is broad and the trace blends with the datum late in its recovery, then rises into a broad late crest before reaching the frame.
- Bounds use the local transverse ink half-width. At shared ink, I used the nearest readable thickness and added an allowance for the overlap. The overlays keep scan orientation, with orange for trace samples and blue for features. Their crop origins in scan pixels are (294, 1270), (927, 1270), and (1375, 1270), respectively.
