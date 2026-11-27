from PIL import Image,ImageDraw
from pathlib import Path
import json,math
p=json.loads(Path('out/final-pixels.json').read_text());c=json.loads(Path('out/config.json').read_text())
for fig in c:
 items=[(s,i+1,a) for s in ['upper','lower'] for i,a in enumerate(p[fig][s]['points']) if 'gap:' in a['note']];sheet=Image.new('RGB',(1200,290*math.ceil(len(items)/3)),'white');sd=ImageDraw.Draw(sheet);src=Image.open('packet/'+c[fig]['page']+'.png').convert('RGB')
 for j,(s,n,a) in enumerate(items):
  u,v=round(a['u']),round(a['v']);box=(u-60,v-40,u+60,v+40);im=src.crop(box).resize((360,240),Image.Resampling.NEAREST);d=ImageDraw.Draw(im)
  for x in range((box[0]//10+1)*10,box[2],10):
   px=(x-box[0])*3;d.line((px,0,px,240),fill=(240,140,140));d.text((px+1,0),str(x),fill='red')
  for y in range((box[1]//10+1)*10,box[3],10):
   py=(y-box[1])*3;d.line((0,py,360,py),fill=(140,140,245));d.text((1,py+1),str(y),fill='blue')
  px=(a['u']-box[0])*3;py=(a['v']-box[1])*3;d.ellipse((px-3,py-3,px+3,py+3),outline='red',width=1);xx=(j%3)*400;yy=(j//3)*290;sheet.paste(im,(xx,yy+30));sd.text((xx,yy+4),f'{fig} {s} {n} [{a["u"]:.1f},{a["v"]:.1f}]',fill='black')
 sheet.save(f'out/{fig}/all-gap-checks.png')
