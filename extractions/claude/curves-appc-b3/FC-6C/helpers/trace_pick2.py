"""Candidate trace samples for one series (reading aid; every sample is reviewed on the image).
At every column u in [u0, u1]: the dark run (3 adjacent columns all dark, >= 5 px) nearest the
expected position (continuity from the last accepted column, slope from the series' markers),
within tol px. Columns within 8 px of a vertical gridline, or inside a marker's footprint
(any series; half-size by symbol + 2 px) are not used. Then a greedy pass keeps samples no more
than `step` px apart where the ink allows, and the columns right at the edges of each gap.
usage: trace_pick2.py <image> <markers.csv> <calibration.json> <series> <u0> <u1> <step> [tol]"""
import csv, json, sys
import numpy as np
from PIL import Image
img, mk, calp, sid = sys.argv[1:5]
u0, u1, step = int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
tol = float(sys.argv[8]) if len(sys.argv) > 8 else 12
HW = {"plus": 14, "square": 16, "triangle-up": 16, "triangle-down": 16, "circle": 12}
g = np.asarray(Image.open(img).convert("L")) < 128
cal = json.load(open(calp, encoding="utf-8"))
M = list(csv.DictReader(open(mk, encoding="utf-8")))
own = sorted((float(r["u"]), float(r["v"])) for r in M if r["series_id"] == sid)
allm = [(float(r["u"]), float(r["v"]), HW[r["symbol"]] + 2) for r in M]
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
valid = {}
offs = []  # offsets of accepted runs from the marker-interpolated line (robust continuity)
for u in range(u0, u1 + 1):
    base = float(np.interp(u, ou, ov))
    pred = base + (float(np.median(offs[-7:])) if offs else 0.0)
    if any(abs(u - (a + b * pred)) <= 8 for a, b in vl): continue
    if any(abs(m[0] - u) <= m[2] and abs(m[1] - pred) <= m[2] + 6 for m in allm): continue
    lo, hi = int(pred - 40), int(pred + 40)
    col = g[lo:hi, u - 1:u + 2].min(axis=1)
    rr = [(lo + s, lo + p) for s, p in runs(col) if p - s + 1 >= 5]
    rr = [r for r in rr if abs((r[0] + r[1]) / 2 - pred) <= tol]
    if not rr: continue
    best = min(rr, key=lambda r: abs((r[0] + r[1]) / 2 - pred))
    c = (best[0] + best[1]) / 2; L = best[1] - best[0] + 1
    gy = [y for a, b, y in hl if best[0] - 2 <= a + b * u <= best[1] + 2]
    if gy and L <= 7:  # a thin run on a horizontal gridline is the gridline alone
        continue
    valid[u] = (c, L, gy, best)
    offs.append(c - base)
us = sorted(valid)
sel = []
if us:
    u = us[0]; sel.append(u)
    while True:
        nxt = [x for x in us if u < x <= u + step]
        if nxt:
            # inside a run of valid columns: take the farthest; if a gap follows, take its edge
            far = max(nxt)
            u = far
        else:
            later = [x for x in us if x > u]
            if not later: break
            u = min(later)
        sel.append(u)
        if u == us[-1]: break
    # also keep the last valid column before each gap
    for i in range(len(us) - 1):
        if us[i + 1] - us[i] > 3 and us[i] not in sel: sel.append(us[i])
    sel = sorted(set(sel))
    ded = []
    for u in sel:
        if ded and u - ded[-1] < 6 and u != us[-1]:
            continue
        ded.append(u)
    sel = ded
print("u,v,run_len,v0,v1,flags")
for u in sel:
    c, L, gy, b = valid[u]
    fl = ("HGRID" + "/".join(f"{y:g}" for y in gy)) if gy else ""
    print(f"{u},{c:.1f},{L},{b[0]},{b[1]},{fl}")
