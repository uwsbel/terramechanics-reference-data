import csv,json
from pathlib import Path
base=Path('out/FC-6C');checks={1:{'x':(2415,[(0,654),(50,956),(100,1246),(150,1536),(200,1830),(250,2115)]),'y':(640,[(5000,955),(4000,1241),(3000,1540),(2000,1829),(1000,2126),(0,2421)])},2:{'x':(3148,[(0,663),(50,966),(100,1254),(150,1546),(200,1839),(250,2126)]),'y':(660,[(100,2568),(0,2863),(-100,3157)])}}
rows=[]
for panel,axes in checks.items():
 c=json.loads((base/f'cal-p{panel}/calibration.json').read_text())
 for axis,(ref,pts) in axes.items():
  ls=c['vertical_lines' if axis=='x' else 'horizontal_lines']
  for value,eye in pts:
   l=next(l for l in ls if l['x_value' if axis=='x' else 'y_value']==value);fit=l['u_at_v0']+l['slope_du_dv']*ref if axis=='x' else l['v_at_u0']+l['slope_dv_du']*ref
   label='0 (unlabelled zero line)' if panel==2 and axis=='y' and value==0 else value
   rows.append(['FC-6C',panel,axis,label,f'{fit:.2f} at '+('v=' if axis=='x' else 'u=')+str(ref),eye])
with (base/'calibration-eye-checks.csv').open('w',newline='') as f:w=csv.writer(f);w.writerow(['figure','panel','axis','printed_label','fitted_pixel','eye_pixel']);w.writerows(rows)
(base/'notes.md').write_text('''# FC-6C independent reading

Evidence: packet/p0133.png and supplied protocol/index. Unrotated 3213 x 4221 image; no other reading consulted.

Legend confirmed from page: plus 4695/91.0; down triangle 3815/91.0; square 2934/91.0; up triangle 1961/91.0; circle 714/93.3. The numbers are 1961 and 714 as printed, not 1761 and 734. Supplied n1961/n714 IDs retained. Upper range 0 to 5000 psf; lower +100 to -100 thousandths inch.

Calibration eye checks list all six displacement lines and all upper stress levels; lower checks include +100, -100 and the central zero grid line. Only +100/-100 lower ordinate labels are legible/printed on this page; no legible 0 numeral is present beside the middle line, so a third printed y label cannot honestly be checked. Its zero value is inferred from the symmetric frame and central line and explicitly labeled as unlabelled in the checks file. All detected lines confirmed; none predicted. P1 RMS x 0.640 thousandths, y 9.750 psf; P2 x 0.581, y 0.072 thousandths. Neither RMS exceeds 0.5% of span. The slightly wider first displacement bay contributes to horizontal residual; the 3000-psf grid is partly obscured by the down-triangle plateau. Scan has a noticeable tilt, handled by affine calibration.

Markers were read first on labeled zoom-3 crops. White interiors were used to refine open marker centers, with a shape check to distinguish triangle interiors from square interiors in the crowded upper plateau. Centers whose contour is interrupted retain 6 px rather than a falsely precise 2 px bound; other overlapping/frame/grid centers have explicit bounds/notes. All five lower symbol types are identifiable: plus signs lie between square columns and should not be treated as square centers. There are 12 lower plus markers, 13 for each other lower series. First/last circles and triangles/squares lie on the frame/grid; several lower circles touch the zero line. Their outlines are only partly separable there. Lower up-triangle near u1025 has a broken base but a clear upper apex; wide bound retained. No unresolved stacked symbol is guessed. No lower connecting lines are present; short dashes near symbols are not read as curves.

Upper plus first marker is the tiny plus at the 2000-psf gridline near u700; the initial thick curve starts above/right of it. Plus plateau around 4000 psf has shared/doubled ink with the horizontal grid, and portions of its lower parallel stroke cannot be separated from the grid. The dark-run center may cover this merged thickness, with bounds half that thickness. Down-triangle plateau close to 3000 psf also shares grid ink; the square curve below it remains distinguishable by white gap and square markers. Near their last marker columns, inspect shapes rather than vertical proximity alone. The broken down triangle near u881 has a recognizable lower apex, with 7 px bound. Squares near u1743 and the right frame have interrupted interiors, hence wide bounds.

Trace samples are column dark-run centers on the ink, selected using manually read paths, never values interpolated from those paths. Nominal 20 px interval (about 3.42 thousandths) is below 5. Dash/marker exclusions produce wider gaps, deliberately unsampled to honor rule 7. Some sampling is conservative around interrupted outlines. No artificial segment is filled through a white gap. The first/peak/last feature points were checked on zoom-4 start and zoom-3 end crops; final samples stop at bold line ends before the last symbols. The up-triangle has a shallow broad local maximum around u1680; its x bound covers the flat maximum. Flat maxima of other series have broad horizontal bounds. Printed-circle observations have a long nearly flat curve; first/last symbols are separate from its first/last line ink.

Files: cal-p1/anchors.csv and calibration.json; cal-p2/anchors.csv and calibration.json; calibration-eye-checks.csv; points-p1.csv, points-p1-native.csv, points-p2.csv, points-p2-native.csv; overlay-p1.png, overlay-p2.png; counts.csv. readings.json, crops, and helper scripts retained for audit/reproduction.
''')
