"""Assemble points-p1.csv from the reviewed marker readings (markers-p1.csv), the reviewed trace
samples (tr/*.csv, with the drops and additions listed below after review on the page image),
and the feature points. Bounds: markers as read; trace u bound 1 px (the column is chosen), v
bound half the dark run along the column (half the line thickness, or half the merged run where
the line shares ink with a gridline), at least 2 px."""
import csv
from pathlib import Path
H = Path(__file__).parent
import json
CAL = json.loads((H.parent / "cal-p1" / "calibration.json").read_text(encoding="utf-8"))
FIG = "FC-6C"
GRIDNOTE = {"3000": "line runs along the 3000 psf gridline and shares ink with it; v is the center of the merged run, bound half of it",
            "4000": "line runs along the 4000 psf gridline and shares ink with it; v is the center of the merged run, bound half of it",
            "2000": "line crosses the 2000 psf gridline at this column; run includes the gridline",
            "1000": "line crosses the 1000 psf gridline at this column; run includes the gridline"}
# series -> (trace files, drops (u), additions {u: (v, ub, vb, note)}, features)
CFG = {
 "n4695": (["n4695"], {709, 2061}, {
     709.5: (1811, 3, 3, "first ink of the drawn line (lower end); the line stops about 12 px short of the first plus marker"),
     2061: (1225, 2, 8, "last ink of the drawn line; ends about 19 px short of the last plus marker (only the 4000 gridline continues); merged with the 4000 gridline, v center of merged run")},
   [("first", 709.5, 1811, 3, 3, "first point: lower end of the drawn line"),
    ("peak", 2015, 1224, 46, 8.5, "peak: the drawn line is flat-topped (top edge v 1217) from u about 1969 to 2062, merged with the 4000 gridline; v = highest trace sample (u 1989 and 2049), u the middle of the flat top, u bound covers it"),
    ("last", 2061, 1225, 2, 8, "last point: right end of the drawn line's ink, merged with the 4000 gridline")]),
 "n3815": (["n3815"], {1944, 2079}, {
     712.5: (1995.5, 3, 2, "first ink of the drawn line, where it meets the top edge of the first triangle"),
     1948: (1522, 1, 8.5, "first ink after the gap at the 11th triangle (line resumes at u 1945); merged with the 3000 gridline, v center of the merged run, bound half of it"),
     2080: (1516.5, 2, 5, "last ink of the drawn line, about 4 px left of the last triangle; here the line is separate from the 3000 gridline below it")},
   [("first", 712.5, 1995.5, 3, 2, "first point: lower end of the drawn line at the top edge of the first triangle"),
    ("peak", 2070, 1516.5, 36, 4.5, "peak: the line's top edge is flat (v 1513) from u about 2004 to 2080; v read where the line is separate from the gridline (u 2064 to 2080); u bound covers the flat top"),
    ("last", 2080, 1516.5, 2, 5, "last point: right end of the drawn line's ink next to the last triangle")]),
 "n2934": (["n2934a", "n2934b"], {723, 2123, 2124}, {
     721.5: (2072, 3, 3, "first ink of the drawn line, where it meets the top right corner of the first square"),
     2126: (1564, 2, 4, "last ink of the drawn line: it passes through the last square and pokes out about 10 px past its right edge (x about 253, beyond the 250 gridline)")},
   [("first", 721.5, 2072, 3, 3, "first point: lower end of the drawn line at the first square"),
    ("peak", 1889, 1537.5, 4, 6, "peak: highest ink of the drawn line, at the right end of the dash before the 11th square; the line is hidden by that square from u 1890 to 1946 and descends after it"),
    ("last", 2126, 1564, 2, 4, "last point: right end of the drawn line, just past the right edge of the last square")]),
 "n1961": (["n1961"], {2095}, {
     719: (2162.5, 3, 3, "first ink of the drawn line, where it meets the right side of the first triangle near its apex"),
     2097: (2018.5, 2, 6, "last ink of the drawn line, about 4 px short of the last triangle")},
   [("first", 719, 2162.5, 3, 3, "first point: lower end of the drawn line at the first triangle"),
    ("peak", 1706, 1999.5, 12, 6, "peak: highest stretch of the drawn line between the 9th and 10th triangles (u 1696 to 1716 at the same v)"),
    ("last", 2097, 2018.5, 2, 6, "last point: right end of the drawn line next to the last triangle")]),
 "n714": (["n714"], {731, 2097}, {
     731.5: (2232, 3, 3, "first ink of the drawn line; it does not touch the first circle (gap of about 6 px)"),
     2098: (2194.5, 2, 6, "last ink of the drawn line, about 6 px short of the last circle")},
   [("first", 731.5, 2232, 3, 3, "first point: lower end of the drawn line"),
    ("peak", 855, 2192, 10, 5.5, "peak: the line is nearly flat from x about 40 to 250; its highest stretch (u 848 to 863) is only about 3 px above the plateau"),
    ("last", 2098, 2194.5, 2, 6, "last point: right end of the drawn line next to the last circle")]),
}
EXTRA_DROPS = {}
TRACE_NOTES = {}
def load_extra():
    p = H / "trace_review.csv"
    if p.exists():
        for r in csv.DictReader(open(p, encoding="utf-8")):
            if r["action"] == "drop":
                EXTRA_DROPS.setdefault(r["series_id"], set()).add(float(r["u"]))
            elif r["action"] == "note":
                TRACE_NOTES[(r["series_id"], float(r["u"]))] = r["note"]
load_extra()
rows = []
for r in csv.DictReader(open(H / "markers-p1.csv", encoding="utf-8")):
    rows.append(dict(figure_id=FIG, panel=1, series_id=r["series_id"], point_kind="marker", sequence=int(r["seq"]),
                     pixel_u=r["u"], pixel_v=r["v"], u_bound_px=r["ub"], v_bound_px=r["vb"], symbol=r["symbol"], note=r["note"]))
for sid, (files, drops, adds, feats) in CFG.items():
    pts = []
    for f in files:
        for t in csv.DictReader(open(H / "tr" / f"{f}.csv", encoding="utf-8")):
            u = float(t["u"])
            if u in drops or u in EXTRA_DROPS.get(sid, set()):
                continue
            L = int(t["run_len"]); fl = t["flags"]
            note = []
            if fl.startswith("HGRID"):
                y = fl[5:].split("/")[0]
                gl = [l for l in CAL["horizontal_lines"] if f"{l['y_value']:g}" == y][0]
                gv = gl["v_at_u0"] + gl["slope_dv_du"] * u
                if not (float(t["v0"]) - 1 <= gv <= float(t["v1"]) + 1):  # fitted gridline center more than 1 px outside the run: separate ink (checked on the page for u 2064)
                    note.append(f"line runs next to the {y} psf gridline (separate ink, within 2 px)")
                elif (sid, y) == ("n4695", "3000"):  # the steep 4695 line only crosses the 3000 gridline
                    note.append("line crosses the 3000 psf gridline at this column; run includes the gridline")
                else:
                    note.append(GRIDNOTE.get(y, "run touches a gridline"))
            if L <= 7 and not fl:
                note.append("short run: tapered end of a dash next to a marker")
            if L >= 18 and not fl:
                note.append("steep stroke: run is long along the column; v bound is half the run")
            if (sid, u) in TRACE_NOTES:
                note.append(TRACE_NOTES[(sid, u)])
            pts.append((u, float(t["v"]), 1, max(2.0, L / 2), "; ".join(note)))
    for u, (v, ub, vb, n) in adds.items():
        pts.append((float(u), v, ub, vb, n))
    pts.sort()
    for i, (u, v, ub, vb, n) in enumerate(pts, 1):
        rows.append(dict(figure_id=FIG, panel=1, series_id=sid, point_kind="trace", sequence=i, pixel_u=f"{u:g}", pixel_v=f"{v:g}",
                         u_bound_px=f"{ub:g}", v_bound_px=f"{vb:g}", symbol="", note=n))
    for i, (role, u, v, ub, vb, n) in enumerate(feats, 1):
        rows.append(dict(figure_id=FIG, panel=1, series_id=sid, point_kind="feature", sequence=i, pixel_u=f"{u:g}", pixel_v=f"{v:g}",
                         u_bound_px=f"{ub:g}", v_bound_px=f"{vb:g}", symbol="", note=n))
cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
out = H.parent / "points-p1.csv"
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n"); w.writeheader(); w.writerows(rows)
from collections import Counter
print(out, len(rows), Counter((r["series_id"], r["point_kind"]) for r in rows))
