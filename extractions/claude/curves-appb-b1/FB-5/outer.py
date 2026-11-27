"""Outer edge of each closed marker ring: along rays from the hole-circle centre, the first white
pixel after the ring (starting inside the ring); rays whose ring runs on past 23 px (merged with a
line or a neighbouring symbol) are left out. Usage: python outer.py <image>"""
import sys
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import markers as M

out = {}
for k, (u, v) in M.SEEDS.items():
    h = M.hole_fit(u, v)
    pts = []
    for ang in np.arange(0, 360, 2):
        ca, sa = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        r = h["r_in"] + 1.5
        edge = None
        while r < 26:
            uu, vv = h["u"] + r * ca, h["v"] + r * sa
            if not M.dark[int(round(vv)), int(round(uu))]:
                edge = r
                break
            r += 0.25
        if edge is not None and edge < 23:
            pts.append((h["u"] + (edge - 0.5) * ca, h["v"] + (edge - 0.5) * sa))
    P = np.array(pts)
    uc, vc, R, rms = M.kasa(P[:, 0], P[:, 1])
    # one robust pass
    d = np.hypot(P[:, 0] - uc, P[:, 1] - vc) - R
    keep = np.abs(d) < 2.0
    uc, vc, R, rms = M.kasa(P[keep, 0], P[keep, 1])
    out[k] = (uc, vc, R)
    print(f"{k:16s} hole ({h['u']:.1f}, {h['v']:.1f}) r_in {h['r_in']:.1f} | outer ({uc:.1f}, {vc:.1f}) R {R:.1f} rms {rms:.2f} rays {keep.sum()}/{len(P)} | diff ({uc - h['u']:+.1f}, {vc - h['v']:+.1f})")
