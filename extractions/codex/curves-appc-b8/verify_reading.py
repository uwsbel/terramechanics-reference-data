import csv,json
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
import sys
from types import SimpleNamespace
sys.path.insert(0,str(Path('tools').resolve()))
import plot_grid as pg
results=[]
for d in sorted(Path('out').glob('FC-*')):
 rows=list(csv.DictReader((d/'points-p1-native.csv').open()))
 cal=json.loads((d/'cal-p1'/'calibration.json').read_text());page=cal['image']
 im=Image.open(page).convert('RGB');g=np.asarray(im.convert('L'))
 required=['cal-p1/anchors.csv','cal-p1/calibration.json','cal-p1/verified-knots.json',
 'calibration-eye-checks.csv','points-p1.csv','points-p1-native.csv','overlay-p1.png','notes.md']
 assert all((d/f).is_file() for f in required)
 assert Image.open(d/'overlay-p1.png').size==im.size
 knots=json.loads((d/'cal-p1'/'verified-knots.json').read_text())
 assert len(knots['x'])==8 and len(knots['y'])==9 and not knots['rejected_x'] and not knots['rejected_y']
 checks=list(csv.DictReader((d/'calibration-eye-checks.csv').open()))
 assert sum(c['axis']=='x' for c in checks)==3 and sum(c['axis']=='y' for c in checks)==3
 markers=[r for r in rows if r['point_kind']=='marker'];tr=[r for r in rows if r['point_kind']=='trace'];features=[r for r in rows if r['point_kind']=='feature']
 assert len(features)==3 and sum(r['note']=='intercept' for r in features)==1
 assert [int(r['sequence']) for r in tr]==list(range(1,len(tr)+1))
 assert all(float(tr[i]['pixel_u'])<float(tr[i+1]['pixel_u']) for i in range(len(tr)-1))
 for r in rows:
  assert r['panel']=='1' and r['x_unit']==r['y_unit']=='psf'
  assert float(r['x_read_bound'])>0 and float(r['y_read_bound'])>0
 for r in tr:
  u,v=float(r['pixel_u']),float(r['pixel_v']);gray=int(g[round(v),round(u)])
  assert gray<150,(d.name,'white sample',r['sequence'],u,v,gray)
  target=r['sampling_x_psf']
  if target.isdigit():assert abs(float(r['x_native'])-float(target))<.02
 assert set(r['symbol'] for r in markers)=={'triangle-up'}
 vertices=list(csv.DictReader((d/'triangle-vertices.csv').open()))
 for r,vs in zip(markers,vertices):
  assert float(r['v_bound_px'])+.001>=float(vs['height_px'])/6
 # Final sheets show submitted points, rather than provisional candidates.
 sheet=Image.new('RGB',(1000,((len(tr)+3)//4)*290),'white');dr=ImageDraw.Draw(sheet)
 for i,r in enumerate(tr):
  u,v=float(r['pixel_u']),float(r['pixel_v']);box=[round(u)-40,round(v)-40,round(u)+40,round(v)+40]
  pg.cmd_crop(SimpleNamespace(image=page,box=box,out=str(d/f'trace-crop-{i+1}.png'),zoom=3,step=25))
  crop=Image.open(d/f'trace-crop-{i+1}.png');cd=ImageDraw.Draw(crop)
  x,y=(u-box[0])*3,(v-box[1])*3;cd.ellipse((x-3,y-3,x+3,y+3),outline='lime',width=1)
  ox=i%4*250;oy=i//4*290;sheet.paste(crop,(ox,oy+35));dr.text((ox,oy),f't{r["sequence"]} x={float(r["x_native"]):.2f}; ({u:.1f},{v:.1f})',fill='black')
 sheet.save(d/'submitted-trace-sheet.png')
 sheet.save(d/'trace-sheet.png')
 ov=Image.open(d/'overlay-p1.png');box=(cal['box'][0]-100,2400,min(cal['box'][2],2250),cal['box'][3]+100)
 crop=ov.crop(box);crop.thumbnail((1000,1200));crop.save(d/'overlay-detail.png')
 results.append({'figure_id':d.name,'files_present':True,'calibration_verified':True,'six_label_checks':True,
 'triangle_centroid_bounds_pass':True,'all_trace_centres_on_dark_ink':True,'fixed_x_samples_pass':True,
 'markers':len(markers),'traces':len(tr),'features':len(features),'page_size':im.size})
Path('out/verification.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
