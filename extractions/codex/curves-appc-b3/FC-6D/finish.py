import csv,json
from pathlib import Path
base=Path('out/FC-6D');checks={1:{'x':(2200,[(0,748),(50,1065),(100,1357),(150,1651),(200,1945),(250,2237)]),'y':(735,[(4000,1045),(3000,1341),(2000,1633),(1000,1927),(0,2211)])},2:{'x':(3230,[(0,765),(50,1083),(100,1371),(150,1668),(200,1961),(250,2254)]),'y':(760,[(0,2355),(-100,2645),(-200,2942),(-300,3234)])}}
rows=[]
for panel,axes in checks.items():
 c=json.loads((base/f'cal-p{panel}/calibration.json').read_text())
 for axis,(ref,pts) in axes.items():
  ls=c['vertical_lines' if axis=='x' else 'horizontal_lines']
  for value,eye in pts:
   l=next(l for l in ls if l['x_value' if axis=='x' else 'y_value']==value);fit=l['u_at_v0']+l['slope_du_dv']*ref if axis=='x' else l['v_at_u0']+l['slope_dv_du']*ref
   label='0 (unlabelled top frame)' if panel==2 and axis=='y' and value==0 else value
   rows.append(['FC-6D',panel,axis,label,f'{fit:.2f} at '+('v=' if axis=='x' else 'u=')+str(ref),eye])
with (base/'calibration-eye-checks.csv').open('w',newline='') as f:w=csv.writer(f);w.writerow(['figure','panel','axis','printed_label','fitted_pixel','eye_pixel']);w.writerows(rows)
(base/'notes.md').write_text('''# FC-6D independent reading

Evidence: packet/p0134.png and supplied protocol/index only, no other reading. This page is 3167 x 4221 px, unrotated (narrower than the other three).

Legend confirmed: plus 4695/73.0; down triangle 3814/75.2; square 2934/66.8; circle 1761/70.3; up triangle 147/71.9. Printed numbers are 3814 and 147; retain supplied n3814/n147. Legend header shows sigma and gamma without units; units follow the upper stress axis/report context.

Calibration: the upper initial detection incorrectly selected the title-box lower border as 5000, giving y RMS 84.347 psf. Changed upper box to use actual labeled 0 through 4000 grid lines; the 5000 line is largely covered by the title inset and excluded. Another run caught the thin horizontal scratch below the actual 0 frame; raising frame-frac from .4 to .7 excludes this short track and finds the actual sloping frame (v=2219.5-.0110*u). Final P1 RMS x 1.079 thousandths, y 8.624 psf. P2 RMS x 1.142, y .068 thousandths; both less than .5% axis span. All actual grid lines confirmed on the image. Wider first displacement bay again contributes to affine horizontal residual.

Lower frame is 0 (unlabelled top) to -300; -100 and -200 have printed labels but no drawn horizontal grid lines. The tool's predicted intermediate lines were checked against those label/leader heights, then their synthetic anchors were excluded from the fit using ../prune_predicted.py; they describe nominal scale positions only. Eye checks include six displacement lines and five upper stress lines, plus lower -100/-200/-300 labels and inferred-zero top frame. Checks for -100/-200 refer to label/short leader location rather than a nonexistent grid stroke, with several-pixel uncertainty. No predicted line is misrepresented as detected ink.

Markers read first on labeled zoom-3 crops, white interiors refine open symbols where contours permit. Broken/interrupted centers and grid/frame symbols have wide bounds. The very small n147 upper symbols near the frame are separate markers; their bases/side contours must never be used as trace samples. There are 24 identifiable upper triangles. A possible n147 observation near x=50 (u~1060, v~2195) cannot be found separately from the vertical grid/frame and is omitted with this note. The apparent triangular white space at u1032 is a frame/curve corner, not accepted as a marker. Lower triangle series has 25 identifiable markers including rebound outside the plot's 250 gridline. Upper square near u935, v1846 lies above its author-fit curve and is preserved as an observation, not forced onto the line. Several other circles/squares also sit off their fitted line.

Lower plus and down-triangle symbols often touch at the down-triangle apex/plus stem. Their separate crossbars and downward apices are identifiable away from the grid; bounds 6 px retained, 8 px on frame/grid. The down triangle at about u1365 has a split interior on the 100 gridline, not two observations. Up triangle at 150 gridline and the first/last up triangle have partly interrupted contours and wide bounds. There is no lower drawn connecting curve; small local scratches/dashes beside the circle/square/plus rows are not sampled as traces.

Three symbols are identifiable beyond x=250 in the lower inset: n147 up triangle near u2308,v2557 beneath Rebound; square n2934 near u2322,v2828; down triangle n3814 near u2319,v2908. They are retained as rebound observations outside the calibrated plot area, with 5 px bounds and explicit notes. Their relation to the inset text/short square leader should be checked in review; they could be mistaken for notation glyphs, but their shapes and common displacement with the labelled Rebound triangle support the rebound reading. No circle or plus rebound symbol can be separately identified near that same displacement; any such symbol may be hidden by Same Notation As Above (circle expected broadly y~-120 to -150, plus broadly y~-200 to -260). Those symbols are omitted rather than inferred from the text.

Upper traces: actual column dark-run centers selected by manually read guide paths; guides never supply sampled ordinates. Nominal interval 20 px is ~3.37 thousandths. Dash/marker interruptions are preserved as gaps, so larger spacing around symbols is intentional under rule 7. Vertical grid columns avoided. Thick merged ink at horizontal grid crossings uses half its measured vertical run thickness. The first n147 stroke shares the lower frame at very small displacement, so its position is uncertain within the merged thickness. Its later stroke is separate from the frame and from triangle outlines. First/last/peak locations checked against endpoint crops and an explicit pixel ink audit. All corrected feature samples are on dark pixels; endpoints precede final symbol outlines. Rising curves have coincident peak/last roles; plus/n147 broad maxima have wide horizontal peak bounds. No extrapolated trace through white dash gaps.

Files: cal-p1/anchors.csv and calibration.json; cal-p2/anchors.csv and calibration.json; calibration-eye-checks.csv; points-p1.csv, points-p1-native.csv, points-p2.csv, points-p2-native.csv; overlay-p1.png, overlay-p2.png; counts.csv. readings.json, crops, and helper scripts retained for audit/reproduction. Final CSV coordinates supersede approximate guide paths.
''')
