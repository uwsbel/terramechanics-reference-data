import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
ap=argparse.ArgumentParser(description='Review fitted-line endpoints from unaltered packet pixels.')
ap.add_argument('--run',action='store_true');a=ap.parse_args()
if a.run:
 data=json.loads(Path('out/reading.json').read_text(encoding='utf-8'))
 for fig,c in data.items():
  im=Image.open('packet/'+c['page']+'.png').convert('RGB');ss=list(c['series'].items())
  sheet=Image.new('RGB',(len(ss)*450,950),'white');d=ImageDraw.Draw(sheet)
  for i,(sid,s) in enumerate(ss):
   for j,(u,v) in enumerate(s['line']):
    l=u-55;t=v-55
    crop=im.crop((l,t,u+55,v+55)).resize((440,440));sheet.paste(crop,(i*450,j*475+30))
    d.text((i*450,j*475),f'{sid} {"left" if j==0 else "right"} seed ({u},{v})',fill='black')
    for uu in range((l//10+1)*10,u+55,10):
     x=i*450+(uu-l)*4;d.line([(x,j*475+30),(x,j*475+470)],fill=(255,130,130));d.text((x,j*475+30),str(uu),fill='red')
    for vv in range((t//10+1)*10,v+55,10):
     y=j*475+30+(vv-t)*4;d.line([(i*450,y),(i*450+440,y)],fill=(130,130,255));d.text((i*450,y),str(vv),fill='blue')
  sheet.save(Path('out',fig,'endpoints.png'))
