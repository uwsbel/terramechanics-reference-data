from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json
p=json.loads(Path('out/final-pixels.json').read_text());c=json.loads(Path('out/config.json').read_text())
items=[('FA-23','upper',7),('FA-47','lower',9),('FA-27','lower',7),('FA-3','lower',3),('FA-27','upper',6),('FA-7','lower',8)]
for fig,s,n in items:
 a=p[fig][s]['points'][n-1];u,v=round(a['u']),round(a['v']);box=(u-60,v-40,u+60,v+40);im=Image.open('packet/'+c[fig]['page']+'.png').convert('RGB').crop(box).resize((600,400),Image.Resampling.NEAREST);d=ImageDraw.Draw(im)
 for x in range((box[0]//10+1)*10,box[2],10):
  px=(x-box[0])*5;d.line((px,0,px,400),fill=(240,130,130),width=1);d.text((px+1,1),str(x),fill='red')
 for y in range((box[1]//10+1)*10,box[3],10):
  py=(y-box[1])*5;d.line((0,py,600,py),fill=(130,130,245),width=1);d.text((1,py+1),str(y),fill='blue')
 px=(a['u']-box[0])*5;py=(a['v']-box[1])*5;d.ellipse((px-4,py-4,px+4,py+4),outline='red',width=2);im.save(f'out/{fig}/last-check-{s}-{n}.png')
