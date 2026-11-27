"""Assemble points-p1.csv and points-p2.csv for FC-6B from markers.csv (markers.py), the trace
samples (samples/<series>.csv from sample.py) and the dense tracks (tracks/<series>.csv, for the
peak features), plus the hand readings listed below where the automatic sampler cannot see the
line (the start of n4695 between its first triangle and the first n3815 square, the split of
the shared n4695/n3815 band, and the first ink of three lines that start against a symbol).
"""
import csv

import numpy as np

FIG = "FC-6B"
COLS = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v",
        "u_bound_px", "v_bound_px", "symbol", "note"]
SERIES = ["n4695", "n3815", "n2934", "n1761", "n734"]
U_MAX = {"n4695": 2072, "n3815": 2069, "n2934": 2071, "n1761": 2071, "n734": 2065}
SHARED = "shared ink: the n4695 and n3815 lines are drawn on top of each other from the first n3815 square up to u 797 (band about twice the line width); band center, bound half the band"
HG_NOTE = {
    "n4695": {(842, 856): "2000", (1100, 1145): "3000", (1690, 1765): "4000"},
    "n3815": {(842, 919): "2000", (1355, 1405): "3000"},
    "n2934": {(735, 770): "1000", (1189, 1245): "2000"},
    "n1761": {(955, 1010): "1000"},
}

# hand readings: (series, u, v, u_bound, v_bound, note); replace any automatic sample within 8 px
MANUAL = {
    "n4695": [(708.5, 1762.0, 2, 6, "first ink of the line: the short stroke leaving the apex of the first triangle, below the first n3815 square (the line then crosses the lower-right corner of that square, not sampled)"),
              (803, 1562.4, 1, 11, "n4695 line just after it leaves the shared band, heading for the second triangle along the left side of the second n3815 square")],
    "n3815": [(803, 1588.5, 1, 7.5, "n3815 line just after it leaves the shared band, entering the left side of the second square"),
              (860, 1530.0, 1, 8, "filler sample read from the column scan, to keep the spacing under 5 thousandths next to the hand-read gridline samples"),
              (875, 1517.5, 1, 9.5, "line merged with the 2000 gridline here; center from the run's free (lower) edge, read by hand"),
              (888, 1506.5, 1, 9.5, "line merged with the 2000 gridline here; center from the run's free (upper) edge, read by hand")],
    "n2934": [(730, 1825.5, 1, 6, "first ink of the line, at the upper-right corner of the first triangle")],
    "n1761": [(726, 1921.5, 1, 6, "first ink of the line, just right of the first circle")],
    "n734": [(726, 1982.0, 1, 5.5, "first ink of the line: the first dash starts against the right arm of the first plus"),
             (741, 1981.8, 1, 6.5, "filler sample read from the column scan, to keep the spacing under 5 thousandths after the hand-read first point")],
}


def load_samples(s):
    out = []
    for r in csv.DictReader(open(f"samples/{s}.csv", encoding="utf-8")):
        u, v, b, kind = int(r["u"]), float(r["v"]), float(r["v_bound"]), r["kind"]
        if u > U_MAX[s]:
            continue
        note = ""
        if kind == "hgrid":
            g = next((val for (a, bb), val in HG_NOTE.get(s, {}).items() if a <= u <= bb), "a")
            note = f"line merged with the {g} gridline here; center from the run's free edge"
        if s in ("n4695", "n3815") and u <= 797:
            note = SHARED
        out.append([float(u), v, 1.0, b, note])
    for (mu, mv, mub, mvb, mnote) in MANUAL.get(s, []):
        out = [p for p in out if abs(p[0] - mu) > 8]
        out.append([mu, mv, mub, mvb, mnote])
    out.sort(key=lambda p: p[0])
    return out


def peak(s, samples):
    rows = [r for r in csv.DictReader(open(f"tracks/{s}.csv", encoding="utf-8"))
            if r["v"] != "" and not (set(r["flags"].split("|")) & {"vgrid", "hgrid", "symbol", "none"})
            and 5 <= int(r["thick"]) <= 45 and 721 <= int(r["u"]) <= U_MAX[s]]
    u = np.array([int(r["u"]) for r in rows])
    v = np.array([float(r["v"]) for r in rows])
    t = np.array([int(r["thick"]) for r in rows])
    med = np.array([np.median(t[np.abs(u - x) <= 40]) for x in u])
    keep = t >= 0.7 * med
    u, v, t = u[keep], v[keep], t[keep]
    sm = np.array([v[np.abs(u - x) <= 5].mean() for x in u])
    i = int(np.argmin(sm))
    region = u[sm <= sm[i] + 1.0]
    lo, hi = int(region.min()), int(region.max())
    pu = (lo + hi) / 2
    ub = max(2.0, (hi - lo) / 2)
    note = "peak of the drawn line (minimum v)"
    if hi - lo > 10:
        note += f"; flat top: the line stays within 1 px of its highest level from u {lo} to {hi}, so u is not an observation"
    if s == "n2934":
        note += "; the line rises to its end, so the peak is at the last inked column"
    return pu, float(sm[i]), ub, float(t[i]) / 2, note, lo, hi


def main():
    rows = []
    markers = list(csv.DictReader(open("markers.csv", encoding="utf-8")))
    report = []
    for s in SERIES:
        ms = [m for m in markers if m["panel"] == "1" and m["series_id"] == s]
        rows += ms
        smp = load_samples(s)
        for k, (u, v, ub, vb, note) in enumerate(smp, 1):
            rows.append(dict(figure_id=FIG, panel=1, series_id=s, point_kind="trace", sequence=k,
                             pixel_u=u, pixel_v=round(v, 1), u_bound_px=ub, v_bound_px=vb, symbol="", note=note))
        f0, fl = smp[0], smp[-1]
        pu, pv, pub, pvb, pnote, lo, hi = peak(s, smp)
        feats = [(f0[0], f0[1], f0[2], f0[3], "first point of the drawn line (where its ink starts)"),
                 (pu, pv, pub, pvb, pnote),
                 (fl[0], fl[1], fl[2], fl[3], "last point of the drawn line (where its ink ends, against the last marker)")]
        for k, (u, v, ub, vb, note) in enumerate(feats, 1):
            rows.append(dict(figure_id=FIG, panel=1, series_id=s, point_kind="feature", sequence=k,
                             pixel_u=round(u, 1), pixel_v=round(v, 1), u_bound_px=round(ub, 1), v_bound_px=round(vb, 1), symbol="", note=note))
        gaps = [(smp[i][0], smp[i + 1][0]) for i in range(len(smp) - 1) if smp[i + 1][0] - smp[i][0] > 28.9]
        report.append(f"{s}: {len(ms)} markers, {len(smp)} trace, 3 features; peak u {pu:.0f} (flat {lo}-{hi}) v {pv:.1f}; gaps > 5 thousandths: {gaps}")
    with open("points-p1.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    rows2 = [m for m in markers if m["panel"] == "2"]
    with open("points-p2.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows2)
    print("\n".join(report))
    print(f"panel 1: {len(rows)} points; panel 2: {len(rows2)} points")


if __name__ == "__main__":
    main()
