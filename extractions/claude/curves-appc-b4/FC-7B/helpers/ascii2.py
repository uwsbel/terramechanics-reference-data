"""ASCII view of small windows; dark pixels inside a fitted grid-line band (+-4 px) are drawn
as '|' (vertical line) or '-' (horizontal line) so a symbol edge on a line can be judged."""
import sys, json
import numpy as np
from PIL import Image
g = np.asarray(Image.open("packet/p0136.png").convert("L"))
cal = json.load(open("out/FC-7B/cal-p1/calibration.json"))
for spec in sys.argv[1:]:
    name, box = spec.split(":")
    u0, v0, u1, v1 = map(int, box.split(","))
    print(f"== {name}  u {u0}..{u1-1}  v {v0}..{v1-1}")
    print("      " + "".join(str((u // 10) % 10) if u % 10 == 0 else " " for u in range(u0, u1)))
    print("      " + "".join(str(u % 10) for u in range(u0, u1)))
    for v in range(v0, v1):
        row = []
        for u in range(u0, u1):
            if g[v, u] >= 128:
                row.append(".")
                continue
            ch = "#"
            for ln in cal["vertical_lines"]:
                if abs(u - (ln["u_at_v0"] + ln["slope_du_dv"] * v)) <= 4:
                    ch = "|"
            for ln in cal["horizontal_lines"]:
                if abs(v - (ln["v_at_u0"] + ln["slope_dv_du"] * u)) <= 4:
                    ch = "-" if ch == "#" else "+"
            row.append(ch)
        print(f"{v:5d} " + "".join(row))
