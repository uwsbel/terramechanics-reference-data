import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ap=argparse.ArgumentParser(description='Make packet-only inspection crops and labeled contact sheets.')
ap.add_argument('--build', action='store_true')
a=ap.parse_args()
if a.build:
    boxes={
      'FC-1A':('p0116',(760,1160,2160,3460)),
      'FC-2A':('p0120',(780,1360,2500,3550)),
      'FC-3A':('p0123',(760,1310,2440,3380)),
      'FC-4A':('p0126',(760,980,2440,3640))}
    for fig,(page,box) in boxes.items():
        d=Path('out')/fig; d.mkdir(exist_ok=True)
        im=Image.open('packet/'+page+'.png').convert('RGB')
        im.crop(box).save(d/'panel-original.png')
        # Four close inspection quadrants, preserving image pixels.
        u0,v0,u1,v1=box
        for i,(l,t,r,b) in enumerate([(u0,v0,(u0+u1)//2+40,(v0+v1)//2+40),((u0+u1)//2-40,v0,u1,(v0+v1)//2+40),(u0,(v0+v1)//2-40,(u0+u1)//2+40,v1),((u0+u1)//2-40,(v0+v1)//2-40,u1,v1)]):
            c=im.crop((l,t,r,b)); draw=ImageDraw.Draw(c)
            for u in range((l//25+1)*25,r,25):
                draw.line([(u-l,0),(u-l,b-t)],fill=(255,190,190))
                if u%100==0: draw.text((u-l+1,2),str(u),fill='red')
            for v in range((t//25+1)*25,b,25):
                draw.line([(0,v-t),(r-l,v-t)],fill=(190,190,255))
                if v%100==0: draw.text((2,v-t+1),str(v),fill='blue')
            c.save(d/f'quadrant-{i}.png')
