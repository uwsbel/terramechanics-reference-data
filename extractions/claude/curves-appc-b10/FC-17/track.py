"""Reader's helper: follow one drawn curve column by column on the binary page image.

    python track.py <image> <calibration.json> <name> <u_start> <v_start> <u_stop> [--json out.json]

At each column u the dark runs within 14 px of the predicted centre (linear prediction from the last
clean columns) are listed. A column is
    clean   one run of normal thickness, away from grid lines: centre = run centre;
    vgrid   within 5 px of a vertical grid line or frame line (the column is dark there);
    hgrid   the run touches a horizontal grid line: the curve's centre is taken from its free edge
            (the edge outside the grid line's band) minus or plus half the curve's thickness;
    thick   a run much thicker than the curve away from grid lines (a symbol or another line);
    gap     no ink near the prediction.
Prints a summary of the dashes (stretches of ink separated by gaps of 3 or more empty columns, a
vertical grid line crossing does not break a dash when ink is found on both sides) and writes every
column's record to the json file.
"""
import argparse
import json
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("image")
ap.add_argument("cal")
ap.add_argument("name")
ap.add_argument("u_start", type=int)
ap.add_argument("v_start", type=float)
ap.add_argument("u_stop", type=int)
ap.add_argument("--json")
ap.add_argument("--window", type=float, default=14)
ap.add_argument("--mask", default="", help="u,v,r;u,v,r discs (plotted circles) whose ink is not this curve")
a = ap.parse_args()

g = np.asarray(Image.open(a.image).convert("L")) < 128
g = g.copy()
masks = [tuple(float(x) for x in m.split(",")) for m in a.mask.split(";") if m.strip()]
VV, UU = np.mgrid[0:g.shape[0], 0:g.shape[1]]
for mu, mv, mr in masks:
    sl = (slice(int(mv - mr - 1), int(mv + mr + 2)), slice(int(mu - mr - 1), int(mu + mr + 2)))
    disc = (UU[sl] - mu) ** 2 + (VV[sl] - mv) ** 2 <= mr ** 2
    g[sl][disc] = False
cal = json.load(open(a.cal, encoding="utf-8"))
vls = [(l["u_at_v0"], l["slope_du_dv"]) for l in cal["vertical_lines"]]
# frame lines (measured with plot_grid lines: left 717.5 at v 1330, 755.5 at v 3530; right 2572.5, 2610)
vls += [(717.5 - 1330 * (38 / 2200), 38 / 2200), (2572.5 - 1330 * (37.5 / 2200), 37.5 / 2200)]
hls = [(l["v_at_u0"], l["slope_dv_du"]) for l in cal["horizontal_lines"]]
GRID_HALF_V = 5.0   # half width of a vertical grid line (3) plus margin
GRID_HALF_H = 3.5   # half width of a horizontal grid line


def runs(col, lo, hi):
    lo, hi = int(max(lo, 0)), int(min(hi, len(col) - 1))
    out, s = [], None
    for v in range(lo, hi + 1):
        if col[v] and s is None:
            s = v
        if (not col[v] or v == hi) and s is not None:
            e = v - 1 if not col[v] else v
            out.append((s, e))
            s = None
    return out


recs = []
hist = [(a.u_start, a.v_start)]
t_typ = 8.0
for u in range(a.u_start, a.u_stop + 1):
    pts = hist[-60:]
    if len(pts) >= 5:
        k, c = np.polyfit([p[0] for p in pts], [p[1] for p in pts], 1)
        vp = k * u + c
    else:
        vp = hist[-1][1]
    col = g[:, u]
    # extend runs fully even if they leave the window
    rr = runs(col, vp - a.window, vp + a.window)
    full = []
    for s, e in rr:
        while s > 0 and col[s - 1]:
            s -= 1
        while e < len(col) - 1 and col[e + 1]:
            e += 1
        full.append((s, e))
    near_v = any(abs(u - (iv + sv * vp)) <= GRID_HALF_V for iv, sv in vls)
    rec = {"u": u, "vp": round(vp, 2)}
    if near_v:
        rec["kind"] = "vgrid"
        rec["ink"] = bool(full)
    elif not full:
        rec["kind"] = "gap"
    else:
        s, e = min(full, key=lambda r: abs(0.5 * (r[0] + r[1]) - vp))
        c, t = 0.5 * (s + e), e - s + 1
        hg = [ih + sh * u for ih, sh in hls]
        hit = [vh for vh in hg if s - GRID_HALF_H <= vh <= e + GRID_HALF_H]
        rec.update({"s": s, "e": e, "t": t})
        if not (s - 3 <= vp <= e + 3):
            # the nearest ink does not cover the predicted centre: another line or a symbol, not this curve
            rec = {"u": u, "vp": round(vp, 2), "kind": "gap", "other": [s, e]}
        elif hit:
            vh = hit[0]
            top_band, bot_band = vh - GRID_HALF_H, vh + GRID_HALF_H
            # free edges: the run's edge outside the grid band
            if e > bot_band + 1 and s >= top_band - 1:      # curve sticks out below
                rec.update(kind="hgrid", v=e + 0.5 - t_typ / 2, edge="bottom")
            elif s < top_band - 1 and e <= bot_band + 1:    # curve sticks out above
                rec.update(kind="hgrid", v=s - 0.5 + t_typ / 2, edge="top")
            elif s < top_band - 1 and e > bot_band + 1:     # both: curve wider than band? take middle of the excess
                rec.update(kind="hgrid", v=c, edge="both")
            else:                                           # hidden inside the band
                rec.update(kind="hgrid", v=vh, edge="hidden")
                if abs(vp - vh) > 4:                        # the curve is predicted off the band: grid line only
                    rec = {"u": u, "vp": round(vp, 2), "kind": "gap", "other": [s, e]}
        elif t > 1.6 * t_typ:
            # merged with a symbol or another line: the curve's free edge, the one nearer the prediction
            vt, vb = s - 0.5 + t_typ / 2, e + 0.5 - t_typ / 2
            if abs(vt - vp) <= abs(vb - vp):
                rec.update(kind="thick", v=vt, edge="top")
            else:
                rec.update(kind="thick", v=vb, edge="bottom")
        else:
            rec.update(kind="clean", v=c)
            t_typ = 0.9 * t_typ + 0.1 * t
    recs.append(rec)
    if ((rec.get("kind") == "clean" and rec["t"] >= 0.6 * t_typ) or (rec.get("kind") == "hgrid" and rec.get("edge") in ("top", "bottom"))) and abs(rec["v"] - vp) < 6:
        hist.append((u, rec["v"]))

# dashes
inks = [r for r in recs if r["kind"] in ("clean", "hgrid", "thick") or (r["kind"] == "vgrid" and r.get("ink"))]
dashes = []
cur = None
for r in recs:
    has = r["kind"] in ("clean", "hgrid", "thick") or r["kind"] == "vgrid"
    if r["kind"] == "gap":
        if cur is not None:
            cur["gap"] += 1
            if cur["gap"] >= 3:
                dashes.append(cur)
                cur = None
        continue
    if cur is None:
        cur = {"u0": r["u"], "u1": r["u"], "gap": 0}
    cur["u1"] = r["u"]
    cur["gap"] = 0
if cur is not None:
    dashes.append(cur)
print(f"{a.name}: typical thickness {t_typ:.1f} px; columns: " + ", ".join(
    f"{k} {sum(1 for r in recs if r['kind'] == k)}" for k in ("clean", "hgrid", "vgrid", "thick", "gap")))
for d in dashes:
    sub = [r for r in recs if d["u0"] <= r["u"] <= d["u1"] and "v" in r]
    v0 = sub[0]["v"] if sub else None
    v1 = sub[-1]["v"] if sub else None
    print(f"  dash u {d['u0']}..{d['u1']}  v {v0} .. {v1}")
if a.json:
    json.dump({"name": a.name, "t_typ": t_typ, "records": recs, "dashes": [[d["u0"], d["u1"]] for d in dashes]},
              open(a.json, "w", encoding="utf-8"), indent=0)
