"""Connected dark blobs near a page point (dots of the dotted trace, dashes): centroid, size, bbox."""
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
WS = HERE.parents[1]
g = np.asarray(Image.open(WS / "packet" / "p0104.png").convert("L"))
DARK = 160


def blobs_near(u, v, r=14, win=30):
    u0, v0 = int(u) - win, int(v) - win
    sub = g[v0:v0 + 2 * win + 1, u0:u0 + 2 * win + 1] < DARK
    lab = np.zeros(sub.shape, int)
    n = 0
    out = []
    for i in range(sub.shape[0]):
        for j in range(sub.shape[1]):
            if sub[i, j] and not lab[i, j]:
                n += 1
                stack = [(i, j)]; lab[i, j] = n; pts = []
                while stack:
                    a, b = stack.pop(); pts.append((a, b))
                    for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        aa, bb = a + da, b + db
                        if 0 <= aa < sub.shape[0] and 0 <= bb < sub.shape[1] and sub[aa, bb] and not lab[aa, bb]:
                            lab[aa, bb] = n; stack.append((aa, bb))
                P = np.array(pts)
                cu, cv = P[:, 1].mean() + u0, P[:, 0].mean() + v0
                d = math.hypot(cu - u, cv - v)
                touches = P[:, 0].min() == 0 or P[:, 1].min() == 0 or P[:, 0].max() == sub.shape[0] - 1 or P[:, 1].max() == sub.shape[1] - 1
                out.append(dict(cu=round(cu, 1), cv=round(cv, 1), n=len(pts), d=round(d, 1),
                                bbox=(int(P[:, 1].min() + u0), int(P[:, 0].min() + v0), int(P[:, 1].max() + u0), int(P[:, 0].max() + v0)),
                                edge=bool(touches)))
    return sorted([o for o in out if o["d"] <= r + 20], key=lambda o: o["d"])


if __name__ == "__main__":
    for a in sys.argv[1:]:
        u, v = map(float, a.split(","))
        print(a, blobs_near(u, v)[:4])
