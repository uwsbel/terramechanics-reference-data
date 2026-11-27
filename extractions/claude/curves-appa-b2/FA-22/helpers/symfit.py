"""Locate a symbol centre near an eye estimate: the centre of the radius-r disk holding the most
non-grid ink (de-gridded mask), searched within +-s px; reports also the ink-weighted centroid in that
disk. A check of the eye reading, not a replacement for it."""
import sys
import numpy as np
from PIL import Image
import fa22lib as L
D = np.asarray(Image.open(L.OUT / "helpers" / "degrid.png"))
REST = (D == 0).astype(float)
INK = (D < 255).astype(float)
def best(u, v, r=12, s=10, M=REST):
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; disk = (xx ** 2 + yy ** 2) <= r * r
    sc = {}
    for dv in range(-s, s + 1):
        for du in range(-s, s + 1):
            cu, cv = int(u) + du, int(v) + dv
            sc[(cu, cv)] = float((M[cv - r:cv + r + 1, cu - r:cu + r + 1] * disk).sum())
    m = max(sc.values())
    top = [k for k, val in sc.items() if val >= m - 0.5]
    cu = np.mean([k[0] for k in top]); cv = np.mean([k[1] for k in top])
    return cu, cv, m / disk.sum(), len(top)
if __name__ == "__main__":
    for a in sys.argv[1:]:
        lab, u, v = a.split(":")
        cu, cv, f, n = best(float(u), float(v))
        cu2, cv2, f2, n2 = best(float(u), float(v), M=INK)
        print(f"{lab:8s} eye ({u},{v})  rest-disk ({cu:.1f},{cv:.1f}) fill {f:.2f} [{n}]   ink-disk ({cu2:.1f},{cv2:.1f}) fill {f2:.2f}")
