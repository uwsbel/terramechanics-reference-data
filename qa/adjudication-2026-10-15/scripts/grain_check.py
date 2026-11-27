"""Grain-size charts FA-2 ... FA-46: D10, D50, D60, D95 and Cu of each canonical curve (interpolated in log10 of
grain size along the drawn curve), against the parameters printed in each chart's table (page transcriptions)."""
import csv, math, re
from pathlib import Path
REPO = Path(r"<repository>")
rows = {r["id"]: r for r in csv.DictReader(open(REPO / "corpus/1968-vol2/figures.csv", encoding="utf-8-sig"))}
can = [r for r in csv.DictReader(open(REPO / "qa/curves-appa-b2/canonical.csv", encoding="utf-8"))
       if r["point_kind"] == "trace" and r["status"] in ("agreed", "one-sided-verified", "resolved")]


def d_at(pts, p):
    """Grain size at percent finer p: first crossing walking up the curve, interpolated in log10(size)."""
    pts = sorted(pts, key=lambda t: t[0])
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if (y0 - p) * (y1 - p) <= 0 and y1 != y0:
            t = (p - y0) / (y1 - y0)
            return 10 ** (math.log10(x0) + t * (math.log10(x1) - math.log10(x0)))
    return float("nan")


print("| figure | printed (inset) | average: D10 D50 D60 D95 Cu | range of upper/lower D50 |")
print("|---|---|---|---|")
for fid in ("FA-2", "FA-6", "FA-18", "FA-22", "FA-26", "FA-38", "FA-46"):
    page = (REPO / f"corpus/1968-vol2/pages/p{int(rows[fid]['pdf_page']):04d}.md").read_text(encoding="utf-8")
    pr = {}
    for line in page.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4:
            sym = re.sub(r"[_{}$ ]", "", cells[1])
            if sym in ("D50", "D10", "Cu", "D95"):
                pr[sym] = (cells[2], cells[3])
    s = {}
    for ser in ("average", "upper", "lower"):
        pts = [(float(r["x_native"]), float(r["y_native"])) for r in can if r["figure_id"] == fid and r["series_id"] == ser]
        d = {p: d_at(pts, p) for p in (10, 50, 60, 95)}
        s[ser] = d
    a = s["average"]
    printed = "; ".join(f"{k} {v[0]} ({v[1]})" for k, v in pr.items())
    print(f"| {fid} | {printed} | {a[10]:.3g} {a[50]:.3g} {a[60]:.3g} {a[95]:.3g} {a[60] / a[10]:.3g} | "
          f"{min(s['upper'][50], s['lower'][50]):.3g} to {max(s['upper'][50], s['lower'][50]):.3g} |")
