"""Find tick stubs along each frame line of FB-6: ink in a band parallel to the frame, at a given
distance range from the frame centre line, on the inside and on the outside of the plot."""
import sys
import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L"))
dark = g < 128
frames = {  # (c, k): vertical u = c + k v ; horizontal v = c + k u ; inside direction sign
    "left":   ("v", 603.97, 0.03117, +1, (900, 3990)),
    "right":  ("v", 2484.99, 0.02982, -1, (830, 3950)),
    "top":    ("h", 852.11, -0.02563, +1, (660, 2490)),
    "bottom": ("h", 4052.17, -0.02779, -1, (760, 2590)),
}
d_lo, d_hi = int(sys.argv[2]) if len(sys.argv) > 2 else 9, int(sys.argv[3]) if len(sys.argv) > 3 else 20
for name, (o, c, k, ins, (t0, t1)) in frames.items():
    for side, sgn in (("inside", ins), ("outside", -ins)):
        hits = []
        for t in range(t0, t1):
            p = c + k * t
            cnt = 0
            for d in range(d_lo, d_hi + 1):
                q = int(round(p + sgn * d))
                cnt += dark[t, q] if o == "v" else dark[q, t]
            hits.append(cnt)
        hits = np.array(hits)
        full = np.where(hits >= 0.8 * (d_hi - d_lo + 1))[0]
        groups = np.split(full, np.where(np.diff(full) > 2)[0] + 1) if len(full) else []
        desc = [f"{t0 + (gr[0] + gr[-1]) / 2:.0f}(w{gr[-1] - gr[0] + 1})" for gr in groups if len(gr)]
        print(f"{name:6s} {side:7s} stubs at t = {', '.join(desc)}")
