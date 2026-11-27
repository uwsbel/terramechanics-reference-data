from PIL import Image,ImageDraw
from pathlib import Path
for j in range(3,8):
 p=Path('packet')/f'p{j+106:04}.png'; im=Image.open(p).convert("RGB")
 # full plot crops, reduced to 1400 px tall and coordinate ticks
 box={3:(480,790,2550,3990),4:(520,1040,2610,3950),5:(580,800,2880,4030),6:(540,740,2650,4100),7:(420,800,2790,3980)}[j]
 cr=im.crop(box); cr.thumbnail((1500,1800)); d=ImageDraw.Draw(cr); sx=cr.width/(box[2]-box[0]); sy=cr.height/(box[3]-box[1])
 for u in range((box[0]//100+1)*100,box[2],100):
  x=(u-box[0])*sx; d.line((x,0,x,cr.height),fill=(200,210,240),width=1); d.text((x+1,0),str(u),fill='red')
 for v in range((box[1]//100+1)*100,box[3],100):
  y=(v-box[1])*sy; d.line((0,y,cr.width,y),fill=(200,210,240),width=1); d.text((0,y+1),str(v),fill='red')
 cr.save(f'out/FB-{j}-overview.png')
