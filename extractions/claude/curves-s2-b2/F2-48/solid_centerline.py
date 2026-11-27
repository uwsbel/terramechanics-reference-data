"""Dense centerline of the solid trace (lpt87, Four-Inch Cylinder) of F2-48.

Row scan (one row v at a time, from the knee near v = 3672 up to the end near v = 1350): in each
row the run of ink nearest the predicted column is taken, with the load grid lines masked; rows on
a penetration grid line are skipped. Column scan for the first, nearly horizontal stretch (from the
bottom frame at u = 2246 left to u = 2040). Each centerline point keeps the horizontal and the
vertical run through it, from which the line's thickness across itself is t = H V / sqrt(H^2 + V^2).
Writes out/F2-48/solid-centerline.csv.
"""
import csv
import numpy as np
from trace_lib import B, NV, NU, HL, VL, u_line, v_line, h_half, v_half, runs_1d, near_h_grid, near_v_grid

vv, uu = np.mgrid[0:NV, 0:NU]
vmask = np.zeros_like(B)
for L in VL:
    vmask |= np.abs(uu - u_line(L, vv)) <= v_half(L)
hmask = np.zeros_like(B)
for L in HL:
    hmask |= np.abs(vv - v_line(L, uu)) <= h_half(L)
Bv = B & ~vmask      # ink without the load grid lines
Bh = B & ~hmask      # ink without the penetration grid lines


def vrun(u, v):
    """vertical run of raw ink through (u, v)"""
    if not B[v, u]:
        return 0
    a = v
    while B[a - 1, u]:
        a -= 1
    b = v
    while B[b + 1, u]:
        b += 1
    return b - a + 1


def hrun(u, v):
    if not B[v, u]:
        return 0
    a = u
    while B[v, a - 1]:
        a -= 1
    b = u
    while B[v, b + 1]:
        b += 1
    return b - a + 1


pts = []   # (scan, u, v, run_a, run_b, flag)

# ---- column scan: the first, nearly horizontal stretch, from the frame leftwards
pred = 3740.0
for u in range(2215, 2039, -1):
    col = Bh[3640:3758, u]
    rs = [(a + 3640, b + 3640) for a, b in runs_1d(col)]
    best = None
    for a, b in rs:
        c = (a + b) / 2
        if abs(c - pred) <= 9 and (b - a + 1) <= 30:
            if best is None or abs(c - pred) < abs((best[0] + best[1]) / 2 - pred):
                best = (a, b)
    if best is None:
        pts.append(("col", u, None, None, None, "missing"))
        continue
    a, b = best
    c = (a + b) / 2
    flag = "grid" if near_v_grid(u, c, 2) is not None else ""
    pts.append(("col", u, c, a, b, flag))
    pred = c

# ---- row scan: from the knee up to the end
pred_u = 2030.0
hist = []
miss = 0
for v in range(3672, 1330, -1):
    if near_h_grid(pred_u, v, 0.5) is not None:
        pts.append(("row", None, v, None, None, "hgrid"))
        continue
    row = Bv[v, 900:2300]
    rs = [(a + 900, b + 900) for a, b in runs_1d(row)]
    # slope prediction from the last good rows
    if len(hist) >= 6:
        h = np.array(hist[-20:])
        p = np.polyfit(h[:, 0], h[:, 1], 1)
        pu = np.polyval(p, v)
    else:
        pu = pred_u
    best = None
    for a, b in rs:
        c = (a + b) / 2
        if abs(c - pu) <= min(8 + 2 * miss, 30) and (b - a + 1) <= 30:
            if best is None or abs(c - pu) < abs((best[0] + best[1]) / 2 - pu):
                best = (a, b)
    if best is None:
        pts.append(("row", None, v, None, None, "missing"))
        miss += 1
        continue
    a, b = best
    c = (a + b) / 2
    flag = ""
    L = near_v_grid(c, v, 1)
    if L is not None or vmask[v, a - 1] or vmask[v, b + 1]:
        flag = "vgrid"
    pts.append(("row", c, v, a, b, flag))
    if not flag:
        hist.append((v, c))
        miss = 0
    else:
        miss += 1
    pred_u = c

with open("out/F2-48/solid-centerline.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["scan", "u", "v", "run_a", "run_b", "hrun", "vrun", "t_perp", "flag"])
    for s, u, v, a, b, flag in pts:
        if u is None or v is None:
            w.writerow([s, u, v, a, b, "", "", "", flag])
            continue
        ui, vi = int(round(u)), int(round(v))
        H, V = hrun(ui, vi), vrun(ui, vi)
        if s == "row":
            H = b - a + 1
        else:
            V = b - a + 1
        t = H * V / np.hypot(H, V) if H and V else ""
        w.writerow([s, u, v, a, b, H, V, f"{t:.2f}" if t != "" else "", flag])
n = sum(1 for p in pts if p[5] == "")
print(len(pts), "rows/cols;", n, "clean;", sum(1 for p in pts if p[5] == "missing"), "missing;",
      sum(1 for p in pts if p[5] in ("vgrid", "grid")), "at load grid lines")
miss = [p for p in pts if p[5] == "missing"]
print("missing at:", [(p[0], p[1] if p[0] == "col" else p[2]) for p in miss][:60])
