"""Verification sheet: for each reading (readings.csv), a 56x56 px window around the center at
zoom 4, a red cross at the center and a green rectangle for the bounds. Usage:
python verify_sheet.py <image> readings.csv out.png [--ids a,b] [--cols 10]"""
import csv, sys
from PIL import Image, ImageDraw

img, rp, outp = sys.argv[1:4]
args = sys.argv[4:]
ids = args[args.index('--ids') + 1].split(',') if '--ids' in args else None
cols = int(args[args.index('--cols') + 1]) if '--cols' in args else 10
Z, H = 4, 28
page = Image.open(img).convert('RGB')
tiles = []
for r in csv.DictReader(open(rp)):
    if ids and r['id'] not in ids:
        continue
    uc, vc = float(r['pixel_u']), float(r['pixel_v'])
    ub, vb = float(r['u_bound_px']), float(r['v_bound_px'])
    cu0, cv0 = int(round(uc)) - H, int(round(vc)) - H
    t = page.crop((cu0, cv0, cu0 + 2 * H + 1, cv0 + 2 * H + 1)).resize(((2 * H + 1) * Z, (2 * H + 1) * Z), Image.NEAREST)
    d = ImageDraw.Draw(t)
    x, y = (uc + 0.5 - cu0) * Z, (vc + 0.5 - cv0) * Z
    d.rectangle([x - ub * Z, y - vb * Z, x + ub * Z, y + vb * Z], outline=(0, 170, 0), width=2)
    d.line([(x - 14, y), (x + 14, y)], fill=(255, 0, 0), width=2)
    d.line([(x, y - 14), (x, y + 14)], fill=(255, 0, 0), width=2)
    tt = Image.new('RGB', (t.width, t.height + 14), 'white')
    ImageDraw.Draw(tt).text((2, 1), '%s %.1f,%.1f' % (r['id'], uc, vc), fill=(0, 0, 0))
    tt.paste(t, (0, 14))
    tiles.append(tt)
tw, th = tiles[0].width + 6, tiles[0].height + 6
nr = (len(tiles) + cols - 1) // cols
sheet = Image.new('RGB', (tw * cols, th * nr), (200, 200, 200))
for k, t in enumerate(tiles):
    sheet.paste(t, ((k % cols) * tw, (k // cols) * th))
sheet.save(outp)
print('wrote', outp, sheet.size, len(tiles))
