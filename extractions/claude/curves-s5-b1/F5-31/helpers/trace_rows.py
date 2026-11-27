"""Row-by-row extraction of the single drawn line of Figure 5-31 (reader helper).

The figure is printed sideways: time increases up the page (v decreasing) and depth increases to the
left (u decreasing). The trace is single valued in time, so every pixel row v crosses it once. For each
row the dark run nearest the tracked position is taken; a row is `clean` when that run is clear of every
grid line band (the curve's own ink, not merged with a grid line or the frame). Writes rows.csv:
v, left, right, center, width, clean, why.
"""
import csv, json, sys
from pathlib import Path
import numpy as np
from PIL import Image

ws = Path(__file__).resolve().parents[3]
img = np.asarray(Image.open(ws / "packet" / "p0336.png").convert("L")) < 128
cal = json.loads((ws / "out" / "F5-31" / "cal-p1" / "calibration.json").read_text())
VL = [(l["y_value"], l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
HL = [(l["x_value"], l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
GL_HALF = 4.5      # half thickness of a grid line (6 to 7 px measured) plus half a pixel
FRAME_HALF = 6.0   # the bottom frame is about 10 px thick


def runs(row):
    idx = np.where(row)[0]
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append((int(s), int(p)))
            s = i
        p = i
    out.append((int(s), int(p)))
    return out


def vline_u(v):
    return [(val, u0 + k * v) for val, u0, k in VL]


def hline_v(u):
    return [(val, v0 + k * u) for val, v0, k in HL]


rows = []
pred_hist = []
u_pred = 1937.0   # near the start, from the crop of the lower right corner
for v in range(3500, 1060, -1):
    rr = runs(img[v, 640:2175])
    rr = [(a + 640, b + 640) for a, b in rr]
    # drop runs that are a vertical grid line alone
    vls = vline_u(v)
    cand = []
    for a, b in rr:
        pure_grid = any(a >= uc - GL_HALF - 1 and b <= uc + GL_HALF + 1 for _, uc in vls)
        if not pure_grid:
            cand.append((a, b))
    if len(pred_hist) >= 6:
        P = np.array(pred_hist[-12:])
        k, c = np.polyfit(P[:, 0], P[:, 1], 1)
        u_pred = k * v + c
    if not cand:
        rows.append([v, "", "", "", "", 0, "no candidate run"])
        continue
    a, b = min(cand, key=lambda r: abs((r[0] + r[1]) / 2 - u_pred) if r[1] - r[0] < 60 else 1e9)
    whys = []
    if b - a >= 60:
        whys.append("row on a horizontal line")
    for val, uc in vls:
        if a <= uc + GL_HALF and b >= uc - GL_HALF:
            whys.append(f"touches depth line {val:g}")
    center = (a + b) / 2
    for val, vc in hline_v(center):
        half = FRAME_HALF if val == 0.0 else GL_HALF   # the top frame is 8 px thick, like a grid line; the bottom one 10
        if abs(v - vc) <= half + 4:   # +4: the curve's own half width, so the run is the curve's ink alone
            whys.append(f"within the band of time line {val:g}")
    clean = int(not whys)
    if abs(center - u_pred) > 15 and len(pred_hist) >= 6:
        whys.append(f"far from prediction {u_pred:.1f}")
        clean = 0
    rows.append([v, a, b, center, b - a + 1, clean, "; ".join(whys)])
    if clean:
        pred_hist.append((v, center))

out = ws / "out" / "F5-31" / "helpers" / "rows.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["v", "left", "right", "center", "width", "clean", "why"])
    w.writerows(rows)
n_clean = sum(r[5] for r in rows)
print(f"wrote {out}: {len(rows)} rows, {n_clean} clean")
