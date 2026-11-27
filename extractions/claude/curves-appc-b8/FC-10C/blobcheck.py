"""Completeness check for markers (reader's helper, not part of tools/): masks the grid lines of a
calibration and the drawn line (v = a + b u, +-halfv px vertically), then lists clusters of remaining
dark ink inside the plot frame with their bbox and pixel count, so a symbol the reader missed shows up.

    python blobcheck.py <image> <cal_dir> <a> <b> <halfv> [--min 120]
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def main():
    img, cal_dir, a, b, halfv = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    mn = int(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 120
    g = np.asarray(Image.open(img).convert("L")) < 150
    cal = json.loads((Path(cal_dir) / "calibration.json").read_text(encoding="utf-8"))
    H, W = g.shape
    V, U = np.mgrid[0:H, 0:W]
    mask = np.zeros_like(g)
    for l in cal["vertical_lines"]:
        mask |= np.abs(U - (l["u_at_v0"] + l["slope_du_dv"] * V)) <= 7
    for l in cal["horizontal_lines"]:
        mask |= np.abs(V - (l["v_at_u0"] + l["slope_dv_du"] * U)) <= 7
    mask |= np.abs(V - (a + b * U)) <= halfv
    u0, v0, u1, v1 = cal["box"]
    inside = (U > u0 + 15) & (U < u1 - 15) & (V > v0 + 15) & (V < v1 - 15)
    ink = g & ~mask & inside
    # coarse cells of 8 px, then 8-connected clusters of non-empty cells
    c = 8
    h, w = H // c, W // c
    cells = ink[:h * c, :w * c].reshape(h, c, w, c).sum(axis=(1, 3))
    occ = cells > 0
    seen = np.zeros_like(occ)
    out = []
    for i, j in zip(*np.where(occ)):
        if seen[i, j]:
            continue
        stack, comp = [(i, j)], []
        seen[i, j] = True
        while stack:
            p, q = stack.pop()
            comp.append((p, q))
            for dp in (-1, 0, 1):
                for dq in (-1, 0, 1):
                    r, s = p + dp, q + dq
                    if 0 <= r < h and 0 <= s < w and occ[r, s] and not seen[r, s]:
                        seen[r, s] = True
                        stack.append((r, s))
        n = int(sum(cells[p, q] for p, q in comp))
        if n >= mn:
            ps, qs = [p for p, _ in comp], [q for _, q in comp]
            out.append((min(qs) * c, max(qs) * c + c, min(ps) * c, max(ps) * c + c, n))
    for uu0, uu1, vv0, vv1, n in sorted(out):
        print(f"ink cluster u {uu0}..{uu1} v {vv0}..{vv1}: {n} px")


if __name__ == "__main__":
    main()
