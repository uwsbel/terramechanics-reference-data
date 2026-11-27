"""Tiles of soft-rendered crops (half-size `half` around each point), zoom z, 10 px ticks labelled
every 20 px, tiled `cols` per row. Viewing aid only. Usage: python softtiles.py out half z cols label:u:v ..."""
import sys
from PIL import Image, ImageDraw, ImageFilter
import fa22lib as L
out, half, z, cols = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
page = Image.open(L.PAGE).convert("L")
tiles = []
for s in sys.argv[5:]:
    parts = s.split(":"); lab, u, v = parts[0], int(float(parts[1])), int(float(parts[2]))
    mk = (float(parts[3]), float(parts[4])) if len(parts) > 4 else None
    u0, v0 = u - half, v - half
    t = page.crop((u0 - 4, v0 - 4, u0 + 2 * half + 4, v0 + 2 * half + 4)).filter(ImageFilter.GaussianBlur(0.9)).crop((4, 4, 4 + 2 * half, 4 + 2 * half))
    S = int(2 * half * z)
    t = t.resize((S, S), Image.BICUBIC).convert("RGB")
    d = ImageDraw.Draw(t)
    for k in range(2 * half + 1):
        if (u0 + k) % 10 == 0:
            x = k * z; d.line([(x, 0), (x, 6 if (u0 + k) % 20 else 12)], fill=(255, 0, 0), width=1); d.line([(x, S - (6 if (u0 + k) % 20 else 12)), (x, S)], fill=(255, 0, 0))
            if (u0 + k) % 20 == 0: d.text((x + 2, 10), str(u0 + k), fill=(220, 0, 0))
        if (v0 + k) % 10 == 0:
            y = k * z; d.line([(0, y), (6 if (v0 + k) % 20 else 12, y)], fill=(0, 0, 255)); d.line([(S - (6 if (v0 + k) % 20 else 12), y), (S, y)], fill=(0, 0, 255))
            if (v0 + k) % 20 == 0: d.text((14, y - 6), str(v0 + k), fill=(0, 0, 220))
    if mk:
        x, y = (mk[0] - u0) * z, (mk[1] - v0) * z
        d.line([(x - 6, y), (x + 6, y)], fill=(0, 200, 0), width=2); d.line([(x, y - 6), (x, y + 6)], fill=(0, 200, 0), width=2)
        d.ellipse([x - 12 * z, y - 12 * z, x + 12 * z, y + 12 * z], outline=(0, 200, 0), width=1)
    d.rectangle([0, S - 13, 7 * len(lab) + 6, S], fill=(255, 255, 160)); d.text((3, S - 13), lab, fill=(0, 0, 0))
    tiles.append(t)
n = len(tiles); rows = (n + cols - 1) // cols; S = tiles[0].size[0] + 6
M = Image.new("RGB", (cols * S, rows * S), (90, 90, 90))
for i, t in enumerate(tiles):
    M.paste(t, ((i % cols) * S, (i // cols) * S))
M.save(out); print("wrote", out, M.size)
