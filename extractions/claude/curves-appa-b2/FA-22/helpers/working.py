"""Working table of trace samples: tracer2/edge values merged with the reader's by-eye decisions
(OVERRIDE, in page pixels, from the check tiles and pixel rows). Writes working.json. Samples above
the merge region (log >= +0.70 for average/lower, >= +0.75 for upper) are left to manual reading."""
import json
import fa22lib as L
cc = json.loads((L.OUT / "helpers" / "crosscheck.json").read_text(encoding="utf-8"))
# by-eye decisions on the flagged samples (u in page px); None = handle manually (symbol, gap, merge)
OVERRIDE = {
 "average": {-0.95: 2009.6, -0.90: 1988.0, -0.80: 1943.5, -0.75: 1920.3, -0.70: 1895.5, -0.65: 1869.5,
             -0.50: 1790.5, -0.40: 1735.5, -0.10: 1565.0, -0.05: 1536.0, 0.05: 1476.0, 0.15: 1412.0,
             0.20: 1380.0, 0.25: 1345.0, 0.60: 962.0, 0.65: 897.0, -0.60: None, -0.85: None},
 "upper": {-0.75: 1789.5, -0.70: 1764.0, -0.15: 1387.5, 0.10: 1222.5, 0.15: 1189.0, 0.60: 849.0,
           -0.85: None, -0.60: None, 0.00: None},
 "lower": {-1.00: 2072.0, -0.40: 1841.0, -0.35: 1821.0, -0.25: 1778.5, -0.10: 1709.0, -0.05: 1683.0,
           0.05: 1629.0, 0.25: 1481.0, 0.30: 1437.5, 0.45: 1265.0, 0.55: 1115.0, 0.60: 1033.0, 0.65: 941.0,
           -1.10: None, -0.85: None, -0.80: None, -0.75: None, -0.60: None, -0.50: None, -0.45: None},
}
LIMIT = {"upper": 0.70, "average": 0.65, "lower": 0.65}
out = {}
for s, lst in cc.items():
    res = []
    for m in lst:
        if m["e"] > LIMIT[s] + 1e-9:
            continue
        ov = OVERRIDE[s].get(round(m["e"], 2), "none")
        if ov is None:
            u, src = None, "manual"
        elif ov != "none":
            u, src = ov, "eye"
        else:
            ok = m["u_edge"] is not None and abs(m["diff"]) <= 1.5 and m["kind"].startswith("ok")
            u, src = ((m["u_edge"] + m["u_tr"]) / 2, "auto") if ok else (m["u_tr"], "tracer-unchecked")
        res.append({"e": m["e"], "v": m["v"], "u": u, "src": src})
    out[s] = res
(L.OUT / "helpers" / "working.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
for s, r in out.items():
    print(s, len(r), [x["e"] for x in r if x["src"] in ("manual", "tracer-unchecked")])
