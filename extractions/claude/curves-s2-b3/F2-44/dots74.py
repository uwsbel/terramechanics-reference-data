"""Collect the isolated dots of trace 74 along its guide (blob centroids)."""
import json, math
from pathlib import Path
import blobs, snap
spec = json.loads((Path(__file__).parent / "guides.json").read_text(encoding="utf-8"))["lpt74"]
guide = spec["guide"]
L = sum(math.hypot(b[0]-a[0], b[1]-a[1]) for a, b in zip(guide, guide[1:]))
seen = []
s = 0.0
while s < L:
    u, v, _ = snap.point_at_arc(guide, s)
    for b in blobs.blobs_near(u, v, r=9, win=22):
        if b["d"] <= 9 and not b["edge"] and b["n"] < 160 and (b["bbox"][2]-b["bbox"][0]) < 16 and (b["bbox"][3]-b["bbox"][1]) < 16:
            if all(math.hypot(b["cu"]-c[0], b["cv"]-c[1]) > 3 for c in seen):
                x, y = snap.xy(b["cu"], b["cv"])
                seen.append((float(b["cu"]), float(b["cv"]), b["n"], b["bbox"], round(x, 3), round(y)))
    s += 4
seen.sort(key=lambda t: t[0])
for t in seen: print(t)
json.dump(seen, open(Path(__file__).parent / "dots74.json", "w"), indent=0)
