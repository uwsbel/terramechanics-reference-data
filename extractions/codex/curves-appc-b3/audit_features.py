from PIL import Image
import numpy as np,csv,sys
sys.path.insert(0,'out');from read_curves import dark_runs
for fig,page in [('FC-5B','p0130'),('FC-6B','p0132'),('FC-6C','p0133'),('FC-6D','p0134')]:
 im=np.asarray(Image.open('packet/'+page+'.png').convert('L'))
 for r in csv.DictReader(open('out/'+fig+'/points-p1.csv')):
  if r['point_kind']!='feature':continue
  u,v=round(float(r['pixel_u'])),round(float(r['pixel_v']))
  if im[v,u]<200:continue
  print(fig,r['series_id'],r['note'],u,v)
  for x in range(u-8,u+9,2):
   print(x,[(round(c+v-12,1),w) for c,w in dark_runs(im[v-12:v+13,x]<200)])
