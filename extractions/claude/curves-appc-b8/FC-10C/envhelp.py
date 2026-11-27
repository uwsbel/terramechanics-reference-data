"""Reader's helper for a computer-plotted failure envelope (one straight line, triangle symbols).

Not part of tools/. Written by the Claude reader, batch curves-appc-b8. Uses tools/calibrate_axes.py
(imported, unmodified) for the piecewise map.

    scan    --image IMG --p0 u v --p1 u v [--halfwin 14] [--dark 150] [--grid-u u,u,..] [--grid-v v,v,..]
            column-by-column centre of the drawn line between two rough end points: darkness-weighted
            centre and vertical run length of the dark run nearest the predicted position. Columns
            within 7 px of a vertical grid line, rows within 7 px of a horizontal grid line, and runs
            longer than 1.5 x the median run are flagged and not used in the fit. Prints the robust
            straight-line fit v = a + b u, its residual RMS, the run length, the perpendicular
            thickness, and the gaps (columns with no ink near the line).
    tri     --image IMG --box u0 v0 u1 v1 [--line a b --mask px]
            bbox of the dark ink in the box after removing the pixels within `mask` px (vertically)
            of the line v = a + b u; prints the outer bbox and the centroid of the upright triangle
            whose base is the bottom row and apex the top row: u_c = (uL + uR + u_apex)/3,
            v_c = (2 v_base + v_apex)/3.
    samples --image IMG --cal CALDIR --line a b --xs 500,1000,.. [--clean u0:u1,..]
            for each x value, the column u where the line (v = a + b u) has that x on the piecewise
            map, and the line's measured centre at that column (mean of the clean measured centres
            within +-2 columns; when there are none, e.g. on a vertical grid line, the mean of the
            measured centres 6 to 14 columns either side, which on a straight line is its centre).
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def gray_of(path):
    return np.asarray(Image.open(path).convert("L"), dtype=float)


def runs(idx):
    out = []
    if len(idx) == 0:
        return out
    s = p = int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i != p + 1:
            out.append((s, p))
            s = i
        p = i
    out.append((s, p))
    return out


def column_centres(g, u_from, u_to, a0, b0, halfwin, dark, grid_u=(), grid_v=()):
    rows = []
    for u in range(int(u_from), int(u_to) + 1):
        vp = a0 + b0 * u
        lo, hi = int(vp - halfwin), int(vp + halfwin) + 1
        col = g[lo:hi, u]
        rr = runs(np.where(col < dark)[0])
        if not rr:
            rows.append((u, None, 0, "gap"))
            continue
        best = min(rr, key=lambda r: abs((r[0] + r[1]) / 2 + lo - vp))
        s, e = best
        w = np.clip(255 - col[s:e + 1], 0, None)
        c = lo + float(np.sum(np.arange(s, e + 1) * w) / np.sum(w))
        flag = ""
        if any(abs(u - gu) <= 7 for gu in grid_u):
            flag = "vgrid"
        if any(abs(c - gv) <= 7 for gv in grid_v):
            flag = (flag + " hgrid").strip()
        rows.append((u, c, e - s + 1, flag))
    return rows


def robust_fit(us, vs):
    us, vs = np.asarray(us, float), np.asarray(vs, float)
    keep = np.ones(len(us), bool)
    for _ in range(5):
        b, a = np.polyfit(us[keep], vs[keep], 1)
        res = vs - (a + b * us)
        mad = np.median(np.abs(res[keep] - np.median(res[keep]))) * 1.4826
        new = np.abs(res) <= max(1.0, 3 * mad)
        if (new == keep).all():
            break
        keep = new
    b, a = np.polyfit(us[keep], vs[keep], 1)
    res = vs[keep] - (a + b * us[keep])
    return a, b, float(np.sqrt(np.mean(res ** 2))), keep


def cmd_scan(a):
    g = gray_of(a.image)
    (u0, v0), (u1, v1) = a.p0, a.p1
    b0 = (v1 - v0) / (u1 - u0)
    a0 = v0 - b0 * u0
    gu = [float(x) for x in a.grid_u.split(",")] if a.grid_u else []
    gv = [float(x) for x in a.grid_v.split(",")] if a.grid_v else []
    rows = column_centres(g, u0, u1, a0, b0, a.halfwin, a.dark, gu, gv)
    ok = [r for r in rows if r[1] is not None and not r[3]]
    med = float(np.median([r[2] for r in ok]))
    clean = [r for r in ok if r[2] <= 1.5 * med]
    fa, fb, rms, keep = robust_fit([r[0] for r in clean], [r[1] for r in clean])
    thick = med * abs(np.cos(np.arctan(fb)))
    print(f"fit v = {fa:.3f} + {fb:.6f} u over {keep.sum()} of {len(clean)} clean columns, residual RMS {rms:.3f} px")
    print(f"median vertical run {med:.1f} px; perpendicular thickness {thick:.2f} px; angle {np.degrees(np.arctan(-fb)):.2f} deg")
    gaps = runs(np.array([r[0] for r in rows if r[1] is None]))
    print("gaps (no ink within the window): " + (", ".join(f"{s}..{e}" for s, e in gaps) or "none"))
    far = [r for r in rows if r[1] is not None and abs(r[1] - (fa + fb * r[0])) > 2.5]
    print("columns whose nearest run is >2.5 px off the fit: " + (", ".join(f"{s}..{e}" for s, e in runs(np.array([r[0] for r in far]))) or "none"))
    if a.dump:
        with open(a.dump, "w", encoding="utf-8") as f:
            f.write("u,v_centre,run,flag,res\n")
            for r in rows:
                res = "" if r[1] is None else f"{r[1] - (fa + fb * r[0]):.2f}"
                f.write(f"{r[0]},{'' if r[1] is None else round(r[1], 2)},{r[2]},{r[3]},{res}\n")
    return 0


def cmd_tri(a):
    g = gray_of(a.image)
    u0, v0, u1, v1 = a.box
    sub = g[v0:v1, u0:u1] < a.dark
    if a.line:
        la, lb = a.line
        V, U = np.mgrid[v0:v1, u0:u1]
        sub &= ~(np.abs(V - (la + lb * U)) <= a.mask)
    ys, xs = np.where(sub)
    if len(xs) == 0:
        print("no ink")
        return 1
    vt, vb = ys.min() + v0, ys.max() + v0
    uL, uR = xs.min() + u0, xs.max() + u0
    top = xs[ys == ys.min()] + u0
    ua = float(np.mean(top))
    h = vb - vt + 1
    # outer edges are pixel edges: top edge at vt - 0.5, bottom edge at vb + 0.5
    vte, vbe, uLe, uRe = vt - 0.5, vb + 0.5, uL - 0.5, uR + 0.5
    uc = (uLe + uRe + ua) / 3
    vc = (2 * vbe + vte) / 3
    print(f"ink bbox u {uL}..{uR}, v {vt}..{vb} (outer edges u {uLe}..{uRe}, v {vte}..{vbe}); height {h} px, width {uR - uL + 1} px; apex u {ua:.1f}")
    print(f"centroid u {uc:.1f}, v {vc:.1f}; bbox midpoint v {(vte + vbe) / 2:.1f}; h/6 = {h / 6:.1f}")
    return 0


def cmd_rows(a):
    """Per row of the box: the dark runs (u from..to). For reading a symbol's outline by eye."""
    g = gray_of(a.image)
    u0, v0, u1, v1 = a.box
    for v in range(v0, v1 + 1):
        rr = runs(np.where(g[v, u0:u1 + 1] < a.dark)[0])
        print(f"{v}: " + " ".join(f"{s + u0}-{e + u0}" for s, e in rr))
    return 0


def cmd_labels(a):
    """Centre of a printed axis label, to compare with the line it names. y labels: the text band
    (rows with ink) in the label column u0..u1 within +-search of the line's v. x labels: in the label
    row v0..v1, the text band, then the u extent of the ink cluster nearest the line (clusters split at
    gaps over `gap` px), using the upper 60 percent of the band so baseline dots and underscores do
    not count."""
    g = gray_of(a.image) < a.dark
    lo, hi = a.span
    for item in a.lines.split(","):
        name, pos = item.split(":")
        pos = float(pos)
        if a.axis == "y":
            v0, v1 = int(pos - a.search), int(pos + a.search)
            cnt = g[v0:v1, lo:hi].sum(axis=1)
            rr = runs(np.where(cnt >= 2)[0])
            best = min(rr, key=lambda r: abs((r[0] + r[1]) / 2 + v0 - pos))
            # merge neighbouring runs closer than 4 px (a digit's gap)
            s, e = best
            for r in rr:
                if r[0] > e and r[0] - e <= 4:
                    e = r[1]
                if r[1] < s and s - r[1] <= 4:
                    s = r[0]
            c = (s + e) / 2 + v0
            print(f"y label {name}: text rows {s + v0}..{e + v0}, centre v {c:.1f}; line at v {pos:.1f}; label - line {c - pos:+.1f} px")
        else:
            cnt = g[lo:hi, :].sum(axis=1)
            u0, u1 = int(pos - a.search), int(pos + a.search)
            sub = g[lo:hi, u0:u1]
            rows_ = np.where(sub.sum(axis=1) >= 2)[0]
            top, bot = rows_.min(), rows_.max()
            band = sub[top:top + int(0.6 * (bot - top + 1)), :]
            cols = np.where(band.sum(axis=0) >= 1)[0]
            cl = runs(cols)
            merged = []
            for s, e in cl:
                if merged and s - merged[-1][1] <= a.gap:
                    merged[-1] = (merged[-1][0], e)
                else:
                    merged.append((s, e))
            best = min(merged, key=lambda r: abs((r[0] + r[1]) / 2 + u0 - pos))
            c = (best[0] + best[1]) / 2 + u0
            print(f"x label {name}: text cols {best[0] + u0}..{best[1] + u0} (rows {top + lo}..{bot + lo}), centre u {c:.1f}; line at u {pos:.1f}; label - line {c - pos:+.1f} px")
    return 0


def cmd_fit(a):
    """Slope and intercept of the trace samples (least squares, y on x) and of the markers, from a
    points file with x_native, y_native; the intercept feature's y; against the printed values."""
    import csv
    rows = list(csv.DictReader(open(a.native, encoding="utf-8-sig")))
    def lsq(kind):
        P = [(float(r["x_native"]), float(r["y_native"])) for r in rows if r["point_kind"] == kind]
        x, y = np.array([p[0] for p in P]), np.array([p[1] for p in P])
        b, c = np.polyfit(x, y, 1)
        return b, c, len(P), float(np.sqrt(np.mean((y - (c + b * x)) ** 2)))
    b, c, n, rms = lsq("trace")
    print(f"trace: {n} samples, slope {b:.4f}, intercept at x = 0 {c:.1f} psf, residual RMS {rms:.1f} psf")
    if a.tan is not None:
        print(f"  slope - tan theta = {b - a.tan:+.4f} ({(b - a.tan) / a.tan * 100:+.2f} %); angle {np.degrees(np.arctan(b)):.2f} deg vs printed tan {np.degrees(np.arctan(a.tan)):.2f}")
    for r in rows:
        if r["point_kind"] == "feature" and "intercept" in r["note"]:
            yi = float(r["y_native"])
            print(f"intercept feature: x {float(r['x_native']):.1f}, y {yi:.1f} psf +- {float(r['y_read_bound']):.1f}"
                  + (f"; minus cohesion {yi - a.coh:+.1f} psf" if a.coh is not None else ""))
    bm, cm, nm, rm = lsq("marker")
    print(f"markers (diagnostic only): {nm} markers, slope {bm:.4f}, intercept {cm:.1f} psf, residual RMS {rm:.1f} psf")
    return 0


def cmd_samples(a):
    sys.path.insert(0, str(Path(a.tools).resolve()))
    import calibrate_axes as ca
    cal, X, Y = ca.piecewise_maps(a.cal, a.image)
    g = gray_of(a.image)
    la, lb = a.line
    gu = [float(x) for x in a.grid_u.split(",")] if a.grid_u else []
    gv = [float(x) for x in a.grid_v.split(",")] if a.grid_v else []
    for xv in [float(x) for x in a.xs.split(",")]:
        lo, hi = a.urange
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if X.value(mid, la + lb * mid)[0] < xv:
                lo = mid
            else:
                hi = mid
        u = 0.5 * (lo + hi)
        ui = int(round(u))
        near = column_centres(g, ui - 2, ui + 2, la, lb, a.halfwin, a.dark, gu, gv)
        near = [r for r in near if r[1] is not None and not r[3] and abs(r[1] - (la + lb * r[0])) < 2.5]
        how = "local"
        if near:
            v = float(np.mean([r[1] - lb * (r[0] - u) for r in near]))
        else:
            side = column_centres(g, ui - 14, ui - 6, la, lb, a.halfwin, a.dark, gu, gv) + \
                column_centres(g, ui + 6, ui + 14, la, lb, a.halfwin, a.dark, gu, gv)
            side = [r for r in side if r[1] is not None and abs(r[1] - (la + lb * r[0])) < 2.5]
            v = float(np.mean([r[1] - lb * (r[0] - u) for r in side])) if side else la + lb * u
            how = f"sides({len(side)})" if side else "fit"
        xr = X.value(u, v)[0]
        yr = Y.value(u, v)[0]
        print(f"x={xv:g}: u {u:.1f} v {v:.1f} ({how}); fit v {la + lb * u:.1f}; reads x {xr:.1f} y {yr:.1f}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("scan")
    s.add_argument("--image", required=True)
    s.add_argument("--p0", nargs=2, type=float, required=True)
    s.add_argument("--p1", nargs=2, type=float, required=True)
    s.add_argument("--halfwin", type=int, default=14)
    s.add_argument("--dark", type=int, default=150)
    s.add_argument("--grid-u", default="")
    s.add_argument("--grid-v", default="")
    s.add_argument("--dump")
    t = sp.add_parser("tri")
    t.add_argument("--image", required=True)
    t.add_argument("--box", nargs=4, type=int, required=True)
    t.add_argument("--line", nargs=2, type=float)
    t.add_argument("--mask", type=float, default=6)
    t.add_argument("--dark", type=int, default=150)
    r = sp.add_parser("rows")
    r.add_argument("--image", required=True)
    r.add_argument("--box", nargs=4, type=int, required=True)
    r.add_argument("--dark", type=int, default=150)
    lb = sp.add_parser("labels")
    lb.add_argument("--image", required=True)
    lb.add_argument("--axis", choices=["x", "y"], required=True)
    lb.add_argument("--span", nargs=2, type=int, required=True, help="u range of the y label column, or v range of the x label row")
    lb.add_argument("--lines", required=True, help="name:pos,... the line's position (v for y, u for x) at the labels")
    lb.add_argument("--search", type=int, default=60)
    lb.add_argument("--gap", type=int, default=20)
    lb.add_argument("--dark", type=int, default=150)
    f = sp.add_parser("fit")
    f.add_argument("native")
    f.add_argument("--tan", type=float)
    f.add_argument("--coh", type=float)
    m = sp.add_parser("samples")
    m.add_argument("--image", required=True)
    m.add_argument("--cal", required=True)
    m.add_argument("--tools", required=True)
    m.add_argument("--line", nargs=2, type=float, required=True)
    m.add_argument("--xs", required=True)
    m.add_argument("--urange", nargs=2, type=float, required=True)
    m.add_argument("--halfwin", type=int, default=14)
    m.add_argument("--dark", type=int, default=150)
    m.add_argument("--grid-u", default="")
    m.add_argument("--grid-v", default="")
    a = ap.parse_args()
    return {"scan": cmd_scan, "tri": cmd_tri, "rows": cmd_rows, "labels": cmd_labels, "fit": cmd_fit, "samples": cmd_samples}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
