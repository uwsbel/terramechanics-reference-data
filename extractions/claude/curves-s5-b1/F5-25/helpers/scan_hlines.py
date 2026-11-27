"""Scan for horizontal (time) line ink: for windows of 30 px along u, rows whose dark fraction
exceeds a threshold, merged into runs; prints window center u and run center v."""
import sys
import numpy as np
from PIL import Image
img = np.asarray(Image.open(sys.argv[1]).convert("L"))
dark = img < 160
u0, u1, v0, v1 = 725, 2285, 1780, 3545
W = 30
for uc in range(u0, u1, W):
    sub = dark[v0:v1, uc:uc + W]
    frac = sub.mean(axis=1)
    idx = np.where(frac >= 0.6)[0]
    runs = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i != p + 1:
                runs.append((s + p) / 2 + v0); s = i
            p = i
        runs.append((s + p) / 2 + v0)
    print(uc + W // 2, " ".join(f"{r:.0f}" for r in runs))
