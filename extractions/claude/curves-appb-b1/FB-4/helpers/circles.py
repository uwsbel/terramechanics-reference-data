"""Find open-circle symbols inside the plot frame of FB-4: ring score = fraction of dark pixels on a
circle of radius r around a candidate centre (72 angles), for r in a range; local maxima above a
threshold are listed with the best radius, the ring score at that radius and the fraction of white
pixels in the inner disc (an open circle's hole). A straight line crossing a candidate covers only
two points of the ring, so it does not make a circle; two overlapping circles give two maxima."""
import sys
import numpy as np
from PIL import Image

D = (np.asarray(Image.open(sys.argv[1]).convert("L")) < 128).astype(np.float32)
u0, v0, u1, v1 = [int(x) for x in sys.argv[2:6]]
thr = float(sys.argv[6]) if len(sys.argv) > 6 else 0.8
pad = 30
S = D[v0 - pad:v1 + pad, u0 - pad:u1 + pad]
H, W = v1 - v0, u1 - u0
ang = np.linspace(0, 2 * np.pi, 72, endpoint=False)
best = np.zeros((H, W), np.float32)
best_r = np.zeros((H, W), np.float32)
for r in np.arange(13.0, 20.01, 0.5):
    acc = np.zeros((H, W), np.float32)
    for a in ang:
        du, dv = int(round(r * np.cos(a))), int(round(r * np.sin(a)))
        acc += S[pad + dv:pad + dv + H, pad + du:pad + du + W]
    acc /= len(ang)
    m = acc > best
    best[m] = acc[m]
    best_r[m] = r
# inner disc whiteness (radius <= 7)
inner = np.zeros((H, W), np.float32)
n = 0
for dv in range(-7, 8):
    for du in range(-7, 8):
        if du * du + dv * dv <= 49:
            inner += 1 - S[pad + dv:pad + dv + H, pad + du:pad + du + W]
            n += 1
inner /= n
# local maxima of the ring score in a 9x9 neighbourhood
from numpy.lib.stride_tricks import sliding_window_view
k = 4
P = np.pad(best, k, constant_values=0)
win = sliding_window_view(P, (2 * k + 1, 2 * k + 1)).max(axis=(2, 3))
peaks = np.argwhere((best >= win) & (best >= thr))
seen = []
for vv, uu in sorted(peaks.tolist(), key=lambda p: -best[p[0], p[1]]):
    if any(abs(vv - a) <= 3 and abs(uu - b) <= 3 for a, b in seen):
        continue
    seen.append((vv, uu))
rows = []
for vv, uu in seen:
    # refine: score-weighted centroid in a 5x5 neighbourhood of the maximum
    sub = best[max(0, vv - 2):vv + 3, max(0, uu - 2):uu + 3]
    ys, xs = np.mgrid[max(0, vv - 2):vv + 3, max(0, uu - 2):uu + 3]
    w = np.clip(sub - (best[vv, uu] - 0.1), 0, None)
    cu = float((xs * w).sum() / w.sum()) + u0
    cv = float((ys * w).sum() / w.sum()) + v0
    rows.append((cu, cv, best[vv, uu], best_r[vv, uu], inner[vv, uu]))
for cu, cv, s, r, inn in sorted(rows, key=lambda x: (x[0], x[1])):
    print(f"u {cu:8.1f}  v {cv:8.1f}  ring {s:.2f}  r {r:4.1f}  inner_white {inn:.2f}")
