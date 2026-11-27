"""Snap trace samples of F2-44 to the ink (Claude reader, batch curves-s2-b3).

For each trace a guide polyline is read by eye from zoomed crops (pixel coordinates of p0104.png).
Sampling locations: every 0.25 in of penetration, and on the steep initial rise every 100 lb of
load. At each location the guide gives an approximate pixel position; the sample is moved onto
the ink of the line: the centre of the dark run crossing the guide, in the pixel column (shallow
stretches) or the pixel row (steep stretches), chosen by `pick`:
  nearest  the run whose centre is nearest the guide
  left     left edge of the run plus half the line's width (a line overlapped on its right)
  right    right edge of the run minus half the line's width (a line overlapped on its left)
  top      top edge plus half width (column mode; a line overlapped below)
  bottom   bottom edge minus half width (column mode; a line overlapped above)
  guide    no snapping: the guide point itself (for samples set by hand, with a note)
On a dashed or dotted line a location that falls in a gap is moved along the guide to the
nearest ink (never sampled in the gap). The line width is measured on the run and converted to
a width across the line with the guide's local angle.
This script only proposes; samples.json (written by hand from its output and the crops) is final.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
WS = HERE.parents[1]
g = np.asarray(Image.open(WS / "packet" / "p0104.png").convert("L"))
cal = json.loads((HERE / "cal-p1" / "calibration.json").read_text(encoding="utf-8"))
AX, AY = cal["ax"], cal["ay"]
DARK = 160


def xy(u, v):
    return AX[0] * u + AX[1] * v + AX[2], AY[0] * u + AY[1] * v + AY[2]


def runs(arr, off):
    idx = np.where(arr)[0]
    out = []
    if len(idx) == 0:
        return out
    s = p = int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i != p + 1:
            out.append((s + off, p + off)); s = i
        p = i
    out.append((s + off, p + off))
    return out


def col_runs(u, v0, v1):
    return runs(g[v0:v1 + 1, u] < DARK, v0)


def row_runs(v, u0, u1):
    return runs(g[v, u0:u1 + 1] < DARK, u0)


def locate_on_guide(guide, target, which):
    """Points on the polyline where x (which='x') or y (which='y') equals target: list of
    (arc parameter, u, v, slope dv/du, angle from horizontal in rad)."""
    out = []
    arc = 0.0
    for (u0, v0), (u1, v1) in zip(guide, guide[1:]):
        a0 = xy(u0, v0)[0 if which == "x" else 1]
        a1 = xy(u1, v1)[0 if which == "x" else 1]
        seg = math.hypot(u1 - u0, v1 - v0)
        if (a0 - target) * (a1 - target) <= 0 and a0 != a1:
            f = (target - a0) / (a1 - a0)
            if 0 <= f < 1 or (f == 1 and (u1, v1) == tuple(guide[-1])):
                ang = math.atan2(abs(v1 - v0), abs(u1 - u0) + 1e-9)
                out.append((arc + f * seg, u0 + f * (u1 - u0), v0 + f * (v1 - v0), ang))
        arc += seg
    return out


def point_at_arc(guide, s):
    arc = 0.0
    for (u0, v0), (u1, v1) in zip(guide, guide[1:]):
        seg = math.hypot(u1 - u0, v1 - v0)
        if arc + seg >= s:
            f = (s - arc) / seg if seg else 0
            return u0 + f * (u1 - u0), v0 + f * (v1 - v0), math.atan2(abs(v1 - v0), abs(u1 - u0) + 1e-9)
        arc += seg
    (u0, v0), (u1, v1) = guide[-2], guide[-1]
    return u1, v1, math.atan2(abs(v1 - v0), abs(u1 - u0) + 1e-9)


VL = [(l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
HL = [(l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
GRID_CLEAR = 6   # a sample is not read in a pixel column or row within this distance of a grid line


def guide_at(guide, coord, val, s_near):
    """Point of the guide where u (coord 0) or v (coord 1) equals val, nearest to arc s_near."""
    best, arc = None, 0.0
    for (u0, v0), (u1, v1) in zip(guide, guide[1:]):
        a, b = (u0, u1) if coord == 0 else (v0, v1)
        seg = math.hypot(u1 - u0, v1 - v0)
        if (a - val) * (b - val) <= 0 and a != b:
            f = (val - a) / (b - a)
            s = arc + f * seg
            cand = (abs(s - s_near), s, u0 + f * (u1 - u0), v0 + f * (v1 - v0), math.atan2(abs(v1 - v0), abs(u1 - u0) + 1e-9))
            if best is None or cand[0] < best[0]:
                best = cand
        arc += seg
    return best[1:] if best else None


def clear_of_grid(guide, s, ug, vg, ang):
    """Move a sampling location off a grid line, along the guide (the location is a sampling choice)."""
    steep = ang > math.radians(55)
    for _ in range(2):
        if steep:
            for v0, k in HL:
                gv = v0 + k * ug
                if abs(vg - gv) < GRID_CLEAR:
                    nv = gv + (GRID_CLEAR if vg >= gv else -GRID_CLEAR)
                    r = guide_at(guide, 1, nv, s)
                    if r:
                        s, ug, vg, ang = r
        else:
            for u0, k in VL:
                gu = u0 + k * vg
                if abs(ug - gu) < GRID_CLEAR:
                    nu = gu + (GRID_CLEAR if ug >= gu else -GRID_CLEAR)
                    r = guide_at(guide, 0, nu, s)
                    if r:
                        s, ug, vg, ang = r
    return s, ug, vg, ang


def snap(ug, vg, ang, pick="nearest", R=9, half=None):
    """Returns (u, v, run_len, width_across, mode, nruns) or None."""
    steep = ang > math.radians(55)
    if steep:
        v = int(round(vg))
        rs = [r for r in row_runs(v, int(ug) - 40, int(ug) + 40)]
        rs = [r for r in rs if r[0] - R <= ug <= r[1] + R]
        if not rs:
            return None
        r = min(rs, key=lambda r: abs((r[0] + r[1]) / 2 - ug))
        L = r[1] - r[0] + 1
        w = L * math.sin(ang)
        h = (half if half else w / 2) / max(math.sin(ang), 0.2)
        c = {"left": r[0] + h - 0.5, "right": r[1] - h + 0.5}.get(pick, (r[0] + r[1]) / 2)
        return c, float(v), L, w, "row", len(rs)
    u = int(round(ug))
    rs = [r for r in col_runs(u, int(vg) - 40, int(vg) + 40)]
    rs = [r for r in rs if r[0] - R <= vg <= r[1] + R]
    if not rs:
        return None
    r = min(rs, key=lambda r: abs((r[0] + r[1]) / 2 - vg))
    L = r[1] - r[0] + 1
    w = L * math.cos(ang)
    h = (half if half else w / 2) / max(math.cos(ang), 0.2)
    c = {"top": r[0] + h - 0.5, "bottom": r[1] - h + 0.5}.get(pick, (r[0] + r[1]) / 2)
    return float(u), c, L, w, "col", len(rs)


def propose(name, spec, show=True):
    guide = spec["guide"]
    targets = []
    x_end = xy(*guide[-1])[0]
    k = 1
    while k * 0.25 <= x_end + 1e-9:
        for hit in locate_on_guide(guide, k * 0.25, "x"):
            targets.append(("x", k * 0.25) + hit)
        k += 1
    for L in spec.get("loads", []):
        hits = locate_on_guide(guide[: spec["rise_end"] + 1], L, "y")
        for hit in hits[:1]:
            targets.append(("y", L) + hit)
    targets.sort(key=lambda t: t[2])
    rows = []
    for kind, val, s, ug, vg, ang in targets:
        pick, R, gap, half = "nearest", spec.get("R", 9), spec.get("gap", 0), None
        for z in spec.get("zones", []):
            if z["s"][0] <= ug <= z["s"][1]:
                pick = z.get("pick", pick); R = z.get("R", R); half = z.get("half", half)
        s, ug, vg, ang = clear_of_grid(guide, s, ug, vg, ang)
        res = snap(ug, vg, ang, pick, R, half) if pick != "guide" else (ug, vg, 0, 0, "guide", 0)
        shift = 0
        if res is None and gap:
            for d in range(1, int(gap) + 6):
                for sgn in (1, -1):
                    uu, vv, aa = point_at_arc(guide, s + sgn * d)
                    _, uu, vv, aa = clear_of_grid(guide, s + sgn * d, uu, vv, aa)
                    res = snap(uu, vv, aa, pick, R, half)
                    if res:
                        shift = sgn * d
                        break
                if res:
                    break
        rows.append((kind, val, s, round(ug, 1), round(vg, 1), math.degrees(ang), res, shift))
        if show:
            if res:
                u, v, Lr, w, mode, nr = res
                x, y = xy(u, v)
                print(f"{name:7s} {kind}={val:<6g} guide ({ug:7.1f},{vg:7.1f}) ang {math.degrees(ang):4.0f} -> "
                      f"({u:7.1f},{v:7.1f}) {mode} run {Lr:3d} w {w:4.1f} nruns {nr} shift {shift:+d}  x {x:.3f} y {y:.0f}")
            else:
                print(f"{name:7s} {kind}={val:<6g} guide ({ug:7.1f},{vg:7.1f}) ang {math.degrees(ang):4.0f} -> NO INK")
    return rows


if __name__ == "__main__":
    specs = json.loads((HERE / "guides.json").read_text(encoding="utf-8"))
    names = sys.argv[1:] or list(specs)
    for n in names:
        propose(n, specs[n])
        print()
