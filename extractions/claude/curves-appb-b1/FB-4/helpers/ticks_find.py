"""Find tick candidates along each frame line of FB-4: stretches where ink sticks out of the
frame on either side (inside or outside), using the frame fits of frame.py."""
import sys
import numpy as np
from PIL import Image

D = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
bot = (3898.86, 0.007517); top = (1098.35, 0.008428)
lef = (617.42, -0.006622); rig = (2571.95, -0.004877)


def groups(ts, cnt, thr):
    out, cur = [], []
    for t, c in zip(ts, cnt):
        if c >= thr:
            cur.append((t, c))
        elif cur:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def scan_h(line, side, label, t0, t1, d0=8, d1=24):
    ts = np.arange(t0, t1)
    cnt = []
    for u in ts:
        c = line[0] + line[1] * u
        if side < 0:
            seg = D[int(round(c - d1)):int(round(c - d0)), u]
        else:
            seg = D[int(round(c + d0)):int(round(c + d1)), u]
        cnt.append(seg.sum())
    for g in groups(ts, cnt, 6):
        us = [t for t, _ in g]
        print(f"  {label}: u {us[0]}..{us[-1]} (w {len(us)}), max count {max(c for _, c in g)}")


def scan_v(line, side, label, t0, t1, d0=7, d1=24):
    ts = np.arange(t0, t1)
    cnt = []
    for v in ts:
        c = line[0] + line[1] * v
        if side < 0:
            seg = D[v, int(round(c - d1)):int(round(c - d0))]
        else:
            seg = D[v, int(round(c + d0)):int(round(c + d1))]
        cnt.append(seg.sum())
    for g in groups(ts, cnt, 6):
        vs = [t for t, _ in g]
        print(f"  {label}: v {vs[0]}..{vs[-1]} (w {len(vs)}), max count {max(c for _, c in g)}")


print("bottom frame, inside (above):"); scan_h(bot, -1, "bottom-in", 610, 2560)
print("bottom frame, outside (below):"); scan_h(bot, +1, "bottom-out", 610, 2560)
print("top frame, inside (below):"); scan_h(top, +1, "top-in", 620, 2560)
print("top frame, outside (above):"); scan_h(top, -1, "top-out", 620, 2560)
print("left frame, inside (right):"); scan_v(lef, +1, "left-in", 1110, 3900)
print("left frame, outside (left):"); scan_v(lef, -1, "left-out", 1110, 3900)
print("right frame, inside (left):"); scan_v(rig, -1, "right-in", 1120, 3905)
print("right frame, outside (right):"); scan_v(rig, +1, "right-out", 1120, 3905)
