"""Ink extents of the printed axis labels of FB-4 (projection of the label rows/columns), so each
label can be compared with the tick or frame line it names."""
import sys
import numpy as np
from PIL import Image

D = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128


def groups(prof, off, gap=10):
    idx = np.where(prof > 0)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i - p > gap:
            out.append((s + off, p + off))
            s = i
        p = i
    out.append((s + off, p + off))
    return out


# x labels: below the bottom frame (frame bottom edge ~3910 to 3923 across the width)
band = D[3925:3995, 540:2640]
print("x label glyph groups (u range, centre; v range):")
for a, b in groups(band.sum(axis=0), 540, gap=12):
    sub = D[3925:3995, a:b + 1]
    rows = np.where(sub.sum(axis=1) > 0)[0]
    print(f"  u {a}..{b}  centre {0.5 * (a + b):.1f}   v {3925 + rows.min()}..{3925 + rows.max()}  width {b - a + 1}")

# y labels: left of the left frame (frame at u ~592-611, labels ~ 500-585)
band = D[1060:3960, 500:585]
print("y label glyph groups (v range, centre; u range):")
for a, b in groups(band.sum(axis=1), 1060, gap=12):
    sub = D[a:b + 1, 500:585]
    cols = np.where(sub.sum(axis=0) > 0)[0]
    print(f"  v {a}..{b}  centre {0.5 * (a + b):.1f}   u {500 + cols.min()}..{500 + cols.max()}  height {b - a + 1}")
