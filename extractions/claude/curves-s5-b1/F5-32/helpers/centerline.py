"""Centre line of the recorded trace of one panel of Figure 5-32, row by row (the time axis runs along v,
so each page row crosses the trace once). Writes centerline-p<n>.csv: v, u_center, run_width, flag.

In each row the dark runs between u_lo and u_hi are found. A run of 5 px or less centred within 2 px of a
load line is the grid line and is left out. A run that holds a load line at one of its edges (within
2.5 px) and is 7 px wide or more is the trace touching the line: the line's 3 px are trimmed from that edge
(flag `trimmed`). Where no other run is left near the expected place, the trace lies on the grid line and
the merged run is used whole (flag `merged`, the bound widened later). The run nearest the position
predicted from the previous rows is the trace.

usage: centerline.py <page.png> <grid_measured.json> <panel> <u_lo> <u_hi> <v_start> <v_end> <u_start> <out.csv>
"""
import csv
import json
import sys

import numpy as np
from PIL import Image


def runs(idx):
    out = []
    if len(idx) == 0:
        return out
    s = p = int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i != p + 1:
            out.append([s, p])
            s = i
        p = i
    out.append([s, p])
    return out


def main():
    page, gm, pn, u_lo, u_hi, v_start, v_end, u_start, out = sys.argv[1:10]
    pn, u_lo, u_hi, v_start, v_end, u_start = int(pn), int(u_lo), int(u_hi), int(v_start), int(v_end), float(u_start)
    g = np.asarray(Image.open(page).convert("L")) < 128
    G = json.load(open(gm, encoding="utf-8"))
    lines = G["load_lines"][str(pn)]
    rows = []
    hist = [(v_start + 1, u_start), (v_start, u_start)]
    step = -1 if v_end < v_start else 1
    for v in range(v_start, v_end + step, step):
        gl = [l["u_at_v0"] + l["slope_du_dv"] * v for l in lines]
        rr = [[u_lo + a, u_lo + b] for a, b in runs(np.where(g[v, u_lo:u_hi + 1])[0])]
        cands = []
        grid_runs = []
        for a, b in rr:
            w = b - a + 1
            c = (a + b) / 2
            near = [x for x in gl if a - 1 <= x <= b + 1]
            if w <= 5 and near and min(abs(c - x) for x in near) <= 2:
                grid_runs.append((c, w, a, b))
                continue
            flag = ""
            if near and w >= 7:
                for x in near:
                    if x - a <= 2.5:
                        a = int(np.ceil(x + 1.5)); flag = "trimmed"
                    elif b - x <= 2.5:
                        b = int(np.floor(x - 1.5)); flag = "trimmed"
            cands.append(((a + b) / 2, b - a + 1, flag))
        # prediction from the last rows
        (v1, u1), (v2, u2) = hist[-1], hist[-2]
        pred = u1 + (u1 - u2) * (v - v1) / (v1 - v2) if v1 != v2 else u1
        best = None
        for c, w, f in cands:
            d = abs(c - pred)
            if best is None or d < best[0]:
                best = (d, c, w, f)
        if best is None or best[0] > 12:
            # the trace on a grid line: the merged run nearest the prediction
            for c, w, a, b in grid_runs:
                d = abs(c - pred)
                if d <= 6 and (best is None or d < best[0] or best[0] > 12):
                    best = (d, c, w, "merged")
        if best is None or best[0] > 25:
            rows.append((v, "", "", "gap"))
            continue
        _, c, w, f = best
        rows.append((v, c, w, f))
        hist.append((v, c))
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["v", "u_center", "run_width", "flag"])
        w.writerows(rows)
    flags = [r[3] for r in rows]
    print(f"panel {pn}: {len(rows)} rows; gap {flags.count('gap')}, merged {flags.count('merged')}, trimmed {flags.count('trimmed')}")


if __name__ == "__main__":
    main()
