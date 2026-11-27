"""Assemble points-p1.csv for FC-23 from samples/<name>.json (trace samples, end features) and the
reader's label centres. Pixel coordinates are page pixels of p0159.png (300 dpi, unrotated)."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
SERIES = [("rc2", "RC2"), ("ps", "PS"), ("rs", "RS"), ("rsmb", "RSM-b"), ("rsma", "RSM-a"), ("ss", "SS")]
SID = {"rc2": "rc2", "ps": "ps", "rs": "rs", "rsmb": "rsm-b", "rsma": "rsm-a", "ss": "ss"}
STYLE = {"rc2": "solid line", "ps": "short dashes", "rs": "medium dashes", "rsmb": "long dash and two short dashes",
         "rsma": "long dashes with medium dashes between", "ss": "solid line"}
# label centres: the middle of the printed text's bounding box (read on zoomed crops)
LABELS = {"rc2": (1633, 1894, "RC2"), "ps": (1662, 2007, "PS"), "rs": (1361.5, 2218, "RS"),
          "rsmb": (1209, 2410.5, "RSM-b"), "rsma": (1786.5, 2240, "RSM-a"), "ss": (1789.5, 2650, "SS")}
U_BOUND = 4.0    # half the line thickness across the line (8 px)
NAMES = {"rc2": "RC2", "ps": "PS", "rs": "RS", "rsmb": "RSM-b", "rsma": "RSM-a", "ss": "SS", "hgrid": "a horizontal grid line"}
EXTRA = {   # reader's notes on particular samples, keyed (series, dr or 'L'/'R')
    ("rc2", 0.05): "PS in a gap here",
    ("rc2", 0.1): "RC2 and PS cross here (u about 1094); the two lines coincide, centre of the joint ink",
    ("ps", 0.1): "RC2 and PS cross here (u about 1094); the two lines coincide, centre of the joint ink",
    ("ps", 0.05): "dash start touching RC2 below it; centre from the top edge",
    ("ps", 0.95): "PS dash; the RS dash that crosses PS starts about 3 px to the right",
    ("ps", 1.0): "RS crosses PS near u 2430 and lies just above here",
    ("rs", 0.6): "RS and RSM-b overlap here (RSM-b crosses RS near u 1850 in a gap of RS); RS centre from the bottom edge of the joint ink",
    ("rsmb", 0.6): "RS and RSM-b overlap here (RSM-b crosses RS near u 1850 in a gap of RS); RSM-b centre from the top edge of the joint ink",
    ("rs", 0.95): "RS dash start inside the PS ink: RS and PS cross near u 2430 and their ink cannot be separated here; wide bound",
    ("rs", "L"): "ink runs into the left frame (frame at u about 792); the end is cut by the frame",
    ("rs", "R"): "ends about 3 px short of the right frame",
    ("ps", "R"): "runs into the right frame",
    ("rsma", "R"): "runs into the right frame",
    ("ps", "L"): "starts just above the start of RC2",
    ("rc2", "L"): "starts just below the start of PS",
    ("rsmb", 0.15): "on the 40 deg grid line, just below the printed label RSM-b",
}


def fmt_note(n, p):
    how = p["how"]
    near = [NAMES.get(x, x) for x in p.get("near", [])]
    parts = []
    if "dr" in p:
        parts.append(f"Dr {p['dr']:.2f} sampling column u {p['u_target']}")
    if how == "ink":
        parts.append("on the ink")
    elif how == "grid-crossing":
        parts.append("on a vertical grid line: centre from the line's ink within 15 px either side")
    elif how.startswith("dash end at grid line"):
        parts.append(f"dash ends at the vertical grid line: moved {p['moved_px']:+d} px to the dash end on the ink (rule 7)")
    elif how.startswith("gap"):
        parts.append(f"in a gap between dashes: moved {p['moved_px']:+d} px to the nearest dash end on the ink (rule 7)")
    elif how == "top-edge":
        parts.append("ink joined with another line below: centre from the top edge plus half the line thickness")
    elif how == "bottom-edge":
        parts.append("ink joined with another line above: centre from the bottom edge minus half the line thickness")
    elif how == "coincident":
        parts.append("this line and another coincide here: centre of the joint ink")
    elif how in ("left end", "right end"):
        parts.append(f"{how}: where the line's ink {'starts' if how == 'left end' else 'ends'}")
    else:
        parts.append(how)
    if near and how not in ("ink",):
        parts.append("near " + ", ".join(near))
    elif near:
        parts.append("close to " + ", ".join(near))
    key = (n, p["dr"]) if "dr" in p else (n, "L" if how == "left end" else "R")
    if key in EXTRA:
        parts.append(EXTRA[key])
    return "; ".join(parts)


rows = []
for n, label in SERIES:
    s = json.loads((OUT / "samples" / f"{n}.json").read_text())
    for i, p in enumerate(s, 1):
        note = fmt_note(n, p)
        if i == 1:
            note += f"; line style: {STYLE[n]}"
        rows.append({"figure_id": "FC-23", "panel": 1, "series_id": SID[n], "point_kind": "trace", "sequence": i,
                     "pixel_u": p["u"], "pixel_v": round(p["v"], 1), "u_bound_px": U_BOUND, "v_bound_px": round(p["vb"], 1),
                     "symbol": "", "note": note})
    first, last = s[0], s[-1]
    rows.append({"figure_id": "FC-23", "panel": 1, "series_id": SID[n], "point_kind": "feature", "sequence": 1,
                 "pixel_u": first["u"], "pixel_v": round(first["v"], 1), "u_bound_px": U_BOUND, "v_bound_px": round(first["vb"], 1),
                 "symbol": "", "note": "first point (left end of the line's ink)" + ("; " + EXTRA[(n, "L")] if (n, "L") in EXTRA else "")})
    rows.append({"figure_id": "FC-23", "panel": 1, "series_id": SID[n], "point_kind": "feature", "sequence": 2,
                 "pixel_u": last["u"], "pixel_v": round(last["v"], 1), "u_bound_px": U_BOUND, "v_bound_px": round(last["vb"], 1),
                 "symbol": "", "note": "last point (right end of the line's ink); also the maximum of the trace, which rises monotonically" + ("; " + EXTRA[(n, "R")] if (n, "R") in EXTRA else "")})
    lu, lv, text = LABELS[n]
    rows.append({"figure_id": "FC-23", "panel": 1, "series_id": SID[n], "point_kind": "feature", "sequence": 3,
                 "pixel_u": lu, "pixel_v": lv, "u_bound_px": 5, "v_bound_px": 5, "symbol": "",
                 "note": f"label: {text}"})

cols = ["figure_id", "panel", "series_id", "point_kind", "sequence", "pixel_u", "pixel_v", "u_bound_px", "v_bound_px", "symbol", "note"]
with (OUT / "points-p1.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print("wrote", OUT / "points-p1.csv", len(rows), "rows")
