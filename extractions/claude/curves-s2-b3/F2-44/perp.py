"""Profile across a line at a page point: the dark runs along the normal of a line at angle `ang`
(degrees from horizontal, positive rising to the right), averaged over +-2 px along the line."""
import math, sys
from pathlib import Path
import numpy as np
from PIL import Image
HERE = Path(__file__).resolve().parent
g = np.asarray(Image.open(HERE.parents[1] / "packet" / "p0104.png").convert("L"), dtype=float)
DARK = 160


def bil(u, v):
    u0, v0 = int(math.floor(u)), int(math.floor(v)); fu, fv = u - u0, v - v0
    return (g[v0, u0] * (1 - fu) * (1 - fv) + g[v0, u0 + 1] * fu * (1 - fv) + g[v0 + 1, u0] * (1 - fu) * fv + g[v0 + 1, u0 + 1] * fu * fv)


def perp(u, v, ang, R=20, along=2):
    a = math.radians(ang)
    d = (math.cos(a), -math.sin(a)); n = (math.sin(a), math.cos(a))
    ss = np.arange(-R, R + 0.01, 0.5)
    prof = []
    for s in ss:
        vals = [bil(u + s * n[0] + t * d[0], v + s * n[1] + t * d[1]) for t in np.arange(-along, along + 0.01, 1.0)]
        prof.append(np.mean(vals))
    prof = np.array(prof)
    dark = prof < DARK
    runs, i = [], 0
    while i < len(ss):
        if dark[i]:
            j = i
            while j + 1 < len(ss) and dark[j + 1]:
                j += 1
            runs.append((ss[i], ss[j]))
            i = j + 1
        else:
            i += 1
    out = []
    for s0, s1 in runs:
        c = (s0 + s1) / 2
        out.append(dict(s0=s0, s1=s1, c=c, w=s1 - s0 + 0.5, u=round(u + c * n[0], 1), v=round(v + c * n[1], 1)))
    return out


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        u, v, ang = map(float, arg.split(","))
        rs = perp(u, v, ang)
        print(arg, " | ".join(f"s {r['s0']:+.1f}..{r['s1']:+.1f} w {r['w']:.1f} -> ({r['u']},{r['v']})" for r in rs))
