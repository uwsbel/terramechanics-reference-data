import argparse,csv,json,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image
ap=argparse.ArgumentParser(description='Verify output structure and ink samples; retain 3x labeled pixel-grid marker crops.')
ap.add_argument('--run',action='store_true');a=ap.parse_args()
if not a.run:raise SystemExit()
data=json.loads(Path('out/reading.json').read_text(encoding='utf-8'))
for fig,c in data.items():
 out=Path('out',fig);rows=list(csv.DictReader((out/'points-p1.csv').open(encoding='utf-8')));native=list(csv.DictReader((out/'points-p1-native.csv').open(encoding='utf-8')))
 assert len(rows)==len(native)
 im=np.asarray(Image.open('packet/'+c['page']+'.png').convert('L'));off=[]
 for r in rows:
  assert r['panel']=='1';assert float(r['u_bound_px'])>0 and float(r['v_bound_px'])>0
  if r['point_kind']=='trace':
   u,v=round(float(r['pixel_u'])),round(float(r['pixel_v']))
   if im[v,u]>=200:off.append((r['series_id'],r['sequence'],u,v,int(im[v,u])))
  if r['point_kind']=='marker':
   u,v=round(float(r['pixel_u'])),round(float(r['pixel_v']));dest=out/'marker-grid';dest.mkdir(exist_ok=True)
   cropfile=dest/(r['series_id']+'-'+r['sequence']+'.png')
   if not cropfile.exists():subprocess.run([sys.executable,'tools/plot_grid.py','crop','packet/'+c['page']+'.png','--box',str(u-40),str(v-40),str(u+40),str(v+40),'--zoom','3','--step','25','--out',str(cropfile)],check=True,capture_output=True)
 for sid in c['series']:
  trace=[r for r in rows if r['series_id']==sid and r['point_kind']=='trace']
  assert all(float(trace[i]['pixel_u'])<float(trace[i+1]['pixel_u']) for i in range(len(trace)-1))
  assert trace[0]['note'].startswith('left end') and trace[-1]['note'].startswith('right end')
  features=[r for r in rows if r['series_id']==sid and r['point_kind']=='feature']
  assert len(features)==2 and features[0]['note'].startswith('intercept') and features[1]['note'].startswith('label: ')
 checks=list(csv.DictReader((out/'calibration-eye-checks.csv').open()));assert len(checks)==6
 assert sum(r['axis']=='x' for r in checks)==3 and sum(r['axis']=='y' for r in checks)==3
 print(fig,'rows',len(rows),'off ink',off)
 assert not off
