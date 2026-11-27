"""Claude reader helper (FA-18): print the ink along an iso-percent line (scan in v) or an
iso-grain-size line (scan in u): C = curve ink (dark, not on a grid line), g = dark on a grid line,
. = white. Used to read the band edges and the dash gaps of the three curves."""
import sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import geom  # noqa: E402

WS = HERE.parents[3]
mask = np.load(WS / "out/FA-18/scratch/mask.npy")
dark = geom.gray < 128


def cls(u, v):
    ui, vi = int(round(u)), int(round(v))
    if not dark[vi, ui]:
        return "."
    return "g" if mask[vi, ui] else "C"


def along_p(p, v0, v1):
    c, k = geom.iso_p(p)
    return [(c + k * v, v, cls(c + k * v, v)) for v in range(v0, v1)]


def along_g(g, u0, u1):
    c, k = geom.iso_g(g)
    return [(u, c + k * u, cls(u, c + k * u)) for u in range(u0, u1)]


def show(seq, key, pad=8):
    s = "".join(x[2] for x in seq)
    idx = [i for i, ch in enumerate(s) if ch == "C"]
    if not idx:
        print(f"{key}: no curve ink"); return
    a, b = max(0, idx[0] - pad), min(len(s), idx[-1] + pad + 1)
    t0 = seq[a][1] if seq is not None and isinstance(seq[a][1], (int, np.integer)) and False else None
    print(f"{key}: from ({seq[a][0]:.0f},{seq[a][1]:.0f}) {s[a:b]}")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "p":
        v0, v1 = int(sys.argv[2]), int(sys.argv[3])
        for p in [float(x) for x in sys.argv[4].split(",")]:
            show(along_p(p, v0, v1), f"p={p:5.1f}")
    else:
        u0, u1 = int(sys.argv[2]), int(sys.argv[3])
        for g in [float(x) for x in sys.argv[4].split(",")]:
            show(along_g(g, u0, u1), f"g={g:.4f}")
