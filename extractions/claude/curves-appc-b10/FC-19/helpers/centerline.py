"""Per-column centerlines of the three curves of Fig. C-19 (FC-19), for the Claude reader.

For each curve a rough guide polyline (read by eye from crops) gives the expected v at each column u;
in each column the dark runs within +-WIN px of the guide, after masking the grid lines of the
calibration (cal-p1), are found and the run nearest the guide is kept. Columns where the curve's run
touches a masked grid line are flagged (the curve's ink there is merged with the grid line's).
Writes centerline-<curve>.csv: u, v_center, run_px, flag.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]          # the workspace (packet/, tools/, out/)
IMG = ROOT / "packet" / "p0155.png"
CAL = HERE.parent / "cal-p1" / "calibration.json"
DARK = 160
WIN = 22
VMASK = 5      # half width of the mask around a vertical grid line's center, px
HMASK = 4      # around a horizontal grid line's center

GUIDES = {
    "mean": [(986, 2219), (1115, 2190), (1270, 2125), (1405, 2055), (1580, 1955), (1730, 1863),
             (1895, 1763), (2050, 1668), (2200, 1582), (2355, 1505), (2512, 1437)],
    "upper": [(962, 2118), (1102, 2075), (1170, 2048), (1315, 1986), (1368, 1960), (1520, 1880),
              (1563, 1857), (1728, 1768), (1790, 1733), (1928, 1650), (1978, 1622), (2130, 1535),
              (2175, 1510), (2322, 1435), (2380, 1408), (2518, 1360)],
    "lower": [(966, 2324), (1146, 2268), (1197, 2248), (1353, 2180), (1400, 2157), (1570, 2070),
              (1644, 2033), (1810, 1943), (1870, 1908), (1990, 1835), (2035, 1808), (2165, 1730),
              (2215, 1702), (2345, 1623), (2380, 1605), (2525, 1528)],
}


def runs(mask):
    idx = np.where(mask)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i != p + 1:
            out.append((s, p))
            s = i
        p = i
    out.append((s, p))
    return out


def main():
    g = np.asarray(Image.open(IMG).convert("L"))
    dark = g < DARK
    cal = json.loads(CAL.read_text(encoding="utf-8"))
    vl = [(l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
    hl = [(l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
    for name, guide in GUIDES.items():
        gu = np.array([p[0] for p in guide], float)
        gv = np.array([p[1] for p in guide], float)
        rows = []
        for u in range(int(gu[0]) - 15, int(gu[-1]) + 15):
            vg = float(np.interp(u, gu, gv))
            v0, v1 = int(vg - WIN), int(vg + WIN) + 1
            col = dark[v0:v1, u].copy()
            # grid masks in this column
            masked = np.zeros_like(col)
            for (a, b) in vl:
                for k, v in enumerate(range(v0, v1)):
                    if abs(u - (a + b * v)) <= VMASK:
                        masked[k] = True
            for (c, d) in hl:
                vc = c + d * u
                for k, v in enumerate(range(v0, v1)):
                    if abs(v - vc) <= HMASK:
                        masked[k] = True
            if masked.all():
                rows.append({"u": u, "v_center": "", "run_px": "", "flag": "vertical-grid"})
                continue
            rr = runs(col & ~masked)
            if not rr:
                rows.append({"u": u, "v_center": "", "run_px": "", "flag": "no-ink"})
                continue
            best = min(rr, key=lambda r: abs((r[0] + r[1]) / 2 + v0 - vg))
            s, e = best
            flag = ""
            if (s > 0 and masked[s - 1]) or (e < len(col) - 1 and masked[e + 1]):
                flag = "touches-grid"
            if masked.any() and any(masked[max(0, s - 1):e + 2]):
                flag = flag or "touches-grid"
            rows.append({"u": u, "v_center": round((s + e) / 2 + v0, 2), "run_px": e - s + 1, "flag": flag})
        out = HERE / f"centerline-{name}.csv"
        with out.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["u", "v_center", "run_px", "flag"], lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {out.name}: {len(rows)} columns")


if __name__ == "__main__":
    sys.exit(main())
