from PIL import Image
import numpy as np,json
im=np.array(Image.open('packet/p0080.png').convert('L'))
c=json.load(open('out/F2-29/cal-p1/calibration.json'))
for v in range(1340,3790,100):
 a=im[v,450:2370]<180
 for l in c['vertical_lines']:
  u=l['u_at_v0']+l['slope_du_dv']*v;a[max(0,int(u)-450-9):max(0,int(u)-450+10)]=False
 if 2940<v<3690:a[700-450:1070-450]=False
 idx=np.flatnonzero(a);groups=np.split(idx,np.where(np.diff(idx)>1)[0]+1)
 print(v,[(round(g.mean()+450,1),len(g)) for g in groups if len(g)>=3])
