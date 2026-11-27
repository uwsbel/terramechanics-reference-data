"""Follow a drawn (dashed) curve column by column from a start point, using the series' markers
as waypoints, and write the ink centre every `step` px; then pick samples every `every` x units
away from vertical gridlines.

    python trace.py <image> <calibration.json> <markers.csv> <series_id> <out_track.csv>
                    [--step 2] [--tol 9] [--maxgap 40] [--thick 3 24] [--halfwidth 1]
                    [--u0 U --v0 V] [--u1 U]

The track is the sequence (u, v_center, thickness, state) with state `ink` (a dark run was found
within `tol` px of the prediction) or `gap` (no run; position extrapolated, NOT an observation).
At each column the dark runs are those of plot_grid.py scan: a pixel is dark when it is dark in
all columns u-h..u+h. Markers (from markers.csv) are used only to re-centre the prediction when the
track passes a marker (|du| <= 3): the prediction is pulled toward the marker centre with a weight
of 0.5, since the drawn line passes close to, but not exactly through, the symbols. Everything
written as `ink` is checked on the overlay by eye.
"""
import argparse
import csv
import json

import numpy as np
from PIL import Image


def runs_at(sub_dark, v0):
    """dark runs along a column (bool array), returns list of (center, thickness)."""
    idx = np.where(sub_dark)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i != p + 1:
            out.append(((s + p) / 2 + v0, p - s + 1))
            s = i
        p = i
    out.append(((s + p) / 2 + v0, p - s + 1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("calibration")
    ap.add_argument("markers")
    ap.add_argument("series")
    ap.add_argument("out")
    ap.add_argument("--step", type=int, default=2)
    ap.add_argument("--tol", type=float, default=9)
    ap.add_argument("--maxgap", type=int, default=40)
    ap.add_argument("--thick", type=int, nargs=2, default=[3, 70])
    ap.add_argument("--halfwidth", type=int, default=1)
    ap.add_argument("--u0", type=float)
    ap.add_argument("--v0", type=float)
    ap.add_argument("--u1", type=float)
    ap.add_argument("--vband", type=float, nargs=2, default=[1300, 2500])
    ap.add_argument("--dark", type=int, default=128)
    ap.add_argument("--slope0", type=float, default=0.0, help="initial dv/du (negative = rising stress)")
    a = ap.parse_args()
    g = np.asarray(Image.open(a.image).convert("L"))
    cal = json.load(open(a.calibration, encoding="utf-8"))
    mk = [r for r in csv.DictReader(open(a.markers, encoding="utf-8-sig", newline=""))
          if r["series_id"] == a.series and r["point_kind"] == "marker"]
    mk = sorted([(float(r["pixel_u"]), float(r["pixel_v"])) for r in mk])
    u = a.u0 if a.u0 is not None else mk[0][0]
    v = a.v0 if a.v0 is not None else mk[0][1]
    u_end = a.u1 if a.u1 is not None else mk[-1][0]
    slope = a.slope0
    track = []
    gap = 0
    vlo, vhi = int(a.vband[0]), int(a.vband[1])
    while u <= u_end + 0.5:
        ui = int(round(u))
        h = a.halfwidth
        col = g[vlo:vhi, ui - h:ui + h + 1] < a.dark
        dark = col.all(axis=1)
        rr = [(c, t) for c, t in runs_at(dark, vlo) if a.thick[0] <= t <= a.thick[1]]
        pred = v + slope * a.step
        # pull toward a marker centre when passing one
        for mu, mv in mk:
            if abs(mu - u) <= 3:
                pred = 0.5 * pred + 0.5 * mv
        best = None
        for c, t in rr:
            d = abs(c - pred)
            if d <= a.tol and (best is None or d < best[0]):
                best = (d, c, t)
        if best is not None:
            _, c, t = best
            if track and track[-1][3] == "ink":
                slope = 0.7 * slope + 0.3 * (c - track[-1][1]) / (u - track[-1][0])
            v = c
            track.append((u, c, t, "ink"))
            gap = 0
        else:
            v = pred
            gap += a.step
            track.append((u, v, 0, "gap"))
            if gap > a.maxgap:
                print(f"{a.series}: lost the line at u={u:.0f} (gap > {a.maxgap}); stopping")
                break
        u += a.step
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["u", "v", "thickness", "state"])
        for r in track:
            w.writerow([f"{r[0]:.1f}", f"{r[1]:.1f}", r[2], r[3]])
    n_ink = sum(1 for r in track if r[3] == "ink")
    print(f"{a.series}: {len(track)} columns from u={track[0][0]:.0f} to {track[-1][0]:.0f}, {n_ink} with ink; wrote {a.out}")


main()
