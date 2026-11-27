"""Reading aids for FA-2 (page p0007), built on the reader's own calibration out/FA-2/cal-p1.

    python fa2_tools.py crop u0 v0 u1 v1 out.png [zoom]
        a zoomed crop with a 25 px pixel grid (as tools/plot_grid.py crop) plus the sampling lines
        of constant grain size 10^(0.05 k) in green (labelled) and lines of constant percent finer
        every 5 percent in orange, both from the piecewise map of cal-p1.
    python fa2_tools.py profile g u0 u1 [halfwidth]
        darkness along the sampling line of grain size g (mm) between u0 and u1, as dark runs
        (u centre, width) with the percent finer at each run centre.
    python fa2_tools.py column p v0 v1 [halfwidth]
        the same along the line of constant percent p between v0 and v1, runs as (v centre, width)
        with the grain size at each centre.
    python fa2_tools.py where u v
        the grain size and percent finer at a pixel.

Nothing here decides a value: the reader reads every point by eye on these crops.
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import calibrate_axes as ca  # noqa: E402

IMG = ROOT / "packet" / "p0007.png"
CAL, X, Y = ca.piecewise_maps(HERE / "cal-p1")
GRAY = np.asarray(Image.open(IMG).convert("L"), dtype=float)


def where(u, v):
    return X.value(u, v)[0], Y.value(u, v)[0]


def v_of_grain(g, u, lo=1000.0, hi=3800.0):
    """v at column u where the grain size is g (grain size decreases downward on the page)."""
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if X.value(u, m)[0] > g:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


def u_of_pct(p, v, lo=600.0, hi=2250.0):
    """u at row v where percent finer is p (percent decreases to the right)."""
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if Y.value(m, v)[0] > p:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)


def sample_grains(gmin=0.015, gmax=12.0):
    out = []
    k = math.ceil(math.log10(gmin) / 0.05)
    while 10 ** (0.05 * k) <= gmax:
        out.append((k, 10 ** (0.05 * k)))
        k += 1
    return out


def crop(u0, v0, u1, v1, out, zoom=4):
    im = Image.open(IMG).convert("RGB").crop((u0, v0, u1, v1)).resize(((u1 - u0) * zoom, (v1 - v0) * zoom), Image.NEAREST)
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    for u in range((u0 // 25 + 1) * 25, u1, 25):
        x = (u - u0) * zoom
        d.line([(x, 0), (x, im.height)], fill=(255, 0, 0) if u % 100 == 0 else (255, 170, 170), width=1)
        if u % 100 == 0:
            d.text((x + 2, 2), str(u), fill=(200, 0, 0), font=font)
    for v in range((v0 // 25 + 1) * 25, v1, 25):
        y = (v - v0) * zoom
        d.line([(0, y), (im.width, y)], fill=(0, 0, 255) if v % 100 == 0 else (170, 170, 255), width=1)
        if v % 100 == 0:
            d.text((2, y + 2), str(v), fill=(0, 0, 200), font=font)
    for k, g in sample_grains():
        pts = [((u - u0) * zoom, (v_of_grain(g, u) - v0) * zoom) for u in np.linspace(u0, u1, 9)]
        if all(p[1] < 0 for p in pts) or all(p[1] > im.height for p in pts):
            continue
        d.line(pts, fill=(0, 170, 0), width=1)
        d.text((im.width - 120, pts[-1][1] - 16), f"k={k} {g:.4g}", fill=(0, 130, 0), font=font)
    for p in range(0, 101, 5):
        pts = [((u_of_pct(p, v) - u0) * zoom, (v - v0) * zoom) for v in np.linspace(v0, v1, 9)]
        if all(q[0] < 0 for q in pts) or all(q[0] > im.width for q in pts):
            continue
        d.line(pts, fill=(255, 140, 0), width=1)
        d.text((pts[0][0] + 2, 20), f"{p}%", fill=(220, 110, 0), font=font)
    im.save(out)
    print(f"wrote {out} ({im.width}x{im.height}, zoom {zoom})")


def runs(vals, pos, thr=128):
    dark = vals < thr
    out, s = [], None
    for i, dk in enumerate(dark):
        if dk and s is None:
            s = i
        if (not dk or i == len(dark) - 1) and s is not None:
            e = i if dk else i - 1
            out.append((0.5 * (pos[s] + pos[e]), pos[e] - pos[s] + (pos[1] - pos[0])))
            s = None
    return out


def sample(u, v, hw):
    """minimum (darkest) gray value within +-hw px across, at (u, v)."""
    vi, ui = int(round(v)), int(round(u))
    return GRAY[vi - hw:vi + hw + 1, ui].min() if hw else GRAY[vi, ui]


def profile(g, u0, u1, hw=0):
    us = np.arange(u0, u1 + 0.01, 1.0)
    vs = [v_of_grain(g, u) for u in us]
    vals = np.array([sample(u, v, hw) for u, v in zip(us, vs)])
    for c, w in runs(vals, us):
        vv = v_of_grain(g, c)
        print(f"  u {c:7.1f}  v {vv:7.1f}  width {w:4.0f}  percent {Y.value(c, vv)[0]:6.2f}")


def column(p, v0, v1, hw=0):
    vs = np.arange(v0, v1 + 0.01, 1.0)
    us = [u_of_pct(p, v) for v in vs]
    vals = np.array([GRAY[int(round(v)), int(round(u)) - hw:int(round(u)) + hw + 1].min() for u, v in zip(us, vs)])
    for c, w in runs(vals, vs):
        uu = u_of_pct(p, c)
        print(f"  v {c:7.1f}  u {uu:7.1f}  width {w:4.0f}  grain {X.value(uu, c)[0]:.4f}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "crop":
        u0, v0, u1, v1 = (int(x) for x in sys.argv[2:6])
        crop(u0, v0, u1, v1, sys.argv[6], int(sys.argv[7]) if len(sys.argv) > 7 else 4)
    elif cmd == "profile":
        profile(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]) if len(sys.argv) > 5 else 0)
    elif cmd == "column":
        column(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]) if len(sys.argv) > 5 else 0)
    elif cmd == "where":
        print("grain %.5f mm, percent %.3f" % where(float(sys.argv[2]), float(sys.argv[3])))


def long_run_mask(dark, min_len, axis):
    """True where a pixel belongs to a dark run of at least min_len pixels along `axis` (1: rows, 0: columns)."""
    a = dark if axis == 1 else dark.T
    out = np.zeros_like(a)
    for i in range(a.shape[0]):
        row = a[i].astype(np.int8)
        d = np.diff(np.concatenate(([0], row, [0])))
        starts, ends = np.where(d == 1)[0], np.where(d == -1)[0]
        for s, e in zip(starts, ends):
            if e - s >= min_len:
                out[i, s:e] = True
    return out if axis == 1 else out.T


def crop_nogrid(u0, v0, u1, v1, out, zoom=4, hmin=100, vmin=60):
    """As crop, with ink in long horizontal runs (grid lines) drawn light blue and ink in long vertical
    runs drawn light red, so that the curves stand out in black. A display aid only."""
    pad = 200
    U0, V0, U1, V1 = max(0, u0 - pad), max(0, v0 - pad), u1 + pad, v1 + pad
    dark = GRAY[V0:V1, U0:U1] < 128
    h = long_run_mask(dark, hmin, 1)
    v = long_run_mask(dark, vmin, 0)
    rgb = np.full(dark.shape + (3,), 255, np.uint8)
    rgb[dark] = (0, 0, 0)
    rgb[dark & v] = (255, 170, 170)
    rgb[dark & h] = (160, 200, 255)
    sub = rgb[v0 - V0:v1 - V0, u0 - U0:u1 - U0]
    im = Image.fromarray(sub).resize(((u1 - u0) * zoom, (v1 - v0) * zoom), Image.NEAREST)
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    for uu in range((u0 // 25 + 1) * 25, u1, 25):
        x = (uu - u0) * zoom
        d.line([(x, 0), (x, im.height)], fill=(255, 0, 0) if uu % 100 == 0 else (255, 210, 210), width=1)
        if uu % 100 == 0:
            d.text((x + 2, 2), str(uu), fill=(200, 0, 0), font=font)
    for vv in range((v0 // 25 + 1) * 25, v1, 25):
        y = (vv - v0) * zoom
        d.line([(0, y), (im.width, y)], fill=(0, 0, 255) if vv % 100 == 0 else (210, 210, 255), width=1)
        if vv % 100 == 0:
            d.text((2, y + 2), str(vv), fill=(0, 0, 200), font=font)
    im.save(out)
    print(f"wrote {out} ({im.width}x{im.height}, zoom {zoom})")


if __name__ == "__main__" and sys.argv[1] == "nogrid":
    u0, v0, u1, v1 = (int(x) for x in sys.argv[2:6])
    crop_nogrid(u0, v0, u1, v1, sys.argv[6], int(sys.argv[7]) if len(sys.argv) > 7 else 4)


def colruns(u0, u1, step, v0, v1):
    """per column u: the dark runs between v0 and v1 as start-end (inclusive)."""
    for u in range(u0, u1 + 1, step):
        col = GRAY[v0:v1 + 1, u] < 128
        d = np.diff(np.concatenate(([0], col.astype(np.int8), [0])))
        s, e = np.where(d == 1)[0], np.where(d == -1)[0]
        print(f"u {u}: " + "  ".join(f"{v0 + a}-{v0 + b - 1}" for a, b in zip(s, e)))


def rowruns(v0, v1, step, u0, u1):
    for v in range(v0, v1 + 1, step):
        row = GRAY[v, u0:u1 + 1] < 128
        d = np.diff(np.concatenate(([0], row.astype(np.int8), [0])))
        s, e = np.where(d == 1)[0], np.where(d == -1)[0]
        print(f"v {v}: " + "  ".join(f"{u0 + a}-{u0 + b - 1}" for a, b in zip(s, e)))


if __name__ == "__main__" and sys.argv[1] in ("colruns", "rowruns"):
    f = colruns if sys.argv[1] == "colruns" else rowruns
    f(*(int(x) for x in sys.argv[2:7]))
