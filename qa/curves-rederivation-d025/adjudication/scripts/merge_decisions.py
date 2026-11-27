"""Append the decision rows of an adjudication round (<out_dir>/<batch>/decisions-<figure>-p<n>.csv) to the
batches' own decision files; a point that already has a decision keeps it (reported, not overwritten)."""
import csv
import sys
from pathlib import Path

REPO = Path(r"<repository>")
COLS = ["panel", "series_id", "point_kind", "sequence", "source", "status", "use", "note"]
src_dir = Path(sys.argv[1])
added = clash = 0
for f in sorted(src_dir.glob("*/decisions-*.csv")):
    batch = f.parent.name
    dst = REPO / "qa" / batch / f.name
    old = list(csv.DictReader(open(dst, encoding="utf-8-sig", newline=""))) if dst.exists() else []
    have = {(r["panel"], r["series_id"], r["point_kind"], r["sequence"], r["source"]) for r in old}
    new = []
    for r in csv.DictReader(open(f, encoding="utf-8-sig", newline="")):
        k = (r["panel"], r["series_id"], r["point_kind"], r["sequence"], r["source"])
        if k in have:
            clash += 1
            print("already decided, kept:", batch, f.name, k)
            continue
        new.append(r)
    with open(dst, "w", encoding="utf-8", newline="") as g:
        w = csv.DictWriter(g, fieldnames=COLS, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(old + new)
    added += len(new)
    print(f"{batch}/{f.name}: {len(old)} + {len(new)}")
print("added", added, "kept existing", clash)
