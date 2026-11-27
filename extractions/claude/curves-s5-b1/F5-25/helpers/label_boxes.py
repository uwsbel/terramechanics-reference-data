"""Bounding boxes of the printed axis labels (groups of ink) of Figure 5-25, to check each label by eye
against the line it names: load labels below the baseline, time labels right of the right frame."""
import sys
import numpy as np
from PIL import Image
dark = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128


def groups(mask, axis, gap):
    prof = mask.any(axis=axis)
    idx = np.where(prof)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i - p > gap:
            out.append((s, p)); s = i
        p = i
    out.append((s, p))
    return out


# load labels: v 3540..3615 (below the baseline), grouped along u
v0, v1 = 3540, 3615
sub = dark[v0:v1, 940:2300]
for a, b in groups(sub, 0, 12):
    rows = np.where(sub[:, a:b + 1].any(axis=1))[0]
    print(f"load label u {940 + a}..{940 + b} center {940 + (a + b) / 2:.1f}  v {v0 + rows.min()}..{v0 + rows.max()}")
# time labels: u 2290..2335, grouped along v
u0, u1 = 2290, 2335
sub = dark[1780:3560, u0:u1]
for a, b in groups(sub, 1, 14):
    cols = np.where(sub[a:b + 1, :].any(axis=0))[0]
    print(f"time label v {1780 + a}..{1780 + b} center {1780 + (a + b) / 2:.1f}  u {u0 + cols.min()}..{u0 + cols.max()}")
