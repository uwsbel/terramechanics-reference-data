"""Assemble points-p<n>.csv of Figure 5-25 from the samples (sample_cl.py), the reads where the trace
overlaps a grid line or crosses one (overlap.py, crossing.py), the ink ends and the features, all read
on the page as listed below. Writes ../points-p<n>.csv (reader columns, pixels and bounds)."""
import csv
import json
import numpy as np
from trace_tools import Panel, DARK

SERIES = {1: "strut3", 2: "strut2", 3: "strut1"}
FIG = "F5-25"


def clean_cl(n):
    cl = json.load(open(f"centerline-p{n}.json"))["points"]
    return sorted([p for p in cl if p["kind"] in ("row", "col") and p["chord"] <= 14], key=lambda p: p["x"])


def interp_y(cl, y, t1, t2):
    seg = [p for p in cl if t1 <= p["x"] <= t2]
    for a, b in zip(seg, seg[1:]):
        if (a["y"] - y) * (b["y"] - y) <= 0 and a["y"] != b["y"] and b["x"] - a["x"] <= 0.0006:
            f = (y - a["y"]) / (b["y"] - a["y"])
            return a["u"] + f * (b["u"] - a["u"]), a["v"] + f * (b["v"] - a["v"])
    return None


def extremum(n, kind, t_lo, t_hi, half_w_lb):
    """Smoothed extremum of the clean center line in [t_lo, t_hi]; v bound from the flat extent."""
    cl = clean_cl(n)
    seg = [p for p in cl if t_lo <= p["x"] <= t_hi]
    ys = np.convolve([p["y"] for p in seg], np.ones(7) / 7, mode="same")
    i0, i1 = 3, len(seg) - 3
    idx = list(range(i0, i1))
    i = max(idx, key=lambda k: ys[k]) if kind == "max" else min(idx, key=lambda k: ys[k])
    flat = set(k for k in idx if abs(ys[k] - ys[i]) <= half_w_lb)
    lo = hi = i
    while lo - 1 in flat:
        lo -= 1
    while hi + 1 in flat:
        hi += 1
    vb = max(abs(seg[lo]["v"] - seg[i]["v"]), abs(seg[hi]["v"] - seg[i]["v"]))
    us = [seg[k]["u"] for k in range(max(i0, i - 3), min(i1, i + 4))]
    return float(np.mean(us)), seg[i]["v"], float(ys[i]), vb, seg[lo]["x"], seg[hi]["x"]


ROWS = {1: [], 2: [], 3: []}


BOUND_FLOOR = 2.5   # px: a single row of this binary scan shows the 5 to 6 px line as 4 to 6 px (pixel staircase)


def add(n, kind, u, v, bu, bv, note):
    bu, bv = max(bu, BOUND_FLOOR), max(bv, BOUND_FLOOR)
    ROWS[n].append({"point_kind": kind, "pixel_u": round(u, 2), "pixel_v": round(v, 2), "u_bound_px": round(bu, 1),
                    "v_bound_px": round(bv, 1), "note": note})


for n in (1, 2, 3):
    P = Panel(n)
    S = json.load(open(f"samples-p{n}.json"))["samples"]
    cl = clean_cl(n)
    wmed = float(np.median([s["w"] for s in S]))
    # ---- per-panel corrections and additions (read on the page; see notes.md) ----
    over = {}     # (by, target) -> (u, v, extra bound px, note); None removes the sample
    extra = []    # (u, v, w, note, extra bound px)
    if n == 1:
        start = (1249.0, 3523.0, 3.0, 3.0, "ink starts: the trace comes down along the 0 line into the baseline (the t = 0 line); below v 3524 its ink is lost in the baseline")
        end = (1250.5, 1819.5, 3.0, 3.0, "ink ends at the 0 line where the grid stops (t = 0.10); the trace merges with the top of the 0 line")
        for y, (u, v) in ((40.0, (1080.76, 2119.01)), (20.0, (1168.20, 1974.62))):
            extra.append((u, v, 5.5, f"5 lb sample at {y:g} lb where the center line crosses the +{y:g} line; read from the ink run with the grid line inside it", 1.0))
        for y in (10.0, 5.0):          # steep end after t = 0.095
            r = interp_y(cl, y, 0.095, 0.1002)
            if r:
                extra.append((r[0], r[1], 5.5, f"5 lb sample at {y:g} lb", 0.0))
            else:
                print(f"panel 1: {y} lb near the end not found")
    if n == 2:
        start = (1668.5, 3524.0, 3.0, 3.0, "ink starts: the trace comes down just left of the 0 line into the baseline (the t = 0 line); below v 3525 its ink is lost in the baseline")
        end = (1635.5, 1823.5, 3.0, 3.0, "ink ends at t = 0.10 (end of the record)")
        over[("time", 0.08)] = (1504.5, 2163.74, 1.0, "the trace runs along the +40 line here (t 0.077 to 0.083); center from the ink run with the grid line inside it")
        over[("time", 0.095)] = (1584.5, 1907.12, 0.0, "")
        over[("time", 0.1)] = None      # the last ink (below) is at t = 0.1000
        extra.append((1590.47, 1896.19, 6.0, "5 lb sample at 20 lb where the center line crosses the +20 line; read from the ink run with the grid line inside it", 1.0))
    if n == 3:
        start = (2285.5, 3523.0, 3.0, 3.0, "ink starts right of the 0 line (the right frame), beyond the end of the baseline: a small tension value on this panel's scale, recorded as the scale gives it (beyond the 0 line, extrapolated)")
        end = (2254.0, 1826.0, 2.5, 2.5, "ink ends on the t = 0.10 dash, 1.5 px past it")
        over[("time", 0.002)] = (2266.0, 3497.32, 1.0, "the trace crosses the right frame (the 0 line) here; center from its left edge and its width along the line of constant time")
        over[("time", 0.01)] = (1931.5, 3358.98, 1.0, "the trace lies on the -80 line here; center from its right edge and width")
        over[("time", 0.014)] = (1963.5, 3288.0, 0.5, "the drawn line has a gap at t 0.0137 to 0.0142 (v 3289 to 3297); sample moved to the ink at the gap's upper end, t = 0.0142")
        over[("time", 0.055)] = (1927.5, 2592.03, 1.0, "the trace runs along the -80 line here (t 0.053 to 0.056); center from the ink run with the grid line inside it")
        over[("time", 0.09)] = (2187.5, 1995.91, 1.0, "crossing the -20 line; center from the ink run with the grid line inside it")
        over[("time", 0.1)] = None      # the last ink (below) is 1.5 px past t = 0.10
        for y, (u, v) in ((-60.0, (2014.43, 3158.61)), (-60.0, (2014.77, 2970.06)), (-80.0, (1930.49, 2191.68))):
            extra.append((u, v, 6.0, f"5 lb sample at {y:g} lb where the center line crosses the {y:g} line; read from the ink run with the grid line inside it", 1.0))
    # ---- trace samples ----
    pts = [start]
    for s in S:
        key = (s["by"], round(s["target"], 3))
        u, v, w = s["u"], s["v"], s["w"]
        note = (f"time sample t = {s['target']:g} s" if s["by"] == "time" else f"5 lb sample at {s['target']:g} lb")
        add_b = 0.0
        if key in over:
            if over[key] is None:
                continue
            u, v, add_b, extra_note = over[key]
            note = note + ("; " + extra_note if extra_note else "")
        elif s["flag"]:
            note += "; " + s["flag"]
        pts.append((u, v, w / 2 + add_b, w / 2 + add_b, note))
    # overrides whose sample sample_cl.py could not place (no clean center line there): added here
    have = {(s["by"], round(s["target"], 3)) for s in S}
    for key, val in over.items():
        if val is not None and key not in have:
            u, v, add_b, extra_note = val
            near = sorted(S, key=lambda s: abs(s["v"] - v))[:4]
            w = float(np.median([s["w"] for s in near]))
            pts.append((u, v, w / 2 + add_b, w / 2 + add_b, f"time sample t = {key[1]:g} s; " + extra_note))
    for u, v, w, note, add_b in extra:
        pts.append((u, v, w / 2 + add_b, w / 2 + add_b, note))
    pts.append(end)
    pts.sort(key=lambda p: P.xy(p[0], p[1])[0])      # drawing order: each trace is a function of time
    for u, v, bu, bv, note in pts:
        add(n, "trace", u, v, bu, bv, note)
    # ---- features ----
    hw = wmed / 2
    lbpx = P.cal["y_per_px"]
    feats = [(start[0], start[1], start[2], start[3], "first: " + start[4])]
    if n == 1:
        feats.append((1244.0, 3495.0, 3.0, 3.0, "knee: the trace leaves the 0 line and the load starts to rise (t about 0.0018 s)"))
        ext = [("max", 0.008, 0.024, "peak: first load maximum"),
               ("min", 0.024, 0.040, "knee, minimum: local minimum between the two maxima, a flat stretch"),
               ("max", 0.045, 0.068, "peak: largest load of the record, a broad top")]
    if n == 2:
        feats.append((1662.7, 3455.5, 3.0, 3.0, "knee: the trace leaves the 0 line and the load starts to rise (t about 0.0043 s)"))
        feats.append((1491.6, 3353.5, 3.0, 3.0, "knee: end of the steep rise (t about 0.0102 s)"))
        ext = [("max", 0.012, 0.028, "peak: first load maximum, a broad top"),
               ("min", 0.026, 0.042, "knee, minimum: local minimum between the two maxima, a flat stretch"),
               ("max", 0.045, 0.068, "peak: largest load of the record, a broad top")]
    if n == 3:
        feats.append((2268.5, 3496.0, 4.0, 4.0, "knee: the trace bends where it crosses the right frame (the 0 line); bend point from the two straight stretches, hidden by the frame's ink"))
        feats.append((1929.5, 3365.0, 3.5, 6.0, "knee, minimum: largest compression of the first impact, the most negative value on the printed scale; the trace lies on the -80 line, center from its right edge and width; flat over v 3360 to 3372"))
        ext = [("max", 0.018, 0.036, "peak: local maximum of the recorded value (least compression between the two compression maxima)"),
               ("min", 0.058, 0.078, "knee, minimum: largest compression of the record, the most negative value on the printed scale, a broad extreme")]
    for kind, t1, t2, note in ext:
        u, v, y, vb, xa, xb = extremum(n, kind, t1, t2, hw * lbpx)
        feats.append((u, v, hw, max(hw, vb), note + f" (within half a line width of the extreme from t = {xa:.4f} to {xb:.4f} s)"))
    feats.append((end[0], end[1], end[2], end[3], "last: " + end[4]))
    feats.sort(key=lambda p: P.xy(p[0], p[1])[0])
    for u, v, bu, bv, note in feats:
        add(n, "feature", u, v, bu, bv, note)
    # ---- write ----
    seqs = {"trace": 0, "feature": 0}
    with open(f"../points-p{n}.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v",
                                          "u_bound_px", "v_bound_px", "symbol", "note"], lineterminator="\n")
        w.writeheader()
        for r in ROWS[n]:
            seqs[r["point_kind"]] += 1
            ui, vi = int(round(r["pixel_u"])), int(round(r["pixel_v"]))
            if not DARK[vi - 2:vi + 3, ui - 2:ui + 3].any():
                print(f"WARNING panel {n} {r['point_kind']} {seqs[r['point_kind']]}: no ink within 2 px")
            w.writerow({"figure_id": FIG, "panel": n, "series_id": SERIES[n], "point_kind": r["point_kind"],
                        "sequence": seqs[r["point_kind"]], "pixel_u": r["pixel_u"], "pixel_v": r["pixel_v"],
                        "u_bound_px": r["u_bound_px"], "v_bound_px": r["v_bound_px"], "symbol": "", "note": r["note"]})
    print(f"panel {n}: {seqs['trace']} trace, {seqs['feature']} feature; median width {wmed:.1f} px")
