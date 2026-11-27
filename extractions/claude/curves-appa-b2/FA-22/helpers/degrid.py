"""A viewing aid only (no value is read from it): the page with long horizontal and vertical runs of
ink (grid lines) shown light grey, the remaining ink black, so the curves and symbols stand out.
Usage: python degrid.py <page.png> <out.png> [L]"""
import sys
import numpy as np
from PIL import Image

def win_all(b, L, axis):
    """True where all L consecutive pixels centred on the pixel along `axis` are dark (erosion)."""
    c = np.cumsum(np.pad(b.astype(np.int32), [(1, 0) if a == axis else (0, 0) for a in range(2)]), axis=axis)
    n = b.shape[axis]
    h = L // 2
    idx = np.arange(n)
    lo = np.clip(idx - h, 0, n); hi = np.clip(idx - h + L, 0, n)
    s = np.take(c, hi, axis=axis) - np.take(c, lo, axis=axis)
    return s == L

def win_any(b, L, axis):
    c = np.cumsum(np.pad(b.astype(np.int32), [(1, 0) if a == axis else (0, 0) for a in range(2)]), axis=axis)
    n = b.shape[axis]
    h = L // 2
    idx = np.arange(n)
    lo = np.clip(idx - (L - 1 - h), 0, n); hi = np.clip(idx + h + 1, 0, n)
    s = np.take(c, hi, axis=axis) - np.take(c, lo, axis=axis)
    return s > 0

g = np.asarray(Image.open(sys.argv[1]).convert("L"))
L = int(sys.argv[3]) if len(sys.argv) > 3 else 45
b = g < 128
hline = win_any(win_all(b, L, 1), L, 1)   # opening with a 1 x L horizontal segment
vline = win_any(win_all(b, L, 0), L, 0)
grid = (hline | vline) & b
rest = b & ~grid
out = np.full(g.shape, 255, np.uint8)
out[grid] = 200
out[rest] = 0
Image.fromarray(out).save(sys.argv[2])
print("grid px", int(grid.sum()), "rest px", int(rest.sum()))
