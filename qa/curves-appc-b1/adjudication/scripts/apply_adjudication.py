"""Turn the two blind adjudications (a Claude adjudicator and a Codex adjudicator, same packet, neutral
labels) into decisions files for curves-appc-b1/b2 and the pilot's new curve-end rows.

Rules:
- pair items (marker-, feature-, trace-disagree): both adjudicators must give the same answer.
  The reader they pick: resolved, that reading kept (swapped in when it is not the canonical row's),
  credit to it; `both`: resolved, canonical kept (the difference is within the symbol or line).
- identity items: both must name the same series. The row of that series is one-sided-verified,
  the other identity's one-sided row excluded; `both`: both rows verified (two symbols there).
- one-sided items (marker-only, feature-only, curve-start, curve-end, trace-gap): verified when the
  adjudicator of the OTHER agent (Codex for Claude's points, Claude for Codex's) says yes and the
  first agent's adjudicator does not say no; excluded when both say no.
- everything else is a split, listed for a second round.
Usage: apply_adjudication.py <answers_dir> <key.csv> <out_dir>
"""
import csv, re, sys
from collections import defaultdict, Counter
from pathlib import Path
REPO = Path(r"<repository>")
ADJ, KEYF, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)
BATCH_OF = {"FC-1C": "curves-appc-b1", "FC-1D": "curves-appc-b1", "FC-2B": "curves-appc-b1", "FC-2C": "curves-appc-b1",
            "FC-3B": "curves-appc-b2", "FC-3C": "curves-appc-b2", "FC-4B": "curves-appc-b2", "FC-4C": "curves-appc-b2",
            "FC-1B": "curves-pilot-b1"}


def load(p):
    return list(csv.DictReader(open(p, encoding="utf-8-sig", newline="")))


def norm(a):
    a = (a or "").strip().lower()
    a = re.sub(r"\s+", " ", a)
    return a


ans = {"claude": {}, "codex": {}}
for f in sorted(ADJ.glob("answers-claude-*.csv")):
    for r in load(f):
        ans["claude"][r["item"].zfill(3)] = r
for f in sorted(ADJ.glob("answers-codex-*.csv")):
    for r in load(f):
        ans["codex"][r["item"].zfill(3)] = r
key = load(KEYF)
other = {"claude": "codex", "codex": "claude"}
OFF_LISTS = defaultdict(list)   # (item, adjudicator) -> [((u, v), off|on|unclear)], from <answers_dir>/off-lists.csv
if (ADJ / "off-lists.csv").exists():
    for _r in load(ADJ / "off-lists.csv"):
        _u, _v = map(int, re.match(r"\((\d+),(\d+)\)", _r["sample_px"]).groups())
        OFF_LISTS[(_r["item"].zfill(3), _r["adjudicator"])].append(((_u, _v), _r["verdict"]))
items_by = {r["item"]: r for r in load(ADJ / "packet" / "items.csv")}
row_px = {}   # (figure, panel, "source|series|kind|seq") -> pixel, from the canonical files the packet was built from
for fid, batch in BATCH_OF.items():
    for p in "12":
        f = REPO / "qa" / batch / f"canonical-{fid}-p{p}.csv"
        if batch == "curves-pilot-b1":
            f = Path(sys.argv[4]) / f"canonical-p{p}.csv"
        if f.exists():
            for r in load(f):
                row_px[(fid, p, f"{r['source']}|{r['series_id']}|{r['point_kind']}|{r['sequence']}")] = (round(float(r["pixel_u"])), round(float(r["pixel_v"])))

decisions = defaultdict(dict)   # (figure, panel) -> row id -> decision dict
splits, tally, credit = [], Counter(), Counter()


def decide(fid, panel, rid, status, use, note):
    src, s, kind, seq = rid.split("|")
    prev = decisions[(fid, panel)].get(rid)
    if prev and (prev["status"], prev["use"]) != (status, use):
        splits.append({"item": "-", "why": f"conflicting decisions for {fid} p{panel} {rid}: {prev['status']} vs {status}"})
        return
    decisions[(fid, panel)][rid] = {"panel": panel, "series_id": s, "point_kind": kind, "sequence": seq, "source": src,
                                    "status": status, "use": use, "note": note}


def who(k, a):
    """The reader an adjudicator's p/q answer names."""
    a = norm(a)
    return k["P"] if a == "p" else k["Q"] if a == "q" else a


for k in key:
    it = k["item"]
    ca, xa = ans["claude"].get(it), ans["codex"].get(it)
    if not ca or not xa:
        splits.append({"item": it, "why": "missing answer from " + ", ".join(n for n, x in (("claude", ca), ("codex", xa)) if not x)}); continue
    fid, panel, kind = k["figure"], k["panel"], k["kind"]
    subj, ref = k["subject_rows"].split(";"), [x for x in k["reference_rows"].split(";") if x]
    sr = k["subject_reader"]
    a_c, a_x = norm(ca["answer"]), norm(xa["answer"])
    tag = f"blind adjudication item {it} (Claude's adjudicator: {a_c}; Codex's: {a_x})"
    if k["verify"] == "pair":
        wc, wx = who(k, a_c), who(k, a_x)
        if wc != wx or wc not in ("claude", "codex", "both"):
            splits.append({"item": it, "why": f"pair: {wc} vs {wx}", **{"c": ca["comment"], "x": xa["comment"]}}); continue
        what = {"marker-disagree": "symbol center", "feature-disagree": "feature", "trace-disagree": "drawn line"}[kind]
        if wc == "both":
            decide(fid, panel, subj[0], "resolved", "", f"both readings are on the {what}; the difference is within its size ({tag})")
            tally["pair: both"] += 1
        elif wc == sr:
            decide(fid, panel, subj[0], "resolved", "", f"the {wc} reading is on the {what}; credit {wc} ({tag})")
            tally["pair: canonical kept"] += 1; credit[wc] += 1
        else:
            decide(fid, panel, subj[0], "resolved", wc, f"the {wc} reading is on the {what}; credit {wc} ({tag})")
            tally["pair: other swapped in"] += 1; credit[wc] += 1
    elif k["verify"] == "identity":
        sc = re.findall(r"n\d+", a_c) or (["both"] if "both" in a_c else [a_c])
        sx = re.findall(r"n\d+", a_x) or (["both"] if "both" in a_x else [a_x])
        if sc[:1] != sx[:1] or sc[0] in ("cannot tell", ""):
            splits.append({"item": it, "why": f"identity: {sc} vs {sx}", "c": ca["comment"], "x": xa["comment"]}); continue
        verdict = sc[0]
        subj_series = subj[0].split("|")[1]
        if verdict == "both":
            decide(fid, panel, subj[0], "one-sided-verified", "", f"two symbols at this spot, this one is {subj_series}; {tag}")
            tally["identity: both"] += 1
        elif verdict == subj_series:
            decide(fid, panel, subj[0], "one-sided-verified", "", f"the symbol is {subj_series}; the other reading filed it under another test; credit {sr} ({tag})")
            tally["identity: subject right"] += 1; credit[sr] += 1
        else:
            decide(fid, panel, subj[0], "excluded", "", f"the symbol is {verdict}, not {subj_series}; credit {other[sr]} ({tag})")
            tally["identity: subject wrong"] += 1; credit[other[sr]] += 1
    elif kind in ("curve-start", "curve-end", "trace-gap"):   # runs: decided sample by sample
        subj_px = [row_px[(fid, panel, rid)] for rid in subj]
        unclear = set()   # samples a `some` comment names without saying on or off: left split

        # Until 2026-11-07 this read every pixel pair of a `some` comment as off, including the samples the
        # comment called on the line (D-039); the decisions of this folder's rounds were corrected by
        # qa/adjudication-2026-11-07/scripts/correct_some_older.py. The off samples now come from the round's
        # off-lists.csv (two independent transcriptions of the comments, diffed), as in apply_adjudication4.py.
        def off_set(a, adj):
            if a == "all yes": return set()
            if a == "all no": return set(range(len(subj)))
            if a == "some":
                rows = OFF_LISTS.get((it, adj))
                if not rows: return None   # no transcription: unknown
                found = set()
                for (u, v), verdict in rows:
                    best = min(range(len(subj)), key=lambda i: (subj_px[i][0] - u) ** 2 + (subj_px[i][1] - v) ** 2)
                    if (subj_px[best][0] - u) ** 2 + (subj_px[best][1] - v) ** 2 <= 16:
                        if verdict == "off": found.add(best)
                        elif verdict == "unclear": unclear.add(best)
                return found
            return None
        oc, ox = off_set(a_c, "claude"), off_set(a_x, "codex")
        if oc is None or ox is None:
            splits.append({"item": it, "why": f"run ({kind}, {len(subj)} rows): unreadable or cannot tell (Claude's {a_c}, Codex's {a_x})", "c": ca["comment"], "x": xa["comment"]}); continue
        left = []
        for i, rid in enumerate(subj):
            if i in unclear:
                left.append(rid)
            elif i not in oc and i not in ox:
                decide(fid, panel, rid, "one-sided-verified", "", f"on the ink of the drawn line, verified on the page by {other[sr]}'s adjudicator; {tag}")
                tally[f"{kind}: sample verified"] += 1
            elif i in oc and i in ox:
                decide(fid, panel, rid, "excluded", "", f"off the drawn line (both adjudicators; on a symbol or in white space); {tag}")
                tally[f"{kind}: sample excluded"] += 1
            else:
                left.append(rid)
        if left:
            splits.append({"item": it, "why": f"run ({kind}): {len(left)} of {len(subj)} samples split: " + " ".join(left), "c": ca["comment"], "x": xa["comment"]})
    else:   # one-sided verification
        non_author = ans[other[sr]].get(it)   # the other agent's adjudicator verifies
        na, au = norm(non_author["answer"]), norm(ans[sr][it]["answer"])
        yes = lambda a: a in ("yes", "all yes")
        no = lambda a: a in ("no", "all no")
        if yes(na) and not no(au) and au != "some":
            for rid in subj:
                decide(fid, panel, rid, "one-sided-verified", "", f"verified on the page by {other[sr]}'s adjudicator; {tag}")
            tally[f"{kind}: verified"] += 1
        elif no(na) and no(au):
            for rid in subj:
                decide(fid, panel, rid, "excluded", "", f"not on the ink of this test (both adjudicators); {tag}: " + (non_author['comment'] or '')[:160])
            tally[f"{kind}: excluded"] += 1
        else:
            splits.append({"item": it, "why": f"one-sided ({kind}, {len(subj)} rows): other agent's adjudicator {na}, own {au}",
                           "c": ca["comment"], "x": xa["comment"]})

for (fid, panel), rows in decisions.items():
    batch = BATCH_OF[fid]
    name = f"decisions-{fid}-p{panel}.csv" if batch != "curves-pilot-b1" else f"decisions-p{panel}-adjudication.csv"
    (OUT / batch).mkdir(parents=True, exist_ok=True)
    with open(OUT / batch / name, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["panel", "series_id", "point_kind", "sequence", "source", "status", "use", "note"], lineterminator="\n")
        w.writeheader(); w.writerows(sorted(rows.values(), key=lambda d: (d["series_id"], d["point_kind"], d["source"], int(d["sequence"]))))
with open(OUT / "splits.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["item", "why", "c", "x"], lineterminator="\n", extrasaction="ignore"); w.writeheader(); w.writerows(splits)
print("decided:", dict(tally))
print("credit:", dict(credit))
print("splits:", len(splits))
print("decision rows:", sum(len(v) for v in decisions.values()))
