"""Steep part decomposition aid (see notes.md). Per column u: ink runs of the de-gridded aid near the band;
rows of major/dashed horizontal grid lines flagged; global asymmetric cubic-spline envelopes for the outer
edges of the two dashed curves; the solid curve from columns where it shows alone or next to a white gap.
Output: steep3.csv (per column) and steep3-overlay.png (page with envelopes and solid estimates)."""
import sys, csv, json
import numpy as np
from PIL import Image, ImageDraw
WS = sys.argv[1]
U0, U1 = int(sys.argv[2]), int(sys.argv[3])
g = np.asarray(Image.open(WS + "/out/FA-6/degrid.png").convert("L")) < 128
TILT = -0.003
GRID = [(1450, 1455, 1250), (1516, 1524, 1250), (1592, 1599, 1250), (1639, 1647, 1250), (1715, 1717, 1850),
        (1742, 1747, 1850), (1809, 1817, 1850), (1890, 1895, 950), (1932, 1940, 950), (1964, 1964, 950),
        (2028, 2036, 950), (2103, 2110, 950)]
def grid_rows(u):
    s = set()
    for a, b, ur in GRID:
        d = TILT * (u - ur)
        for v in range(int(np.floor(a + d)) - 1, int(np.ceil(b + d)) + 2):
            s.add(v)
    return s
path = [(830, 1680), (850, 1700), (920, 1740), (1000, 1760), (1100, 1790), (1200, 1812), (1300, 1832),
        (1400, 1855), (1500, 1876), (1600, 1892), (1700, 1915), (1800, 1938), (1900, 1958), (2000, 1990),
        (2060, 2015), (2100, 2040)]
pu = np.array([p[0] for p in path], float); pv = np.array([p[1] for p in path], float)

def runs_in(u, v0, v1):
    idx = np.where(g[v0:v1, u])[0]
    rr = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i > p + 1:
                rr.append([int(s + v0), int(p + v0)]); s = i
            p = i
        rr.append([int(s + v0), int(p + v0)])
    # drop specks (<= 3 px) not within 2 px of a larger run
    big = [r for r in rr if r[1] - r[0] + 1 > 3]
    keep = [r for r in rr if r[1] - r[0] + 1 > 3 or any(abs(r[0] - b[1]) <= 3 or abs(b[0] - r[1]) <= 3 for b in big)]
    return keep

us = np.arange(U0, U1 + 1)
# pass 1: ink centre
m = []
for u in us:
    c = np.interp(u, pu, pv)
    rr = runs_in(u, int(c - 40), int(c + 40))
    w = sum(r[1] - r[0] + 1 for r in rr)
    m.append(sum((r[0] + r[1]) / 2 * (r[1] - r[0] + 1) for r in rr) / w if w else np.nan)
m = np.array(m)
p2 = np.array([np.nanmedian(m[max(0, i - 30):i + 31]) for i in range(len(us))])
recs = []
for i, u in enumerate(us):
    c = p2[i]
    rr = runs_in(u, int(c - 27), int(c + 28))
    if not rr:
        recs.append(None); continue
    gr = grid_rows(u)
    top, bot = rr[0][0], rr[-1][1]
    gaps = [(rr[j][1] + 1, rr[j + 1][0] - 1) for j in range(len(rr) - 1)]
    # circle symbols (centres read on crops m2, m3) are not curve edges
    in_m2 = 1694 <= u <= 1734
    in_m3 = 1538 <= u <= 1582
    recs.append(dict(u=int(u), runs=rr, top=top, bot=bot,
                     top_ok=(top - 1) not in gr and top not in gr and top > c - 26 and not in_m2,
                     bot_ok=(bot + 1) not in gr and bot not in gr and bot < c + 27 and not in_m3,
                     gaps=[(a, b, not any(v in gr for v in range(a - 1, b + 2))) for a, b in gaps]))

def bspline_basis(x, x0, x1, nk):
    t = np.linspace(x0, x1, nk)
    h = t[1] - t[0]
    B = []
    for k in range(-1, nk + 1):
        z = (x - (x0 + k * h)) / h
        a = np.abs(z)
        b = np.where(a < 1, 2 / 3 - a ** 2 + a ** 3 / 2, np.where(a < 2, (2 - a) ** 3 / 6, 0))
        B.append(b)
    return np.array(B).T

def asym_fit(x, y, outer_sign, nk, it=12, inner_w=0.01, tol=2.5, lam=1e-3):
    """outer_sign -1: outer side is smaller y (top edge); +1: larger y (bottom edge)"""
    B = bspline_basis(x, U0, U1, nk)
    w = np.ones(len(x))
    D = np.diff(np.eye(B.shape[1]), 2, axis=0)
    for _ in range(it):
        Wm = B.T * w
        coef = np.linalg.solve(Wm @ B + lam * len(x) * D.T @ D, Wm @ y)
        f = B @ coef
        inside = (y - f) * (-outer_sign)      # >0 = inside the band
        w = np.where(inside > tol, inner_w, 1.0)
    return coef, f

R = [r for r in recs if r]
xt = np.array([r["u"] for r in R if r["top_ok"]], float); yt = np.array([r["top"] for r in R if r["top_ok"]], float)
xb = np.array([r["u"] for r in R if r["bot_ok"]], float); yb = np.array([r["bot"] for r in R if r["bot_ok"]], float)
NK = int(sys.argv[4]) if len(sys.argv) > 4 else 30
ct, _ = asym_fit(xt, yt, -1, NK)
cb, _ = asym_fit(xb, yb, +1, NK)
envT = bspline_basis(us.astype(float), U0, U1, NK) @ ct
envB = bspline_basis(us.astype(float), U0, U1, NK) @ cb
rows = []
for i, r in enumerate(recs):
    if r is None:
        continue
    eT, eB = envT[i], envB[i]
    tdash = r["top_ok"] and r["top"] <= eT + 3
    bdash = r["bot_ok"] and r["bot"] >= eB - 3
    sol = []
    if len(r["runs"]) == 1 and 8 <= r["bot"] - r["top"] + 1 <= 16 and r["top_ok"] and r["bot_ok"] and r["top"] > eT + 6 and r["bot"] < eB - 6:
        sol.append(("alone", 0.5 * (r["top"] + r["bot"])))
    for a, b, ok in r["gaps"]:
        if not ok:
            continue
        if abs(a - (eT + 11.5)) <= 4 and b + 1 < eB - 8:
            sol.append(("tgap", b + 1 + 5.5))
        if abs(b - (eB - 11.5)) <= 4 and a - 1 > eT + 8:
            sol.append(("bgap", a - 1 - 5.5))
    rows.append([r["u"], r["top"], r["bot"], round(eT, 2), round(eB, 2), int(tdash), int(bdash),
                 ";".join(f"{k}:{v:.1f}" for k, v in sol),
                 ";".join(f"{a}-{b}" for a, b in r["runs"])])
with open(WS + "/out/FA-6/helpers/steep3.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["u", "top", "bot", "envT", "envB", "tdash", "bdash", "solid_obs", "runs"]); w.writerows(rows)
im = Image.open(WS + "/packet/p0014.png").convert("RGB"); d = ImageDraw.Draw(im)
for row in rows:
    u, eT, eB = row[0], row[3], row[4]
    d.point([(u, eT)], fill=(255, 0, 0)); d.point([(u, eB)], fill=(0, 0, 255))
    d.point([(u, eT + 5.5)], fill=(255, 140, 0) if row[5] else (255, 220, 160))
    d.point([(u, eB - 5.5)], fill=(0, 160, 255) if row[6] else (160, 220, 255))
    for s in row[7].split(";") if row[7] else []:
        v = float(s.split(":")[1]); d.rectangle([u - 1, v - 1, u + 1, v + 1], fill=(0, 200, 0))
im.save(WS + "/out/FA-6/helpers/steep3-overlay.png")
print("rows", len(rows))
