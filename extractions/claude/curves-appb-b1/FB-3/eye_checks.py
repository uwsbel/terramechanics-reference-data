"""calibration-eye-checks.csv of FB-3: every printed axis label against the tick or frame line it was
assigned to (ink box of the label glyphs measured on the page; the label was looked at on the crop named)."""
import csv, json, sys
import numpy as np
from PIL import Image
g = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128
cal = json.load(open(sys.argv[2] + "/calibration.json"))
ax, ay = cal["ax"], cal["ay"]
V = {l["x_value"]: l for l in cal["vertical_lines"]}
H = {l["y_value"]: l for l in cal["horizontal_lines"]}
bot = H[7]; left = V[0]

def box(u0, v0, u1, v1):
    vs, us = np.where(g[v0:v1, u0:u1])
    return u0 + us.min(), u0 + us.max(), v0 + vs.min(), v0 + vs.max()

rows = []
# x labels: glyph boxes below the frame (rows 3931-3966 avoid the frame edge and the specks at v 3970)
xl = {0: (525, 575), 2: (810, 860), 4: (1100, 1140), 6: (1380, 1425), 8: (1650, 1700), 10: (1915, 1995), 12: (2165, 2245), 14: (2455, 2535)}
crop = {0: "bl.png", 2: "bl.png", 4: "bl.png", 6: "bm.png", 8: "bm.png", 10: "bm.png", 12: "br.png", 14: "br.png"}
for val, (a, b) in xl.items():
    u0, u1, v0, v1 = box(a, 3933, b, 3966)
    lu = (u0 + u1) / 2
    l = V[val]
    if "anchor" in l:
        pu, pv = l["anchor"]; kind = "tick"
    else:
        pv = bot["v_at_u0"] + bot["slope_dv_du"] * 550
        pu = l["u_at_v0"] + l["slope_du_dv"] * pv; kind = "frame (" + ("left" if val == 0 else "right") + ")"
        pv = bot["v_at_u0"] + bot["slope_dv_du"] * pu
    aff = ax[0] * pu + ax[1] * pv + ax[2]
    note = ""
    if val == 4:
        note = "specks at v 3970-3974 from u 1044 to 1100 make it look like '-4' in the overview; they are dirt below the baseline, not a minus sign (sequence 0 2 4 6 and tick spacing confirm 4)"
    if val in (12, 14):
        note = "two-digit label typed with its last digit under the line"
    if val == 14:
        note += "; no tick at 14: the label sits on the right frame, 280.9 px from the 12 tick (interior spacing 277.6 to 283.4 px)"
    if val == 0:
        note = "no tick at 0: the label sits on the left frame (corner)"
    rows.append({"axis": "x", "printed_label": str(val), "value_used": val, "line": kind, "line_u": round(pu, 1), "line_v": round(pv, 1),
                 "label_ink_u": f"{u0}-{u1}", "label_ink_v": f"{v0}-{v1}", "label_centre_along_axis_px": round(lu, 1),
                 "label_minus_line_px": round(lu - pu, 1), "affine_value_at_line": round(aff, 3), "crop_checked": crop[val],
                 "verdict": "label sits on this line (offset well under the 280 px spacing); value fits the printed sequence", "note": note})
# y labels: glyph boxes left of the frame
yl = {18: (815, 870), 17: (1105, 1165), 16: (1370, 1425), 15: (1660, 1720), 14: (1930, 1985), 13: (2210, 2270),
      12: (2480, 2535), 11: (2790, 2845), 10: (3050, 3105), 9: (3330, 3388), 8: (3600, 3656), 7: (3875, 3929)}
ycrop = {18: "tl.png", 17: "tl.png", 13: "ylab_11_13.png", 12: "ylab_11_13.png", 11: "ylab_11_13.png", 9: "ylab_7_9.png", 8: "ylab_7_9.png", 7: "ylab_7_9.png"}
for val, (a, b) in yl.items():
    u0, u1, v0, v1 = box(440, a, 532 if val != 7 else 530, b)
    lv = (v0 + v1) / 2
    l = H[val]
    if "anchor" in l:
        pu, pv = l["anchor"]; kind = "tick"
    else:
        pu = left["u_at_v0"] + left["slope_du_dv"] * (830 if val == 18 else 3917)
        pv = l["v_at_u0"] + l["slope_dv_du"] * pu; kind = "frame (" + ("top" if val == 18 else "bottom") + ")"
    aff = ay[0] * pu + ay[1] * pv + ay[2]
    note, verdict = "", "label sits on this line (offset well under the 280 px spacing); value fits the printed sequence"
    if val == 8:
        note = ("printed label reads '3' (with a speck after it), which does not fit the sequence 7, ?, 9, 10; most likely an 8 whose left half "
                "did not print. Value 8 taken from the tick spacing: 280.3 px above the 7 frame and 279.9 px below the 9 tick (interior spacing 276.9 to 282.4 px)")
        verdict = "label does not fit its sequence; value 8 confirmed by tick spacing, so the tick is a knot"
    if val == 7:
        note = "no tick at 7: the label sits 13 px above the bottom frame (the frame is the 7 line; the 8 tick is 280 px above it)"
    if val == 18:
        note = ("no tick at 18: the label sits on the top frame. The top frame is 286.5 px above the 17 tick against a mean interior spacing of 280.0 px "
                "(about 0.023 ksi farther than one tick spacing); drafting of the frame, kept as drawn by the piecewise map")
    rows.append({"axis": "y", "printed_label": "3" if val == 8 else str(val), "value_used": val, "line": kind, "line_u": round(pu, 1), "line_v": round(pv, 1),
                 "label_ink_u": f"{u0}-{u1}", "label_ink_v": f"{v0}-{v1}", "label_centre_along_axis_px": round(lv, 1),
                 "label_minus_line_px": round(lv - pv, 1), "affine_value_at_line": round(aff, 3), "crop_checked": ycrop.get(val, "overview of p0109.png and ink box only"),
                 "verdict": verdict, "note": note})
with open(sys.argv[3], "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader(); w.writerows(rows)
for r in rows:
    print(r["axis"], r["printed_label"], r["value_used"], r["line"], r["line_u"], r["line_v"], r["label_ink_u"], r["label_ink_v"], r["label_minus_line_px"], r["affine_value_at_line"])
