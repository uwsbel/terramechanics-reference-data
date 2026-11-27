"""Check tiles for trace samples: a soft crop around each sample (half `half` px, zoom z) with the
sampling line drawn (cyan), ticks every 5 px across the line (labelled every 10 px of u), and the
provisional sample as a small magenta mark. Usage: python sampletiles.py <json> <series> <out> [half z cols]"""
import sys, json
from PIL import Image, ImageDraw, ImageFilter
import fa22lib as L
src, ser, out = sys.argv[1], sys.argv[2], sys.argv[3]
half = int(sys.argv[4]) if len(sys.argv) > 4 else 22
z = float(sys.argv[5]) if len(sys.argv) > 5 else 4
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 7
pts = json.loads(open(src, encoding="utf-8").read())[ser]
page = Image.open(L.PAGE).convert("L")
tiles = []
for m in pts:
    u, v = m["u"], m["v"]
    u0, v0 = int(round(u)) - half, int(round(v)) - half
    t = page.crop((u0 - 3, v0 - 3, u0 + 2 * half + 3, v0 + 2 * half + 3)).filter(ImageFilter.GaussianBlur(0.7)).crop((3, 3, 3 + 2 * half, 3 + 2 * half))
    S = int(2 * half * z)
    t = t.resize((S, S), Image.BICUBIC).convert("RGB")
    t = Image.eval(t, lambda p: 90 + int(p * 165 / 255))
    d = ImageDraw.Draw(t)
    y = (v - v0) * z
    d.line([(0, y), (S, y)], fill=(0, 200, 220), width=1)
    for uu in range(u0, u0 + 2 * half + 1):
        if uu % 5 == 0:
            x = (uu - u0) * z
            d.line([(x, y - (6 if uu % 10 else 10)), (x, y + (6 if uu % 10 else 10))], fill=(0, 150, 200), width=1)
            if uu % 10 == 0:
                d.text((x - 8, y + 10), str(uu), fill=(0, 100, 160))
    x = (u - u0) * z
    d.line([(x, y - 14), (x, y - 4)], fill=(230, 0, 200), width=2); d.line([(x, y + 4), (x, y + 14)], fill=(230, 0, 200), width=2)
    lab = f"{m['e']:+.2f} u{u:.0f} v{v:.0f}"
    d.rectangle([0, 0, 6 * len(lab) + 4, 11], fill=(255, 255, 160)); d.text((2, 0), lab, fill=(0, 0, 0))
    tiles.append(t)
n = len(tiles); rows = (n + cols - 1) // cols; S = tiles[0].size[0] + 4
M = Image.new("RGB", (cols * S, rows * S), (60, 60, 60))
for i, t in enumerate(tiles):
    M.paste(t, ((i % cols) * S, (i // cols) * S))
M.save(out); print("wrote", out, M.size, n)
