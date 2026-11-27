"""Claude reader helper (FA-18): in the steep part of the curves, the band of the three curves along
iso-percent lines (half-integer percents, between the 2 percent grid lines): top edge T (the lower
curve's top) and bottom edge B (the upper curve's bottom), tracked from p=60.5 outwards; an edge next
to grid ink is flagged (the band may continue under the grid line)."""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import geom, scanline as sl, cruns  # noqa: E402

V0, V1 = 1600, 1900


def band(p, centre, half=26):
    c, k = geom.iso_p(p)
    seq = [(v, sl.cls(c + k * v, v)) for v in range(V0, V1)]
    rs = [r for r in cruns.runs(seq) if r[1] - r[0] >= 1 and abs((r[0] + r[1]) / 2 - centre) <= half]
    if not rs:
        return None
    T = min(r[0] for r in rs); B = max(r[1] for r in rs)
    tl = [r for r in rs if r[0] == T][0][3]
    bh = [r for r in rs if r[1] == B][0][4]
    return T, B, tl, bh, rs


out = {}
for start, step, stop in ((60.5, 1, 97.6), (59.5, -1, 19.0)):
    centre = 1721.0
    p = start
    while (p <= stop if step > 0 else p >= stop):
        b = band(p, centre)
        if b:
            T, B, tl, bh, rs = b
            out[p] = (T, B, tl, bh)
            centre = 0.5 * (T + B)
            print(f"p={p:5.1f} T={'<' if tl else ' '}{T:5d} B={B:5d}{'>' if bh else ' '} width={B-T+1:3d}  runs " + " ".join(cruns.fmt(r) for r in rs))
        else:
            print(f"p={p:5.1f} none")
        p += step
json.dump({str(k): v for k, v in out.items()}, open(WS := (HERE.parents[3] / "out/FA-18/scratch/steep_band.json"), "w"))
