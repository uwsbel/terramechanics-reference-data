from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os, sys
TEMP = Path(os.environ["TEMP"])
PICS = {
    19: (Image.open("packet/p0208.png").convert("L"), 2.5),
    20: (Image.open("packet/p0209.png").convert("L").transpose(Image.Transpose.ROTATE_270), 4558 / 1275),
}
def tile(fig, name, box, step=20, zoom=3):
    im, scale = PICS[fig]
    x0,y0,x1,y1=box
    im = im.transform(((x1-x0)*zoom,(y1-y0)*zoom),Image.Transform.AFFINE,(scale/zoom,0,x0*scale,0,scale/zoom,y0*scale),Image.Resampling.BILINEAR).convert("RGB")
    pad=28
    dst=Image.new("RGB",(im.width+2*pad,im.height+2*pad),"white")
    dst.paste(im,(pad,pad))
    draw=ImageDraw.Draw(dst)
    for x in range(x0,x1+1):
        if x%step: continue
        u=pad+(x-x0)*zoom
        draw.text((u-8,3),str(x),fill=(34,81,170))
        draw.text((u-8,im.height+pad+2),str(x),fill=(34,81,170))
        for v in range(pad,im.height+pad,9):
            if im.getpixel((min(im.width-1,u-pad),v-pad))[0]>170:
                draw.point((u,v),fill=(72,151,221))
    for y in range(y0,y1+1):
        if y%step: continue
        v=pad+(y-y0)*zoom
        draw.text((1,v-6),str(y),fill=(34,81,170))
        draw.text((im.width+pad+2,v-6),str(y),fill=(34,81,170))
        for u in range(pad,im.width+pad,9):
            if im.getpixel((u-pad,min(im.height-1,v-pad)))[0]>170:
                draw.point((u,v),fill=(72,151,221))
    dst.save(TEMP / f"b1-{name}.png")
if __name__=="__main__":
    tile(int(sys.argv[1]),sys.argv[2],tuple(map(int,sys.argv[3:7])),*map(int,sys.argv[7:]))
