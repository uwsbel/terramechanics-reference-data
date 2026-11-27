"""Centre line of each drawn straight segment of FB-4. For a segment given by two rough end points,
the ink is scanned across the segment (rows for a steep segment, columns for a shallow one); at
each scan line the dark run nearest the rough line is taken, runs wider than 1.6x the median width
(where a circle's outline merges with the line) are set aside, and a straight line is fitted
robustly to the run centres. Prints the fit, the perpendicular thickness, the scatter and the ink
extent; writes segments.json for the later steps."""
import json
import sys
import numpy as np
from PIL import Image

D = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
out = sys.argv[2]

# rough end points (u, v) per segment, read on the zoomed crops
SEG = {
    "dr86_s1": ((966, 2520), (1283, 1862)),
    "dr86_s2": ((1283, 1862), (1966, 1347)),
    "dr22_s1": ((777, 3190), (950, 2775)),
    "dr22_s2": ((950, 2775), (1296, 2309)),
    "dr22_s3": ((1296, 2309), (1953, 1945)),
}
CIRCLES = [(770.5, 3210.2), (957.4, 2579.2), (1284.5, 1833.1), (1285.3, 1900.4), (1294.9, 2475.6),
           (1300.0, 2154.8), (1947.1, 1841.6), (1948.4, 2061.9),
           (942.5, 2525), (942.5, 2540), (953.5, 2756), (944, 2777), (944, 2793), (1974, 1330), (1974, 1344)]
R_OUT = 21.5


def runs(mask):
    idx = np.where(mask)[0]
    res = []
    if len(idx) == 0:
        return res
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            res.append((s, p))
            s = i
        p = i
    res.append((s, p))
    return res


def near_circle(u, v, margin=3.0):
    return any(np.hypot(u - cu, v - cv) <= R_OUT + margin for cu, cv in CIRCLES)


res = {}
for name, ((ua, va), (ub, vb)) in SEG.items():
    steep = abs(vb - va) > abs(ub - ua)
    pts, widths = [], []
    if steep:   # u as a function of v
        k = (ub - ua) / (vb - va)
        lo, hi = sorted((va, vb))
        for v in range(int(lo) - 25, int(hi) + 26):
            up = ua + k * (v - va)
            a = int(up) - 25
            rr = runs(D[v, a:a + 51])
            if not rr:
                continue
            s, p = min(rr, key=lambda r: abs(a + (r[0] + r[1]) / 2 - up))
            c = a + (s + p) / 2
            if abs(c - up) > 12:
                continue
            pts.append((c, v)); widths.append(p - s + 1)
    else:       # v as a function of u
        k = (vb - va) / (ub - ua)
        lo, hi = sorted((ua, ub))
        for u in range(int(lo) - 25, int(hi) + 26):
            vp = va + k * (u - ua)
            a = int(vp) - 25
            rr = runs(D[a:a + 51, u])
            if not rr:
                continue
            s, p = min(rr, key=lambda r: abs(a + (r[0] + r[1]) / 2 - vp))
            c = a + (s + p) / 2
            if abs(c - vp) > 12:
                continue
            pts.append((u, c)); widths.append(p - s + 1)
    P = np.array(pts, float)
    W = np.array(widths, float)
    medw = np.median(W)
    clean = (W <= 1.6 * medw) & np.array([not near_circle(u, v) for u, v in P])
    t = P[:, 1] if steep else P[:, 0]
    c = P[:, 0] if steep else P[:, 1]
    keep = clean.copy()
    for _ in range(4):
        kk, c0 = np.polyfit(t[keep], c[keep], 1)
        r = c - (c0 + kk * t)
        mad = np.median(np.abs(r[keep] - np.median(r[keep]))) * 1.4826
        keep = clean & (np.abs(r) <= max(1.0, 3 * mad))
    kk, c0 = np.polyfit(t[keep], c[keep], 1)
    r = c[keep] - (c0 + kk * t[keep])
    thick = np.median(W[keep]) / np.sqrt(1 + kk ** 2)
    # ink extent along the scan coordinate, of points on the fitted line (all points within 2 px)
    on = np.abs(c - (c0 + kk * t)) <= 2.5
    print(f"{name}: {'u(v)' if steep else 'v(u)'} = {c0:.3f} + {kk:+.5f} t; n {keep.sum()}/{len(t)}, rms {np.sqrt(np.mean(r ** 2)):.2f} px, "
          f"run width median {np.median(W[keep]):.1f} -> perpendicular thickness {thick:.2f} px; "
          f"on-line ink t {t[on].min():.0f}..{t[on].max():.0f}")
    res[name] = {"steep": bool(steep), "c0": float(c0), "k": float(kk), "rms": float(np.sqrt(np.mean(r ** 2))),
                 "thickness": float(thick), "n": int(keep.sum()), "t_min_ink": float(t[on].min()), "t_max_ink": float(t[on].max()),
                 "pts": [[float(x), float(y), float(w), bool(kp)] for (x, y), w, kp in zip(P, W, keep)]}
json.dump(res, open(out, "w"), indent=0)
