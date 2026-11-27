"""Tiles for the samples flagged by crosscheck.py: binary page (grid-line pixels tinted: vertical runs
light red, horizontal runs light blue), the sampling line (cyan) with ticks every 5 px of u, the tracer2
value (magenta, above the line) and the edge value (green, below). Usage: python cktiles.py out [series]"""
import sys, json
import numpy as np
from PIL import Image, ImageDraw
import fa22lib as L
out = sys.argv[1]; only = sys.argv[2] if len(sys.argv) > 2 else None
d = json.loads((L.OUT / "helpers" / "crosscheck.json").read_text(encoding="utf-8"))
INK = L.page() < 128
VL = np.load(L.OUT / "helpers" / "vline.npy"); HL = np.load(L.OUT / "helpers" / "hline.npy")
rgb = np.full(INK.shape + (3,), 255, np.uint8)
rgb[INK] = (40, 40, 40); rgb[VL] = (230, 140, 140); rgb[HL] = (140, 160, 235)
page = Image.fromarray(rgb)
half, z, cols = 24, 4, 6
tiles = []
for s, lst in d.items():
    if only and s != only: continue
    for m in lst:
        ok = m["u_edge"] is not None and abs(m["diff"]) <= 1.5 and m["kind"].startswith("ok")
        if ok: continue
        u, v = m["u_tr"], m["v"]
        u0, v0 = int(round(u)) - half, int(round(v)) - half
        t = page.crop((u0, v0, u0 + 2 * half, v0 + 2 * half)).resize((2 * half * z, 2 * half * z), Image.NEAREST)
        dr = ImageDraw.Draw(t); S = 2 * half * z
        y = (v - v0) * z
        dr.line([(0, y), (S, y)], fill=(0, 200, 220), width=1)
        for uu in range(u0, u0 + 2 * half + 1):
            if uu % 5 == 0:
                x = (uu - u0) * z
                dr.line([(x, y - 4), (x, y + 4)], fill=(0, 150, 200))
                if uu % 10 == 0: dr.text((x - 8, S - 12), str(uu), fill=(0, 90, 160))
        x = (m["u_tr"] - u0) * z; dr.polygon([(x, y - 2), (x - 5, y - 12), (x + 5, y - 12)], fill=(230, 0, 200))
        if m["u_edge"] is not None:
            x = (m["u_edge"] - u0) * z; dr.polygon([(x, y + 2), (x - 5, y + 12), (x + 5, y + 12)], fill=(0, 190, 0))
        lab = f"{s[:2]} {m['e']:+.2f} v{v:.0f}"
        dr.rectangle([0, 0, 6 * len(lab) + 4, 11], fill=(255, 255, 160)); dr.text((2, 0), lab, fill=(0, 0, 0))
        tiles.append(t)
n = len(tiles); rows = (n + cols - 1) // cols; S = tiles[0].size[0] + 4
M = Image.new("RGB", (cols * S, rows * S), (60, 60, 60))
for i, t in enumerate(tiles):
    M.paste(t, ((i % cols) * S, (i // cols) * S))
M.save(out); print("wrote", out, M.size, n)
