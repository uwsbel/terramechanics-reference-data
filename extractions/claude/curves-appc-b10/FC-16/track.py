"""Track the three curves of FC-16 column by column on the page ink (helper for the blind reading).
Prediction from a straight fit to the last 80 px of accepted ink; a run is accepted when its center is
within 4 px of the prediction and it is no thicker than 9 px (thicker: merged with a grid line, a circle
or another curve)."""
import sys, json
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")).astype(float)
DARK = 128
seeds = {"upper": (652, 2412.0, -0.55), "mean": (652, 2446.0, -0.47), "lower": (654, 2522.0, -0.40)}
def runs(col, v0):
    idx = np.where(col < DARK)[0]
    out = []
    if len(idx) == 0: return out
    s = p = idx[0]
    for i in list(idx[1:]) + [None]:
        if i is None or i != p + 1:
            seg = col[s:p+1]; w = 255 - seg
            c = float(np.sum(np.arange(s, p+1) * w) / np.sum(w))
            out.append((int(v0 + s), int(v0 + p), float(v0 + c)))
            if i is None: break
            s = i
        p = i
    return out
res = {}
for name, (u0, vs, sl) in seeds.items():
    pts = []
    hist = [(u0 - 1, vs)]
    for u in range(u0, 2570):
        H = np.array([h for h in hist if h[0] >= u - 80])
        if len(H) >= 15:
            k, b = np.polyfit(H[:, 0], H[:, 1], 1); pred = k * u + b
        else:
            H2 = np.array(hist[-40:])
            if len(H2) >= 15:
                k, b = np.polyfit(H2[:, 0], H2[:, 1], 1); pred = k * u + b
            else:
                pred = hist[-1][1] + sl * (u - hist[-1][0])
        lo, hi = int(pred - 30), int(pred + 30)
        rr = runs(g[lo:hi, u], lo)
        cand = [r for r in rr if r[0] <= pred + 4 and r[1] >= pred - 4]
        if not cand:
            pts.append((u, "gap", None, None, round(pred, 2))); continue
        r = min(cand, key=lambda r: abs(r[2] - pred))
        L = r[1] - r[0] + 1
        if L > 9 or abs(r[2] - pred) > 4:
            pts.append((u, "merged", r[0], r[1], round(pred, 2))); continue
        pts.append((u, "ink", r[0], r[1], round(r[2], 2))); hist.append((u, r[2]))
    res[name] = pts
    segs = []; cur = None
    for p in pts:
        if cur is None or p[1] != cur[0]:
            if cur: segs.append(cur)
            cur = [p[1], p[0], p[0], p[4], p[4], []]
        cur[2] = p[0]; cur[4] = p[4]
        if p[1] == "ink": cur[5].append(p[3] - p[2] + 1)
    segs.append(cur)
    print(f"== {name}")
    for s in segs:
        if s[0] != "ink" and s[2] - s[1] < 12: continue
        th = f" thick(v) med {np.median(s[5]):.0f}" if s[5] else ""
        print(f"  {s[0]:6s} u {s[1]}..{s[2]}  v {s[3]}..{s[4]}{th}")
json.dump(res, open(sys.argv[2], "w"))
