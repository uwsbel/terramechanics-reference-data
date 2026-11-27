"""Sample the three trace centerlines of Figure 2-54 in drawing order."""
import math
from PIL import Image, ImageDraw

import numpy as np

from calibrate_f254 import G, IMAGE, OUT, SCAN, V, AxisKnots, check_y_knots, csv_write
from calibrate_axes import load_anchors, piecewise_rows

# Guides disambiguate ink when a timing line, dashed datum, or ruler is nearby.
# Internal pairs are (clockwise-view x, original-page u).
GUIDES = {
    1: [
        ("x", [(1475,866),(1633,865),(1786,861),(1830,859),(1890,859),(1938,857)]),
        ("u", [(1942,842),(1944,822),(1951,780),(1955,752),(1960,706),(1965,665)]),
        ("x", [(1965,665),(1970,652),(1976,652),(1988,668),(2010,700),(2030,728),
               (2052,759),(2071,779),(2104,789),(2119,792),(2148,788),(2209,781),
               (2225,779),(2248,765),(2257,760),(2295,762),(2392,768),(2550,788),
               (2708,808),(2800,828),(2872,841),(3035,840),(3192,838)])],
    2: [
        ("x", [(1481,1334),(1637,1330),(1714,1329),(1790,1327),(1840,1328),
               (1887,1330),(1908,1328),(1926,1324),(1942,1320)]),
        ("u", [(1943,1320),(1947,1300),(1950,1274),(1955,1224),(1965,1139),
               (1972,1090),(1979,1050),(1984,1022)]),
        ("x", [(1984,1022),(1986,1017),(1991,1028),(2004,1053),(2020,1093),
               (2047,1166),(2071,1211),(2092,1236),(2120,1261),(2127,1264),
               (2160,1256),(2200,1246),(2248,1241),(2260,1244),(2290,1255),
               (2338,1252),(2400,1255),(2465,1259),(2540,1263),(2610,1277),
               (2707,1293),(2795,1303),(2876,1307),(2990,1313),(3193,1316)])],
    3: [
        ("x", [(1490,2352),(1648,2349),(1800,2346),(1850,2346),(1925,2345),
               (1944,2345),(1954,2340),(1960,2334)]),
        ("u", [(1965,2332),(1969,2315),(1973,2297),(1975,2280),(1984,2260),(1986,2210),(1988,2160),
               (1989,2110),(1991,2050),(1995,1940),(1997,1850),(2000,1780),
               (2004,1690),(2006,1610),(2009,1540),(2010,1505),(2014,1476)]),
        ("x", [(2014,1476),(2016,1468),(2019,1480),(2026,1502),(2030,1515)]),
        ("u", [(2030,1515),(2034,1535),(2040,1570),(2046,1615),(2050,1680),
               (2055,1735),(2060,1795),(2064,1880),(2068,1950),(2073,2010),
               (2078,2070),(2081,2130),(2085,2195),(2090,2255),(2094,2295),
               (2098,2318),(2102,2328)]),
        ("x", [(2102,2328),(2110,2339),(2140,2346),(2190,2350),(2256,2348),
               (2408,2342),(2570,2338),(2722,2332),(2880,2331),(2970,2320),
               (3045,2313),(3090,2310),(3145,2314),(3203,2318)])],
}

ZERO_GLYPH = {1: (1795,1823), 2: (1800,1825), 3: (1807,1836)}
FEATURES = {
    1: [
        (1942, 841, "knee, onset | lowest visible rising ink across short gap at 10 ms"),
        (1972, 652, "peak | main flat crest"),
        (2123, 791, "knee, minimum | broad saddle after main peak"),
        (2224, 779, "knee | starts steeper climb to secondary crest"),
        (2264, 761, "peak | broad secondary crest"),
        (2714, 809, "knee | descent steepens"),
        (2855, 839, "knee | levels into dashed zero line"),
    ],
    2: [
        (1925, 1325, "knee, onset | rounded departure from pre-event baseline"),
        (1986, 1016, "peak | main pointed crest"),
        (2048, 1169, "knee | descending slope eases"),
        (2124, 1271, "knee, minimum | trough after main peak"),
        (2245, 1241, "peak | secondary crest at the 30 ms timing line"),
        (2293, 1255, "knee, minimum | shallow trough"),
        (2343, 1252, "peak | small shoulder after the shallow trough"),
        (2542, 1263, "knee | starts steeper descent"),
        (2680, 1290, "knee | descent eases"),
    ],
    3: [
        (1941, 2344, "knee, onset | rounded departure from pre-event baseline"),
        (2015, 1470, "peak | main pointed crest"),
        (2108, 2336, "knee | falling flank turns into tail near the 20 ms timing line"),
        (2230, 2348, "knee, minimum | broad shallow undershoot"),
        (2886, 2331, "knee | begins broad rise from near the dashed zero line"),
        (3094, 2311, "peak | broad late crest"),
    ],
}


def segments(profile, start, threshold=130):
    dark = np.asarray(profile) <= threshold
    stops = np.flatnonzero(np.diff(np.pad(dark, 1)))
    return [(a+start, b-1+start) for a, b in stops.reshape((-1, 2))]


def read_cal(panel):
    import json

    path = OUT / f"cal-p{panel}"
    c = json.loads((path / "calibration.json").read_text())
    a = load_anchors(path)
    time = AxisKnots(a, "x_value", "x_source", c["ax"][:2], SCAN)
    g = check_y_knots(a, c["ay"])
    return c, time, g


def timing_at(c, u):
    return np.array([V-line["v_at_u0"]-line["slope_dv_du"]*u for line in c["horizontal_lines"]])


def dashed_at(c, x):
    d = c["vertical_lines"][0]
    return d["u_at_v0"] + d["slope_du_dv"]*(V-x)


def guide_interp(points, mode):
    points = np.array(points, float)
    if mode == "u":
        points = points[:, ::-1]
    direction = 1 if points[-1,0] > points[0,0] else -1
    grid = np.arange(points[0,0], points[-1,0]+direction, direction)
    order = slice(None, None, direction)
    return zip(grid.astype(int), np.interp(grid, points[order,0], points[order,1]))


def read_section(panel, c, mode, points):
    main = []
    for along, z in guide_interp(points, mode):
        x, u = (along, z) if mode == "x" else (z, along)
        grid = timing_at(c, u)
        distance = float(np.min(np.abs(grid-x)))
        dash = dashed_at(c, x)
        left, right = round(z)-24, round(z)+25
        if mode == "x":
            if distance < 4 or (u > dash and ZERO_GLYPH[panel][0] <= x <= ZERO_GLYPH[panel][1]):
                main.append((x, float("nan")))
                continue
            profile = G[left:right,along].copy()
        else:
            profile = G[along,left:right]
        options = []
        for a,b in segments(profile,left):
            if a == left or b == right-1 or a == b:
                continue
            center = (a+b)/2
            if mode == "x" and x < 1957 and u-dash > 4 and a <= dash+1 <= b:
                # The upper edge can be the dash. The lower edge remains
                # visible, so judge the trace core from that side of the merge.
                center = b-3.5
            if mode == "u":
                # A narrow timing line on its own is not the steep trace.
                if np.min(np.abs(grid-center)) < 2 and b-a+1 <= 6:
                    continue
                if b-a > 22:
                    continue
            if abs(z-center) <= (13 if mode == "x" else 12):
                options.append((abs(z-center), center))
        if not options:
            main.append((along, float("nan")) if mode == "x" else (float("nan"), along))
            continue
        _, center = min(options)
        main.append((along, center) if mode == "x" else (center,along))
    return main


def ink_path(panel, c):
    trace = []
    for n, (mode, nominal) in enumerate(GUIDES[panel]):
        raw = np.asarray(read_section(panel, c, mode, nominal), dtype=float)
        j = 1 if mode == "x" else 0
        valid = np.isfinite(raw[:,j])
        measured = np.flatnonzero(valid)
        filled = np.interp(np.arange(len(raw)), measured, raw[valid,j])
        smooth = np.convolve(np.pad(filled, 2, mode="edge"),
                             [.08,.22,.4,.22,.08], mode="valid")
        # Keep the middle of the visible ink and bridge only short overlaps
        # with timing lines. Long glyph occlusions are handled at sample time.
        raw[:,j] = smooth
        if panel == 1 and n == 1:
            # The scan has a visible break between the leveling lead and rising stroke.
            trace.append((float("nan"), float("nan")))
        if n and np.all(np.isfinite(trace[-1])) and np.linalg.norm(raw[0] - trace[-1]) > 14:
            print("Recheck section join", panel, n, trace[-1], raw[0])
        trace.extend(raw.tolist())
        runs = segments(np.where(valid,255,0),0)
        print(panel,n,mode,"missing index runs > 6",[(a,b) for a,b in runs if b-a>5])
    return np.asarray(trace)


def find_all(path, coord, level):
    """Find occurrences along the stroke, including any near-vertical ones."""
    hits = []
    for i in np.flatnonzero(((coord[:-1] < level) & (coord[1:] >= level)) |
                            ((coord[:-1] > level) & (coord[1:] <= level))):
        f = (level-coord[i])/(coord[i+1]-coord[i])
        hit = (i+f, path[i]+f*(path[i+1]-path[i]))
        if not hits or np.linalg.norm(hit[1]-hits[-1][1]) > 4:
            hits.append(hit)
    return hits


def gray_at(x, u):
    ix, iy = int(x), int(u)
    fx, fy = x-ix, u-iy
    return ((1-fy)*((1-fx)*float(G[iy,ix])+fx*float(G[iy,ix+1])) +
            fy*((1-fx)*float(G[iy+1,ix])+fx*float(G[iy+1,ix+1])))


def trace_end(c, path, side):
    """Frame intercept of the trace center, from the visible adjacent ink."""
    i = 0 if side == "first" else -1
    x, u = path[i]
    j = 0 if side == "first" else -1
    x = timing_at(c, u)[j]
    nearest = np.flatnonzero(np.isfinite(path[:,0]) & (abs(path[:,0]-x) < 20))
    u = float(np.median(path[nearest,1]))
    return (0 if i == 0 else len(path)-1), np.array([timing_at(c,u)[j],u])


def closest(path, gx, gu):
    i = int(np.nanargmin(np.sum((path-np.array([gx,gu]))**2,axis=1)))
    point = path[i].copy()
    if gray_at(gx, gu) <= 130 and np.linalg.norm(point-[gx,gu]) <= 7:
        point = np.array([gx,gu],dtype=float)
    return i, point


def tangent(path, index):
    mid = round(index)
    subset = path[max(0,mid-8):mid+9]
    subset = subset[np.isfinite(subset[:,0])]
    estimate = subset[-1]-subset[0]
    return estimate/np.linalg.norm(estimate)


def widths(c, path, index, pos, panel):
    x, u = pos
    vec = tangent(path,index)
    nx, nu = -vec[1], vec[0]
    grid_gap = np.min(np.abs(timing_at(c,u)-x))
    dash_gap = abs(dashed_at(c,x)-u)
    grid_overlap = grid_gap <= 5
    dash_overlap = dash_gap <= (5.5 if panel != 2 else 6.5)
    ruler_overlap = x < 1923 and ZERO_GLYPH[panel][1]+1 <= x and u >= dashed_at(c,x)
    labels = []
    if grid_overlap:
        labels.append("on timing line")
    if dash_overlap:
        labels.append("on dashed zero line")
    if ruler_overlap and x < 1904:
        labels.append("shared ink with ruler zero tick")
    offsets = np.arange(-16,16.01,.25)
    core = [s for s in offsets if gray_at(x+s*nx,u+s*nu) <= 130]
    width = None
    if core:
        i = min(range(len(core)),key=lambda j:abs(core[j]))
        l, r = i, i
        while l and core[l]-core[l-1] < .26:
            l -= 1
        while r+1 < len(core) and core[r+1]-core[r] < .26:
            r += 1
        if core[l] > offsets[0] and core[r] < offsets[-1]:
            width = (core[r]-core[l]+.25)/2
    if width is None or (grid_overlap and width > 10):
        # A grid crossing can have no isolated transverse edge. Measure the
        # nearby trace away from grid ink and add the overlap allowance below.
        candidates = []
        for i in (round(index)-8, round(index)+8, round(index)-13, round(index)+13):
            if 0 <= i < len(path) and np.isfinite(path[i][0]):
                xx, yy = path[i]
                if np.min(np.abs(timing_at(c,yy)-xx)) <= 6:
                    continue
                local = [s for s in offsets if gray_at(xx+s*nx,yy+s*nu) <= 130]
                if not local:
                    continue
                closest_index = min(range(len(local)), key=lambda j: abs(local[j]))
                first = last = closest_index
                while first > 0 and local[first]-local[first-1] < .26:
                    first -= 1
                while last+1 < len(local) and local[last+1]-local[last] < .26:
                    last += 1
                candidates.append((local[last]-local[first]+.25)/2)
        if not candidates:
            # The immediate neighborhood also merges. Use the observed
            # dark core size if only one edge is separable.
            if core:
                width = max(abs(core[0]),abs(core[-1]))
            else:
                raise ValueError(f"No transverse ink at {panel}, {pos}, {index}")
        else:
            width = float(np.median(candidates))
    bu = bv = width
    if grid_overlap:
        bv += 2.5
        bu += 1.5
    if dash_overlap:
        bu += 2
        bv += .5
    if ruler_overlap and x < 1904:
        bu += 2
        bv += 1
    return bu, bv, labels


def sampled_rows(panel, c, time, decel, path):
    T, Y = [
        np.asarray([axis.value(u,V-x)[0] if np.isfinite(x) else np.nan for x,u in path])
        for axis in (time,decel)
    ]
    first, last = [trace_end(c,path,side) for side in ("first","last")]
    picks = [(*first,"trace","first visible timed point"), (*last,"trace","right end merged with frame")]
    feature_picks = [(*first,"feature","first | trace at first timing line right of break marks"),
                     (*last,"feature","last | right end of ink at frame")]
    feature_picks[1:1] = [(*closest(path,x,u),"feature",role) for x,u,role in FEATURES[panel]]
    onset = feature_picks[1]
    peak = feature_picks[2]
    start = math.floor(2*(T[onset[0]]-2))/2
    stop = T[peak[0]]+5
    fixed = [*range(-18, math.ceil(start),2), *np.arange(start,math.ceil(2*stop)/2+.0001,.5),
             *range(math.floor(stop)+1,21), *range(22,90,2)]
    fixed = sorted(set(t for t in fixed if t < 90))
    omissions = []
    for t in fixed:
        hits = find_all(path,T,t)
        if t == 10 and panel == 1 and not hits:
            # Read the preceding timed stroke at the 10 ms line. The scan has
            # a gap before the disjoint start of the rising ink.
            idx = np.flatnonzero(~np.isfinite(path[:,0]))[0]-1
            u = path[idx,1]
            hits = [(idx,np.array([timing_at(c,u)[3],u]))]
        if not hits:
            omissions.append((t,"no supported crossing"))
        for index, point in hits:
            x,u = point
            if ZERO_GLYPH[panel][0] <= x <= ZERO_GLYPH[panel][1] and u > dashed_at(c,x):
                omissions.append((t,"trace obscured by printed 0"))
                continue
            picks.append((index,point,"trace",""))
    step = 5 if panel == 3 else 2
    for y in range(step, math.floor(np.nanmax(Y))+1,step):
        for index, point in find_all(path,Y,y):
            x,u = point
            if T[round(index)] > stop:
                continue
            i = round(index)
            left, right = max(0,i-6), min(i+6,len(path)-1)
            local_t, local_y = T[right]-T[left], Y[right]-Y[left]
            if not np.isfinite(local_t) or abs(local_y) < .05:
                continue
            if abs(step*local_t/local_y) >= .5:
                continue
            if any(np.linalg.norm(point-p[1]) < 1.25 for p in picks):
                continue
            picks.append((index,point,"trace",f"{y} g steep-flank sample"))
    rows = []
    for i, (index,pos,kind,note) in enumerate(sorted(picks+feature_picks, key=lambda p:p[0]),1):
        x,u = pos
        bu,bv,flags = widths(c,path,index,pos,panel)
        if any(flag in note for flag in ("broad","flat","rounded")):
            bv += 2
        if gray_at(x,u) > 160:
            # At a shared grid crossing, an adjacent trace fragment can fix the
            # center. Otherwise move only within the visible core nearest it.
            nx, nu = -tangent(path,index)[1], tangent(path,index)[0]
            offsets = np.arange(-2,2.1,.25)
            good = [q for q in offsets if gray_at(x+q*nx,u+q*nu) <= 130]
            if not good:
                print("Off ink",panel,kind,round(time.value(u,V-x)[0],2),pos,note,flags)
                omissions.append((round(time.value(u,V-x)[0],2),"no identifiable trace ink at sample"))
                if kind == "feature":
                    raise ValueError("Selected feature must be on the trace")
                continue
            offset = min(good,key=abs)
            x += offset*nx
            u += offset*nu
        rows.append(dict(figure_id="F2-54",panel=panel,series_id={1:"r53958",2:"r54025",3:"r5465"}[panel],
                         point_kind=kind,sequence=len(rows)+1,pixel_u=round(float(u),2),
                         pixel_v=round(float(V-x),2),u_bound_px=round(float(bu),2),
                         v_bound_px=round(float(bv),2),symbol="",note=" | ".join(filter(None,[note,*flags]))))
    print(panel, "sample window", start, round(stop,3), "omissions", omissions)
    return rows


def overlay(panel, rows):
    # The overlay retains the unrotated scan orientation.
    bounds = {1: (294, 1270, 930, 3850), 2: (927, 1270, 1380, 3850),
              3: (1375, 1270, 2467, 3850)}[panel]
    base = Image.open(IMAGE).convert("RGBA").crop(bounds)
    marks = Image.new("RGBA", base.size)
    draw = ImageDraw.Draw(marks)
    origin_u, origin_v = bounds[:2]
    for row in rows:
        u = row["pixel_u"] - origin_u
        v = row["pixel_v"] - origin_v
        bu, bv = row["u_bound_px"], row["v_bound_px"]
        feature = row["point_kind"] == "feature"
        color = (0, 142, 208, 200) if feature else (223, 75, 19, 160)
        draw.line((u-bu, v, u+bu, v), fill=color)
        draw.line((u, v-bv, u, v+bv), fill=color)
        radius = 6 if feature else 2
        draw.ellipse((u-radius,v-radius,u+radius,v+radius), outline=color, width=2 if feature else 1)
    Image.alpha_composite(base, marks).convert("RGB").save(OUT/f"overlay-p{panel}.png")


def main():
    for panel in (1,2,3):
        c, time, decel = read_cal(panel)
        path = ink_path(panel,c)
        rows = sampled_rows(panel,c,time,decel,path)
        csv_write(OUT/f"points-p{panel}.csv",rows)
        overlay(panel, rows)
        extra = piecewise_rows(c,time,decel,rows)
        csv_write(OUT/f"points-p{panel}-native.csv",rows)
        print(panel,len(rows),"rows",extra,"extrapolated")


if __name__ == "__main__":
    main()


