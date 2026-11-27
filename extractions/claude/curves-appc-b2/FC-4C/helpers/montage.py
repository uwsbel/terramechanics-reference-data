"""Montage of zoomed windows around marker centers, each with a crosshair at the center, a 5 px
grid (10 px lines darker) and a label, for checking the centers by eye.

    python montage.py <image> <points.csv> <out_prefix> [--half 20] [--zoom 6] [--cols 5] [--rows 4]
                      [--ucol u_ref --vcol v_ref]
"""
import argparse
import csv

from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("image")
ap.add_argument("csv")
ap.add_argument("prefix")
ap.add_argument("--half", type=int, default=20)
ap.add_argument("--zoom", type=int, default=6)
ap.add_argument("--cols", type=int, default=5)
ap.add_argument("--rows", type=int, default=4)
ap.add_argument("--ucol", default="u_ref")
ap.add_argument("--vcol", default="v_ref")
a = ap.parse_args()
img = Image.open(a.image).convert("L")
rows = list(csv.DictReader(open(a.csv, encoding="utf-8-sig", newline="")))
cell = (2 * a.half + 1) * a.zoom
pad = 26
per = a.cols * a.rows
for p in range(0, len(rows), per):
    chunk = rows[p:p + per]
    W, H = a.cols * (cell + pad), a.rows * (cell + pad)
    sheet = Image.new("RGB", (W, H), (255, 255, 255))
    dd = ImageDraw.Draw(sheet)
    for k, r in enumerate(chunk):
        cu, cv = float(r[a.ucol]), float(r[a.vcol])
        u0, v0 = int(round(cu)) - a.half, int(round(cv)) - a.half
        crop = img.crop((u0, v0, u0 + 2 * a.half + 1, v0 + 2 * a.half + 1))
        crop = crop.resize((cell, cell), Image.NEAREST).convert("RGB")
        ox, oy = (k % a.cols) * (cell + pad), (k // a.cols) * (cell + pad) + pad
        sheet.paste(crop, (ox, oy))
        for i in range(2 * a.half + 1):
            if (u0 + i) % 5 == 0:
                x = ox + i * a.zoom
                col = (255, 0, 0) if (u0 + i) % 10 == 0 else (255, 170, 170)
                dd.line([(x, oy), (x, oy + cell)], fill=col, width=1)
            if (v0 + i) % 5 == 0:
                y = oy + i * a.zoom
                col = (0, 0, 255) if (v0 + i) % 10 == 0 else (170, 170, 255)
                dd.line([(ox, y), (ox + cell, y)], fill=col, width=1)
        x = ox + (cu - u0 + 0.5) * a.zoom
        y = oy + (cv - v0 + 0.5) * a.zoom
        dd.line([(x - 14, y), (x + 14, y)], fill=(0, 190, 0), width=2)
        dd.line([(x, y - 14), (x, y + 14)], fill=(0, 190, 0), width=2)
        idx = p + k
        lab = f"#{idx} {r.get('series_id','')} {r.get('symbol','')} ({cu:.1f},{cv:.1f}) u{u0}.. v{v0}.. {r.get('flag','')}"
        dd.text((ox + 2, oy - pad + 3), lab, fill=(0, 0, 0))
    name = f"{a.prefix}-{p // per:02d}.png"
    sheet.save(name)
    print("wrote", name, len(chunk), "cells; red/blue lines every 10 px, pale every 5 px")
