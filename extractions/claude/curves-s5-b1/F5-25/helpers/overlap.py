"""Samples where the trace overlaps a grid line (load line) or is broken, read from the union of ink.

Along the line of constant time t (or constant load y) near a guess (u, v), the ink run (with thin time
dashes removed) containing or nearest the guess is taken whole, grid line included. The trace's own
edges are told from the grid line's: when the run is no wider than the trace plus 2 px, its midpoint is
used (the grid line lies inside the trace); when wider and a grid line sits at one end, the center is
put half a trace width inside the other end. Prints the run, the grid lines it meets and the result."""
import sys
import numpy as np
from trace_tools import Panel, THICK, DARK, LINES


def gridlines_at(v):
    return [(L["value"], L["panel"], L["u_at_v0"] + L["slope_du_dv"] * v) for L in LINES["vertical"]]


def row_union(P, t, u_guess, w, mask=THICK, span=30):
    us = np.arange(int(u_guess) - span, int(u_guess) + span + 1)
    va, vb = P.v_at_t(us[0], t), P.v_at_t(us[-1], t)
    vs = va + (vb - va) * (us - us[0]) / (us[-1] - us[0])
    on = np.array([mask[int(round(v)), u] for u, v in zip(us, vs)])
    runs, s = [], None
    for i, f in enumerate(list(on) + [False]):
        if f and s is None:
            s = i
        if not f and s is not None:
            runs.append((us[s], us[i - 1])); s = None
    if not runs:
        return None
    a, b = min(runs, key=lambda r: 0 if r[0] <= u_guess <= r[1] else min(abs(r[0] - u_guess), abs(r[1] - u_guess)))
    vmid = va + (vb - va) * ((a + b) / 2 - us[0]) / (us[-1] - us[0])
    g = [x for x in gridlines_at(vmid) if a - 3 <= x[2] <= b + 3]
    L = b - a + 1
    if L <= w + 2 or not g:
        c, how = (a + b) / 2, "midpoint" + (" (grid line inside)" if g else "")
    else:
        gl = min(g, key=lambda x: min(abs(x[2] - a), abs(x[2] - b)))
        if abs(gl[2] - a) < abs(gl[2] - b):
            c, how = b - (w - 1) / 2, f"right edge - w/2 (grid {gl[0]:g} at left end)"
        else:
            c, how = a + (w - 1) / 2, f"left edge + w/2 (grid {gl[0]:g} at right end)"
    v = va + (vb - va) * (c - us[0]) / (us[-1] - us[0])
    return {"a": int(a), "b": int(b), "len": int(L), "u": float(c), "v": float(v), "how": how,
            "grid": [(x[0], round(x[2], 1)) for x in g]}


def col_union(P, y, v_guess, w, mask=THICK, span=30, du=0.0):
    vs = np.arange(int(v_guess) - span, int(v_guess) + span + 1)
    ua, ub = P.u_at_y(vs[0], y) + du, P.u_at_y(vs[-1], y) + du
    us = ua + (ub - ua) * (vs - vs[0]) / (vs[-1] - vs[0])
    on = np.array([mask[v, int(round(u))] for u, v in zip(us, vs)])
    runs, s = [], None
    for i, f in enumerate(list(on) + [False]):
        if f and s is None:
            s = i
        if not f and s is not None:
            runs.append((vs[s], vs[i - 1])); s = None
    if not runs:
        return None
    a, b = min(runs, key=lambda r: 0 if r[0] <= v_guess <= r[1] else min(abs(r[0] - v_guess), abs(r[1] - v_guess)))
    c = (a + b) / 2
    u = ua + (ub - ua) * (c - vs[0]) / (vs[-1] - vs[0])
    return {"a": int(a), "b": int(b), "len": int(b - a + 1), "u": float(u), "v": float(c), "how": "midpoint"}


if __name__ == "__main__":
    n, by, target, guess, w = int(sys.argv[1]), sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    P = Panel(n)
    r = row_union(P, target, guess, w) if by == "t" else col_union(P, target, guess, w)
    if r:
        x, y = P.xy(r["u"], r["v"])
        print(f"panel {n} {by}={target}: run {r['a']}..{r['b']} ({r['len']} px) {r['how']} grid {r.get('grid')} -> u={r['u']:.2f} v={r['v']:.2f} x={x:.5f} y={y:.2f}")
    else:
        print("no run")
