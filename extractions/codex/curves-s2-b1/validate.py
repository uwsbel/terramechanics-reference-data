import csv,json,math
from pathlib import Path
from PIL import Image
summary=json.load(open('out/summary.json'))
for f,v in summary.items():
 d=Path('out')/f
 for fn in ['points-p1.csv','points-p1-native.csv','calibration-eye-checks.csv','overlay-p1.png','notes.md','cal-p1/calibration.json','cal-p1/anchors.csv','cal-p1/verified-knots.json']:assert(d/fn).exists(),(f,fn)
 p=list(csv.DictReader(open(d/'points-p1.csv')));n=list(csv.DictReader(open(d/'points-p1-native.csv')))
 assert len(p)==len(n)==v['total_points']
 assert all(int(r['panel'])==1 and r['symbol']=='' for r in p)
 assert all(float(r['u_bound_px'])>0 and float(r['v_bound_px'])>0 for r in p)
 assert all(math.isfinite(float(r[k])) for r in n for k in ['x_native','y_native','x_read_bound','y_read_bound'])
 assert all(r['cal_model'].startswith('piecewise') for r in n)
 for s in v['counts']:
  q=[r for r in p if r['series_id']==s];assert [int(r['sequence']) for r in q]==list(range(1,len(q)+1))
  kinds={r['note'].split(';')[0] for r in q if r['point_kind']=='feature'}
  if s not in ['fit','bce']:assert {'first','last','peak'}<=kinds,(f,s,kinds)
 eye=list(csv.DictReader(open(d/'calibration-eye-checks.csv')));assert len(eye)==6
 print(f,len(p),'points; overlay',Image.open(d/'overlay-p1.png').size,'all file checks pass')
 # Inspectable detail of the final point overlay, same page orientation.
 im=Image.open(d/'overlay-p1.png')
 box={'F2-29':(1950,3420,2390,3820),'F2-32':(870,2170,1090,2500),'F2-33':(870,2470,1130,2780),'F2-34':(1760,2880,2230,3140)}[f]
 im.crop(box).resize(((box[2]-box[0])*2,(box[3]-box[1])*2)).save(d/'final-detail.png')
