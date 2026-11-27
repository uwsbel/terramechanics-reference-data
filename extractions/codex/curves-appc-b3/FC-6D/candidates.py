import sys
sys.path.insert(0,'out')
from read_curves import hole_refine
from PIL import Image
import numpy as np
im=np.asarray(Image.open('packet/p0134.png').convert('L'))
cfg={
'lower-up':('triangle-up',[(750,2555),(900,2580),(1350,2575),(1950,2550),(2250,2545)]),
'lower-circle':('circle',[(750,2788),(1000,2800),(1500,2788),(1800,2770),(2250,2759)]),
'lower-square':('square',[(750,2974),(1100,2995),(1500,2980),(1800,2960),(2150,2940),(2250,2926)]),
'lower-down':('triangle-down',[(750,3097),(900,3130),(1150,3140),(1450,3130),(1750,3120),(2000,3110),(2250,3080)]),
'upper-up':('triangle-up',[(810,2203),(1200,2190),(1700,2180),(2240,2175)]),
'upper-down':('triangle-down',[(810,1840),(1000,1600),(1200,1395),(1350,1290),(1500,1213),(1800,1140),(2250,1110)]),
'upper-square':('square',[(820,2000),(1050,1790),(1250,1670),(1500,1540),(1800,1450),(2100,1430),(2250,1425)]),
'upper-circle':('circle',[(810,2080),(1000,1965),(1250,1880),(1500,1830),(1800,1780),(2100,1745),(2250,1735)])}
for name,(sym,guide) in cfg.items():
 us,vs=np.array(guide).T; found=[]
 for u in range(int(us[0]),int(us[-1])+1,8):
  v=int(np.interp(u,us,vs));a,b=hole_refine(im,u,v,sym)
  if (a,b)!=(u,v) and not any(abs(a-x)<8 and abs(b-y)<8 for x,y in found):found.append((a,b))
 print(name,sorted(found))
