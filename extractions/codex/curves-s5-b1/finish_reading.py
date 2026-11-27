"""Write eye checks, build overlays, and check the submitted point files."""
import csv
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

from strut_calibration import axes, write_csv
from trace_reading import FIGURES


LABELS_Y = {
    329: [[(0, "0"), (1, "1.0"), (2, "2.0"), (3, "3.0"), (4, "4.0"), (5, "5.0"), (6, "6.0"), (7, "")]],
    330: [
        [(0, "0"), (20, "+20"), (40, "+40"), (60, "+60")],
        [(0, "0"), (20, "+20"), (40, "+40"), (60, "-60")],
        [(0, "0"), (-20, "-20"), (-40, "-40"), (-60, "-60"), (-80, "-80"), (-100, "-100")],
    ],
    336: [[(-1, "-1.0"), (0, "0"), (1, "+1.0"), (2, "2.0"), (3, "3.0"), (4, "4.0"), (5, "5.0"), (5.5, "")]],
    337: [
        [(0, "0"), (-20, "-20"), (-40, "-40"), (-60, "-60")],
        [(0, "0"), (20, "+20"), (40, "+40"), (60, "-60")],
        [(0, "0"), (-20, "-20"), (-40, "-40"), (-60, "-60"), (-80, "-80")],
    ],
}

# Boxes in the page coordinates, including the axis-title side of the crop.
OVERLAY = {
    329: [(550, 1070, 2490, 3810)],
    330: [(870, 1800, 1275, 3715), (1320, 1805, 1710, 3715), (1815, 1805, 2370, 3720)],
    336: [(550, 1040, 2390, 3830)],
    337: [(1035, 1705, 1395, 3715), (1440, 1705, 1815, 3715), (1910, 1705, 2380, 3715)],
}


def row(fig, p, axis, text, assigned, u, v, status, note):
    return dict(figure_id=fig, panel=p, axis=axis, printed_label=text, anchored_value=assigned,
                pixel_u=round(u, 1), pixel_v=round(v, 1), status=status, note=note)


def eye_checks(page, fig, panel, cal):
    x_lines = {r["x_value"]:r for r in cal["horizontal_lines"]}
    y_lines = {r["y_value"]:r for r in cal["vertical_lines"]}
    bottom_u = {329:2319, 330:2271, 336:2205, 337:2287}[page]
    rows = []
    for i in range(11):
        value = i/100
        printed = "0" if i == 0 else f".{i:02d}"
        status, note, anchor = "matched", "Label matches the measured rule", value
        u = bottom_u
        if page in (329, 336) and i == 10:
            printed = ".1"
        if page in (330, 337):
            note = "Label matches the measured shared lower tick"
            u = {330:2244, 337:2254}[page]
            if i == 0:
                note = "Label matches the shared time-zero frame"
        if i == 9 and page == 330:
            printed, status, u = ".", "sequence", 2224
            note = "Decimal point and two digit-bottom fragments survive. The short tick lies between .08 and .10"
        if i == 9 and page == 337:
            printed, status, u = "09", "sequence", 2220
            note = "Digits partial and decimal point lost. Aligned lower tick stubs fix the .09 position"
        if i == 10 and page == 337:
            u, v = 2269, 1792.5
            rows.append(row(fig, panel, "x", printed, "", u, v, "label only",
                            "Approximate position above the label. The ruling has too little surviving ink for a knot"))
            continue
        rule = x_lines[value]
        v = rule["v_at_u0"] + rule["slope_dv_du"]*u
        rows.append(row(fig, panel, "x", printed, anchor, u, v, status, note))
    left_v = {329:3534, 330:3526, 336:3509, 337:3502}[page]
    for value, printed in LABELS_Y[page][panel-1]:
        rule = y_lines[value]
        u = rule["u_at_v0"] + rule["slope_du_dv"]*left_v
        status, note = "matched", "Label matches the measured load or depth rule"
        if not printed:
            status = "unlabelled frame"
            note = ("Verified frame one full interval above 6.0" if page == 329
                    else "Verified frame one half interval above 5.0")
        if page in (330, 337) and panel == 2 and value == 60:
            status, note = "sequence", "Printed -60 above +40. Its ruled line is the next +20 lb step"
        rows.append(row(fig, panel, "y", printed, value, u, left_v, status, note))
    return rows


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def run():
    for page, (fig, series, _) in FIGURES.items():
        image = f"packet/p{page:04}.png"
        raw = np.asarray(Image.open(image).convert("L"))
        folder = Path("out") / fig
        checks = []
        for panel, name in enumerate(series, 1):
            cal, xa, ya = axes.piecewise_maps(folder / f"cal-p{panel}", image)
            assert not xa.rejected and not ya.rejected
            checks.extend(eye_checks(page, fig, panel, cal))
            points = folder / f"points-p{panel}.csv"
            native = folder / f"points-p{panel}-native.csv"
            original, native_rows = read_csv(points), read_csv(native)
            assert len(original) == len(native_rows)
            assert all(all(p[k] == n[k] for k in p) for p,n in zip(original, native_rows))
            assert all(p["series_id"] == name and p["symbol"] == "" for p in original)
            assert [int(p["sequence"]) for p in original] == list(range(1,len(original)+1))
            assert all(raw[round(float(p["pixel_v"])),round(float(p["pixel_u"]))] < 150 for p in original)
            assert all(float(p["x_read_bound"]) > 0 and float(p["y_read_bound"]) > 0 for p in native_rows)
            trace = [r for r in native_rows if r["point_kind"] == "trace"]
            assert np.all(np.diff([float(p["x_native"]) for p in trace]) >= 0)
            features = [r for r in native_rows if r["point_kind"] == "feature"]
            assert features[0]["note"].startswith("first") and features[-1]["note"].startswith("last")
            assert all(r["note"].split(",")[0] in ("first","last","peak","knee") for r in features)
            for tr, ft in zip((trace[0], trace[-1]), (features[0], features[-1])):
                assert (tr["pixel_u"], tr["pixel_v"]) == (ft["pixel_u"], ft["pixel_v"])
            targets = [*np.arange(0,.02001,.002), *np.arange(.025,.10501,.005)]
            times = np.array([float(p["x_native"]) for p in trace])
            furthest = max(min(abs(times-t)) for t in targets if min(times)-.00025 <= t <= max(times)+.00025)
            assert furthest < .00027, (fig, panel, furthest)
            out = folder / f"overlay-p{panel}.png"
            subprocess.run([sys.executable,"tools/plot_grid.py","overlay",image,"--points",str(points),
                            "--box",*map(str,OVERLAY[page][panel-1]),"--out",str(out)],check=True)
            with Image.open(out) as ov:
                ov.transpose(Image.Transpose.ROTATE_270).save(Path("out")/f"qa-overlay-{page}-p{panel}.png")
            counts = Counter(r["point_kind"] for r in native_rows)
            scale_diff = np.max([
                np.abs(np.array([float(r["x_native"]),float(r["y_native"])]) -
                        np.array([cal["ax"],cal["ay"]]) @ [float(r["pixel_u"]),float(r["pixel_v"]),1])
                for r in native_rows
            ], axis=0)
            print(fig, name, counts,
                  "rms", f"{cal['rms_residual_x']:.8f}", f"{cal['rms_residual_y']:.5f}",
                  "max residual",f"{cal['max_residual_x']:.8f}", f"{cal['max_residual_y']:.5f}",
                  "sensitivity", scale_diff,
                  "times", (min(times),max(times)), "cadence tolerance",furthest, flush=True)
        write_csv(folder / "calibration-eye-checks.csv", checks)


if __name__ == "__main__":
    run()
