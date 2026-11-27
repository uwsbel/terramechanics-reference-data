"""Final panel-1 points of F2-48: the first reading (points-p1-prev.csv, from sample_points.py) with the
changes made when it was checked against the page on zoomed crops (2026-11-02). Every trace sample of the
first reading was checked on the ink and is kept unchanged; only features change, as listed below with the
evidence. Writes out/F2-48/points-p1.csv in drawing order (sequence renumbered per series).

Run from the workspace root, after sample_points.py:
    python out/F2-48/finalize_points.py
"""
import csv
import sys

sys.path.insert(0, "out/F2-48")
from trace_lib import x_of  # noqa: E402  (penetration at a pixel, only to order the rows)

SRC = "out/F2-48/points-p1-prev.csv"
OUT = "out/F2-48/points-p1.csv"
rows = list(csv.DictReader(open(SRC, encoding="utf-8")))


def find(series, kind, u, v):
    hits = [r for r in rows if r["series_id"] == series and r["point_kind"] == kind
            and abs(float(r["pixel_u"]) - u) < 0.05 and abs(float(r["pixel_v"]) - v) < 0.05]
    assert len(hits) == 1, (series, kind, u, v, len(hits))
    return hits[0]


def setp(r, u=None, v=None, bu=None, bv=None, note=None):
    if u is not None:
        r["pixel_u"] = f"{u:.1f}"
    if v is not None:
        r["pixel_v"] = f"{v:.1f}"
    if bu is not None:
        r["u_bound_px"] = f"{bu:.1f}"
    if bv is not None:
        r["v_bound_px"] = f"{bv:.1f}"
    if note is not None:
        r["note"] = note


# ---------------------------------------------------------------- lpt87 (solid, Four-Inch Cylinder)
setp(find("lpt87", "feature", 2245.0, 3758.0),
     note="first: the solid line's ink comes out of the bottom frame line (penetration 0) here, just left of "
          "the corner; the lowest dots of lpt85 merge with its upper edge (the two traces run together below "
          "about 0.13 in), so the bound is widened; whether it continues inside the frame to the corner cannot be seen")
# toe knee: the bend lies where dots of lpt85 sit on the solid line's upper edge (u 2222 to 2246), so its
# position along the line is known to about 5 px, not 3.5
setp(find("lpt87", "feature", 2218.0, 3738.0), bu=5.0, bv=4.0,
     note="knee (toe): the line bends from the steep run into the frame corner (about 200 lb/in) to the fast "
          "rise (about 600 lb/in); lpt85 dots sit on the line's upper edge just right of it, so the bound along "
          "the line is widened")
# knee onto the plateau: a rounded turn; two-line fits over different windows put the corner at 0.35 to
# 0.50 in, the ink turns between about 0.38 and 0.455 in; the bound now covers the turn
setp(find("lpt87", "feature", 2031.5, 3668.0), bu=6.0, bv=10.0,
     note="knee: end of the initial rise, the trace turns onto the plateau; the turn is rounded (from about "
          "165 lb/in to flat between 0.38 and 0.455 in), so the bound covers the bend, not a corner")
# local maximum of the plateau: the leftmost ink (highest load) is flat within 1 px (0.65 lb) from v 3608
# to 3660 (0.45 to 0.68 in), with one 4 px wiggle at v 3624-3632; the first reading put it at v 3648 with a
# 10 px bound, which left out the upper half of the flat top
setp(find("lpt87", "feature", 2026.5, 3648.0), u=2026.5, v=3634.0, bu=3.0, bv=27.0,
     note="knee: local maximum of the plateau, a flat top (u within 1 px from 0.45 to 0.68 in); x is not an "
          "observation here, the v bound covers the whole flat top")
setp(find("lpt87", "feature", 2044.5, 3502.0), bv=12.0,
     note="knee: lowest load of the plateau, after which the second rise begins; the minimum is flat within "
          "1 px from about 1.07 to 1.11 in, so the v bound covers it")

# ---------------------------------------------------------------- lpt85 (dotted, Four-Inch Footpad)
# knee onto the plateau: the dot direction changes between the dots at v 3616 and 3600 (du/dv about 0.5
# below, 0.05 above; the two straight runs meet at v 3612); in value space 78 lb/in up to the dot at
# 0.643 in, 21 lb/in after it; two-line fits put the corner at 0.62 to 0.65 in. The first reading put
# the knee on the next dot (0.715 in), past the corner.
setp(find("lpt85", "feature", 2136.0, 3599.5), u=2138.3, v=3616.4, bu=6.0, bv=9.0,
     note="knee: end of the initial rise, the dots turn onto the plateau (on the dot nearest the corner, "
          "which two-line fits put at 0.62 to 0.65 in)")
setp(find("lpt85", "feature", 2122.0, 3447.2), bv=10.0,
     note="knee: the second rise begins, slope up from about 20 to 90 lb/in (on a dot); two-line fits put "
          "the corner at 1.28 to 1.35 in, the dots are 0.05 in apart")
# new: a clear bend near 4.9 in, visible against a ruler on the page; two-line fits over 3.8-6.0,
# 4.2-5.6 and 4.4-5.4 in put it at 4.87 to 4.89 in (slope 78 to 99 lb/in, rms 0.13 to 0.30 lb against
# 1.0 to 3.1 lb for one line). The corner (u 1649.5, v 2324) is on the 400 lb grid line, where the dots
# merge with it; the knee goes on the nearest dot with its own ink left of the grid line.
rows.append(dict(figure_id="F2-48", panel="1", series_id="lpt85", point_kind="feature", sequence="",
                 pixel_u="1643.9", pixel_v="2315.4", u_bound_px="6.5", v_bound_px="10.0", symbol="",
                 note="knee: the slope rises from about 78 to 99 lb/in (corner at 4.87 to 4.89 in by two-line "
                      "fits, on the 400 lb grid line); on the nearest dot, which touches the grid line on its "
                      "right (its center from the ink left of the line)"))

# ---------------------------------------------------------------- trace ends as trace samples
# Rule 7 and lesson 1 of the task: a curve's first and last trace samples are where its ink starts and
# ends. The first reading had those two points only as features, so its traces began at 0.25 in and
# ended at the last 0.25 in step; the ends are added as trace rows at the same pixels and bounds.
for series in ("lpt87", "lpt85"):
    f_first = [r for r in rows if r["series_id"] == series and r["point_kind"] == "feature"
               and r["note"].startswith("first")]
    f_last = [r for r in rows if r["series_id"] == series and r["point_kind"] == "feature"
              and r["note"].startswith("last")]
    assert len(f_first) == 1 and len(f_last) == 1
    for f, where in ((f_first[0], "start"), (f_last[0], "end")):
        extra = ("; the two traces run together here (lpt85 dots on the solid line's upper edge), bound widened"
                 if where == "start" else "")
        rows.append(dict(f, point_kind="trace", sequence="",
                         note=f"trace sample at the {where} of the ink (the same point as the "
                              f"{'first' if where == 'start' else 'last'} feature){extra}"))

# ---------------------------------------------------------------- drawing order, sequence, write
order = {"lpt87": 0, "lpt85": 1}
kind_rank = {"trace": 0, "feature": 1}


def key(r):
    note = r["note"]
    x = x_of(float(r["pixel_u"]), float(r["pixel_v"]))
    # first point before everything, last point after the peak at the same ink
    tie = 0 if note.startswith("first") else 2 if note.startswith("last") else 1
    return (order[r["series_id"]], tie == 2, tie != 0, round(x, 6), kind_rank[r["point_kind"]], tie)


rows.sort(key=key)
cnt = {}
for r in rows:
    cnt[r["series_id"]] = cnt.get(r["series_id"], 0) + 1
    r["sequence"] = str(cnt[r["series_id"]])
cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px",
        "v_bound_px", "symbol", "note"]
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
for s in ("lpt87", "lpt85"):
    print(s, {k: sum(1 for r in rows if r["series_id"] == s and r["point_kind"] == k) for k in ("trace", "feature")})
