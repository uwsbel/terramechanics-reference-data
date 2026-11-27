"""Contact sheet to check marker centers by eye: each cell is a zoomed crop around a proposed
center, the page ink in gray, the proposed center as a red cross and the template outline (ink
cells of the matched template) as a thin green overlay. A fine pixel grid (every 5 px, darker
every 10 px) with labels lets the reader correct a center.

python check.py <image> <points.csv> <out.png> [--keys k1,k2,...] [--ucol u_fit --vcol v_fit]
"""
import argparse
import csv

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from match import template


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("points")
    ap.add_argument("out")
    ap.add_argument("--keys", default="")
    ap.add_argument("--prefix", default="")
    ap.add_argument("--ucol", default="u_fit")
    ap.add_argument("--vcol", default="v_fit")
    ap.add_argument("--half", type=int, default=24)
    ap.add_argument("--zoom", type=int, default=6)
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--no-template", action="store_true")
    a = ap.parse_args()
    g = np.asarray(Image.open(a.image).convert("L"))
    rows = list(csv.DictReader(open(a.points, encoding="utf-8")))
    keys = [k for k in a.keys.split(",") if k]
    if keys:
        rows = [r for r in rows if r["key"] in keys]
    if a.prefix:
        rows = [r for r in rows if r["key"].startswith(a.prefix)]
    try:
        font = ImageFont.truetype("arial.ttf", 13)
    except OSError:
        font = ImageFont.load_default()
    h, z = a.half, a.zoom
    cell = 2 * h * z
    pl, pt = 44, 34
    W = a.cols * (cell + pl + 6)
    nrow = (len(rows) + a.cols - 1) // a.cols
    sheet = Image.new("RGB", (W, nrow * (cell + pt + 6)), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    for k, r in enumerate(rows):
        uf, vf = float(r[a.ucol]), float(r[a.vcol])
        uc, vc = int(round(uf)), int(round(vf))
        u0, v0 = uc - h, vc - h
        patch = g[v0:v0 + 2 * h, u0:u0 + 2 * h]
        rgb = np.stack([patch] * 3, -1).astype(np.uint8)
        rgb = np.where(rgb < 128, 90, 255).astype(np.uint8)
        if not a.no_template and r.get("symbol"):
            w, _ = template(r["symbol"], h)
            ink = (w == 1.0)[:2 * h, :2 * h]
            # outline of ink region only
            edge = ink & ~(np.roll(ink, 1, 0) & np.roll(ink, -1, 0) & np.roll(ink, 1, 1) & np.roll(ink, -1, 1))
            sh_u, sh_v = uc - uf, vc - vf  # template drawn at integer center (sub-px ignored)
            rgb[edge] = (0, 170, 0)
        im = Image.fromarray(rgb).resize((cell, cell), Image.NEAREST)
        cd = ImageDraw.Draw(im)
        for t in range(0, 2 * h + 1):
            if (u0 + t) % 5 == 0:
                cd.line([(t * z, 0), (t * z, cell)], fill=(255, 0, 0) if (u0 + t) % 10 == 0 else (255, 180, 180))
            if (v0 + t) % 5 == 0:
                cd.line([(0, t * z), (cell, t * z)], fill=(0, 0, 255) if (v0 + t) % 10 == 0 else (180, 180, 255))
        # proposed center (sub-pixel), pixel centers at (i+0.5)*z
        x, y = (uf - u0 + 0.5) * z, (vf - v0 + 0.5) * z
        cd.line([(x - 18, y), (x + 18, y)], fill=(230, 0, 0), width=3)
        cd.line([(x, y - 18), (x, y + 18)], fill=(230, 0, 0), width=3)
        rr, qq = divmod(k, a.cols)
        ox, oy = qq * (cell + pl + 6) + pl, rr * (cell + pt + 6) + pt
        sheet.paste(im, (ox, oy))
        d.text((ox, oy - 32), f"{r['key']} ({uf:.1f},{vf:.1f})", fill=(0, 0, 0), font=font)
        for t in range(0, 2 * h + 1):
            if (u0 + t) % 20 == 0:
                d.text((ox + t * z - 12, oy - 16), str(u0 + t), fill=(200, 0, 0), font=font)
            if (v0 + t) % 20 == 0:
                d.text((ox - 42, oy + t * z - 7), str(v0 + t), fill=(0, 0, 200), font=font)
    sheet.save(a.out)
    print(f"wrote {a.out} {sheet.size} ({len(rows)} cells)")


if __name__ == "__main__":
    main()
