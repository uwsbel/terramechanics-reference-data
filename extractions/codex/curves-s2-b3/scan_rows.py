from PIL import Image
import numpy as np
for page in ['p0102','p0104']:
 a=np.array(Image.open('packet/'+page+'.png').convert('L'))
 vs=[1335,1490,1597,1666,1750,1800,1900,1950,1995,2030,2100,2200,2300,2400,2500,2600,2700,2800,2900,3000,3100,3200,3300] if page=='p0102' else [1840,2000,2200,2400,2500,2600,2700,2800,2900,3000,3100,3140]
 print(page)
 for v in vs:
  u0,u1=(832,1750) if page=='p0102' else (730,2200)
  ids=np.where(a[v,u0:u1]<150)[0]+u0
  rr=np.split(ids,np.where(np.diff(ids)>1)[0]+1)
  print(v,[(int(r[0]),int(r[-1])) for r in rr if len(r)>1])
