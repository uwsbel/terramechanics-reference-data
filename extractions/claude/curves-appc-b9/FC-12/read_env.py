"""Reader's helper for a computer-plotted failure envelope (one straight line, triangle markers).

    python read_env.py config.json            -> prints diagnostics, writes points-p1.csv

config.json keys:
  image, cal_dir, tools_dir, figure_id, series_id, out
  line_p1, line_p2   two (u, v) points near the drawn line (by eye), to seed the fit
  triangles          list of [u0, v0, u1, v1] boxes, one per symbol, tight around it (by eye)
  tri_notes          optional list of notes, one per triangle
  left_end, right_end  optional overrides {"u":..,"v":..,"bu":..,"bv":..,"note":..}
  intercept          optional override, same form, or "none"

Pixel coordinates: page image as scanned, u right, v down. Values come from the tools' piecewise map
(D-025). Nothing here edits tools/.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

DARK = 128


def runs(mask_col):
    idx = np.where(mask_col)[0]
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


def main():
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    sys.path.insert(0, cfg["tools_dir"])
    import calibrate_axes as ca

    gray = np.asarray(Image.open(cfg["image"]).convert("L"), dtype=float)
    D = gray < DARK
    H, W = D.shape
    cal = json.loads((Path(cfg["cal_dir"]) / "calibration.json").read_text(encoding="utf-8"))
    _, X, Y = ca.piecewise_maps(cfg["cal_dir"], cfg["image"])
    vlines = [(l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
    hlines = [(l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]

    def near_vline(u, v, tol):
        return any(abs(u - (a + b * v)) <= tol for a, b in vlines)

    def near_hline(u, v, tol):
        return any(abs(v - (a + b * u)) <= tol for a, b in hlines)

    tris = cfg["triangles"]

    def in_tri(u, v, pad=4):
        return any(t[0] - pad <= u <= t[2] + pad and t[1] - pad <= v <= t[3] + pad for t in tris)

    # ---- 1. the drawn line: run centres per column, robust straight fit (diagnostic and seed only)
    (pu1, pv1), (pu2, pv2) = cfg["line_p1"], cfg["line_p2"]
    k0 = (pv2 - pv1) / (pu2 - pu1)
    seed = lambda u: pv1 + k0 * (u - pu1)
    cols = []
    for u in range(int(min(pu1, pu2)), int(max(pu1, pu2)) + 1):
        vs = seed(u)
        if near_vline(u, vs, 9) or in_tri(u, vs, 6):
            continue
        lo, hi = int(vs - 25), int(vs + 25)
        rr = [(a + lo, b + lo) for a, b in runs(D[lo:hi, u])]
        rr = [r for r in rr if r[0] - 3 <= vs <= r[1] + 3]
        if len(rr) != 1:
            continue
        a, b = rr[0]
        c = 0.5 * (a + b)
        if near_hline(u, a, 6) or near_hline(u, b, 6):
            continue
        cols.append((u, c, b - a + 1))
    C = np.array(cols, dtype=float)
    Lmed = float(np.median(C[:, 2]))
    keep = np.abs(C[:, 2] - Lmed) <= 2.5
    k, v0 = np.polyfit(C[keep, 0], C[keep, 1], 1)
    for _ in range(3):
        res = C[:, 1] - (v0 + k * C[:, 0])
        keep = (np.abs(res) <= 2.0) & (np.abs(C[:, 2] - Lmed) <= 2.5)
        k, v0 = np.polyfit(C[keep, 0], C[keep, 1], 1)
    res = C[keep, 1] - (v0 + k * C[keep, 0])
    fit = lambda u: v0 + k * u
    theta = np.arctan(abs(k))
    w_perp = Lmed * np.cos(theta)
    half = 0.5 * w_perp
    print(f"line fit: v = {v0:.2f} + {k:.5f} u over {keep.sum()} clean columns; residual rms {res.std():.2f} px, max {np.abs(res).max():.2f}")
    print(f"  vertical run median {Lmed:.1f} px -> perpendicular thickness {w_perp:.1f} px (half {half:.1f})")
    # curvature check: residual by thirds
    third = np.array_split(np.argsort(C[keep, 0]), 3)
    print("  mean residual by thirds (px): " + ", ".join(f"{res[t].mean():+.2f}" for t in third))

    # ---- 2. ink along the centreline: gaps and ends
    e_t = np.array([1.0, k]) / np.hypot(1.0, k)
    e_s = np.array([-e_t[1], e_t[0]])

    def ink_at(u):
        v = fit(u)
        p = np.array([u, v])
        for ds in np.arange(-half + 1, half - 0.9, 1.0):
            q = p + ds * e_s
            if D[int(round(q[1])), int(round(q[0]))]:
                return True
        return False

    u_lo = int(min(pu1, pu2)) - 120
    u_hi = int(max(pu1, pu2)) + 120
    flags = [(u, ink_at(u)) for u in range(u_lo, u_hi + 1)]
    segs = []
    cur = None
    for u, f in flags:
        if f and cur is None:
            cur = [u, u]
        elif f:
            cur[1] = u
        elif cur is not None:
            segs.append(cur)
            cur = None
    if cur is not None:
        segs.append(cur)
    print("ink intervals along the fitted centreline (u):")
    for s in segs:
        if s[1] - s[0] >= 2:
            print(f"  {s[0]:5d} .. {s[1]:5d}   (v {fit(s[0]):.0f} .. {fit(s[1]):.0f})")

    # ---- 3. local centre of the ink at a column, from clean neighbouring columns
    ONE_SIDED = set()

    def local(u_t, span=16, side=None):
        pts = []
        rng = range(int(u_t) - span, int(u_t) + span + 1)
        if side == 'right':
            rng = range(int(u_t) + 2, int(u_t) + 2 * span + 1)
        elif side == 'left':
            rng = range(int(u_t) - 2 * span, int(u_t) - 1)
        for u in rng:
            vs = fit(u)
            if near_vline(u, vs, 7) or in_tri(u, vs, 3):
                continue
            lo, hi = int(vs - 20), int(vs + 20)
            rr = [(a + lo, b + lo) for a, b in runs(D[lo:hi, u])]
            rr = [r for r in rr if r[0] - 2 <= vs <= r[1] + 2]
            if len(rr) != 1:
                continue
            a, b = rr[0]
            if abs((b - a + 1) - Lmed) > 2.5 or near_hline(u, a, 5) or near_hline(u, b, 5):
                continue
            pts.append((u, 0.5 * (a + b)))
        if len(pts) < 4:
            return None, len(pts)
        P = np.array(pts, dtype=float)
        if side is None and not (P[:, 0].min() <= u_t + 3 and P[:, 0].max() >= u_t - 3):
            gap = min(abs(P[:, 0] - u_t))
            if len(pts) < 6 or gap > 10:
                return None, len(pts)
            ONE_SIDED.add(round(u_t, 1))
        kk, cc = np.polyfit(P[:, 0], P[:, 1], 1)
        return float(cc + kk * u_t), len(pts)

    # ---- 4. triangles: sides and base from the ink with the grid and the drawn line masked
    M = D.copy()
    vv, uu = np.mgrid[0:H, 0:W]
    rows = []
    for i, t in enumerate(tris):
        u0, v0b, u1, v1b = t
        sub = M[v0b:v1b + 1, u0:u1 + 1].copy()
        U = uu[v0b:v1b + 1, u0:u1 + 1]
        V = vv[v0b:v1b + 1, u0:u1 + 1]
        for a, b in hlines:
            sub &= ~(np.abs(V - (a + b * U)) <= 5)
        for a, b in vlines:
            sub &= ~(np.abs(U - (a + b * V)) <= 5)
        lm = (cfg.get("line_mask") or ["all"] * len(tris))[i]
        if lm != "none":
            dist = np.abs((V - fit(U)) * np.cos(theta))
            near = dist <= half + 1.5
            if lm != "all":
                near &= (U >= lm[0]) & (U <= lm[1])
            sub &= ~near
        masked = D[v0b:v1b + 1, u0:u1 + 1] & ~sub
        def dil(m):
            o = m.copy()
            o[1:, :] |= m[:-1, :]
            o[:-1, :] |= m[1:, :]
            o2 = o.copy()
            o2[:, 1:] |= o[:, :-1]
            o2[:, :-1] |= o[:, 1:]
            return o2
        sub = ~dil(~dil(sub)) | sub
        opt = (cfg.get("tri_opts") or [{}] * len(tris))[i] or {}
        ys, xs = np.where(sub)
        if len(ys) == 0:
            print(f"triangle {i+1}: no ink left after masking")
            continue
        top, bot = ys.min(), ys.max()
        left, right = xs.min(), xs.max()
        h_box = bot - top
        bc = opt.get("base_cols")
        xr = range(bc[0] - u0, bc[1] - u0 + 1) if bc else range(int(left + 0.3 * (right - left)), int(right - 0.3 * (right - left)) + 1)
        bases, bwid, bbot = [], [], []
        for x in xr:
            rr = runs(sub[:, x])
            if rr and rr[-1][0] > top + 0.6 * h_box:
                bases.append(0.5 * (rr[-1][0] + rr[-1][1]))
                bwid.append(rr[-1][1] - rr[-1][0] + 1)
                bbot.append(rr[-1][1])
        if not bases:
            print(f"triangle {i+1}: no base found")
            continue
        vb = float(np.median(bases))
        wst = float(opt.get("stroke", np.median(bwid)))
        Hn = opt.get("h_nominal", 30.0)
        r0, r1 = opt.get("rows", [vb + v0b - 0.78 * Hn, vb + v0b - wst / 2 - 2])
        Ls, Rs, Lo, Ro = [], [], [], []
        for y in range(int(round(r0 - v0b)), int(round(r1 - v0b)) + 1):
            if y < 0 or y >= sub.shape[0]:
                continue
            rr = runs(sub[y, :])
            if len(rr) >= 2:
                Ls.append((y, 0.5 * (rr[0][0] + rr[0][1])))
                Rs.append((y, 0.5 * (rr[-1][0] + rr[-1][1])))
                Lo.append((y, rr[0][0] - 0.5))
                Ro.append((y, rr[-1][1] + 0.5))

        def sidefit(S):
            if len(S) < 4:
                return None
            S = np.array(S, dtype=float)
            a1, a0 = np.polyfit(S[:, 0], S[:, 1], 1)
            r = S[:, 1] - (a0 + a1 * S[:, 0])
            ok = np.abs(r) <= 1.5
            if ok.sum() >= 4:
                a1, a0 = np.polyfit(S[ok, 0], S[ok, 1], 1)
            return [a1, a0, int(ok.sum()), len(S)]

        sl, sr, so_l, so_r = sidefit(Ls), sidefit(Rs), sidefit(Lo), sidefit(Ro)
        if so_l is not None:
            so_l[1] += 0.5 * wst * np.hypot(1, so_l[0])
        if so_r is not None:
            so_r[1] -= 0.5 * wst * np.hypot(1, so_r[0])
        vb_edge = float(np.median(bbot)) + 0.5 - wst / 2
        mir = opt.get("mirror")
        if mir:
            # isosceles: the hidden side is the mirror of the visible one about the base's axis
            yb = int(round(vb))
            rr = runs(sub[yb, :])
            ax = opt.get("axis_u", 0.5 * (rr[0][0] + rr[-1][1]) + u0) - u0
            print(f"  mirror axis u = {ax + u0:.1f} (base row runs {[(a + u0, b + u0) for a, b in rr]})")
            if mir == "left":
                sl = [-sr[0], 2 * ax - sr[1], sr[2], sr[3]]
                so_l = [-so_r[0], 2 * ax - so_r[1], so_r[2], so_r[3]]
            else:
                sr = [-sl[0], 2 * ax - sl[1], sl[2], sl[3]]
                so_r = [-so_l[0], 2 * ax - so_l[1], so_l[2], so_l[3]]

        def recon(sl, sr, vb):
            ya = (sr[1] - sl[1]) / (sl[0] - sr[0])
            ua = sl[1] + sl[0] * ya
            ubl = sl[1] + sl[0] * vb
            ubr = sr[1] + sr[0] * vb
            return (ua + u0, ya + v0b), (ubl + u0, vb + v0b), (ubr + u0, vb + v0b)

        if sl is None or sr is None:
            print(f"triangle {i+1}: could not reconstruct (left {sl}, right {sr})")
            continue
        A, BL, BR = recon(sl, sr, vb)
        A2, BL2, BR2 = recon(so_l, so_r, vb_edge)
        cu, cv = (A[0] + BL[0] + BR[0]) / 3, (A[1] + BL[1] + BR[1]) / 3
        cu2, cv2 = (A2[0] + BL2[0] + BR2[0]) / 3, (A2[1] + BL2[1] + BR2[1]) / 3
        h, h2 = BL[1] - A[1], BL2[1] - A2[1]
        bbox_mid = (0.5 * (left + right) + u0, 0.5 * (top + bot) + v0b)
        print(f"triangle {i+1}: stroke {wst:.1f}; centres: apex ({A[0]:.1f},{A[1]:.1f}) base v {BL[1]:.1f} u {BL[0]:.1f}..{BR[0]:.1f} "
              f"h {h:.1f} b {BR[0]-BL[0]:.1f} -> centroid ({cu:.1f},{cv:.1f}) [rows {sl[2]}/{sl[3]}, {sr[2]}/{sr[3]}, base cols {len(bases)}]")
        print(f"            edges inset: apex ({A2[0]:.1f},{A2[1]:.1f}) base v {BL2[1]:.1f} u {BL2[0]:.1f}..{BR2[0]:.1f} "
              f"h {h2:.1f} b {BR2[0]-BL2[0]:.1f} -> centroid ({cu2:.1f},{cv2:.1f}); ink bbox mid ({bbox_mid[0]:.1f},{bbox_mid[1]:.1f})"
              + (f"; mirrored {mir}" if mir else ""))
        meth = opt.get("method", "centre")
        pick = (cu, cv, h) if meth == "centre" else (cu2, cv2, h2)
        rows.append({"i": i + 1, "cu": pick[0], "cv": pick[1], "h": pick[2], "centre": [cu, cv, h], "edge": [cu2, cv2, h2],
                     "stroke": wst, "method": meth})
        from PIL import ImageDraw
        Z = 8
        pad = 6
        bu0, bv0, bu1, bv1 = u0 - pad, v0b - pad, u1 + pad, v1b + pad
        img = np.full((bv1 - bv0 + 1, bu1 - bu0 + 1, 3), 255, np.uint8)
        img[D[bv0:bv1 + 1, bu0:bu1 + 1]] = (190, 190, 190)
        img[pad:pad + sub.shape[0], pad:pad + sub.shape[1]][sub & D[v0b:v1b + 1, u0:u1 + 1]] = (0, 0, 0)
        im = Image.fromarray(img).resize((img.shape[1] * Z, img.shape[0] * Z), Image.NEAREST)
        dr = ImageDraw.Draw(im)
        Pz = lambda q: ((q[0] - bu0 + 0.5) * Z, (q[1] - bv0 + 0.5) * Z)
        dr.polygon([Pz(A), Pz(BL), Pz(BR)], outline=(230, 0, 0))
        dr.polygon([Pz(A2), Pz(BL2), Pz(BR2)], outline=(0, 170, 0))
        for (qx, qy), col in (((cu, cv), (230, 0, 0)), ((cu2, cv2), (0, 170, 0))):
            cx, cy = Pz((qx, qy))
            dr.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=col)
        im.save(Path(cfg["out"]) / f"check-tri{i+1}.png")

    # ---- 5. sampling at every 500 psf
    def x_at(u):
        return X.value(u, fit(u))[0]

    def u_for_x(xt, a, b):
        fa = x_at(a) - xt
        for _ in range(60):
            m = 0.5 * (a + b)
            fm = x_at(m) - xt
            if (fm > 0) == (fa > 0):
                a, fa = m, fm
            else:
                b = m
        return 0.5 * (a + b)

    cfg_out = {"fit": [float(v0), float(k)], "Lmed": Lmed, "w_perp": float(w_perp), "half": float(half),
               "segs": [s for s in segs if s[1] - s[0] >= 2], "triangles": rows}
    Path(cfg["out"]).mkdir(parents=True, exist_ok=True)
    (Path(cfg["out"]) / "helper-diagnostics.json").write_text(json.dumps(cfg_out, indent=1), encoding="utf-8")

    print("samples at multiples of 500 psf (local ink centre from clean neighbouring columns):")
    lo_u, hi_u = cfg.get("sample_range", [segs[0][0], segs[-1][1]])
    x_lo, x_hi = x_at(lo_u), x_at(hi_u)
    xs = np.arange(np.ceil((x_lo + 1e-6) / 500) * 500, x_hi, 500)
    samples = []
    for xt in xs:
        ut = u_for_x(xt, lo_u - 50, hi_u + 50)
        vc, n = local(ut)
        on_ink = ink_at(ut) or near_vline(ut, fit(ut), 7)
        flag = "" if (vc is not None and on_ink and not in_tri(ut, fit(ut), 0)) else "CHECK"
        print(f"  x {xt:6.0f}: u {ut:7.1f}  v_fit {fit(ut):7.1f}  v_local {vc if vc is None else round(vc, 1)}  ({n} cols) "
              f"{'on vertical grid line' if near_vline(ut, fit(ut), 7) else ''} {'in triangle box' if in_tri(ut, fit(ut), 0) else ''} {flag}")
        samples.append((float(xt), float(ut), vc, flag))
    (Path(cfg["out"]) / "helper-samples.json").write_text(json.dumps(samples, indent=1), encoding="utf-8")

    # ---- 6. points file
    def sym_row(kind, seq, u, v, bu, bv, symbol, note):
        return {"figure_id": cfg["figure_id"], "panel": 1, "series_id": cfg["series_id"], "point_kind": kind,
                "sequence": seq, "pixel_u": round(u, 1), "pixel_v": round(v, 1), "u_bound_px": bu, "v_bound_px": bv,
                "symbol": symbol, "note": note}

    out_rows = []
    tb = cfg.get("tri_bounds") or [[2, 5]] * len(rows)
    tn = cfg.get("tri_notes") or [""] * len(rows)
    for j, r in enumerate(sorted(rows, key=lambda r: r["cu"])):
        k_ = r["i"] - 1
        note = f"centroid of the reconstructed triangle ({r['method']} method), height {r['h']:.1f} px"
        if tn[k_]:
            note += "; " + tn[k_]
        out_rows.append(sym_row("marker", j + 1, r["cu"], r["cv"], tb[k_][0], tb[k_][1], "triangle-up", note))
    hb = cfg.get("trace_half", round(half, 1))
    le, re_ = cfg["left_end"], cfg["right_end"]

    def end_point(e):
        u = e["u"]
        v, n = local(u, side=e["side"])
        return u, v, n

    lu, lv, ln = end_point(le)
    ru, rv, rn = end_point(re_)
    print(f"left end: u {lu:.1f} v {lv:.1f} ({ln} cols, {le['side']} side); right end: u {ru:.1f} v {rv:.1f} ({rn} cols, {re_['side']} side)")
    trace = [(lu, lv, le["bu"], le["bv"], le["note"])]
    skip = {float(k): v for k, v in (cfg.get("trace_override") or {}).items()}
    for xt, ut, vc, flag in samples:
        if ut <= lu + 2 or ut >= ru - 2:
            continue
        if xt in skip:
            o = skip[xt]
            if o == "skip":
                print(f"  x {xt:g}: skipped by config")
                continue
            ut = o["u"]
            vc, _ = local(ut)
            note = o["note"]
        else:
            note = ""
        if vc is None:
            print(f"  x {xt:g}: no clean ink, left out")
            continue
        if near_vline(ut, vc, 7):
            how = "clean columns on one side only (within 10 px)" if round(ut, 1) in ONE_SIDED else "clean columns either side"
            note = (note + "; " if note else "") + f"at x = {xt:g} psf, on a vertical grid line crossing: centre from {how}"
        trace.append((ut, vc, hb, hb, note or f"at x = {xt:g} psf"))
    trace.append((ru, rv, re_["bu"], re_["bv"], re_["note"]))
    for j, (u, v, bu, bv, note) in enumerate(trace):
        out_rows.append(sym_row("trace", j + 1, u, v, bu, bv, "", note))
    out_rows.append(sym_row("feature", 1, lu, lv, le["bu"], le["bv"], "", "first point of the line: " + le["note"]))
    out_rows.append(sym_row("feature", 2, ru, rv, re_["bu"], re_["bv"], "", "last point of the line: " + re_["note"]))
    ic = cfg.get("intercept")
    if ic and ic != "none":
        iv, n = local(ic["u"], side=ic["side"])
        out_rows.append(sym_row("feature", 3, ic["u"], iv, ic["bu"], ic["bv"], "", "intercept: " + ic["note"]))
        print(f"intercept: u {ic['u']:.1f} v {iv:.1f} ({n} cols)")
    cols_ = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
    with (Path(cfg["out"]) / "points-p1.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols_, lineterminator="\n")
        w.writeheader()
        w.writerows(out_rows)
    print(f"wrote points-p1.csv: {sum(r['point_kind'] == 'marker' for r in out_rows)} markers, "
          f"{sum(r['point_kind'] == 'trace' for r in out_rows)} trace, {sum(r['point_kind'] == 'feature' for r in out_rows)} features")


if __name__ == "__main__":
    main()
