"""Locate the four frame lines of FB-6: at every sample along a line, the ink run nearest a rough
prediction; runs much wider than the line (a tick or a label touching it) are set aside; robust
straight-line fit."""
import sys
import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L"))
dark = g < 128

def runs_of(idx):
    if len(idx) == 0:
        return []
    return np.split(idx, np.where(np.diff(idx) != 1)[0] + 1)

def sample(orient, rough, t_range, half=25, step=5):
    """orient 'v': a near-vertical line u = c + k v, sampled along rows; 'h': v = c + k u along columns."""
    c0, k0 = rough
    pts = []
    for t in range(t_range[0], t_range[1], step):
        p = c0 + k0 * t
        lo = int(round(p - half))
        prof = dark[t, lo:lo + 2 * half + 1] if orient == "v" else dark[lo:lo + 2 * half + 1, t]
        rs = runs_of(np.where(prof)[0])
        if not rs:
            continue
        r = min(rs, key=lambda r: abs(lo + (r[0] + r[-1]) / 2 - p))
        pts.append((t, lo + (r[0] + r[-1]) / 2, len(r)))
    return np.array(pts, dtype=float)

def robust_fit(pts, name, maxw):
    t, p, w = pts.T
    keep = w <= maxw
    for _ in range(5):
        k, c = np.polyfit(t[keep], p[keep], 1)
        res = p - (c + k * t)
        s = 1.4826 * np.median(np.abs(res[keep]))
        keep = (w <= maxw) & (np.abs(res) <= max(1.5, 3 * s))
    res = p[keep] - (c + k * t[keep])
    print(f"{name}: pos = {c:.2f} {k:+.5f} t ; kept {keep.sum()}/{len(t)} rms {res.std():.2f} max {np.abs(res).max():.2f} "
          f"width median {np.median(w[keep]):.0f}; t {t[keep].min():.0f}..{t[keep].max():.0f}")
    return c, k

L = robust_fit(sample("v", (602, 0.032), (860, 4000)), "left   u(v)", 11)
R = robust_fit(sample("v", (2485, 0.030), (800, 3950)), "right  u(v)", 11)
T = robust_fit(sample("h", (852, -0.0257), (650, 2490)), "top    v(u)", 13)
B = robust_fit(sample("h", (4052, -0.0278), (740, 2590)), "bottom v(u)", 14)
import math
for n, (c, k) in [("left", L), ("right", R)]:
    print(f"  {n}: angle from vertical {math.degrees(math.atan(k)):.3f} deg")
for n, (c, k) in [("top", T), ("bottom", B)]:
    print(f"  {n}: angle from horizontal {math.degrees(math.atan(k)):.3f} deg")
def X(vl, hl):
    (cv, kv), (ch, kh) = vl, hl
    u = (cv + kv * ch) / (1 - kv * kh); return u, ch + kh * u
for a, b, n in [(L, T, "TL"), (R, T, "TR"), (L, B, "BL"), (R, B, "BR")]:
    print(n, "corner u,v = %.1f, %.1f" % X(a, b))
