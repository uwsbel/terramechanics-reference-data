"""Erase the grid lines of a calibration from the (binary) page image, for viewing and tracing only.

A grid pixel run is erased where the run of ink across the line, measured from the line's centre,
is no wider than the line itself plus a margin: where a curve crosses or touches the line the run is
wider and the ink is kept. Output: a PNG of the same size as the page (pixel coordinates unchanged).
Never used for values: samples are always placed and checked on the original page.

usage: degrid.py <calibration_dir> <image> <out.png>
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def main():
    cal = json.loads((Path(sys.argv[1]) / "calibration.json").read_text(encoding="utf-8"))
    g = np.asarray(Image.open(sys.argv[2]).convert("L")).copy()
    ink = g < 128
    h, w = g.shape
    widths = {r["value"]: r["median_width_px"] for r in cal["refinement"]["lines"]}
    out = g.copy()
    for l in cal["vertical_lines"]:
        val = [v for k, v in l.items() if k.endswith("_value")][0]
        lw = widths[val]
        for v in range(h):
            c = l["u_at_v0"] + l["slope_du_dv"] * v
            ci = int(round(c))
            if not (0 <= ci < w) or not ink[v, ci]:
                # find nearest ink within half width
                cand = [ci + d for d in range(-int(lw), int(lw) + 1) if 0 <= ci + d < w and ink[v, ci + d]]
                if not cand:
                    continue
                ci = min(cand, key=lambda x: abs(x - c))
            a = ci
            while a - 1 >= 0 and ink[v, a - 1]:
                a -= 1
            b = ci
            while b + 1 < w and ink[v, b + 1]:
                b += 1
            if b - a + 1 <= lw + 3 and abs((a + b) / 2 - c) <= lw:
                out[v, a:b + 1] = 255
    for l in cal["horizontal_lines"]:
        val = [v for k, v in l.items() if k.endswith("_value")][0]
        lw = widths[val]
        for u in range(w):
            c = l["v_at_u0"] + l["slope_dv_du"] * u
            ci = int(round(c))
            if not (0 <= ci < h) or not ink[ci, u]:
                cand = [ci + d for d in range(-int(lw), int(lw) + 1) if 0 <= ci + d < h and ink[ci + d, u]]
                if not cand:
                    continue
                ci = min(cand, key=lambda x: abs(x - c))
            a = ci
            while a - 1 >= 0 and ink[a - 1, u]:
                a -= 1
            b = ci
            while b + 1 < h and ink[b + 1, u]:
                b += 1
            if b - a + 1 <= lw + 3 and abs((a + b) / 2 - c) <= lw:
                out[a:b + 1, u] = 255
    Image.fromarray(out).save(sys.argv[3])
    print("wrote", sys.argv[3])


if __name__ == "__main__":
    main()
