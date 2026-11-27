import csv,json
from pathlib import Path
from PIL import Image
import numpy as np
for fig,page,box in json.loads(Path('out/config.json').read_text()):
 d=Path('out')/fig;rr=list(csv.DictReader((d/'points-p1-native.csv').open()));g=np.asarray(Image.open('packet/'+page).convert('L'));print(fig)
 for r in rr:
  if r['point_kind']=='trace':
   u,v=float(r['pixel_u']),float(r['pixel_v']);tone=g[round(v),round(u)];target=r['x_target_psf'];err=float(r['x_native'])-float(target) if target else None
   print(r['sequence'],r['x_native'],r['y_native'],'uv',u,v,'bounds',r['u_bound_px'],r['v_bound_px'],'ink',tone,'target_error',err)
   assert tone<128,(fig,r)
   if target:assert abs(err)<0.025,(fig,r)
 for r in rr:
  assert int(r['panel'])==1
  assert float(r['u_bound_px'])>0 and float(r['v_bound_px'])>0
  if r['point_kind']=='marker':assert r['symbol']=='triangle-up' and float(r['v_bound_px'])>=4
 assert (d/'points-p1.csv').read_bytes()==(d/'points-p1-native.csv').read_bytes()
 # Make inspectable plot-only overlay at the original pixel scale.
 im=Image.open(d/'overlay-p1.png');im.crop((box[0]-50,box[1]+600,box[2]+50,box[3]+35)).save(d/'overlay-detail.png')
