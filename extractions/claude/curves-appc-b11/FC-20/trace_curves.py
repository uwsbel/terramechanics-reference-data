"""Follow each drawn curve of FC-20 column by column on the page (reader's helper).

For every column u from a curve's left end to its right end, the dark runs (gray < 128) within
+-WIN px of the predicted v are listed; the run nearest the prediction is the curve's ink in that
column, its center the line's centerline there. The prediction is a straight line fitted to the
last 30 accepted centers (runs of 4 px or more, no flag). Columns within 7 px of a vertical grid line (whose ink fills the column)
are skipped, a run touching a horizontal grid line (within 6 px of its center) or a circle ring is
flagged, and a column without ink near the prediction is a gap. Writes trace-<curve>.csv (u, v,
run, status) and prints the stretches of ink (dashes) and the gaps between them.

Pixel coordinates refer to the unrotated 300 dpi page image.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
img = np.asarray(Image.open(sys.argv[1]).convert("L"))
cal = json.loads((HERE / "cal-p1" / "calibration.json").read_text(encoding="utf-8"))
VL = [(l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
HL = [(l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
# the frame and the unlabelled lines outside the labelled grid are not crossed by the curves
CIRCLES = [(825.3, 3228.9), (827.5, 3280.5), (1009.2, 3280.3), (1264.1, 2964.0), (1531.4, 2671.5),
           (1994.2, 2318.4), (2341.2, 2320.9)]
R_OUT = 19.0
WIN = 9

# restart points: at column u the prediction restarts from (u, v) read on the crops (the last dash
# of the upper curve lies 7 px above the line extrapolated from the dash before it)
RESEED = {"upper": {2284: 2174.0}}

# curve: (left end u, v), right end u
CURVES = {
    "mean": ((798.5, 3266.5), 2326),
    "upper": ((800.0, 3171.0), 2345),
    "lower": ((805.0, 3382.0), 2350),
}


def near_vgrid(u, v):
    return any(abs(u - (a + b * v)) <= 7 for a, b in VL)


def near_hgrid(u, v0, v1):
    for a, b in HL:
        vh = a + b * u
        if v0 - 6 <= vh <= v1 + 6:
            return True
    return False


def near_circle(u, v0, v1):
    for cu, cv in CIRCLES:
        dv = max(v0 - cv, 0, cv - v1)
        if np.hypot(u - cu, dv) <= R_OUT + 1:
            return True
    return False


def runs(col, off):
    idx = np.where(col)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            out.append((s + off, p + off))
            s = i
        p = i
    out.append((s + off, p + off))
    return out


def trace(name, start, u_end):
    u0, v0 = start
    acc = [(u0, v0)]
    rows = []
    for u in range(int(round(u0)), u_end + 1):
        if u in RESEED.get(name, {}):
            acc = [(u, RESEED[name][u])]
        P = np.array(acc[-30:])
        if len(P) >= 4 and np.ptp(P[:, 0]) > 2:
            k, c = np.polyfit(P[:, 0], P[:, 1], 1)
            pred = k * u + c
        else:
            pred = acc[-1][1]
        if near_vgrid(u, pred):
            rows.append((u, "", "", "vgrid"))
            continue
        lo, hi = int(pred - WIN - 30), int(pred + WIN + 30)
        col = img[lo:hi, u] < 128
        cand = [(a, b) for a, b in runs(col, lo) if not (b < pred - WIN or a > pred + WIN)]
        if not cand:
            rows.append((u, "", "", "gap"))
            continue
        a, b = min(cand, key=lambda r: abs((r[0] + r[1]) / 2 - pred))
        c = (a + b) / 2
        flags = []
        if near_hgrid(u, a, b):
            flags.append("hgrid")
        if near_circle(u, a, b):
            flags.append("circle")
        if b - a + 1 > 30:
            flags.append("long")
        if b - a + 1 < 4:
            flags.append("thin")   # the tip of a dash or a speck: recorded, not used for the prediction
        rows.append((u, c, b - a + 1, "+".join(flags) or "ink"))
        if not flags:
            acc.append((u, c))
    with (HERE / f"trace-{name}.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["u", "v", "run", "status"])
        w.writerows(rows)
    # stretches: consecutive columns with ink (any flag), vgrid columns bridged when ink on both sides
    seg, segs = None, []
    for u, v, r, st in rows:
        if st == "gap":
            if seg:
                segs.append(seg)
                seg = None
        elif st == "vgrid":
            continue
        else:
            if seg is None:
                seg = [u, u]
            seg[1] = u
    if seg:
        segs.append(seg)
    print(f"{name}: {len(segs)} stretches of ink")
    for s in segs:
        print(f"   u {s[0]}..{s[1]}")


for name, (start, u_end) in CURVES.items():
    if len(sys.argv) > 2 and name not in sys.argv[2:]:
        continue
    trace(name, start, u_end)
