"""Summarize a dense track (track.py output) as runs of consecutive inked columns: start and end
column, v at both ends, thickness range, largest jump in v between neighbouring columns, flags.
python segs.py tracks/n4695.csv
"""
import csv
import sys

rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
segs = []
cur = None
for r in rows:
    ok = r["v"] != ""
    if ok and cur is not None and int(r["u"]) == cur[-1]["u"] + 1 and abs(float(r["v"]) - cur[-1]["v"]) <= 6:
        cur.append(dict(u=int(r["u"]), v=float(r["v"]), t=int(r["thick"]), f=r["flags"], g=float(r["guide"])))
    else:
        if cur:
            segs.append(cur)
        cur = [dict(u=int(r["u"]), v=float(r["v"]), t=int(r["thick"]), f=r["flags"], g=float(r["guide"]))] if ok else None
if cur:
    segs.append(cur)
for s in segs:
    flags = sorted(set(f for x in s for f in x["f"].split("|") if f))
    ts = [x["t"] for x in s]
    dev = max(abs(x["v"] - x["g"]) for x in s)
    print(f"u {s[0]['u']:5d}-{s[-1]['u']:5d} ({len(s):4d})  v {s[0]['v']:7.1f} -> {s[-1]['v']:7.1f}  "
          f"thick {min(ts):2d}-{max(ts):2d} med {sorted(ts)[len(ts)//2]:2d}  maxdev {dev:5.1f}  {','.join(flags)}")
