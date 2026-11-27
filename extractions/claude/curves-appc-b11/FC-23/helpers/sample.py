"""Trace samples of the FC-23 curves from the guided column measurements (Claude reader's helper).

For each curve: its left end, a sample at every 0.05 of Dr (the page u where the piecewise x value
equals the target, at the curve's height), its right end. In drawing order. At a sample column:
    on the curve's ink                      the measured centre (median of the columns u-1..u+1)
    on a vertical grid line, ink both sides the straight line through the ink columns within 15 px
                                            either side, evaluated at u (the curve crosses the line)
    in a gap between dashes                 moved to the nearest dash end, on the ink (rule 7)
Overrides (reader's decisions from the column runs, see notes.md) mark columns where a curve's
guide runs through another curve's ink while the curve itself is in a gap.
Writes samples/<name>.json with u, v, bounds and a note per sample.
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
CAL = json.loads((OUT / "cal-p1" / "calibration.json").read_text(encoding="utf-8"))
VL = sorted([(l["x_value"], l["u_at_v0"], l["slope_du_dv"]) for l in CAL["vertical_lines"]])
INKY = ("ink", "top-edge", "bottom-edge", "coincident", "mid-merge", "thick")
# columns where the curve is in a gap although a run of another curve lies on its guide
GAP_OVERRIDE = {"rs": [(1835, 1865), (2396, 2416)]}


def u_of_x(x, v):
    """Page u where Dr = x at height v: linear between the two bracketing vertical lines (extrapolated
    from the outer pair beyond 0 or 1.0)."""
    xs = [l[0] for l in VL]
    us = [l[1] + l[2] * v for l in VL]
    k = int(np.clip(np.searchsorted(xs, x) - 1, 0, len(xs) - 2))
    return us[k] + (x - xs[k]) / (xs[k + 1] - xs[k]) * (us[k + 1] - us[k])


def load(name):
    recs = json.loads((OUT / "tracks" / f"{name}_m.json").read_text())
    for a, b in GAP_OVERRIDE.get(name, []):
        for r in recs:
            if a <= r["u"] <= b and r["status"] in INKY + ("other",):
                r["status"] = "gap"
                r["overridden"] = True
                r.pop("v", None)
    return {r["u"]: r for r in recs}


def fitline(pts, u):
    p = np.array(pts, dtype=float)
    if len(p) >= 2 and np.ptp(p[:, 0]) > 0:
        c1, c0 = np.polyfit(p[:, 0], p[:, 1], 1)
        return float(c0 + c1 * u)
    return float(p[:, 1].mean())


def dash_end_point(R, ue, direction):
    """v at the dash end column ue from a line through the dash's ink columns within 10 px inward
    (direction: +1 when the dash lies to the left of ue, -1 when it lies to the right), and the
    bound: half the line's vertical thickness over those columns (the cap itself is thinner)."""
    cols = [u for u in range(ue, ue - direction * 11, -direction) if u in R and R[u]["status"] in INKY]
    pts = [(u, R[u]["v"]) for u in cols]
    vb = float(np.median([R[u]["vb"] for u in cols]))
    return fitline(pts, ue), max(vb, R[ue]["tv"] / 2)


def thick_enough(R, u):
    r = R[u]
    return r["status"] in INKY and (r["run"][1] - r["run"][0] + 1) >= 4


def sample_at(R, u_target, ends):
    u0 = int(round(u_target))
    r = R.get(u0)
    lo, hi = ends
    if r is None:
        return None
    st = r["status"]
    if st in INKY:
        pts = [(u, R[u]["v"]) for u in (u0 - 1, u0, u0 + 1) if u in R and R[u]["status"] == st]
        v = float(np.median([p[1] for p in pts]))
        return {"u": u0, "v": v, "vb": r["vb"], "how": st, "near": r.get("near", [])}
    if st == "grid":
        # ink columns either side of the grid line
        left = [u for u in range(u0 - 1, u0 - 25, -1) if u in R and R[u]["status"] != "grid"]
        right = [u for u in range(u0 + 1, u0 + 25) if u in R and R[u]["status"] != "grid"]
        gl, gr = (left[0] if left else None), (right[0] if right else None)
        okl = gl is not None and R[gl]["status"] in INKY
        okr = gr is not None and R[gr]["status"] in INKY
        if okl and okr:
            pts = [(u, R[u]["v"]) for u in range(gl - 14, gr + 15) if u in R and R[u]["status"] in INKY]
            v = fitline(pts, u0)
            return {"u": u0, "v": v, "vb": max(R[gl]["vb"], R[gr]["vb"]) + 0.5, "how": "grid-crossing",
                    "near": sorted(set(R[gl].get("near", []) + R[gr].get("near", [])))}
        # the dash ends at or under the grid line: nearest ink column
        cands = []
        if okl:
            cands.append((u0 - gl, gl, -1))
        if okr:
            cands.append((gr - u0, gr, +1))
        if not cands:
            return gap_to_end(R, u0, lo, hi)
        d, ue, side = min(cands)
        v, vb = dash_end_point(R, ue, -side if side == +1 else +1)
        return {"u": ue, "v": v, "vb": vb, "how": "dash end at grid line (%s side)" % ("left" if side < 0 else "right"),
                "near": R[ue].get("near", []), "moved_px": ue - u0}
    return gap_to_end(R, u0, lo, hi)


def gap_to_end(R, u0, lo, hi):
    # nearest ink column in either direction (skipping grid columns)
    best = None
    for direction in (-1, +1):
        u = u0
        while lo <= u <= hi:
            u += direction
            if u in R and R[u]["status"] in INKY:
                if best is None or abs(u - u0) < abs(best[0] - u0):
                    best = (u, direction)
                break
    ue, direction = best
    # the dash extends away from u0: inward direction is the same as the search direction
    v, vb = dash_end_point(R, ue, -direction)
    return {"u": ue, "v": v, "vb": vb, "how": "gap: moved to dash end", "near": R[ue].get("near", []), "moved_px": ue - u0}


def curve_samples(name):
    R = load(name)
    ink = sorted(u for u, r in R.items() if r["status"] in INKY)
    solid = [u for u in ink if thick_enough(R, u)]
    lo, hi = solid[0], solid[-1]
    out = []
    # left end
    vL, vbL = dash_end_point(R, lo, -1)
    out.append({"u": lo, "v": vL, "vb": vbL, "how": "left end", "near": R[lo].get("near", [])})
    gu = np.array([u for u in ink]); gv = np.array([R[u]["v"] for u in ink])
    vat = lambda u: float(np.interp(u, gu, gv))
    x = -0.10
    while x <= 1.10 + 1e-9:
        # the u of this Dr at the curve's height (two iterations)
        u = u_of_x(round(x, 2), vat(lo))
        for _ in range(3):
            u = u_of_x(round(x, 2), vat(u))
        if lo + 2 < u < hi - 2:
            s = sample_at(R, u, (lo, hi))
            s["dr"] = round(x, 2)
            s["u_target"] = round(u, 1)
            out.append(s)
        x += 0.05
    vR, vbR = dash_end_point(R, hi, +1)
    out.append({"u": hi, "v": vR, "vb": vbR, "how": "right end", "near": R[hi].get("near", [])})
    return out


if __name__ == "__main__":
    names = sys.argv[1].split(",")
    (OUT / "samples").mkdir(exist_ok=True)
    for n in names:
        s = curve_samples(n)
        R = load(n)
        for p in s:   # a line's centre is known to within half its thickness, never better
            p["vb"] = max(p["vb"], R[p["u"]]["tv"] / 2)
        (OUT / "samples" / f"{n}.json").write_text(json.dumps(s, indent=0))
        print(f"== {n}: {len(s)} samples")
        for p in s:
            print(f"  dr={p.get('dr', ''):>5} u_t={p.get('u_target', ''):>7} u={p['u']:>5} v={p['v']:.1f} vb={p['vb']:.1f} {p['how']} {p.get('moved_px', '')} {','.join(p['near'])}")
