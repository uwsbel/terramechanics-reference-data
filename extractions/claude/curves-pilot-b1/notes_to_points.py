import csv, re, sys
from pathlib import Path
HERE = Path(__file__).parent
SID = {"circle": "n294", "triangle-up": "n587", "triangle-down": "n1172", "plus": "n1760", "asterisk": "n2935", "square": "n2345", "x": "n3520"}
rows, seq = [], {}
for line in (HERE / "notes-lower-markers.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(circle|triangle-up|triangle-down|plus|asterisk|square|x) (\d+) (\d+)(.*)$", line.strip())
    if not m:
        continue
    sym, u, v, rest = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4).strip()
    bm = re.search(r"bound (\d+)", rest)
    b = int(bm.group(1)) if bm else 3
    note = re.sub(r"\s*bound \d+", "", rest).strip(" ()")
    sid = SID[sym]
    seq[sid] = seq.get(sid, 0) + 1
    rows.append({"figure_id": "FC-1B", "panel": 2, "series_id": sid, "point_kind": "marker", "sequence": seq[sid],
                 "pixel_u": u, "pixel_v": v, "u_bound_px": b, "v_bound_px": b, "symbol": sym, "note": note})
rows.sort(key=lambda r: (r["series_id"], r["pixel_u"]))
for sid in SID.values():
    for i, r in enumerate([r for r in rows if r["series_id"] == sid], 1):
        r["sequence"] = i
with (HERE / "claude-fc1b-p2-markers.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), "markers;", {s: sum(1 for r in rows if r["series_id"] == s) for s in SID.values()})
