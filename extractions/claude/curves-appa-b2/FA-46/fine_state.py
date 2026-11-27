"""Per-row state in the fine part: B's run, A presence (ink left of B), C presence (ink between B and frame)."""
import numpy as np
from PIL import Image
from pathlib import Path
HERE = Path(__file__).resolve().parent
g = np.asarray(Image.open(HERE.parent.parent / "packet" / "p0095.png").convert("L")) < 128
def runs(v, lo=2100, hi=2205):
    line = g[v, lo:hi + 1]; out = []; s = None
    for i, d in enumerate(line):
        if d and s is None: s = i
        if not d and s is not None: out.append((lo + s, lo + i - 1)); s = None
    if s is not None: out.append((lo + s, hi))
    return out
def bexp(v):  # rough expected B centre: 2165.5 at v<=2600, 2174 at v>=3060, linear between
    if v <= 2600: return 2165.5
    if v >= 3060: return 2174.0
    return 2165.5 + (v - 2600) * (8.5 / 460)
def frame_c(v):
    return 2174.9 + 0.0060 * v
rows = []
for v in range(2380, 3196):
    r = runs(v)
    grid = any(a <= 2135 and b >= 2145 for a, b in r)
    bc = bexp(v)
    R = next(((a, b) for a, b in r if a <= bc <= b), None)
    fc = frame_c(v)
    F = next(((a, b) for a, b in r if a <= fc <= b), None)
    if R is None:
        print(f"{v} {'G' if grid else ' '} B? runs={r}")
        continue
    merged_frame = F is not None and R == F
    A = "A" if R[0] <= bc - 9 else "."
    # C: ink at bc+9..bc+12 region
    cprobe = int(round(bc + 10))
    C = "C" if g[v, cprobe] and g[v, cprobe - 2] else "."
    print(f"{v} {'G' if grid else ' '} R={R[0]}-{R[1]} {'=F' if merged_frame else '  '} F={F} {A}{C} Bexp={bc:.1f}")
