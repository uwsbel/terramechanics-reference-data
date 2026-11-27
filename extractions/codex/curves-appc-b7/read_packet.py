import sys,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'tools'); import calibrate_axes as c
rough={'FC-8':[(782,3350),(955,3159),(1429,2770),(1596,2550),(1849,2407),(2108,2328)],'FC-9A':[(741,3440),(824,3319),(1075,2973),(1328,2621),(1498,2423),(1667,2272)],'FC-9B':[(951,3290),(1255,3000),(1507,2675),(1850,2350)],'FC-9C':[(557,3620),(639,3465),(724,3340),(852,3237),(982,2994),(1151,2945),(1236,2645),(1408,2626),(1413,2449),(1580,2300),(1752,2305)],'FC-10A':[(841,3427),(1050,3184),(1254,2939),(1462,2759),(1674,2575),(1885,2389)]}
Path('out/rough.json').write_text(json.dumps(rough))
for fig,page,box in json.loads(Path('out/config.json').read_text()):
 d=Path('out')/fig; cal,X,Y=c.piecewise_maps(d/'cal-p1','packet/'+page)
 (d/'cal-p1'/'knots.json').write_text(json.dumps(c.knots_summary(X,Y),indent=2))
 print(fig,'rejected',[(k['value'],k['reason']) for k in X.rejected],[(k['value'],k['reason']) for k in Y.rejected])
 im=Image.open('packet/'+page).convert('RGB'); marks=rough[fig]; canvas=Image.new('RGB',(900,330*((len(marks)+2)//3)),'white');draw=ImageDraw.Draw(canvas)
 for i,(u,v) in enumerate(marks):
  crop=im.crop((u-45,v-45,u+45,v+45)).resize((270,270)); dr=ImageDraw.Draw(crop)
  for uu in range((u-45+9)//10*10,u+45,10):
   x=(uu-u+45)*3;dr.line((x,0,x,270),fill=(170,210,235));dr.text((x+1,0),str(uu),fill='blue')
  for vv in range((v-45+9)//10*10,v+45,10):
   y=(vv-v+45)*3;dr.line((0,y,270,y),fill=(170,210,235));dr.text((0,y+1),str(vv),fill='blue')
  x=(i%3)*300;y=(i//3)*330;canvas.paste(crop,(x,y+25));draw.text((x,y),f'{i+1}: center approx {u},{v}',fill='black')
 canvas.save(d/'markers-inspect.png')
