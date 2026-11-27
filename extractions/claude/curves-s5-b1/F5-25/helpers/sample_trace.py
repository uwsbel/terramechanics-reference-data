"""Locate the trace of one panel of Figure 5-25 on the page ink at the sampling times and, on steep
stretches, at every 5 lb. A sample is the midpoint of the trace's chord along the line of constant
time (or of constant load), which for a locally straight band of ink lies on its center line. Thin
horizontal time-line dashes are removed first (vertical opening, 5 px; the trace is 6 to 8 px thick);
a chord ending inside a vertical grid line's band is flagged. Prints a table; writes raw JSON."""
import json
import sys
import numpy as np
from trace_tools import Panel, THICK, DARK, vline_band

n = int(sys.argv[1])
out = sys.argv[2]
P = Panel(n)
U0, U1 = P.urange
TIMES = [round(0.002 * k, 3) for k in range(1, 11)] + [round(0.02 + 0.005 * k, 3) for k in range(1, 17)]


def row_runs(t, mask=THICK):
    """Runs of ink along the line of constant time t inside the panel's u range."""
    us = np.arange(U0, U1 + 1)
    va, vb = P.v_at_t(U0, t), P.v_at_t(U1, t)
    vs = va + (vb - va) * (us - U0) / (U1 - U0)
    on = np.array([mask[int(round(v)), u] for u, v in zip(us, vs)])
    band = np.array([vline_band(u, v) for u, v in zip(us, vs)])
    runs, s = [], None
    for i, f in enumerate(list(on) + [False]):
        if f and s is None:
            s = i
        if not f and s is not None:
            a, b = s, i - 1
            free = (~band[a:b + 1]).sum()
            if free >= 3:
                amb = bool(band[a] or band[b])
                runs.append({"a": int(us[a]), "b": int(us[b]), "u": (us[a] + us[b]) / 2, "len": b - a + 1,
                             "amb": amb})
            s = None
    for r in runs:
        r["v"] = va + (vb - va) * (r["u"] - U0) / (U1 - U0)
    return runs


def col_runs(y, v_lo, v_hi, du=0.0, mask=THICK):
    """Runs of ink along the line of constant load y (shifted du px across it), v in [v_lo, v_hi]."""
    vs = np.arange(int(v_lo), int(v_hi) + 1)
    ua, ub = P.u_at_y(v_lo, y) + du, P.u_at_y(v_hi, y) + du
    us = ua + (ub - ua) * (vs - v_lo) / max(1, (v_hi - v_lo))
    on = np.array([mask[v, int(round(u))] for u, v in zip(us, vs)])
    runs, s = [], None
    for i, f in enumerate(list(on) + [False]):
        if f and s is None:
            s = i
        if not f and s is not None:
            a, b = s, i - 1
            if b - a + 1 >= 3:
                vm = (vs[a] + vs[b]) / 2
                runs.append({"a": int(vs[a]), "b": int(vs[b]), "v": vm, "len": b - a + 1,
                             "u": ua + (ub - ua) * (vm - v_lo) / max(1, (v_hi - v_lo))})
            s = None
    return runs


def chord_v(u, v):
    """Vertical chord of the trace through (u, v), in THICK, avoiding grid bands (shift 5 px if needed)."""
    for du in (0, 5, -5, 8, -8):
        uu = int(round(u + du))
        if vline_band(uu, v):
            continue
        vi = int(round(v))
        if not THICK[vi, uu]:
            continue
        a = vi
        while THICK[a - 1, uu]:
            a -= 1
        b = vi
        while THICK[b + 1, uu]:
            b += 1
        return b - a + 1
    return None


samples = []
prev_u = None
for t in TIMES:
    runs = row_runs(t)
    if not runs:
        print(f"t={t:.3f}: no ink"); continue
    if prev_u is None:
        r = max(runs, key=lambda r: r["len"]) if len(runs) > 1 else runs[0]
    else:
        r = min(runs, key=lambda r: abs(r["u"] - prev_u))
    prev_u = r["u"]
    others = [(q["a"], q["b"]) for q in runs if q is not r]
    lv = chord_v(r["u"], r["v"])
    lu = r["len"]
    w = lu * lv / np.hypot(lu, lv) if lv else None
    x, y = P.xy(r["u"], r["v"])
    samples.append({"kind": "t", "target": t, "u": float(r["u"]), "v": float(r["v"]), "lu": lu, "lv": lv, "w": w,
                    "amb": r["amb"], "x": x, "y": y, "others": others})
    print(f"t={t:.3f}  u={r['u']:7.1f} v={r['v']:7.1f}  chord {r['a']}..{r['b']} ({lu})  lv={lv}  w={w if w is None else round(w, 1)}  "
          f"x={x:.4f} y={y:7.2f} {'AMB' if r['amb'] else ''} others={others}")
json.dump({"panel": n, "samples": samples}, open(out, "w", encoding="utf-8"), indent=1)
