"""Final decision per re-checked point from the two rounds (round 1 settles where the adjudicators agreed,
round 2 where they agreed there; otherwise still split), with the size of the change where a reading moves.

Decisions:
  keep            the kept reading stands (both adjudicators: the kept mark, or both marks, are on the ink)
  switch          the other reading is on the ink and the kept one is not: take the other reading
  off-ink trace   a trace sample neither reading has on the line's own ink (in a dash/symbol gap or on a
                  symbol): drop the sample, the symbol carries the point (conventions 1, 2, 8 of round 2)
  outside box     a kept symbol center just outside its error box: widen the bound
  unresolved      both adjudicators cannot tell: widen the bound to cover both readings
  split           the adjudicators still disagree after two rounds

Usage: finalize.py <adjudication_dir>   (reads round1/, round2/, key.csv; writes final-decisions.csv)
"""
import csv, re, sys
from collections import Counter
from pathlib import Path

D = Path(sys.argv[1])
load = lambda p: list(csv.DictReader(open(p, encoding="utf-8-sig", newline="")))
r1 = {r["item"]: r for r in load(D / "round1" / "recheck-results.csv")}
r2 = {r["item"]: r for r in load(D / "round2" / "recheck-results.csv")}
key = {r["item"]: r for r in load(D / "key.csv")}
# blue (kept) and orange (other) values the student packets printed, from the wave 1 keys
vals = {}
for f in sorted((D.parent / "audits" / "keys").glob("key-*-[A-E].csv")):  # D is qa/adjudication-<date>
    for k in load(f):
        if k["kind"] == "compare":
            obj = "/".join(k[c] for c in ("figure_id", "panel", "series_id", "point_kind", "source", "sequence"))
            num = lambda s: float(re.match(r"\s*(-?\d+(?:\.\d+)?)", s).group(1)) if s and re.match(r"\s*-?\d", s) else None
            unit = (k["blue"].split(" ")[1] if k["blue"] and len(k["blue"].split(" ")) > 1 else "")
            vals[obj] = (num(k["blue"]), num(k["orange"]), unit)


def decide(r):
    a = r["action"]
    if a == "keep":
        return "keep"
    if a.startswith("switch"):
        return "switch"
    if a == "re-read":
        return "outside box" if r["kind"] == "check-marker" else "off-ink trace"
    if a.startswith("unresolved"):
        return "unresolved"
    return "split"


rows = []
for item, a in sorted(r1.items()):
    rr, rnd = (a, 1) if a["agree"] == "yes" else (r2[item], 2)
    dec = decide(rr)
    kept, other, unit = vals.get(a["object"], (None, None, ""))
    delta = f"{other - kept:+.1f} {unit}" if dec == "switch" and kept is not None and other is not None else ""
    rel = f"{100 * (other - kept) / kept:+.1f}%" if delta and kept else ""
    rows.append({"item": item, "object": a["object"], "kind": a["kind"], "review_outcome": a["review_outcome"],
                 "reviews": a["reviews"], "round": rnd, "claude": rr["claude"], "codex": rr["codex"], "decision": dec,
                 "kept_value": "" if kept is None else kept, "other_value": "" if other is None else other, "change": delta, "change_pct": rel})
with open(D / "final-decisions.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n"); w.writeheader(); w.writerows(rows)
print("decisions:", dict(Counter(r["decision"] for r in rows)))
for ro in ("flagged", "split", "both cannot tell", "single-problem"):
    print(f"  students {ro:17}", dict(Counter(r["decision"] for r in rows if r["review_outcome"] == ro)))
print("by kind:", dict(Counter((r["kind"], r["decision"]) for r in rows)))
for r in rows:
    if r["decision"] == "switch":
        print("  switch", r["item"], r["object"], r["kept_value"], "->", r["other_value"], r["change"], r["change_pct"])
