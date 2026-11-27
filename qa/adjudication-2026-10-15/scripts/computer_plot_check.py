"""Computer plots C-8 to C-15: the printed box (tan theta, cohesion) against (a) the drawn line as read by each
reader (least squares through its trace samples) and (b) a least-squares line through the plotted symbols."""
import csv, re, sys
import numpy as np
from pathlib import Path
REPO = Path(r"<repository>")
rows = {r["id"]: r for r in csv.DictReader(open(REPO / "corpus/1968-vol2/figures.csv", encoding="utf-8-sig"))}
def box(fid):
    t = (REPO / f"corpus/1968-vol2/pages/p{int(rows[fid]['pdf_page']):04d}.md").read_text(encoding="utf-8")
    g = lambda k: float(re.search(k + r"\s*=\s*(-?[\d.]+)", t).group(1))
    return g("Tan Theta"), g("Cohesion"), g("Angle of Friction")
def fit(pts):
    x, y = np.array([p[0] for p in pts]), np.array([p[1] for p in pts])
    b, a = np.polyfit(x, y, 1)
    return b, a
print("| figure | printed tan, c | line Claude tan, c | line Codex tan, c | symbols (canonical) tan, c | n |")
print("|---|---|---|---|---|---|")
for batch in sys.argv[1:]:
    can = list(csv.DictReader(open(REPO / "qa" / batch / "canonical.csv", encoding="utf-8")))
    for fid in dict.fromkeys(r["figure_id"] for r in can):
        tn, c, ph = box(fid)
        cells = []
        for lab in ("claude", "codex"):
            rd = [r for r in csv.DictReader(open(REPO / "qa" / batch / "rederived" / lab / fid / "points-p1-native.csv", encoding="utf-8"))
                  if r["point_kind"] == "trace"]
            b, a = fit([(float(r["x_native"]), float(r["y_native"])) for r in rd])
            cells.append(f"{b:.4f}, {a:.1f}")
        mk = [(float(r["x_native"]), float(r["y_native"])) for r in can if r["figure_id"] == fid and r["point_kind"] == "marker"]
        b, a = fit(mk)
        print(f"| {fid} | {tn}, {c} | {cells[0]} | {cells[1]} | {b:.4f}, {a:.1f} | {len(mk)} |")
