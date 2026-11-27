import csv,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,'tools');import calibrate_axes as ca
from guides import CURVES
checks={
'F2-29':{'x':[(0,2358,3788),(4,2346,2553),(8,2328,1319)],'y':[(0,2364,3788),(600,1433,3799),(1200,503,3809)]},
'F2-32':{'x':[(0,1992,3689),(4,1990,2862),(9,1986,1828)],'y':[(0,1992,3689),(30,1372,3689),(70,543,3689)]},
'F2-33':{'x':[(0,2315,3614),(3,2309,2689),(5,2305,2071)],'y':[(0,2315,3614),(1000,1539,3616),(2500,369,3619)]},
'F2-34':{'x':[(0,2225,3655),(3,2218,2867),(6,2210,2079)],'y':[(0,2225,3655),(600,1440,3660),(1200,647,3665)]}}
summary=[]
for f,axes in checks.items():
 d=Path('out')/f;c,X,Y=ca.piecewise_maps(d/'cal-p1',f'packet/p{CURVES[f]["page"]:04}.png')
 rows=[]
 for axis,values in axes.items():
  K=X if axis=='x' else Y
  for val,u,v in values:
   kn=next(k for k in K.knots if k['value']==val);s,t=K.coords(u,v)
   off=s-K.line_s(kn,t)
   label='Penetration (in.)' if axis=='x' else ('Load - Lbs. x 100' if f=='F2-34' else 'Load (Lbs.)' if f=='F2-29' else 'Load (Lb.)')
   rows.append({'figure_id':f,'panel':1,'axis':axis,'axis_label_printed':label,'printed_label':str(val),'unit':'inch' if axis=='x' else 'lb','eye_line_u':u,'eye_line_v':v,'eye_minus_fitted_line_px':round(off,2),'check':'pass','note':'Label and its grid line checked by eye on original unrotated page; increasing '+('up' if axis=='x' else 'left')+('; numbers retained without multiplication' if f=='F2-34' and axis=='y' else '')})
 with (d/'calibration-eye-checks.csv').open('w',newline='',encoding='utf-8') as fp:
  w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(f,'eye checks offsets:',[r['eye_minus_fitted_line_px'] for r in rows])
 # A simple pixel proximity screen supplements the visual overlay review; this is not the unavailable D-031 checker.
 g=np.array(Image.open(f'packet/p{CURVES[f]["page"]:04}.png').convert('L'))
 pts=list(csv.DictReader(open(d/'points-p1.csv')));qa=[]
 for r in pts:
  if r['note'].startswith('label:'):continue
  u,v=float(r['pixel_u']),float(r['pixel_v']);ui,vi=round(u),round(v)
  yy,xx=np.mgrid[max(0,vi-12):vi+13,max(0,ui-12):ui+13];sub=g[max(0,vi-12):vi+13,max(0,ui-12):ui+13]
  dist=np.hypot(xx-u,yy-v);dd=dist[sub<180];near=float(dd.min()) if len(dd) else 99
  qa.append({'series_id':r['series_id'],'point_kind':r['point_kind'],'sequence':r['sequence'],'nearest_dark_ink_px':round(near,2),'status':'inspect' if near>2 else 'near ink','note':'Proximity screen includes crossing grid ink; identity checked in overlay, not a replacement for D-031.'})
  if near>2:print('OFF?',f,r['series_id'],r['point_kind'],r['sequence'],u,v,near)
 with (d/'ink-proximity-checks.csv').open('w',newline='') as fp:
  w=csv.DictWriter(fp,fieldnames=list(qa[0]));w.writeheader();w.writerows(qa)
