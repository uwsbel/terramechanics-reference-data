from PIL import Image
import numpy as np,json,csv
for fig,p,ids in [('FC-7B','p0136',[21,27,31,38,44,51,57,63,67,73,79]),('FC-7C','p0137',[1,26,32,38,44,50,56,62,68,74,80,86])]:
 cal=json.load(open(f'out/{fig}/cal-p1/calibration.json'));g=np.array(Image.open(f'packet/{p}.png').convert('L'));rs={int(r['id']):r for r in csv.DictReader(open(f'out/{fig}/candidates.csv'))}
 print(fig)
 for i in ids:
  r=rs[i];u,v=round(float(r['u'])),round(float(r['v']));us=np.arange(u-24,u+25);vs=np.arange(v-23,v+24);m=g[v-23:v+24,u-24:u+25]<150
  for l in cal['vertical_lines']:m &= abs(us[None,:]-(l['u_at_v0']+l['slope_du_dv']*vs[:,None]))>5
  for l in cal['horizontal_lines']:m &= abs(vs[:,None]-(l['v_at_u0']+l['slope_dv_du']*us[None,:]))>5
  ux=us[m.sum(axis=0)>=9];vy=vs[m.sum(axis=1)>=9]
  print(i,((ux.min()+ux.max())/2,(vy.min()+vy.max())/2) if len(ux) and len(vy) else 'none')
