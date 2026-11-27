# Figure 5-25 · NASA Test No. 1

The caption reads “Strut Axial Load versus Time (NASA Test No. 1).” The shared axis reads “Time - Seconds.” The labels are `0`, `.01` through `.08`, a damaged `.09`, and `.10`. At `.09` the decimal point and the bottoms of two digits survive. The short ruled tick above the damaged section of baseline is one .01 s interval after `.08` and was measured at .09 s. The faint `.10` tick was also measured.

| Panel | Printed axis title | Printed load labels from bottom to top |
| --- | --- | --- |
| 1 | (Tension) Load on Strut No. 3 | `0`, `+20`, `+40`, `+60` |
| 2 | (Tension) Load on Strut No. 2 (lbs.) | `0`, `+20`, `+40`, `-60` |
| 3 | (Compression) Load on Strut No. 1 (lbs.) | `0`, `-20`, `-40`, `-60`, `-80`, `-100` |

Panel 1 has no visible unit text after “No. 3.” Loads are reported in pounds, consistent with the figure's other load panels and its index row. In panel 2, the line carrying the printed `-60` is a single 20 lb interval above the `+40` line. It anchors +60 lb. The panel 3 scale is signed, so its two crests in compression magnitude are local minima of the reported load.

The inset conditions read “Vᵥ = -114.93 in. sec.   Vₕ = 0” and “RS Loose   Level Surface.” Table 5-T3 gives -114.9 and 0 in./sec for NASA Test No. 1. The inset's geometry and callouts were read as annotations.

All 11 shared time knots and all labelled load rules passed the ink check. The fit of the +40 and +60 lb rules in panel 1 stops before the right-side callout boxes. The time scale uses measured lower ticks with their common lean estimated from surviving upper marks. Native time bounds include an allowance up to about 4 px for projecting that lean away from the lower ticks.

| Series | RMS time, s | RMS load, lb | Largest anchor residual, s / lb | Largest affine-to-piecewise change, s / lb |
| --- | ---: | ---: | ---: | ---: |
| strut3 | 0.00005103 | 0.14028 | 0.00016702 / 0.40487 | 0.00012238 / 0.21346 |
| strut2 | 0.00005103 | 0.19805 | 0.00016702 / 0.47139 | 0.00012257 / 0.23606 |
| strut1 | 0.00005103 | 0.15835 | 0.00016702 / 0.40394 | 0.00012204 / 0.20705 |

The RMS residuals are below 0.5% of each axis span. Individual load anchors in panels 1 and 2 exceed 0.5% of their labelled 60 lb span. The piecewise values follow the verified rulings at their own positions and tilts.

- **strut3** leaves the left frame along the zero ruling and meets that ruling again at the right tip. The shallow ripples near .024–.032 s and .072–.075 s are only a few pixels high. The main crest is near .059 s.
- **strut2** starts close to the left frame and zero ruling. Its first small near-zero shoulder is visible just above the ruling. It ends freely at about +10 lb.
- **strut1** starts with a free tip below the zero ruling, about +3.9 lb on the signed scale. Its first compression crest merges with the `-80` rule around .009–.010 s. A small scan break follows on the descending compression-magnitude limb near .014 s. The unloading stroke is distinct from a fleck above it at the damaged `.09` tick. The final tip is at about -4.7 lb.

Pixel bounds use the local stroke half-thickness. At joins, the nearest clear part of the stroke gives the thickness. The three panels contain no point symbols.
