"""Build out/FC-5A/points-p1.csv for Figure C-5A from the readings recorded below.

Markers and label positions were read by eye on zoomed crops and ASCII dumps of the page
(crops2/, dump.py, ring.py, comps.py). Trace samples are measured here: for each sample of normal
stress (every 250 psf) the column u is found from the calibration and the line's straight fit
(linefit.json, fitted on the line's own ink), then the line's center in that column is
  - 'run'    the center of the dark run of that column (clean line ink), or
  - 'interp' a local straight fit of clean run centers within 30 px on either side, where the
             column itself is crossed by a grid line (its ink merges with the line), or
  - 'fit'    the line's straight fit, only at 250 psf where the four lines merge into one band.
Samples whose column meets a symbol (its outer box) or a white gap are not written; notes.md lists
them. usage: build_points.py image calibration.json linefit.json out.csv"""
import sys, json, csv
import numpy as np
from PIL import Image

g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
cal = json.load(open(sys.argv[2])); L = json.load(open(sys.argv[3])); out = sys.argv[4]
ax = cal["ax"]
FIG = "FC-5A"

SERIES = {"L1_41.5": "dr77", "L2_36.9": "dr48", "L3_32.8": "dr30", "L4_29": "dr2-13"}
HALF = {"L1_41.5": 7.5, "L2_36.9": 6.5, "L3_32.8": 6.0, "L4_29": 6.0}   # half the nominal vertical run

MERGED = "four lines merge into one band (v 2959 to 3000) at this column; center from the line's straight fit"
# sample plan: sigma -> (mode, note)
PLAN = {
 "L1_41.5": {250: ("fit", MERGED + ", which matches the band's upper edge"),
             500: ("run", ""), 1000: ("interp", "at the 1000 psf grid line"), 1500: ("run", ""),
             2000: ("interp", "at the 2000 psf grid line"),
             2250: ("interp", "crosses the 2000 psf horizontal grid line here"),
             2750: ("run", "")},
 "L2_36.9": {250: ("fit", MERGED),
             500: ("run", ""), 1000: ("interp", "at the 1000 psf grid line"),
             1250: ("run", "on the line's ink about 4 px left of the triangle-down at about 1300 psf, whose top-left corner the line enters"),
             1500: ("run", ""), 1750: ("run", ""), 2250: ("run", ""), 2750: ("run", ""),
             3000: ("interp", "at the 3000 psf grid line"),
             3250: ("run", ""), 3500: ("run", ""), 3750: ("run", "")},
 "L3_32.8": {250: ("fit", MERGED),
             500: ("run", ""), 1000: ("interp", "at the 1000 psf grid line"), 1250: ("run", ""),
             1500: ("interp", "crosses the 1000 psf horizontal grid line here"),
             2000: ("interp", "at the 2000 psf grid line"),
             2250: ("run", ""), 2750: ("run", ""),
             3000: ("interp", "at the 3000 psf grid line, just below the 2000 psf horizontal line"),
             3250: ("run", ""), 3500: ("run", ""), 3750: ("run", ""),
             4000: ("run", "next to the 4000 psf grid line (left of its ink)"),
             4250: ("run", ""), 4500: ("run", "")},
 "L4_29":   {250: ("fit", MERGED + ", which matches the band's lower edge"),
             500: ("run", ""), 1000: ("interp", "at the 1000 psf grid line"), 1250: ("run", ""),
             1500: ("run", ""), 2000: ("interp", "at the 2000 psf grid line"), 2250: ("run", ""),
             2500: ("run", ""), 2750: ("run", ""),
             3000: ("interp", "at the 3000 psf grid line; the line's ink resumes at the grid line after its gap around the circle at 2910 psf, so only ink on the right is used"),
             3250: ("run", ""), 3500: ("interp", "crosses the 2000 psf horizontal grid line here"),
             4000: ("interp", "at the 4000 psf grid line"), 4250: ("run", ""), 4500: ("run", "")},
}
# right ends (u, v or None for the fit, note) read on the dumps; left ends at the origin corner
RIGHT = {"L1_41.5": (1680, None, "right end of the line's ink"),
         "L2_36.9": (1966, None, "right end of the line's ink"),
         "L3_32.8": (2154, None, "right end of the line's ink, just below the 3000 psf horizontal grid line"),
         "L4_29":   (2280, 2197.0, "dashed; right end where the second dash meets the right frame (5000 psf line)")}
U_LEFT = 825   # first column right of the sigma = 0 frame line's ink near the corner


def runs(u, v0, v1):
    col = g[v0:v1, u]; idx = np.where(col)[0]; res = []
    if len(idx):
        s = p = idx[0]
        for i in idx[1:]:
            if i != p + 1:
                res.append((s + v0, p + v0)); s = i
            p = i
        res.append((s + v0, p + v0))
    return res


def run_center(name, u):
    a, b = L[name]["a"], L[name]["b"]; vp = a * u + b
    for t, bb in runs(u, int(vp) - 25, int(vp) + 25):
        if t - 1 <= vp <= bb + 1:
            return (t + bb) / 2, bb - t + 1
    return None, None


def clean_center(name, u):
    nom = L[name]["median_run"]; a, b = L[name]["a"], L[name]["b"]
    c, ln = run_center(name, u)
    if c is not None and abs(ln - nom) <= 2 and abs(c - (a * u + b)) <= 3:
        return c
    return None


def interp(name, uc):
    us, vs = [], []
    for u in range(uc - 30, uc + 31):
        if abs(u - uc) < 8:
            continue
        c = clean_center(name, u)
        if c is not None:
            us.append(u); vs.append(c)
    k = np.polyfit(us, vs, 1)
    left = sum(1 for u in us if u < uc); right = len(us) - left
    return float(np.polyval(k, uc)), left, right


rows = []


def add(series, kind, seq, u, v, bu, bv, sym, note):
    rows.append(dict(figure_id=FIG, panel=1, series_id=series, point_kind=kind, sequence=seq,
                     pixel_u=round(u, 1), pixel_v=round(v, 1), u_bound_px=bu, v_bound_px=bv,
                     symbol=sym, note=note))


# ---- markers (read by eye, see notes.md) ----
M = {
 "dr77": ("triangle-up", [
   (910.5, 2929.0, 2, 6, "centroid; lowest normal stress of the figure; about 22 px above the 41.5 deg line, base and lower right merged with the converging lines"),
   (1024.5, 2840.0, 3, 6, "centroid; top of the stacked group at about 700 psf (triangle-up over triangle-down over square); right side merged with the 41.5 deg line"),
   (1200.5, 2709.8, 2, 6, "centroid; apex on the 41.5 deg line, triangle below it"),
   (1343.0, 2577.0, 2, 6, "centroid; apex merged with the 41.5 deg line; base stacked on the top side of the triangle-down below (hourglass)"),
   (1543.5, 2393.5, 2, 6, "centroid; on the 41.5 deg line (right side merged with it)")]),
 "dr48": ("triangle-down", [
   (1024.5, 2864.0, 3, 6, "centroid; middle of the stacked group at about 700 psf, between the triangle-up above and the square below; apex reaches into the square's top side"),
   (1207.0, 2745.2, 2, 6, "centroid; top side lies on the 1000 psf horizontal grid line; apex touches the square below"),
   (1344.5, 2601.0, 2, 6, "centroid; sits between the 41.5 deg and 36.9 deg lines, about 34 px from each; series by shape (rule 9); top side stacked on the triangle-up above"),
   (1546.5, 2487.7, 2, 6, "centroid; on the 36.9 deg line (line broken inside the symbol)"),
   (1897.5, 2242.5, 2, 6, "centroid; about 21 px below the 36.9 deg line, which crosses its top-left corner")]),
 "dr30": ("square", [
   (1025.3, 2889.8, 3, 4, "bottom of the stacked group at about 700 psf; top side merged with the triangle-down's apex and the 36.9 deg line; 32.8 deg line broken around it"),
   (1209.3, 2775.5, 2, 2, "on the 32.8 deg line; top side touches the triangle-down above"),
   (1348.3, 2703.0, 2, 3, "about 20 px below the 32.8 deg line (which crosses its top-left corner) and about 30 px above the 29 deg line"),
   (1548.3, 2553.5, 2, 2, "on the 32.8 deg line (line broken inside the symbol)"),
   (2011.0, 2244.5, 2, 2, "on the 32.8 deg line, just right of the 4000 psf grid line")]),
 "dr2-13": ("circle", [
   (1037.5, 2779.5, 2, 2, "isolated, far above all four lines (about 130 px above the 29 deg line, 60 px above the 41.5 deg line); not on its group's line"),
   (1328.0, 2739.0, 2, 3, "the 1000 psf horizontal grid line crosses it; in a gap of the 29 deg line"),
   (1674.5, 2561.5, 2, 2, "about 16 px below the 29 deg line, in a gap of it"),
   (1930.5, 2400.2, 2, 2, "on the 29 deg line, in a gap of it"),
   (2184.8, 2247.5, 2, 2, "on the 29 deg line in its last gap; the dashed part continues to the right")]),
}
for s, (sym, lst) in M.items():
    for i, (u, v, bu, bv, note) in enumerate(lst, 1):
        add(s, "marker", i, u, v, bu, bv, sym, note)

# ---- traces ----
for name, plan in PLAN.items():
    s = SERIES[name]; a, b = L[name]["a"], L[name]["b"]; h = HALF[name]; seq = 1
    add(s, "trace", seq, U_LEFT, a * U_LEFT + b, 3, 8, "",
        "left end at the origin corner: the four lines and the frame lines merge here; v from the line's straight fit")
    for sig in sorted(plan):
        mode, note = plan[sig]
        u = (sig - ax[2] - ax[1] * b) / (ax[0] + ax[1] * a); uc = int(round(u))
        if mode == "run":
            c, ln = run_center(name, uc)
            assert c is not None and abs(c - (a * uc + b)) <= 3, (name, sig, c)
            v, bv = c, h
            note = f"sigma {sig}" + (f"; {note}" if note else "")
        elif mode == "interp":
            v, nl, nr = interp(name, uc); bv = h
            note = f"sigma {sig}; {note}; center interpolated from clean line ink ({nl} columns left, {nr} right, within 30 px)"
        else:
            v, bv = a * uc + b, 8
            note = f"sigma {sig}; {note}"
        seq += 1
        add(s, "trace", seq, uc, v, 2, bv, "", note)
    ur, vr, note = RIGHT[name]
    if vr is None:
        vr = a * ur + b
    seq += 1
    add(s, "trace", seq, ur, vr, 3, h, "", note)

# ---- features ----
c0 = cal["vertical_lines"][0]["u_at_v0"]; c1 = cal["vertical_lines"][0]["slope_du_dv"]
LABELS = {"L1_41.5": (1593.5, 2292.5, "41.5", "text box u 1549-1638, v 2239-2346, above the line"),
          "L2_36.9": (1817.5, 2233.5, "36.9", "text box u 1768-1867, v 2181-2286, above the line"),
          "L3_32.8": (1832.0, 2316.5, "32.8", "text box u 1780-1884, v 2266-2367, between the 36.9 deg and 32.8 deg lines, baseline toward the 32.8 deg line"),
          "L4_29":   (2070.0, 2271.5, "29", "text box u 2036-2104, v 2236-2307, between the 32.8 deg and 29 deg lines, baseline toward the 29 deg line")}
for name in PLAN:
    s = SERIES[name]; a, b = L[name]["a"], L[name]["b"]
    ui = (c0 + c1 * b) / (1 - c1 * a); vi = a * ui + b
    add(s, "feature", 1, ui, vi, 3, 8, "",
        "intercept; the line's straight fit (its own ink, u 1000 to its right end) met with the sigma = 0 grid line; at the corner the four lines and the frame merge into one wedge (v 3012 to 3033), so the bound is wide")
    lu, lv, txt, box = LABELS[name]
    add(s, "feature", 2, lu, lv, 5, 5, "", f"label: {txt}°; center of the printed angle's text box ({box})")

cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v",
        "u_bound_px", "v_bound_px", "symbol", "note"]
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print(f"wrote {len(rows)} rows to {out}")
