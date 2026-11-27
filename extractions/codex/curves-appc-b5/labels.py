import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
ap=argparse.ArgumentParser(description='Inspect the printed angle label centers.')
ap.add_argument('--run',action='store_true');a=ap.parse_args()
if a.run:
 data=json.loads(Path('out/reading.json').read_text(encoding='utf-8'))
 pts=[(fig,c['page'],sid,s) for fig,c in data.items() for sid,s in c['series'].items()]
 sheet=Image.new('RGB',(1200,1200),'white');d=ImageDraw.Draw(sheet)
 for i,(fig,page,sid,s) in enumerate(pts):
  u,v=s['label'];x=i%3*400;y=i//3*400
  im=Image.open('packet/'+page+'.png').convert('RGB');sheet.paste(im.crop((u-65,v-65,u+65,v+65)).resize((390,390)),(x,y+10));d.text((x,y),fig+' '+sid,fill='red')
  d.line([(x+195,y+10),(x+195,y+400)],fill='red');d.line([(x,y+205),(x+390,y+205)],fill='blue')
 sheet.save('out/angles.png')
