"""Cross-check of the provisional samples: the grid-aware edge measurement (edgetrack2.measure_at)
started from each tracer2 sample with the local slope of the tracer2 polyline. Writes crosscheck.json."""
import json
import numpy as np
import fa22lib as L
import edgetrack2 as E
d = json.loads((L.OUT / "helpers" / "tracer2-out.json").read_text(encoding="utf-8"))
out = {}
for s, lst in d.items():
    res = []
    for i, m in enumerate(lst):
        a = lst[max(i - 1, 0)]; b = lst[min(i + 1, len(lst) - 1)]
        slope = (b["u"] - a["u"]) / (b["v"] - a["v"]) if b["v"] != a["v"] else 0.5
        u, w, n, kind = E.measure_at(m["v"], m["u"], slope, tol=5.0)
        diff = None if u is None else u - m["u"]
        res.append({"e": m["e"], "v": m["v"], "u_tr": m["u"], "u_edge": u, "w": w, "n": n, "kind": kind, "slope": slope, "diff": diff})
        flag = "" if (diff is not None and abs(diff) <= 1.5 and kind.startswith("ok")) else "  <-- check"
        print(f"{s:8s} {m['e']:+.2f} v {m['v']:7.1f} tr {m['u']:7.1f} edge {('%.1f' % u) if u is not None else '  -  '} "
              f"w {('%.1f' % w) if w is not None else '-'} n {n:2d} {kind:10s} s {slope:+.2f}{flag}")
    out[s] = res
(L.OUT / "helpers" / "crosscheck.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
