"""Sample visible strokes on the requested time and load/depth increments."""
import csv
import math
from pathlib import Path

import numpy as np
from PIL import Image

from strut_calibration import axes, write_csv
from trace_reading import FIGURES, nearby_frame, rules_at, runs


# The two ends as read from the enlarged images. Coordinates are in the working view.
ENDS = {
    (329, 1): ((930, 2310), (3355, 1226.5)),
    (330, 1): ((982, 1249.5), (2688, 1250.5)),
    (330, 2): ((979, 1668.5), (2685, 1634.5)),
    (330, 3): ((983, 2285.5), (2681, 2253.5)),
    (336, 1): ((1000, 1958), (3430, 905)),
    (337, 1): ((1004, 1356.5), (2763, 1237)),
    (337, 2): ((1008, 1778), (2763, 1547.5)),
    (337, 3): ((1014, 2264), (2765, 2057)),
}

# Ranges delimit flat extrema and allow use of the representative center of the ink.
FEATURES = {
    (329, 1): [
        ("knee", 1175, "initial slope eases"), ("knee", 1870, "middle shoulder"),
        ("knee", 2370, "approach to the broad crest"),
        ("peak", (2860, 2960), "broad crest near .08 s"),
    ],
    (330, 1): [
        ("knee", 1031, "initial rise steepens"), ("knee", 1143, "rise eases into first crest"),
        ("peak", (1205, 1260), "first crest"),
        ("knee, minimum", (1355, 1395), "shallow dip before the small rebound"),
        ("peak", (1408, 1450), "small rebound"),
        ("knee, minimum", (1500, 1555), "second dip"),
        ("peak", (1940, 2025), "broad main crest"),
        ("knee, minimum", (2182, 2220), "shallow dip"),
        ("peak", (2230, 2280), "small crest before descent"),
        ("knee", 2362, "descent steepens"),
    ],
    (330, 2): [
        ("knee", 1047, "leaves the near-zero shoulder"),
        ("knee", 1152, "rise eases into the first crest"),
        ("peak", (1260, 1350), "first broad crest"),
        ("knee, minimum", (1515, 1584), "shallow dip"),
        ("peak", (1900, 2019), "broad crest"),
        ("knee", 2478, "terminal fall steepens"),
    ],
    (330, 3): [
        ("knee", 1013, "initial rise steepens in compression"),
        ("knee", 1080, "steeper approach to the first compression crest"),
        ("knee, minimum", 1137, "first compression crest at the −80 lb ruling"),
        ("peak", (1410, 1474), "signed-load maximum between compression crests"),
        ("knee", 1588, "return toward compression eases"),
        ("knee, minimum", (2100, 2175), "largest compression magnitude"),
        ("knee", 2357, "unloading steepens"),
        ("knee", 2451, "unloading eases into the tail"),
    ],
    (336, 1): [
        ("knee", 1733, "initial rise eases"),
        ("knee", 2410, "change to a gentler rise"),
        ("knee", 3005, "approach to the terminal shoulder"),
        ("peak", "end", "terminal maximum where the trace meets the frame"),
    ],
    (337, 1): [
        ("knee, minimum", (1080, 1124), "first compression crest"),
        ("peak", (1196, 1226), "positive lobe below the zero ruling"),
        ("knee, minimum", (1280, 1330), "first small compression lobe"),
        ("peak", (1392, 1458), "shallow signed-load maximum"),
        ("knee, minimum", (1545, 1604), "second small compression lobe"),
        ("peak", 1796, "near-zero shoulder with partly merged ink"),
        ("knee", 1955, "compression starts increasing more rapidly"),
        ("knee", 2400, "rise eases toward the late compression crest"),
        ("knee, minimum", (2575, 2685), "largest compression magnitude"),
    ],
    (337, 2): [
        ("knee", 1068, "initial rise steepens"),
        ("peak", (1130, 1170), "first peak"),
        ("knee, minimum", (1215, 1265), "first trough"),
        ("knee", 1355, "first recovery eases"),
        ("knee", 1544, "second recovery eases"),
        ("peak", (1980, 2065), "small crest on upper shoulder"),
        ("knee, minimum", (2075, 2165), "slight sag on the shoulder"),
        ("peak", (2250, 2350), "second slight crest on the shoulder"),
        ("knee, minimum", (2460, 2556), "shallow dip before the terminal rise"),
        ("peak", "end", "terminal maximum"),
    ],
    (337, 3): [
        ("knee", 1054, "initial compression rise eases"),
        ("knee, minimum", (1170, 1230), "first compression crest"),
        ("peak", (1330, 1400), "signed-load maximum between compression crests"),
        ("knee", 1558, "second rise in compression eases"),
        ("knee, minimum", (2190, 2350), "broad compression crest near the −60 lb ruling"),
    ],
}

ENDS_NOTES = {
    (329, 1): ("trace joins the origin frame", "trace meets the .1 s frame"),
    (330, 1): ("trace and zero ruling merge at the left frame", "trace meets the zero ruling"),
    (330, 2): ("initial trace merges with zero ruling and left frame", "free end above zero"),
    (330, 3): ("free tip below zero", "free end at faint .10 s tick"),
    (336, 1): ("trace merges with left frame at zero depth", "trace meets the .1 s frame"),
    (337, 1): ("origin partially merged with left frame and zero ruling", "free tip beyond .10 s"),
    (337, 2): ("origin partially merged with left frame and zero ruling", "free tip beyond .10 s"),
    (337, 3): ("earliest identifiable junction with left frame", "free tip beyond .10 s"),
}


def linear_smooth(a, radius):
    return np.convolve(np.pad(a, radius, mode="edge"), np.ones(2*radius+1)/(2*radius+1), "valid")


def geom(grid, columns, cal, x, y, gradient):
    """Measure the local stroke across its normal, away from rules if merged."""
    length = np.hypot(1, gradient)
    nx, ny = -gradient / length, 1 / length
    off = np.arange(-10, 10.01, .25)
    vmax = grid.shape[1] - 1
    coords_x = np.rint(x+nx*off).astype(int)
    coords_y = np.rint(y+ny*off).astype(int)
    spans = runs(grid[coords_y, coords_x] < 150)
    if not spans:
        return None
    span = min(spans, key=lambda s: abs((off[s[0]] + off[s[-1]]) / 2))
    center = (off[span[0]] + off[span[-1]]) / 2
    width = len(span)*.25
    near_rule = min(abs(y-k) for k in rules_at(cal, x, vmax)) <= 4
    near_frame = nearby_frame(cal, x, y, vmax)
    return center, width, near_rule or near_frame


def make_track(page, panel, gray, y_axis, xmax):
    prefix = Path("out") / f"track-{page}-p{panel}.npz"
    track = np.load(prefix)
    known_x, known_y = track["columns"], track["projected"]
    first, last = ENDS[page, panel]
    columns = np.arange(first[0], last[0] + 1)
    projected = np.interp(columns, known_x, known_y)
    # Inspect long mergers as connected bands. Their full thickness is not
    # attributed to the trace. At the first F5-25 compression crest the trace
    # enters and leaves on the lower edge of the -80 ruling.
    shared_bands = {
        (330, 3): [(1127, 1155, 1929)],
        (337, 1): [(1745, 1932, 1347)],
        (337, 3): [(2005, 2455, 2025)],
    }
    for left, right, near in shared_bands.get((page, panel), []):
        for x in range(left, right + 1):
            i = x-columns[0]
            spans = runs(gray[near-14:near+15, x] < 150)
            if not spans:
                continue
            band = min(spans, key=lambda span: abs(np.mean(span)+near-14-projected[i]))
            center = (band[0]+band[-1])/2 + near-14
            if (page, panel) == (330, 3):
                center = max(center, band[-1] + near-14 - 2)
            projected[i] = center
    if (page, panel) == (330, 3):
        # Follow the unloading stroke past the .09 tick and reject the isolated
        # fleck above it at u=2175.
        for x in range(2498, 2522):
            expected = np.interp(x, [2498, 2521], [2183, 2194])
            top = round(expected)-7
            span = max(runs(gray[top:top+15, x] < 150), key=len)
            projected[x-columns[0]] = (span[0]+span[-1])/2 + top
    projected[0], projected[-1] = first[1], last[1]
    # These segments have visible ink on both sides. Over the join the center is
    # read along the same stroke, with thickness measured on the nearest clear side.
    # The guide's gentle slopes are sufficient for a normal profile at pixel scale.
    smooth = linear_smooth(projected, 6)
    gradient = np.gradient(smooth)
    yn = np.array([y_axis.value(y, xmax-x)[0] for x, y in zip(columns, projected)])
    return columns, projected, gradient, yn


def find_pixel(grid, cal, path, x_target, endpoint=False):
    columns, yy, slopes, _ = path
    x = int(np.clip(round(x_target), columns[0], columns[-1]))
    y = float(yy[x-columns[0]])
    grad = slopes[x-columns[0]]
    measurement = geom(grid, columns, cal, x, y, grad)
    note = ""
    if endpoint and grid[round(y), x] < 150 and (measurement is None or abs(measurement[0]) > 2.3):
        measurement = (0, 0, True)
    if measurement is None or abs(measurement[0]) > 2.3:
        if endpoint:
            raise ValueError(f"No trace near endpoint {x}, {y}")
        # Nominal section can fall in the white part of a scan break.
        for d in (1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6):
            i = x+d-columns[0]
            if 0 <= i < len(columns):
                m = geom(grid, columns, cal, x+d, yy[i], slopes[i])
                if m is not None and abs(m[0]) <= 2.3 and not m[2]:
                    x, y, grad, measurement = x+d, yy[i], slopes[i], m
                    note = "shifted to surviving ink beside scan break"
                    break
        else:
            return None

    center, width, joined = measurement
    if not endpoint and not joined and 2.25 <= width <= 11:
        length = np.hypot(1, grad)
        dx, dy = -grad * center / length, center / length
        if grid[round(y+dy), round(x+dx)] < 150:
            x, y = x+dx, y+dy
    if joined or not 2.25 <= width <= 11:
        widths = []
        i = int(round(x))-columns[0]
        for d in sorted(range(-42, 43), key=abs):
            j = i+d
            if d == 0 or not 0 <= j < len(columns):
                continue
            m = geom(grid, columns, cal, columns[j], yy[j], slopes[j])
            if m and abs(m[0]) < 2 and 2.25 <= m[1] <= 11 and not m[2]:
                widths.append(m[1])
                if len(widths) == 7:
                    break
        # In long merges use the visible outer stroke where the core is still measurable.
        if not widths and 2.25 <= width <= 11:
            widths = [width]
        if not widths:
            raise ValueError(f"No trace thickness near {x}, {y}")
        width = float(np.median(widths))
        if not note:
            note = "ruling or frame meets trace; measured nearby stroke thickness"
    xi, yi = int(round(x)), int(round(y))
    if grid[yi, xi] >= 150:
        # Keep a fractional center only when the ink covers it in the page raster.
        dark = [(i, j) for i in range(xi-1, xi+2) for j in range(yi-2, yi+3) if grid[j, i] < 150]
        if not dark:
            return None
        x, y = min(dark, key=lambda ij: (ij[0]-x)**2 + (ij[1]-y)**2)
    return float(x), float(y), width / 2, note


def requests(path, time_axis, vmax, step, features):
    columns, y, _, values = path
    tt = np.array([time_axis.value(u, vmax-x)[0] for x, u in zip(columns, y)])
    smooth_val = linear_smooth(values, 6)
    target_t = [*np.arange(0, .02001, .002), *np.arange(.025, .10501, .005)]
    samples = [(float(np.interp(tx, tt, columns)), "time") for tx in target_t if tt[0] < tx < tt[-1]]
    for level in np.arange(math.floor(min(values)/step)*step, max(values)+step, step):
        for i in np.flatnonzero((smooth_val[:-1] < level) != (smooth_val[1:] < level)):
            half = 6
            l, r = max(0, i-half), min(len(tt)-1, i+half)
            ratio = abs(smooth_val[r] - smooth_val[l]) / (tt[r] - tt[l])
            dt = .002 if tt[i] < .02 else .005
            if ratio * dt < step:
                continue
            x = columns[i] + (level-smooth_val[i])/(smooth_val[i+1]-smooth_val[i])
            # Avoid double counting where the two scheduled locations nearly coincide.
            if all(abs(x-s[0]) > 2.0 for s in samples):
                samples.append((float(x), "value"))
    samples = [(x, "trace", "") for x, _ in samples if columns[0]+2 < x < columns[-1]-2]
    for x in (columns[0], columns[-1]):
        samples.append((x, "trace", ""))
    for role, loc, description in features:
        if loc == "end":
            x = columns[-1]
        elif isinstance(loc, tuple):
            i = np.flatnonzero((columns >= loc[0]) & (columns <= loc[1]))
            zz = smooth_val[i] * (1 if role == "peak" else -1)
            best = i[zz >= zz.max() - abs(smooth_val.max()-smooth_val.min())*.002]
            x = columns[int(np.median(best))]
        else:
            x = loc
        samples.append((x, "feature", f"{role}, {description}"))
    samples += [(columns[0], "feature", "first"), (columns[-1], "feature", "last")]
    return sorted(samples, key=lambda r: r[0])


def fill_native(cal, xa, ya, rows, page):
    """Use verified piecewise knots plus the measured common-tick lean allowance."""
    for row in rows:
        u = float(row["pixel_u"])
        if page in (330, 337):
            base_errors = [kn["err"] for kn in xa.knots]
            for kn in xa.knots:
                if kn["value"] != 0:
                    # Surviving marks on the upper field differ from the common
                    # projected lean by up to about 4 px over a 1500 px span.
                    kn["err"] += .0027*max(0, 2210-u)
        axes.piecewise_rows(cal, xa, ya, [row])
        if page in (330, 337):
            for kn, error in zip(xa.knots, base_errors):
                kn["err"] = error


def run():
    for page, (figure, series, step) in FIGURES.items():
        name = f"packet/p{page:04}.png"
        grid = np.asarray(Image.open(name).convert("L").transpose(Image.Transpose.ROTATE_270))
        vmax = grid.shape[1]-1
        folder = Path("out") / figure
        for panel, series_id in enumerate(series, 1):
            cal, xa, ya = axes.piecewise_maps(folder / f"cal-p{panel}", name)
            path = make_track(page, panel, grid, ya, vmax)
            pending = requests(path, xa, vmax, step, FEATURES[page, panel])
            located = []
            for tx, kind, comment in pending:
                at_end = tx in (path[0][0], path[0][-1])
                p = find_pixel(grid, cal, path, tx, endpoint=at_end)
                if p is None:
                    print(f"omitted {figure}/{panel} at upright column {tx:.1f}: scan dropout")
                    continue
                x, y, bound, rationale = p
                if at_end:
                    end_detail = ENDS_NOTES[page, panel][int(tx == path[0][-1])]
                    rationale = end_detail
                note = ", ".join(filter(None, (comment, rationale)))
                located.append((x, y, bound, kind, note))
            located.sort(key=lambda p: p[0])
            rows = [
                dict(figure_id=figure, panel=panel, series_id=series_id, point_kind=kind, sequence=i,
                     pixel_u=round(y, 2), pixel_v=round(vmax-x, 2), u_bound_px=bound, v_bound_px=bound,
                     symbol="", note=note)
                for i, (x, y, bound, kind, note) in enumerate(located, 1)
            ]
            write_csv(folder / f"points-p{panel}.csv", rows)
            fill_native(cal, xa, ya, rows, page)
            write_csv(folder / f"points-p{panel}-native.csv", rows)
            kinds = [p["point_kind"] for p in rows]
            print(figure, panel, kinds.count("trace"), kinds.count("feature"),
                  "width half range", min(r["u_bound_px"] for r in rows), max(r["u_bound_px"] for r in rows))
            for r in rows:
                if r["point_kind"] == "feature":
                    print(f"  {r['x_native']:.5f} {r['y_native']:7.3f} {r['note']}")


if __name__ == "__main__":
    run()
