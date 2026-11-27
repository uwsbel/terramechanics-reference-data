"""Where a drawn segment's ink merges into a symbol's ring: walk along the fitted centreline towards the
symbol, 0.5 px steps, measuring the ink run across the line (no averaging along it); the line's ink end
is the last position whose run is no wider than the line's median thickness + 3 px and lies within
2 px of the centreline (three failing positions in a row end the walk; the run is averaged over 3 px along the line). Prints the profile so the merge can be seen."""
import json, sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L"), dtype=float)
S = json.load(open(sys.argv[2]))

def bil(u, v):
    u0, v0 = int(np.floor(u)), int(np.floor(v)); fu, fv = u - u0, v - v0
    return g[v0, u0]*(1-fu)*(1-fv) + g[v0, u0+1]*fu*(1-fv) + g[v0+1, u0]*(1-fu)*fv + g[v0+1, u0+1]*fu*fv

def run_at(p, n, half=16):
    s = np.arange(-half, half + 0.001, 0.25)
    e_ = np.array([n[1], -n[0]])
    d = np.array([np.mean([bil(*(p + si*n + ti*e_)) for ti in (-1, 0, 1)]) for si in s]) < 128
    if not d[len(s)//2 - 2: len(s)//2 + 3].any():
        return None
    i = len(s)//2
    # grow from the centre (or nearest dark) to the run edges
    idx = np.where(d)[0]; c = idx[np.argmin(abs(idx - i))]
    a = b = c
    while a > 0 and d[a-1]: a -= 1
    while b < len(s)-1 and d[b+1]: b += 1
    return s[a], s[b]

def walk(name, start, towards_t_sign, thick, maxlen=80):
    p = np.array(S[name]["point"]); e = np.array(S[name]["dir"]); n = np.array([-e[1], e[0]])
    t0 = (np.array(start) - p) @ e
    last_ok = None; out = []
    for k in range(int(maxlen / 0.5)):
        t = t0 + towards_t_sign * 0.5 * k
        q = p + t*e
        r = run_at(q, n)
        if r is None:
            out.append((t, None)); break
        a, b = r; w = b - a + 0.25; c = (a + b)/2
        out.append((t, round(w, 2), round(c, 2)))
        if w <= thick + 3.0 and abs(c) <= 2.0:
            last_ok = (t, q + c*n, w); bad = 0
        else:
            bad = locals().get("bad", 0) + 1
            if bad >= 3:
                break
    return last_ok, out

thick = {"dense_S1": 8.2, "dense_S2": 9.6, "loose_S1": 9.0, "loose_S2": 9.1}
cases = [("dense_S1 left end (2.3 lower circle)", "dense_S1", (930, 2900), -1),
         ("dense_S1 right end (4.9 pair)", "dense_S1", (1200, 2120), +1),
         ("dense_S2 left end (4.9 pair)", "dense_S2", (1300, 1900), -1),
         ("dense_S2 right end (9.9 lower circle)", "dense_S2", (1880, 1000), +1),
         ("loose_S1 left end (lowest circle C)", "loose_S1", (1100, 3818), -1),
         ("loose_S1 above A/B: first clean ink", "loose_S1", (1150, 3720), -1),
         ("loose_S1 right end (6 psi circle)", "loose_S1", (1340, 3340), +1),
         ("loose_S2 left end (6 psi circle)", "loose_S2", (1460, 3170), -1)]
for label, name, start, sgn in cases:
    ok, prof = walk(name, start, sgn, thick[name], maxlen=120)
    print(label, "->", None if ok is None else (round(ok[1][0], 1), round(ok[1][1], 1), round(ok[2], 1)), "| stop at", prof[-1])
