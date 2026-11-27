"""Series assignment of the candidate blobs (by eye, from the zoomed crops), and a flag for every
blob that a grid line crosses or touches (its bbox may be truncated by the line removal)."""
import csv, json, sys
cal = json.load(open("out/FC-7B/cal-p1/calibration.json"))
assign = {
 "n27p1psi": [178,168,162,154,135,122,115,109,98,90,79,68,54,46,31,21,16,12],
 "n13p8psi": [179,169,166,150,137,124,117,110,100,91,80,70,56,48,32,22],
 "n10p2psi": [167,148,138,123,118,112,99,92,82,71,58,47,26],
 "n6p6psi":  [164,152,136,125,116,111,101,93,83,73,60,50,33,25],
 "n5p1psi":  [163,153,134,128,120,114,103,95,84,74,59,49,35],
 "n3p4psi":  [165,151,139,127,119,113,102,94,81,72,57,51,34],
}
c = {int(r["cid"]): r for r in csv.DictReader(open("out/FC-7B/helpers/candidates.csv"))}
for s, ids in assign.items():
    for i in ids:
        r = c[i]
        umin, umax, vmin, vmax = (float(r[k]) for k in ("umin", "umax", "vmin", "vmax"))
        flags = []
        for ln in cal["vertical_lines"]:
            uc = ln["u_at_v0"] + ln["slope_du_dv"] * (vmin + vmax) / 2
            if umin - 6 <= uc <= umax + 6:
                flags.append(f"Vline y={ln['y_value']:g} at u={uc:.1f}")
        for ln in cal["horizontal_lines"]:
            vc = ln["v_at_u0"] + ln["slope_dv_du"] * (umin + umax) / 2
            if vmin - 6 <= vc <= vmax + 6:
                flags.append(f"Hline x={ln['x_value']:g} at v={vc:.1f}")
        print(f"{s:9s} {i:4d} uc={float(r['uc']):7.1f} vc={float(r['vc']):7.1f} w={r['w']:>3s} h={r['h']:>3s}  {'; '.join(flags)}")
