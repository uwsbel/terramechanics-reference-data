"""Claude reader helper (FA-18): along an iso-percent line (near-vertical on the page), the runs of
curve ink (C), grid ink (g) and white, as v intervals; used for the steep part of the curves."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import geom, scanline as sl  # noqa: E402

v0, v1 = int(sys.argv[1]), int(sys.argv[2])
for p in [float(x) for x in sys.argv[3].split(",")]:
    c, k = geom.iso_p(p)
    seq = [(v, sl.cls(c + k * v, v)) for v in range(v0, v1)]
    runs, i = [], 0
    while i < len(seq):
        j = i
        while j + 1 < len(seq) and seq[j + 1][1] == seq[i][1]:
            j += 1
        if seq[i][1] != ".":
            runs.append(f"{seq[i][1]}{seq[i][0]}-{seq[j][0]}")
        i = j + 1
    print(f"p={p:5.1f} u@1750={c + k * 1750:7.1f}: " + " ".join(runs))
