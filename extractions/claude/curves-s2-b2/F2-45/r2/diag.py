"""Diagnostic crop: page ink faded to gray, solid-trace row centers (red clean, orange flagged), dots
(blue crosses, numbered every 5th), and samples from a points CSV (green boxes = bounds), with a pixel
grid every 25 px labeled in page pixels.
Usage: diag.py u0 v0 u1 v1 zoom out.png [points.csv]"""
import sys, csv, os
import numpy as np
from PIL import Image, ImageDraw

u0, v0, u1, v1, z = map(int, sys.argv[1:6])
out = sys.argv[6]
pts = sys.argv[7] if len(sys.argv) > 7 else None
im = Image.open('packet/p0106.png').convert('RGB').crop((u0, v0, u1, v1))
im = im.resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
im = Image.fromarray((np.array(im) * 0.55 + 110).astype(np.uint8))
d = ImageDraw.Draw(im)
for g in range((u0 // 25 + 1) * 25, u1, 25):
    x = (g - u0) * z
    d.line([x, 0, x, im.size[1]], fill=(255, 200, 200) if g % 100 else (255, 120, 120))
    if g % 100 == 0:
        d.text((x + 2, 2), str(g), fill=(200, 0, 0))
for g in range((v0 // 25 + 1) * 25, v1, 25):
    y = (g - v0) * z
    d.line([0, y, im.size[0], y], fill=(200, 200, 255) if g % 100 else (120, 120, 255))
    if g % 100 == 0:
        d.text((2, y + 2), str(g), fill=(0, 0, 200))


def P(u, v):
    return (u - u0 + 0.5) * z, (v - v0 + 0.5) * z


if os.path.exists('out/F2-45/r2/solid-rows.csv') and not pts:
    for r in csv.DictReader(open('out/F2-45/r2/solid-rows.csv')):
        if r['c'] == '':
            continue
        u, v = float(r['c']), int(r['v'])
        if u0 <= u < u1 and v0 <= v < v1:
            x, y = P(u, v)
            col = (230, 0, 0) if r['clean'] == '1' else (255, 150, 0)
            d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=col)
if os.path.exists('out/F2-45/r2/dots.csv') and not pts:
    for r in csv.DictReader(open('out/F2-45/r2/dots.csv')):
        u, v = float(r['u']), float(r['v'])
        if u0 <= u < u1 and v0 <= v < v1:
            x, y = P(u, v)
            d.line([x - 6, y, x + 6, y], fill=(0, 0, 255), width=2)
            d.line([x, y - 6, x, y + 6], fill=(0, 0, 255), width=2)
            if int(r['k']) % 5 == 0 or int(r['k']) == 1:
                d.text((x + 8, y - 6), r['k'], fill=(0, 0, 200))
if pts:
    for r in csv.DictReader(open(pts)):
        u, v = float(r['pixel_u']), float(r['pixel_v'])
        if not (u0 <= u < u1 and v0 <= v < v1):
            continue
        bu, bv = float(r['u_bound_px']), float(r['v_bound_px'])
        x, y = P(u, v)
        col = (0, 160, 0) if r['series_id'] == 'lpt95' else (0, 0, 230)
        if r['point_kind'] == 'feature':
            col = (220, 0, 220)
        d.rectangle([x - bu * z, y - bv * z, x + bu * z, y + bv * z], outline=col, width=2)
        d.line([x - 4, y, x + 4, y], fill=col, width=2)
        d.line([x, y - 4, x, y + 4], fill=col, width=2)
        tag = r['sequence'] if r['point_kind'] == 'trace' else 'F' + r['sequence']
        d.text((x + bu * z + 3, y - 6), tag, fill=col)
im.save(out)
print('wrote', out, im.size)
