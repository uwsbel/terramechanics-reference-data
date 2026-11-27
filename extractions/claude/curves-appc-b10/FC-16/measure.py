"""Measure the ink centre line of each dash (or stretch of the solid curve) of FC-16, column by column.
Dash extents are the reader's, from the column classification (dashes.py) checked on zoomed crops.
Columns under a grid line (+-5 px), a horizontal grid line (+-7 px, inside the frame), a circle (<= 22 px
from its centre) or a frame are skipped; elsewhere the dark run (gray < 128) overlapping the prediction
+-4 px and no thicker than 13 px gives the centre (darkness weighted). Two passes: straight guess, then a
quadratic fit to the first pass. Writes measured.json: per curve, per dash, [u, v, vertical thickness]."""
import json
import numpy as np
from PIL import Image
g = np.asarray(Image.open("packet/p0152.png").convert("L")).astype(float)
cal = json.load(open("out/FC-16/cal-p1/calibration.json"))
VL = [(l["x_value"], l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
HL = [(l["y_value"], l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
CIRC = {"p1L": (642.2, 2458.4), "p1R": (793.5, 2453.0), "p2L": (1563.6, 1919.4), "p2R": (1679.0, 1921.8),
        "p3L": (1923.7, 1848.3), "p3R": (2146.5, 1847.0), "p4L": (2345.2, 1532.3), "p4R": (2547.7, 1528.6),
        "sTop": (2498.5, 1391.8), "sMid": (2501.3, 1617.0), "sLow": (2500.2, 1846.6)}
def zone(u, v):
    z = []
    for val, u0, k in VL:
        if abs(u - (u0 + k * v)) <= 5: z.append(f"vline {val:g}")
    if 652 < u < 2488:
        for val, v0, k in HL:
            if abs(v - (v0 + k * u)) <= 7: z.append(f"hline {val:g}")
    for n, (cu, cv) in CIRC.items():
        if np.hypot(u - cu, v - cv) <= 22: z.append(f"circle {n}")
    if u <= 652 or 2488 <= u <= 2507: z.append("frame")
    return z
def run_at(u, p):
    lo = int(p) - 20
    col = g[lo:lo + 41, u]
    d = col < 128
    best = None
    i = 0
    while i < len(d):
        if d[i]:
            j = i
            while j + 1 < len(d) and d[j + 1]: j += 1
            a, b = lo + i, lo + j
            if a <= p + 4 and b >= p - 4:
                w = 255 - col[i:j + 1]
                c = float(np.sum(np.arange(a, b + 1) * w) / np.sum(w))
                if best is None or abs(c - p) < abs(best[0] - p): best = (c, b - a + 1)
            i = j + 1
        else: i += 1
    return best
# dashes: (u_start, v_start_guess, u_end, v_end_guess)
DASHES = {
 "upper": [(653, 2413, 724, 2374), (764, 2349, 870, 2289), (898, 2273, 995, 2218), (1017, 2205, 1118, 2150),
           (1148, 2133, 1270, 2067), (1308, 2047, 1416, 1991), (1450, 1972, 1536, 1930), (1583, 1908, 1676, 1863),
           (1704, 1850, 1824, 1792), (1856, 1776, 1977, 1714), (1996, 1704, 2121, 1637), (2147, 1622, 2278, 1547),
           (2315, 1524, 2414, 1461), (2441, 1437, 2531, 1369)],
 "mean":  [(660, 2443, 860, 2335), (840, 2346, 1100, 2209), (1080, 2219, 1360, 2079), (1340, 2089, 1620, 1958),
           (1600, 1966, 1880, 1858), (1860, 1865, 2140, 1759), (2120, 1766, 2400, 1652), (2380, 1660, 2546, 1582)],
 "lower": [(653, 2523, 753, 2477), (821, 2445, 931, 2397), (975, 2378, 1115, 2319), (1163, 2298, 1349, 2222),
           (1390, 2204, 1508, 2157), (1531, 2148, 1655, 2101), (1678, 2093, 1803, 2046), (1849, 2029, 1980, 1985),
           (2040, 1963, 2161, 1925), (2215, 1909, 2321, 1880), (2358, 1872, 2482, 1850)],
}
out = {}
for name, dl in DASHES.items():
    out[name] = []
    for (ua, va, ub, vb) in dl:
        poly = np.polyfit([ua, ub], [va, vb], 1)
        for it in range(3):
            pts = []
            for u in range(ua, ub + 1):
                p = float(np.polyval(poly, u))
                if zone(u, p): continue
                r = run_at(u, p)
                if r is None or r[1] > 13: continue
                pts.append((u, r[0], r[1]))
            P = np.array(pts)
            deg = 2 if ub - ua > 60 and len(P) > 30 else 1
            poly = np.polyfit(P[:, 0], P[:, 1], deg)
            res = P[:, 1] - np.polyval(poly, P[:, 0])
            keep = np.abs(res) <= 2.5
            poly = np.polyfit(P[keep, 0], P[keep, 1], deg)
        P = P[keep]
        out[name].append({"u0": ua, "u1": ub, "pts": P.tolist()})
        rms = float(np.sqrt(np.mean((P[:, 1] - np.polyval(poly, P[:, 0])) ** 2)))
        print(f"{name} {ua}..{ub}: {len(P)} columns measured, first {P[0,0]:.0f} last {P[-1,0]:.0f}, "
              f"rms about quadratic {rms:.2f} px, vthick med {np.median(P[:,2]):.0f}, rejected {int((~keep).sum())}")
json.dump(out, open("out/FC-16/measured.json", "w"))
