"""Adjudication packet built from the canonical files of curves-appc-b1/b2 (and the pilot's new
one-sided curve-end samples): one crop per item with the readings drawn under neutral labels (P blue
circles, Q orange squares; which reader is P is shuffled per item and kept in a hidden key).

Items (kind):
  marker-disagree   a paired marker whose two positions disagree
  feature-disagree  a paired first/last point (or peak height) that disagrees
  trace-disagree    a trace sample that disagrees with the other trace
  identity          one symbol recorded under two different tests
  marker-only       a marker only one reader recorded
  feature-only      a feature only one reader recorded
  curve-start, curve-end, trace-gap   consecutive trace samples only one reader took (one item per run)
Usage: make_disputes.py <out_dir> <key_csv>
"""
import csv, random, sys
from collections import defaultdict, Counter
from pathlib import Path
from PIL import Image, ImageDraw
REPO = Path(r"<repository>")
sys.path.insert(0, str(REPO / "tools"))
import diff_curves as dc  # noqa: E402

OUT, KEYF = Path(sys.argv[1]), Path(sys.argv[2])
(OUT / "crops").mkdir(parents=True, exist_ok=True)
SETS = [("curves-appc-b1", f, "qa/curves-appc-b1/canonical-{f}-p{p}.csv") for f in ("FC-1C", "FC-1D", "FC-2B", "FC-2C")] + \
       [("curves-appc-b2", f, "qa/curves-appc-b2/canonical-{f}-p{p}.csv") for f in ("FC-3B", "FC-3C", "FC-4B", "FC-4C")] + \
       [("curves-pilot-b1", "FC-1B", sys.argv[3] + "/canonical-p{p}.csv" if len(sys.argv) > 3 else None)]
PAGES = {"FC-1B": 117, "FC-1C": 118, "FC-1D": 119, "FC-2B": 121, "FC-2C": 122, "FC-3B": 124, "FC-3C": 125, "FC-4B": 127, "FC-4C": 128}
READ = {"curves-pilot-b1": {"claude": {"1": "claude-fc1b-p1-traces-native.csv", "2": "claude-fc1b-p2-markers-native.csv"},
                            "codex": {"1": "points-p1-native.csv", "2": "points-p2-native.csv"}}}
rng = random.Random(20261013)
BLUE, ORANGE = (30, 90, 230), (240, 120, 0)
items, key = [], []


def load(p):
    return list(csv.DictReader(open(p, encoding="utf-8-sig", newline="")))


def draw(img, subj, ref, center, half, scale, name, lines):
    x0, y0 = int(center[0] - half), int(center[1] - half)
    c = img.crop((x0, y0, x0 + 2 * half, y0 + 2 * half)).convert("RGB")
    c = c.resize((c.width * scale, c.height * scale), Image.NEAREST)
    d = ImageDraw.Draw(c)
    for pts, col, shape in ((subj, BLUE, "circle"), (ref, ORANGE, "square")):
        prev = None
        for (u, v) in pts:
            X, Y = (u - x0) * scale, (v - y0) * scale
            r = (2 if lines else 4) * scale
            (d.ellipse if shape == "circle" else d.rectangle)([X - r, Y - r, X + r, Y + r], outline=col, width=2)
            if lines and prev:
                d.line([prev, (X, Y)], fill=col, width=1)
            prev = (X, Y)
    c.save(OUT / "crops" / name)


def add(kind, fid, panel, series, question, first, second, first_lab, second_lab, lines=False, extra=None, verify=""):
    """first: the subject points (one reader), second: the reference points (the other reader or rivals)."""
    iid = f"{len(items) + 1:03d}"
    swap = rng.random() < 0.5
    pl, ql = ("Q", "P") if swap else ("P", "Q")   # labels of first and second
    P, Q = (second, first) if swap else (first, second)
    q = question.replace("{S}", pl).replace("{R}", ql)
    pts = [x[:2] for x in first + second]
    us, vs = [p[0] for p in pts], [p[1] for p in pts]
    center = ((min(us) + max(us)) / 2, (min(vs) + max(vs)) / 2)
    half = int(max(60, (max(us) - min(us)) / 2 + 40, (max(vs) - min(vs)) / 2 + 40))
    scale = 4 if half <= 75 else 3 if half <= 110 else 2
    name = f"item-{iid}.png"
    # blue circles always mark P, orange squares Q
    draw(IMG[fid], [x[:2] for x in P], [x[:2] for x in Q], center, half, scale, name, lines)
    fmt = lambda L: "; ".join(f"px ({u:.0f},{v:.0f}) x {x:.1f} y {y:.1f}" + (f" [{t}]" if t else "") for u, v, x, y, t in L[:8]) + (" ..." if len(L) > 8 else "") if L else "(none)"
    items.append({"item": iid, "kind": kind, "figure": fid, "panel": panel, "series": series,
                  "legend_symbol": LEG[fid].get(series, ""), "question": q, "P": fmt(P), "Q": fmt(Q),
                  "crop": f"crops/{name}", "crop_origin_px": f"{int(center[0] - half)},{int(center[1] - half)}", "crop_scale": scale,
                  **(extra or {})})
    key.append({"subject_rows": ";".join(x.rid for x in first), "reference_rows": ";".join(x.rid for x in second),
                "item": iid, "P": second_lab if swap else first_lab, "Q": first_lab if swap else second_lab,
                "subject_label": pl, "subject_reader": first_lab, "verify": verify})


class Pt(tuple):
    """(u, v, x, y, tag) with the identity of the row it came from, for the key."""
    rid = ""


def pt(r, tag=""):
    t = Pt((float(r["pixel_u"]), float(r["pixel_v"]), float(r["x_native"]), float(r["y_native"]), tag))
    t.rid = f"{r.get('source') or r.get('_lab')}|{r['series_id']}|{r['point_kind']}|{r['sequence']}"
    return t


IMG, LEG = {}, {}
for batch, fid, pattern in SETS:
    if pattern is None:
        continue
    IMG[fid] = Image.open(REPO / f"corpus/1968-vol2/images/p{PAGES[fid]:04d}.png")
    LEG.setdefault(fid, {})
    for p in "12":
        files = READ.get(batch, {"claude": {p: f"{fid}/points-p{p}-native.csv"}, "codex": {p: f"{fid}/points-p{p}-native.csv"}})
        R = {lab: [r for r in load(REPO / "extractions" / lab / batch / files[lab][p]) if r["panel"] == p] for lab in ("claude", "codex")}
        for lab in R:
            for r in R[lab]:
                r["_lab"] = lab
        for lab in R:
            for r in R[lab]:
                if r["point_kind"] == "marker" and r["symbol"]:
                    LEG[fid].setdefault(r["series_id"], r["symbol"])
        can = load(REPO / pattern.format(f=fid, p=p) if not Path(pattern).is_absolute() else pattern.format(p=p))
        le = Counter(r["source"] for r in can).most_common(1)[0][0]
        if batch == "curves-pilot-b1":   # only the curve ends the new rule added to the pilot
            can = [r for r in can if r["source"] == "claude" and r["status"] == "one-sided"]
        bykey = {(lab, r["series_id"], r["point_kind"], r["sequence"]): r for lab in R for r in R[lab]}
        other_of = lambda lab: "codex" if lab == "claude" else "claude"
        series_rows = defaultdict(list)
        for r in can:
            series_rows[r["series_id"]].append(r)
        for s, rows in series_rows.items():
            for r in rows:
                kind, src, st = r["point_kind"], r["source"], r["status"]
                ol = other_of(src)
                if st == "pending-review" and kind in ("marker", "feature") and (r.get("decision_note") or "").startswith("rule: identity conflict"):
                    rivals = [x for x in R[ol] if x["point_kind"] == "marker" and x["series_id"] != s and dc.pixel_distance(x, r) <= 10]
                    same = [x for x in R[ol] if x["point_kind"] == "marker" and x["series_id"] == s and dc.pixel_distance(x, r) <= 45]
                    add("identity", fid, p, s,
                        f"One reader recorded the symbol at the {{S}} mark as a {r['symbol']} of {s}; the other recorded the same ink "
                        f"(the {{R}} mark) as " + ", ".join(f"a {x['symbol']} of {x['series_id']}" for x in rivals) +
                        ". Which is right? Answer with the series id whose symbol this is (look at the shape; the legend gives each test's symbol), "
                        "`both` if there are really two symbols here, or `cannot tell`.",
                        [pt(r, f"{s} {r['symbol']}")], [pt(x, f"{x['series_id']} {x['symbol']}") for x in rivals + same], src, ol,
                        extra={"candidates": "; ".join([f"{s} {r['symbol']}"] + [f"{x['series_id']} {x['symbol']}" for x in rivals])},
                        verify="identity")
                elif st == "pending-review" and kind in ("marker", "feature"):
                    o = next((x for x in R[ol] if x["series_id"] == s and x["point_kind"] == kind and x["x_native"] == r["other_x_native"]
                              and x["y_native"] == r["other_y_native"]), None)
                    if kind == "marker":
                        add("marker-disagree", fid, p, s,
                            f"Both readers placed a {r['symbol'] or LEG[fid].get(s, '')} of {s} here, at different centers. Which mark is on the "
                            "center of that symbol? `P`, `Q`, `both` (both inside the symbol), `neither`, `cannot tell`; say if the symbol is not this test's.",
                            [pt(r)], [pt(o)] if o else [], src, ol, verify="pair")
                    else:
                        role = dc.feature_role(r)
                        add("feature-disagree", fid, p, s,
                            f"The two readers' '{role}' point of the drawn {s} line differ (notes in note_P, note_Q). Which mark is the {role} "
                            f"point of the drawn line" + (" (its height matters; on a flat top its x does not)" if role == "peak" else "") +
                            "? `P`, `Q`, `both`, `neither`, `cannot tell`.",
                            [pt(r)], [pt(o)] if o else [], src, ol, extra={"_n1": r.get("note", ""), "_n2": (o or {}).get("note", "")}, verify="pair")
                elif st == "pending-review" and kind == "trace":
                    near = sorted([x for x in R[ol] if x["series_id"] == s and x["point_kind"] == "trace"],
                                  key=lambda x: abs(float(x["pixel_u"]) - float(r["pixel_u"])))[:4]
                    add("trace-disagree", fid, p, s, f"Which trace sample is on the drawn line of {s}: the {{S}} mark or the {{R}} line? `P`, `Q`, `both`, `neither`, `cannot tell`.",
                        [pt(r)], sorted([pt(x) for x in near]), src, ol, lines=True, verify="pair")
                elif st == "one-sided" and kind == "marker":
                    near = [x for x in R[ol] if x["point_kind"] == "marker" and dc.pixel_distance(x, r) <= 45]
                    add("marker-only", fid, p, s,
                        f"Only one reader recorded a {r['symbol'] or LEG[fid].get(s, '')} of {s} at the {{S}} mark (the other reader's marks within "
                        "45 px are drawn as {R}, whatever their test). Is there a printed symbol of this test there, centered within a few pixels? "
                        "`yes`, `no` (no symbol, or it belongs to another test: say which), `cannot tell`.",
                        [pt(r, f"{s} {r['symbol']}")], [pt(x, f"{x['series_id']} {x['symbol']}") for x in near], src, ol, verify="one-sided")
                elif st == "one-sided" and kind == "feature":
                    role = dc.feature_role(r)
                    add("feature-only", fid, p, s,
                        f"Only one reader marked this point of the drawn {s} line, as '{(r.get('note') or role)[:80]}'. Is the {{S}} mark on the drawn line "
                        "and does it represent what the note says? `yes`, `no`, `cannot tell`.",
                        [pt(r)], [], src, ol, verify="one-sided")
            # runs of one-sided trace samples
            tr = [r for r in rows if r["point_kind"] == "trace"]
            for src in ("claude", "codex"):
                ol = other_of(src)
                own = [r for r in tr if r["source"] == src]
                if not own:
                    continue
                ot = sorted([x for x in R[ol] if x["series_id"] == s and x["point_kind"] == "trace"], key=lambda x: int(x["sequence"]))
                runs, cur = [], []
                for r in tr:   # drawing order; a run breaks at any sample that is not this reader's one-sided one
                    if r["source"] == src and r["status"] == "one-sided":
                        cur.append(r)
                    elif cur:
                        runs.append(cur); cur = []
                if cur:
                    runs.append(cur)
                for run in runs:
                    if not ot:
                        continue
                    xo = [float(x["x_native"]) for x in ot]
                    xr = [float(r["x_native"]) for r in run]
                    where = "curve-start" if max(xr) < min(xo) else "curve-end" if min(xr) > max(xo) else "trace-gap"
                    lo_x, hi_x = min(xr), max(xr)
                    ref = [x for x in ot if lo_x - 15 <= float(x["x_native"]) <= hi_x + 15] or \
                          (ot[:3] if where == "curve-start" else ot[-3:])
                    q = {"curve-start": f"The {{S}} samples extend the {s} curve before the first {{R}} sample.",
                         "curve-end": f"The {{S}} samples extend the {s} curve beyond the last {{R}} sample.",
                         "trace-gap": f"The {{S}} samples lie inside a gap of the {{R}} trace (a dashed line is often interrupted around a symbol)."}[where]
                    add(where, fid, p, s, q + f" Is every {{S}} sample on the ink of the drawn {s} line (not on a symbol, not in white space, "
                        "not on another curve or a grid line)? `all yes`, `all no`, or list the off-line ones by pixel; or `cannot tell`.",
                        [pt(r) for r in run], [pt(x) for x in ref], src, ol, lines=True, extra={"n_subject": len(run)}, verify="one-sided")

for it in items:   # notes travel with their marks, under the neutral labels
    if "_n1" in it:
        k = key[int(it["item"]) - 1]
        n1, n2 = it.pop("_n1"), it.pop("_n2")
        it["note_P"], it["note_Q"] = (n1, n2) if k["subject_label"] == "P" else (n2, n1)
fields = list(dict.fromkeys(k for it in items for k in it))
with open(OUT / "items.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(items)
with open(KEYF, "w", encoding="utf-8", newline="") as f:
    meta = [dict(k, figure=i["figure"], panel=i["panel"], series=i["series"], kind=i["kind"]) for k, i in zip(key, items)]
    w = csv.DictWriter(f, fieldnames=list(meta[0].keys()), lineterminator="\n"); w.writeheader(); w.writerows(meta)
print(len(items), "items:", dict(Counter(i["kind"] for i in items)))
