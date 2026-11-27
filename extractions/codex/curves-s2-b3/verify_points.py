import csv,json
from PIL import Image
import numpy as np
for fig,page in [('F2-42','p0102'),('F2-44','p0104')]:
 rows=list(csv.DictReader(open('out/'+fig+'/points-p1-native.csv')))
 a=np.array(Image.open('packet/'+page+'.png').convert('L'))
 print(fig)
 print('Features:')
 for r in rows:
  if r['point_kind']=='feature':print(r['series_id'],r['sequence'],r['pixel_u'],r['pixel_v'],r['x_native'],r['y_native'],r['u_bound_px'],r['v_bound_px'],r['note'][:75])
 print('nonblack centers',[(r['series_id'],r['sequence']) for r in rows if a[round(float(r['pixel_v'])),round(float(r['pixel_u']))]>150])
 print('max shifts',sorted(list(csv.DictReader(open('out/'+fig+'/sampling-audit.csv'))),key=lambda r:float(r['move_px']),reverse=True)[:7])
