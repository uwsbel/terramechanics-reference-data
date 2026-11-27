"""Write the re-check's decisions into the batches' decision files (hand inputs of tools/diff_curves.py).

  switch         status resolved, use <other reader>   (the other reading is on the ink, the kept one is not)
  off-ink trace  status excluded                        (on neither reading's line ink: a symbol or a gap)
  outside box    status resolved, use span              (the kept center just outside its box: widen)
  unresolved     status pending-review, use span        (nobody can tell: keep the value, widen to both)
Still-split points are left as they are. A point that already has a decision row keeps its row, updated in
place, with the earlier note kept in front of the new one. Decisions name points by the submitted series
id (series-ids.csv). Run once; a second run finds every row already written and changes nothing.

Usage: write_decisions.py <adjudication_dir> [--with-exclusions]

Exclusions are held back by default (2026-10-27): excluding a kept sample opens a break in its trace, and the
other reader's samples in that break enter as unverified one-sided points, 3 to 5 per break at the symbol,
where the adjudicators found the other line off the ink too. They wait for the off-ink rule, which judges
both readings' samples.
"""
import csv, json, sys
from pathlib import Path

D = Path(sys.argv[1]); QA = D.parent
load = lambda p: list(csv.DictReader(open(p, encoding="utf-8-sig", newline="")))
FIELDS = ["panel", "series_id", "point_kind", "sequence", "source", "status", "use", "note"]
key = {r["item"]: r for r in load(D / "key.csv")}
TAG = "audit re-check 2026-10-27"
plan = {"switch": ("resolved", None), "off-ink trace": ("excluded", ""), "outside box": ("resolved", "span"),
        "unresolved": ("pending-review", "span")}
why = {"switch": "the other reading is on the line's ink and the kept one is not; credit {other}",
       "off-ink trace": "off the drawn line's own ink (on a symbol or in a dash/symbol gap)",
       "outside box": "the symbol center lies just outside this reading's box; bounds widened",
       "unresolved": "neither reading could be shown right on the page; value kept, bounds widened to both"}
files, written, updated, skipped = {}, 0, 0, 0
WITH_EXCL = "--with-exclusions" in sys.argv
for r in load(D / "final-decisions.csv"):
    if r["decision"] not in plan or (r["decision"] == "off-ink trace" and not WITH_EXCL):
        continue
    fig, panel, sid, kind, src, seq = r["object"].split("/")
    b = key[r["item"]]["batch"]
    sub = next((x["submitted"] for x in load(QA / b / "series-ids.csv") if x["figure_id"] == fig and x["series_id"] == sid),
               sid) if (QA / b / "series-ids.csv").exists() else sid
    other = "codex" if src.split("-")[0] == "claude" else "claude"
    status, use = plan[r["decision"]]
    use = other if use is None else use
    reviews = r["reviews"].replace(":", " ")
    note = (f"{why[r['decision']].format(other=other)} ({TAG}: item {r['item']}, round {r['round']}, "
            f"Claude's adjudicator {r['claude']}, Codex's {r['codex']}; students {reviews})")
    f = QA / b / f"decisions-{fig}-p{panel}.csv"
    if f not in files:
        files[f] = load(f) if f.exists() else []
    rows = files[f]
    hit = next((x for x in rows if x["series_id"] == sub and x["point_kind"] == kind and x["sequence"] == seq
                and (x.get("source") or src) == src), None)
    if hit and TAG in hit.get("note", ""):
        skipped += 1; continue
    if hit:
        hit.update({"source": src, "status": status, "use": use, "note": f"{hit['note']}; then {note}"}); updated += 1
    else:
        rows.append({"panel": panel, "series_id": sub, "point_kind": kind, "sequence": seq, "source": src,
                     "status": status, "use": use, "note": note}); written += 1
for f, rows in files.items():
    with open(f, "w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=FIELDS, lineterminator="\n", extrasaction="ignore"); w.writeheader(); w.writerows(rows)
print(f"{written} rows added, {updated} updated in place, {skipped} already there; files: {sorted(str(f.relative_to(QA)) for f in files)}")
