"""Edges of the merged band where the three FA-2 curves run together (reading aid).

Row mode (top end near the 100 percent frame, fine end along the 0 percent frame): for each page row
v, the band's left and right ink edges; column mode (the shallow stretch u 700..1160): for each
column, the band's top and bottom edges. An edge lying on a printed grid line (frame included) is
flagged hidden: the ink of the curve cannot be told from the grid there.

    python band.py row v0 v1 umin umax centre_seeds.json   -> prints v, left, right, flags
    python band.py col u0 u1 vmin vmax centre_seeds.json
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import track as TR  # noqa: E402

DARK = TR.DARK


def band_at(line, lo, hi, centre, grid, gap=3):
    """the band: runs in [lo, hi] joined across gaps of up to `gap` px, the joined group nearest `centre`.
    Returns (start, end, start_hidden, end_hidden) or None."""
    runs = TR.runs_1d(line[lo:hi + 1], lo)
    if not runs:
        return None
    groups = [[runs[0][0], runs[0][1]]]
    for a, b in runs[1:]:
        if a - groups[-1][1] - 1 <= gap:
            groups[-1][1] = b
        else:
            groups.append([a, b])
    g = min(groups, key=lambda g: 0 if g[0] <= centre <= g[1] else min(abs(g[0] - centre), abs(g[1] - centre)))
    if not (g[0] - 15 <= centre <= g[1] + 15):
        return None
    a, b = g
    return a, b, TR.on_grid(a, grid), TR.on_grid(b, grid)


def scan(mode, t0, t1, lo, hi, seeds):
    out = []
    for t in range(t0, t1 + 1):
        c, _ = TR.interp_seeds(seeds, t, "v" if mode == "row" else "u")
        line = DARK[t, :] if mode == "row" else DARK[:, t]
        grid = TR.grid_cols_at(t) if mode == "row" else TR.grid_rows_at(t)
        r = band_at(line, lo, hi, c, grid)
        out.append((t, c, r))
    return out


if __name__ == "__main__":
    mode = sys.argv[1]
    t0, t1, lo, hi = (int(x) for x in sys.argv[2:6])
    seeds = json.loads(Path(sys.argv[6]).read_text())
    for t, c, r in scan(mode, t0, t1, lo, hi, seeds):
        if r is None:
            print(f"{t}: centre {c:.0f}  none")
        else:
            a, b, ha, hb = r
            print(f"{t}: centre {c:.0f}  {a}{'(h)' if ha else ''} - {b}{'(h)' if hb else ''}  width {b - a + 1}")
