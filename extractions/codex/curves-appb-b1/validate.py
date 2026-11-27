from pathlib import Path
import csv,json,hashlib
from collections import Counter
from PIL import Image,ImageDraw
import numpy as np
summary=json.loads(Path('out/summary.json').read_text());qa=[]
for s in summary:
 d=Path('out')/s['figure_id'];j=int(s['figure_id'][-1]);im=Image.open(f'packet/p{j+106:04}.png').convert('RGB');g=np.array(im.convert('L'));rows=list(csv.DictReader((d/'points-p1.csv').open()));native=list(csv.DictReader((d/'points-p1-native.csv').open()));trace=[r for r in rows if r['point_kind']=='trace'];bad=[]
 can=Image.new('RGB',(1000,190*((len(trace)+3)//4)),'white');dr=ImageDraw.Draw(can)
 for i,r in enumerate(trace):
  u,v=[float(r[k]) for k in ['pixel_u','pixel_v']];ink=int(g[round(v),round(u)])
  if ink>=180:bad.append([r['series_id'],r['sequence'],u,v,ink])
  box=(round(u)-18,round(v)-18,round(u)+19,round(v)+19);cr=im.crop(box).resize((148,148));dd=ImageDraw.Draw(cr);cx=(u-box[0])*4;cy=(v-box[1])*4
  dd.line((cx-12,cy,cx-5,cy),fill='red',width=1);dd.line((cx+5,cy,cx+12,cy),fill='red',width=1);dd.line((cx,cy-12,cx,cy-5),fill='red',width=1);dd.line((cx,cy+5,cx,cy+12),fill='red',width=1)
  xx=i%4*250;yy=i//4*190;can.paste(cr,(xx,yy+30));dr.text((xx,yy),f'{r["series_id"]} T{r["sequence"]} ({u:.1f},{v:.1f})',fill='blue')
 can.save(d/'cal-p1'/'trace-ink-checks.png')
 checks=list(csv.DictReader((d/'calibration-eye-checks.csv').open()))
 assert len(checks)==6 and len(rows)==len(native)
 assert all(float(r['u_bound_px'])>0 and float(r['v_bound_px'])>0 for r in rows)
 assert not bad,bad
 K=json.loads((d/'cal-p1'/'verified-knots.json').read_text());assert all(k['verified'] for axis in ['x','y'] for k in K[axis])
 qa.append({'figure_id':s['figure_id'],'rows':len(rows),'trace_centres_on_dark_ink':len(trace),'trace_centres_on_white':len(bad),'verified_x_knots':len(K['x']),'verified_y_knots':len(K['y']),'eye_checks':len(checks)})
 # update tick fit inventory to final tip fits, not preliminary contaminated B7 fits
 cal=json.loads((d/'cal-p1'/'calibration.json').read_text());tf=[]
 for axis,key,sk,bk in [('x','vertical_lines','slope_du_dv','u_at_v0'),('y','horizontal_lines','slope_dv_du','v_at_u0')]:
  for l in cal[key]:
   P=np.array(l['samples']);res=P[:,1]-(l[sk]*P[:,0]+l[bk]);tf.append({'axis':axis,'value':l[axis+'_value'],'slope':l[sk],'intercept':l[bk],'rms_px':float(np.sqrt(np.mean(res*res))),'n':len(P),'source':l['source']})
 with (d/'cal-p1'/'tick-fits.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(tf[0]));w.writeheader();w.writerows(tf)
 # explicit per-series sensitivity demanded by protocol
 sens=list(csv.DictReader((d/'cal-p1'/'calibration-sensitivity.csv').open()));ss=['# Affine versus piecewise calibration sensitivity','','Absolute maxima over markers and trace samples; values use native units. This is a correlated calibration sensitivity, not independent point noise.','','| Series | max |dx| (psi) | max |dy| (kips/in.^2) |','|---|---:|---:|']
 for sid in s['counts']:
  rr=[r for r in sens if r['series_id']==sid and r['point_kind']!='feature'];ss.append(f'| {sid} | {max(abs(float(r["affine_minus_piecewise_x"])) for r in rr):.6f} | {max(abs(float(r["affine_minus_piecewise_y"])) for r in rr):.6f} |')
 (d/'cal-p1'/'calibration-sensitivity.md').write_text('\n'.join(ss)+'\n')
 # eye checks address actual tick identification without claiming text center is precisely on tick
 for r in checks:r['result']='Printed value identifies the measured tick/frame in the ordered sequence; typographic offset is not used as tick position.'
 with (d/'calibration-eye-checks.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)
 with (d/'notes.md').open('a',encoding='utf-8') as f:f.write('\nAxis-label registration: several y-label glyph centers sit modestly below their tick, and terminal x labels can sit inward of the frame corner. Values were assigned from the printed ordered sequence and measured tick ink, never from the text center. Frame label checks use the actual bottom/left frame intersections.\n')
Path('out/validation.json').write_text(json.dumps(qa,indent=2));hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('packet').iterdir() if p.is_file()};Path('out/input-sha256.json').write_text(json.dumps(hashes,indent=2));print(json.dumps(qa,indent=2))
