"""Before/after D-025 per panel: canonical reader, point counts, statuses; pending-review points near an
existing decision on the other reader's point (a decision that no longer applies after a canonical flip)."""
import csv
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SP = Path(sys.argv[1])
batches = ["curves-pilot-b1", "curves-appc-b1", "curves-appc-b2", "curves-appc-b3", "curves-appc-b4", "curves-appc-b5"]


def load(p):
    return list(csv.DictReader(open(p, encoding="utf-8-sig", newline="")))


tot = Counter()
for b in batches:
    before = load(SP / "before-d025" / f"{b}.csv")
    after = load(Path("qa") / b / "canonical.csv")
    fb, fa = defaultdict(list), defaultdict(list)
    for r in before:
        fb[(r.get("figure_id") or "FC-1B", r["panel"])].append(r)
    for r in after:
        fa[(r.get("figure_id") or "FC-1B", r["panel"])].append(r)
    for k in sorted(fa):
        sb = Counter(r["source"] or "?" for r in fb[k])
        sa = Counter(r["source"] for r in fa[k])
        cb = max(sb, key=sb.get)
        ca = max(sa, key=sa.get)
        stb = Counter(r["status"] for r in fb[k])
        sta = Counter(r["status"] for r in fa[k])
        # decisions on the other reader's points near each pending-review point
        dec_p = Path("qa") / b / f"decisions-{k[0]}-p{k[1]}.csv"
        decs = load(dec_p) if dec_p.exists() else []
        near = 0
        if sta.get("pending-review"):
            # pixel positions of decided points from the before file (same source and sequence)
            pos = {(r["series_id"], r["point_kind"], r["sequence"], r["source"]): (float(r["pixel_u"]), float(r["pixel_v"])) for r in fb[k]}
            dpos = [pos[(d["series_id"], d["point_kind"], d["sequence"], d["source"])] for d in decs
                    if (d["series_id"], d["point_kind"], d["sequence"], d["source"]) in pos]
            for r in fa[k]:
                if r["status"] != "pending-review":
                    continue
                u, v = float(r["pixel_u"]), float(r["pixel_v"])
                near += any(math.hypot(u - a, v - c) < 15 for a, c in dpos)
        flip = "FLIP" if cb != ca else ""
        print(f"{b:<16}{k[0]:<7}p{k[1]}  {cb:>6}->{ca:<6} {flip:<5} pts {len(fb[k]):>4}->{len(fa[k]):<4} "
              f"pending {stb.get('pending-review', 0)}->{sta.get('pending-review', 0)} (near an old decision {near})  "
              f"one-sided {stb.get('one-sided', 0)}->{sta.get('one-sided', 0)}  resolved {stb.get('resolved', 0)}->{sta.get('resolved', 0)}")
        tot["pending"] += sta.get("pending-review", 0)
        tot["near"] += near
        tot["flips"] += bool(flip)
        tot["one-sided"] += sta.get("one-sided", 0) - stb.get("one-sided", 0)
print(dict(tot))
