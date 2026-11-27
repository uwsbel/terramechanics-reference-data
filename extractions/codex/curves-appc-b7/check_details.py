import json,sys
from pathlib import Path
from PIL import Image,ImageDraw
sys.path.insert(0,'tools');import calibrate_axes as c
ends={'FC-8':[(740,3330),(2110,2248)],'FC-9A':[(649,3569),(1681,2201)],'FC-9B':[(659,3613),(1840,2350)],'FC-9C':[(559,3562),(1741,2190)],'FC-10A':[(634,3597),(1871,2378)]}
Path('out/rough-ends.json').write_text(json.dumps(ends))
for fig,page,box in json.loads(Path('out/config.json').read_text()):
 d=Path('out')/fig;im=Image.open('packet/'+page).convert('RGB');cal=json.loads((d/'cal-p1'/'calibration.json').read_text())
 canvas=Image.new('RGB',(1000,600),'white');dr=ImageDraw.Draw(canvas)
 for i,(axis,vals) in enumerate([('x',[0,3000,7000]),('y',[0,4000,8000])]):
  for j,val in enumerate(vals):
   if axis=='x':
    l=next(z for z in cal['vertical_lines'] if z['x_value']==val);u=l['u_at_v0']+l['slope_du_dv']*(box[3]-20);v=box[3]-20;b=(int(u)-120,int(v)-35,int(u)+165,int(v)+135)
   else:
    l=next(z for z in cal['horizontal_lines'] if z['y_value']==val);u=box[0]+15;v=l['v_at_u0']+l['slope_dv_du']*u;b=(int(u)-230,int(v)-70,int(u)+90,int(v)+70)
   canvas.paste(im.crop(b),(j*330,i*250+30));dr.text((j*330,i*250),f'{axis} {val} psf, crop {b}',fill='black')
 canvas.save(d/'label-checks-inspect.png')
 canvas=Image.new('RGB',(1000,480),'white');dr=ImageDraw.Draw(canvas)
 for j,(u,v) in enumerate(ends[fig]):
  b=(u-80,v-80,u+80,v+80);cr=im.crop(b).resize((480,480));di=ImageDraw.Draw(cr)
  for uu in range((u-80+9)//10*10,u+80,10):
   x=(uu-u+80)*3;di.line((x,0,x,480),fill=(190,220,245));di.text((x,0),str(uu),fill='blue')
  for vv in range((v-80+9)//10*10,v+80,10):
   y=(vv-v+80)*3;di.line((0,y,480,y),fill=(190,220,245));di.text((0,y),str(vv),fill='blue')
  canvas.paste(cr,(j*500,0))
 canvas.save(d/'endpoints-inspect.png')
