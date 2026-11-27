"""For each 5% value: column of the constant-y line near the band, and the column runs at offsets."""
import sys, json
sys.argv = sys.argv[:1] + sys.argv[1:]
from geom import u_for_y
from common import g, grid_at, runs_col
m = json.load(open("centers_col.json"))
ys = [int(a) for a in sys.argv[1].split(",")]
offs = [int(a) for a in (sys.argv[2].split(",") if len(sys.argv) > 2 else "-6,-4,-2,0,2,4,6".split(","))]
for y in ys:
    u = 2000.0
    for _ in range(4):
        vB = m[str(int(round(u)))]["B"] if str(int(round(u))) in m else 1800
        u = u_for_y(y, vB)
    ui = int(round(u)); mm = m.get(str(ui)) or m[min(m, key=lambda k: abs(int(k) - ui))]
    print(f"=== y={y} u={u:.1f} model C={mm['C']:.1f} B={mm['B']:.1f} A={mm['A']:.1f} Cp={mm['Cp']} Ap={mm['Ap']}")
    lo, hi = int(mm["Tf"]) - 15, int(mm["Bf"]) + 15
    for o in offs:
        uu = ui + o
        rr = runs_col(uu, lo, hi)
        txt = []
        for a, b in rr:
            gg = [grid_at(v, uu) for v in range(a, b + 1)]
            tag = "g" if all(gg) else ("*" if any(gg) else "")
            txt.append(f"{a}-{b}{tag}")
        print(f"  u={uu}: " + " ".join(txt))
