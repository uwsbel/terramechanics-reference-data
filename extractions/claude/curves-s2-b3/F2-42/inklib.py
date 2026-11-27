"""Small helpers to read the center of a drawn line on the binary page image of Fig. 2-42."""
from pathlib import Path
import numpy as np
from PIL import Image
HERE = Path(__file__).resolve().parent
G = np.asarray(Image.open(HERE.parents[1] / "packet" / "p0102.png").convert("L")) < 128

def runs_1d(arr, off):
    out, s = [], None
    for i, d in enumerate(arr):
        if d and s is None: s = i
        if not d and s is not None: out.append((s + off, i - 1 + off)); s = None
    if s is not None: out.append((s + off, len(arr) - 1 + off))
    return out

def row_runs(v, lo, hi): return runs_1d(G[v, lo:hi + 1], lo)
def col_runs(u, lo, hi): return runs_1d(G[lo:hi + 1, u], lo)

def nearest(runs, guess):
    best = None
    for a, b in runs:
        d = 0 if a <= guess <= b else min(abs(a - guess), abs(b - guess))
        if best is None or d < best[0]: best = (d, a, b)
    return best[1:] if best else None

def row_center(v, guess, win=12):
    r = nearest(row_runs(v, int(guess - win), int(guess + win)), guess)
    return None if r is None else ((r[0] + r[1]) / 2, r[1] - r[0] + 1, r)

def col_center(u, guess, win=12):
    r = nearest(col_runs(u, int(guess - win), int(guess + win)), guess)
    return None if r is None else ((r[0] + r[1]) / 2, r[1] - r[0] + 1, r)

def find_row_crossing(u_target, v_lo, v_hi, guess_u, win=10):
    """Rows v in [v_lo, v_hi] whose run nearest guess_u has its center closest to u_target."""
    best = None
    for v in range(v_lo, v_hi + 1):
        rc = row_center(v, guess_u, win)
        if rc is None: continue
        d = abs(rc[0] - u_target)
        if best is None or d < best[0]: best = (d, v, rc)
    return best
