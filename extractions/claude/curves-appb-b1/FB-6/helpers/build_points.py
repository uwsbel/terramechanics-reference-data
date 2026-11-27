"""Assemble out/FB-6/points-p1.csv (pixels) from markers.json, lines.json and the calibration:
markers, trace samples (left end, every 1 psi, vertex, every 1 psi, right end, in drawing order),
features (first point, vertex, last point, label)."""
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

W = Path(sys.argv[1])
sys.path.insert(0, str(W / "tools"))
import calibrate_axes as ca  # noqa: E402

img = W / "packet" / "p0112.png"
dark = np.asarray(Image.open(img).convert("L")) < 128
cal, X, Y = ca.piecewise_maps(str(W / "out" / "FB-6" / "cal-p1"), str(img))
H = W / "out" / "FB-6" / "helpers"
M = json.loads((H / "markers.json").read_text(encoding="utf-8"))
L = json.loads((H / "lines.json").read_text(encoding="utf-8"))
R_OUT = 20.6
centre = {m["id"]: (m["u"], m["v"]) for m in M}

MARKER_NOTES = {
    "d1": ("", 2.0, 2.0),
    "d2": ("", 2.0, 2.0),
    "d3": ("", 2.0, 2.0),
    "d4": ("", 2.0, 2.0),
    "d5": ("", 2.0, 2.0),
    "d6": ("the dense line runs along the right side of this circle's ring and merges with it", 2.5, 2.5),
    "d7": ("the dense line is drawn up to this circle's ring from above and below; no line ink inside its hole", 2.0, 2.0),
    "l1": ("the loose line crosses the right side of this circle's ring", 2.5, 2.5),
    "l2": ("sits on the bottom frame line; the x = 2 tick shows inside its hole; the loose line ends on its ring", 3.0, 3.0),
    "l3": ("", 2.0, 2.0),
    "l4": ("", 2.0, 2.0),
    "l5a": ("upper of two overlapping circles (centres about 16 px apart, told apart by three white areas: the upper hole, the shared part of both holes, the lower hole)", 2.5, 3.0),
    "l5b": ("lower of two overlapping circles; the loose line ends on its ring", 2.5, 3.0),
}

LABELS = {"dr82": ((2191.5, 1110.5), "label: Dense Dr = 0.82"), "dr02": ((2172.5, 2693.5), "label: Loose Dr = 0.02")}

# where each line's ink starts and ends (pixels) and how it ends
ENDS = {
    "dr82": {"first": "free end", "last": "free end"},
    "dr02": {"first": ("ring", "l2"), "last": ("ring", "l5b")},
}

rows = []


def add(series, kind, seq, u, v, bu, bv, symbol, note):
    rows.append({"figure_id": "FB-6", "panel": 1, "series_id": series, "point_kind": kind, "sequence": seq,
                 "pixel_u": round(u, 1), "pixel_v": round(v, 1), "u_bound_px": bu, "v_bound_px": bv,
                 "symbol": symbol, "note": note})


def xval(u, v):
    return X.value(u, v)[0]


# markers, numbered left to right within each series
for sid in ("dr82", "dr02"):
    ms = sorted([m for m in M if m["series_id"] == sid], key=lambda m: (xval(m["u"], m["v"]), -m["v"]))
    for i, m in enumerate(ms, 1):
        note, bu, bv = MARKER_NOTES[m["id"]]
        add(sid, "marker", i, m["u"], m["v"], bu, bv, "circle", note)


def runs(row):
    idx = np.where(row)[0]
    return np.split(idx, np.where(np.diff(idx) != 1)[0] + 1) if len(idx) else []


def ink_u(v, u_pred, half=6):
    """centre of the dark run in row v nearest u_pred (the line's ink at that row)"""
    lo = int(round(u_pred - half))
    rs = runs(dark[int(round(v)), lo:lo + 2 * half + 1])
    if not rs:
        return None
    r = min(rs, key=lambda r: abs(lo + (r[0] + r[-1]) / 2 - u_pred))
    return lo + (r[0] + r[-1]) / 2


def outermost(v_start, seg, step):
    """the outermost row of a free line end: from v_start, step outward while the row still has ink
    within 6 px of the previous row's ink centre"""
    v, uc = v_start, ink_u(v_start, seg["a"] + seg["b"] * v_start)
    while True:
        nxt = ink_u(v + step, uc)
        if nxt is None:
            return v
        v, uc = v + step, nxt


def on_ring_end(seg, mid):
    """the point on the segment's centre line at the ring's outer radius from the circle's centre,
    on the line's side of the circle"""
    a, b = seg["a"], seg["b"]
    cu, cv = centre[mid]
    # (a + b v - cu)^2 + (v - cv)^2 = R^2
    A = b * b + 1
    B = 2 * b * (a - cu) - 2 * cv
    C = (a - cu) ** 2 + cv * cv - R_OUT ** 2
    disc = math.sqrt(B * B - 4 * A * C)
    return [(a + b * v, v) for v in ((-B - disc) / (2 * A), (-B + disc) / (2 * A))]


for sid in ("dr82", "dr02"):
    info = L[sid]
    lower, upper = info["segs"]
    uv, vv = info["vertex"]
    bl, bu_ = round(lower["thick"] / 2, 1), round(upper["thick"] / 2, 1)
    # first point (left, lower end)
    if ENDS[sid]["first"] == "free end":
        v_out = outermost(info["v_end_lo"], lower, +1)
        v0 = v_out - 1.5                       # 1.5 px inside the outermost ink row
        u0 = ink_u(v0, lower["a"] + lower["b"] * v0)
        first_note = "first point: the line's free lower end (where its ink stops)"
        fb = (bl, bl)
    else:
        mid = ENDS[sid]["first"][1]
        cands = on_ring_end(lower, mid)
        u0, v0 = min(cands, key=lambda p: p[1])      # the crossing on the upper side of the ring
        first_note = f"first point: the line's ink runs into the ring of the circle at ({centre[mid][0]:.0f}, {centre[mid][1]:.0f}); taken on the line's centre where it meets the ring's outer edge"
        fb = (bl, bl + 1.0)
    if ENDS[sid]["last"] == "free end":
        v_out = outermost(info["v_end_hi"], upper, -1)
        v1 = v_out + 1.5
        u1 = ink_u(v1, upper["a"] + upper["b"] * v1)
        last_note = "last point: the line's free upper end (where its ink stops); also the trace's maximum"
        lb = (bu_, bu_)
    else:
        mid = ENDS[sid]["last"][1]
        cands = on_ring_end(upper, mid)
        u1, v1 = max(cands, key=lambda p: p[1])      # the crossing on the lower side of the ring
        last_note = f"last point: the line's ink runs into the ring of the circle at ({centre[mid][0]:.0f}, {centre[mid][1]:.0f}); taken on the line's centre where it meets the ring's outer edge; also the trace's maximum"
        lb = (bu_, bu_ + 1.0)
    x0, xv, x1 = xval(u0, v0), xval(uv, vv), xval(u1, v1)
    seq = 0
    trace = []

    def sample(seg, xt):
        # v on the segment's fitted centre line where the piecewise x equals xt (bisection), then onto the ink
        a, b = seg["a"], seg["b"]
        lo_v, hi_v = 900.0, 4100.0
        f = lambda v: xval(a + b * v, v) - xt
        for _ in range(60):
            mid = (lo_v + hi_v) / 2
            if (f(lo_v) > 0) == (f(mid) > 0):
                lo_v = mid
            else:
                hi_v = mid
        v = round((lo_v + hi_v) / 2)
        u = ink_u(v, a + b * v)
        return u, v

    trace.append((u0, v0, fb, first_note.split(":")[0] + " (left end)"))
    for xt in range(math.floor(x0) + 1, math.ceil(xv)):
        u, v = sample(lower, xt)
        trace.append((u, v, (bl, bl), f"at sigma3 = {xt} psi"))
    vin = ink_u(vv, uv)
    trace.append((uv, vv, (bl, bl), "vertex (intersection of the two fitted straight segments; ink centre in that row %.1f)" % vin))
    for xt in range(math.floor(xv) + 1, math.ceil(x1)):
        u, v = sample(upper, xt)
        trace.append((u, v, (bu_, bu_), f"at sigma3 = {xt} psi"))
    trace.append((u1, v1, lb, "last point (right end)"))
    for i, (u, v, (b1, b2), note) in enumerate(trace, 1):
        mind = min(math.hypot(u - a, v - b) for a, b in centre.values())
        if mind < 23 and "point" not in note:
            note += f"; {mind:.0f} px from a circle's centre"
        add(sid, "trace", i, u, v, b1, b2, "", note)
    add(sid, "feature", 1, u0, v0, fb[0], fb[1], "", first_note)
    add(sid, "feature", 2, uv, vv, bl, bl, "", "vertex")
    add(sid, "feature", 3, u1, v1, lb[0], lb[1], "", last_note)
    (lu, lv), ltext = LABELS[sid]
    add(sid, "feature", 4, lu, lv, 8.0, 8.0, "", ltext)

out = W / "out" / "FB-6" / "points-p1.csv"
with out.open("w", encoding="utf-8", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    wr.writeheader()
    wr.writerows(rows)
print(f"wrote {out}: {len(rows)} rows")
for r in rows:
    print(r["series_id"], r["point_kind"], r["sequence"], r["pixel_u"], r["pixel_v"], r["u_bound_px"], r["v_bound_px"], r["note"][:90])
