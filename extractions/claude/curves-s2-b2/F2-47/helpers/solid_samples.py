"""Solid-trace samples every 0.25 in from the column tracks (F2-47 helper).

Reads helpers/solid-track.csv (u 620..900), solid-track2.csv (u 926..2354) and solid-track3.csv
(u 2357..2639), all made with helpers/track.py on the page, and for each target penetration finds
the column whose run center maps to that penetration, then reports the run, its length, the local
slope dv/du (fit over +-8 columns) and the line thickness across the line (run length times
cos(atan(slope))). Flagged columns (run touching a grid line or another line) are reported so they
can be checked by eye. Values here use the affine-free piecewise interpolation of helpers/probe.py.
"""
import csv, json, sys
import numpy as np
sys.argv = [sys.argv[0], 'out/F2-47/cal-p1/calibration.json', 'packet/p0108.png', '0', '0']
exec(open('out/F2-47/helpers/probe.py').read().split("u = u_of(x, vg)")[0])
tr = {}
for fn, lo, hi in [('solid-track.csv', 620, 900), ('solid-track2.csv', 926, 2354), ('solid-track3.csv', 2357, 2639)]:
    for r in csv.DictReader(open('out/F2-47/helpers/' + fn)):
        u = int(r['u'])
        if lo <= u <= hi:
            tr[u] = (int(r['top']), int(r['bot']), float(r['center']), int(r['length']), r['flag'])
us = sorted(tr)
for k in range(2, 28):
    x = k * 0.25
    best = None
    for u in us:
        xx = x_of(u, tr[u][2])
        if best is None or abs(xx - x) < abs(best[1] - x): best = (u, xx)
    u = best[0]
    nb = [w for w in range(u - 8, u + 9) if w in tr and not tr[w][4]]
    p = np.polyfit(nb, [tr[w][2] for w in nb], 1) if len(nb) > 3 else [0, 0]
    s = p[0]
    t, b, c, L, f = tr[u]
    thick = L / np.sqrt(1 + s * s)
    print(f"x={x:5.2f} u={u} v={c:7.1f} run {t}-{b} L={L} slope={s:+.2f} thick={thick:4.1f}  x={best[1]:.4f} load={y_of(u, c):7.1f} {f}")
