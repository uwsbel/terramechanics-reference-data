"""Pick candidate trace samples for one series between u0 and u1 (spacing ~step), at columns
away from vertical gridlines and from markers of any series; the dark run (3 adjacent columns
all dark) nearest the expected position, preferring a run at least 7 px long over a thin run on
a horizontal gridline. Output CSV rows u,v,run_len,flags. A reading aid: every sample is
reviewed on the page image (overlay and ASCII crops) before it goes into the points file.
usage: trace_pick.py <image> <markers.csv> <calibration.json> <series> <u0> <u1> <step> [tol] [exclude_px]"""
import csv, json, sys
import numpy as np
from PIL import Image
img, mk, calp, sid = sys.argv[1:5]
u0, u1, step = int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
tol = float(sys.argv[8]) if len(sys.argv) > 8 else 22
ex = float(sys.argv[9]) if len(sys.argv) > 9 else 17
g = np.asarray(Image.open(img).convert("L")) < 128
cal = json.load(open(calp, encoding="utf-8"))
M = list(csv.DictReader(open(mk, encoding="utf-8")))
own = sorted((float(r["u"]), float(r["v"])) for r in M if r["series_id"] == sid)
allm = [(float(r["u"]), float(r["v"])) for r in M]
ou = np.array([a for a, b in own]); ov = np.array([b for a, b in own])
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
prev = None; last_u = -999
print("u,v,run_len,flags")
for u in range(u0, u1 + 1):
    if u - last_u < step: continue
    base = float(np.interp(u, ou, ov))
    pred = base if prev is None else prev[1] + (base - float(np.interp(prev[0], ou, ov)))
    if any(abs(u - (a + b * pred)) <= 8 for a, b in vl): continue
    if any(abs(m[0] - u) <= ex and abs(m[1] - pred) <= 22 for m in allm): continue
    lo, hi = int(pred - 50), int(pred + 50)
    col = g[lo:hi, u - 1:u + 2].min(axis=1)
    rr = [(lo + s, lo + p) for s, p in runs(col) if p - s + 1 >= 3]
    rr = [r for r in rr if abs((r[0] + r[1]) / 2 - pred) <= tol]
    if not rr: continue
    def ongrid(r):
        return [y for a, b, y in hl if r[0] - 2 <= a + b * u <= r[1] + 2]
    thick = [r for r in rr if r[1] - r[0] + 1 >= 7]
    cand = thick if thick else rr
    best = min(cand, key=lambda r: abs((r[0] + r[1]) / 2 - pred))
    c = (best[0] + best[1]) / 2; L = best[1] - best[0] + 1
    fl = []
    gy = ongrid(best)
    if gy: fl.append("HGRID" + "/".join(f"{y:g}" for y in gy))
    if L < 7: fl.append("THIN")
    print(f"{u},{c:.1f},{L},{' '.join(fl)}")
    prev = (u, c); last_u = u
