"""For each working sample: is there stroke ink at the sample? Counts ink pixels (vertical grid ink
excluded) within u +-6 in rows v-1..v+1; where those rows lie on a horizontal grid line, the nearest
rows above and below the grid line are counted instead (reported as 'above/below')."""
import json
import numpy as np
import fa22lib as L
INK = L.page() < 128
VL = np.load(L.OUT / "helpers" / "vline.npy"); HL = np.load(L.OUT / "helpers" / "hline.npy")
wk = json.loads((L.OUT / "helpers" / "working.json").read_text(encoding="utf-8"))
def count(r, u):
    a, b = int(round(u)) - 6, int(round(u)) + 7
    return int((INK[r, a:b] & ~VL[r, a:b]).sum()), float(HL[r, a:b].mean())
for s in ("upper", "lower", "average"):
    for m in wk[s]:
        if m["u"] is None: continue
        v = int(round(m["v"])); u = m["u"]
        cs = [count(r, u) for r in (v - 1, v, v + 1)]
        on_grid = all(h > 0.5 for _, h in cs)
        if on_grid:
            up = v - 2
            while HL[up, int(u) - 6:int(u) + 7].mean() > 0.5: up -= 1
            dn = v + 2
            while HL[dn, int(u) - 6:int(u) + 7].mean() > 0.5: dn += 1
            a, _ = count(up, u - 0.5 * (v - up)); b, _ = count(dn, u + 0.5 * (dn - v))
            msg = f"on grid line rows {up+1}..{dn-1}: ink above {a} below {b}"
            flag = "" if (a >= 4 and b >= 4) else "  <-- gap at grid line?"
        else:
            n = sum(c for c, h in cs if h <= 0.5)
            msg = f"ink {n}"
            flag = "" if n >= 8 else "  <-- gap?"
        if flag or s != "average":
            if flag: print(f"{s:8s} {m['e']:+.2f} v {m['v']:.0f} u {u:.1f} {msg}{flag}")
