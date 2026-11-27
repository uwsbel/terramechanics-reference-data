"""Dense centre line of each drawn trace, re-centred on the ink across a guide polyline.

The guide (helpers/guides.json) is resampled every 1 px of arc length. At each guide point the ink
profile across the guide (its normal, +-R px, averaged over 3 px along it) is read on the de-gridded
page (grid ink removed only where it was not touching a curve; curve ink is unchanged), the dark run
nearest the guide is taken, and the point is moved to the run's centre. Status:
  ok     one clean run, width <= WMAX, not touching the window edge
  wide   the run is wider than WMAX or touches the window edge (another trace, a grid line or the
         frame runs into it): centre not trusted
  none   no ink (a gap between dashes or dots, or a dropout of the scan)
Output: dense.csv (series, segment, i, arc, guide u v, centre u v, width, status) and, for checking,
x and y values from the affine map (targeting only; reported values come from the piecewise map).

usage: trace.py <guides.json> <degrid.png> <calibration.json> <dense.csv>
"""
import csv
import json
import sys

import numpy as np
from PIL import Image

R = 9.0
WMAX = 14.0


def resample(pts, step=1.0):
    P = np.array(pts, dtype=float)
    d = np.hypot(*np.diff(P, axis=0).T)
    s = np.concatenate([[0], np.cumsum(d)])
    n = int(s[-1] // step) + 1
    ss = np.linspace(0, s[-1], n)
    u = np.interp(ss, s, P[:, 0])
    v = np.interp(ss, s, P[:, 1])
    return ss, np.vstack([u, v]).T


def tangents(Q, k=3):
    T = np.zeros_like(Q)
    for i in range(len(Q)):
        a, b = max(0, i - k), min(len(Q) - 1, i + k)
        t = Q[b] - Q[a]
        T[i] = t / (np.hypot(*t) + 1e-12)
    return T


def profile_run(ink, p, t, n):
    offs = np.arange(-R, R + 0.01, 0.5)
    h, w = ink.shape
    acc = np.zeros(len(offs))
    for dt in (-1.0, 0.0, 1.0):
        U = np.round(p[0] + offs * n[0] + dt * t[0]).astype(int)
        V = np.round(p[1] + offs * n[1] + dt * t[1]).astype(int)
        U = np.clip(U, 0, w - 1)
        V = np.clip(V, 0, h - 1)
        acc += ink[V, U]
    dark = acc / 3.0 >= 0.5
    runs, i = [], 0
    while i < len(dark):
        if dark[i]:
            j = i
            while j + 1 < len(dark) and dark[j + 1]:
                j += 1
            runs.append((offs[i], offs[j], i == 0 or j == len(dark) - 1))
            i = j + 1
        else:
            i += 1
    if not runs:
        return None, None, "none", 0
    a, b, edge = min(runs, key=lambda r: 0 if r[0] <= 0 <= r[1] else min(abs(r[0]), abs(r[1])))
    width = b - a + 0.5
    status = "ok" if (width <= WMAX and not edge) else "wide"
    return (a + b) / 2, width, status, len(runs)


def main():
    guides = json.load(open(sys.argv[1], encoding="utf-8"))
    ink = (np.asarray(Image.open(sys.argv[2]).convert("L")) < 128).astype(float)
    cal = json.load(open(sys.argv[3], encoding="utf-8"))
    ax, ay = cal["ax"], cal["ay"]
    rows = []
    for sid, spec in guides.items():
        if sid.startswith("_"):
            continue
        arc0 = 0.0
        for k, seg in enumerate(spec["segments"]):
            ss, Q = resample(seg["points"])
            T = tangents(Q)
            for i, (s, q, t) in enumerate(zip(ss, Q, T)):
                n = np.array([-t[1], t[0]])
                c, wdt, st, nr = profile_run(ink, q, t, n)
                cu, cv = (q + c * n) if c is not None else q
                x = ax[0] * cu + ax[1] * cv + ax[2]
                y = ay[0] * cu + ay[1] * cv + ay[2]
                rows.append({"series_id": sid, "segment": k + 1, "i": i, "arc": round(arc0 + s, 1),
                             "gu": round(q[0], 2), "gv": round(q[1], 2), "cu": round(float(cu), 2), "cv": round(float(cv), 2),
                             "tu": round(t[0], 4), "tv": round(t[1], 4),
                             "width": "" if wdt is None else wdt, "status": st, "nruns": nr,
                             "x_aff": round(x, 4), "y_aff": round(y, 2)})
            arc0 += ss[-1] + 1000.0   # segments are separated in arc length so nothing bridges them
    with open(sys.argv[4], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    for sid in guides:
        if sid.startswith("_"):
            continue
        c = Counter(r["status"] for r in rows if r["series_id"] == sid)
        print(sid, dict(c))


if __name__ == "__main__":
    main()
