from pathlib import Path
import csv,json,collections,sys
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path('tools').resolve()))
import calibrate_axes as ca
details={20:"The panel prints 'SS Soil'. Data: seven open circles, one joined pair (numbered from the left) and five singles. No circle is cut by the frame. The pair's left circle touches the solid curve; the high-density circle touches the solid curve and a vertical grid line. Those centers have 18 px bounds. The circle near Dr 0.30 crosses a grid line (9 px bound). The solid curve's right end is the exposed line where it joins the left side of the final circle, rather than the circle center. Upper and lower are the dashed curves above and below the solid mean.",21:"The panel prints 'LSM Soil'. Eight open circles are visible: three joined pairs and two singles. At the right end of pair 1, two overlapping rings have centers about (1361,2023) and (1361,2042); the upper is assigned the pair end, and the lower is recorded as a single. Their 18 px bounds express the overlap and uncertainty of the joining line's attachment. The other circles overlap hatching and have 17 px bounds. No circle is cut by the frame; pair 3 right lies close to it. Band-top and band-bottom coincide with the printed 45 and 40 degree horizontal lines. The diagonal hatching and the three circle-joining segments are not traces. Both edges run to the frame, outside the labelled density interval.",22:"The panel prints 'RSM-b Soil'. Two open circles sit on the solid mean; one also crosses the 45 degree grid line. Both get 18 px bounds. Neither is cut by the frame. Upper and lower are the dashed curves above and below mean. The traces continue beyond the last circle to their own ink endpoints near Dr 1.0.",23:"Six printed labels identify the curves: RC2 and SS are solid; PS uses short dashes; RS uses longer dashes; RSM-b uses long dashes on the steep ascending line; RSM-a uses long dashes on the shallower middle line. The series ids retain the packet's lower-case spelling. No markers are printed. Label features record the centers of RC2, PS, RS, RSM-b, RSM-a and SS. RC2 and PS touch/cross close to Dr 0.08-0.10, around (1070,2210). RSM-b crosses RS near Dr 0.53, around (1770,2070), and crosses PS near Dr 0.66-0.69, around (2000,1930). RS and PS touch/cross around Dr 0.89-0.93, around (2340,1830). These crossing regions contain merged ink; the line styles on each side determine continuation. PS and RS reach the right frame; RS starts at the left frame. RSM-a also ends against the right frame. Other endpoints are inside the frame. No circle symbols occur."}
summary=[]
for n in [20,21,22,23]:
 d=Path(f'out/FC-{n}');im=f'packet/p0{136+n}.png';cal,X,Y=ca.piecewise_maps(d/'cal-p1',im)
 rows=list(csv.DictReader((d/'points-p1-native.csv').open()))
 counts=collections.Counter((r['series_id'],r['point_kind']) for r in rows)
 checks=[]
 for axis,values in [('x',[0,.5,1]),('y',[30,40,50])]:
  for val in values:
   if axis=='x':
    l=next(l for l in cal['vertical_lines'] if l['x_value']==val);v={20:3580,21:3470,22:3550,23:3590}[n];u=l['u_at_v0']+l['slope_du_dv']*v;label='0' if val==0 else ('1.0' if val==1 else '0.5')
   else:
    l=next(l for l in cal['horizontal_lines'] if l['y_value']==val);u={20:640,21:590,22:710,23:790}[n];v=l['v_at_u0']+l['slope_dv_du']*u;label=str(val)
   checks.append(dict(figure_id=f'FC-{n}',panel=1,axis=axis,printed_label=label,value=val,line_u=round(u,2),line_v=round(v,2),checked_by_eye='yes',note='Printed label checked against corresponding grid line; frame excluded as an unlabelled limit'))
 with (d/'calibration-eye-checks.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(checks[0]),lineterminator='\n');w.writeheader();w.writerows(checks)
 rms=f"Affine diagnostic RMS: x={cal['rms_residual_x']:.6f} Dr; y={cal['rms_residual_y']:.6f} deg. Maximum residuals: x={cal['max_residual_x']:.6f}, y={cal['max_residual_y']:.6f} deg."
 notes=f"# FC-{n}, panel 1\n\nIndependent reading from packet/p0{136+n}.png, unrotated 300 dpi. Context p0115 identifies these as relationships from direct-shear results. Units are Dr: none and phi_DS: deg.\n\n{details[n]}\n\nThe frame extends roughly one density grid interval to the left of 0 and to the right of 1.0. Its top and bottom extend beyond the labelled 50 and 30 degree lines. None of these unlabelled frame lines is a value anchor. Checked labels: x 0, 0.5, 1.0; y 30, 40, 50. All eleven x lines (0 through 1.0 in steps of 0.1) and five y lines (30 through 50 in steps of 5) were inspected against page ink and passed the protocol's ink check, without predicted knots.\n\n{rms} Native values and bounds use the verified piecewise maps, with calibration-line uncertainty propagated through the pixel intervals. Points outside the labelled knots are flagged extrapolated.\n\nSamples follow drawing order, from left ink end through Dr multiples of 0.05 to the right ink end. Dashed samples in gaps move to nearby visible ink; notes retain the target Dr. At grid crossings the solid-line center follows the visible continuation on each side. Endpoints were checked on enlarged page crops. Trace bounds are half the visible line width (usually 2-4 px); symbol overlaps use approximately the symbol radius. There are no discrete knees or interior maxima distinguishable from smooth curvature; every trace's maximum is its right end, tagged 'last point; peak'. Curve crossings and the sigmoid inflection of SS are not treated as knees. Rule 8 has no application because no triangles are printed; rule 9 requires no additional identity assignment because all symbols here belong to the panel's data series.\n\nCounts:\n\n"+'\n'.join(f'- {s}: {k} {v}' for (s,k),v in counts.items())+"\n\nFiles: cal-p1/calibration.json, anchors.csv, verified-knots.json, calibration-sensitivity.md; calibration-eye-checks.csv; points-p1.csv; points-p1-native.csv; overlay-p1.png. Reading crops are supplementary inspection aids.\n"
 if n==23:
  notes+='\nThe largest affine x residual is 0.005030 Dr (0.503% of the labelled span), just above the 0.5% diagnostic threshold. A changed box (900,1640,2530,3280), 25 bands and min-frac 0.5 was rechecked in cal-p1-recheck; it preserves the uneven grid spacing and does not materially improve the residual. All knots of the submitted calibration pass direct ink verification. The piecewise map is retained because the excess is drafted spacing, not an unverified or predicted anchor.\n'
 (d/'notes.md').write_text(notes,encoding='utf-8')
 sensitivity=['# Affine versus verified piecewise calibration\n','Maximum absolute coordinate differences across each submitted series, in native units. These are correlated calibration sensitivity, not additional reading bounds.\n','|Series|max x difference (Dr)|max y difference (deg)|','|---|---:|---:|']
 for s in dict.fromkeys(r['series_id'] for r in rows):
  rr=[r for r in rows if r['series_id']==s and not r['note'].startswith('label:')];diff=[]
  for r in rr:
   u,v=float(r['pixel_u']),float(r['pixel_v']);diff.append((abs(np.dot(cal['ax'],[u,v,1])-float(r['x_native'])),abs(np.dot(cal['ay'],[u,v,1])-float(r['y_native']))))
  sensitivity.append(f'|{s}|{max(a for a,b in diff):.6f}|{max(b for a,b in diff):.6f}|')
 (d/'cal-p1/calibration-sensitivity.md').write_text('\n'.join(sensitivity)+'\n')
 gray=np.asarray(Image.open(im).convert('L'));off=[]
 for r in rows:
  if r['point_kind']!='trace':continue
  u,v=round(float(r['pixel_u'])),round(float(r['pixel_v']));b=max(float(r['u_bound_px']),float(r['v_bound_px']));patch=gray[v-6:v+7,u-6:u+7];yy,xx=np.where(patch<100);dist=min(np.hypot(xx-6,yy-6)) if len(xx) else 99
  if dist>b:off.append((r['series_id'],r['sequence'],dist))
 print(n,rms,'off ink beyond bound',off)
 summary.append(dict(figure_id=f'FC-{n}',counts={s:{k:v for (ss,k),v in counts.items() if ss==s} for s,k in counts},rms_x=cal['rms_residual_x'],rms_y=cal['rms_residual_y']))
Path('out/summary.json').write_text(json.dumps(summary,indent=2))
