"""Claude reader helper (FA-18): viewing image with the straight grid lines greyed (see gridmask.py).
A candidate line is kept only when its ink is present along most of its length (chunks outside the
table), so a curve stretch that happens to lie along a tilted projection is not masked. The two
frame lines and the labelled lines are taken from cal-p1 (measured), the rest from gridmask.find."""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import gridmask as gm  # noqa: E402

WS = HERE.parents[3]
dark = gm.dark
cal = json.loads((WS / "out/FA-18/cal-p1/calibration.json").read_text(encoding="utf-8"))
TABLE = (893, 2105, 1485, 3610)   # u0, v0, u1, v1 of the parameter table (white inside)


def in_table(u, v):
    return TABLE[0] <= u <= TABLE[2] and TABLE[1] <= v <= TABLE[3]


def presence(axis, c, k, w, nchunks=14):
    half = max(1.0, w / 2)
    if axis == "h":
        ts = np.linspace(gm.U0 + 5, gm.U1 - 5, nchunks * 40)
    else:
        ts = np.linspace(gm.V0 + 5, gm.V1 - 5, nchunks * 40)
    ok, tot = 0, 0
    for ch in np.array_split(ts, nchunks):
        hits, n = 0, 0
        for t in ch:
            if axis == "h":
                u, v = t, c + k * t
            else:
                u, v = c + k * t, t
            if in_table(u, v):
                continue
            n += 1
            ss = np.arange(-half, half + 0.1, 1.0)
            if axis == "h":
                vals = dark[np.round(v + ss).astype(int), int(round(u))]
            else:
                vals = dark[int(round(v)), np.round(u + ss).astype(int)]
            hits += vals.any()
        if n >= 10:
            tot += 1
            ok += hits / n >= 0.25
    return ok, tot


lines = []   # (axis, c, k, half-thickness)
for c, w, m in gm.find("h", -0.0190, 0.3):
    ok, tot = presence("h", c, -0.0190, w)
    if tot and ok >= 0.75 * tot:
        lines.append(("h", c, -0.0190, min(w / 2 + 1.5, 4.5)))
for c, w, m in gm.find("v", 0.0216, 0.3):
    if w > 20:
        continue   # the 0 percent frame merged with the curves: taken from cal-p1 below
    ok, tot = presence("v", c, 0.0216, w)
    if tot and ok >= 0.75 * tot:
        lines.append(("v", c, 0.0216, min(w / 2 + 1.5, 4.5)))
# measured labelled lines (better tilt) replace the projections near them
for l in cal["horizontal_lines"]:
    lines = [x for x in lines if not (x[0] == "h" and abs((x[1] + x[2] * 1300) - (l["v_at_u0"] + l["slope_dv_du"] * 1300)) < 6)]
    lines.append(("h", l["v_at_u0"], l["slope_dv_du"], 5.5))
for l in cal["vertical_lines"]:
    lines = [x for x in lines if not (x[0] == "v" and abs((x[1] + x[2] * 2400) - (l["u_at_v0"] + l["slope_du_dv"] * 2400)) < 6)]
    lines.append(("v", l["u_at_v0"], l["slope_du_dv"], 5.0))

H, Wd = dark.shape
vv, uu = np.mgrid[0:H, 0:Wd]
mask = np.zeros_like(dark)
for axis, c, k, half in lines:
    if axis == "h":
        mask |= np.abs(vv - (c + k * uu)) <= half
    else:
        mask |= np.abs(uu - (c + k * vv)) <= half
img = np.full((H, Wd, 3), 255, np.uint8)
img[dark & ~mask] = (0, 0, 0)
img[dark & mask] = (190, 190, 230)
Image.fromarray(img).save(WS / "out/FA-18/scratch/clean.png")
np.save(WS / "out/FA-18/scratch/mask.npy", mask & dark)
print(f"{sum(1 for l in lines if l[0]=='h')} horizontal and {sum(1 for l in lines if l[0]=='v')} vertical lines masked")
for l in lines:
    if l[0] == "h":
        print(f"  h v@1000={l[1] + l[2]*1000:7.1f} half {l[3]:.1f}")
