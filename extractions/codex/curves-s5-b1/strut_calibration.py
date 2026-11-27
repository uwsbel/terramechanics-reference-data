"""Measure the shared time ticks and the labelled load rules on the strut pages."""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import calibrate_axes as axes


PAGES = {
    330: {
        "id": "F5-25",
        "slope": -.0055,
        "tick_slope": -.0060,
        "frame": (982, 745, 2263),
        "ticks": [
            (1147, 2225, 2258), (1315, 2202, 2258), (1486, 2220, 2259),
            (1657, 2210, 2259), (1827, 2223, 2261), (1998, 2204, 2237),
            (2167, 2210, 2259), (2338, 2203, 2259), (2511, 2209, 2238),
            (2679, 2241, 2258),
        ],
        "x_range": (988, 2675),
        "y_slope": .0026,
        "panels": [
            [(0, 1248), (20, 1163), (40, 1077), (60, 993)],
            [(0, 1673), (20, 1587), (40, 1502), (60, 1418)],
            [(-100, 1844), (-80, 1929), (-60, 2014), (-40, 2100), (-20, 2185), (0, 2270)],
        ],
    },
    337: {
        "id": "F5-32",
        "slope": .0085,
        "tick_slope": .0056,
        "frame": (998, 765, 2281),
        "ticks": [
            (1181, 2233, 2280), (1350, 2198, 2268), (1521, 2217, 2280),
            (1691, 2237, 2277), (1862, 2231, 2274), (2034, 2220, 2268),
            (2203, 2234, 2274), (2373, 2240, 2272), (2543, 2213, 2271),
        ],
        "x_range": (1010, 2880),
        "y_slope": -.0090,
        "panels": [
            [(-60, 1100), (-40, 1185), (-20, 1271), (0, 1357)],
            [(0, 1780), (20, 1695), (40, 1609), (60, 1524)],
            [(-80, 1950), (-60, 2035), (-40, 2121), (-20, 2205), (0, 2288)],
        ],
    },
}


def fit(positions, centers, slope=None):
    positions, centers = np.array(positions), np.array(centers)
    for _ in range(3):
        if slope is None:
            slope_fit, intercept = np.polyfit(positions, centers, 1)
        else:
            slope_fit, intercept = slope, np.median(centers - slope * positions)
        residual = centers - (slope_fit * positions + intercept)
        good = abs(residual - np.median(residual)) < max(1.1, 3 * np.median(abs(residual)))
        positions, centers = positions[good], centers[good]
    return float(slope_fit), float(intercept), list(zip(positions.tolist(), centers.tolist()))


def measure(gray, positions, reference, slope, search, along, fixed=False):
    """Pick the grid core within a narrow corridor, then fit it to the surviving ink."""
    hits = []
    for p in positions:
        near = round(reference + slope * (p - positions[0]))
        if along == "x":
            window = gray[near - search:near + search + 1, p - 4:p + 5]
        else:
            window = gray[p - 3:p + 4, near - search:near + search + 1].T
        darkness = 255 - window.mean(axis=1)
        if darkness.max() < 55:
            continue
        k = int(np.argmax(darkness))
        ink = np.flatnonzero(darkness >= darkness[k] / 2)
        run = next(r for r in np.split(ink, np.where(np.diff(ink) > 1)[0] + 1) if k in r)
        if len(run) <= 9:
            center = np.average(run, weights=darkness[run]) + near - search
            hits.append((p, center))
    return fit(*zip(*hits), slope=slope if fixed else None)


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def save_calibration(page, info, gray, panel, rules):
    original = f"packet/p{page:04}.png"
    vmax = gray.shape[1] - 1
    anchors, horizontals, verticals = [], [], []
    xfits, yfits = [], []
    xf, f0, frame = measure(gray, list(range(info["frame"][1], info["frame"][2], 27)),
                            info["frame"][0], info["slope"], 6, "y")
    xfits.append((0.0, xf, f0))
    source = "detected shared time-zero frame"
    for y, x in frame:
        anchors.append(dict(x_value=0, y_value="", u=y, v=vmax - x, x_source=source, y_source=""))
    horizontals.append(dict(x_value=0, slope_dv_du=-xf, v_at_u0=vmax - f0,
                            source=source, samples=len(frame)))
    for i, (guess, first, last) in enumerate(info["ticks"], 1):
        tick_slope = info["tick_slope"]
        slope, intercept, hits = measure(gray, list(range(first, last + 1, 3)),
                                          guess, tick_slope, 3, "y", fixed=True)
        if page == 337 and i == 9:
            # The .09 ruling survives as short aligned stubs; use the clear upper stub.
            hits = [(2220, 2543.5)]
            intercept = hits[0][1] - slope * hits[0][0]
        value = i / 100
        xfits.append((value, slope, intercept))
        source = "detected shared lower time-axis tick"
        for y, x in hits:
            anchors.append(dict(x_value=value, y_value="", u=y, v=vmax - x, x_source=source, y_source=""))
        horizontals.append(dict(x_value=value, slope_dv_du=-slope, v_at_u0=vmax - intercept,
                                source=source, samples=len(hits)))
    for value, approx in rules:
        lo, hi = info["x_range"]
        if page == 330 and panel == 1 and value in (40, 60):
            # The inset's box edge runs close to these rulings at the right.
            hi = 2380
        slope, intercept, hits = measure(gray, list(range(lo + 5, hi, 19)),
                                          approx, info["y_slope"], 6, "x")
        yfits.append((value, slope, intercept))
        source = "detected labelled load rule"
        for x, y in hits:
            anchors.append(dict(x_value="", y_value=value, u=y, v=vmax - x, x_source="", y_source=source))
        verticals.append(dict(y_value=value, slope_du_dv=-slope, u_at_v0=intercept+slope*vmax,
                              source=source, samples=len(hits)))

    # Fit the rate to tick locations with the lean independently measured from the frame.
    x_rate, x_intercept = np.polyfit([it[2] for it in xfits], [it[0] for it in xfits], 1)
    ax = [-info["tick_slope"] * x_rate, -x_rate, vmax * x_rate + x_intercept]
    # Fit the load gradient to the ruled lines' mutual intersections with several cross-sections.
    y_diag = [dict(u=intercept + slope*x, v=vmax-x, y_value=value)
              for value, slope, intercept in yfits for x in np.linspace(*info["x_range"], 11)]
    ay = np.linalg.lstsq([[a["u"], a["v"], 1] for a in y_diag],
                        [a["y_value"] for a in y_diag], rcond=None)[0].tolist()

    def residual(coef, field):
        r = [float(a[field]) - (coef[0]*a["u"] + coef[1]*a["v"] + coef[2])
             for a in anchors if a[field] != ""]
        return float(np.sqrt(np.mean(np.square(r)))), float(np.max(np.abs(r)))

    xr, xm = residual(ax, "x_value")
    yr, ym = residual(ay, "y_value")
    ys = [y for _, y in rules]
    cal = dict(image=original, box=[min(ys)-6, vmax-info["x_range"][1], max(ys)+26, vmax-info["frame"][0]+15],
               model="Affine diagnostic on measured shared time ticks and labelled load rules",
               ax=ax, ay=ay, x_per_px=float(np.hypot(*ax[:2])), y_per_px=float(np.hypot(*ay[:2])),
               rms_residual_x=xr, max_residual_x=xm, rms_residual_y=yr, max_residual_y=ym, n_anchors=len(anchors),
               x_direction="up", y_direction="left" if ay[0] < 0 else "right",
               horizontal_lines=horizontals, vertical_lines=verticals)
    folder = Path("out") / info["id"] / f"cal-p{panel}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "calibration.json").write_text(json.dumps(cal, indent=2) + "\n")
    write_csv(folder / "anchors.csv", anchors)
    return folder


if __name__ == "__main__":
    for page, info in PAGES.items():
        name = f"packet/p{page:04}.png"
        gray = np.asarray(Image.open(name).convert("L").transpose(Image.Transpose.ROTATE_270))
        for panel, rules in enumerate(info["panels"], 1):
            folder = save_calibration(page, info, gray, panel, rules)
            cal, x, y = axes.piecewise_maps(folder, name)
            for axis, knots in (("x", x), ("y", y)):
                print(folder, axis, [
                    (k["value"], round(k["err"], 2), k.get("reason", "verified"))
                    for k in knots.knots + knots.rejected
                ], "RMS", cal[f"rms_residual_{axis}"])
