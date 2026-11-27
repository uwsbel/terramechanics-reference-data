import sys, json, csv
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path('tools').resolve()))
import calibrate_axes as ca
import plot_grid as pg

META = {
 'FC-10B':('p0143',[(624,3678),(1263,3037),(1857,2503)]),
 'FC-10C':('p0144',[(520,3757),(694,3517),(908,3274),(1125,3042),(1167,3114),(1337,2867),(1544,2688),(1764,2584),(1764,2504)]),
 'FC-11A':('p0145',[(922,3573),(1219,3278),(1558,3014),(1816,2938),(2077,2702)]),
 'FC-11B':('p0146',[(691,3465),(1377,2937),(1377,2915),(2057,2455),(2057,2423)]),
 'FC-11C':('p0149',[(677,3505),(850,3516),(1144,3219),(1355,2977),(1356,2954),(1485,2950),(1746,2870),(1996,2636),(2022,2487),(2022,2452)])}

for fig,(page,pts) in META.items():
 d=Path('out')/fig; im=Image.open(f'packet/{page}.png').convert('RGB')
 sheet=Image.new('RGB',(900,((len(pts)+2)//3)*330),'white'); dr=ImageDraw.Draw(sheet)
 for i,(u,v) in enumerate(pts):
  box=(u-45,v-45,u+45,v+45); dest=d/f'marker-crop-{i+1}.png'
  pg.cmd_crop(SimpleNamespace(image=f'packet/{page}.png',box=box,out=str(dest),zoom=3,step=25))
  x=(i%3)*300;y=(i//3)*330
  sheet.paste(Image.open(dest),(x,y+35));dr.text((x,y),f'{i+1}: box={box}',fill='black')
 sheet.save(d/'marker-sheet.png')
 cal,X,Y=ca.piecewise_maps(d/'cal-p1',f'packet/{page}.png')
 (d/'cal-p1'/'verified-knots.json').write_text(json.dumps(ca.knots_summary(X,Y),indent=2))
 print(fig,'verified',len(X.knots),len(Y.knots),'rejected',[(k['value'],k['reason']) for k in X.rejected+Y.rejected])
 # Eye checks: full bottom and left labels plus the box, at readable native scale.
 vl=cal['vertical_lines'];hl=cal['horizontal_lines']
 bottom=next(l for l in hl if l['y_value']==0)
 def cross(vl,hl):
  u=(vl['u_at_v0']+vl['slope_du_dv']*hl['v_at_u0'])/(1-vl['slope_du_dv']*hl['slope_dv_du'])
  return u,hl['v_at_u0']+hl['slope_dv_du']*u
 sheet=Image.new('RGB',(1080,700),'white');dr=ImageDraw.Draw(sheet)
 for i,l in enumerate(vl):
  u,v=cross(l,bottom); x=(i%4)*270;y=(i//4)*145
  sheet.paste(im.crop((int(u)-130,int(v)-15,int(u)+140,int(v)+115)),(x,y+15))
  dr.text((x,y),f'x knot {l["x_value"]:g} psf at {u:.1f},{v:.1f}',fill='blue')
 for i,l in enumerate(hl):
  u,v=cross(vl[0],l); x=(i%3)*360;y=300+(i//3)*125
  sheet.paste(im.crop((int(u)-270,int(v)-50,int(u)+50,int(v)+40)),(x,y+20))
  dr.text((x,y),f'y knot {l["y_value"]:g} psf at {u:.1f},{v:.1f}',fill='blue')
 sheet.save(d/'label-sheet.png')
 u,v=cross(vl[0],hl[0])
 im.crop((int(u)+600,int(v)-370,int(u)+1530,int(v))).save(d/'box-crop.png')
