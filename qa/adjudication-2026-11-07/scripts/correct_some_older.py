"""Correct the decisions that came from run items answered `some` in the six older adjudication rounds (D-039,
second part): rounds 1 and 2 of qa/curves-appc-b1/adjudication and of qa/curves-appc-b3/adjudication (applied by
apply_adjudication.py and apply_adjudication2.py with round2_apply*.py) and rounds 1 to 3 of
qa/curves-rederivation-d025/adjudication (apply_adjudication3.py, round2_apply3.py, merge_decisions.py). Round 4
of the D-025 chain has no `some` answer but is loaded, since its decisions are later than the others.

These tools took every pixel pair in a `some` comment as an off-line sample, including the samples the comment
called on the line. The comments are transcribed sample by sample in each round's off-lists.csv (two independent
transcriptions, diffed; a disagreement settled from the comment text).

The older chains differ from the 2026-10-15 rounds in two ways that the first correction script
(correct_some_answers.py) did not have to handle:

1. A second round re-asked only the samples the first round split (its `focus` column names them by pixel), and
   the split was computed with the defective parser; its own `some` answers have the same defect.
2. Rounds were merged with "the first decision wins" (round2_apply*.py, merge_decisions.py), and the D-025 rounds
   were merged into decision files that already held the decisions of the earlier chains.

So the correction replays every round in order (ROUNDS below) with both parsers. For a run item with a `some`
answer, each sample gets a defective outcome (what the tools did) and a corrected one (verified, excluded or
undecided). A sample is touched only when some round's outcome for it changes. Its corrected state is the
decision of the latest round that decides it, a corrected outcome for a `some` item and the recorded outcome of
every other item (the rows a round wrote are read from the stored round outputs or matched in the batch files by
their note); a sample no round decides is undecided, and its row is removed. A later round's decision is never
overwritten by the correction of an earlier one.

Usage:
  correct_some_older.py inventory <some-answers.csv>     list the `some` answers (subject samples, comment)
  correct_some_older.py packet <dir>                      the transcription packet input (same rows, no decisions)
  correct_some_older.py correct <report.md> [--dry-run]  replay, correct the decision files, write the report
"""
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
F = ["panel", "series_id", "point_kind", "sequence", "source", "status", "use", "note"]
TAG = re.compile(r"blind adjudication item (\d+) \(Claude's adjudicator: ([^;]+); Codex's: ([^)]+)\)")
PX = re.compile(r"\(?(\d{3,4})\s*,\s*(\d{3,4})\)?")
RUNS = ("curve-start", "curve-end", "trace-gap")
NOTE = " (corrected 2026-11-07, D-039: the `some` comment named this sample on the line)"


def load(p):
    return list(csv.DictReader(open(p, encoding="utf-8-sig", newline="")))


def norm(a):
    return re.sub(r"\s+", " ", (a or "").strip().lower())


B1 = REPO / "qa/curves-appc-b1/adjudication"
B3 = REPO / "qa/curves-appc-b3/adjudication"
D25 = REPO / "qa/curves-rederivation-d025/adjudication"
# (round id, adjudication dir, round dir, key file, round-2 of (round id) or None, answers glob per adjudicator)
ROUNDS = [
    ("appc-b1/r1", B1, B1 / "round1", B1 / "key.csv", None, "answers-{w}-*.csv"),
    ("appc-b1/r2", B1, B1 / "round2", B1 / "key.csv", "appc-b1/r1", "answers-round2-{w}.csv"),
    ("appc-b3/r1", B3, B3 / "round1", B3 / "key.csv", None, "answers-{w}-*.csv"),
    ("appc-b3/r2", B3, B3 / "round2", B3 / "key.csv", "appc-b3/r1", "answers-round2-{w}.csv"),
    ("d025/r1", D25, D25 / "round1", D25 / "key.csv", None, "answers-{w}-*.csv"),
    ("d025/r2", D25, D25 / "round2", D25 / "key.csv", "d025/r1", "answers-{w}-round2.csv"),
    ("d025/r3", D25, D25 / "round3", D25 / "key-round3.csv", None, "answers-{w}-r3.csv"),
    ("d025/r4", D25, D25 / "round4", D25 / "key-round4.csv", None, "answers-{w}-r4.csv"),
]
ORDER = {r[0]: i for i, r in enumerate(ROUNDS)}

batch_of = {}
for ov in REPO.glob("qa/*/overlays.csv"):
    for r in load(ov):
        batch_of.setdefault(r["figure_id"], set()).add(ov.parent.name)
_px = {}


def pixel(fid, panel, rid):
    """A reading's sample pixel, from the re-derived reading files (every submitted point)."""
    src, s, kind, seq = rid.split("|")
    (batch,) = batch_of[fid]
    if (batch, src, fid) not in _px:
        d = {}
        for f in (REPO / "qa" / batch / "rederived" / src / fid).glob("points-p*-native.csv"):
            for r in load(f):
                d[(r["panel"], r["series_id"], r["point_kind"], r["sequence"])] = (round(float(r["pixel_u"])), round(float(r["pixel_v"])))
        _px[(batch, src, fid)] = d
    return _px[(batch, src, fid)][(panel, s, kind, seq)]


def item_file(rd):
    for n in ("items.csv", "items-round2.csv"):
        if (rd / n).exists():
            return rd / n


def load_round(rid_, adj, rd, keyf, r1, glob):
    """Items of a round: key row, subject rows and pixels, both answers. A second round's run items keep only the
    samples its `focus` names."""
    items = {r["item"].zfill(3): r for r in load(item_file(rd))}
    keys = {k["item"].zfill(3): k for k in load(keyf)}
    ans = {"claude": {}, "codex": {}}
    for w in ans:
        for f in sorted(rd.glob(glob.format(w=w))):
            for r in load(f):
                ans[w][r["item"].zfill(3)] = r
    out = []
    for it, i in items.items():
        k = dict(keys[it])
        subj = k["subject_rows"].split(";")
        spx = [pixel(k["figure"], k["panel"], x) for x in subj]
        listed = [tuple(map(int, m)) for m in re.findall(r"px \((\d+),(\d+)\)", i[k["subject_label"]])]
        if r1 is None and k["kind"] in RUNS:   # the packet's subject pixels are the reading's
            assert len(listed) == len(spx) and all(abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1 for a, b in zip(listed, spx)), (rid_, it)
        # a whole run split in the first round (an unknown answer) is asked again whole: its focus lists no pixels
        focus = [tuple(map(int, m)) for m in re.findall(r"\((\d+),(\d+)\)", i.get("focus") or "")]
        if r1 is not None and k["kind"] in RUNS and focus:
            keep = [j for j, p in enumerate(spx) if any(abs(p[0] - f[0]) <= 1 and abs(p[1] - f[1]) <= 1 for f in focus)]
            assert len(keep) == len(focus), (rid_, it, focus)
            subj, spx = [subj[j] for j in keep], [spx[j] for j in keep]
        out.append({"round": rid_, "item": it, "key": k, "subj": subj, "spx": spx,
                    "a": {w: norm(ans[w][it]["answer"]) for w in ans if it in ans[w]},
                    "c": {w: ans[w][it]["comment"] for w in ans if it in ans[w]}})
    return out


def rounds():
    return {r[0]: load_round(*r) for r in ROUNDS}


def some_rows(R):
    rows = []
    for rid_, items in R.items():
        for x in items:
            if x["key"]["kind"] not in RUNS:
                continue
            for w in ("claude", "codex"):
                if x["a"].get(w) == "some":
                    rows.append({"round": rid_, "item": x["item"], "adjudicator": w,
                                 "subject_samples": " ".join(f"({u},{v})" for u, v in x["spx"]), "comment": x["c"][w]})
    return rows


def write(p, rows, fields):
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def off_old(x, a, comment):
    """The defective parser of apply_adjudication.py to apply_adjudication3.py: every pixel pair in a `some`
    comment within 4 px of a subject sample counts as off."""
    if a == "all yes":
        return set()
    if a == "all no":
        return set(range(len(x["subj"])))
    if a == "some":
        found = set()
        for u, v in PX.findall(comment or ""):
            u, v = int(u), int(v)
            i = min(range(len(x["spx"])), key=lambda j: (x["spx"][j][0] - u) ** 2 + (x["spx"][j][1] - v) ** 2)
            if (x["spx"][i][0] - u) ** 2 + (x["spx"][i][1] - v) ** 2 <= 16:
                found.add(i)
        return found if found else None
    return None


def off_new(x, a, offl, who):
    """The corrected reading, per sample: 'off', 'on' or 'unclear' (a `some` answer from the round's
    off-lists.csv); None when the answer gives no off set at all (`cannot tell`, or `some` untranscribed).
    An unclear sample leaves only that sample undecided: the other samples of the answer are read as written.
    (correct_some_answers.py, and apply_adjudication4.py until this correction, made the whole answer unknown;
    on the first part's one unclear case, 2026-10-15 grain-size round 1 item 308, both rules give the same
    decisions. Here they differ on appc-b1 round 1 item 068: Codex's trace 1 of n3660 verified and traces 3
    to 5 excluded, where the whole-answer rule would leave all four undecided.)"""
    n = len(x["subj"])
    if a == "all yes":
        return ["on"] * n
    if a == "all no":
        return ["off"] * n
    if a == "some":
        rows = offl.get((x["item"], who))
        if not rows:
            return None
        got = ["on"] * n
        for (u, v), verdict in rows:
            i = min(range(n), key=lambda j: (x["spx"][j][0] - u) ** 2 + (x["spx"][j][1] - v) ** 2)
            assert (x["spx"][i][0] - u) ** 2 + (x["spx"][i][1] - v) ** 2 <= 16, (x["round"], x["item"], who, u, v)
            got[i] = verdict
        return got
    return None


def outcomes(x, oc, ox):
    """Per subject sample: 'verified', 'excluded' or None (split). oc, ox: off sets (old parser) or per-sample
    verdict lists (corrected reading); None is unknown."""
    n = len(x["subj"])
    if oc is None or ox is None:
        return [None] * n
    if isinstance(oc, set):
        oc = ["off" if i in oc else "on" for i in range(n)]
        ox = ["off" if i in ox else "on" for i in range(n)]
    return ["excluded" if (c, d) == ("off", "off") else "verified" if (c, d) == ("on", "on") else None
            for c, d in zip(oc, ox)]


def offlists(claude_csv, codex_csv, settled_csv):
    """Merge the two transcriptions into each round's off-lists.csv. A disagreement must be settled in
    settled_csv (from the comment text); any other disagreement stops the script."""
    k = lambda r: (r["round"], r["item"], r["adjudicator"], r["sample_px"])
    a = {k(r): r["verdict"] for r in load(claude_csv)}
    b = {k(r): r["verdict"] for r in load(codex_csv)}
    s = {k(r): r["verdict"] for r in load(settled_csv)}
    assert set(a) == set(b), "the transcriptions cover different samples"
    out = defaultdict(list)
    for key in a:
        if a[key] != b[key] and key not in s:
            raise SystemExit(f"unsettled disagreement: {key} claude {a[key]} codex {b[key]}")
        v = s.get(key, a[key])
        out[key[0]].append({"item": key[1], "adjudicator": key[2], "sample_px": key[3], "verdict": v})
    rd_of = {r[0]: r[2] for r in ROUNDS}
    for rid_, rows in out.items():
        write(rd_of[rid_] / "off-lists.csv", rows, ["item", "adjudicator", "sample_px", "verdict"])
        print(rd_of[rid_].relative_to(REPO).as_posix(), len(rows), "samples")


def correct(report_path, dry):
    R = rounds()
    rd_of = {r[0]: r[2] for r in ROUNDS}
    per = defaultdict(list)       # (fid, panel, rid) -> [(order, round, item record, old, new)], every run item
    nonrun = defaultdict(list)    # (fid, panel, rid) -> [(round, item, kind)], items of other kinds naming it
    for rid_, items in R.items():
        offl = defaultdict(list)
        if (rd_of[rid_] / "off-lists.csv").exists():
            for r in load(rd_of[rid_] / "off-lists.csv"):
                u, v = map(int, PX.match(r["sample_px"]).groups())
                offl[(r["item"].zfill(3), r["adjudicator"])].append(((u, v), r["verdict"]))
        for x in items:
            k = x["key"]
            if k["kind"] not in RUNS:
                for r in k["subject_rows"].split(";") + [y for y in k["reference_rows"].split(";") if y]:
                    nonrun[(k["figure"], k["panel"], r)].append((rid_, x["item"], k["kind"]))
                continue
            if "claude" not in x["a"] or "codex" not in x["a"]:
                continue
            a_c, a_x = x["a"]["claude"], x["a"]["codex"]
            old = outcomes(x, off_old(x, a_c, x["c"]["claude"]), off_old(x, a_x, x["c"]["codex"]))
            new = outcomes(x, off_new(x, a_c, offl, "claude"), off_new(x, a_x, offl, "codex"))
            for i, r in enumerate(x["subj"]):
                per[(k["figure"], k["panel"], r)].append((ORDER[rid_], rid_, x, old[i], new[i]))
    touched = {s: ev for s, ev in per.items() if any(o != n for _, _, _, o, n in ev)}

    def latest(ev, j):   # the decision of the latest round that decides the sample (j = 3 old, 4 new)
        dec = [e for e in sorted(ev, key=lambda e: e[0]) if e[j] is not None]
        return dec[-1] if dec else None

    def row_for(s, e, status):
        x, k = e[2], e[2]["key"]
        src, ser, kind, seq = s[2].split("|")
        other = "codex" if k["subject_reader"] == "claude" else "claude"
        tag = f"blind adjudication item {x['item']} (Claude's adjudicator: {x['a']['claude']}; Codex's: {x['a']['codex']})"
        note = (f"on the ink of the drawn line, verified on the page by {other}'s adjudicator; {tag}" if status == "verified"
                else f"off the drawn line (both adjudicators; on a symbol or in white space); {tag}")
        if e[1].endswith("/r2"):
            note = "second round: " + note
        return {"panel": s[1], "series_id": ser, "point_kind": kind, "sequence": seq, "source": src,
                "status": "one-sided-verified" if status == "verified" else "excluded", "use": "", "note": note + NOTE}

    status_of = {"verified": "one-sided-verified", "excluded": "excluded"}
    cache, changed, problems, lines_t = {}, defaultdict(list), [], []
    for s, ev in sorted(touched.items()):
        fid, panel, rid = s
        if nonrun.get(s):
            problems.append(f"{fid} p{panel} {rid}: also named by items of other kinds {nonrun[s]}; not touched")
            continue
        (batch,) = batch_of[fid]
        p = REPO / "qa" / batch / f"decisions-{fid}-p{panel}.csv"
        if p not in cache:
            cache[p] = load(p) if p.exists() else []
        src, ser, kind, seq = rid.split("|")
        ident = lambda d: (d["panel"], d["source"], d["series_id"], d["point_kind"], d["sequence"]) == (panel, src, ser, kind, seq)
        rows = [d for d in cache[p] if ident(d)]
        if len(rows) > 1:
            problems.append(f"{fid} p{panel} {rid}: {len(rows)} rows in the decisions file; not touched")
            continue
        lo, ln = latest(ev, 3), latest(ev, 4)
        hist = "; ".join(f"{e[1]} item {e[2]['item']} ({e[2]['a']['claude']} / {e[2]['a']['codex']}): {e[3] or 'split'} -> {e[4] or 'split'}" for e in ev)
        lines_t.append(f"{fid} p{panel} {rid}: {hist}")
        have = rows[0]["status"] if rows else None
        want_old = status_of[lo[3]] if lo else None
        if have != want_old:   # the replay of the defective tools must reproduce the file, or the sample is left alone
            problems.append(f"{fid} p{panel} {rid}: the file has {have}, the replay of the tools gives {want_old}; not touched")
            continue
        want = status_of[ln[4]] if ln else None
        if want == have:
            continue
        if want is None:
            cache[p].remove(rows[0])
            changed[p].append(f"{fid} {rid}: {have} removed, now undecided ({hist})")
        elif rows:
            new = row_for(s, ln, ln[4])
            rows[0].update(new)
            changed[p].append(f"{fid} {rid}: {have} -> {want}, decided by {ln[1]} item {ln[2]['item']} ({hist})")
        else:
            cache[p].append(row_for(s, ln, ln[4]))
            changed[p].append(f"{fid} {rid}: undecided -> {want}, decided by {ln[1]} item {ln[2]['item']} ({hist})")

    lines = ["# Correction of decisions from `some` answers in the older rounds (D-039, second part)", "",
             f"{len(touched)} samples whose outcome in some round changes with the corrected reading "
             "(round, item, answers: outcome as the tools applied it -> corrected):", ""]
    lines += [f"1. {t}" for t in lines_t] + [""]
    if problems:
        lines += ["## Left alone", ""] + [f"1. {q}" for q in problems] + [""]
    for p, ch in changed.items():
        lines += [f"## {p.relative_to(REPO).as_posix()}", ""] + [f"1. {c}" for c in ch] + [""]
        if not dry:   # row order kept (it records the merge order): rows replaced or removed in place, new rows appended
            write(p, cache[p], F)
    lines.append(f"{sum(len(c) for c in changed.values())} rows changed in {len(changed)} files; {len(problems)} samples left alone.")
    Path(report_path).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(lines[-1])


if __name__ == "__main__" and sys.argv[1] == "correct":
    correct(sys.argv[2], "--dry-run" in sys.argv)

if __name__ == "__main__" and sys.argv[1] == "offlists":
    offlists(*map(Path, sys.argv[2:5]))

if __name__ == "__main__" and sys.argv[1] in ("inventory", "packet"):
    R = rounds()
    rows = some_rows(R)
    if sys.argv[1] == "inventory":
        write(Path(sys.argv[2]), rows, ["round", "item", "adjudicator", "subject_samples", "comment"])
    else:
        Path(sys.argv[2]).mkdir(parents=True, exist_ok=True)
        write(Path(sys.argv[2]) / "some-answers.csv", rows, ["round", "item", "adjudicator", "subject_samples", "comment"])
    per = defaultdict(int)
    for r in rows:
        per[r["round"]] += 1
    print(len(rows), "some answers:", dict(per), "samples:", sum(len(r["subject_samples"].split()) for r in rows))
