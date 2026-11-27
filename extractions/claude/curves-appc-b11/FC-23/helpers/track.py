"""Follow one drawn curve column by column on the page image (FC-23 reading helper, Claude reader).

A curve is seeded by the reader at a point on its ink with its local slope (dv/du). The tracker steps
one column at a time in both directions, predicts the line's position from a straight-line fit to the
last measured stretch, and in each column takes the dark run whose centre is nearest the prediction.
Each column gets a status:
    ink     a clean run of curve ink: centre and thickness measured
    grid    the column is on a vertical grid line or the frame: not measured
    hgrid   the curve is crossing a horizontal grid line here: ink present, not measured
    merged  a run much thicker than the line (another curve touching): ink present, not measured
    gap     no ink near the prediction (a gap between dashes)
The track stops when the gap exceeds max_gap columns. Output: JSON with the per-column records.
Nothing here decides identity: the reader seeds each curve and checks the overlay by eye.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CAL = json.loads((HERE.parent / "cal-p1" / "calibration.json").read_text(encoding="utf-8"))
VLINES = [(l["u_at_v0"], l["slope_du_dv"]) for l in CAL["vertical_lines"]]
HLINES = [(l["v_at_u0"], l["slope_dv_du"]) for l in CAL["horizontal_lines"]]
# frame lines (not labelled; only used to stop the tracker), measured from scans
VLINES_FRAME = [(791.0 - 0.0075 * 2450, 0.0075), (2660.0 - 0.0075 * 1630, 0.0075)]


def runs(col, lo, hi):
    out = []
    i = lo
    while i < hi:
        if col[i]:
            j = i
            while j + 1 < hi and col[j + 1]:
                j += 1
            out.append((i, j))
            i = j + 1
        else:
            i += 1
    return out


def track(dark, seed_u, seed_v, slope, max_gap=60, win=14, fit_len=40, thick0=9.0, stop_u=None):
    h, w = dark.shape
    recs = {}
    for direction in (+1, -1):
        hist = [(seed_u, seed_v)]
        u = seed_u
        s = slope
        gap = 0
        while True:
            u += direction
            if u < 5 or u > w - 5:
                break
            if stop_u and (u < stop_u[0] or u > stop_u[1]):
                break
            # prediction from the recent stretch
            pts = [p for p in hist if abs(p[0] - u) <= fit_len]
            if len(pts) >= 6 and np.ptp([p[0] for p in pts]) >= 5:
                c1, c0 = np.polyfit([p[0] for p in pts], [p[1] for p in pts], 1)
                vp = c0 + c1 * u
            else:
                last = hist[-1]
                vp = last[1] + s * (u - last[0])
            on_grid = any(abs(u - (a + b * vp)) <= 6 for a, b in VLINES + VLINES_FRAME)
            near_h = any(abs(vp - (c + d * u)) <= 9 for c, d in HLINES)
            col = dark[:, u]
            rr = runs(col, int(vp - win), int(vp + win) + 1)
            # a run touching the window edge may continue beyond: extend it
            best = None
            for a, b in rr:
                while a > 0 and col[a - 1]:
                    a -= 1
                while b < h - 1 and col[b + 1]:
                    b += 1
                c = 0.5 * (a + b)
                d = abs(c - vp)
                if best is None or d < best[0]:
                    best = (d, a, b, c)
            if on_grid:
                recs[u] = {"u": u, "status": "grid", "vp": round(float(vp), 1)}
                gap = 0 if best and best[0] < 8 else gap
                continue
            if best is None or (best[0] > 7 and not (best[1] - 3 <= vp <= best[2] + 3)):
                gap += 1
                recs[u] = {"u": u, "status": "gap", "vp": round(float(vp), 1)}
                if gap > max_gap:
                    break
                continue
            d, a, b, c = best
            th = b - a + 1
            if near_h:
                recs[u] = {"u": u, "status": "hgrid", "vp": round(float(vp), 1), "run": [a, b]}
                gap = 0
                continue
            if th > 1.7 * thick0 / max(0.3, np.cos(np.arctan(s))) + 2:
                recs[u] = {"u": u, "status": "merged", "vp": round(float(vp), 1), "run": [a, b]}
                gap = 0
                continue
            gap = 0
            recs[u] = {"u": u, "status": "ink", "v": float(c), "run": [a, b], "thick": int(th), "vp": round(float(vp), 1)}
            hist.append((u, float(c)))
            if len(hist) > 200:
                hist = hist[-200:]
    # trim trailing gaps at both ends
    us = sorted(recs)
    ink_us = [u for u in us if recs[u]["status"] in ("ink", "hgrid", "merged")]
    lo, hi = min(ink_us), max(ink_us)
    return [recs[u] for u in us if lo <= u <= hi]


if __name__ == "__main__":
    img, name, su, sv, sl = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    max_gap = int(sys.argv[6]) if len(sys.argv) > 6 else 60
    stop = (int(sys.argv[7]), int(sys.argv[8])) if len(sys.argv) > 8 else None
    g = np.asarray(Image.open(img).convert("L"))
    dark = g < 150
    recs = track(dark, su, sv, sl, max_gap=max_gap, stop_u=stop)
    out = HERE.parent / "tracks" / f"{name}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(recs), encoding="utf-8")
    st = {}
    for r in recs:
        st[r["status"]] = st.get(r["status"], 0) + 1
    ink = [r for r in recs if r["status"] == "ink"]
    print(name, "u", recs[0]["u"], "to", recs[-1]["u"], st, "first ink", (ink[0]["u"], round(ink[0]["v"], 1)), "last ink", (ink[-1]["u"], round(ink[-1]["v"], 1)),
          "median thick", np.median([r["thick"] for r in ink]))
