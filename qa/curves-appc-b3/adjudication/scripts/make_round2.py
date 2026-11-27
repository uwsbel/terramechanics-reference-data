"""Second-round packet: the items the two first-round adjudicators split, with both answers and
comments under neutral names (adjudicator 1 and 2, order shuffled per item). Same crops and pages.
Usage: make_round2.py <adj_dir> <key.csv> <out_dir>"""
import csv, random, re, shutil, sys
from pathlib import Path
ADJ, KEYF, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(ADJ / "packet", OUT)
load = lambda p: list(csv.DictReader(open(p, encoding="utf-8-sig", newline="")))
items = {r["item"]: r for r in load(ADJ / "packet" / "items.csv")}
splits = load(ADJ / "decisions-r1" / "splits.csv")
ans = {"claude": {}, "codex": {}}
for f in ADJ.glob("answers-claude-*.csv"):
    for r in load(f): ans["claude"][r["item"].zfill(3)] = r
for f in ADJ.glob("answers-codex-*.csv"):
    for r in load(f): ans["codex"][r["item"].zfill(3)] = r
key = {k["item"]: k for k in load(KEYF)}
rng = random.Random(2)
rows, hidden = [], []
for s in splits:
    it = s["item"]
    if it == "-":
        continue
    i = items[it]
    order = ["claude", "codex"]
    rng.shuffle(order)
    focus = ""
    if s["why"].startswith("run"):
        rids = s["why"].split(": ", 2)[-1].split()
        # pixels of the split samples, from the subject list
        subj = key[it]["subject_rows"].split(";")
        px = re.findall(r"px \((\d+),(\d+)\)", i[key[it]["subject_label"]])
        pts = [f"({u},{v})" for (rid, (u, v)) in zip(subj, px) if rid in rids] if len(px) >= len(subj) else []
        focus = ("Only these samples are still in question: " + " ".join(pts)) if pts else \
                f"{len(rids)} of the subject samples are still in question (see the two comments for which)."
    rows.append({"item": it, "kind": i["kind"], "figure": i["figure"], "panel": i["panel"], "series": i["series"],
                 "legend_symbol": i["legend_symbol"], "question": i["question"], "focus": focus, "P": i["P"], "Q": i["Q"],
                 "crop": i["crop"], "crop_origin_px": i["crop_origin_px"], "crop_scale": i["crop_scale"],
                 "answer_1": ans[order[0]][it]["answer"], "comment_1": ans[order[0]][it]["comment"],
                 "answer_2": ans[order[1]][it]["answer"], "comment_2": ans[order[1]][it]["comment"],
                 **{k: i[k] for k in ("candidates", "note_P", "note_Q") if k in i}})
    hidden.append({"item": it, "adjudicator_1": order[0], "adjudicator_2": order[1]})
for f in (OUT / "items.csv",):
    f.unlink()
with open(OUT / "items-round2.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(dict.fromkeys(k for r in rows for k in r)), lineterminator="\n"); w.writeheader(); w.writerows(rows)
with open(KEYF.parent / "round2-adjudicator-order.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["item", "adjudicator_1", "adjudicator_2"], lineterminator="\n"); w.writeheader(); w.writerows(hidden)
(OUT / "BRIEF-ROUND2.md").write_text("""# Second round: items the first two adjudicators split

Read `BRIEF.md` first (the figures, the files, the blindness rules, the answer vocabulary per kind);
everything there still applies. This round has only the items on which two independent first-round
adjudicators disagreed: `items-round2.csv`, with both of their answers and comments (`answer_1`,
`comment_1`, `answer_2`, `comment_2`; who they are does not matter). Where only some samples of a run
are still in question, the `focus` column names them.

For each item, look at the crop and the page yourself, weigh the two comments as evidence (they may
point at something you would have missed, or be wrong), and give the answer the ink supports, in the
brief's vocabulary. For a run, answer for the samples in question only: `all yes`, `all no`, or
`some` with the off-line ones listed by pixel. When the ink cannot settle it, `cannot tell` is the
right answer: the item then goes to a person.

Conventions both first-round adjudicators were unsure about, settled for this round:
1. A trace sample counts as on the line when it is on the line's ink or within 2 px of it at the
   line's height. A sample on a symbol's outline, or in the white gap between a dash and a symbol,
   is off the line, even if its height is close.
2. The first or last point of a drawn line is where its ink starts or ends. When the line runs
   into a plotted symbol without a white gap, the point is the symbol's center; when a white gap
   separates the line's end from the symbol, it is the end of the ink.
3. For an identity item, `both` means two separate symbols are printed there (name them in the
   comment); a white pocket enclosed by the strokes of neighbouring symbols is not a symbol.

Write `answers-round2.csv` (`item,answer,confidence,comment`), one row per item, none skipped.
""", encoding="utf-8")
print(len(rows), "items in round 2")
