"""Compare two independent readings of the curves of one figure (see docs/CURVE-READING.md, section 4).

Usage:
    python tools/diff_curves.py <A_points_native.csv> <B_points_native.csv> \
        --cal-a <A calibration.json> --cal-b <B calibration.json> [--labels claude,codex] \
        [--panel 1] [--out report.md] [--canonical canonical.csv] [--decisions decisions.csv]
        [--bound-scale 0.5] [--maps piecewise --image <page.png>]

Inputs are the points files after `tools/calibrate_axes.py apply` (columns x_native, y_native,
x_read_bound, y_read_bound present). Only rows of the given panel are compared (default: all).

The report lists: series present in one reading only; marker symbol disagreements; the two
calibrations compared at the four corners of reading A's box (the same pixels through both maps);
per series the matched points, agreements and disagreements, with both readings and both bounds;
and unmatched points.

Matching rules:
    markers, features, gridline points: by distance on the page (both readings use the same page
        pixels), closest pairs first, each point used once, within --match-px (default: half the
        median distance between consecutive points of that kind in the evaluating reading, at least
        12 px). Agreement: |xA - xB| <= bA + bB and likewise in y. (Until 2026-10-13 points were
        paired by sequence whenever both readings held the same number of them; one marker missing
        at one end and one extra at the other then shifted every pair, as in the lower panel of
        FC-4C. Pairing by position cannot shift.)
    trace points: the two readers sample the drawn line at displacements of their own choosing,
        so x is a sampling location, not a measurement. The other reading's trace is interpolated
        linearly (in drawing order) at each sample of the evaluating reading; agreement is
        |y - y_interp| <= b_y + b_y_other + |slope| (b_x + b_x_other). No interpolation across a
        gap wider than three times the other reading's median sample spacing (a drawn gap); such
        samples are reported unmatched.

    features: paired by role first (first, peak, last, from the reader's note), then by position. A
        peak is compared in y only (on a flat top its x is not an observation) and the canonical x
        bound is widened to take in the other reading's x; first and last points in x and y.
        (Rules agreed with Codex on 2026-10-13, batch curves-appc-b1.)
        With --feature-roles leading (from 2026-11-19, batch curves-s4-b1; set per figure and panel by the
        `feature_roles` column of qa/<batch>/overlays.csv): a history with several maxima, minima and knees
        per series. The note's opening word gives the role (first, last; peak, maximum, crest; knee, with
        "minimum" in the opening clause a minimum), so "knee, minimum after the first peak" is a minimum and
        not a first point; knees and minima pair in one group; a role group with more than one feature on
        either side pairs only within FEATURE_PX on the page, and a minimum paired with a minimum is
        compared like a peak (y only). The default, earliest, keeps the rule above for the batches built
        with it.

With --maps piecewise (D-025, the default of tools/reconcile_curves.py) the points files carry values
from `tools/calibrate_axes.py piecewise` and each calibration's directory holds its anchors; the two
readings' maps are then compared line by line instead of at four corners: for every printed value of
either axis, whether both readings hold the line (coverage), the largest distance between their two
lines, and each line's distance from the ink of the page (located once per position, between the two
lines; `calibrate_axes.compare_knots`), then both maps along every verified line of either reading
and along the midline of every interval between adjacent lines. A reader's line that fails the ink
check is not a knot of its map (`calibrate_axes.AxisKnots`) and is listed. The canonical reading
(D-026): with the same verified lines, the one whose lines lie closer to the ink (the mean over the
shared lines of each line's median distance from the ink); within 0.25 px of each other, the first
submission (A). A reading whose lines include all of the other's and more wins when its shared lines
are as close to the ink; coverage that differs both ways is flagged for review (recover the lines,
or name the canonical reading). A line more than 1 px from the ink in median is flagged.

Without --maps piecewise (affine values), the evaluating reading is the canonical one: per panel the
reading with the smaller calibration RMS residual (sum of x and y RMS in units of the axis span), tie
to A. With --canonical, the
canonical points are written with `status` agreed | pending-review | one-sided per point, a
`source` column naming the reading, and the other reading's value (interpolated for traces).
Points only the other reading holds (markers and features the canonical reader did not record,
trace samples beyond either end of the canonical trace) are written too, as `one-sided` with that
reading as `source`, in its own calibration and numbering; within a series the output is in
drawing order (the other reading's samples before the start of the canonical trace come first, those
after its end last), and tools/build_observations.py keeps that order.
With --decisions, a CSV (panel, series_id, point_kind, sequence, source, status, use, note) overrides
the status of named points after a page re-read: `status` is the new status (resolved,
one-sided-verified, excluded, ...), `use` names the reading whose value is kept (empty keeps the
value of the reading the decision names; the other label swaps in the other reading's whole
submitted record, or for a trace sample a value interpolated on the other trace, source
`<reader>-interp`; `span` keeps the value and widens its x and y read bounds to take in the other
reading's value and bound, for a point neither reading could be shown right on), `note` is kept in
`decision_note`. Excluded points are removed from their reading
before matching and interpolation, leaving a break in a trace. A resolution made on the other
reading's paired marker or feature (when it was canonical) is carried to the pair (D-026).
"""
import argparse
import csv
import json
import math
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import calibrate_axes  # noqa: E402

VALIDATION_TIE_PX = 0.25   # two readings whose lines are this close to the ink, on average, cannot be told apart
OFF_INK_PX = 1.0           # a line whose median distance from the ink exceeds this is flagged in the report


def load(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def key(r):
    return (r["figure_id"], r["panel"], r["series_id"])


def apply_q(cal, u, v):
    """A calibration's affine map, in the plotting coordinates of its axes (the printed values on linear axes)."""
    ax, ay = cal["ax"], cal["ay"]
    return (ax[0] * u + ax[1] * v + ax[2], ay[0] * u + ay[1] * v + ay[2])


def apply_map(cal, u, v):
    """A calibration's affine map in the printed unit (through the axis transforms, D-027)."""
    tx, ty = calibrate_axes.axis_transforms(cal)
    qx, qy = apply_q(cal, u, v)
    return calibrate_axes.TRANSFORMS[tx][1](qx), calibrate_axes.TRANSFORMS[ty][1](qy)


def corners(cal, box, f=apply_map):
    u0, v0, u1, v1 = box
    return [f(cal, u, v) for u, v in ((u0, v0), (u1, v0), (u0, v1), (u1, v1))]


AXES = ("linear", "linear")   # the panel's axis transforms (D-027), set in main from the calibrations


def fmt_value(v):
    """A value written into the canonical file: three decimals on linear axes (as always), six significant
    digits when an axis is transformed (a grain size of 0.074 mm would lose a digit to three decimals)."""
    return f"{v:.3f}" if AXES == ("linear", "linear") else f"{v:.6g}"


def fmt_outward(v):
    """fmt_value rounded up: a bound written to cover another reading must not fall short of it (Codex's review of
    curves-s5-b1, 2026-11-19)."""
    s = fmt_value(v)
    if float(s) >= v:
        return s
    return f"{math.ceil(v * 1000) / 1000:.3f}" if AXES == ("linear", "linear") else f"{v * (1 + 1e-5):.6g}"


BOUND_SCALE = 1.0
FEATURE_ROLES = "earliest"   # --feature-roles
# Two readers' features of one role more than this far apart on the page (about 3 ms on Fig. 4-19, 0.1 in on
# Fig. 4-20) are not shown to be the same feature when a series has several of that role: each stays one-sided.
FEATURE_PX = 40.0


def fl(r, c):
    v = float(r[c])
    return v * BOUND_SCALE if c.endswith("_read_bound") else v


def interp_trace(rows, x, max_gap, reach=0.0):
    """Linear interpolation of a trace (rows in drawing order) at x. Returns
    (y, x_bound, y_bound, slope, pixel_u, pixel_v, x_other) or None when x falls outside the trace or inside a
    drawn gap. The pixel position is interpolated with the same parameter, so a value swapped in by a
    decision keeps a pixel position on the reading it came from. With `reach` (the x bound of the sample
    being compared), an x beyond an end of the trace by no more than `reach` plus that end sample's own x
    bound is compared with the end sample: the two lie within each other's reading bounds, and the
    caller's tolerance carries the x offset into y through the slope (2026-10-15: a sample at 499.9 psf
    was left unmatched by a trace starting at 500.0, and every exclusion at a curve's end made more)."""
    # interpolated in the plotting coordinates, along the curve as drawn (D-027; on linear axes as before)
    fx, fy, iy = (calibrate_axes.TRANSFORMS[AXES[0]][0], calibrate_axes.TRANSFORMS[AXES[1]][0],
                  calibrate_axes.TRANSFORMS[AXES[1]][1])
    pts = [(fl(r, "x_native"), fl(r, "y_native"), fl(r, "x_read_bound"), fl(r, "y_read_bound"),
            float(r["pixel_u"]), float(r["pixel_v"])) for r in rows]
    def intact(i):   # the step from sample i-1 to sample i is drawn (no gap, no break)
        return 0 < i < len(pts) and abs(fx(pts[i][0]) - fx(pts[i - 1][0])) <= max_gap and not rows[i].get("_break_before")

    def end_slope(i, j):   # slope from sample i to its neighbour j, only along a drawn step (Codex's review, 2026-11-19)
        return (pts[j][1] - pts[i][1]) / (pts[j][0] - pts[i][0]) if intact(max(i, j)) and pts[j][0] != pts[i][0] else 0.0

    side = None   # beside a documented break: the nearest end sample of an intact stretch, within the bounds
    for i, ((x0, y0, bx0, by0, u0, v0), (x1, y1, bx1, by1, u1, v1), r1) in enumerate(zip(pts, pts[1:], rows[1:])):
        lo, hi = min(x0, x1), max(x0, x1)
        if lo <= x <= hi and hi > lo:
            # a drawn gap, or a break where an excluded sample was: never bridged; a sample at the end of a
            # gap is still on the next segment, so the search goes on (until 2026-10-14 the first segment
            # holding x decided, and a sample at a dash's end counted as inside the gap before it)
            if abs(fx(x1) - fx(x0)) > max_gap or r1.get("_break_before"):
                if r1.get("_scan_break") and reach > 0 and side is None:
                    # a documented break (--break): the sample is compared directly with the other reading's sample
                    # at the end of the stretch on the sample's own side of the break, as at the end of a trace, never
                    # through the break; a sample inside the break's span has no side (Codex's review, 2026-11-19)
                    blo, bhi = (float(v) for v in r1["_scan_break"].split())
                    lo_end, hi_end = ((i, i - 1), (i + 1, i + 2)) if x0 < x1 else ((i + 1, i + 2), (i, i - 1))
                    k, j = lo_end if x <= blo else hi_end if x >= bhi else (None, None)
                    if k is not None:
                        xe, ye, bxe, bye, ue, ve = pts[k]
                        if abs(x - xe) <= reach + bxe:
                            side = (ye, bxe, bye, end_slope(k, j) if 0 <= j < len(pts) else 0.0, ue, ve, xe)
                continue
            t = (fx(x) - fx(x0)) / (fx(x1) - fx(x0))
            qy = fy(y0) + t * (fy(y1) - fy(y0))
            if AXES == ("linear", "linear"):
                slope = (y1 - y0) / (x1 - x0)
            else:   # dy/dx at x on the segment drawn straight in q, which carries an x bound into y (Codex's review)
                dzx, dzy = calibrate_axes.TRANSFORMS[AXES[0]][2], calibrate_axes.TRANSFORMS[AXES[1]][2]
                slope = dzy(qy) * (fy(y1) - fy(y0)) / (fx(x1) - fx(x0)) / dzx(fx(x))
            return (iy(qy), max(bx0, bx1), max(by0, by1), slope, u0 + t * (u1 - u0), v0 + t * (v1 - v0), x)
    if side is not None:
        return side
    if reach > 0 and len(pts) >= 2:
        xs = [p[0] for p in pts]
        for k, j in ((0, 1), (len(pts) - 1, len(pts) - 2)):
            xe, ye, bxe, bye, ue, ve = pts[k]
            beyond = (x < min(xs)) if xe == min(xs) else (x > max(xs)) if xe == max(xs) else False
            if beyond and abs(x - xe) <= reach + bxe and pts[j][0] != xe:
                # the slope only from a drawn step: a first step across a break carries none (Codex's review)
                slope = (pts[j][1] - ye) / (pts[j][0] - xe) if not rows[max(k, j)].get("_scan_break") else 0.0
                return (ye, bxe, bye, slope, ue, ve, x)   # x as before 2026-11-19 (the other_x of a trace end's match)
    return None


def pixel_distance(r, s):
    return math.hypot(float(r["pixel_u"]) - float(s["pixel_u"]), float(r["pixel_v"]) - float(s["pixel_v"]))


def match_by_position(ke, ko, tol_px):
    """Pairs (i, j) of points of one kind in one series, closest pairs first, each point used once,
    within tol_px on the page."""
    cand = sorted((pixel_distance(r, s), i, j) for i, r in enumerate(ke) for j, s in enumerate(ko))
    used_i, used_j, pairs = set(), set(), []
    for d, i, j in cand:
        if d > tol_px:
            break
        if i in used_i or j in used_j:
            continue
        used_i.add(i); used_j.add(j); pairs.append((i, j))
    return sorted(pairs)


def leading_role(n):
    """The role named by a note's opening word (--feature-roles leading), or None."""
    m = re.match(r"\s*([a-z]+)", n)
    w = m.group(1) if m else ""
    if w in ("first", "last"):
        return w
    if w in ("peak", "maximum", "crest"):
        return "peak"
    if w in ("knee", "minimum"):
        return "minimum" if "minimum" in re.split(r"[:;]", n, maxsplit=1)[0] else "knee"
    return None


def feature_role(r):
    """first, peak or last, from the reader's note on a feature point (the protocol asks for these three);
    the earliest of the words in the note decides, so "peak: minimum v among the samples" is a peak.
    With --feature-roles leading, the opening word decides first (leading_role)."""
    n = (r.get("note") or "").lower()
    if FEATURE_ROLES == "leading":
        ro = leading_role(n)
        if ro:
            return ro
    hits = [(n.find(w), role) for w, role in (("first", "first"), ("peak", "peak"), ("maximum", "peak"),
                                              ("crest", "peak"), ("last", "last"),
                                              # failure envelopes (from batch curves-appc-b5): where the line meets
                                              # the shear-stress axis, and the printed friction-angle label
                                              ("intercept", "intercept"), ("label", "label"))]
    hits = [h for h in hits if h[0] >= 0]
    return min(hits)[1] if hits else "other"


def median_step_px(rows):
    steps = [pixel_distance(a, b) for a, b in zip(rows, rows[1:])]
    return statistics.median(steps) if steps else 0.0


def median_spacing(rows):
    """The median spacing of a trace's samples in x, in the plotting coordinate (D-027)."""
    fx = calibrate_axes.TRANSFORMS[AXES[0]][0]
    xs = sorted(fx(fl(r, "x_native")) for r in rows)
    gaps = [b - c for b, c in zip(xs[1:], xs)]
    return statistics.median(gaps) if gaps else 0.0


def dkey(r, src):
    return (r["panel"], r["series_id"], r["point_kind"], r["sequence"], src)


def drop_excluded(rows, src, decisions):
    """A reading without its excluded points; the trace sample after an excluded one carries
    `_break_before`, so interpolation never joins its neighbours across it."""
    out, n = [], 0
    groups = defaultdict(list)
    for r in rows:
        groups[(r["panel"], r["series_id"], r["point_kind"])].append(r)
    for g in groups.values():
        g.sort(key=lambda r: int(r["sequence"]))
        brk = False
        for r in g:
            if decisions.get(dkey(r, src), {}).get("status") == "excluded":
                brk, n = True, n + 1
                continue
            if brk and r["point_kind"] == "trace":
                r = dict(r, _break_before="1")
            brk = False
            out.append(r)
    return out, n


def die(msg):
    """An input error: exit 2, never 1, which tells tools/reconcile_curves.py the comparison ran and found disagreements."""
    print(msg, file=sys.stderr)
    sys.exit(2)


def mark_breaks(rows, breaks):
    """The steps of a reading's trace across a documented break in the drawn line (qa/<batch>/breaks.csv, passed as
    --break SERIES X_LO X_HI, the span of the page with no ink) carry `_break_before`, like the step over an excluded
    sample: a break outranks --max-gap, so a sample beside it is compared only with the other reading's samples on its
    own side (Codex's reviews of curves-s5-b1, 2026-11-19). A step that only touches the span at an end is not across
    it. Applied to the other (non-canonical) reading only."""
    if not breaks:
        return rows
    spans = defaultdict(list)
    for sid, lo, hi in breaks:
        lo, hi = float(lo), float(hi)
        if not (math.isfinite(lo) and math.isfinite(hi) and lo < hi):
            die(f"--break {sid} {lo} {hi}: the limits must be finite and increasing")
        if not any(r["series_id"] == sid for r in rows):
            die(f"--break {sid}: no such series in this reading")
        spans[sid].append((lo, hi))
    out, prev = [], {}
    for r in sorted(rows, key=lambda r: (r["panel"], r["series_id"], r["point_kind"], int(r["sequence"]))):
        k = (r["panel"], r["series_id"], r["point_kind"])
        if r["point_kind"] == "trace" and k in prev:
            x0, x1 = fl(prev[k], "x_native"), fl(r, "x_native")
            if any(min(x0, x1) < hi and max(x0, x1) > lo for lo, hi in spans.get(r["series_id"], [])):
                crossed = [(lo, hi) for lo, hi in spans.get(r["series_id"], []) if min(x0, x1) < hi and max(x0, x1) > lo]
                span = f"{min(c[0] for c in crossed)!r} {max(c[1] for c in crossed)!r}"   # all breaks in the step (Codex)
                r = dict(r, _break_before="1", _scan_break=span)
        if r["point_kind"] == "trace":
            prev[k] = r
        out.append(r)
    return out


def piecewise_section(rep, dir_a, dir_b, image, la, lb, box):
    """The D-025 comparison of the two readings' maps (see the module docstring). Appends to the report;
    returns (number of disagreements, whether A is canonical, the reason)."""
    if not image:
        sys.exit("--maps piecewise needs --image")
    gray = np.asarray(Image.open(image).convert("L"), dtype=float)
    cal_a, XA, YA = calibrate_axes.piecewise_maps(dir_a, image)
    cal_b, XB, YB = calibrate_axes.piecewise_maps(dir_b, image)
    rep += ["Maps: piecewise between the verified lines of each reading (D-025); the residuals above are of the "
            "affine fit, a diagnostic of the drafting.", "",
            f"| axis | value | lines apart (px) | {la} from ink, median (px) | {lb} from ink, median (px) | positions | "
            f"{la} line error (px) | {lb} line error (px) | verdict |", "|---|---|---|---|---|---|---|---|---|"]
    n_dis, score = 0, {}
    sets = {}
    for name, KA, KB in (("x", XA, XB), ("y", YA, YB)):
        for lab, K in ((la, KA), (lb, KB)):
            for kn in K.rejected:
                rep.append(f"| {name} | {kn['value']:g} | | | | | | | {lab}'s line not a knot: {kn['reason']} |")
        rows, only_a, only_b = calibrate_axes.compare_knots(KA, KB, gray)
        sets[name] = ({kn["value"] for kn in KA.knots}, {kn["value"] for kn in KB.knots})
        err_a = {kn["value"]: kn["err"] for kn in KA.knots}
        err_b = {kn["value"]: kn["err"] for kn in KB.knots}
        line_a, line_b = [], []
        for r in rows:
            ma = statistics.median(abs(o) for o in r["off_a"]) if r["off_a"] else float("nan")
            mb = statistics.median(abs(o) for o in r["off_b"]) if r["off_b"] else float("nan")
            if r["off_a"] and r["off_b"]:
                line_a.append(ma)
                line_b.append(mb)
            ok = r["gap_px"] <= err_a[r["value"]] + err_b[r["value"]]
            n_dis += not ok
            verdict = "agree" if ok else "**disagree**"
            verdict += "".join(f"; {lab} off the ink" for lab, m in ((la, ma), (lb, mb)) if m > OFF_INK_PX)
            rep.append(f"| {name} | {r['value']:g} | {r['gap_px']:.2f} | {ma:.2f} | {mb:.2f} | {r['n']} | "
                       f"{err_a[r['value']]:.2f} | {err_b[r['value']]:.2f} | {verdict} |")
        for v in only_a:
            rep.append(f"| {name} | {v:g} | | | | | {err_a[v]:.2f} | | only in {la} |")
        for v in only_b:
            rep.append(f"| {name} | {v:g} | | | | | | {err_b[v]:.2f} | only in {lb} |")
        score[name] = (line_a, line_b)
    rep.append("")

    # both maps along every verified line of either reading and along the midline of every interval between
    # adjacent lines (Codex's review, 2026-10-14: a 9 x 9 grid is not a comparison at every knot), at 7
    # positions across the box; tolerance: the two maps' bracketing line errors there
    u0, v0, u1, v1 = box
    corners = np.array([[u0, v0], [u1, v0], [u0, v1], [u1, v1]], dtype=float)
    n_eval = n_out = 0
    worst = {}
    for name, KA, KB in (("x", XA, XB), ("y", YA, YB)):
        tmin, tmax = float((corners @ KA.e_t).min()), float((corners @ KA.e_t).max())
        lines = []   # (label, s(t) in A's frame)
        for K, lab in ((KA, la), (KB, lb)):
            for kn in K.knots:
                lines.append((f"{lab} {kn['value']:g}", K, kn))
        worst[name] = (0.0, 0.0, "")
        for t in np.linspace(tmin, tmax, 7):
            pts = []
            for lab, K, kn in lines:
                tk = float((t * KA.e_t + (corners.mean(axis=0) @ KA.e_s) * KA.e_s) @ K.e_t)
                q = K.line_s(kn, tk) * K.e_s + tk * K.e_t
                pts.append((float(q @ KA.e_s), lab, q))
            pts.sort(key=lambda x: x[0])
            mids = [((p1[0] + p2[0]) / 2, f"between {p1[1]} and {p2[1]}", (p1[2] + p2[2]) / 2) for p1, p2 in zip(pts, pts[1:])]
            for _, lab, q in pts + mids:
                if not (u0 - 2 <= q[0] <= u1 + 2 and v0 - 2 <= q[1] <= v1 + 2):
                    continue
                va, _, ea, _ = KA.value_q(*q)   # in the plotting coordinate (the printed value on a linear axis)
                vb, _, eb, _ = KB.value_q(*q)
                d = abs(va - vb)
                n_eval += 1
                n_out += d > ea + eb
                if d > worst[name][0]:
                    worst[name] = (d, ea + eb, lab)
    rep.append(("" if AXES == ("linear", "linear") else f"(In the plotting coordinates: {AXES[0]} x, {AXES[1]} y.) ") +
               f"Both maps along every verified line and every interval midline ({n_eval} places): largest difference "
               f"{worst['x'][0]:.4g} in x (tolerance {worst['x'][1]:.4g}, {worst['x'][2]}), {worst['y'][0]:.4g} in y "
               f"(tolerance {worst['y'][1]:.4g}, {worst['y'][2]}); {n_out} beyond the two maps' line errors.")
    rep.append("")

    # canonical: equal coverage, then the lines' distance from the ink; a strict superset of lines wins only
    # when the shared lines are as close to the ink; coverage that differs both ways needs review
    def mean(x):
        return statistics.mean(x) if x else float("inf")
    sc_a = {n: mean(score[n][0]) for n in score}
    sc_b = {n: mean(score[n][1]) for n in score}
    line_a = score["x"][0] + score["y"][0]
    line_b = score["x"][1] + score["y"][1]
    ta, tb = mean(line_a), mean(line_b)
    what = (f"{len(line_a)} shared lines checked against the ink, mean of the median distances {ta:.2f} px ({la}: "
            f"x {sc_a['x']:.2f}, y {sc_a['y']:.2f}), {tb:.2f} px ({lb}: x {sc_b['x']:.2f}, y {sc_b['y']:.2f})")
    a_sup = all(sets[n][0] >= sets[n][1] for n in sets)
    b_sup = all(sets[n][1] >= sets[n][0] for n in sets)
    review = 0
    if a_sup and b_sup:   # the same lines
        if not line_a or abs(ta - tb) <= VALIDATION_TIE_PX:
            use_a, why = True, f"same lines; {what}, within {VALIDATION_TIE_PX} px of each other, so the first submission"
        else:
            use_a, why = ta < tb, f"same lines; {what}"
    elif a_sup and ta <= tb + VALIDATION_TIE_PX:
        use_a, why = True, f"{la}'s lines include all of {lb}'s and more, as close to the ink; {what}"
    elif b_sup and tb <= ta + VALIDATION_TIE_PX:
        use_a, why = False, f"{lb}'s lines include all of {la}'s and more, as close to the ink; {what}"
    else:
        review = 1
        use_a = not line_a or ta <= tb + VALIDATION_TIE_PX
        why = (f"**coverage cannot be ranked** (lines {la}: x {sorted(sets['x'][0])}, y {sorted(sets['y'][0])}; {lb}: "
               f"x {sorted(sets['x'][1])}, y {sorted(sets['y'][1])}): recover the missing lines or name the canonical "
               f"reading in overlays.csv; meanwhile {'first submission' if use_a else lb} by the ink; {what}")
    return n_dis + (n_out > 0) + review, use_a, why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--cal-a", required=True)
    ap.add_argument("--cal-b", required=True)
    ap.add_argument("--labels", default="A,B")
    ap.add_argument("--panel")
    ap.add_argument("--match-px", type=float, help="pairing radius on the page for markers and features (pixels)")
    ap.add_argument("--canonical-from", help="name the canonical reading (one of --labels) instead of the residual rule")
    ap.add_argument("--canonical-reason", help="why, for the report")
    ap.add_argument("--out")
    ap.add_argument("--canonical")
    ap.add_argument("--decisions")
    ap.add_argument("--ink-checks", help="a batch's ink-checks.csv (tools/check_trace_ink.py, D-031): its excluded trace "
                    "samples are excluded like hand decisions, and override a hand decision that kept them")
    ap.add_argument("--maps", choices=["affine", "piecewise"], default="affine",
                    help="piecewise: compare the readings' maps line by line and choose the canonical reading by the ink (D-025)")
    ap.add_argument("--image", help="the page image (needed with --maps piecewise)")
    ap.add_argument("--break", dest="breaks", nargs=3, action="append", default=[], metavar=("SERIES", "X_LO", "X_HI"),
                    help="a documented break in a series' drawn line, from x X_LO to X_HI (native units): no trace step "
                         "across it is interpolated (tools/reconcile_curves.py passes qa/<batch>/breaks.csv)")
    for lab in ("a", "b"):
        ap.add_argument(f"--break-{lab}", dest=f"breaks_{lab}", nargs=3, action="append", default=[],
                        metavar=("SERIES", "X_LO", "X_HI"),
                        help=f"as --break, for reading {lab.upper()} only: the break's span on that reading's own map")
    ap.add_argument("--max-gap", type=float, help="a trace step wider than this (x, in its plotting coordinate) is a drawn "
                    "gap; default three times the reading's median sample spacing")
    ap.add_argument("--end-dedup", action="store_true", help="do not append the other reading's sample at the canonical end "
                    "of a trace when it is the same point within both readings' bounds")
    ap.add_argument("--feature-roles", choices=["earliest", "leading"], default="earliest",
                    help="how a feature's role is read from its note (see the module docstring)")
    ap.add_argument("--bound-scale", type=float, default=1.0,
                    help="multiply every reading bound before comparing (sensitivity check of the agreement rule; report only)")
    a = ap.parse_args()
    if a.max_gap is not None and not (math.isfinite(a.max_gap) and a.max_gap > 0):   # 0, -1 or nan changed the comparison silently
        ap.error(f"--max-gap must be a positive number, not {a.max_gap}")
    global BOUND_SCALE, FEATURE_ROLES
    BOUND_SCALE = a.bound_scale
    FEATURE_ROLES = a.feature_roles
    la, lb = a.labels.split(",")
    A, B = load(a.a), load(a.b)
    if a.panel:
        A = [r for r in A if r["panel"] == a.panel]
        B = [r for r in B if r["panel"] == a.panel]
    cal_a, cal_b = json.loads(Path(a.cal_a).read_text()), json.loads(Path(a.cal_b).read_text())
    global AXES
    AXES = calibrate_axes.axis_transforms(cal_a)
    if calibrate_axes.axis_transforms(cal_b) != AXES:
        sys.exit(f"the readings declare different axis transforms ({AXES}, {calibrate_axes.axis_transforms(cal_b)}): "
                 "settle the axis type from the page before comparing (D-027)")
    rep = [f"# Curve diff: {la} vs {lb}", "", f"Files: `{a.a}` ({la}), `{a.b}` ({lb}).", ""]
    if BOUND_SCALE != 1.0:
        rep += [f"Sensitivity run: every reading bound multiplied by {BOUND_SCALE} before comparing.", ""]

    # calibration: the same pixels (A's box corners) through both maps
    rep += ["## Calibration", "", f"| | {la} | {lb} |", "|---|---|---|",
            f"| anchors | {cal_a['n_anchors']} | {cal_b['n_anchors']} |",
            f"| x per px | {cal_a['x_per_px']:.4f} | {cal_b['x_per_px']:.4f} |",
            f"| y per px | {cal_a['y_per_px']:.4f} | {cal_b['y_per_px']:.4f} |",
            f"| RMS residual x, y | {cal_a['rms_residual_x']:.3f}, {cal_a['rms_residual_y']:.3f} | {cal_b['rms_residual_x']:.3f}, {cal_b['rms_residual_y']:.3f} |", ""]
    # the corners of a box both maps are evaluated at; a calibration made by hand from tick marks may
    # record none (Fig. C-2A, batch curves-appc-b5), and then the other reading's box serves
    box = cal_a.get("box") or cal_b.get("box")
    cal_a.setdefault("box", box)
    ca, cb = corners(cal_a, box), corners(cal_b, box)
    # residuals and scales are in the plotting coordinates, so the corners are compared there (D-027)
    qa_, qb_ = corners(cal_a, box, apply_q), corners(cal_b, box, apply_q)
    tol_x = cal_a["rms_residual_x"] + cal_b["rms_residual_x"] + max(cal_a["x_per_px"], cal_b["x_per_px"])
    tol_y = cal_a["rms_residual_y"] + cal_b["rms_residual_y"] + max(cal_a["y_per_px"], cal_b["y_per_px"])
    unit = "" if AXES == ("linear", "linear") else f" (in the plotting coordinates of {AXES[0]} x, {AXES[1]} y)"
    rep.append(f"Corners of {la}'s box {cal_a['box']} mapped by both calibrations (tolerance {tol_x:.2f} in x, {tol_y:.2f} in y{unit}):")
    rep.append("")
    cal_dis = 0
    for (xa, ya), (xb, yb), (qxa, qya), (qxb, qyb) in zip(ca, cb, qa_, qb_):
        flag = "" if abs(qxa - qxb) <= tol_x and abs(qya - qyb) <= tol_y else "  **disagree**"
        cal_dis += bool(flag)
        rep.append(f"- ({xa:.1f}, {ya:.1f}) vs ({xb:.1f}, {yb:.1f}){flag}")
    rep.append("")

    if a.maps == "piecewise":
        cal_dis, use_a, why = piecewise_section(rep, Path(a.cal_a).parent, Path(a.cal_b).parent, a.image, la, lb, box)

    # canonical (evaluating) reading
    span_x = max(abs(c[0] - qa_[0][0]) for c in qa_) or 1
    span_y = max(abs(c[1] - qa_[0][1]) for c in qa_) or 1
    score_a = cal_a["rms_residual_x"] / span_x + cal_a["rms_residual_y"] / span_y
    score_b = cal_b["rms_residual_x"] / span_x + cal_b["rms_residual_y"] / span_y
    if a.maps != "piecewise":
        use_a = score_a <= score_b
    # A residual measured on lines the tool predicted from the frame shows internal consistency only;
    # it cannot compete with one measured against printed marks (D-024, with Codex; Figs. C-3A and
    # C-4A have ticks but no grid). A batch then names the canonical reading with its reason.
    if a.maps != "piecewise":
        why = f"calibration score {min(score_a, score_b):.5f} vs {max(score_a, score_b):.5f}"
    if a.canonical_from:
        use_a = a.canonical_from == la
        why = f"named by the batch: {a.canonical_reason or 'see the batch review'}; " + (
            why if a.maps == "piecewise" else f"calibration scores {score_a:.5f} ({la}), {score_b:.5f} ({lb})")
    le, lo = (la, lb) if use_a else (lb, la)
    # decisions are read before the comparison: a point excluded on the page is not a reading of ink and
    # supports nothing, so it is removed from its reading before matching and interpolation, and a trace
    # keeps a break where it was (its neighbours are not joined across it). Until 2026-10-14 exclusions
    # only dropped output rows, and 75 agreed trace samples had been compared against a stretch of the
    # other trace that included an excluded sample (Codex's review of D-025).
    decisions = {}
    if a.decisions:
        for d in load(a.decisions):
            decisions[(d["panel"], d["series_id"], d["point_kind"], d["sequence"], d.get("source") or le)] = d
    # D-031: trace samples the ink check shows off their line's own ink are excluded like a hand exclusion. A
    # hand decision cannot keep such a sample (Codex's design): the ink check measures the page, while the hand
    # decisions it overrides were made before the rule existed (the pilot's n2345 group was one, 2026-10-27);
    # every override is listed in the report for review.
    ink_excluded, ink_conflicts = 0, []
    if a.ink_checks:
        fids = {r["figure_id"] for r in (A or B)}
        for r in load(a.ink_checks):
            if r["figure_id"] not in fids or r["panel"] != a.panel or r["verdict"] != "excluded":
                continue
            k = (r["panel"], r["series_id"], r["point_kind"], r["sequence"], r["reader"])
            hand = decisions.get(k)
            if hand and hand.get("status") == "excluded":
                continue
            note = f"D-031 ink check: {r['reason']}"
            if hand:
                ink_conflicts.append(f"{r['reader']} {r['series_id']} {r['point_kind']} {r['sequence']}: hand decision "
                                     f"{hand.get('status')}{(' use ' + hand['use']) if hand.get('use') else ''} ({(hand.get('note') or '')[:100]})")
                note += f"; overrides a hand decision ({hand.get('status')}{(' use ' + hand['use']) if hand.get('use') else ''})"
            decisions[k] = {"panel": r["panel"], "series_id": r["series_id"], "point_kind": r["point_kind"],
                            "sequence": r["sequence"], "source": r["reader"], "status": "excluded", "use": "", "note": note}
            ink_excluded += 1
    out_cols = list((A or B)[0].keys())
    A, n_ex_a = drop_excluded(A, la, decisions)
    B, n_ex_b = drop_excluded(B, lb, decisions)
    E, O = (A, B) if use_a else (B, A)           # evaluating (canonical) and other
    # a documented break: the other reading is not interpolated across it; the canonical reading's own step over it
    # is left alone, so the other reading's samples beside the break are not added as points of their own
    O = mark_breaks(O, a.breaks + (a.breaks_b if use_a else a.breaks_a))   # each reading's own span on its own map
    rep.append(f"Canonical reading: {le} ({why}); points are evaluated at {le}'s samples.")
    rep.append("")

    # series
    SE, SO = defaultdict(list), defaultdict(list)
    for r in E:
        SE[key(r)].append(r)
    for r in O:
        SO[key(r)].append(r)
    only_e, only_o = sorted(set(SE) - set(SO)), sorted(set(SO) - set(SE))
    rep += ["## Series", "", f"{len(SE)} series in {le}, {len(SO)} in {lo}."]
    if only_e:
        rep.append(f"Only in {le}: {', '.join('/'.join(k) for k in only_e)}")
    if only_o:
        rep.append(f"Only in {lo}: {', '.join('/'.join(k) for k in only_o)}")
    for k in sorted(set(SE) & set(SO)):
        se = {r.get("symbol", "") for r in SE[k] if r["point_kind"] == "marker" and r.get("symbol")}
        so = {r.get("symbol", "") for r in SO[k] if r["point_kind"] == "marker" and r.get("symbol")}
        if se and so and se != so:
            rep.append(f"- marker symbol disagreement in {'/'.join(k)}: {le} {sorted(se)}, {lo} {sorted(so)}")
    rep.append("")

    agreed = disagreed = unmatched = 0
    canon_rows = []   # (key, row, other dict or None, status, source label, rule note)
    hdr = f"| series | kind | seq ({le}/{lo}) | {le} x, y (bounds) | {lo} x, y (bounds) | dx | dy | verdict |"
    rows_tbl = [hdr, "|---|---|---|---|---|---|---|---|"]
    for k in sorted(set(SE) | set(SO)):
        pe, po = SE.get(k, []), SO.get(k, [])
        for kind in sorted({r["point_kind"] for r in pe} | {r["point_kind"] for r in po}):
            ke = sorted([r for r in pe if r["point_kind"] == kind], key=lambda r: int(r["sequence"]))
            ko = sorted([r for r in po if r["point_kind"] == kind], key=lambda r: int(r["sequence"]))
            if kind == "trace" and ke and ko:
                # a drawn gap: a step wider than three times the reading's median sample spacing, or the batch's
                # own threshold (--max-gap, in the plotting coordinate of x): a history sampled at several spacings
                # by rule (0.5 ms on a pulse, 2 ms after it) has a median far below its ordinary steps (2026-11-19)
                max_gap = a.max_gap if a.max_gap is not None else 3 * (median_spacing(ko) or float("inf"))
                # samples of the other reading beyond either end of the evaluating trace are kept as its
                # own one-sided points (a curve start or end only one reader sampled), in drawing order
                xs_e = [fl(r, "x_native") for r in ke]
                # with --end-dedup, a sample of the other reading just beyond the canonical end, within the two readings'
                # bounds of that end in x and y, is the same point as the end, which it already supports: not appended as
                # a point of its own (Codex's review, 2026-11-19: a duplicate 1.1 microseconds from the end of a DPT record).
                # Opt-in per figure: applied to the earlier batches it would remove 193 such end points (159
                # one-sided-verified, 34 one-sided), a decision left to Dan (docs/OPEN-QUESTIONS.md)
                end_lo, end_hi = min(ke, key=lambda r: fl(r, "x_native")), max(ke, key=lambda r: fl(r, "x_native"))
                same = lambda s, e: (a.end_dedup and abs(fl(s, "x_native") - fl(e, "x_native")) <= fl(s, "x_read_bound") + fl(e, "x_read_bound")
                                     and abs(fl(s, "y_native") - fl(e, "y_native")) <= fl(s, "y_read_bound") + fl(e, "y_read_bound"))
                head = [s for s in ko if fl(s, "x_native") < min(xs_e) and not same(s, end_lo)]
                tail = [s for s in ko if fl(s, "x_native") > max(xs_e) and not same(s, end_hi)]
                # and inside the canonical trace's range where it has no support (a drawn gap, a break left by
                # an excluded sample): kept as one-sided, placed in the gap they fill (Codex's review, 2026-10-14)
                max_gap_e = a.max_gap if a.max_gap is not None else 3 * (median_spacing(ke) or float("inf"))
                inner = defaultdict(list)
                for s in ko:
                    xs = fl(s, "x_native")
                    if min(xs_e) <= xs <= max(xs_e) and interp_trace(ke, xs, max_gap_e) is None:
                        j = next((j for j in range(len(ke) - 1)
                                  if min(xs_e[j], xs_e[j + 1]) <= xs <= max(xs_e[j], xs_e[j + 1])), len(ke) - 1)
                        inner[j].append(s)
                for s in head:
                    unmatched += 1
                    canon_rows.append((k, s, None, "one-sided", lo, ""))
                for i, r in enumerate(ke):
                    for s in inner.get(i - 1, []):   # the other reading's samples filling the gap before this one
                        unmatched += 1
                        canon_rows.append((k, s, None, "one-sided", lo, ""))
                    xe, ye, bxe, bye = (fl(r, "x_native"), fl(r, "y_native"), fl(r, "x_read_bound"), fl(r, "y_read_bound"))
                    it = interp_trace(ko, xe, max_gap, reach=bxe)
                    if it is None:
                        unmatched += 1
                        canon_rows.append((k, r, None, "one-sided", le, ""))
                        rows_tbl.append(f"| {k[2]} | trace | {r['sequence']}/- | {xe:.1f}, {ye:.1f} ({bxe:.1f}, {bye:.1f}) | (no trace at this x) | | | unmatched in {lo} |")
                        continue
                    yi, bxo, byo, slope, puo, pvo, xo = it
                    tol = bye + byo + abs(slope) * (bxe + bxo)
                    ok = abs(ye - yi) <= tol
                    agreed += ok; disagreed += (not ok)
                    other = {"x_native": fmt_value(xo), "y_native": fmt_value(yi), "x_read_bound": fmt_value(bxo), "y_read_bound": fmt_value(byo),
                             "pixel_u": f"{puo:.1f}", "pixel_v": f"{pvo:.1f}"}
                    if not ok:
                        rows_tbl.append(f"| {k[2]} | trace | {r['sequence']}/interp | {xe:.1f}, {ye:.1f} ({bxe:.1f}, {bye:.1f}) | {xe:.1f}, {yi:.1f} ({bxo:.1f}, {byo:.1f}) | slope {slope:+.1f} | {ye - yi:+.1f} (tol {tol:.1f}) | **disagree** |")
                    canon_rows.append((k, r, other, "agreed" if ok else "pending-review", le, ""))
                for s in inner.get(len(ke) - 1, []) + tail:
                    unmatched += 1
                    canon_rows.append((k, s, None, "one-sided", lo, ""))
                # the other reading's samples inside the evaluating trace's range are not observations of their own
                continue
            # markers, features, gridline points (and a trace only one reading has): pair by position on the
            # page; features first by role (first, peak, last), so a peak is never paired with a first point
            groups = [(ke, ko)]
            first_row = len(canon_rows)
            if kind == "feature":
                # knees and minima pair in one group
                group_of = ((lambda r: "knee" if feature_role(r) == "minimum" else feature_role(r))
                            if FEATURE_ROLES == "leading" else feature_role)
                roles = sorted({group_of(r) for r in ke} | {group_of(s) for s in ko})
                groups = [([r for r in ke if group_of(r) == ro], [s for s in ko if group_of(s) == ro]) for ro in roles]
            for ge, go in groups:
                tol = a.match_px or max(12.0, median_step_px(ge) / 2 if len(ge) > 1 else float("inf"))
                if kind == "feature":
                    tol = float("inf")  # one first, one peak, one last per series: their role pairs them
                    if FEATURE_ROLES == "leading" and max(len(ge), len(go)) > 1:
                        tol = FEATURE_PX   # several of one role in a series: the role alone does not pair them
                ij = match_by_position(ge, go, tol)
                mi, mj = {i for i, _ in ij}, {j for _, j in ij}
                for i, r in enumerate(ge):
                    if i not in mi:
                        unmatched += 1
                        canon_rows.append((k, r, None, "one-sided", le, ""))
                        rows_tbl.append(f"| {k[2]} | {kind} | {r['sequence']}/- | {fl(r, 'x_native'):.1f}, {fl(r, 'y_native'):.1f} | (none) | | | unmatched in {lo} |")
                for i, j in ij:
                    r, s = ge[i], go[j]
                    xe, ye, xo, yo = (fl(r, "x_native"), fl(r, "y_native"), fl(s, "x_native"), fl(s, "y_native"))
                    bxe, bye, bxo, byo = (fl(r, "x_read_bound"), fl(r, "y_read_bound"), fl(s, "x_read_bound"), fl(s, "y_read_bound"))
                    rule = ""
                    if kind == "feature" and feature_role(r) == "label":
                        # a printed label is text: the readings agree when they read the same number (an envelope's
                        # angle) or, for a label without one, the same first word (a soil name on Fig. C-23, from
                        # 2026-10-15); its position only shows which line it belongs to and is not compared
                        def num(x):
                            t = (x.get("note") or "").split("label", 1)[-1]
                            return re.findall(r"\d+(?:\.\d+)?", t)[:1] or [w.upper() for w in re.findall(r"[A-Za-z][A-Za-z0-9-]*", t)[:1]]
                        ok = bool(num(r)) and num(r) == num(s)
                    elif kind == "feature" and (feature_role(r) == "peak" or
                                                (FEATURE_ROLES == "leading" and feature_role(r) == feature_role(s) == "minimum")):
                        # the height of a peak is the observation; on a flat top its x is not, so x is not compared
                        # and the canonical x bound is widened to take in the other reading's x interval
                        ok = abs(ye - yo) <= bye + byo
                        if ok and abs(xe - xo) > bxe + bxo:
                            rule = (f"rule: peak compared in y only; x bound widened from {bxe:.3f} to cover the "
                                    f"other reading's x {xo:.3f} +- {bxo:.3f}")
                    else:
                        ok = abs(xe - xo) <= bxe + bxo and abs(ye - yo) <= bye + byo
                    agreed += ok; disagreed += (not ok)
                    if not ok:
                        rows_tbl.append(f"| {k[2]} | {kind} | {r['sequence']}/{s['sequence']} | {xe:.1f}, {ye:.1f} ({bxe:.1f}, {bye:.1f}) | {xo:.1f}, {yo:.1f} ({bxo:.1f}, {byo:.1f}) | {xe - xo:+.1f} | {ye - yo:+.1f} | **disagree** |")
                    canon_rows.append((k, r, s, "agreed" if ok else "pending-review", le, rule))
                # points only the other reading holds are kept as its own one-sided points (a marker the
                # canonical reader missed is still an observation; the smaller residual does not make a reading complete)
                for j, s in enumerate(go):
                    if j not in mj:
                        unmatched += 1
                        canon_rows.append((k, s, None, "one-sided", lo, ""))
                        rows_tbl.append(f"| {k[2]} | {kind} | -/{s['sequence']} | (none) | {fl(s, 'x_native'):.1f}, {fl(s, 'y_native'):.1f} | | | unmatched in {le} |")
            # within the kind: the canonical reading's points in its own order, then the other reading's
            canon_rows[first_row:] = sorted(canon_rows[first_row:], key=lambda c: (c[4] != le, int(c[1]["sequence"])))
    # one symbol filed under two tests: a one-sided marker of one reading that sits on a marker the other
    # reading assigned to another series is an identity conflict, not two observations (Codex's check,
    # 2026-10-13: the stacked symbols of FC-2C's lower panel); it goes to review with both identities named
    marks = {la: [r for r in A if r["point_kind"] == "marker"], lb: [r for r in B if r["point_kind"] == "marker"]}
    for n, (k, r, other, status, src, rule) in enumerate(canon_rows):
        if status != "one-sided" or r["point_kind"] != "marker":
            continue
        rival = lb if src == la else la
        hit = [s for s in marks[rival] if s["series_id"] != r["series_id"] and pixel_distance(r, s) <= 10]
        if hit:
            names = ", ".join(f"{s['series_id']} ({s.get('symbol', '')})" for s in hit)
            canon_rows[n] = (k, r, other, "pending-review", src, f"rule: identity conflict; {rival} recorded this symbol as {names}")
            rows_tbl.append(f"| {k[2]} | marker | {r['sequence']} ({src}) | {fl(r, 'x_native'):.1f}, {fl(r, 'y_native'):.1f} | {rival}: {names} | | | **identity conflict** |")
    n_own = sum(1 for c in canon_rows if c[3] == "one-sided" and c[4] == le)
    n_kept = sum(1 for c in canon_rows if c[3] == "one-sided" and c[4] == lo)
    rep += ["", "## Points", "", f"Matched: {agreed + disagreed}; agreed {agreed}; disagreed {disagreed}; unmatched {unmatched} "
            f"(kept as one-sided: {n_own} of {le}, {n_kept} of {lo}).", ""]
    rep += rows_tbl if len(rows_tbl) > 2 else ["No point disagreements."]
    if a.ink_checks:
        rep += ["", f"## Ink check (D-031): {ink_excluded} trace samples excluded", ""]
        rep += ([f"Overrides of hand decisions ({len(ink_conflicts)}), for review:", ""] + [f"- {c}" for c in ink_conflicts]
                if ink_conflicts else ["No hand decision overridden."])
    text = "\n".join(rep) + "\n"
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8", newline="\n")
    else:
        print(text)

    if a.canonical:
        # a decision names its point by (panel, series, kind, sequence) and, since points of both readings
        # can be in the output, by `source` (the reading whose numbering `sequence` is); a decision without a
        # source column means the canonical reading (decision files written before 2026-10-13)
        # other_pixel_u/v: where the other reading lies on the page (its own point, or the pixel interpolated along
        # its own samples by interp_trace, end rule included), so that an audit packet draws it there instead of
        # mapping its value through a fit to the canonical reading (the deferred D-027 item, closed for wave 6 on
        # Codex's review of 2026-11-18; appended last so that every earlier column keeps its place)
        cols = [c for c in out_cols if c != "_break_before"] + ["status", "source", "other_x_native", "other_y_native",
                                                                 "decision_note", "other_pixel_u", "other_pixel_v"]
        n_written = 0
        counts = defaultdict(int, {"excluded": n_ex_a + n_ex_b})
        with Path(a.canonical).open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
            w.writeheader()
            for k, r, other, status, src, rule in canon_rows:
                row = dict(r)
                row.update({"status": status, "source": src, "decision_note": rule,
                            "other_x_native": other["x_native"] if other else "",
                            "other_y_native": other["y_native"] if other else "",
                            "other_pixel_u": other["pixel_u"] if other else "",
                            "other_pixel_v": other["pixel_v"] if other else ""})
                if rule.startswith("rule: peak") and other:
                    row["x_read_bound"] = fmt_value(max(fl(r, 'x_read_bound'), abs(fl(r, 'x_native') - fl(other, 'x_native')) + fl(other, 'x_read_bound')))
                d = decisions.get(dkey(row, src))
                carried = ""
                if not d and other is not None and "sequence" in other and src == le:
                    # a decision made on the paired point of the other reading, when that reading was canonical,
                    # follows the physical symbol or feature it was made on: the pair is the correspondence
                    # (Codex's review of D-025, 2026-10-14); only a resolution carries, a verification does not
                    d0 = decisions.get(dkey(other, lo))
                    if d0 and d0["status"] == "resolved":
                        keep_other = d0.get("use") in ("", None, lo)   # it kept the value of the reading it was made on
                        d = dict(d0, use=lo if keep_other else le)
                        carried = f"decision made on {lo} {other['sequence']}, carried to its pair {le} {r['sequence']}"
                if d:
                    row["status"] = d["status"]
                    row["decision_note"] = "; ".join(x for x in (rule, carried, d.get("note", "")) if x)
                    if d.get("use") and d["use"] == lo and other:
                        if "sequence" in other:
                            # a submitted point of the other reading: its whole record (sequence, pixels, bounds,
                            # symbol, note), so `source` and `sequence` name the point the values come from
                            # (until 2026-10-14 the row kept the evaluating reading's sequence and bounds)
                            note = row["decision_note"]
                            row = dict(other)
                            row.update({"status": d["status"], "source": lo, "decision_note": note,
                                        "other_x_native": r["x_native"], "other_y_native": r["y_native"],
                                        "other_pixel_u": r["pixel_u"], "other_pixel_v": r["pixel_v"]})
                        else:
                            # a value interpolated on the other reading's trace at this sample's displacement: no
                            # submitted point holds it, so its source says so and `sequence` stays that of the
                            # canonical sample whose displacement it was taken at
                            row.update({"x_native": other["x_native"], "y_native": other["y_native"],
                                        "x_read_bound": other["x_read_bound"], "y_read_bound": other["y_read_bound"],
                                        "pixel_u": other["pixel_u"], "pixel_v": other["pixel_v"],
                                        "source": f"{lo}-interp",
                                        "other_x_native": r["x_native"], "other_y_native": r["y_native"],
                                        "other_pixel_u": r["pixel_u"], "other_pixel_v": r["pixel_v"]})
                    elif d.get("use") == "span":
                        # neither reading could be shown right on the page (audit re-check, 2026-10-27): keep this
                        # reading's value and widen its bounds to take in the other reading's value and bound, so
                        # the record carries the real uncertainty instead of a choice nobody could make
                        if other:
                            for ax in ("x", "y"):
                                own = fl(row, f"{ax}_read_bound")
                                reach = abs(fl(row, f"{ax}_native") - fl(other, f"{ax}_native")) + fl(other, f"{ax}_read_bound")
                                row[f"{ax}_read_bound"] = fmt_outward(max(own, reach))
                            row["decision_note"] += "; bounds widened to cover the other reading (use span)"
                        else:
                            row["decision_note"] += "; use span asked but no other reading here, bounds unchanged"
                counts[row["status"]] += 1
                w.writerow(row); n_written += 1
        print(f"canonical: {le}; {n_written} points written to {a.canonical}: " + ", ".join(f"{s} {n}" for s, n in sorted(counts.items())))
    return 1 if (disagreed or unmatched or cal_dis or only_e or only_o) else 0


if __name__ == "__main__":
    sys.exit(main())
