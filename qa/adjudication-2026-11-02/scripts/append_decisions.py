"""Append the round 2 decision rows to the batches' decisions files; refuse a point decided twice."""
import csv
import sys
from pathlib import Path

REPO = Path(r"<repository>")
SRC = Path(sys.argv[1])
F = ["panel", "series_id", "point_kind", "sequence", "source", "status", "use", "note"]
key = lambda d: (d["panel"], d["source"], d["series_id"], d["point_kind"], d["sequence"])
for f in sorted(SRC.glob("*/decisions-*.csv")):
    dest = REPO / "qa" / f.parent.name / f.name
    old = list(csv.DictReader(open(dest, encoding="utf-8"))) if dest.exists() else []
    new = list(csv.DictReader(open(f, encoding="utf-8")))
    clash = {key(d) for d in old} & {key(d) for d in new}
    assert not clash, f"{dest}: decided twice: {sorted(clash)}"
    with open(dest, "w", encoding="utf-8", newline="") as o:
        w = csv.DictWriter(o, fieldnames=F, lineterminator="\n")
        w.writeheader()
        w.writerows(old + new)
    print(f"{dest.relative_to(REPO)}: {len(old)} + {len(new)} rows")
