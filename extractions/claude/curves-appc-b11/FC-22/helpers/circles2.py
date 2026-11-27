"""Circle centres, robust: rays from a seed; inner edge kept unless it lies on the y=45 grid line band;
outer edge kept only where the ring is 5..10 px thick (not merged with a line)."""
import sys, json
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L"), dtype=float)
cal = json.load(open(sys.argv[2]))
hl = [(l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
def fit(P):
    P = np.array(P); A = np.c_[2 * P[:, 0], 2 * P[:, 1], np.ones(len(P))]
    b = (P ** 2).sum(1); c, *_ = np.linalg.lstsq(A, b, rcond=None)
    r = np.sqrt(c[2] + c[0] ** 2 + c[1] ** 2); res = np.hypot(P[:, 0] - c[0], P[:, 1] - c[1]) - r
    return c[0], c[1], r, np.sqrt(np.mean(res ** 2))
def sample(u, v):
    u0, v0 = int(u), int(v); fu, fv = u - u0, v - v0
    return (g[v0, u0] * (1 - fu) * (1 - fv) + g[v0, u0 + 1] * fu * (1 - fv) + g[v0 + 1, u0] * (1 - fu) * fv + g[v0 + 1, u0 + 1] * fu * fv)
def on_hline(p):
    return any(abs(p[1] - (i0 + s * p[0])) <= 5 for i0, s in hl)
for seeds in [[(1689.0, 2007.0), (1689.0, 2026.0)], [(2342.0, 1584.0)]]:
    inner, outer = [], []
    for seed in seeds:
        for ang in np.arange(0, 360, 3):
            d = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang))])
            ts = np.arange(0, 35, 0.25)
            prof = np.array([sample(*(np.array(seed) + t * d)) for t in ts])
            dk = prof < 128
            if not dk.any(): continue
            i0 = int(np.argmax(dk))
            p_in = np.array(seed) + ts[i0] * d
            if on_hline(p_in): continue
            rest = ~dk[i0:]
            if not rest.any(): continue
            i1 = i0 + int(np.argmax(rest))
            p_out = np.array(seed) + ts[i1] * d
            inner.append(p_in)
            if 5 <= ts[i1] - ts[i0] <= 10 and not on_hline(p_out):
                outer.append(p_out)
    for nm, P in (("inner", inner), ("outer", outer)):
        print(seeds[0], nm, "n", len(P), "fit u %.2f v %.2f r %.2f rms %.2f" % fit(P))
