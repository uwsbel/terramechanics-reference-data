"""Candidate trace samples for one series: at each column, the dark run nearest the series'
marker-interpolated position. Prints u, run center v, run length, flags. A reading aid only:
every sample is reviewed on the image before it is written to points.
usage: tracker.py <image> <markers.csv> <calibration.json> <series> <u0> <u1> <step> [tol]"""
import csv, json, sys
import numpy as np
from PIL import Image
img, mk, calp, sid = sys.argv[1:5]
u0, u1, step = int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
tol = float(sys.argv[8]) if len(sys.argv) > 8 else 25
g = np.asarray(Image.open(img).convert("L")) < 128
cal = json.load(open(calp, encoding="utf-8"))
M = [r for r in csv.DictReader(open(mk, encoding="utf-8"))]
own = sorted([(float(r["u"]), float(r["v"])) for r in M if r["series_id"] == sid])
allm = [(float(r["u"]), float(r["v"]), r["series_id"]) for r in M]
ou, ov = np.array([a for a, b in own]), np.array([b for a, b in own])
vl = [(l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
hl = [(l["v_at_u0"], l["slope_dv_du"], l["y_value"]) for l in cal["horizontal_lines"]]
def runs(col):
    idx = np.where(col)[0]; out = []
    if len(idx) == 0: return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1: out.append((s, p)); s = i
        p = i
    out.append((s, p)); return out
prev = None
for u in range(u0, u1 + 1, step):
    pred = float(np.interp(u, ou, ov))
    if prev is not None and abs(prev[1] - pred) > 0:  # blend with continuity
        pred = 0.5 * pred + 0.5 * (prev[1] + (np.interp(u, ou, ov) - np.interp(prev[0], ou, ov)))
    flags = []
    if any(abs(u - (a + b * pred)) <= 7 for a, b in vl): flags.append("VGRID")
    near = [m for m in allm if abs(m[0] - u) <= 17 and abs(m[1] - pred) <= 25]
    if near: flags.append("MARKER:" + "/".join(f"{m[2]}@{m[0]:.0f}" for m in near))
    lo, hi = int(pred - 60), int(pred + 60)
    col = g[lo:hi, u - 1:u + 2].min(axis=1)  # all three columns dark
    rr = [(lo + s, lo + p) for s, p in runs(col)]
    if not rr:
        print(f"{u},NA,0,{' '.join(flags)} no-run"); continue
    best = min(rr, key=lambda r: abs((r[0] + r[1]) / 2 - pred))
    c = (best[0] + best[1]) / 2; L = best[1] - best[0] + 1
    if abs(c - pred) > tol: flags.append(f"FAR({c - pred:+.0f})")
    for a, b, y in hl:
        gv = a + b * u
        if best[0] - 2 <= gv <= best[1] + 2: flags.append(f"HGRID{y:g}")
    others = [f"{(s+p)/2:.0f}/{p-s+1}" for s, p in rr if (s, p) != best]
    print(f"{u},{c:.1f},{L},{' '.join(flags)}  pred={pred:.0f} others={' '.join(others)}")
    if not flags or all(f.startswith("HGRID") for f in flags):
        prev = (u, c)
