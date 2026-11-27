"""Cluster marker-interior holes (helpers.holes) into marker candidates; print bbox centers."""
import sys
sys.path.insert(0, "out/FC-3B")
from helpers import holes
img = "packet/p0124.png"
panel = int(sys.argv[1])
box = (686,1600,2142,2730) if panel == 1 else (686,2878,2142,3450)
hs = holes(img, box)
used = [False]*len(hs); clusters = []
for i, a in enumerate(hs):
    if used[i]: continue
    cl = [a]; used[i] = True; changed = True
    while changed:
        changed = False
        for j, b in enumerate(hs):
            if used[j]: continue
            for c in cl:
                ou = min(c["u1"], b["u1"]) - max(c["u0"], b["u0"])
                gv = max(c["v0"], b["v0"]) - min(c["v1"], b["v1"])
                gu = max(c["u0"], b["u0"]) - min(c["u1"], b["u1"])
                if (ou > -3 and gv <= 12) or (abs(c["cv"]-b["cv"]) < 10 and gu <= 12):
                    cl.append(b); used[j] = True; changed = True; break
    clusters.append(cl)
for cl in sorted(clusters, key=lambda c: (min(x["u0"] for x in c)//60, min(x["v0"] for x in c))):
    u0 = min(x["u0"] for x in cl); u1 = max(x["u1"] for x in cl)
    v0 = min(x["v0"] for x in cl); v1 = max(x["v1"] for x in cl)
    print(f"n={len(cl)} center=({(u0+u1)/2:.1f},{(v0+v1)/2:.1f}) w={u1-u0+1} h={v1-v0+1} bbox=({u0},{v0},{u1},{v1})")
