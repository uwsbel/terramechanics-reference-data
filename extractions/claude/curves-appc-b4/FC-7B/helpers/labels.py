"""Ink extents of the printed axis labels (load labels below the frame, motion labels right of it),
to compare by eye with the fitted grid-line positions."""
import json
import numpy as np
from PIL import Image
g = np.asarray(Image.open("packet/p0136.png").convert("L")) < 128
cal = json.load(open("out/FC-7B/cal-p1/calibration.json"))
def groups(mask_1d, off, gap=12):
    idx = np.nonzero(mask_1d)[0]
    out, s, p = [], None, None
    for i in idx:
        if s is None: s = p = i; continue
        if i - p > gap: out.append((s + off, p + off)); s = i
        p = i
    if s is not None: out.append((s + off, p + off))
    return out
# load labels: band v 3300..3400 under the frame
band = g[3300:3400, 560:2360]
print("load-axis label ink groups (u range, center) in v 3300..3400:")
for a, b in groups(band.any(axis=0), 560):
    sub = g[3300:3400, a:b + 1]
    vv = np.nonzero(sub.any(axis=1))[0]
    print(f"  u {a}..{b} center {(a+b)/2:.1f}   v {3300+vv.min()}..{3300+vv.max()}")
for ln in cal["vertical_lines"]:
    print(f"  fitted y={ln['y_value']:g} line at v 3290: u = {ln['u_at_v0'] + ln['slope_du_dv']*3290:.1f}")
band = g[1280:3330, 2335:2420]
print("motion-axis label ink groups (v range, center) in u 2335..2420:")
for a, b in groups(band.any(axis=1), 1280):
    sub = g[a:b + 1, 2335:2420]
    uu = np.nonzero(sub.any(axis=0))[0]
    print(f"  v {a}..{b} center {(a+b)/2:.1f}   u {2335+uu.min()}..{2335+uu.max()}")
for ln in cal["horizontal_lines"]:
    print(f"  fitted x={ln['x_value']:g} line at u 2310: v = {ln['v_at_u0'] + ln['slope_dv_du']*2310:.1f}")
