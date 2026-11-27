"""Trace samples of one tracked curve at every 0.05 of Dr (FC-18 blind reading helper).

    python sample_curve.py <calibration.json> <track.csv> <name> <dashed 0|1> <exclude "u0-u1,u0-u1"> <out.csv>

Reads the column centres written by track_curve.py. Only `ok` columns are used, minus the excluded
u ranges (where a circle sits on the curve and its ring merges with the line).

Location of a target Dr: the u where the curve crosses the line of constant Dr interpolated between
the two bracketing vertical grid lines of the calibration (each with its own tilt), at the curve's v;
beyond the 1.0 line, extrapolated from the 0.9 and 1.0 lines. This is only where to sample; the values
come later from the piecewise map.

Dashed curve: the dashes are the stretches of ink (ok and merged columns, and grid-line columns with ink on
both sides) between gaps (gap and speck columns) of 8 columns or more. A target that falls in a gap moves to the nearest dash end, on the
ink: the last (or first) column of that dash whose dark run is at least 5 px tall.
A target inside an excluded range moves to the nearest end of that range.

v at the sample: a straight line fitted to the ok columns within +-15 px (widened up to +-40 px until
10 columns are found), on the same dash. Bounds: v half the median vertical run of those columns,
u half the line thickness across it (v bound times cos of the slope angle).
"""
import csv
import json
import math
import sys

import numpy as np


def main():
    cal_path, track, name, dashed, excl, out = sys.argv[1:7]
    dashed = dashed == "1"
    excl = [tuple(float(x) for x in r.split("-")) for r in excl.split(",") if r]
    cal = json.loads(open(cal_path, encoding="utf-8").read())
    V = sorted([(l["x_value"], l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]])
    with open(track, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["u"] = int(r["u"])
        r["c"] = float(r["centre"]) if r["centre"] else None
        r["len"] = int(r["length"])
    excluded = lambda u: any(a <= u <= b for a, b in excl)
    ok = [r for r in rows if r["flag"] == "ok" and not excluded(r["u"])]
    U = np.array([r["u"] for r in ok], float)
    C = np.array([r["c"] for r in ok], float)
    glob = np.polyfit(U, C, 3)                      # only to find where to sample
    # dashes
    dashes = []
    if dashed:
        # ok and merged columns are ink, gap and speck columns are not; a stretch of grid-line columns
        # (vgrid, hgrid) cannot show whether the curve is drawn under the grid line, so it counts as ink
        # only when the columns on both sides of it are ink (a crossing inside a dash), else as gap (the
        # dash end is then put at the last column seen clear of the grid line)
        state = [True if r["flag"] in ("ok", "merged") else False if r["flag"] in ("gap", "speck") else None for r in rows]
        ink = list(state)
        i = 0
        while i < len(rows):
            if state[i] is None:
                j = i
                while j < len(rows) and state[j] is None:
                    j += 1
                left = state[i - 1] if i > 0 else False
                right = state[j] if j < len(rows) else False
                for k in range(i, j):
                    ink[k] = bool(left and right)
                i = j
            else:
                i += 1
        start, gap = None, 0
        for i, r in enumerate(rows):
            if ink[i]:
                if start is None:
                    start = i
                gap = 0
                last = i
            else:
                gap += 1
                if start is not None and gap >= 8:
                    dashes.append((rows[start]["u"], rows[last]["u"]))
                    start = None
        if start is not None:
            dashes.append((rows[start]["u"], rows[last]["u"]))
        # trim each dash to columns with a run of 5 px or more at its ends
        trimmed = []
        byu = {r["u"]: r for r in rows}
        for a, b in dashes:
            while a < b and not (byu[a]["len"] >= 5):
                a += 1
            while b > a and not (byu[b]["len"] >= 5):
                b -= 1
            trimmed.append((a, b))
        dashes = trimmed
        print(f"{name}: {len(dashes)} dashes: " + ", ".join(f"{a}-{b}" for a, b in dashes))

    def x_at(u, v):
        pos = [(xv, a + s * v) for xv, a, s in V]
        for (x0, u0), (x1, u1) in zip(pos, pos[1:]):
            if u0 <= u <= u1:
                return x0 + (u - u0) * (x1 - x0) / (u1 - u0)
        (x0, u0), (x1, u1) = (pos[0], pos[1]) if u < pos[0][1] else (pos[-2], pos[-1])
        return x0 + (u - u0) * (x1 - x0) / (u1 - u0)

    def u_for(d):
        lo, hi = U.min() - 50, U.max() + 60
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if x_at(mid, np.polyval(glob, mid)) < d:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def dash_of(u):
        for a, b in dashes:
            if a <= u <= b:
                return (a, b)
        return None

    out_rows = []
    d = 0.05
    while d < 1.0999:
        ut = u_for(d)
        note = ""
        u = ut
        if dashed and dash_of(round(u)) is None:
            ends = [(abs(u - a), a, (a, b), "start") for a, b in dashes] + [(abs(u - b), b, (a, b), "end") for a, b in dashes]
            dist, u, dsh, which = min(ends)
            note = f"Dr {d:.2f} falls in a gap between dashes; moved to the nearest dash {which} (u {u})"
        for a, b in excl:
            if a <= u <= b:
                u2 = a - 1 if u - a < b - u else b + 1
                note = (note + "; " if note else "") + f"Dr {d:.2f} falls where a circle merges with the line (u {a:.0f}-{b:.0f}); moved to u {u2:.0f}"
                u = u2
        dsh = dash_of(round(u)) if dashed else None
        for w in (15, 20, 25, 30, 40):
            sel = [(r["u"], r["c"], r["len"]) for r in ok if abs(r["u"] - u) <= w and (dsh is None or dsh[0] <= r["u"] <= dsh[1])]
            if len(sel) >= 10:
                break
        A = np.array(sel, float)
        k, b = np.polyfit(A[:, 0], A[:, 1], 1)
        v = k * u + b
        res = A[:, 1] - (k * A[:, 0] + b)
        vb = 0.5 * float(np.median(A[:, 2]))
        ub = vb * math.cos(math.atan(abs(k)))
        out_rows.append({"target_dr": round(d, 2), "target_u": round(float(ut), 1), "u": round(float(u), 1), "v": round(float(v), 1),
                         "u_bound": round(ub, 1), "v_bound": round(vb, 1), "n_cols": len(sel), "window": w,
                         "slope": round(float(k), 3), "fit_rms": round(float(np.sqrt(np.mean(res ** 2))), 2), "note": note})
        d += 0.05
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(out_rows)
    for r in out_rows:
        print(f"  Dr {r['target_dr']:.2f}: ({r['u']}, {r['v']}) b ({r['u_bound']}, {r['v_bound']}) n {r['n_cols']} w {r['window']} "
              f"slope {r['slope']} rms {r['fit_rms']} {r['note']}")


if __name__ == "__main__":
    main()
