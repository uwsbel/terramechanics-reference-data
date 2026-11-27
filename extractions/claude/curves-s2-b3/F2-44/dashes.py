"""List the connected ink pieces met along a guide (dashes of a dashed trace)."""
import json, math, sys
from pathlib import Path
import blobs, snap
name = sys.argv[1]
spec = json.loads((Path(__file__).parent / "guides.json").read_text(encoding="utf-8"))[name]
guide = spec["guide"]
L = sum(math.hypot(b[0]-a[0], b[1]-a[1]) for a, b in zip(guide, guide[1:]))
seen = {}
s = 0.0
while s < L:
    u, v, _ = snap.point_at_arc(guide, s)
    for b in blobs.blobs_near(u, v, r=6, win=40):
        if b["d"] <= 40:
            # does the blob have ink within 5 px of the guide point?
            pass
    # ink at the guide point within 5 px
    bl = [b for b in blobs.blobs_near(u, v, r=6, win=40)]
    for b in bl:
        key = b["bbox"]
        u0, v0, u1, v1 = key
        if u0 - 5 <= u <= u1 + 5 and v0 - 5 <= v <= v1 + 5 and not b["edge"]:
            if key not in seen:
                seen[key] = (round(s), b["n"], b["cu"], b["cv"])
    s += 3
for k, (s, n, cu, cv) in sorted(seen.items(), key=lambda t: t[1][0]):
    x0, y0 = snap.xy(k[0], k[3]); x1, y1 = snap.xy(k[2], k[1])
    print(f"arc {s:5d} bbox u {k[0]}-{k[2]} v {k[1]}-{k[3]} n {n:4d} centroid ({cu},{cv})  x {x0:.3f}-{x1:.3f}")
