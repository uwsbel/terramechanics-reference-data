"""Helpers for reading a plotted curve from a scanned page image, by pixel.

Two sub-commands. Both work on the unrotated page image as rendered by tools/render_pages.py; all
pixel coordinates are (u, v) with u to the right and v downward, origin at the top-left corner of
that image, so a reading can be checked by anyone who renders the same page at the same dpi.

    python tools/plot_grid.py lines <image> --box u0 v0 u1 v1 [--min-frac 0.6] [--dark 128]
        Lists candidate axis and grid lines inside the box: rows (v) and columns (u) where at least
        `min-frac` of the pixels across the box are dark. Runs of adjacent rows or columns are
        merged and reported by their center and width. These are the pixel positions that go into
        anchors.csv together with the printed value of the gridline.

    python tools/plot_grid.py crop <image> --box u0 v0 u1 v1 --out crop.png [--zoom 3] [--step 25]
        Writes an enlarged crop with a labeled pixel grid drawn over it (lines every `step` pixels
        of the original image, labels in original-image pixels), so marker centers can be read to
        a few pixels and recorded as pixel coordinates.

Needs Pillow and NumPy (an existing conda env; nothing is installed by this tool).
"""
import argparse
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def load_gray(path):
    return np.asarray(Image.open(path).convert("L"))


def runs(indices):
    """Merge consecutive indices into (center, width) runs."""
    out = []
    if len(indices) == 0:
        return out
    start = prev = int(indices[0])
    for i in indices[1:]:
        i = int(i)
        if i != prev + 1:
            out.append(((start + prev) / 2, prev - start + 1))
            start = i
        prev = i
    out.append(((start + prev) / 2, prev - start + 1))
    return out


def cmd_lines(a):
    g = load_gray(a.image)
    u0, v0, u1, v1 = a.box
    sub = g[v0:v1, u0:u1] < a.dark
    row_frac = sub.mean(axis=1)
    col_frac = sub.mean(axis=0)
    print(f"box u {u0}..{u1}, v {v0}..{v1}; dark threshold {a.dark}; min fraction {a.min_frac}"
          + (f"; strongest {a.top} runs per direction" if a.top else ""))

    def report(frac, offset, label):
        cands = runs(np.where(frac >= a.min_frac)[0])
        scored = []
        for c, w in cands:
            lo, hi = int(c - w / 2 + 0.5), int(c + w / 2 + 0.5) + 1
            scored.append((frac[lo:hi].max(), c + offset, w))
        if a.top:
            scored = sorted(scored, reverse=True)[:a.top]
            scored.sort(key=lambda t: t[1])
        for f, c, w in scored:
            print(f"  {label} = {c:8.1f}   {w:3d}   {f:.2f}")

    print("horizontal lines (v center, thickness px, dark fraction):")
    report(row_frac, v0, "v")
    print("vertical lines (u center, thickness px, dark fraction):")
    report(col_frac, u0, "u")


def cmd_scan(a):
    """For each column u, list the dark runs (center v, thickness) between v0 and v1: the places
    where a drawn curve, a marker or a horizontal grid line crosses that column. The reader
    assigns runs to series (curves keep a known vertical order away from crossings) and the
    run center is the trace position with a bound of half its thickness."""
    g = load_gray(a.image)
    us = [int(x) for x in a.us.split(",")] if a.us else list(range(a.u_range[0], a.u_range[1] + 1, a.u_range[2]))
    print("u,v_center,thickness")
    for u in us:
        col = g[a.v0:a.v1, u - a.halfwidth:u + a.halfwidth + 1].min(axis=1) < a.dark
        for c, w in runs(np.where(col)[0]):
            print(f"{u},{c + a.v0:.1f},{w}")


COLORS = [(220, 0, 0), (0, 140, 0), (0, 0, 220), (200, 120, 0), (150, 0, 150), (0, 150, 150), (120, 60, 0),
          (255, 0, 120), (90, 90, 90)]


def cmd_overlay(a):
    """Draw the points of one or two readings over the page image (cropped to --box when given):
    a filled circle per point, colored by series, with a bar for the pixel bounds; the second
    reading, if any, is drawn as hollow squares so the two can be compared on the page."""
    im = Image.open(a.image).convert("RGB")
    d = ImageDraw.Draw(im)
    import csv
    series = {}
    for k, path in enumerate(a.points):
        with open(path, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                sid = r["series_id"]
                col = COLORS[series.setdefault(sid, len(series)) % len(COLORS)]
                u, v = float(r["pixel_u"]), float(r["pixel_v"])
                bu, bv = float(r.get("u_bound_px") or 0), float(r.get("v_bound_px") or 0)
                d.line([(u, v - bv), (u, v + bv)], fill=col, width=2)
                d.line([(u - bu, v), (u + bu, v)], fill=col, width=2)
                if k == 0:
                    d.ellipse([u - 5, v - 5, u + 5, v + 5], fill=col)
                else:
                    d.rectangle([u - 6, v - 6, u + 6, v + 6], outline=col, width=2)
    if a.box:
        u0, v0, u1, v1 = a.box
        im = im.crop((u0, v0, u1, v1))
    im.save(a.out)
    print(f"wrote {a.out}; series colors: " + ", ".join(f"{s}={COLORS[i % len(COLORS)]}" for s, i in series.items()))


def cmd_crop(a):
    im = Image.open(a.image).convert("RGB")
    u0, v0, u1, v1 = a.box
    crop = im.crop((u0, v0, u1, v1)).resize(((u1 - u0) * a.zoom, (v1 - v0) * a.zoom), Image.NEAREST)
    d = ImageDraw.Draw(crop)
    try:
        font = ImageFont.truetype("arial.ttf", 11 * max(1, a.zoom // 2))
    except OSError:
        font = ImageFont.load_default()
    first_u = (u0 // a.step + 1) * a.step
    first_v = (v0 // a.step + 1) * a.step
    for u in range(first_u, u1, a.step):
        x = (u - u0) * a.zoom
        major = (u % (a.step * 4) == 0)
        d.line([(x, 0), (x, crop.height)], fill=(255, 0, 0) if major else (255, 160, 160), width=1)
        if major:
            d.text((x + 2, 2), str(u), fill=(200, 0, 0), font=font)
    for v in range(first_v, v1, a.step):
        y = (v - v0) * a.zoom
        major = (v % (a.step * 4) == 0)
        d.line([(0, y), (crop.width, y)], fill=(0, 0, 255) if major else (160, 160, 255), width=1)
        if major:
            d.text((2, y + 2), str(v), fill=(0, 0, 200), font=font)
    crop.save(a.out)
    print(f"wrote {a.out}: {crop.width}x{crop.height}, grid every {a.step} px (labels every {a.step * 4} px), zoom {a.zoom}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("lines")
    l.add_argument("image")
    l.add_argument("--box", nargs=4, type=int, required=True)
    l.add_argument("--min-frac", type=float, default=0.6)
    l.add_argument("--dark", type=int, default=128)
    l.add_argument("--top", type=int, default=0, help="report only the N strongest runs per direction (faint grids)")
    s = sub.add_parser("scan")
    s.add_argument("image")
    s.add_argument("--us", help="comma-separated column positions u")
    s.add_argument("--u-range", nargs=3, type=int, metavar=("U0", "U1", "STEP"))
    s.add_argument("--v0", type=int, required=True)
    s.add_argument("--v1", type=int, required=True)
    s.add_argument("--dark", type=int, default=200)
    s.add_argument("--halfwidth", type=int, default=1, help="columns u-h..u+h are combined (min), so a 1 px gap in a line does not split a run")
    o = sub.add_parser("overlay")
    o.add_argument("image")
    o.add_argument("--points", nargs="+", required=True, help="one or two points CSV files (pixel_u, pixel_v, series_id, bounds)")
    o.add_argument("--box", nargs=4, type=int)
    o.add_argument("--out", required=True)
    c = sub.add_parser("crop")
    c.add_argument("image")
    c.add_argument("--box", nargs=4, type=int, required=True)
    c.add_argument("--out", required=True)
    c.add_argument("--zoom", type=int, default=3)
    c.add_argument("--step", type=int, default=25)
    a = ap.parse_args()
    {"lines": cmd_lines, "crop": cmd_crop, "scan": cmd_scan, "overlay": cmd_overlay}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
