import argparse,csv,json,subprocess,sys
from pathlib import Path
from collections import Counter
import numpy as np
from PIL import Image,ImageDraw
ap=argparse.ArgumentParser(description='Write axis eye checks, verified label coordinates, notes and final native-unit files.')
ap.add_argument('--run',action='store_true');a=ap.parse_args()
if not a.run:raise SystemExit()
p=Path('out/reading.json');data=json.loads(p.read_text(encoding='utf-8'))
centers={'FC-1A':[[1812,2213.5],[1684.5,2233],[1687.5,2055]],'FC-2A':[[1697.5,2328.5],[1880.5,2285]],'FC-3A':[[1645.5,2500],[1618.5,2220.5]],'FC-4A':[[1587.5,2037.5],[1802.5,2571]]}
for fig,c in data.items():
 for s,xy in zip(c['series'].values(),centers[fig]):s['label']=xy
# Further by-eye center refinements, clean fills and open squares with broken outlines.
data['FC-1A']['series']['dr73-88']['markers'][2][:2]=[1783,2135]
data['FC-1A']['series']['dr73-88']['markers'][3][:2]=[1952.5,2058]
data['FC-1A']['series']['dr100-116']['markers'][3][:2]=[1440.5,2482]
data['FC-4A']['series']['dr95']['markers'][2][:2]=[1771,1867]
data['FC-4A']['series']['dr95']['markers'][3][:2]=[2034,1378]
data['FC-4A']['series']['dr95']['markers'][4][:2]=[2283,1348]
data['FC-4A']['series']['dr0']['markers'][4][:2]=[2294,2163]
p.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
subprocess.run([sys.executable,'out/traces.py','--run'],check=True)
summary=[]
for fig,c in data.items():
 out=Path('out',fig);cal=json.loads((out/'cal-p1/calibration.json').read_text());ax=cal['ax'];ay=cal['ay']
 checks=[]
 if fig=='FC-1A':
  ticks=[('x',0,928,3305),('x',2000,1501,3305),('x',4000,2107,3305),('y',0,928,3305),('y',3000,926,2448),('y',6000,924,1578)]
 else:
  idxs={'FC-2A':([0,2,5],[1,3,6]),'FC-3A':([1,3,5],[1,3,6]),'FC-4A':([1,3,5],[1,4,7])}[fig]
  ticks=[(axis,i*1000,*cal['axis_ticks_'+axis][i]) for axis,ids in zip(['x','y'],idxs) for i in ids]
 sheet=Image.new('RGB',(750,6*300),'white');draw=ImageDraw.Draw(sheet);im=Image.open('packet/'+c['page']+'.png').convert('RGB')
 for j,(axis,value,u,v) in enumerate(ticks):
  coeff=ax if axis=='x' else ay;actual=coeff[0]*u+coeff[1]*v+coeff[2]
  fu=(value-coeff[1]*v-coeff[2])/coeff[0] if axis=='x' else u
  fv=(value-coeff[0]*u-coeff[2])/coeff[1] if axis=='y' else v
  note='Printed label read by eye; correct sign, order and axis; tick/frame ink confirmed.'
  if fig=='FC-1A':note+=' Uneven hand-drawn grid; fitted location differs from ink within recorded affine residual.'
  checks.append(dict(figure_id=fig,panel=1,axis=axis,printed_label=str(value),printed_value=value,pixel_u=round(u,2),pixel_v=round(v,2),fitted_pixel_u=round(fu,2),fitted_pixel_v=round(fv,2),native_at_checked_ink=round(actual,3),residual_psf=round(actual-value,3),eye_check='confirmed',note=note))
  if axis=='x':box=(round(u)-100,round(v)-32,round(u)+100,round(v)+95)
  else:box=(round(u)-175,round(v)-50,round(u)+60,round(v)+50)
  crop=im.crop(box);crop=crop.resize((crop.width*2,crop.height*2));sheet.paste(crop,(270,j*300+10))
  draw.text((0,j*300+20),f'{axis}: printed {value}\nObserved ({u:.1f},{v:.1f})\nfit ({fu:.1f},{fv:.1f})\nResidual {actual-value:.2f} psf',fill='black')
  uu=270+(fu-box[0])*2;vv=j*300+10+(fv-box[1])*2
  draw.line([(uu-8,vv),(uu+8,vv)],fill='red',width=2);draw.line([(uu,vv-8),(uu,vv+8)],fill='red',width=2)
 sheet.save(out/'cal-p1/eye-checks.png')
 with (out/'calibration-eye-checks.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)
 subprocess.run([sys.executable,'tools/calibrate_axes.py','apply',str(out/'cal-p1/calibration.json'),str(out/'points-p1.csv'),str(out/'points-p1-native.csv')],check=True)
 subprocess.run([sys.executable,'tools/plot_grid.py','overlay','packet/'+c['page']+'.png','--points',str(out/'points-p1.csv'),'--out',str(out/'overlay-p1.png')],check=True)
 rows=list(csv.DictReader((out/'points-p1.csv').open(encoding='utf-8')))
 counts=Counter((r['series_id'],r['point_kind']) for r in rows)
 lines=['# Independent packet reading: '+fig,'','Read only the supplied page images, introduction, protocol and series identifiers. No external or other-reader extraction consulted. Figure-index reading/notes columns were not used as measurements or identity evidence. All coordinates refer to the unrotated 300 dpi page.','',
 '## Calibration','',f"Affine RMS residuals: x {cal['rms_residual_x']:.3f} psf; y {cal['rms_residual_y']:.3f} psf. Maximum residuals: x {cal['max_residual_x']:.3f}; y {cal['max_residual_y']:.3f} psf.",
 'Six independent printed-label checks (three per axis) are recorded in calibration-eye-checks.csv and visually documented in cal-p1/eye-checks.png. Increasing normal stress is rightward; increasing shear stress is upward. Both quantities use psf.','']
 if fig=='FC-1A':
  lines+=['All grid lines were detected and confirmed. No predicted grid line was used. The x RMS residual is 0.598% of the 4000 psf span, exceeding the 0.5% protocol flag. I changed the box from 920,1570,2110,3315 to 914,1568,2113,3316 and changed bands/dark/fraction from 5/200/0.6 to 9/140/0.5 before reading points. Residual remained about 24 psf because the printed grid is uneven (successive x spacings roughly 285-311 pixels). The residual is retained in all native reading bounds; it has not been concealed by using predicted evenly spaced lines.','']
 else:
  lines+=['There is no interior grid. The supplied detect command was run, but its grid assumption picked up legend borders (and, with sparse thresholds, curves) or interpolated nonexistent interior lines. The rejected trials are not the operative calibration. The operative cal-p1 files use every labeled bottom/left axis tick intersection measured on packet ink and the independently measured frame tilt. The same supplied fit_affine function fits those anchors; apply computes native values and bounds. Axis tick centers are recorded in calibration.json. No predicted interior grid lines are claimed or used. This tick-anchor adaptation is necessary to apply the protocol to these gridless figures.','']
 lines+=['## Series, printed legend and angle associations','']
 for sid,s in c['series'].items():
  lines.append(f"- {sid}: printed angle {s['angle']}; markers {counts[sid,'marker']}, trace samples {counts[sid,'trace']}, features {counts[sid,'feature']} (intercept and printed angle center).")
 if fig=='FC-1A':
  lines+=['','Legend: hollow circle, gamma 46.7 to 47.4 lb/ft^3, Dr .50 to .57; filled circle, gamma 49.2 to 51.1, Dr .73 to .88; upward triangle, gamma 53 to 55.4, Dr 1.0 to 1.16. The lower, middle and upper drawn fits carry 45.5°, 47° and 51° respectively.',
   'The plot triangles point downward. The triangle at (928.3,3169.5) is on the lower dashed fit at the axis, so it is recorded as dr50-57, with a 14 pixel bound for axis overlap and the legend mismatch. The filled circle near (1013,3089) is on the lower dashed fit and is assigned dr50-57 despite its fill. Hollow circles near (1092.4,2916.5) and (1608.6,2412.9) sit by the middle fit and are assigned dr73-88 despite their fill.',
   'The filled circle near (1440.5,2482) lies much closer to the upper fit than to the middle fit; it is assigned dr100-116 by that line neighborhood, with a 7 pixel bound and an explicit identity caveat. It is off the line, so this assignment is less secure than the triangle assignments. The lower circle at (1777.6,2318.6) is close to the vertical grid and fit; its bound is widened to 5 pixels.',
   'The lower fit intercept is obscured by the axis triangle: its feature has a 15 pixel bound. Its first trace sample is the actual first visible dash beyond the triangle, not the triangle outline. The lower solid fit ends before the last circle; the right endpoint is on that line cap rather than on the circle or horizontal grid. No hidden additional marker is inferred.','']
 elif fig=='FC-2A':
  lines+=['','Legend: square, gamma 25.6 to 26.8 lb/ft^3, Dr .33 to .53; hollow circle, gamma 31.7 to 33.1, Dr 1.15 to 1.3. These match the supplied identifiers. The upper square-associated fit carries 49.5°; the lower circle-associated fit carries 46.7°. Assignment follows this page alone. The top square has a broken outline, but its square shape and center remain readable. No symbol identity conflict or hidden marker was observed.','']
 elif fig=='FC-3A':
  lines+=['','Legend: hollow circle, gamma 57.9 to 59.4 lb/ft^3, Dr 0 to .15; square, gamma 75, Dr 1.0 to 1.3. These match the supplied identifiers. The lower circle-associated fit carries 38°; the upper square-associated fit carries 47°. The right-hand extensions are dashed as well as the left-hand intercept extensions. The upper endpoint is on the final dash below the top frame, not the top frame. No symbol identity conflict or hidden marker was observed.','']
 else:
  lines+=['','Legend: square, gamma 81.8 lb/ft^3, Dr .95; hollow circle, gamma 58.7, Dr 0. These match the supplied identifiers. The steep square-associated fit carries 53°; the lower circle-associated fit carries 43°. The two highest square markers are below the steep fit. The steep line continues above the 8000 psf frame; its final dash is included and the last feature/trace native values may therefore exceed the plotted y span. The bottom intercept extension and top extension are dashed; the lower fit also has a dashed right extension. Several square outlines are broken but recognizable; no hidden marker or series conflict was observed.','']
 lines+=['## Ink sampling and bounds','',
 'Markers were read before trace sampling and reviewed at 3x enlargement. Every symbol is retained with its drawn shape. Clean marker centers use 2 pixel bounds; overlap and identity caveats use the stated wider bounds.',
 'Every trace sample is on visible fitted-line ink, excluding all marker neighborhoods. Endpoints were separately checked on enlarged packet crops. Regular targets are every 250 psf from the left, followed by the observed right cap. When a target falls in a dash gap, marker neighborhood or grid interference, the nearest visible line ink is read and the target/actual x difference is noted. No sample was inserted by interpolation into a white gap. Samples on dashed portions are marked dashed. Sample bounds are half the observed line thickness (column thickness, including diagonal projection); endpoint bounds use the adjacent cap stroke width, not marker size. Only the hidden intercept feature uses an extrapolated location with a wide bound.',
 'Sequences are independent within each series and kind. Trace order is left-to-right drawing order. The first and last trace samples also document the monotonic fitted line endpoints; the requested feature rows are intercept and label center. Angle label centers were measured from the printed glyph bounding boxes, including the degree sign.',
 '', 'Files: cal-p1/anchors.csv, cal-p1/calibration.json, cal-p1/eye-checks.png, calibration-eye-checks.csv, points-p1.csv, points-p1-native.csv, overlay-p1.png and notes.md. Additional marker, endpoint and trace crops are retained for review.']
 (out/'notes.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 summary.append(dict(figure_id=fig,rms_x_psf=cal['rms_residual_x'],rms_y_psf=cal['rms_residual_y'],counts={sid:{kind:counts[sid,kind] for kind in ['marker','trace','feature']} for sid in c['series']},angles={sid:s['angle'] for sid,s in c['series'].items()},eye_checks=[(r['axis'],r['printed_value'],r['residual_psf']) for r in checks]))
Path('out/summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
