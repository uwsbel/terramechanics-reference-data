"""Synthetic check of log and reciprocal axes in the curve-reading tools (D-027).

    python tools/tests/test_axis_transforms.py

Draws a page with a log10 x grid (grain size 0.01 to 10 mm, labelled decades and the 2 and 5 lines)
and a reciprocal y grid (unit weight 80 to 120 pcf, lines evenly spaced in 1/gamma), upright and
turned sideways, then checks: detect finds every line and fits the plotting coordinates exactly;
values between lines come back as the analytic ones (halfway between 1 and 10 mm in q is sqrt(10);
halfway between 80 and 120 pcf is 96); the read bound of a point holds the value at every corner of
its pixel interval; a line left out is recovered where the transform puts it; the comparison of two
readings interpolates a trace in the plotting coordinates; linear calibrations are untouched.
Exit status 0 when every check passes.
"""
import csv
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import calibrate_axes as ca  # noqa: E402
import diff_curves as dc  # noqa: E402

X_VALUES = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]
Y_VALUES = [80, 90, 100, 110, 120]
U0, U1, V0, V1 = 300, 2700, 400, 2200          # the plot frame (upright page)
QX0, QX1 = math.log10(0.01), math.log10(10)
QY0, QY1 = 1 / 80, 1 / 120                       # q decreases upward: 80 pcf at the bottom


def u_of(x):
    return U0 + (U1 - U0) * (math.log10(x) - QX0) / (QX1 - QX0)


def v_of(y):
    return V1 - (V1 - V0) * (1 / y - QY0) / (QY1 - QY0)


def page(path, sideways=False):
    g = np.full((2600, 3000), 255, dtype=np.uint8)
    for x in X_VALUES:
        u = int(round(u_of(x)))
        g[V0:V1 + 1, u - 1:u + 2] = 0
    for y in Y_VALUES:
        v = int(round(v_of(y)))
        g[v - 1:v + 2, U0:U1 + 1] = 0
    img = Image.fromarray(g)
    if sideways:   # turned a quarter turn counterclockwise: x then increases up the page
        img = img.transpose(Image.Transpose.ROTATE_90)
    img.save(path)


def run(*args):
    r = subprocess.run([sys.executable, str(TOOLS / "calibrate_axes.py"), *args], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr)
    return r.stdout


def check(cond, what):
    print(("ok    " if cond else "FAIL  ") + what)
    return bool(cond)


def main():
    ok = True
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        img = d / "page.png"
        page(img)
        out = run("detect", str(img), "--box", str(U0 - 40), str(V0 - 40), str(U1 + 40), str(V1 + 40),
                  "--x-values", ",".join(map(str, X_VALUES)), "--y-values", ",".join(map(str, Y_VALUES)),
                  "--x-transform", "log10", "--y-transform", "reciprocal", "--out", str(d / "cal"))
        cal = json.loads((d / "cal" / "calibration.json").read_text())
        ok &= check("predicted" not in out, "detect finds all 10 log lines and 5 reciprocal lines (none predicted)")
        ok &= check(cal.get("x_transform") == "log10" and cal.get("y_transform") == "reciprocal", "transforms recorded")
        ok &= check(cal["max_residual_x"] < 1e-3 and cal["max_residual_y"] < 1e-6,
                    f"affine fit in the plotting coordinates (max residual {cal['max_residual_x']:.2g} decade, {cal['max_residual_y']:.2g} 1/pcf)")

        # values between lines, through both maps; points at known values and halfway in q
        truth = [(0.01, 80), (10, 120), (math.sqrt(10), 96), (0.3, 85), (3.0, 115), (0.0316, 101)]
        rows = [{"panel": "1", "series_id": "s", "point_kind": "marker", "sequence": str(i), "pixel_u": f"{u_of(x):.3f}",
                 "pixel_v": f"{v_of(y):.3f}", "u_bound_px": "2", "v_bound_px": "2"} for i, (x, y) in enumerate(truth)]
        pts = d / "points.csv"
        with pts.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        run("piecewise", str(d / "cal"), str(pts), str(d / "pw.csv"), "--image", str(img))
        run("apply", str(d / "cal" / "calibration.json"), str(pts), str(d / "af.csv"))
        for name in ("pw", "af"):
            got = list(csv.DictReader((d / f"{name}.csv").open()))
            err = max(max(abs(float(r["x_native"]) / x - 1), abs(float(r["y_native"]) / y - 1)) for r, (x, y) in zip(got, truth))
            ok &= check(err < 2e-3, f"{name}: values at known points within 0.2 percent (largest {err:.1e}), incl. sqrt(10) mm and 96 pcf")
            # the bound holds the map's own value at every corner of the 2 px interval (the map as fitted to
            # lines drawn on whole pixels, not the ideal grid)
            _, X, Y = ca.piecewise_maps(d / "cal", img)
            holds = True
            for r, (x, y) in zip(got, truth):
                for du in (-2, 2):
                    for dv in (-2, 2):
                        uc, vc = u_of(x) + du, v_of(y) + dv
                        if name == "pw":
                            xc, yc = X.value(uc, vc)[0], Y.value(uc, vc)[0]
                        else:
                            xc, yc = dc.apply_map(cal, uc, vc)
                        holds &= abs(xc - float(r["x_native"])) <= float(r["x_read_bound"]) * 1.001
                        holds &= abs(yc - float(r["y_native"])) <= float(r["y_read_bound"]) * 1.001
            ok &= check(holds, f"{name}: every read bound holds the values at the corners of its pixel interval")

        # recovery: drop the 0.5 mm and 100 pcf lines from the anchors and recover them from the page
        _, X, Y = ca.piecewise_maps(d / "cal", img)
        gray = np.asarray(Image.open(img).convert("L"), dtype=float)
        an = [a for a in ca.load_anchors(d / "cal") if float(a["x_value"]) != 0.5 and float(a["y_value"]) != 100]
        Xr = ca.AxisKnots(an, "x_value", "x_source", cal["ax"][:2], gray, "log10")
        Yr = ca.AxisKnots(an, "y_value", "y_source", cal["ay"][:2], gray, "reciprocal")
        span = lambda K: (min(t for kn in K.knots for t in kn["t"]), max(t for kn in K.knots for t in kn["t"]))
        # a search window of 8 px: the prediction itself must be right (a prediction linear in the value puts
        # the 100 pcf line about 44 px off, which the default 60 px window would hide; Codex's review)
        px, _ = ca.recover_line(gray, Xr, 0.5, span(Xr), search_px=8)
        py, _ = ca.recover_line(gray, Yr, 100, span(Yr), search_px=8)
        ok &= check(px and abs(np.mean([p[0] for p in px]) - u_of(0.5)) < 1.5, "the 0.5 mm line is recovered where log spacing puts it")
        ok &= check(py and abs(np.mean([p[1] for p in py]) - v_of(100)) < 1.5, "the 100 pcf line is recovered where reciprocal spacing puts it")

        # comparison: a trace interpolated in the plotting coordinates; a curve straight on this page has
        # 1/y linear in log10 x, so samples a decade apart reproduce it exactly between them
        f = lambda x: 1 / (QY0 + (QY1 - QY0) * (math.log10(x) - QX0) / (QX1 - QX0))
        dc.AXES = ("log10", "reciprocal")
        trace = [{"x_native": str(x), "y_native": str(f(x)), "x_read_bound": "0", "y_read_bound": "0",
                  "pixel_u": "0", "pixel_v": "0"} for x in (0.01, 0.1, 1, 10)]
        y, *_ = dc.interp_trace(trace, math.sqrt(0.1), float("inf"))
        ok &= check(abs(y - f(math.sqrt(0.1))) < 1e-9, f"a trace is interpolated along the curve as drawn ({y:.3f} vs {f(math.sqrt(0.1)):.3f} pcf)")
        # pixels interpolated with the value, on samples placed where the page puts them
        trace_px = [dict(r, pixel_u=str(u_of(float(r["x_native"]))), pixel_v=str(v_of(float(r["y_native"])))) for r in trace]
        it = dc.interp_trace(trace_px, math.sqrt(0.1), float("inf"))
        ok &= check(abs(it[4] - u_of(math.sqrt(0.1))) < 1e-6 and abs(it[5] - v_of(it[0])) < 1e-6,
                    "the interpolated pixel is where the interpolated value is on the page")
        # the slope that carries an x bound into y is dy/dx at the point (Codex's review: not the chord in values)
        dc.AXES = ("log10", "linear")
        seg = [{"x_native": "1", "y_native": "0", "x_read_bound": "0", "y_read_bound": "0", "pixel_u": "0", "pixel_v": "0"},
               {"x_native": "10", "y_native": "1", "x_read_bound": "0", "y_read_bound": "0", "pixel_u": "0", "pixel_v": "0"}]
        sl = dc.interp_trace(seg, 1.1, float("inf"))[3]
        ok &= check(abs(sl - 1 / (1.1 * math.log(10))) < 1e-9, f"slope at x = 1.1 on a log axis {sl:.4f} = 1/(1.1 ln 10)")
        dc.AXES = ("linear", "linear")
        y, *_ = dc.interp_trace([{**r, "x_native": str(i), "y_native": str(2 * i)} for i, r in enumerate(trace)], 1.5, float("inf"))
        ok &= check(y == 3.0, "linear axes interpolate as before")

        # a reciprocal interval reaching 1/value = 0 has no finite bound
        K = ca.AxisKnots([{"x_value": "", "y_value": "100", "u": "0", "v": "0", "x_source": "", "y_source": "t"},
                          {"x_value": "", "y_value": "50", "u": "10", "v": "0", "x_source": "", "y_source": "t"}],
                         "y_value", "y_source", [1.0, 0.0], None, "reciprocal")
        try:
            K.interval(-9, 0, 2, 0)
            ok &= check(False, "a reciprocal interval crossing the singularity is rejected")
        except ValueError:
            ok &= check(True, "a reciprocal interval crossing the singularity is rejected")
        import to_si
        ok &= check(to_si.convert_cell("85", "percent", "none")[0] == "0.85" and to_si.convert_cell("1.5e-3", "mm", "m")[0] == "1.5e-06",
                    "percent to a fraction, and values in scientific notation, convert to SI")

        # sideways: the same grid turned; x increases up the page, y to the right
        side = d / "side.png"
        page(side, sideways=True)
        H = 3000   # rotated: new v = (W_old - 1) - u_old, new u = v_old
        out = run("detect", str(side), "--box", str(V0 - 40), str(H - 1 - U1 - 40), str(V1 + 40), str(H - 1 - U0 + 40),
                  "--x-values", ",".join(map(str, X_VALUES)), "--y-values", ",".join(map(str, Y_VALUES)),
                  "--x-transform", "log10", "--y-transform", "reciprocal", "--x-direction", "up", "--y-direction", "left",
                  "--out", str(d / "cal-side"))
        _, Xs, Ys = ca.piecewise_maps(d / "cal-side", side)
        x, y = Xs.value(v_of(96), H - 1 - u_of(math.sqrt(10)))[0], Ys.value(v_of(96), H - 1 - u_of(math.sqrt(10)))[0]
        ok &= check("predicted" not in out and abs(x / math.sqrt(10) - 1) < 2e-3 and abs(y / 96 - 1) < 2e-3,
                    f"sideways and transformed at once: ({x:.4f} mm, {y:.3f} pcf) for (sqrt(10), 96)")
    print("all checks passed" if ok else "SOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
