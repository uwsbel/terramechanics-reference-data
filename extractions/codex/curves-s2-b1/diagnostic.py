import sys,json,csv
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,'tools');import calibrate_axes as ca
from guides import CURVES

def grid_mask(c,shape):
 mask=np.zeros(shape,dtype=bool)
 vv=np.arange(shape[0]);uu=np.arange(shape[1])
 for l in c['vertical_lines']:
  us=l['u_at_v0']+l['slope_du_dv']*vv
  for dv in range(-7,8):
   ix=np.clip(np.rint(us).astype(int)+dv,0,shape[1]-1); mask[vv,ix]=True
 for l in c['horizontal_lines']:
  vs=l['v_at_u0']+l['slope_dv_du']*uu
  for dv in range(-7,8):
   iy=np.clip(np.rint(vs).astype(int)+dv,0,shape[0]-1); mask[iy,uu]=True
 return mask
for f,s in CURVES.items():
 c=json.load(open(f'out/{f}/cal-p1/calibration.json'));g=np.array(Image.open(f'packet/p{s["page"]:04}.png').convert('L'));mask=grid_mask(c,g.shape)
 print('\n',f)
 vs=range(1400,3700,100) if f=='F2-29' else range(2250,3650,100) if f=='F2-33' else range(1550,3650,100) if f=='F2-34' else range(2250,3650,100)
 for v in vs:
  idx=np.flatnonzero((g[v]<150)&~mask[v]);groups=np.split(idx,np.where(np.diff(idx)>1)[0]+1)
  gs=[(round(a.mean(),1),len(a)) for a in groups if len(a)>=3 and c['box'][0]+20<a.mean()<c['box'][2]-20]
  print(v,gs)
