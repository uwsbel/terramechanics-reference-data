"""Centrelines from the decomposition aids: steep part by column (steep3.csv), tail by row (tail3.csv).
lower = top dashed (steep) / right dashed (tail); upper = bottom dashed (steep) / left dashed (tail);
average = robust smoothing spline through the solid-line observations. Writes centerlines.json and an overlay."""
import sys, csv, json
import numpy as np
from PIL import Image, ImageDraw
WS = sys.argv[1]
HALF = 5.5
def basis(x, x0, x1, nk):
    t = np.linspace(x0, x1, nk); h = t[1] - t[0]; B = []
    for k in range(-1, nk + 1):
        z = np.abs((x - (x0 + k * h)) / h)
        B.append(np.where(z < 1, 2 / 3 - z ** 2 + z ** 3 / 2, np.where(z < 2, (2 - z) ** 3 / 6, 0)))
    return np.array(B).T
def robust_spline(x, y, x0, x1, nk, lam=3e-3, it=8, c=4.0):
    B = basis(x, x0, x1, nk); w = np.ones(len(x)); D = np.diff(np.eye(B.shape[1]), 2, axis=0)
    for _ in range(it):
        Wm = B.T * w
        coef = np.linalg.solve(Wm @ B + lam * len(x) * D.T @ D, Wm @ y)
        r = y - B @ coef
        s = 1.4826 * np.median(np.abs(r)) + 0.5
        w = 1.0 / (1.0 + (r / (c * s)) ** 2)
    return coef
out = {}
S = list(csv.DictReader(open(WS + "/out/FA-6/helpers/steep3.csv")))
us = np.array([float(r["u"]) for r in S]); eT = np.array([float(r["envT"]) for r in S]); eB = np.array([float(r["envB"]) for r in S])
xs, ys = [], []
for r in S:
    for s in r["solid_obs"].split(";") if r["solid_obs"] else []:
        xs.append(float(r["u"])); ys.append(float(s.split(":")[1]))
xs, ys = np.array(xs), np.array(ys)
u0, u1 = us.min(), us.max()
cs = robust_spline(xs, ys, u0, u1, 24)
avg = basis(us, u0, u1, 24) @ cs
# support: number of solid observations within +-20 px
sup = np.array([np.sum(np.abs(xs - u) <= 20) for u in us])
out["steep"] = dict(u=us.tolist(), lower=(eT + HALF).tolist(), upper=(eB - HALF).tolist(), average=avg.tolist(),
                    tdash=[int(float(r["top"]) <= float(r["envT"]) + 3.5) for r in S], bdash=[int(float(r["bot"]) >= float(r["envB"]) - 3.5) for r in S], avg_support=sup.tolist(),
                    envT=eT.tolist(), envB=eB.tolist())
T = list(csv.DictReader(open(WS + "/out/FA-6/helpers/tail3.csv")))
vs = np.array([float(r["v"]) for r in T]); eL = np.array([float(r["envL"]) for r in T]); eR = np.array([float(r["envR"]) for r in T])
xs, ys = [], []
for r in T:
    for s in r["solid_obs"].split(";") if r["solid_obs"] else []:
        xs.append(float(r["v"])); ys.append(float(s.split(":")[1]))
xs, ys = np.array(xs), np.array(ys)
v0, v1 = vs.min(), vs.max()
ct = robust_spline(xs, ys, v0, v1, 16)
avg_t = basis(vs, v0, v1, 16) @ ct
supt = np.array([np.sum(np.abs(xs - v) <= 20) for v in vs])
out["tail"] = dict(v=vs.tolist(), upper=(eL + HALF).tolist(), lower=(eR - HALF).tolist(), average=avg_t.tolist(),
                   ldash=[int(float(r["L"]) <= float(r["envL"]) + 3.5) for r in T], rdash=[int(float(r["R"]) >= float(r["envR"]) - 3.5) for r in T], avg_support=supt.tolist(),
                   envL=eL.tolist(), envR=eR.tolist(), frame_left=[float(r["frame_left"]) for r in T])
json.dump(out, open(WS + "/out/FA-6/helpers/centerlines.json", "w"))
im = Image.open(WS + "/packet/p0014.png").convert("RGB"); d = ImageDraw.Draw(im)
st = out["steep"]
for i, u in enumerate(st["u"]):
    d.point([(u, st["lower"][i])], fill=(255, 120, 0)); d.point([(u, st["upper"][i])], fill=(0, 90, 255))
    d.point([(u, st["average"][i])], fill=(0, 190, 0) if st["avg_support"][i] else (170, 255, 170))
tl = out["tail"]
for i, v in enumerate(tl["v"]):
    d.point([(tl["lower"][i], v)], fill=(255, 120, 0)); d.point([(tl["upper"][i], v)], fill=(0, 90, 255))
    d.point([(tl["average"][i], v)], fill=(0, 190, 0) if tl["avg_support"][i] else (170, 255, 170))
im.save(WS + "/out/FA-6/helpers/centerlines-overlay.png")
print("ok; solid obs steep", len(cs), "tail obs", len(xs))
