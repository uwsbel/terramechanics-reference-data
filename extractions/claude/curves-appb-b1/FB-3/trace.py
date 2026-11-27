"""Trace the drawn straight segments of FB-3 on the ink: at every 2 px along a segment's approximate
direction, the profile across it (bilinear, 0.25 px steps, averaged over +-2 px along), and the dark run
nearest the predicted centre; its midpoint (50 % edges) is the line's centre there and its length the
line's thickness across. Positions where the run is wider than 1.5 times the median (a symbol's ring
merged with the line) are set aside. A straight line is fitted to the rest (3 MAD rejection)."""
import json, sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L"), dtype=float)

def sample(p):
    u, v = p
    u0, v0 = int(np.floor(u)), int(np.floor(v))
    fu, fv = u - u0, v - v0
    return (g[v0, u0] * (1 - fu) * (1 - fv) + g[v0, u0 + 1] * fu * (1 - fv) + g[v0 + 1, u0] * (1 - fu) * fv + g[v0 + 1, u0 + 1] * fu * fv)

def across(p, n, e, half=12):
    s = np.arange(-half, half + 0.001, 0.25)
    prof = np.array([np.mean([sample(p + si * n + ti * e) for ti in (-2, -1, 0, 1, 2)]) for si in s])
    dark = prof < 128
    idx = np.where(dark)[0]
    if len(idx) == 0:
        return None
    runs, st = [], idx[0]
    for a, b in zip(idx, idx[1:]):
        if b != a + 1:
            runs.append((st, a)); st = b
    runs.append((st, idx[-1]))
    a, b = min(runs, key=lambda r: abs((s[r[0]] + s[r[1]]) / 2))
    touches = a == 0 or b == len(s) - 1
    return (s[a] + s[b]) / 2, s[b] - s[a] + 0.25, touches

def trace(P0, P1, step=2.0):
    P0, P1 = np.array(P0, float), np.array(P1, float)
    L = np.linalg.norm(P1 - P0); e = (P1 - P0) / L; n = np.array([-e[1], e[0]])
    rows = []
    for t in np.arange(0, L + 0.001, step):
        p = P0 + t * e
        r = across(p, n, e)
        if r is None:
            rows.append((t, None, None, True)); continue
        off, w, touch = r
        rows.append((t, *(p + off * n), w, touch))
    return e, n, rows

segs = json.loads(sys.argv[2])
out = {}
for name, (P0, P1) in segs.items():
    e, n, rows = trace(P0, P1)
    good = [r for r in rows if len(r) == 5 and not r[4]]
    ws = np.array([r[3] for r in good]); medw = np.median(ws)
    clean = [r for r in good if r[3] <= 1.5 * medw]
    U = np.array([r[1] for r in clean]); V = np.array([r[2] for r in clean])
    # fit u = a + b v (steep lines) or v = a + b u: use the total least squares direction
    X = np.c_[U, V]; m = X.mean(0); _, _, vt = np.linalg.svd(X - m); d = vt[0]; nn = np.array([-d[1], d[0]])
    res = (X - m) @ nn
    mad = 1.4826 * np.median(np.abs(res - np.median(res)))
    keep = np.abs(res) <= max(1.0, 3 * mad)
    X2 = X[keep]; m = X2.mean(0); _, _, vt = np.linalg.svd(X2 - m); d = vt[0]; nn = np.array([-d[1], d[0]])
    res2 = (X2 - m) @ nn
    print(f"{name}: {len(rows)} positions, {len(good)} with ink, {len(clean)} clean, {keep.sum()} kept; median thickness {medw:.2f} px; "
          f"straightness rms {np.sqrt(np.mean(res2**2)):.2f} max {np.abs(res2).max():.2f} px; dir ({d[0]:.4f},{d[1]:.4f}) through ({m[0]:.2f},{m[1]:.2f})")
    wide = [(round(r[1], 1), round(r[2], 1), round(r[3], 1)) for r in good if r[3] > 1.5 * medw]
    if wide: print("   wide (symbol merged):", wide[:3], "...", wide[-3:], len(wide))
    nof = [round(r[0], 1) for r in rows if len(r) != 5 or r[4]]
    if nof: print("   no clean ink at t:", nof[:5], "...", nof[-5:], len(nof))
    out[name] = {"point": m.tolist(), "dir": d.tolist(), "thickness": float(medw), "rms": float(np.sqrt(np.mean(res2**2))),
                 "samples": [[float(r[1]), float(r[2]), float(r[3])] for r in clean]}
json.dump(out, open(sys.argv[3], "w"), indent=1)
