"""Model fit of overlapping open circles on FB-4: the ink of a region is compared with the union of
N rings (inner radius r_in, outer radius r_out, 4x4 supersampled coverage) whose centres are free;
pixels near a drawn line are left out of the comparison (the line is not part of the model).
Pattern search on the summed squared difference. First calibrates r_in, r_out on the isolated
circles (centre and radii free), then fits each cluster with the radii fixed, and reports how
much the centres move when the radii change by +-0.5 px and the line corridor by +-2 px."""
import json
import sys
import numpy as np
from PIL import Image

D = (np.asarray(Image.open(sys.argv[1]).convert("L")) < 128).astype(float)
SEG = json.load(open(sys.argv[2]))
SS = 4
off = (np.arange(SS) + 0.5) / SS - 0.5


def seg_dist(name, U, V):
    s = SEG[name]
    if s["steep"]:   # u = c0 + k v
        return np.abs(U - (s["c0"] + s["k"] * V)) / np.sqrt(1 + s["k"] ** 2)
    return np.abs(V - (s["c0"] + s["k"] * U)) / np.sqrt(1 + s["k"] ** 2)


def model(box, centres, r_in, r_out):
    u0, v0, u1, v1 = box
    uu = np.arange(u0, u1)[None, :, None, None] + off[None, None, None, :]
    vv = np.arange(v0, v1)[:, None, None, None] + off[None, None, :, None]
    cov = np.zeros((v1 - v0, u1 - u0, SS, SS), bool)
    for cu, cv in centres:
        d = np.sqrt((uu - cu) ** 2 + (vv - cv) ** 2)
        cov |= (d >= r_in) & (d <= r_out)
    return cov.mean(axis=(2, 3))


def cost(box, mask, centres, r_in, r_out):
    u0, v0, u1, v1 = box
    O = D[v0:v1, u0:u1]
    M = model(box, centres, r_in, r_out)
    return float(((O - M) ** 2)[mask].sum())


def make_mask(box, lines, extra):
    u0, v0, u1, v1 = box
    U, V = np.meshgrid(np.arange(u0, u1), np.arange(v0, v1))
    m = np.ones(U.shape, bool)
    for name in lines:
        hw = SEG[name]["thickness"] / 2
        m &= seg_dist(name, U, V) > hw + extra
    return m


def search(box, mask, params, free, step=1.0, min_step=0.125):
    """params: flat list; free: indices to vary. Pattern search."""
    def f(p):
        cs = [(p[i], p[i + 1]) for i in range(0, len(p) - 2, 2)]
        return cost(box, mask, cs, p[-2], p[-1])
    p = list(params)
    best = f(p)
    while step >= min_step:
        improved = False
        for i in free:
            for d in (step, -step):
                q = list(p)
                q[i] += d
                c = f(q)
                if c < best - 1e-9:
                    best, p, improved = c, q, True
        if not improved:
            step /= 2
    return p, best


# 1. radii from the isolated circles
iso = [(770.5, 3210.2, ["dr22_s1"]), (1284.5, 1833.1, []), (1294.9, 2475.6, []), (1300.0, 2154.8, []),
       (1947.1, 1841.6, []), (1948.4, 2061.9, [])]
rin_l, rout_l = [], []
print("isolated circles (centre, r_in, r_out, cost):")
for cu, cv, lines in iso:
    box = (int(cu) - 28, int(cv) - 28, int(cu) + 29, int(cv) + 29)
    mask = make_mask(box, lines, 2.0)
    p, c = search(box, mask, [cu, cv, 12.75, 20.9], [0, 1, 2, 3])
    rin_l.append(p[2]); rout_l.append(p[3])
    print(f"  ({p[0]:.2f}, {p[1]:.2f})  r_in {p[2]:.2f}  r_out {p[3]:.2f}  cost {c:.1f}")
R_IN, R_OUT = float(np.median(rin_l)), float(np.median(rout_l))
print(f"radii used: r_in {R_IN:.2f}, r_out {R_OUT:.2f}")

# 2. clusters: (name, box, initial centres, fixed extra circles, line corridors)
CL = [
    ("A dense x~2.5", (905, 2490, 1000, 2610), [(942.5, 2525), (942.5, 2540)], [(957.4, 2579.2)], ["dr86_s1"]),
    ("A' dense x~2.5 (lower circle free too)", (905, 2490, 1000, 2610), [(942.5, 2525), (942.5, 2540), (957.4, 2579.2)], [], ["dr86_s1"]),
    ("B loose x~2.5", (905, 2720, 1000, 2830), [(953.5, 2756), (944, 2777), (944, 2793)], [], ["dr22_s1", "dr22_s2"]),
    ("B2 loose x~2.5, two circles only", (905, 2720, 1000, 2830), [(953.5, 2756), (944, 2785)], [], ["dr22_s1", "dr22_s2"]),
    ("C dense x~10", (1940, 1295, 2010, 1380), [(1974, 1330), (1974, 1344)], [], ["dr86_s2"]),
    ("C1 dense x~10, one circle only", (1940, 1295, 2010, 1380), [(1974, 1337)], [], ["dr86_s2"]),
]
result = {"r_in": R_IN, "r_out": R_OUT, "clusters": {}}
for name, box, init, fixed, lines in CL:
    n = len(init)
    sols = []
    for dr in (0.0, -0.5, 0.5):
        for ex in (2.0, 0.0, 4.0):
            if dr != 0 and ex != 2.0:
                continue
            mask = make_mask(box, lines, ex)
            flat = [c for xy in init for c in xy]

            def full(p):
                return p
            # fixed circles are added as extra centres that never move
            fflat = flat + [c for xy in fixed for c in xy]
            p, c = search(box, mask, fflat + [R_IN + dr, R_OUT + dr], list(range(2 * n)))
            sols.append(((dr, ex), [(p[2 * i], p[2 * i + 1]) for i in range(n)], c, int(mask.sum())))
    base = sols[0]
    print(f"\n{name}: base cost {base[2]:.1f} on {base[3]} px")
    spread = []
    for i in range(n):
        us = [s[1][i][0] for s in sols]
        vs = [s[1][i][1] for s in sols]
        spread.append((max(us) - min(us), max(vs) - min(vs)))
        print(f"  circle {i + 1}: ({base[1][i][0]:.2f}, {base[1][i][1]:.2f})   range over variants u {min(us):.2f}..{max(us):.2f}, v {min(vs):.2f}..{max(vs):.2f}")
    for s in sols[1:]:
        print(f"    variant dr {s[0][0]:+.1f} corridor +{s[0][1]:.0f}: cost {s[2]:.1f}  " + "  ".join(f"({a:.2f}, {b:.2f})" for a, b in s[1]))
    result["clusters"][name] = {"centres": base[1], "cost": base[2], "n_px": base[3], "spread": spread}
json.dump(result, open(sys.argv[3], "w"), indent=1)
