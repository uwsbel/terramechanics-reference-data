"""Reader's helper: fit the ring of each open circle on the page by rays cast from a rough center.

For each ray (every 5 degrees) the first dark run between r = 6 and r = 30 px is the ring; its middle
is a point on the ring's centre line. Rays whose run is much thicker than the ring (a grid line, a
curve or a joining line crossing it) or that find no ink are left out. A circle is fitted to the
remaining points by least squares (Kasa), points more than 2 px off are dropped, and the fit is
repeated from the new center. Prints center, radius, ring thickness, rays used and the angles left out.
"""
import sys
import numpy as np
from PIL import Image

img = sys.argv[1]
g = np.asarray(Image.open(img).convert("L")) < 128


def ray_points(uc, vc):
    pts, skipped, thick = [], [], []
    for deg in range(0, 360, 5):
        th = np.radians(deg)
        du, dv = np.cos(th), -np.sin(th)          # angle measured counter-clockwise on the page
        rs = np.arange(4, 32, 0.25)
        vals = []
        for r in rs:
            u, v = uc + r * du, vc + r * dv
            vals.append(g[int(round(v)), int(round(u))])
        vals = np.array(vals)
        idx = np.where(vals)[0]
        if len(idx) == 0:
            skipped.append((deg, "no ink"))
            continue
        # first run
        s = idx[0]
        e = s
        while e + 1 < len(vals) and vals[e + 1]:
            e += 1
        r_in, r_out = rs[s], rs[e]
        w = r_out - r_in
        if r_in < 8:
            skipped.append((deg, f"ink at r={r_in:.1f} (inside)"))
            continue
        if w > 9 or r_out >= rs[-1] - 0.5:
            skipped.append((deg, f"run {w:.1f} px (merged)"))
            continue
        rm = 0.5 * (r_in + r_out)
        pts.append((deg, uc + rm * du, vc + rm * dv))
        thick.append(w)
    return pts, skipped, thick


def fit(pts):
    P = np.array([[p[1], p[2]] for p in pts])
    A = np.c_[2 * P[:, 0], 2 * P[:, 1], np.ones(len(P))]
    b = (P ** 2).sum(1)
    c, *_ = np.linalg.lstsq(A, b, rcond=None)
    uc, vc = c[0], c[1]
    r = np.sqrt(c[2] + uc ** 2 + vc ** 2)
    res = np.hypot(P[:, 0] - uc, P[:, 1] - vc) - r
    return uc, vc, r, res


for arg in sys.argv[2:]:
    name, uv = arg.split("=")
    uc, vc = (float(x) for x in uv.split(","))
    for it in range(3):
        pts, skipped, thick = ray_points(uc, vc)
        uc2, vc2, r, res = fit(pts)
        keep = np.abs(res) <= 2.0
        pts2 = [p for p, k in zip(pts, keep) if k]
        uc2, vc2, r, res = fit(pts2)
        uc, vc = uc2, vc2
    print(f"{name}: center ({uc:.1f}, {vc:.1f}) r_mid {r:.1f} ring {np.median(thick):.1f} px; rays used {len(pts2)}/72; "
          f"rms {np.sqrt(np.mean(res**2)):.2f}; skipped: {', '.join(str(d) + ' ' + why for d, why in skipped)}"
          + (f"; dropped as outliers {len(pts) - len(pts2)}" if len(pts) != len(pts2) else ""))
