import csv,json,math,numpy as np
from pathlib import Path
from PIL import Image
cfg=json.loads(Path('out/config.json').read_text());report=[]
for fig,c in cfg.items():
 d=Path('out')/fig;rr=list(csv.DictReader((d/'points-p1.csv').open()));nn=list(csv.DictReader((d/'points-p1-native.csv').open()));g=np.asarray(Image.open('packet/'+c['page']+'.png').convert('L'));kn=json.loads((d/'cal-p1'/'verified-knots.json').read_text())
 assert len(rr)==len(nn);assert not kn['rejected_x'] and not kn['rejected_y']
 bad=[]
 for sid in ['mean','upper','lower']:
  tr=[r for r in rr if r['series_id']==sid and r['point_kind']=='trace'];assert len(tr)==11;assert [int(r['sequence']) for r in tr]==list(range(1,12));assert all(float(a['pixel_u'])<float(b['pixel_u']) for a,b in zip(tr,tr[1:]))
  for r in tr:
   u,v=round(float(r['pixel_u'])),round(float(r['pixel_v']));
   if g[v,u]>160:bad.append([sid,r['sequence'],u,v,int(g[v,u])])
 for r in nn:
  for k in ['x_native','y_native','x_read_bound','y_read_bound']:assert math.isfinite(float(r[k]))
 for name in ['calibration-eye-checks.csv','points-p1.csv','points-p1-native.csv','overlay-p1.png','notes.md']:assert (d/name).exists()
 report.append(dict(figure=fig,total=len(rr),trace=33,features=len(rr)-33,white_trace_centres=bad,verified_x=len(kn['x']),verified_y=len(kn['y'])))
 print(report[-1])
Path('out/file-validation.json').write_text(json.dumps(report,indent=2))
