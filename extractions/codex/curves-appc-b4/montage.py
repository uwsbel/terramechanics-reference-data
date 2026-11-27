from PIL import Image,ImageDraw,ImageFont
import csv
from pathlib import Path
for fig,p in [('FC-7B','p0136'),('FC-7C','p0137')]:
 rows=list(csv.DictReader(open(f'out/{fig}/candidates.csv'))); base=Image.open(f'packet/{p}.png').convert('RGB');font=ImageFont.truetype('arial.ttf',15)
 for k in range(0,len(rows),24):
  sheet=Image.new('RGB',(6*240,4*255),'white');d=ImageDraw.Draw(sheet)
  for j,r in enumerate(rows[k:k+24]):
   u,v=float(r['u']),float(r['v']);x,y=(j%6)*240,(j//6)*255
   tile=base.crop((round(u)-35,round(v)-35,round(u)+35,round(v)+35)).resize((210,210));td=ImageDraw.Draw(tile);td.line((99,105,111,105),fill='red');td.line((105,99,105,111),fill='red');sheet.paste(tile,(x,y+30));d.text((x+2,y+4),f"{r['id']}: {u},{v}",fill='blue',font=font)
  sheet.save(f'out/{fig}/sheet-{k//24+1}.png')
