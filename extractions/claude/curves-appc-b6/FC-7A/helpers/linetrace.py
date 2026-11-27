"""Measure a drawn straight line column by column and place trace samples on its ink.

For every column u in [u_from, u_to] the dark run nearest the seed line v = v0 + s (u - u0) is
taken; its midpoint is the line center at that column (for a sloped line the vertical run's
midpoint lies on the centerline). Columns whose run is longer than `maxlen` (a symbol, a grid line
or a label merged with the line) or that have no ink (a dash gap) are flagged and not used.
A robust straight fit over the clean columns is printed with its residuals, then for each target
x value the sample is put at the clean column whose center maps closest to that x, using a local
straight fit over clean columns within +-12 px, and the ink there is reported.
Usage: linetrace.py image calibration.json u0 v0 slope u_from u_to x_targets(comma) [maxlen]"""
import sys, json
import numpy as np
from PIL import Image

img, calp = sys.argv[1], sys.argv[2]
u0, v0, s, ua, ub = map(float, sys.argv[3:8])
targets = [float(t) for t in sys.argv[8].split(",")] if len(sys.argv) > 8 and sys.argv[8] else []
maxlen = int(sys.argv[9]) if len(sys.argv) > 9 else 14
cal = json.load(open(calp))
ax, ay = cal["ax"], cal["ay"]
X = lambda u, v: ax[0] * u + ax[1] * v + ax[2]
Y = lambda u, v: ay[0] * u + ay[1] * v + ay[2]
g = np.asarray(Image.open(img).convert("L")) < 160
rows = []
for u in range(int(ua), int(ub) + 1):
    vp = v0 + s * (u - u0)
    a, b = int(vp - 25), int(vp + 25)
    col = g[a:b, u]
    runs, i = [], 0
    while i < len(col):
        if col[i]:
            j = i
            while j + 1 < len(col) and col[j + 1]:
                j += 1
            runs.append((a + i, a + j)); i = j + 1
        else:
            i += 1
    near = [r for r in runs if abs((r[0] + r[1]) / 2 - vp) < 14]
    if not near:
        rows.append((u, None, 0, "gap")); continue
    r = min(near, key=lambda r: abs((r[0] + r[1]) / 2 - vp))
    L = r[1] - r[0] + 1
    rows.append((u, (r[0] + r[1] + 1) / 2, L, "ok" if L <= maxlen else "long"))
clean = [(u, c) for u, c, L, f in rows if f == "ok"]
U = np.array([c[0] for c in clean], float); V = np.array([c[1] for c in clean], float)
p = np.polyfit(U, V, 1)
for _ in range(3):
    res = V - np.polyval(p, U); k = np.abs(res) < 2.5 * max(res.std(), 0.5)
    p = np.polyfit(U[k], V[k], 1)
res = V - np.polyval(p, U)
print(f"clean columns {len(U)}, fit v = {p[1]:.2f} + {p[0]:.5f} u, rms {res.std():.2f}, max |res| {np.abs(res).max():.2f}")
Ls = [L for u, c, L, f in rows if f == "ok"]
print(f"median vertical run {np.median(Ls):.1f} px")
# runs of flags
prev, start = None, None
segs = []
for u, c, L, f in rows:
    if f != prev:
        if prev is not None: segs.append((prev, start, u - 1))
        prev, start = f, u
segs.append((prev, start, rows[-1][0]))
print("segments:", " ".join(f"{f}[{a}-{b}]" for f, a, b in segs))
# residuals by 50-px block
for a in range(int(ua), int(ub) + 1, 100):
    k = (U >= a) & (U < a + 100)
    if k.sum(): print(f"  u {a}-{a+99}: n {k.sum():3d} mean res {res[k].mean():+.2f}")
cd = dict(clean)
for t in targets:
    best = None
    for u in cd:
        loc = [(uu, cd[uu]) for uu in range(u - 12, u + 13) if uu in cd]
        if len(loc) < 8: continue
        q = np.polyfit([l[0] for l in loc], [l[1] for l in loc], 1)
        vv = np.polyval(q, u)
        e = abs(X(u, vv) - t)
        if best is None or e < best[0]: best = (e, u, vv, len(loc))
    if best is None:
        print(f"x={t}: no clean ink"); continue
    e, u, vv, n = best
    print(f"x={t}: u {u} v {vv:.1f}  (x {X(u,vv):.3f}, y {Y(u,vv):.3f})  local n {n}  fitline v {np.polyval(p,u):.1f}")
