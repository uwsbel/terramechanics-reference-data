"""Claude reader helper (FA-18): find every straight grid line of the sheet (labelled, unlabelled,
dashed sieve lines, frame) and write a viewing image in which the grid's pixels are grey and all
other ink black, so the three curves can be followed where they cross the dense log grid. For
reading only: the calibration uses the labelled lines of cal-p1, never this mask."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve()
WS = HERE.parents[3]
g = np.asarray(Image.open(WS / "packet/p0039.png").convert("L"))
dark = g < 128
H, Wd = g.shape
U0, U1, V0, V1 = 575, 2115, 1085, 3760


def find(axis, k, thr):
    """lines along `axis` ('h': v = c + k u; 'v': u = c + k v): dark fraction along every tilted line"""
    out = []
    if axis == "h":
        us = np.arange(U0, U1)
        for c in np.arange(V0 - k * U0 - 40, V1 - k * U0 + 40, 1.0):
            vs = np.round(c + k * us).astype(int)
            ok = (vs >= V0) & (vs < V1)
            if ok.sum() < 0.5 * len(us):
                out.append(0.0); continue
            out.append(dark[vs[ok], us[ok]].mean())
        base = V0 - k * U0 - 40
    else:
        vs = np.arange(V0, V1)
        for c in np.arange(U0 - k * V0 - 80, U1 - k * V0 + 10, 1.0):
            us = np.round(c + k * vs).astype(int)
            ok = (us >= U0) & (us < U1)
            if ok.sum() < 0.5 * len(vs):
                out.append(0.0); continue
            out.append(dark[vs[ok], us[ok]].mean())
        base = U0 - k * V0 - 80
    f = np.array(out)
    lines = []
    i = 0
    while i < len(f):
        if f[i] >= thr:
            j = i
            while j + 1 < len(f) and f[j + 1] >= thr:
                j += 1
            seg = f[i:j + 1]
            c = base + i + (np.arange(len(seg)) * seg).sum() / seg.sum()
            lines.append((c, j - i + 1, float(seg.max())))
            i = j + 1
        else:
            i += 1
    return lines


if __name__ == "__main__":
    thr = float(sys.argv[1]) if len(sys.argv) > 1 else 0.3
    hl = find("h", -0.0190, thr)
    vl = find("v", 0.0216, thr)
    print("horizontal (v at u=0, width, max):", len(hl))
    for c, w, m in hl:
        print(f"  {c:8.1f} {w:3d} {m:.2f}   v@u=1000: {c - 0.019 * 1000:.1f}")
    print("vertical (u at v=0, width, max):", len(vl))
    for c, w, m in vl:
        print(f"  {c:8.1f} {w:3d} {m:.2f}   u@v=2500: {c + 0.0216 * 2500:.1f}")
    np.save(WS / "out/FA-18/scratch/gridlines.npy", np.array([("h", c, w) for c, w, m in hl] + [("v", c, w) for c, w, m in vl], dtype=object), allow_pickle=True)
