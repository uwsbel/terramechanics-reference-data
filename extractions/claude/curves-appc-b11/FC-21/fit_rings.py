# Sub-pixel centers of open circles by matching a ring template (ink for rin<=r<=rout, white for r<rin-1),
# one circle or two overlapping ones. Pixels of a column band (a grid line) can be masked out.
import sys, itertools
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
RIN, ROUT = 12.0, 18.5
def cost(centers, u0, v0, u1, v1, mask_cols=()):
    vv, uu = np.mgrid[v0:v1, u0:u1].astype(float)
    ring = np.zeros_like(uu, bool); hole_any = np.zeros_like(uu, bool)
    for (cu, cv) in centers:
        r = np.hypot(uu - cu, vv - cv)
        ring |= (r >= RIN) & (r <= ROUT)
        hole_any |= r < RIN - 1
    white_pred = hole_any & ~ring
    O = g[v0:v1, u0:u1]
    keep = np.ones_like(O, bool)
    for a, b in mask_cols:
        keep &= ~((uu >= a + (vv - 2030) * 0.0234) & (uu <= b + (vv - 2030) * 0.0234))
    miss = (ring & ~O & keep).sum(); extra = (white_pred & O & keep).sum()
    return miss + extra, miss, extra
mode = sys.argv[2]
if mode == "one":
    cu, cv = float(sys.argv[3]), float(sys.argv[4])
    best = min(((cost([(cu + du, cv + dv)], int(cu) - 25, int(cv) - 25, int(cu) + 26, int(cv) + 26)[0], cu + du, cv + dv)
                for du in np.arange(-3, 3.01, 0.25) for dv in np.arange(-3, 3.01, 0.25)))
    print("one", best)
else:
    # two circles near (1359, 2025) and (1359, 2035); grid line x=0.4 masked
    res = []
    for ua, va, ub, vb in itertools.product(np.arange(1356, 1362.1, 0.5), np.arange(2022, 2028.1, 0.5),
                                            np.arange(1356, 1362.1, 0.5), np.arange(2032, 2039.1, 0.5)):
        c = cost([(ua, va), (ub, vb)], 1330, 2000, 1390, 2060, mask_cols=[(1357.5, 1364.5)])
        res.append((c[0], ua, va, ub, vb, c[1], c[2]))
    res.sort()
    for r in res[:12]:
        print(r)
