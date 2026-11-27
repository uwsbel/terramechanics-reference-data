"""Reader helper (FA-38, Claude): refit the grid lines found by `calibrate_axes.py detect` on the ink outside
the Grain Size Parameters table, which is printed inside the plot frame and carries its own rules (a
vertical rule 8 to 10 px right of the 50 percent line, another near the 40 percent line, a row rule 3 to
8 px below the 3.0 mm line). detect's band tracks picked those rules up inside the table and tilted the
fitted lines (50: slope 0.0019 against 0.0065 for the clean lines; 1.0 mm, 20 and 30 percent failed the
ink check by 2.7 to 4.3 px). Here each line is seeded from detect's band samples outside the table,
then located on the ink with tools/calibrate_axes.ink_offset (unmodified) every 10 px along its length
outside the table, fitted robustly (residuals over max(1.5 px, 3 MAD) set aside), and the anchors are
the intersections of the refitted lines. Writes anchors.csv and calibration.json in detect's layout."""
import csv, json, sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import calibrate_axes as ca

src_dir, out_dir, image = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
TABLE = (1330, 1250, 1945, 2745)   # u0 v0 u1 v1 of the table, with a margin of about 8 px
cal = json.loads((src_dir / "calibration.json").read_text(encoding="utf-8"))
gray = np.asarray(Image.open(image).convert("L"), dtype=float)
u0, v0, u1, v1 = cal["box"]

def in_table(u, v):
    return TABLE[0] <= u <= TABLE[2] and TABLE[1] <= v <= TABLE[3]

def robust(T, P):
    T, P = np.asarray(T, float), np.asarray(P, float)
    keep = np.ones(len(T), bool)
    for _ in range(4):
        c1, c0 = np.polyfit(T[keep], P[keep], 1)
        res = P - (c0 + c1 * T)
        mad = float(np.median(np.abs(res[keep] - np.median(res[keep])))) * 1.4826
        new = np.abs(res) <= max(1.5, 3 * mad)
        if (new == keep).all():
            break
        keep = new
    c1, c0 = np.polyfit(T[keep], P[keep], 1)
    return float(c1), float(c0), keep

def refit(line, kind):
    """kind 'v': u = c0 + c1 v (t = v); kind 'h': v = c0 + c1 u (t = u)."""
    samp = [(t, p) for t, p in line["samples"]
            if not (in_table(p, t) if kind == "v" else in_table(t, p))]
    c1, c0, _ = robust([s[0] for s in samp], [s[1] for s in samp])
    lo, hi = (v0, v1) if kind == "v" else (u0, u1)
    for _ in range(3):
        n = np.hypot(c1, 1.0)
        if kind == "v":
            e_t = np.array([c1, 1.0]) / n; e_s = np.array([1.0, -c1]) / n
        else:
            e_t = np.array([1.0, c1]) / n; e_s = np.array([-c1, 1.0]) / n
        T, P = [], []
        for t in np.arange(lo + 6, hi - 6, 10.0):
            pos = c0 + c1 * t
            u, v = (pos, t) if kind == "v" else (t, pos)
            if in_table(u, v):
                continue
            off = ca.ink_offset(gray, np.array([u, v]), e_s, e_t)
            if off is None:
                continue
            q = np.array([u, v]) + off * e_s
            T.append(q[1] if kind == "v" else q[0]); P.append(q[0] if kind == "v" else q[1])
        c1, c0, keep = robust(T, P)
    T, P = np.array(T), np.array(P)
    rms = float(np.sqrt(np.mean((P[keep] - (c0 + c1 * T[keep])) ** 2)))
    return c1, c0, [[round(float(a), 1), round(float(b), 2)] for a, b in zip(T[keep], P[keep])], int(keep.sum()), len(T), rms

xdir, ydir = cal.get("x_direction", "right"), cal.get("y_direction", "up")
vkey = "y_value" if xdir in ("up", "down") else "x_value"
hkey = "x_value" if vkey == "y_value" else "y_value"
vl, hl = [], []
for l in cal["vertical_lines"]:
    c1, c0, s, nk, nt, rms = refit(l, "v")
    vl.append((l[vkey], c1, c0, f"refit on ink outside the table: {nk}/{nt} positions, rms {rms:.2f} px", s))
    print(f"vertical   {vkey[0]}={l[vkey]:>6g}  u = {c0:.1f} {c1:+.4f} v  (detect: {l['u_at_v0']:.1f} {l['slope_du_dv']:+.4f} v)  kept {nk}/{nt}, rms {rms:.2f}")
for l in cal["horizontal_lines"]:
    c1, c0, s, nk, nt, rms = refit(l, "h")
    hl.append((l[hkey], c1, c0, f"refit on ink outside the table: {nk}/{nt} positions, rms {rms:.2f} px", s))
    print(f"horizontal {hkey[0]}={l[hkey]:>6g}  v = {c0:.1f} {c1:+.4f} u  (detect: {l['v_at_u0']:.1f} {l['slope_dv_du']:+.4f} u)  kept {nk}/{nt}, rms {rms:.2f}")

# Anchors: the intersections of the refitted lines where both are printed, i.e. outside the table
# (an intersection inside the table is a crossing of two lines the page does not draw there). A vertical
# line that crosses the table has only the 9.0 mm line above it, which would leave its ink check (positions
# between anchors) without support above the table: it also gets two one-axis anchors on its own ink
# above the table, the measured samples nearest v = 1195 and 1225 (between the 9.0 line and the table).
anchors, dropped = [], 0
for h in hl:
    for v in vl:
        u, vv = ca.intersect(h, v)
        if in_table(u, vv):
            dropped += 1
            continue
        xl, yl = (h, v) if hkey == "x_value" else (v, h)
        anchors.append({"x_value": xl[0], "y_value": yl[0], "u": round(u, 1), "v": round(vv, 1),
                        "x_source": xl[3], "y_source": yl[3]})
extra = 0
for l in vl:
    T = np.array([a for a, _ in l[4]]); P = np.array([b for _, b in l[4]])
    above = (T > 1180) & (T < TABLE[1])
    crosses = TABLE[0] <= l[2] + l[1] * (TABLE[1] + TABLE[3]) / 2 <= TABLE[2]
    if not crosses or above.sum() < 2:
        continue
    for target in (1195, 1225):
        i = int(np.argmin(np.where(above, np.abs(T - target), 1e9)))
        rec = {"x_value": "", "y_value": "", "u": round(float(P[i]), 1), "v": round(float(T[i]), 1), "x_source": "", "y_source": ""}
        rec[vkey] = l[0]; rec[vkey[0] + "_source"] = "ink sample above the table (one-axis anchor)"
        anchors.append(rec); extra += 1
print(f"{dropped} intersections inside the table left out; {extra} one-axis anchors on the ink above the table")
tx, ty = cal.get("x_transform", "linear"), cal.get("y_transform", "linear")
ax, ay, rmsx, rmsy, maxx, maxy = ca.fit_affine([a for a in anchors if a["x_value"] != "" and a["y_value"] != ""], tx, ty)
out_dir.mkdir(parents=True, exist_ok=True)
with (out_dir / "anchors.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["x_value", "y_value", "u", "v", "x_source", "y_source"], lineterminator="\n")
    w.writeheader(); w.writerows(anchors)
new = dict(cal)
new.update({"ax": ax, "ay": ay, "x_per_px": float(np.hypot(ax[0], ax[1])), "y_per_px": float(np.hypot(ay[0], ay[1])),
            "rms_residual_x": rmsx, "rms_residual_y": rmsy, "max_residual_x": maxx, "max_residual_y": maxy,
            "n_anchors": len(anchors), "anchors_note": "intersections inside the table left out; one-axis anchors (one value empty) are ink samples of the 50 to 20 percent lines above the table; the affine fit uses the two-value anchors",
            "vertical_lines": [{vkey: l[0], "slope_du_dv": l[1], "u_at_v0": l[2], "source": l[3], "samples": l[4]} for l in vl],
            "horizontal_lines": [{hkey: l[0], "slope_dv_du": l[1], "v_at_u0": l[2], "source": l[3], "samples": l[4]} for l in hl],
            "refit": "lines located by calibrate_axes.py detect (box, values, directions and transform as recorded here), "
                     "then refitted on the ink outside the Grain Size Parameters table by out/FA-38/refit_lines.py "
                     f"(table excluded: u {TABLE[0]}..{TABLE[2]}, v {TABLE[1]}..{TABLE[3]}); detect's own output is kept in cal-p1-detect/"})
(out_dir / "calibration.json").write_text(json.dumps(new, indent=1), encoding="utf-8")
print(f"{len(anchors)} anchors; x rms residual {rmsx:.5f} (max {maxx:.5f}) in log10 units; y rms {rmsy:.3f} (max {maxy:.3f})")
