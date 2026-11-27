"""Apply the second-round answers with the same rules as the first round, restricted to the split
items (for runs, to the split samples), then merge with the first round's decisions (first round
wins where both decided) into <adj>/decisions-final/.
Usage: round2_apply2.py <adj_dir> <key.csv> <claude_r2.csv> <codex_r2.csv> <batch> [<batch> ...]"""
import csv, shutil, subprocess, sys
from pathlib import Path
ADJ, KEYF, CR2, XR2 = map(Path, sys.argv[1:5])
BATCHES = sys.argv[5:]
load = lambda p: list(csv.DictReader(open(p, encoding="utf-8-sig", newline="")))
W = ADJ / "r2work"
if W.exists():
    shutil.rmtree(W)
(W / "packet").mkdir(parents=True)
shutil.copy2(ADJ / "packet" / "items.csv", W / "packet" / "items.csv")
splits = {s["item"]: s for s in load(ADJ / "decisions-r1" / "splits.csv") if s["item"] != "-"}
key = [k for k in load(KEYF) if k["item"] in splits]
for k in key:
    why = splits[k["item"]]["why"]
    if why.startswith("run") and "samples split:" in why:
        k["subject_rows"] = ";".join(why.split("samples split: ", 1)[1].split())
with open(W / "key.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(key[0].keys()), lineterminator="\n"); w.writeheader(); w.writerows(key)
shutil.copy2(CR2, W / "answers-claude-r2.csv")
shutil.copy2(XR2, W / "answers-codex-r2.csv")
# the round's `some` answers transcribed sample by sample (D-039). A re-run restricts the runs to the samples the
# corrected first round splits, which can differ from the samples this round was asked about; the decisions as
# recorded were corrected sample by sample through the rounds by qa/adjudication-2026-11-07/scripts/correct_some_older.py.
if (CR2.parent / "off-lists.csv").exists():
    shutil.copy2(CR2.parent / "off-lists.csv", W / "off-lists.csv")
r = subprocess.run([sys.executable, str(Path(__file__).parent / "apply_adjudication3.py"), str(W), str(W / "key.csv"), str(W / "decisions")] + BATCHES,
                   capture_output=True, text=True, encoding="utf-8")
print("round 2:", r.stdout, r.stderr[-1500:])
# merge
out = ADJ / "decisions-final"
if out.exists():
    shutil.rmtree(out)
n1 = n2 = 0
for d in (ADJ / "decisions-r1", W / "decisions"):
    for f in d.rglob("decisions-*.csv"):
        rel = f.relative_to(d)
        tgt = out / rel
        tgt.parent.mkdir(parents=True, exist_ok=True)
        rows = load(f)
        old = load(tgt) if tgt.exists() else []
        seen = {(x["series_id"], x["point_kind"], x["sequence"], x["source"]) for x in old}
        new = [x for x in rows if (x["series_id"], x["point_kind"], x["sequence"], x["source"]) not in seen]
        if d.name == "decisions":
            for x in new:
                x["note"] = "second round: " + x["note"]
            n2 += len(new)
        else:
            n1 += len(new)
        with open(tgt, "w", encoding="utf-8", newline="") as g:
            w = csv.DictWriter(g, fieldnames=["panel", "series_id", "point_kind", "sequence", "source", "status", "use", "note"], lineterminator="\n")
            w.writeheader(); w.writerows(sorted(old + new, key=lambda x: (x["series_id"], x["point_kind"], x["source"], int(x["sequence"]))))
shutil.copy2(W / "decisions" / "splits.csv", out / "still-split.csv")
print(f"merged: {n1} first-round and {n2} second-round decision rows; still split: {len(load(out / 'still-split.csv'))}")
