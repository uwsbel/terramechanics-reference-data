"""Contact sheet for checking symbol centers by eye: one tile per symbol, zoomed, with the
outer box used (green) and the center (red cross), pixel ticks every 10 px, tile label = id and
the box origin. Usage: python sheet.py <image> centers.csv out.png [--zoom 4] [--cols 6] [--ids a,b]
"""
import csv, sys
from PIL import Image, ImageDraw

img, cp, outp = sys.argv[1:4]
args = sys.argv[4:]
zoom = int(args[args.index('--zoom') + 1]) if '--zoom' in args else 4
cols = int(args[args.index('--cols') + 1]) if '--cols' in args else 6
ids = args[args.index('--ids') + 1].split(',') if '--ids' in args else None
page = Image.open(img).convert('RGB')
rows = [r for r in csv.DictReader(open(cp)) if ids is None or r['id'] in ids]
M = 10
tiles = []
for r in rows:
    u0, v0, u1, v1 = (float(r[k]) for k in ('u0', 'v0', 'u1', 'v1'))
    uc, vc = float(r['uc']), float(r['vc'])
    cu0, cv0 = int(min(u0, uc) - M), int(min(v0, vc) - M)
    cu1, cv1 = int(max(u1, uc) + M), int(max(v1, vc) + M)
    t = page.crop((cu0, cv0, cu1 + 1, cv1 + 1)).resize(((cu1 - cu0 + 1) * zoom, (cv1 - cv0 + 1) * zoom), Image.NEAREST)
    d = ImageDraw.Draw(t)
    for u in range((cu0 // 10 + 1) * 10, cu1 + 1, 10):
        d.line([((u - cu0) * zoom, 0), ((u - cu0) * zoom, 6)], fill=(0, 0, 255))
    for v in range((cv0 // 10 + 1) * 10, cv1 + 1, 10):
        d.line([(0, (v - cv0) * zoom), (6, (v - cv0) * zoom)], fill=(0, 0, 255))
    d.rectangle([((u0 - cu0) * zoom, (v0 - cv0) * zoom), ((u1 + 1 - cu0) * zoom, (v1 + 1 - cv0) * zoom)], outline=(0, 170, 0))
    x, y = (uc + 0.5 - cu0) * zoom, (vc + 0.5 - cv0) * zoom
    d.line([(x - 12, y), (x + 12, y)], fill=(255, 0, 0), width=2)
    d.line([(x, y - 12), (x, y + 12)], fill=(255, 0, 0), width=2)
    lab = Image.new('RGB', (t.width, 16), 'white')
    ImageDraw.Draw(lab).text((2, 2), '%s %d,%d' % (r['id'], cu0, cv0), fill=(0, 0, 0))
    tt = Image.new('RGB', (t.width, t.height + 16), 'white')
    tt.paste(lab, (0, 0)); tt.paste(t, (0, 16))
    tiles.append(tt)
tw = max(t.width for t in tiles) + 8
th = max(t.height for t in tiles) + 8
nr = (len(tiles) + cols - 1) // cols
sheet = Image.new('RGB', (tw * cols, th * nr), (220, 220, 220))
for k, t in enumerate(tiles):
    sheet.paste(t, ((k % cols) * tw, (k // cols) * th))
sheet.save(outp)
print('wrote', outp, sheet.size)
