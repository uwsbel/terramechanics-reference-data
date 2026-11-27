"""Tile zoomed crops of the page around given points, each with a pixel grid (every 10 px, labelled
every 20 px in page pixels) and an optional cross at given marks. Viewing aid only.
Usage: python montage.py <out.png> <half> <zoom> <cols> label:u:v[:mu:mv[;mu:mv...]] ..."""
import sys
from PIL import Image, ImageDraw
import fa22lib as L

out, half, zoom, cols = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
specs = sys.argv[5:]
page = Image.open(L.PAGE).convert("RGB")
tiles = []
for s in specs:
    parts = s.split(":")
    lab, u, v = parts[0], float(parts[1]), float(parts[2])
    marks = []
    if len(parts) > 3:
        rest = ":".join(parts[3:])
        for m in rest.split(";"):
            a, b = m.split(":")
            marks.append((float(a), float(b)))
    u0, v0 = int(round(u)) - half, int(round(v)) - half
    t = page.crop((u0, v0, u0 + 2 * half, v0 + 2 * half)).resize((2 * half * zoom, 2 * half * zoom), Image.NEAREST)
    d = ImageDraw.Draw(t)
    for k in range(0, 2 * half + 1):
        if (u0 + k) % 10 == 0:
            d.line([(k * zoom, 0), (k * zoom, 2 * half * zoom)], fill=(255, 150, 150) if (u0 + k) % 20 else (255, 0, 0), width=1)
            if (u0 + k) % 20 == 0:
                d.text((k * zoom + 2, 2), str(u0 + k), fill=(220, 0, 0))
        if (v0 + k) % 10 == 0:
            d.line([(0, k * zoom), (2 * half * zoom, k * zoom)], fill=(150, 150, 255) if (v0 + k) % 20 else (0, 0, 255), width=1)
            if (v0 + k) % 20 == 0:
                d.text((2, k * zoom + 2), str(v0 + k), fill=(0, 0, 220))
    for (mu, mv) in marks:
        x, y = (mu - u0) * zoom, (mv - v0) * zoom
        d.line([(x - 8, y), (x + 8, y)], fill=(0, 200, 0), width=2)
        d.line([(x, y - 8), (x, y + 8)], fill=(0, 200, 0), width=2)
    d.rectangle([0, 2 * half * zoom - 16, 2 * half * zoom, 2 * half * zoom], fill=(255, 255, 200))
    d.text((4, 2 * half * zoom - 14), lab, fill=(0, 0, 0))
    tiles.append(t)
n = len(tiles); rows = (n + cols - 1) // cols
S = 2 * half * zoom + 6
M = Image.new("RGB", (cols * S, rows * S), (90, 90, 90))
for i, t in enumerate(tiles):
    M.paste(t, ((i % cols) * S, (i // cols) * S))
M.save(out)
print("wrote", out, M.size)
