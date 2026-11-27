"""Claude reader helper (FA-18): along each page row v, the dark runs left of the 0 percent frame,
as offsets (px) from the frame's measured centre line; rows crossed by a horizontal grid line
(dark far to the left of the band) are marked GRID."""
import sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import geom  # noqa: E402

dark = geom.gray < 128
f0 = [l for l in geom.cal["vertical_lines"] if l["y_value"] == 0][0]
v0, v1, step = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
reach = int(sys.argv[4]) if len(sys.argv) > 4 else 70
for v in range(v0, v1, step):
    f = f0["u_at_v0"] + f0["slope_du_dv"] * v
    fi = int(round(f))
    seg = dark[v, fi - reach: fi + 8]
    runs, i = [], 0
    while i < len(seg):
        if seg[i]:
            j = i
            while j + 1 < len(seg) and seg[j + 1]:
                j += 1
            runs.append((i - reach + (fi - f), j - reach + (fi - f)))
            i = j + 1
        else:
            i += 1
    tag = "GRID" if dark[v, fi - reach - 15: fi - reach].mean() > 0.6 else ""
    print(f"{v} f={f:.1f} {tag:4s} " + " ".join(f"[{a:+.0f},{b:+.0f}]" for a, b in runs))
