"""Where the three FA-2 curves run together (the top end along the 100 percent frame, the shallow
stretch u 745..1160, the fine end along the 0 percent frame), the strokes cannot be told apart, but
their order can: at a given grain size the upper curve has the highest percent finer (left on the
page), the lower curve the lowest (right). So:

    upper   = the band's outer edge on the high-percent side + half the stroke's extent,
    lower   = the band's outer edge on the low-percent side  - half the stroke's extent,
    average = midway (it is hidden somewhere between the two),

with the edges taken as envelopes over +-W scan lines (a dash gap must not pull an edge inward), and
only from ink edges that are not on a printed grid line. Bounds are widened accordingly (see
`bounds`). This is a reading aid: every value is checked on the page before it is used.

Row mode: page rows v, edges in u (left = high percent). Column mode: columns u, edges in v
(top = low percent side, the lower curve; bottom = the upper curve).
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import track as TR  # noqa: E402
import band as B  # noqa: E402

THICK = TR.THICK
W = 10


def edges(mode, t0, t1, lo, hi, seeds, gap=2):
    rows = []
    for t in range(t0, t1 + 1):
        c, s = TR.interp_seeds(seeds, t, "v" if mode == "row" else "u")
        line = TR.DARK[t, :] if mode == "row" else TR.DARK[:, t]
        grid = TR.grid_cols_at(t) if mode == "row" else TR.grid_rows_at(t)
        r = B.band_at(line, lo, hi, c, grid, gap=gap)
        rows.append((t, c, s, r))
    return rows


def envelopes(rows, t):
    """(lo_env, hi_env, n_lo, n_hi) at scan line t, edges shifted along the local slope."""
    _, c, s, _ = rows[[x[0] for x in rows].index(t)]
    los, his = [], []
    for tt, cc, ss, r in rows:
        if abs(tt - t) > W or r is None:
            continue
        a, b, ha, hb = r
        if b - a > 80:   # a grid line along the scan, not the band
            continue
        if not ha:
            los.append(a - s * (tt - t))
        if not hb:
            his.append(b - s * (tt - t))
    return (min(los) if los else None, max(his) if his else None, len(los), len(his))


def strands(rows, t):
    """centres (high-percent strand, middle, low-percent strand) on scan line t, with the stroke's
    half extent h2 along the scan line; None where an edge is hidden over the whole window."""
    _, c, s, _ = rows[[x[0] for x in rows].index(t)]
    h2 = THICK * np.sqrt(1 + s * s) / 2
    lo, hi, nlo, nhi = envelopes(rows, t)
    return lo, hi, h2, nlo, nhi


if __name__ == "__main__":
    mode = sys.argv[1]
    t0, t1, lo, hi = (int(x) for x in sys.argv[2:6])
    seeds = json.loads(Path(sys.argv[6]).read_text())
    step = int(sys.argv[7]) if len(sys.argv) > 7 else 5
    rows = edges(mode, t0, t1, lo, hi, seeds)
    for t in range(t0 + W, t1 - W + 1, step):
        a, b, h2, na, nb = strands(rows, t)
        print(f"{t}: env {a} .. {b}  (h/2 {h2:.1f}, edges {na}/{nb})")
