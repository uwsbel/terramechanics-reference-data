"""Follow a drawn (dashed) curve by arc length: at each step a short profile perpendicular to the
current direction is read from the page image, the dark run nearest the predicted position is
taken as the line (its width is the line thickness), and the direction is updated. Works for
steep and flat segments alike (the column scan of trace.py fails on the steep rises).

    python trace2.py <image> <markers.csv> <series_id> <out_track.csv> --u0 U --v0 V --slope0 S
                     [--u1 2232] [--step 2] [--tol 12] [--maxgap 50] [--thick 3 22] [--marker-r 12]

Inside a marker footprint (within `marker-r` px of a marker centre of this series) the ink is
the symbol, not the line, so the tracker coasts straight through (state `marker`). Where no run
is found the position is extrapolated (state `gap`) for up to `maxgap` px. Only `ink` rows are
observations; everything is checked on the overlay by eye.
"""
import argparse
import csv
import math

import numpy as np
from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("markers")
    ap.add_argument("series")
    ap.add_argument("out")
    ap.add_argument("--u0", type=float, required=True)
    ap.add_argument("--v0", type=float, required=True)
    ap.add_argument("--slope0", type=float, required=True)
    ap.add_argument("--u1", type=float, default=2232)
    ap.add_argument("--step", type=float, default=2)
    ap.add_argument("--tol", type=float, default=12)
    ap.add_argument("--maxgap", type=float, default=50)
    ap.add_argument("--thick", type=float, nargs=2, default=[3, 22])
    ap.add_argument("--marker-r", type=float, default=12)
    ap.add_argument("--dark", type=int, default=128)
    a = ap.parse_args()
    g = np.asarray(Image.open(a.image).convert("L"))
    H, W = g.shape
    mk = [(float(r["pixel_u"]), float(r["pixel_v"])) for r in csv.DictReader(open(a.markers, encoding="utf-8-sig", newline=""))
          if r["series_id"] == a.series and r["point_kind"] == "marker"]

    def is_dark(u, v):
        ui, vi = int(round(u)), int(round(v))
        return 0 <= ui < W and 0 <= vi < H and g[vi, ui] < a.dark

    u, v = a.u0, a.v0
    d = np.array([1.0, a.slope0])
    d /= np.linalg.norm(d)
    track = []
    gap = 0.0
    last_ink = None
    while u <= a.u1:
        n = np.array([-d[1], d[0]])  # perpendicular
        near_marker = any(math.hypot(u - mu, v - mv) <= a.marker_r for mu, mv in mk)
        found = None
        if not near_marker:
            offs = np.arange(-a.tol, a.tol + 0.5, 0.5)
            dark = np.array([is_dark(u + s * n[0], v + s * n[1]) for s in offs])
            runs = []
            i = 0
            while i < len(offs):
                if dark[i]:
                    j = i
                    while j + 1 < len(offs) and dark[j + 1]:
                        j += 1
                    runs.append(((offs[i] + offs[j]) / 2, offs[j] - offs[i] + 0.5))
                    i = j + 1
                else:
                    i += 1
            best = None
            for c, t in runs:
                if a.thick[0] <= t <= a.thick[1] and (best is None or abs(c) < abs(best[0])):
                    best = (c, t)
            if best is not None:
                found = best
        if found is not None:
            c, t = found
            u, v = u + c * n[0], v + c * n[1]
            if last_ink is not None:
                vec = np.array([u - last_ink[0], v - last_ink[1]])
                if np.linalg.norm(vec) > 0.5:
                    vec /= np.linalg.norm(vec)
                    d = 0.6 * d + 0.4 * vec
                    d /= np.linalg.norm(d)
            track.append((u, v, t, "ink"))
            last_ink = (u, v)
            gap = 0.0
        else:
            track.append((u, v, 0, "marker" if near_marker else "gap"))
            if not near_marker:
                gap += a.step
                if gap > a.maxgap:
                    print(f"{a.series}: lost the line at u={u:.0f}, v={v:.0f} (gap > {a.maxgap}); stopping")
                    break
        if d[0] <= 0.05:  # never run backwards in u
            d = np.array([0.05, math.copysign(1.0, d[1])])
            d /= np.linalg.norm(d)
        u, v = u + a.step * d[0], v + a.step * d[1]
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["u", "v", "thickness", "state"])
        for r in track:
            w.writerow([f"{r[0]:.1f}", f"{r[1]:.1f}", f"{r[2]:.1f}", r[3]])
    n_ink = sum(1 for r in track if r[3] == "ink")
    print(f"{a.series}: {len(track)} steps, u {track[0][0]:.0f} to {track[-1][0]:.0f}, {n_ink} ink; wrote {a.out}")


main()
