"""Self-check in the spirit of D-031: every trace sample and feature has ink of its own line within 2 px
once the grid lines and the frame (bands of trace_lib.grid_mask, widened by 1 px) are removed."""
import csv, sys
sys.path.insert(0, "out/F2-48")
import numpy as np
from trace_lib import B, VL, HL, u_line, v_line, h_half, v_half, NV, NU
vv, uu = np.mgrid[0:NV, 0:NU]
gm = np.zeros_like(B)
for L in VL:
    gm |= np.abs(uu - u_line(L, vv)) <= v_half(L) + 1
for L in HL:
    gm |= np.abs(vv - v_line(L, uu)) <= h_half(L) + 1
rem = B & ~gm
bad = 0
for r in csv.DictReader(open("out/F2-48/points-p1.csv", encoding="utf-8")):
    u, v = float(r["pixel_u"]), float(r["pixel_v"])
    ui, vi = int(round(u)), int(round(v))
    win = rem[vi - 2:vi + 3, ui - 2:ui + 3]
    ok = win.any()
    if not ok:
        bad += 1
        print("NO OWN INK within 2 px:", r["series_id"], r["point_kind"], r["sequence"], u, v, r["note"][:60])
print("checked; samples without own ink:", bad)
