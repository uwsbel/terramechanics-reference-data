"""Tail (curves nearly vertical on the page, next to the 0 percent frame): per row v, ink runs of the de-gridded aid
between U_LO and the frame's left edge; envelopes of the left edge (outer edge of the left dashed curve) and of the
right edge (outer edge of the right dashed curve) by asymmetric cubic splines; the solid curve from rows where it
shows alone or bounded by a white gap. Output tail3.csv and tail3-overlay.png."""
import sys, csv
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("\\", 1)[0])
WS = sys.argv[1]
V0, V1 = int(sys.argv[2]), int(sys.argv[3]); NK = int(sys.argv[4])
g = np.asarray(Image.open(WS + "/out/FA-6/degrid.png").convert("L")) < 128
pg = np.asarray(Image.open(WS + "/packet/p0014.png").convert("L")) < 128
# horizontal grid rows: dark over most of u 2120..2178 on the page (left of the band); an edge on them is not used
gridrow = set()
for vv in range(V0 - 5, V1 + 6):
    if pg[vv, 2120:2178].mean() > 0.5:
        gridrow.update((vv - 1, vv, vv + 1))
def frame_left(v):          # 0 percent frame: u = 2243.0 + 0.0042 v (cal-p1), about 10 px thick
    return 2243.0 + 0.0042 * v - 5.0
path = [(2140, 2175), (2200, 2205), (2300, 2218), (2400, 2222), (2500, 2228), (2600, 2232), (2700, 2236), (2800, 2236), (2900, 2240), (2960, 2242)]
pv = np.array([p[0] for p in path], float); pu = np.array([p[1] for p in path], float)
recs = []
for v in range(V0, V1 + 1):
    c = np.interp(v, pv, pu)
    fl = int(np.floor(frame_left(v))) - 1
    a0, a1 = int(c - 30), min(int(c + 30), fl)
    idx = np.where(g[v, a0:a1])[0]
    rr = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i > p + 1:
                rr.append([int(s + a0), int(p + a0)]); s = i
            p = i
        rr.append([int(s + a0), int(p + a0)])
    big = [r for r in rr if r[1] - r[0] + 1 > 3]
    rr = [r for r in rr if r[1] - r[0] + 1 > 3 or any(abs(r[0] - b[1]) <= 3 or abs(b[0] - r[1]) <= 3 for b in big)]
    if not rr:
        recs.append(None); continue
    L, R = rr[0][0], rr[-1][1]
    recs.append(dict(v=v, runs=rr, L=L, R=R, L_ok=L > a0 + 1 and v not in gridrow, R_ok=R < a1 - 2 and v not in gridrow,
                     gaps=[(rr[j][1] + 1, rr[j + 1][0] - 1) for j in range(len(rr) - 1)]))

def basis(x, x0, x1, nk):
    t = np.linspace(x0, x1, nk); h = t[1] - t[0]; B = []
    for k in range(-1, nk + 1):
        z = np.abs((x - (x0 + k * h)) / h)
        B.append(np.where(z < 1, 2 / 3 - z ** 2 + z ** 3 / 2, np.where(z < 2, (2 - z) ** 3 / 6, 0)))
    return np.array(B).T
def asym(x, y, sign, it=12, tol=2.5, lam=1e-3):
    B = basis(x, V0, V1, NK); w = np.ones(len(x)); D = np.diff(np.eye(B.shape[1]), 2, axis=0)
    for _ in range(it):
        Wm = B.T * w
        c = np.linalg.solve(Wm @ B + lam * len(x) * D.T @ D, Wm @ y)
        inside = (y - B @ c) * (-sign)
        w = np.where(inside > tol, 0.01, 1.0)
    return c
Rr = [r for r in recs if r]
xl = np.array([r["v"] for r in Rr if r["L_ok"]], float); yl = np.array([r["L"] for r in Rr if r["L_ok"]], float)
xr = np.array([r["v"] for r in Rr if r["R_ok"]], float); yr = np.array([r["R"] for r in Rr if r["R_ok"]], float)
cl = asym(xl, yl, -1); cr = asym(xr, yr, +1)
vs = np.arange(V0, V1 + 1).astype(float)
eL = basis(vs, V0, V1, NK) @ cl; eR = basis(vs, V0, V1, NK) @ cr
rows = []
for i, r in enumerate(recs):
    if r is None:
        continue
    l, rr_ = eL[i], eR[i]
    ld = r["L_ok"] and r["L"] <= l + 3
    rd = r["R_ok"] and r["R"] >= rr_ - 3
    sol = []
    if len(r["runs"]) == 1 and 8 <= r["R"] - r["L"] + 1 <= 16 and r["L"] > l + 6 and r["R"] < rr_ - 6:
        sol.append(("alone", 0.5 * (r["L"] + r["R"])))
    for a, b in r["gaps"]:
        if abs(a - (l + 11.5)) <= 4 and b + 1 < rr_ - 8:
            sol.append(("lgap", b + 1 + 5.5))
        if abs(b - (rr_ - 11.5)) <= 4 and a - 1 > l + 8:
            sol.append(("rgap", a - 1 - 5.5))
    rows.append([r["v"], r["L"], r["R"], round(l, 2), round(rr_, 2), int(ld), int(rd), ";".join(f"{k}:{x:.1f}" for k, x in sol),
                 ";".join(f"{a}-{b}" for a, b in r["runs"]), round(frame_left(r["v"]), 1)])
with open(WS + "/out/FA-6/helpers/tail3.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["v", "L", "R", "envL", "envR", "ldash", "rdash", "solid_obs", "runs", "frame_left"]); w.writerows(rows)
im = Image.open(WS + "/packet/p0014.png").convert("RGB"); d = ImageDraw.Draw(im)
for row in rows:
    v, l, rr_ = row[0], row[3], row[4]
    d.point([(l, v)], fill=(255, 0, 0)); d.point([(rr_, v)], fill=(0, 0, 255))
    d.point([(l + 5.5, v)], fill=(255, 140, 0) if row[5] else (255, 220, 160))
    d.point([(rr_ - 5.5, v)], fill=(0, 160, 255) if row[6] else (160, 220, 255))
    for s in row[7].split(";") if row[7] else []:
        x = float(s.split(":")[1]); d.rectangle([x - 1, v - 1, x + 1, v + 1], fill=(0, 200, 0))
im.save(WS + "/out/FA-6/helpers/tail3-overlay.png")
print("rows", len(rows))
