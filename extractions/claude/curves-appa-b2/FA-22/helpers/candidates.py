"""Candidate curve crossings along each sampling line (grain size constant), from the de-gridded
viewing aid: runs of non-grid ink within +-3 px of the line. Printed for the reader to assign by eye."""
import sys
import numpy as np
from PIL import Image
import fa22lib as L

D = np.asarray(Image.open(L.OUT / "helpers" / "degrid.png"))
rest = D == 0
def runs(x, u0=755, u1=2235, half=3, minfrac=2):
    us = np.arange(u0, u1)
    va, vb = L.v_of_x(x, u0), L.v_of_x(x, u1)
    vs = va + (vb - va) * (us - u0) / (u1 - u0)
    prof = np.array([rest[int(round(v)) - half:int(round(v)) + half + 1, u].sum() for u, v in zip(us, vs)])
    on = prof >= minfrac
    out = []
    i = 0
    while i < len(us):
        if on[i]:
            j = i
            while j + 1 < len(us) and on[j + 1]:
                j += 1
            w = prof[i:j + 1].astype(float)
            c = float((us[i:j + 1] * w).sum() / w.sum())
            out.append((round(c, 1), int(j - i + 1), round(float(vs[i]), 1)))
            i = j + 1
        else:
            i += 1
    return out

if __name__ == "__main__":
    for e in [float(a) for a in sys.argv[1:]]:
        x = 10 ** e
        r = [c for c in runs(x) if c[1] >= 5]
        print(f"log {e:+.2f} x {x:.4f} v~{L.v_of_x(x, 1800):.1f}: " + " ".join(f"{c[0]:.0f}({c[1]})" for c in r))
