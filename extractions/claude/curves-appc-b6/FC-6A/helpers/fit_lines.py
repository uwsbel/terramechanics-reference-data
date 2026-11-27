"""Fit the three drawn lines of FC-6A (A top, M middle, B bottom at the right end) on their ink.

For each line, column runs whose center is within 5 px of the current line and whose thickness
is that of a single stroke (8 to 17 px) are taken as samples, but only where the other two lines
are at least 22 px away and away from grid lines and symbols (exclusion boxes); v = a + b u is
fitted by least squares and iterated. Prints the fits in pixels and in psf (calibration cal-p1),
and the residuals. Reader's aid; the outputs are the fitted lines used to place trace samples.
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
WS = HERE.parents[2]
g = np.asarray(Image.open(WS / "packet" / "p0131.png").convert("L"))
cal = json.loads((HERE.parent / "cal-p1" / "calibration.json").read_text())
ax, ay = cal["ax"], cal["ay"]
dark = g < 160

lines = {"A": [2923.5 + 0.99432 * 1020, -0.99432], "M": [2481.5 + 1.0101 * 1500, -1.0101],
         "B": [2499 + 0.9207 * 1500, -0.9207]}
# symbol exclusion boxes (u0, v0, u1, v1)
SYM = [(940, 2940, 1012, 3000), (1125, 2750, 1175, 2795), (1125, 2860, 1170, 2900),
       (1415, 2505, 1475, 2565), (1420, 2570, 1460, 2610), (1735, 2105, 1810, 2230),
       (1995, 1870, 2065, 1935), (2235, 1620, 2295, 1670), (2270, 1720, 2310, 1815)]
ranges = {"A": (1015, 2345), "M": (1190, 2252), "B": (1180, 2262)}


def runs_at(u, lo, hi):
    col = dark[lo:hi, u]
    idx = np.where(col)[0]
    out = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i != p + 1:
                out.append((lo + s, lo + p)); s = i
            p = i
        out.append((lo + s, lo + p))
    return out


def near_grid(u, v):
    for l in cal["horizontal_lines"]:
        if abs(v - (l["v_at_u0"] + l["slope_dv_du"] * u)) < 14:
            return True
    for l in cal["vertical_lines"]:
        if abs(u - (l["u_at_v0"] + l["slope_du_dv"] * v)) < 10:
            return True
    return False


for it in range(4):
    new = {}
    samples = {}
    for name, (a, b) in lines.items():
        pts = []
        for u in range(ranges[name][0], ranges[name][1] + 1):
            vp = a + b * u
            if near_grid(u, vp):
                continue
            if any(x0 <= u <= x1 and y0 - 8 <= vp <= y1 + 8 for x0, y0, x1, y1 in SYM):
                continue
            others = [lines[o][0] + lines[o][1] * u for o in lines if o != name]
            if min(abs(vp - o) for o in others) < 22:
                continue
            for s, p in runs_at(u, int(vp) - 15, int(vp) + 16):
                c = (s + p) / 2
                if abs(c - vp) <= 5 and 8 <= p - s + 1 <= 17:
                    pts.append((u, c, p - s + 1))
        pts = np.array(pts, float)
        bb, aa = np.polyfit(pts[:, 0], pts[:, 1], 1)
        new[name] = [aa, bb]
        samples[name] = pts
    lines = new
for name, (a, b) in lines.items():
    pts = samples[name]
    res = pts[:, 1] - (a + b * pts[:, 0])
    # in psf: two points on the line
    u1, u2 = ranges[name]
    def val(u, v):
        return ax[0]*u + ax[1]*v + ax[2], ay[0]*u + ay[1]*v + ay[2]
    x1, y1 = val(u1, a + b*u1); x2, y2 = val(u2, a + b*u2)
    slope = (y2 - y1) / (x2 - x1)
    icpt = y1 - slope * x1
    print(f"{name}: v = {a:.2f} + ({b:.5f}) u ; n={len(pts)} rms {np.sqrt((res**2).mean()):.2f} px max {abs(res).max():.2f}; "
          f"median thickness {np.median(pts[:,2]):.0f} px; tau = {icpt:.1f} + {slope:.5f} sigma (phi {np.degrees(np.arctan(slope)):.2f} deg)")
json.dump({k: v for k, v in lines.items()}, open(HERE / "fit_lines.json", "w"), indent=1)
