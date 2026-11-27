"""Diagnostic overlay crops: tracked solid-trace row centers (red, clean rows; orange, interpolated or
grid-touching rows) and chained dots (blue, numbered every 5th). Usage: check_overlay.py u0 v0 u1 v1 zoom out.png"""
import sys, csv
import numpy as np
from PIL import Image, ImageDraw
u0, v0, u1, v1, z = map(int, sys.argv[1:6]); out = sys.argv[6]
im = Image.open('packet/p0106.png').convert('RGB').crop((u0, v0, u1, v1))
im = im.resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
im = Image.fromarray((np.array(im) * 0.45 + 140).astype(np.uint8))   # fade the page ink to gray
d = ImageDraw.Draw(im)
for r in csv.DictReader(open('out/F2-45/work/solid-rows.csv')):
    if r['c'] == '': continue
    u, v = float(r['c']), int(r['v'])
    if u0 <= u < u1 and v0 <= v < v1:
        x, y = (u - u0 + 0.5) * z, (v - v0 + 0.5) * z
        col = (230, 0, 0) if r['clean'] == '1' else (255, 150, 0)
        d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=col)
        # run extent
        d.line([((int(r['s']) - u0) * z, y), ((int(r['e']) + 1 - u0) * z, y)], fill=col + (80,), width=1) if False else None
for r in csv.DictReader(open('out/F2-45/work/dots.csv')):
    u, v = float(r['u']), float(r['v'])
    if u0 <= u < u1 and v0 <= v < v1:
        x, y = (u - u0 + 0.5) * z, (v - v0 + 0.5) * z
        d.line([x - 6, y, x + 6, y], fill=(0, 0, 255), width=2); d.line([x, y - 6, x, y + 6], fill=(0, 0, 255), width=2)
        if int(r['k']) % 5 == 0 or int(r['k']) == 1:
            d.text((x + 8, y - 6), r['k'], fill=(0, 0, 200))
im.save(out)
print('wrote', out, im.size)
