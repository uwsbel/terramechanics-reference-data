"""qa/<batch>/overlays.csv for a filed curve batch: one row per figure and panel; the box is the union of
the two readers' calibration boxes, a little outside, so the overlay shows everything both read."""
import csv, json, sys
from pathlib import Path
REPO = Path(r"<repository>")
batch = sys.argv[1]
cfg = json.loads((REPO / "qa" / batch / "batch.json").read_text(encoding="utf-8"))
rows = {r["id"]: r for r in csv.DictReader(open(REPO / "corpus" / cfg["source"] / "figures.csv", encoding="utf-8-sig"))}
out = []
for fid in cfg["figures"]:
    boxes = []
    for lab in ("claude", "codex"):
        c = json.loads((REPO / "extractions" / lab / batch / fid / "cal-p1" / "calibration.json").read_text(encoding="utf-8"))
        if c.get("box"):
            boxes.append(c["box"])
    b = [min(x[0] for x in boxes) - 60, min(x[1] for x in boxes) - 60, max(x[2] for x in boxes) + 60, max(x[3] for x in boxes) + 60]
    out.append({"figure_id": fid, "panel": "1", "image": f"corpus/{cfg['source']}/images/p{int(rows[fid]['pdf_page']):04d}.png",
                "box": " ".join(str(int(v)) for v in b),
                "points_a": f"extractions/claude/{batch}/{fid}/points-p1-native.csv",
                "points_b": f"extractions/codex/{batch}/{fid}/points-p1-native.csv", "name": f"{fid}-p1"})
with open(REPO / "qa" / batch / "overlays.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n"); w.writeheader(); w.writerows(out)
print("\n".join(f"{o['figure_id']} {o['box']}" for o in out))
