"""Row scan: list dark runs (center u, width) along rows v, between u0 and u1.
python rowscan.py <image> --vs 2080,2090 --u0 600 --u1 2200 [--dark 128] [--halfwidth 1]"""
import argparse
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("image")
ap.add_argument("--vs", required=True)
ap.add_argument("--u0", type=int, required=True)
ap.add_argument("--u1", type=int, required=True)
ap.add_argument("--dark", type=int, default=128)
ap.add_argument("--halfwidth", type=int, default=1)
a = ap.parse_args()
g = np.asarray(Image.open(a.image).convert("L"))
print("v,u_center,width")
for v in [int(x) for x in a.vs.split(",")]:
    row = g[v - a.halfwidth:v + a.halfwidth + 1, a.u0:a.u1].min(axis=0) < a.dark
    idx = np.where(row)[0]
    if len(idx) == 0:
        continue
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            print(f"{v},{(s + p) / 2 + a.u0:.1f},{p - s + 1}")
            s = i
        p = i
    print(f"{v},{(s + p) / 2 + a.u0:.1f},{p - s + 1}")
