"""Axis calibration for a scanned plot: grid intersections as anchors, affine pixel-to-value fit.

    python tools/calibrate_axes.py detect <image> --box u0 v0 u1 v1 \
        --x-values 0,50,100,150,200,250 --y-values 0,1000,2000,3000,4000,5000,6000 \
        --out <dir>  [--bands 5] [--dark 200] [--min-frac 0.6] [--snap 10]

        The box encloses one panel's plot frame (a little outside the frame is fine). The grid is
        assumed rectangular with the outer frame lines carrying the first and last values of each
        list. Because a scan is never perfectly square, each grid line is located in `bands`
        narrow strips across the box (where its tilt is negligible), fitted as a straight line,
        and the intersections of the fitted lines are the anchors. Writes
            <dir>/anchors.csv       x_value, y_value, u, v, x_source, y_source
            <dir>/calibration.json  affine maps value = A [u v 1], residuals, the detected lines
        A line not found within `snap` pixels of its predicted position is interpolated from the
        frame lines and marked `predicted`; the reader should check it on the image.

    python tools/calibrate_axes.py apply <calibration.json> <points.csv> <out.csv>

        Adds x_native, y_native (from pixel_u, pixel_v) and x_read_bound, y_read_bound (from
        u_bound_px, v_bound_px times the local scale, plus the calibration RMS residual) to a
        points file written by a reader (see docs/CURVE-READING.md for the columns).

    A figure printed sideways is calibrated on the page as scanned: --x-direction and
    --y-direction name the page directions in which x and y increase (for example --x-direction up
    --y-direction right), and the grid values are assigned to the horizontal or vertical lines
    accordingly. The affine map and the bounds of `apply` hold for any orientation. A wrong
    direction still fits with a small residual (the values are only assigned in reverse), so the
    by-eye check of three printed labels per axis (docs/CURVE-READING.md, section 2) is what
    catches it; tested 2026-10-13 on FC-2C turned sideways: the right directions reproduce the
    upright map within 0.86 psf, the wrong y direction fits as well and is off by 6000 psf.

    An axis drawn evenly in a function of its value is declared with --x-transform or --y-transform
    (D-027): log10 for log paper (grain size), reciprocal for an axis drawn evenly in 1/value (unit
    weight on the density charts of Appendix A). Readers give the printed values, never logarithms;
    the tool predicts, fits and interpolates in the plotting coordinate q = T(value) and writes values
    in the printed unit, so `ax`, `ay`, the residuals and `x_per_px`, `y_per_px` of such an axis are in
    q. A calibration without the keys is linear. A read bound is the largest change of the value over
    the point's interval in q, mapped back: a symmetric, conservative half width of an interval that is
    asymmetric in the printed unit (the tools say how many points are asymmetric by more than 10
    percent; the pixels and the calibration keep the exact interval recoverable).

Pixel coordinates are those of the unrotated page image (u right, v down, origin top-left).
Needs Pillow and NumPy; nothing is installed by this tool.
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

# Axis transforms (D-027): q = T(z) is the plotting coordinate in which the printed grid is drawn evenly;
# values are written in the printed unit, z = T^-1(q). Each entry: forward, inverse, dz/dq.
TRANSFORMS = {
    "linear": (lambda z: z, lambda q: q, lambda q: 1.0),
    "log10": (math.log10, lambda q: 10.0 ** q, lambda q: math.log(10.0) * 10.0 ** q),
    "reciprocal": (lambda z: 1.0 / z, lambda q: 1.0 / q, lambda q: -1.0 / q ** 2),
}
ASYMMETRY_NOTE = 1.1   # an interval whose two halves differ by more than 10 percent is counted and reported


def forward(name, z):
    """q = T(z), the domain checked: a log axis carries no zero or negative value, a reciprocal one no zero."""
    if name == "log10" and not z > 0:
        raise ValueError(f"a log axis cannot carry the value {z:g}")
    if name == "reciprocal" and z == 0:
        raise ValueError("a reciprocal axis cannot carry the value 0")
    return TRANSFORMS[name][0](z)


def axis_transforms(cal):
    """The transforms of a calibration's x and y axes (linear when not recorded)."""
    return cal.get("x_transform", "linear"), cal.get("y_transform", "linear")


def native_interval(name, q, dq):
    """(z, half width, lower half, upper half) of the values T^-1([q - dq, q + dq]); on a linear axis
    exactly (q, dq, dq, dq). An interval reaching a reciprocal axis's singularity has no finite bound."""
    if name == "linear":
        return q, dq, dq, dq
    inv = TRANSFORMS[name][1]
    if name == "reciprocal" and (q - dq) * (q + dq) <= 0:
        raise ValueError("an interval reaches the reciprocal axis's singularity")
    z = inv(q)
    lo_end, hi_end = sorted((inv(q - dq), inv(q + dq)))
    lo, hi = z - lo_end, hi_end - z
    return z, max(lo, hi), lo, hi


def decimals(per_px):
    """Three significant digits of one pixel's worth of value, never fewer than three decimals."""
    return max(3, 3 - math.floor(math.log10(per_px)))


def asymmetric(lo, hi):
    return min(lo, hi) > 0 and max(lo, hi) / min(lo, hi) > ASYMMETRY_NOTE


def dark_runs(frac, min_frac):
    idx = np.where(frac >= min_frac)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i != p + 1:
            out.append(((s + p) / 2, frac[s:p + 1].max()))
            s = i
        p = i
    out.append(((s + p) / 2, frac[s:p + 1].max()))
    return out


def locate(g, box, values, axis, bands, dark, min_frac, snap, frame_frac=0.75, qvals=None):
    """Locate len(values) parallel grid lines (qvals: the values in the plotting coordinate, D-027). axis 'h': horizontal lines (positions in v, found
    in vertical strips along u); axis 'v': vertical lines (positions in u, strips along v).
    Returns a list of (value, slope, intercept, source) with position = intercept + slope * t,
    where t is the coordinate along the line (u for horizontal lines, v for vertical ones)."""
    u0, v0, u1, v1 = box
    sub = g[v0:v1, u0:u1] < dark
    n = len(values)
    length = (u1 - u0) if axis == "h" else (v1 - v0)
    width = length // bands
    off_t = u0 if axis == "h" else v0          # coordinate along the line
    off_p = v0 if axis == "h" else u0          # coordinate across the line (its position)
    # Candidates per band, then tracks: a candidate continues a track when it lies within `snap`
    # pixels of the track's last position (a tilt of a degree moves a line by about a pixel per
    # band). A grid line spans the box, so its track covers most bands; a curve plateau, a label
    # or a legend line covers a few bands only and is dropped by the coverage threshold.
    tracks = []
    for b in range(bands):
        lo, hi = b * width, (b + 1) * width if b < bands - 1 else length
        strip = sub[:, lo:hi] if axis == "h" else sub[lo:hi, :]
        frac = strip.mean(axis=1) if axis == "h" else strip.mean(axis=0)
        t = (lo + hi) / 2 + off_t
        for c, f in dark_runs(frac, min_frac):
            pos = c + off_p
            best = None
            for tr in tracks:
                if tr["last_band"] < b and abs(tr["pos"][-1] - pos) <= snap:
                    d = abs(tr["pos"][-1] - pos)
                    if best is None or d < best[0]:
                        best = (d, tr)
            if best:
                tr = best[1]
                tr["t"].append(t); tr["pos"].append(pos); tr["f"].append(f); tr["last_band"] = b
            else:
                tracks.append({"t": [t], "pos": [pos], "f": [f], "last_band": b})
    good = [tr for tr in tracks if len(tr["t"]) >= frame_frac * bands]
    good.sort(key=lambda tr: np.mean(tr["pos"]))
    if len(good) < 2:
        raise SystemExit(f"{axis}: fewer than two grid lines span {frame_frac:.0%} of the bands; lower --frame-frac or --min-frac, or adjust the box.")
    # The outermost long tracks are the frame lines. Each expected line is matched to the track
    # nearest its equally spaced prediction, within a quarter of the spacing; an expected line
    # with no track (hidden behind a legend, too faint) is interpolated from the frame lines and
    # marked `predicted` for the reader to check. Extra tracks (curve plateaus) are dropped.
    positions = [float(np.mean(tr["pos"])) for tr in good]
    first, last = positions[0], positions[-1]
    # each expected line is predicted where its value falls between the frame lines in the plotting
    # coordinate, and matched within a quarter of the distance to its nearest predicted neighbour (D-027:
    # on log paper the decades and their subdivisions are not equally spaced; until 2026-10-14 the
    # prediction assumed equally spaced values)
    qv = qvals if qvals is not None else values
    frac = [(q - qv[0]) / (qv[-1] - qv[0]) for q in qv]
    pred = [first + (last - first) * f for f in frac]
    window = [min(abs(pred[i] - pred[k]) for k in (i - 1, i + 1) if 0 <= k < n) / 4 for i in range(n)]
    fits = []
    for tr in good:
        pts = np.array(list(zip(tr["t"], tr["pos"])))
        fits.append((np.polyfit(pts[:, 0], pts[:, 1], 1), pts))
    lines, used = [], set()
    for i in range(n):
        j = min(range(len(good)), key=lambda j: abs(positions[j] - pred[i]))
        if abs(positions[j] - pred[i]) <= window[i] and j not in used:
            used.add(j)
            (slope, intercept), pts = fits[j]
            lines.append((values[i], float(slope), float(intercept), f"detected in {len(pts)}/{bands} bands", pts.tolist()))
        else:
            (s0, i0), _ = fits[0]
            (s1, i1), _ = fits[-1]
            w = frac[i]
            lines.append((values[i], float(s0 * (1 - w) + s1 * w), float(i0 * (1 - w) + i1 * w), "predicted", []))
    dropped = [positions[j] for j in range(len(good)) if j not in used]
    if dropped:
        print(f"  note ({axis}): tracks dropped as not grid lines at {', '.join(f'{p:.0f}' for p in dropped)}")
    return lines


def intersect(hline, vline):
    """Horizontal line v = ih + sh*u; vertical line u = iv + sv*v. Solve for (u, v)."""
    _, sh, ih, _, _ = hline
    _, sv, iv, _, _ = vline
    # u = iv + sv*(ih + sh*u)  ->  u (1 - sv*sh) = iv + sv*ih
    u = (iv + sv * ih) / (1 - sv * sh)
    v = ih + sh * u
    return u, v


def fit_affine(anchors, tx="linear", ty="linear"):
    """Least-squares affine maps from pixels to the plotting coordinates of the anchors' values."""
    U = np.array([[a["u"], a["v"], 1.0] for a in anchors])
    X = np.array([forward(tx, float(a["x_value"])) for a in anchors], dtype=float)
    Y = np.array([forward(ty, float(a["y_value"])) for a in anchors], dtype=float)
    ax, *_ = np.linalg.lstsq(U, X, rcond=None)
    ay, *_ = np.linalg.lstsq(U, Y, rcond=None)
    rx, ry = X - U @ ax, Y - U @ ay
    return ax.tolist(), ay.tolist(), float(np.sqrt((rx ** 2).mean())), float(np.sqrt((ry ** 2).mean())), float(np.abs(rx).max()), float(np.abs(ry).max())


def cmd_detect(a):
    g = np.asarray(Image.open(a.image).convert("L"))
    xs = [float(x) for x in a.x_values.split(",")]
    ys = [float(y) for y in a.y_values.split(",")]
    # Which page lines carry which axis. On an upright plot (the default) vertical grid lines carry
    # x values (left to right) and horizontal lines carry y values; the image v axis runs downward,
    # so the topmost horizontal line is the largest y. A figure printed sideways is read on the page
    # as scanned (docs/CURVE-READING.md, rule 5): --x-direction up or down puts x on the horizontal
    # lines, --y-direction left or right puts y on the vertical lines. locate() wants each list in
    # page order (left to right, top to bottom), hence the reversals.
    xdir, ydir = a.x_direction, a.y_direction
    if (xdir in ("right", "left")) == (ydir in ("right", "left")):
        sys.exit("--x-direction and --y-direction must be perpendicular")
    in_page_order = lambda vals, d: list(reversed(vals)) if d in ("left", "up") else vals
    on_v = (xs, xdir, "x") if xdir in ("right", "left") else (ys, ydir, "y")
    on_h = (ys, ydir, "y") if on_v[2] == "x" else (xs, xdir, "x")
    tr = {"x": a.x_transform, "y": a.y_transform}
    vvals, hvals = in_page_order(*on_v[:2]), in_page_order(*on_h[:2])
    vlines = locate(g, a.box, vvals, "v", a.bands, a.dark, a.min_frac, a.snap, a.frame_frac,
                    qvals=[forward(tr[on_v[2]], z) for z in vvals])
    hlines = locate(g, a.box, hvals, "h", a.bands, a.dark, a.min_frac, a.snap, a.frame_frac,
                    qvals=[forward(tr[on_h[2]], z) for z in hvals])
    anchors = []
    for h in hlines:
        for v in vlines:
            u, vv = intersect(h, v)
            xl, yl = (v, h) if on_v[2] == "x" else (h, v)
            anchors.append({"x_value": xl[0], "y_value": yl[0], "u": round(u, 1), "v": round(vv, 1),
                            "x_source": xl[3], "y_source": yl[3]})
    ax, ay, rmsx, rmsy, maxx, maxy = fit_affine(anchors, a.x_transform, a.y_transform)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
        w.writeheader()
        w.writerows(anchors)
    cal = {
        "image": a.image, "box": a.box, "bands": a.bands, "dark": a.dark, "min_frac": a.min_frac, "snap": a.snap,
        "model": "x = ax[0]*u + ax[1]*v + ax[2]; y = ay[0]*u + ay[1]*v + ay[2] (affine, least squares on the grid intersections)",
        "ax": ax, "ay": ay,
        "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
        "rms_residual_x": rmsx, "rms_residual_y": rmsy, "max_residual_x": maxx, "max_residual_y": maxy,
        "n_anchors": len(anchors),
        "vertical_lines": [{f"{on_v[2]}_value": l[0], "slope_du_dv": l[1], "u_at_v0": l[2], "source": l[3], "samples": l[4]} for l in vlines],
        "horizontal_lines": [{f"{on_h[2]}_value": l[0], "slope_dv_du": l[1], "v_at_u0": l[2], "source": l[3], "samples": l[4]} for l in hlines],
    }
    if (xdir, ydir) != ("right", "up"):   # recorded only for a figure printed sideways, so upright output is unchanged
        cal["x_direction"], cal["y_direction"] = xdir, ydir
    for k, t in (("x_transform", a.x_transform), ("y_transform", a.y_transform)):
        if t != "linear":   # recorded only for a transformed axis, so linear output is unchanged (D-027)
            cal[k] = t
            cal["model"] = cal["model"].split(" (D-027")[0] + " (D-027: x and y here are the plotting coordinates T(value) of the axes' transforms)"
    (out / "calibration.json").write_text(json.dumps(cal, indent=1), encoding="utf-8")
    print(f"{len(anchors)} anchors; x: {cal['x_per_px']:.4f} per px, rms residual {rmsx:.3f}, max {maxx:.3f}; "
          f"y: {cal['y_per_px']:.4f} per px, rms residual {rmsy:.3f}, max {maxy:.3f}")
    for l in vlines:
        print(f"  vertical   {on_v[2]}={l[0]:>8g}  u = {l[2]:.1f} + {l[1]:+.4f} v   ({l[3]})")
    for l in hlines:
        print(f"  horizontal {on_h[2]}={l[0]:>8g}  v = {l[2]:.1f} + {l[1]:+.4f} u   ({l[3]})")
    return 0


def cmd_apply(a):
    cal = json.loads(Path(a.calibration).read_text(encoding="utf-8"))
    ax, ay = cal["ax"], cal["ay"]
    with Path(a.points).open(encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        rows, cols = list(rd), rd.fieldnames
    # decimals: three significant digits of one pixel's worth of value, never fewer than three. A
    # fixed three decimals was 0.3 percent of the span on an axis in inches running to 0.32 (Fig.
    # C-7B) and printed its bounds as 0.0 (found by a Claude reader, 2026-10-13); psf axes keep 3
    dx = max(3, 3 - math.floor(math.log10(cal["x_per_px"])))
    dy = max(3, 3 - math.floor(math.log10(cal["y_per_px"])))
    tx, ty = axis_transforms(cal)
    n_asym = 0
    for r in rows:
        u, v = float(r["pixel_u"]), float(r["pixel_v"])
        bu, bv = float(r.get("u_bound_px") or 0), float(r.get("v_bound_px") or 0)
        # in the plotting coordinate, then back to the printed unit (D-027; on a linear axis exactly as before)
        for k, t, A, d, rms, per_px in (("x", tx, ax, dx, cal["rms_residual_x"], cal["x_per_px"]),
                                        ("y", ty, ay, dy, cal["rms_residual_y"], cal["y_per_px"])):
            z, b, lo, hi = native_interval(t, A[0] * u + A[1] * v + A[2], abs(A[0]) * bu + abs(A[1]) * bv + rms)
            if t != "linear":
                d = decimals(abs(TRANSFORMS[t][2](forward(t, z))) * per_px)
                n_asym += asymmetric(lo, hi)
            r[f"{k}_native"], r[f"{k}_read_bound"] = round(z, d), round(b, d)
    extra = [c for c in ("x_native", "y_native", "x_read_bound", "y_read_bound") if c not in cols]
    with Path(a.out).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols + extra, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {a.out}: {len(rows)} points converted with {a.calibration}"
          + (f"; {n_asym} values with an interval asymmetric by more than 10 percent (bound: the larger half)" if n_asym else ""))
    return 0


LINE_LOCATION_PX = 0.5   # a knot line located from one tick (no fit scatter to measure) is known to about half a pixel
INK_HALF_WIDTH_PX = 6    # the ink check looks this far either side of a line, across it
INK_HALF_LENGTH_PX = 4   # and averages this far along it
INK_POSITIONS = 25       # positions checked along a drawn line (a tick is checked where it is)
INK_QUANTILE = 80        # a line's ink error: this percentile of |offset| (robust to curves and symbols crossing it)
ON_INK_PX = 2.0          # a reader's line is verified when its median distance from the ink is within 2 px (two thirds
                         # of a line width; on Appendix C both readers' lines sit within 1.8 px where they coincide,
                         # and a misplaced line sits 2.9 px or more from the ink)
TICK_STUB_PX = (-14, -10, -6, 6, 10, 14)   # where a lone tick is checked, along it from its anchor
TICK_SPAN_PX = 60        # a line whose anchors span no more than this is a tick: its own tilt, measured over a few tens
                         # of pixels, would move it by tens of pixels across the plot (Codex's ticks of Appendix B,
                         # anchored at every pixel along 19 px, 2026-10-15), so it takes the tilt of the affine map


def ink_positions(t_anchors):
    """Where along a line to check its ink: between its anchors (crossings with other grid lines and
    ticks, where the ink is a blob), at a quarter, half and three quarters of every gap wide enough,
    evenly thinned to INK_POSITIONS. A lone tick is read where it meets the axis line, which can be as
    thick as the check's window (8 px on Fig. C-2A): it is checked on its stubs, 6 to 14 px either side
    of the anchor, where only the tick has ink."""
    ts = sorted(set(round(float(t), 3) for t in t_anchors))
    if ts[-1] - ts[0] <= 1:
        return [ts[0] + d for d in TICK_STUB_PX]
    keep = INK_HALF_LENGTH_PX + 3
    pos = [a + f * (b - a) for a, b in zip(ts, ts[1:]) if b - a > 2 * keep for f in (0.25, 0.5, 0.75)]
    if not pos and ts[-1] - ts[0] > 2 * INK_HALF_LENGTH_PX + 2:
        # anchors packed closer than the check window, such as a short tick measured at every pixel along its
        # length (Codex's ticks of Appendix B, 2026-10-15, all rejected as "0 of 0" before): check evenly along
        # the stretch they cover, the averaging window kept inside it
        pos = [float(x) for x in np.linspace(ts[0] + INK_HALF_LENGTH_PX, ts[-1] - INK_HALF_LENGTH_PX, 5)]
    if len(pos) > INK_POSITIONS:
        pos = [pos[int(round(i))] for i in np.linspace(0, len(pos) - 1, INK_POSITIONS)]
    return pos


def load_anchors(cal_dir):
    """The anchors of a calibration directory: anchors.csv, or the `anchors` list a hand-made tick
    calibration keeps inside calibration.json (Claude's FC-3A tick map, batch curves-appc-b5)."""
    d = Path(cal_dir)
    if (d / "anchors.csv").exists():
        with (d / "anchors.csv").open(encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    cal = json.loads((d / "calibration.json").read_text(encoding="utf-8"))
    return [{k: ("" if v is None else str(v)) for k, v in a.items()} for a in cal.get("anchors", [])]


def ink_offset(gray, p, e_s, e_t):
    """Where the ink of a line passing near page point p lies, measured across the line (along e_s)
    from p, in pixels: the darkness-weighted centre of the line's core in the profile across it,
    averaged over a short stretch along it. None when there is no ink contrast there. `gray` is a float
    array (0 black, 255 white). Independent of how the line was located: it reads the page again."""
    s_off = np.arange(-INK_HALF_WIDTH_PX, INK_HALF_WIDTH_PX + 0.01, 0.25)
    t_off = np.arange(-INK_HALF_LENGTH_PX, INK_HALF_LENGTH_PX + 0.01, 1.0)
    S, T = np.meshgrid(s_off, t_off)
    U = p[0] + S * e_s[0] + T * e_t[0]
    V = p[1] + S * e_s[1] + T * e_t[1]
    h, w = gray.shape
    if U.min() < 0 or V.min() < 0 or U.max() > w - 2 or V.max() > h - 2:
        return None
    u0, v0 = np.floor(U).astype(int), np.floor(V).astype(int)
    fu, fv = U - u0, V - v0
    g = (gray[v0, u0] * (1 - fu) * (1 - fv) + gray[v0, u0 + 1] * fu * (1 - fv)
         + gray[v0 + 1, u0] * (1 - fu) * fv + gray[v0 + 1, u0 + 1] * fu * fv)
    prof = g.mean(axis=0)
    dark = np.clip(np.max(prof) - prof, 0, None)        # background: the lightest part of the window
    if dark.max() < 40:                                   # no line here (a gap, a missing tick)
        return None
    core = dark >= 0.5 * dark.max()                      # the line's core, not its faint halo
    i = int(np.argmax(dark))
    lo, hi = i, i
    while lo > 0 and core[lo - 1]:
        lo -= 1
    while hi < len(core) - 1 and core[hi + 1]:
        hi += 1
    wgt = dark[lo:hi + 1]
    return float(np.sum(s_off[lo:hi + 1] * wgt) / np.sum(wgt))


class AxisKnots:
    """The lines of constant value of one axis (D-025): for each printed value with anchors that are
    not `predicted`, the line s = s0 + k t, where s is the page coordinate across the lines (along the
    affine gradient of the axis) and t the coordinate along them. A grid line with several anchors keeps
    its own tilt; a lone tick takes the tilt of the affine map (k = 0).

    With the page image every reader's line is checked against the ink (`ink_offset` at
    `ink_positions`), and only a verified line is a knot; a line that fails is kept in `rejected` with
    the reason, like a predicted line it is not evidence of the scale. A drawn line is verified when
    the ink found along it supports its whole length: ink at a quarter of its positions or more (at
    least 3), spread over a third of its length or more, and the straight line fitted to the ink
    (robustly: offsets more than 3 MAD from a first fit, at least 1.5 px, are set aside as crossing
    curves or symbols) within 2 px of the reader's line at both ends of the line's length. (Codex's
    review, 2026-10-14: a median distance alone passed a line 12 px off at both ends that found ink
    only near its middle; the pilot's x = 50 line of Claude's FC-1B calibration, found in 10 of 24
    bands, is 16 px from the ink at the top of the plot.) A lone tick is verified on its stubs: ink at
    two positions or more within a median 2 px. A line whose ink is too scarce to judge is rejected as
    `insufficient ink`, one the ink contradicts as `misplaced`.

    A knot's location error (pixels) is the largest of: half a pixel; the scatter of its anchors about
    its fitted line; and, with the image, the largest distance between the reader's line and the ink's
    line over the line's length plus the RMS scatter of the ink about its own line (a tick: the 80th
    percentile of its stub distances)."""

    def __init__(self, anchors, value_col, source_col, grad, gray=None, transform="linear"):
        self.transform = transform   # D-027: lines keep their printed value, interpolation is in q = T(value)
        g = np.array(grad, dtype=float)
        self.e_s = g / np.hypot(*g)                       # across the lines, towards increasing value
        self.e_t = np.array([-self.e_s[1], self.e_s[0]])  # along the lines
        by = {}
        for a in anchors:
            if "predicted" in (a.get(source_col) or "") or str(a.get(value_col, "")).strip() == "":
                continue   # an interpolated line is not evidence of the scale; a row may anchor one axis only
            by.setdefault(float(a[value_col]), []).append((float(a["u"]), float(a["v"])))
        self.knots = []     # dicts: value, s0, k, t (anchor positions along the line), err (px), check (the ink check)
        self.rejected = []  # the same, with `reason`, for lines that failed the ink check
        for val, pts in sorted(by.items()):
            P = np.array(pts)
            s, t = P @ self.e_s, P @ self.e_t
            if len(P) >= 2 and np.ptp(t) > TICK_SPAN_PX:
                k, s0 = np.polyfit(t, s, 1)
                scatter = float(np.sqrt(np.mean((s - (s0 + k * t)) ** 2))) if len(P) >= 3 else 0.0
            else:
                k, s0, scatter = 0.0, float(np.mean(s)), 0.0
            kn = {"value": val, "q": forward(transform, val), "s0": float(s0), "k": float(k), "t": [float(x) for x in t], "check": {}}
            kn["err"] = max(LINE_LOCATION_PX, scatter)
            if gray is not None:
                ok, err, reason, check = self.check_line(gray, kn)
                kn["check"] = check
                kn["err"] = max(kn["err"], err)
                if not ok:
                    kn["reason"] = reason
                    self.rejected.append(kn)
                    continue
            self.knots.append(kn)
        if len(self.knots) < 2:
            raise ValueError("fewer than two verified lines on an axis")
        self.check_order()

    def check_line(self, gray, kn):
        """(verified, location error px, reason, record) of a reader's line against the ink."""
        pos = ink_positions(kn["t"])
        found, missing = [], []
        for tt in pos:
            p = self.line_s(kn, tt) * self.e_s + tt * self.e_t
            off = ink_offset(gray, p, self.e_s, self.e_t)
            (missing.append(round(tt, 1)) if off is None else found.append((tt, -off)))   # reader's line minus the ink
        rec = {"positions": len(pos), "found": [[round(tt, 1), round(o, 2)] for tt, o in found], "missing": missing}
        if np.ptp(kn["t"]) <= TICK_SPAN_PX:   # a tick: on its stubs, or along its own short stretch
            offs = np.array([o for _, o in found])
            if len(offs) < 2:
                return False, 0.0, f"insufficient ink: tick found at {len(offs)} of {len(pos)} stub positions", rec
            med = float(np.median(np.abs(offs)))
            rec["median_px"] = round(med, 2)
            if med > ON_INK_PX:
                return False, 0.0, f"misplaced: tick {med:.2f} px from the ink (median of its stubs)", rec
            return True, float(np.percentile(np.abs(offs), INK_QUANTILE)), "", rec
        t0, t1 = min(kn["t"]), max(kn["t"])
        need = max(3, len(pos) / 4)
        span = (max(tt for tt, _ in found) - min(tt for tt, _ in found)) if len(found) >= 2 else 0.0
        rec["span_fraction"] = round(span / (t1 - t0), 2)
        if len(found) < need or span < (t1 - t0) / 3:
            return False, 0.0, (f"insufficient ink: found at {len(found)} of {len(pos)} positions over "
                                f"{span / (t1 - t0):.0%} of the line's length"), rec
        T, O = np.array([tt for tt, _ in found]), np.array([o for _, o in found])
        c1, c0 = np.polyfit(T, O, 1)
        res = O - (c0 + c1 * T)
        mad = float(np.median(np.abs(res - np.median(res)))) * 1.4826
        keep = np.abs(res) <= max(1.5, 3 * mad)
        if keep.sum() >= max(3, need):
            c1, c0 = np.polyfit(T[keep], O[keep], 1)
            res = O[keep] - (c0 + c1 * T[keep])
        rms = float(np.sqrt(np.mean(res ** 2)))
        dev = max(abs(c0 + c1 * t0), abs(c0 + c1 * t1))   # reader's line against the ink's line, at its ends
        rec.update({"ink_line_offset_px": [round(float(c0 + c1 * t0), 2), round(float(c0 + c1 * t1), 2)],
                    "ink_scatter_px": round(rms, 2), "set_aside": int((~keep).sum())})
        if dev > ON_INK_PX:
            return False, 0.0, f"misplaced: {dev:.2f} px from the ink's line at an end of the line", rec
        return True, dev + rms, "", rec

    def check_order(self):
        """Two adjacent lines whose position intervals overlap leave the scale between them undefined."""
        ts = [t for kn in self.knots for t in kn["t"]]
        for t in (min(ts), max(ts)):
            at = sorted(((self.line_s(kn, t), kn) for kn in self.knots), key=lambda x: x[0])
            for (sa, a), (sb, b) in zip(at, at[1:]):
                if sb - sa <= a["err"] + b["err"]:
                    raise ValueError(f"lines {a['value']:g} and {b['value']:g} overlap within their location errors")

    @staticmethod
    def line_s(kn, t):
        return kn["s0"] + kn["k"] * t

    def coords(self, u, v):
        p = np.array([u, v], dtype=float)
        return float(p @ self.e_s), float(p @ self.e_t)

    def _interp(self, s, t, shift=None):
        """(q, scale in q per px, bracketing pair, extrapolated) at (s, t), in the plotting coordinate (the
        printed value on a linear axis), with the lines shifted across by `shift` (knot index -> px); the
        bracket is recomputed from the shifted positions."""
        shift = shift or {}
        at = sorted((self.line_s(kn, t) + shift.get(i, 0.0), kn["q"], i) for i, kn in enumerate(self.knots))
        vals = [x[1] for x in at]
        if vals != sorted(vals) and vals != sorted(vals, reverse=True):
            raise ValueError("shifted lines change order: their position intervals overlap")
        j = next((j for j in range(len(at) - 1) if at[j][0] <= s <= at[j + 1][0]), None)
        extra = j is None
        if extra:
            j = 0 if s < at[0][0] else len(at) - 2
        (sa, va, ia), (sb, vb, ib) = at[j], at[j + 1]
        scale = (vb - va) / (sb - sa)
        return va + (s - sa) * scale, scale, (ia, ib), extra

    def value(self, u, v):
        """(value, local scale in value per px across the lines, bracketing location error in value, extrapolated)"""
        s, t = self.coords(u, v)
        q, scale, (ia, ib), extra = self._interp(s, t)
        _, inv, dz = TRANSFORMS[self.transform]
        scale = scale * dz(q)   # value per px in the printed unit (a local derivative on a transformed axis)
        return inv(q), scale, abs(scale) * max(self.knots[ia]["err"], self.knots[ib]["err"]), extra

    def value_q(self, u, v):
        """As `value`, in the plotting coordinate q, where a line's location error is a fixed number of pixels
        times a locally constant scale (the comparison of two maps is made here; Codex's review of D-027:
        a derivative in the printed unit understates the error of an extrapolated log value fourfold). On
        a linear axis the same numbers as `value`."""
        s, t = self.coords(u, v)
        q, scale, (ia, ib), extra = self._interp(s, t)
        return q, scale, abs(scale) * max(self.knots[ia]["err"], self.knots[ib]["err"]), extra

    def interval(self, u, v, bu, bv):
        """(value, read bound, extrapolated): the largest change of value over the point's pixel interval
        (its four corners and its centre) with each of the two lines bracketing it moved to either end of
        its own position interval, the bracket recomputed after the move. The positions are propagated
        exactly, so a point beyond the outermost line, or near an uncertain outer line, gets the wider
        bound it needs (Codex's review, 2026-10-14); no global residual (D-025). On a transformed axis the
        moves are made in q and each result mapped back, so the bound is the larger half of the interval in
        the printed unit (D-027)."""
        val, lo, hi, extra = self.interval_ends(u, v, bu, bv)
        return val, max(lo, hi), extra

    def interval_ends(self, u, v, bu, bv):
        """(value, how far below it, how far above it, extrapolated): see `interval`."""
        inv = TRANSFORMS[self.transform][1]
        s, t = self.coords(u, v)
        q0, _, (ia, ib), extra = self._interp(s, t)
        qs = [q0]
        for du, dv in ((0, 0), (-bu, -bv), (-bu, bv), (bu, -bv), (bu, bv)):
            sc, tc = self.coords(u + du, v + dv)
            _, _, (ja, jb), xx = self._interp(sc, tc)
            extra = extra or xx
            for da in (-1, 1):
                for db in (-1, 1):
                    qs.append(self._interp(sc, tc, {ja: da * self.knots[ja]["err"], jb: db * self.knots[jb]["err"]})[0])
        if self.transform == "reciprocal" and min(qs) * max(qs) <= 0:
            # the interval reaches 1/value = 0: the value is unbounded there, not a finite number (Codex's review)
            raise ValueError(f"the interval of the point at ({u:.1f}, {v:.1f}) reaches the reciprocal axis's singularity")
        val = inv(q0)
        lo = hi = 0.0
        for q in qs[1:]:
            vv = inv(q)
            lo, hi = max(lo, val - vv), max(hi, vv - val)
        return val, lo, hi, extra


def piecewise_maps(cal_dir, image=None):
    """The calibration and the x and y knots of a calibration directory (anchors.csv and
    calibration.json, or anchors kept in calibration.json); with the page image, each line is also
    checked against the ink."""
    cal = json.loads((Path(cal_dir) / "calibration.json").read_text(encoding="utf-8"))
    an = load_anchors(cal_dir)
    gray = np.asarray(Image.open(image).convert("L"), dtype=float) if image else None
    tx, ty = axis_transforms(cal)
    return (cal, AxisKnots(an, "x_value", "x_source", cal["ax"][:2], gray, tx),
            AxisKnots(an, "y_value", "y_source", cal["ay"][:2], gray, ty))


def compare_knots(KA, KB, gray):
    """The lines of one axis in two readings, value by value (D-025). For a value both readings hold,
    positions are taken along the stretch both lines cover, in one page frame (A's: B's anchors are
    projected onto A's line direction; Codex's review, 2026-10-14), between the anchors of both (or on
    the stubs of a tick); at each, the ink is located once around the midpoint of the two lines and each
    reading's distance from it measured in pixels. Returns (rows, only_a, only_b): rows are dicts
    value, n (positions with ink), gap_px (largest distance between the two lines over the positions),
    off_a, off_b (signed distances from the ink)."""
    if KA.transform != KB.transform:
        raise ValueError(f"the readings declare different axis transforms ({KA.transform}, {KB.transform}): "
                         "settle the axis type from the page before comparing")
    va = {kn["value"]: kn for kn in KA.knots}
    vb = {kn["value"]: kn for kn in KB.knots}
    e_s, e_t = KA.e_s, KA.e_t

    def t_in_a(K, kn):   # the anchors of a reading's line, as positions along A's line direction
        return [float((K.line_s(kn, t) * K.e_s + t * K.e_t) @ e_t) for t in kn["t"]]

    rows = []
    for val in sorted(set(va) & set(vb)):
        a, b = va[val], vb[val]
        ta, tb = a["t"], t_in_a(KB, b)
        if np.ptp(ta) > TICK_SPAN_PX and np.ptp(tb) > TICK_SPAN_PX:   # two drawn lines: along the stretch both cover
            lo, hi = max(min(ta), min(tb)), min(max(ta), max(tb))
            ts = [t for t in ink_positions(ta + tb) if lo - 1 <= t <= hi + 1]
        else:                                           # a tick in either reading: on the stubs of the ticks as read
            ts = ink_positions(ta) + ink_positions(tb)
        off_a, off_b, gap = [], [], 0.0
        for t in ts:
            sa = KA.line_s(a, t)
            pa = sa * e_s + t * e_t
            tb_ = float(pa @ KB.e_t)                     # B's line near that point, in A's frame
            sb = float((KB.line_s(b, tb_) * KB.e_s + tb_ * KB.e_t) @ e_s)
            gap = max(gap, abs(sa - sb))
            mid = 0.5 * (sa + sb)
            off = ink_offset(gray, mid * e_s + t * e_t, e_s, e_t)
            if off is None:
                continue
            ink = mid + off
            off_a.append(sa - ink)
            off_b.append(sb - ink)
        rows.append({"value": val, "n": len(off_a), "gap_px": gap, "off_a": off_a, "off_b": off_b})
    return rows, sorted(set(va) - set(vb)), sorted(set(vb) - set(va))


def knots_summary(X, Y):
    """A JSON-ready record of the lines a piecewise map uses and of those its ink check rejected."""
    def axis(lines):
        return [{"value": kn["value"], "s0_px": round(kn["s0"], 2), "tilt": round(kn["k"], 5),
                 "location_error_px": round(kn["err"], 2), "n_anchors": len(kn["t"]), "ink_check": kn["check"],
                 **({"reason": kn["reason"]} if "reason" in kn else {})} for kn in lines]
    out = {"across_x": [round(float(c), 6) for c in X.e_s], "across_y": [round(float(c), 6) for c in Y.e_s],
           "x": axis(X.knots), "y": axis(Y.knots), "rejected_x": axis(X.rejected), "rejected_y": axis(Y.rejected)}
    for k, K in (("x_transform", X), ("y_transform", Y)):
        if K.transform != "linear":   # recorded only for a transformed axis (D-027)
            out[k] = K.transform
    return out


def recover_line(gray, K, value, t_range, search_px=60, step=50):
    """Measure on the page a line of constant `value` that a reading left out or misplaced (D-025): its
    position is predicted from the reading's own two nearest verified lines (extrapolated or
    interpolated linearly in value), the darkest long run parallel to them is searched within
    `search_px` across, every `step` px along the line over `t_range`, and refined with `ink_offset`;
    only the points that agree on one straight line are kept (a curve near the line can be darker in
    some bands). Independent of the other reading. Returns (points [(u, v)], straight-line residual RMS px)."""
    qv = forward(K.transform, value)   # predicted in the plotting coordinate (D-027)
    kns = sorted(K.knots, key=lambda kn: abs(kn["q"] - qv))[:2]
    (a, b) = sorted(kns, key=lambda kn: kn["q"])
    f = (qv - a["q"]) / (b["q"] - a["q"])
    pts = []
    for t in np.arange(t_range[0] + step / 2, t_range[1], step):
        s_pred = K.line_s(a, t) + f * (K.line_s(b, t) - K.line_s(a, t))
        best = None
        for ds in np.arange(-search_px, search_px + 0.5, 1.0):
            q = (s_pred + ds) * K.e_s + t * K.e_t
            run = [(s_pred + ds) * K.e_s + (t + dt) * K.e_t for dt in range(-20, 21, 2)]
            vals = [gray[int(round(r[1])), int(round(r[0]))] for r in run
                    if 0 <= int(round(r[1])) < gray.shape[0] and 0 <= int(round(r[0])) < gray.shape[1]]
            if len(vals) < 15:
                continue
            m = float(np.mean(vals))
            if best is None or m < best[0]:
                best = (m, q)
        if best is None or best[0] > 100:      # no long dark run here (a gap, a legend box)
            continue
        off = ink_offset(gray, best[1], K.e_s, K.e_t)
        if off is not None:
            pts.append(tuple(float(c) for c in best[1] + off * K.e_s))
    if len(pts) < 3:
        return pts, float("nan")
    # a plotted curve running near the line can be darker than it in some bands: keep the points that agree
    # on one straight line (the pair of points with the most others within 1.5 px), refit on those
    S = np.array([np.array(q) @ K.e_s for q in pts])
    T = np.array([np.array(q) @ K.e_t for q in pts])
    best = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if abs(T[j] - T[i]) < 1:
                continue
            k = (S[j] - S[i]) / (T[j] - T[i])
            inl = np.abs(S - (S[i] + k * (T - T[i]))) <= 1.5
            if best is None or inl.sum() > best.sum():
                best = inl
    if best is None or best.sum() < 3:
        return pts, float("nan")
    c1, c0 = np.polyfit(T[best], S[best], 1)
    pts = [q for q, keep in zip(pts, best) if keep]
    return pts, float(np.sqrt(np.mean((S[best] - (c0 + c1 * T[best])) ** 2)))


def cmd_recover(a):
    """Print knots.csv rows for a line measured on the page (see `recover_line`)."""
    cal, X, Y = piecewise_maps(a.calibration_dir, a.image)
    K = X if a.axis == "x" else Y
    ts = [t for kn in K.knots for t in kn["t"]]
    gray = np.asarray(Image.open(a.image).convert("L"), dtype=float)
    pts, rms = recover_line(gray, K, a.value, (min(ts), max(ts)))
    print(f"{len(pts)} points on the {a.axis} = {a.value:g} line, straight-line residual RMS {rms:.2f} px", file=sys.stderr)
    w = csv.writer(sys.stdout, lineterminator="\n")
    for u, v in pts:
        w.writerow([a.figure, a.panel, a.reader, a.value if a.axis == "x" else "", a.value if a.axis == "y" else "",
                    round(u, 2), round(v, 2), a.source if a.axis == "x" else "", a.source if a.axis == "y" else "", a.note])
    return 0


def piecewise_rows(cal, X, Y, rows):
    """Rewrites x_native, y_native, x_read_bound, y_read_bound and cal_model of reader rows in place
    from their pixels; returns the number of points beyond the outermost verified line."""
    dx = max(3, 3 - math.floor(math.log10(cal["x_per_px"])))
    dy = max(3, 3 - math.floor(math.log10(cal["y_per_px"])))
    n_extra = n_asym = 0
    for r in rows:
        u, v = float(r["pixel_u"]), float(r["pixel_v"])
        bu, bv = float(r.get("u_bound_px") or 0), float(r.get("v_bound_px") or 0)
        xv, xb, xo = X.interval(u, v, bu, bv)
        yv, yb, yo = Y.interval(u, v, bu, bv)
        px, py = dx, dy
        asym = []
        for K, k in ((X, "x"), (Y, "y")):
            if K.transform != "linear":   # decimals from the local scale; the asymmetry counted and kept (D-027)
                d = decimals(abs(K.value(u, v)[1]))
                px, py = (d, py) if k == "x" else (px, d)
                _, lo, hi, _ = K.interval_ends(u, v, bu, bv)
                if asymmetric(lo, hi):
                    n_asym += 1
                    asym.append(f"{k} {lo:.4g} below {hi:.4g} above")
        r["x_native"], r["y_native"] = round(xv, px), round(yv, py)
        r["x_read_bound"], r["y_read_bound"] = round(xb, px), round(yb, py)
        r["cal_model"] = "piecewise" + (" extrapolated" + (" x" if xo else "") + (" y" if yo else "") if xo or yo else "")
        if asym:   # the interval's two halves, where they differ by more than 10 percent (the bound is the larger)
            r["cal_model"] += "; asymmetric " + ", ".join(asym)
        n_extra += bool(xo or yo)
    if n_asym:
        print(f"note: {n_asym} values with an interval asymmetric by more than 10 percent (bound: the larger half)", file=sys.stderr)
    return n_extra


def cmd_piecewise(a):
    """Values between the drawn lines (D-025). Writes the same columns as apply plus `cal_model`, which
    names the map and flags a value extrapolated beyond the outermost verified line; with --image each
    line's location error includes its distance from the ink on the page."""
    cal, X, Y = piecewise_maps(a.calibration_dir, a.image)
    with Path(a.points).open(encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        rows, cols = list(rd), rd.fieldnames
    n_extra = piecewise_rows(cal, X, Y, rows)
    extra = [c for c in ("x_native", "y_native", "x_read_bound", "y_read_bound", "cal_model") if c not in cols]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with Path(a.out).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols + extra, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {a.out}: {len(rows)} points, piecewise on {len(X.knots)} x and {len(Y.knots)} y lines "
          f"of {a.calibration_dir}; {n_extra} beyond the outermost verified line")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("detect")
    d.add_argument("image")
    d.add_argument("--box", nargs=4, type=int, required=True)
    d.add_argument("--x-values", required=True)
    d.add_argument("--y-values", required=True)
    d.add_argument("--out", required=True)
    d.add_argument("--bands", type=int, default=5)
    d.add_argument("--dark", type=int, default=200)
    d.add_argument("--min-frac", type=float, default=0.6)
    d.add_argument("--x-direction", choices=["right", "left", "up", "down"], default="right",
                   help="the page direction in which x increases (up or down for a figure printed sideways)")
    d.add_argument("--y-direction", choices=["right", "left", "up", "down"], default="up",
                   help="the page direction in which y increases")
    d.add_argument("--x-transform", choices=list(TRANSFORMS), default="linear",
                   help="log10 for log paper, reciprocal for an axis drawn evenly in 1/value (D-027); give printed values")
    d.add_argument("--y-transform", choices=list(TRANSFORMS), default="linear")
    d.add_argument("--snap", type=float, default=10)
    d.add_argument("--frame-frac", type=float, default=0.5, help="fraction of the bands a line must be found in to count as a grid line")
    p = sub.add_parser("apply")
    p.add_argument("calibration")
    p.add_argument("points")
    p.add_argument("out")
    q = sub.add_parser("piecewise", help="values between the drawn lines (D-025) from a calibration directory")
    q.add_argument("calibration_dir", help="directory with calibration.json and anchors.csv (or anchors inside calibration.json)")
    q.add_argument("points")
    q.add_argument("out")
    q.add_argument("--image", help="the page image: each line's location error then includes its distance from the ink")
    r = sub.add_parser("recover", help="measure on the page a line a reading left out (D-025); prints knots.csv rows")
    r.add_argument("calibration_dir")
    r.add_argument("--image", required=True)
    r.add_argument("--axis", choices=["x", "y"], required=True)
    r.add_argument("--value", type=float, required=True)
    r.add_argument("--figure", required=True)
    r.add_argument("--panel", required=True)
    r.add_argument("--reader", required=True)
    r.add_argument("--source", default="measured on the page (D-025 recovery)")
    r.add_argument("--note", default="")
    a = ap.parse_args()
    return {"detect": cmd_detect, "apply": cmd_apply, "piecewise": cmd_piecewise, "recover": cmd_recover}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
