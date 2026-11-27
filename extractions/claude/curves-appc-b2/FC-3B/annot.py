"""Zoomed crop with pixel grid plus candidate centers drawn (green circle + label).
python annot.py <image> u0 v0 u1 v1 out.png zoom step cand.csv
cand.csv columns: label,u,v"""
import sys, csv
from PIL import Image, ImageDraw, ImageFont
img, u0, v0, u1, v1, out, zoom, step, cand = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6], int(sys.argv[7]), int(sys.argv[8]), sys.argv[9]
im = Image.open(img).convert("RGB")
crop = im.crop((u0, v0, u1, v1)).resize(((u1-u0)*zoom, (v1-v0)*zoom), Image.NEAREST)
d = ImageDraw.Draw(crop)
try: font = ImageFont.truetype("arial.ttf", 11*max(1, zoom//2))
except OSError: font = ImageFont.load_default()
for u in range((u0//step+1)*step, u1, step):
    x = (u-u0)*zoom; major = u % (step*4) == 0
    d.line([(x,0),(x,crop.height)], fill=(255,0,0) if major else (255,170,170), width=1)
    if major: d.text((x+2,2), str(u), fill=(200,0,0), font=font)
for v in range((v0//step+1)*step, v1, step):
    y = (v-v0)*zoom; major = v % (step*4) == 0
    d.line([(0,y),(crop.width,y)], fill=(0,0,255) if major else (170,170,255), width=1)
    if major: d.text((2,y+2), str(v), fill=(0,0,200), font=font)
with open(cand, newline="") as f:
    for r in csv.DictReader(f):
        u, v = float(r["u"]), float(r["v"])
        if not (u0 <= u < u1 and v0 <= v < v1): continue
        x, y = (u-u0)*zoom, (v-v0)*zoom
        d.ellipse([x-4,y-4,x+4,y+4], outline=(0,170,0), width=2)
        d.line([(x-12,y),(x+12,y)], fill=(0,170,0), width=1); d.line([(x,y-12),(x,y+12)], fill=(0,170,0), width=1)
        d.text((x+6,y-16), r["label"], fill=(0,120,0), font=font)
crop.save(out); print("wrote", out, crop.size)
