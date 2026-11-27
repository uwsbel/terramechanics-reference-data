from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
cfg={80:(450,1300,2380,3830),88:(520,1880,2010,3710),89:(350,2050,2330,3640),90:(630,1500,2250,3700)}
for n,b in cfg.items():
 im=Image.open(f'packet/p{n:04}.png').crop(b)
 d=ImageDraw.Draw(im)
 for u in range((b[0]//100+1)*100,b[2],100):
  d.line((u-b[0],0,u-b[0],im.height),fill='#88ccff',width=1); d.text((u-b[0]+2,8),str(u),fill='red')
 for v in range((b[1]//100+1)*100,b[3],100):
  d.line((0,v-b[1],im.width,v-b[1]),fill='#88ccff',width=1); d.text((2,v-b[1]+2),str(v),fill='red')
 im.save(f'out/read-{n}.png')
