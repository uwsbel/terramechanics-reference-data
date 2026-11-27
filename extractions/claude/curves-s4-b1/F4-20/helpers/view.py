"""Zoomed view of the page with dense trace points and/or samples drawn on it (checking only).

usage: view.py <image> <u0> <v0> <u1> <v1> <zoom> <out.png> [--dense dense.csv] [--points points.csv ...]
Dense points: ok green, wide orange, none red (series: run4 dark, run10 mid, run12 light shade).
Samples: a cross at the pixel and a rectangle of the bounds, blue (trace) or magenta (feature).
"""
import argparse
import csv

from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("image")
ap.add_argument("box", nargs=4, type=int)
ap.add_argument("zoom", type=int)
ap.add_argument("out")
ap.add_argument("--dense")
ap.add_argument("--points", nargs="*", default=[])
ap.add_argument("--step", type=int, default=10)
a = ap.parse_args()
u0, v0, u1, v1 = a.box
z = a.zoom
im = Image.open(a.image).convert("RGB").crop((u0, v0, u1, v1)).resize(((u1 - u0) * z, (v1 - v0) * z), Image.NEAREST)
d = ImageDraw.Draw(im)
for u in range((u0 // a.step + 1) * a.step, u1, a.step):
    d.line([((u - u0) * z, 0), ((u - u0) * z, im.height)], fill=(255, 200, 200) if u % (4 * a.step) else (255, 120, 120))
    if u % (4 * a.step) == 0:
        d.text(((u - u0) * z + 2, 2), str(u), fill=(200, 0, 0))
for v in range((v0 // a.step + 1) * a.step, v1, a.step):
    d.line([(0, (v - v0) * z), (im.width, (v - v0) * z)], fill=(200, 200, 255) if v % (4 * a.step) else (120, 120, 255))
    if v % (4 * a.step) == 0:
        d.text((2, (v - v0) * z + 2), str(v), fill=(0, 0, 200))
col = {"ok": (0, 170, 0), "wide": (255, 140, 0), "none": (230, 0, 0)}


def P(u, v):
    return ((u - u0 + 0.5) * z, (v - v0 + 0.5) * z)


if a.dense:
    for r in csv.DictReader(open(a.dense, encoding="utf-8")):
        u, v = float(r["cu"]), float(r["cv"])
        if not (u0 <= u < u1 and v0 <= v < v1):
            continue
        x, y = P(u, v)
        rr = 1 if r["status"] != "ok" else 1
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col[r["status"]])
for f in a.points:
    for r in csv.DictReader(open(f, encoding="utf-8")):
        u, v = float(r["pixel_u"]), float(r["pixel_v"])
        if not (u0 - 20 <= u < u1 + 20 and v0 - 20 <= v < v1 + 20):
            continue
        bu, bv = float(r["u_bound_px"]), float(r["v_bound_px"])
        c = (0, 0, 255) if r["point_kind"] == "trace" else (220, 0, 220)
        x, y = P(u, v)
        d.rectangle([x - bu * z, y - bv * z, x + bu * z, y + bv * z], outline=c)
        d.line([(x - 4, y), (x + 4, y)], fill=c, width=2)
        d.line([(x, y - 4), (x, y + 4)], fill=c, width=2)
        d.text((x + bu * z + 2, y - 6), f"{r['series_id']}#{r['sequence']}", fill=c)
im.save(a.out)
print("wrote", a.out, im.size)
