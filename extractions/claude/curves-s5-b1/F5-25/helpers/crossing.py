"""Where a trace's center line crosses a load grid line (a 5 lb sample at a grid value): the trace's
center is read along lines of constant time every 0.0001 s with overlap.row_union (the grid line inside
the trace's run is taken with it), and the crossing is interpolated where the center's load passes the
grid value."""
import sys
import numpy as np
from trace_tools import Panel
from overlap import row_union

n, y0, t1, t2, u_guess, w = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
P = Panel(n)
prev = None
ug = u_guess
for t in np.arange(t1, t2 + 1e-9, 0.0001):
    r = row_union(P, t, ug, w)
    if r is None:
        continue
    ug = r["u"]
    x, y = P.xy(r["u"], r["v"])
    if prev and (prev[1] - y0) * (y - y0) <= 0:
        f = (y0 - prev[1]) / (y - prev[1])
        u = prev[2] + f * (r["u"] - prev[2]); v = prev[3] + f * (r["v"] - prev[3])
        X, Y = P.xy(u, v)
        print(f"panel {n} y={y0}: between t={prev[0]:.4f} ({prev[1]:.2f}, {prev[4]}) and {x:.4f} ({y:.2f}, {r['how']}, run {r['len']}): u={u:.2f} v={v:.2f} x={X:.5f} y={Y:.2f}")
        break
    prev = (x, y, r["u"], r["v"], f"{r['how']}, run {r['len']}")
