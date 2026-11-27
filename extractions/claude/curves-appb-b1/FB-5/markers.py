"""Open-circle marker centres on FB-5 (p0111.png).
For a marker whose hole (the white interior) is closed, the centre is a least-squares circle fitted
to the hole's boundary pixels, checked against a circle fitted to the ring's outer boundary where the
ring is not merged with a line. For markers whose holes are cut (overlapping circles, a partly printed
circle) a ring template of the measured radii is matched to the ink instead (see `template`).
Usage: python markers.py <image>"""
import sys
import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L"))
dark = g < 128


def flood(mask, seed):
    """Connected component (4-neighbour) of True pixels in mask containing seed (v, u)."""
    h, w = mask.shape
    out = np.zeros_like(mask)
    st = [seed]
    while st:
        v, u = st.pop()
        if v < 0 or u < 0 or v >= h or u >= w or out[v, u] or not mask[v, u]:
            continue
        out[v, u] = True
        st.extend(((v + 1, u), (v - 1, u), (v, u + 1), (v, u - 1)))
    return out


def kasa(us, vs):
    A = np.c_[us, vs, np.ones_like(us)]
    b = us ** 2 + vs ** 2
    c, *_ = np.linalg.lstsq(A, b, rcond=None)
    uc, vc = c[0] / 2, c[1] / 2
    r = np.sqrt(c[2] + uc ** 2 + vc ** 2)
    res = np.hypot(us - uc, vs - vc) - r
    return uc, vc, r, float(np.sqrt(np.mean(res ** 2)))


def hole_fit(seed_u, seed_v, win=40):
    """Fit a circle to the boundary of the white hole containing the seed."""
    u0, v0 = int(seed_u) - win, int(seed_v) - win
    sub = ~dark[v0:v0 + 2 * win, u0:u0 + 2 * win]
    hole = flood(sub, (int(seed_v) - v0, int(seed_u) - u0))
    if hole[0, :].any() or hole[-1, :].any() or hole[:, 0].any() or hole[:, -1].any():
        return None   # not closed
    # boundary: hole pixels with a dark 4-neighbour; use the pixel edge midpoint between them
    pts = []
    for dv, du in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nb = np.roll(np.roll(hole, -dv, axis=0), -du, axis=1)
        vv, uu = np.nonzero(hole & ~nb & np.roll(np.roll(~sub, -dv, axis=0), -du, axis=1))
        pts += list(zip(uu + 0.5 * du, vv + 0.5 * dv))
    P = np.array(pts, dtype=float)
    uc, vc, r, rms = kasa(P[:, 0] + u0, P[:, 1] + v0)
    area = hole.sum()
    vv, uu = np.nonzero(hole)
    return dict(u=uc, v=vc, r_in=r, rms=rms, n=len(P), area=int(area), cu=uu.mean() + u0, cv=vv.mean() + v0,
                ext=(uu.min() + u0, uu.max() + u0, vv.min() + v0, vv.max() + v0))


def outer_fit(uc, vc, r_lo, r_hi, exclude=()):
    """Outer edge of the ring: along rays from (uc, vc), the last dark pixel before white beyond
    r_lo..r_hi; rays in `exclude` angular ranges (degrees, page frame, 0 = +u, 90 = +v) skipped."""
    pts = []
    for ang in np.arange(0, 360, 3):
        if any(a <= ang <= b for a, b in exclude):
            continue
        ca, sa = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        last = None
        for r in np.arange(r_lo, r_hi, 0.25):
            u, v = uc + r * ca, vc + r * sa
            if dark[int(round(v)), int(round(u))]:
                last = r
        if last is not None:
            pts.append((uc + (last + 0.5) * ca, vc + (last + 0.5) * sa, ang, last))
    P = np.array(pts)
    return kasa(P[:, 0], P[:, 1]), P


SEEDS = {
    # name: approximate hole centre (u, v), from the zoomed crops
    "dense_left_top": (1044, 2889),
    "dense_mid_up": (1387, 2172),
    "dense_mid_low": (1391, 2237),
    "dense_top_up": (2376, 1081),
    "dense_top_low": (2377, 1150),
    "loose_bot_up": (1123, 3471),
    "loose_bot_low": (1135, 3507),
    "loose_mid_up": (1580, 3028),
    "loose_mid_low": (1585, 3067),
    "loose_top_up": (2352, 2479),
}

if __name__ == "__main__":
    res = {}
    for k, (u, v) in SEEDS.items():
        h = hole_fit(u, v)
        if h is None:
            print(f"{k:16s} hole not closed")
            continue
        res[k] = h
        print(f"{k:16s} hole-circle ({h['u']:.1f}, {h['v']:.1f}) r_in {h['r_in']:.1f} rms {h['rms']:.2f} n {h['n']}  "
              f"centroid ({h['cu']:.1f}, {h['cv']:.1f}) ext u {h['ext'][0]}-{h['ext'][1]} v {h['ext'][2]}-{h['ext'][3]}")
