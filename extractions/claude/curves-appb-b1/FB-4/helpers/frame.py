"""Locate the four frame lines of FB-4 (p0110.png) by the centre of their dark run, fitted as
straight lines; rows/columns where a tick or a curve merges with the frame are set aside."""
import sys
import numpy as np
from PIL import Image

img = sys.argv[1]
D = np.asarray(Image.open(img).convert("L")) < 128


def runs(mask):
    idx = np.where(mask)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append((s, p))
            s = i
        p = i
    out.append((s, p))
    return out


def fit(ts, cs, label):
    ts, cs = np.array(ts, float), np.array(cs, float)
    k, c0 = np.polyfit(ts, cs, 1)
    for _ in range(3):
        r = cs - (c0 + k * ts)
        mad = np.median(np.abs(r - np.median(r))) * 1.4826
        keep = np.abs(r) <= max(1.0, 3 * mad)
        k, c0 = np.polyfit(ts[keep], cs[keep], 1)
    r = cs[keep] - (c0 + k * ts[keep])
    print(f"{label}: pos = {c0:.2f} + {k:+.6f} t   n={keep.sum()}/{len(ts)}  rms={np.sqrt(np.mean(r**2)):.2f}")
    return c0, k


def horiz(vlo, vhi, ulo, uhi, label, maxw=14):
    ts, cs, ws = [], [], []
    for u in range(ulo, uhi, 3):
        col = D[vlo:vhi, u]
        rr = runs(col)
        if not rr:
            continue
        s, p = max(rr, key=lambda x: x[1] - x[0])
        w = p - s + 1
        if w > maxw or w < 3:
            continue
        ts.append(u); cs.append(vlo + (s + p) / 2); ws.append(w)
    print(f"  {label} thickness median {np.median(ws):.1f}")
    return fit(ts, cs, label)


def vert(ulo, uhi, vlo, vhi, label, maxw=14):
    ts, cs, ws = [], [], []
    for v in range(vlo, vhi, 3):
        row = D[v, ulo:uhi]
        rr = runs(row)
        if not rr:
            continue
        s, p = max(rr, key=lambda x: x[1] - x[0])
        w = p - s + 1
        if w > maxw or w < 3:
            continue
        ts.append(v); cs.append(ulo + (s + p) / 2); ws.append(w)
    print(f"  {label} thickness median {np.median(ws):.1f}")
    return fit(ts, cs, label)


bot = horiz(3880, 3935, 640, 2520, "bottom frame (y=0) v(u)")
top = horiz(1085, 1140, 640, 2520, "top frame (y=10) v(u)")
lef = vert(570, 630, 1150, 3870, "left frame (x=0) u(v)")
rig = vert(2530, 2590, 1150, 3870, "right frame (x=14) u(v)")
