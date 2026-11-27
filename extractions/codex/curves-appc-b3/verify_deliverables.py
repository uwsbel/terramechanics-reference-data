import csv,json
from pathlib import Path
from PIL import Image
manifest=[]
for fig in ['FC-5B','FC-6B','FC-6C','FC-6D']:
 base=Path('out')/fig;cfg=json.loads((base/'readings.json').read_text());im=Image.open(cfg['image']).convert('L');counts=[]
 for panel in [1,2]:
  rows=list(csv.DictReader((base/f'points-p{panel}.csv').open()));native=list(csv.DictReader((base/f'points-p{panel}-native.csv').open()));assert len(rows)==len(native)
  for sid in cfg['series']:
   rr=[r for r in rows if r['series_id']==sid];seq=[int(r['sequence']) for r in rr];assert seq==list(range(1,len(rr)+1))
   tr=[r for r in rr if r['point_kind']=='trace'];us=[float(r['pixel_u']) for r in tr]
   if len(us)!=len(set(us)):print('duplicate trace u',fig,sid)
   kinds=[sum(r['point_kind']==kind for r in rr) for kind in ['marker','trace','feature']];counts.append([fig,panel,sid,*kinds,len(rr)])
   for r in tr+[r for r in rr if r['point_kind']=='feature']:
    u,v=float(r['pixel_u']),float(r['pixel_v'])
    if im.getpixel((round(u),round(v)))>200:print('WHITE INK SAMPLE',fig,sid,r['point_kind'],u,v)
  cal=json.loads((base/f'cal-p{panel}/calibration.json').read_text());manifest.append([fig,panel,len(rows),cal['rms_residual_x'],cal['rms_residual_y']])
 with (base/'counts.csv').open('w',newline='') as f:w=csv.writer(f);w.writerow(['figure_id','panel','series_id','markers','traces','features','total']);w.writerows(counts)
 for required in ['notes.md','calibration-eye-checks.csv','overlay-p1.png','overlay-p2.png','points-p1.csv','points-p2.csv','points-p1-native.csv','points-p2-native.csv','cal-p1/anchors.csv','cal-p1/calibration.json','cal-p2/anchors.csv','cal-p2/calibration.json']:assert(base/required).exists()
 print(fig,counts)
with Path('out/summary.csv').open('w',newline='') as f:w=csv.writer(f);w.writerow(['figure_id','panel','total_points','rms_x_native','rms_y_native']);w.writerows(manifest)
print(manifest)
