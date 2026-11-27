"""Builds points-p1.csv for FA-6 from the reader's centrelines (see notes.md):
  tail end (merged, page rows), tail (tail3 envelopes), knee (page row runs read by eye, listed below),
  knee entrance (page column runs, listed below), steep part (steep3 envelopes), top bend (page row runs, below).
Each series is a polyline in drawing order from its fine end; trace samples are taken where it crosses
log10(grain size) = k * 0.05 and, where it rises by more than 10 percent between two such samples, every
5 percent finer in between. A dashed-curve sample that falls in a dash gap is moved to the nearest dash end
(rule 7). Sampling positions come from the reader's own calibration (cal-p1); values are written later by
calibrate_axes.py piecewise."""
import sys, csv, json, math
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve()
WS = HERE.parents[3]
sys.path.insert(0, str(WS / "tools"))
import calibrate_axes as ca

_cal, XK, YK = ca.piecewise_maps(str(WS / "out/FA-6/cal-p1"), str(WS / "out/FA-6/p0014-table-masked.png"))
def qy(u, v):
    return math.log10(XK.value(u, v)[0]), YK.value(u, v)[0]

page = np.asarray(Image.open(WS / "packet/p0014.png").convert("L")) < 128
CL = json.load(open(WS / "out/FA-6/helpers/centerlines.json"))
HALF = 6.0

def V(u, v, b=HALF, tag="sep", ink=True):
    return dict(u=float(u), v=float(v), bu=float(b), bv=float(b), tag=tag, ink=ink)

# ---------- tail end: the three curves run together (page rows) ----------
def tail_end():
    out = []
    for v in range(2945, 2849, -3):
        if v == 2945:
            out.append(dict(u=2241.5, v=2945.0, bu=4.0, bv=3.0, tag="merged", ink=True)); continue
        row = page[v, 2222:2250]
        idx = np.where(row)[0]
        if len(idx) == 0:
            continue
        L, R = 2222 + idx[0], 2222 + idx[-1]
        if 2885 <= v <= 2920:          # left arc of the circle at (2229, 2904) is not curve ink
            L = max(L, 2236)
        L = max(L, 2225)
        c, h = 0.5 * (L + R), max(HALF, 0.5 * (R - L) + 1)
        out.append(dict(u=c, v=float(v), bu=h, bv=HALF, tag="merged", ink=True))
    return out

# ---------- tail: rows from tail3 envelopes ----------
def tail_rows(series, v_hi, v_lo):
    t = CL["tail"]; out = []
    for i, v in enumerate(t["v"]):
        if not (v_lo <= v <= v_hi) or int(v) % 2:
            continue
        eL, eR = t["envL"][i], t["envR"][i]
        band = eR - eL
        up, lo = eL + HALF - 0.5, eR - HALF + 0.5
        if band < 22:
            out.append(dict(u=0.5 * (eL + eR), v=v, bu=max(HALF, 0.5 * band + 1), bv=HALF, tag="merged", ink=True))
            continue
        if series == "upper":
            out.append(dict(u=up, v=v, bu=HALF, bv=HALF, tag="sep" if t["ldash"][i] else "gap", ink=bool(t["ldash"][i])))
        elif series == "lower":
            out.append(dict(u=lo, v=v, bu=HALF, bv=HALF, tag="sep" if t["rdash"][i] else "gap", ink=bool(t["rdash"][i])))
        else:
            if t["avg_support"][i] >= 3:
                out.append(dict(u=t["average"][i], v=v, bu=HALF, bv=HALF, tag="sep", ink=True))
            else:
                out.append(dict(u=0.5 * (up + lo), v=v, bu=max(HALF, 0.5 * (lo - up)), bv=HALF, tag="inferred", ink=True))
    out.sort(key=lambda d: -d["v"])
    return out

# ---------- steep part: columns from steep3 envelopes ----------
def steep_cols(series, u_hi, u_lo):
    s = CL["steep"]; out = []
    for i, u in enumerate(s["u"]):
        if not (u_lo <= u <= u_hi) or int(u) % 2:
            continue
        lo_, up_ = s["lower"][i], s["upper"][i]
        if series == "lower":
            out.append(dict(u=u, v=lo_, bu=HALF, bv=HALF, tag="sep" if s["tdash"][i] else "gap", ink=bool(s["tdash"][i])))
        elif series == "upper":
            out.append(dict(u=u, v=up_, bu=HALF, bv=HALF, tag="sep" if s["bdash"][i] else "gap", ink=bool(s["bdash"][i])))
        else:
            if s["avg_support"][i] >= 3:
                out.append(dict(u=u, v=s["average"][i], bu=HALF, bv=HALF, tag="sep", ink=True))
            else:
                out.append(dict(u=u, v=s["average"][i], bu=HALF, bv=max(HALF, 0.5 * (up_ - lo_) - 2), tag="inferred", ink=True))
    out.sort(key=lambda d: -d["u"])
    return out

# ---------- knee (page row runs, read on crops knee_pg4, kz, kt) ----------
KNEE = {
    "upper": [  # left strand; dash A'' (2140..2196), gap 2129..2139, dash A' (2088..2128), gap 2081..2087, dash A1 (2056..2080)
        (2193.5, 2196, "sep"), (2191.0, 2190, "sep"), (2190.5, 2172, "sep"), (2193.5, 2168, "sep"), (2193.5, 2164, "sep"),
        (2193.5, 2160, "sep"), (2190.5, 2156, "sep"), (2187.5, 2152, "sep"), (2185.5, 2148, "sep"), (2183.5, 2140, "sep"),
        (2176.0, 2134, "gap"),
        (2169.0, 2128, "sep"), (2171.5, 2124, "sep"), (2170.0, 2120, "sep"), (2167.5, 2116, "sep"), (2166.5, 2112, "sep"),
        (2164.0, 2108, "sep"), (2158.0, 2096, "sep"), (2154.5, 2092, "sep"), (2153.5, 2088, "sep"),
        (2144.0, 2084, "gap"),
        (2134.5, 2080, "sep"), (2135.5, 2076, "sep"), (2131.0, 2072, "sep"), (2127.5, 2068, "sep"), (2122.5, 2064, "sep"),
        (2114.5, 2060, "sep"), (2110.5, 2056, "sep")],
    "average": [
        (2209.5, 2190, "sep"), (2207.5, 2175, "merged"), (2205.5, 2160, "sep"), (2203.5, 2156, "sep"), (2202.5, 2152, "sep"),
        (2200.5, 2148, "sep"), (2198.5, 2140, "sep"), (2197.0, 2136, "sep"), (2194.5, 2132, "sep"), (2191.5, 2128, "sep"),
        (2191.5, 2124, "sep"), (2188.5, 2120, "sep"), (2185.5, 2116, "sep"), (2184.5, 2112, "sep"), (2181.5, 2108, "sep"),
        (2175.5, 2096, "sep"), (2172.0, 2092, "sep"), (2169.0, 2088, "sep"), (2162.5, 2084, "sep"), (2160.5, 2080, "sep"),
        (2157.5, 2076, "sep"), (2153.5, 2072, "sep"), (2149.0, 2068, "sep"), (2144.5, 2064, "sep"), (2141.5, 2060, "sep"),
        (2136.0, 2056, "sep")],
    "lower": [  # right strand; dash C3 below the circle at (2229, 2179) from 2216, gap 2200..2214, circle, dash C3 2152..2162,
                # gap 2141..2151, dash C2 2096..2140, gap 2085..2095, dash C1 2047..2084 from the circle at (2162, 2033)
        (2227.5, 2218, "sep"), (2224.0, 2207, "gap"), (2229.0, 2179, "circle"), (2222.5, 2160, "sep"), (2220.5, 2156, "sep"),
        (2223.5, 2152, "sep"), (2217.0, 2146, "gap"),
        (2212.0, 2140, "sep"), (2212.5, 2136, "sep"), (2210.5, 2132, "sep"), (2208.5, 2128, "sep"), (2206.5, 2124, "sep"),
        (2205.5, 2120, "sep"), (2202.5, 2116, "sep"), (2200.5, 2112, "sep"), (2197.5, 2108, "sep"), (2194.5, 2096, "sep"),
        (2188.0, 2090, "gap"),
        (2182.0, 2084, "sep"), (2183.5, 2080, "sep"), (2181.5, 2076, "sep"), (2178.5, 2072, "sep"), (2176.0, 2068, "sep"),
        (2173.5, 2064, "sep"), (2169.0, 2060, "sep"), (2166.0, 2056, "sep"), (2163.0, 2052, "sep"), (2158.0, 2047, "sep")],
}
# knee entrance (page column runs u 2030..2140; the three curves partly run together with the dashed grid line at v 2025-2033)
ENTRANCE = {
    "upper": [(2100.0, 2051.5, 7, "sep"), (2090.0, 2050.0, 7, "sep"), (2080.0, 2044.5, 7, "merged"), (2070.0, 2032.5, 8, "merged"),
              (2060.0, 2024.5, 8, "merged"), (2045.0, 2015.0, 9, "merged")],
    "average": [(2125.0, 2045.0, 8, "inferred"), (2110.0, 2036.0, 8, "inferred"), (2090.0, 2024.5, 8, "sep"), (2060.0, 2009.5, 8, "merged"),
                (2045.0, 2001.0, 9, "merged")],
    "lower": [(2150.0, 2036.0, 8, "circle"), (2136.0, 2027.5, 6, "sep"), (2130.0, 2029.5, 6, "sep"), (2120.0, 2026.5, 6, "sep"),
              (2114.0, 2024.5, 6, "sep"), (2110.0, 2021.5, 6, "sep"), (2103.0, 2018.0, 6, "sep"), (2095.0, 2013.5, 6, "gap"),
              (2085.0, 2009.5, 6, "sep"), (2080.0, 2008.5, 6, "sep"), (2075.0, 2005.5, 6, "sep"), (2070.0, 2003.5, 6, "sep"),
              (2065.0, 2002.5, 6, "sep"), (2060.0, 2000.5, 6, "sep"), (2055.0, 1996.5, 6, "sep"), (2050.0, 1994.5, 6, "sep"),
              (2045.0, 1991.5, 6, "sep")],
}
# top bend and coarse end (page row runs v 1514..1690 on crops tb, ci_810; grid rows 1517-1525, 1593-1600, 1640-1648 skipped)
TOP = {
    "upper": [(824.0, 1690, 6, "sep"), (822.5, 1686, 6, "sep"), (819.5, 1682, 6, "sep"), (816.5, 1678, 6, "sep"), (810.5, 1674, 6, "sep"),
              (808.5, 1670, 6, "sep"), (807.5, 1666, 6, "sep"), (802.5, 1654, 7, "sep"), (804.5, 1650, 7, "sep"),
              (790.5, 1638, 7, "merged"), (790.5, 1634, 7, "merged"), (792.5, 1630, 7, "merged"), (793.5, 1626, 7, "merged"),
              (793.5, 1622, 7, "merged"), (790.5, 1618, 7, "merged"), (790.5, 1614, 7, "merged"), (790.5, 1610, 7, "merged"),
              (787.5, 1606, 7, "merged"), (787.5, 1602, 7, "merged"), (786.5, 1590, 7, "merged"), (786.5, 1582, 7, "merged"),
              (784.5, 1574, 7, "merged"), (784.5, 1562, 7, "merged"), (783.5, 1554, 7, "merged"), (783.5, 1542, 7, "merged"),
              (783.5, 1534, 7, "merged"), (781.5, 1526, 7, "merged"), (781.5, 1518, 7, "merged"), (780.5, 1514.5, 5, "merged")],
    "lower": [(826.5, 1674, 6, "sep"), (823.5, 1670, 6, "sep"), (820.5, 1666, 6, "sep"), (819.5, 1662, 6, "sep"),
              (822.5, 1658, 6, "sep"), (820.5, 1654, 6, "sep"), (814.5, 1650, 6, "sep"), (814.0, 1638, 6, "sep"),
              (813.0, 1634, 6, "sep"), (813.0, 1630, 6, "sep"), (811.0, 1626, 6, "sep"), (811.0, 1622, 6, "sep"),
              (810.5, 1618, 6, "sep"), (809.0, 1610, 6, "gap"), (807.5, 1602, 7, "sep"), (801.5, 1590, 6, "sep"),
              (799.5, 1586, 6, "sep"), (799.5, 1582, 6, "sep"), (801.5, 1578, 6, "sep"), (796.5, 1574, 6, "sep"),
              (796.5, 1570, 6, "sep"), (795.5, 1566, 6, "sep"), (795.5, 1562, 6, "sep"), (793.5, 1558, 7, "merged"),
              (786.0, 1554, 9, "merged"), (786.0, 1542, 9, "merged"), (786.0, 1530, 9, "merged"), (785.0, 1518, 9, "merged"),
              (780.5, 1514.5, 9, "merged")],
}
def top_average():
    """the solid curve is not seen on its own in the top bend: between the dashed curves, bound to either."""
    up = {v: u for u, v, b, t in TOP["upper"]}; lo = {v: u for u, v, b, t in TOP["lower"]}
    out = []
    for v in sorted(set(up) | set(lo), reverse=True):
        if v > 1674:
            continue
        uu = np.interp(v, sorted(up), [up[k] for k in sorted(up)])
        ll = np.interp(v, sorted(lo), [lo[k] for k in sorted(lo)])
        if v >= 1645:      # one continuous band: between the dashed curves
            out.append(dict(u=0.5 * (uu + ll), v=float(v), bu=max(7.0, 0.5 * abs(ll - uu) + 1), bv=HALF, tag="inferred", ink=True))
        elif v >= 1600:    # two strands on the page; the left one (on the 100 line) is wider and carries upper and average
            vi = int(round(v)); row = page[vi, 774:806]; idx = np.where(row)[0]
            runs, s0 = [], idx[0]
            for a, b in zip(idx, idx[1:]):
                if b > a + 1:
                    runs.append((s0, a)); s0 = b
            runs.append((s0, idx[-1]))
            R = 774 + runs[0][1]
            out.append(dict(u=max(uu, R - 5.5), v=float(v), bu=7.0, bv=HALF, tag="merged", ink=True))
        elif v >= 1555:
            out.append(dict(u=uu + 6.0, v=float(v), bu=7.0, bv=HALF, tag="merged", ink=True))
        else:
            out.append(dict(u=0.5 * (uu + ll), v=float(v), bu=9.0, bv=HALF, tag="merged", ink=True))
    # rows 1678..1690: the band's middle (page rows 811-850 .. 833-861)
    extra = [(830.5, 1678.0), (833.5, 1682.0), (836.5, 1686.0), (838.5, 1690.0)]
    return [dict(u=a, v=b, bu=9.0, bv=HALF, tag="inferred", ink=True) for a, b in reversed(extra)] + out

def manual(lst, default_b=HALF):
    out = []
    for item in lst:
        if len(item) == 3:
            u, v, tag = item; b = default_b
        else:
            u, v, b, tag = item
        out.append(dict(u=float(u), v=float(v), bu=float(b), bv=float(b), tag=tag, ink=tag not in ("gap", "circle")))
    return out

def polyline(series):
    pts = tail_end()
    if series == "lower":
        pts += tail_rows(series, 2848, 2220)
    else:
        pts += tail_rows(series, 2848, 2198)
    pts += manual(KNEE[series])
    pts += manual(ENTRANCE[series])
    pts += steep_cols(series, 2030, 846 if series != "upper" else 846)
    if series == "average":
        pts += top_average()
    else:
        pts += manual(TOP[series])
    for p in pts:
        p["q"], p["y"] = qy(p["u"], p["v"])
    return pts

def crossings(pts, key, target):
    out = []
    for a, b in zip(pts, pts[1:]):
        if (a[key] - target) * (b[key] - target) <= 0 and a[key] != b[key]:
            f = (target - a[key]) / (b[key] - a[key])
            out.append((pts.index(a), f))
    return out

def at(pts, i, f):
    a, b = pts[i], pts[i + 1]
    d = {k: a[k] + f * (b[k] - a[k]) for k in ("u", "v", "q", "y")}
    near = a if f < 0.5 else b
    d["bu"], d["bv"] = max(a["bu"], b["bu"]), max(a["bv"], b["bv"])
    d["tag"] = near["tag"] if a["tag"] == b["tag"] else (a["tag"] + "/" + b["tag"])
    d["ink"] = a["ink"] and b["ink"]
    d["i"], d["f"] = i, f
    return d

def dash_end(pts, i, f):
    """nearest vertex on ink (a dash end) along the polyline from segment i (rule 7)."""
    best = None
    for j, p in enumerate(pts):
        if not p["ink"]:
            continue
        dist = abs((j - (i + f)))
        if best is None or dist < best[0]:
            best = (dist, j)
    return best[1]

NOTES = {"sep": "on the curve's own ink",
         "gap": "",
         "merged": "the three curves run together here; bound widened to the band",
         "inferred": "solid line not seen on its own here: placed between the dashed curves, bound widened",
         "circle": ""}

def samples(series):
    pts = polyline(series)
    q0, q1 = pts[0]["q"], pts[-1]["q"]
    out = []
    first = dict(pts[0]); first["note"] = "first point: where the ink starts at the fine end (the three curves run together there)"
    out.append(("trace", first))
    ks = range(math.ceil(q0 / 0.05 - 1e-9), math.floor(q1 / 0.05 + 1e-9) + 1)
    grain = []
    for k in ks:
        tq = round(k * 0.05, 4)
        cr = crossings(pts, "q", tq)
        if not cr:
            continue
        i, f = cr[0]
        d = at(pts, i, f); d["target"] = f"x=10^{tq:+.2f}"
        grain.append(d)
    seq = []
    for j, d in enumerate(grain):
        seq.append(d)
        if j + 1 < len(grain):
            y0, y1 = d["y"], grain[j + 1]["y"]
            if y1 - y0 > 10:
                for yt in range(int(math.floor(y0 / 5) + 1) * 5, int(math.ceil(y1 / 5)) * 5, 5):
                    if not (y0 < yt < y1):
                        continue
                    # crossing of percent yt between the two grain-size samples along the polyline
                    lo_i = d["i"]; hi_i = grain[j + 1]["i"] + 1
                    cr = [c for c in crossings(pts[lo_i:hi_i + 1], "y", yt)]
                    if not cr:
                        continue
                    ii, ff = cr[0]
                    e = at(pts, lo_i + ii, ff); e["target"] = f"y={yt}"
                    seq.append(e)
    kept, used = [], set()
    for d in seq:
        notes = [d["target"]]
        d["param"] = d["i"] + d["f"]
        if series != "average" and not d["ink"] and "merged" not in d["tag"]:
            j = dash_end(pts, d["i"], d["f"])
            p = pts[j]
            notes.append(f"in a dash gap at ({d['u']:.1f}, {d['v']:.1f}); moved to the nearest dash end (rule 7)")
            d = dict(d, u=p["u"], v=p["v"], bu=p["bu"], bv=p["bv"], tag=p["tag"], param=float(j))
            d["note_extra"] = notes[-1]
            if j in used:
                DROPPED.append((series, d["target"], j)); continue
            used.add(j)
        tagnote = NOTES.get(d["tag"].split("/")[0], "") if "/" not in d["tag"] else \
            ("; ".join(sorted(set(NOTES.get(t, "") for t in d["tag"].split("/")) - {""})))
        uu, vv = int(round(d["u"])), int(round(d["v"]))
        if not page[vv - 2:vv + 3, uu - 2:uu + 3].any():
            # the centre of a merged band fell in white between two strands: move along the row onto the strand on the
            # series' side (upper: left, the others: right), never more than 12 px
            dirs = (-1, 1) if series == "upper" else (1, -1)
            moved = False
            for sgn in dirs:
                for k in range(1, 13):
                    x = uu + sgn * k
                    if page[vv, x]:
                        a = b = x
                        while page[vv, a - 1]: a -= 1
                        while page[vv, b + 1]: b += 1
                        newu = 0.5 * (a + b) if b - a + 1 <= 14 else x + sgn * 2.0
                        notes.append(f"band centre ({d['u']:.1f}) in white between strands; moved onto the strand at {newu:.1f}")
                        d = dict(d, u=newu); moved = True
                        break
                if moved:
                    break
            if not moved:
                notes.append("no ink within 2 px of the centre")
        d["note"] = "; ".join(x for x in notes + [tagnote] if x)
        kept.append(d)
    kept.sort(key=lambda d: d["param"])
    for d in kept:
        out.append(("trace", d))
    last = dict(pts[-1]); last["note"] = "last point: where the ink ends at the coarse end, on the 100 percent line" + \
        ("" if series == "upper" else " (the three curves run together there)")
    out.append(("trace", last))
    return pts, out

def knee(pts, vmin, vmax):
    """the point where the drawn line runs at 45 degrees on the page between its two straight stretches"""
    cand = [k for k in range(1, len(pts) - 1) if vmin <= pts[k]["v"] <= vmax]
    best = None
    for k in cand:
        a, b = pts[max(k - 3, 0)], pts[min(k + 3, len(pts) - 1)]
        du, dv = b["u"] - a["u"], b["v"] - a["v"]
        if du == 0 and dv == 0:
            continue
        ang = abs(math.degrees(math.atan2(abs(dv), abs(du))) - 45)
        if best is None or ang < best[0]:
            best = (ang, k)
    return pts[best[1]]

MARKERS = [  # circles, centres read on crops m1, m2, m3, kt, ci_2900
    ("lower", 2162.0, 2033.0, 4.0, "circle on the lower dashed curve at the knee; the curve passes through it"),
    ("lower", 1714.0, 1891.0, 4.0, "circle touching the outer (upper on the page) edge of the lower dashed curve, centre about 11 px outside its centreline"),
    ("upper", 1560.0, 1906.0, 4.0, "circle touching the outer (lower on the page) edge of the upper dashed curve, centre about 8 px outside its centreline"),
    ("lower", 2229.0, 2179.0, 6.0, "circle on the right-hand (lower) dashed curve where the curves turn down; partly merged with the ink, centre uncertain"),
    ("upper", 2229.0, 2904.0, 6.0, "circle on the left edge of the band near the fine end, where the three curves run together; series by its side of the band, partly merged"),
]

DROPPED = []
rows = []
for series in ("average", "upper", "lower"):
    pts, tr = samples(series)
    for n, (kind, d) in enumerate(tr, 1):
        rows.append(dict(figure_id="FA-6", panel=1, series_id=series, point_kind="trace", sequence=n,
                         pixel_u=round(d["u"], 1), pixel_v=round(d["v"], 1), u_bound_px=round(d["bu"], 1),
                         v_bound_px=round(d["bv"], 1), symbol="", note=d["note"]))
    fpts = [("first point", pts[0]), ("knee (fine side, 45 degrees on the page)", knee(pts, 2040, 2200)),
            ("knee (coarse side, 45 degrees on the page)", knee(pts, 1640, 1720)), ("last point", pts[-1])]
    for n, (role, p) in enumerate(fpts, 1):
        b = 4.0 if role in ("first point",) else (5.0 if role == "last point" and series == "upper" else 9.0)
        bv = 3.0 if role == "first point" else (b if "knee" not in role else 12.0)
        bu = b if "knee" not in role else 12.0
        merged = " (the three curves run together there)" if (role == "first point" or (role == "last point" and series != "upper")) else ""
        rows.append(dict(figure_id="FA-6", panel=1, series_id=series, point_kind="feature", sequence=n,
                         pixel_u=round(p["u"], 1), pixel_v=round(p["v"], 1), u_bound_px=bu, v_bound_px=bv,
                         symbol="", note=role + merged + ("; knee position is a construction, bound covers the bend" if "knee" in role else "")))
nm = {}
for s, u, v, b, note in MARKERS:
    nm[s] = nm.get(s, 0) + 1
    rows.append(dict(figure_id="FA-6", panel=1, series_id=s, point_kind="marker", sequence=nm[s], pixel_u=u, pixel_v=v,
                     u_bound_px=b, v_bound_px=b, symbol="circle", note=note))
cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
with open(WS / "out/FA-6/points-p1.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n"); w.writeheader(); w.writerows(rows)
# polylines for the overlay
json.dump({s: [[p["u"], p["v"], p["tag"]] for p in polyline(s)] for s in ("average", "upper", "lower")},
          open(WS / "out/FA-6/helpers/polylines.json", "w"))
from collections import Counter
print(Counter((r["series_id"], r["point_kind"]) for r in rows))
print("dropped (moved onto a dash end already sampled):", DROPPED)
print("no ink:", [(r["series_id"], r["sequence"]) for r in rows if "no ink" in r["note"]])
