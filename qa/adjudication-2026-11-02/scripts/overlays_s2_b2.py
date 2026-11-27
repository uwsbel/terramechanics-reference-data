"""Write qa/curves-s2-b2/overlays.csv with the batch 1 recipe: the box is reading A's (Claude's) calibration box."""
import csv
import json
from pathlib import Path

REPO = Path(r"<repository>")
B = "curves-s2-b2"
PAGES = {"F2-45": 106, "F2-46": 107, "F2-47": 108, "F2-48": 109}
with (REPO / "qa" / B / "overlays.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["figure_id", "panel", "image", "box", "points_a", "points_b", "name"])
    for fid, p in PAGES.items():
        cal = json.loads((REPO / f"extractions/claude/{B}/{fid}/cal-p1/calibration.json").read_text(encoding="utf-8"))
        assert cal["image"].endswith(f"p{p:04d}.png"), (fid, cal["image"])
        w.writerow([fid, 1, f"corpus/1968/images/p{p:04d}.png", " ".join(str(int(x)) for x in cal["box"]),
                    f"extractions/claude/{B}/{fid}/points-p1-native.csv",
                    f"extractions/codex/{B}/{fid}/points-p1-native.csv", f"{fid}-p1"])
print((REPO / "qa" / B / "overlays.csv").read_text(encoding="utf-8"))
