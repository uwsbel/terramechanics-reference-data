"""Correct the decisions that came from run items answered `some` (D-039).

apply_adjudication3.py and apply_adjudication4.py took every pixel pair in a `some` comment as an off-line
sample, but the comments also name the samples they call on the line ("Off: (650,3567) ... (797,3370) is on
the line"), so samples both adjudicators had called on were excluded, or split. This script recomputes each
such item from the round's off-lists.csv (the comments transcribed sample by sample, two independent
transcriptions diffed; a disagreement is `unclear`) with the rules of apply_adjudication4.py:

- an answer's off set: `all yes` none, `all no` all, `some` the samples off-lists.csv calls off (unknown if
  any of its samples is `unclear`); any other answer is unknown;
- an unknown off set leaves the whole item undecided; otherwise a sample neither calls off is verified,
  one both call off is excluded, any other is undecided.

Then, per sample, against the batch's decisions file: a row written from this item that disagrees is
replaced (or removed, when the sample is now undecided: it returns to its status before adjudication); a
sample with no row gets the corrected decision only if no later round decided it. Writes the decisions
files in place and a report.

Usage: correct_some_answers.py <report.md> <round_dir> [<round_dir> ...]
"""
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(r"<repository>")
F = ["panel", "series_id", "point_kind", "sequence", "source", "status", "use", "note"]
TAG = re.compile(r"blind adjudication item (\d+) \(Claude's adjudicator: ([^;]+); Codex's: ([^)]+)\)")
PX = re.compile(r"\((\d+),(\d+)\)")
RUNS = ("curve-start", "curve-end", "trace-gap")


def load(p):
    return list(csv.DictReader(open(p, encoding="utf-8-sig", newline="")))


def norm(a):
    return re.sub(r"\s+", " ", (a or "").strip().lower())


batch_of = {}
for ov in REPO.glob("qa/*/overlays.csv"):
    for r in load(ov):
        batch_of.setdefault(r["figure_id"], set()).add(ov.parent.name)

report, changed = [], defaultdict(list)
dec_cache = {}


def decisions(batch, fid, panel):
    p = REPO / "qa" / batch / f"decisions-{fid}-p{panel}.csv"
    if p not in dec_cache:
        dec_cache[p] = load(p) if p.exists() else []
    return p, dec_cache[p]


def pixel(batch, fid, panel, rid):
    src, s, kind, seq = rid.split("|")
    for f in (REPO / "qa" / batch / "rederived" / src / fid).glob(f"points-p{panel}-native.csv"):
        for r in load(f):
            if (r["series_id"], r["point_kind"], r["sequence"]) == (s, kind, seq):
                return round(float(r["pixel_u"])), round(float(r["pixel_v"]))
    raise SystemExit(f"no pixel for {batch} {fid} p{panel} {rid}")


out_report = Path(sys.argv[1])
for rd in map(Path, sys.argv[2:]):
    key = {r["item"].zfill(3): r for r in load(rd / "key.csv")}
    ans = {"claude": {}, "codex": {}}
    for who in ans:
        for f in rd.glob(f"answers-{who}-*.csv"):
            for r in load(f):
                ans[who][r["item"].zfill(3)] = r
    offl = defaultdict(list)
    for r in load(rd / "off-lists.csv"):
        u, v = map(int, PX.match(r["sample_px"]).groups())
        offl[(r["item"].zfill(3), r["adjudicator"])].append(((u, v), r["verdict"]))
    for it, k in sorted(key.items()):
        if k["kind"] not in RUNS or it not in ans["claude"] or it not in ans["codex"]:
            continue
        a_c, a_x = norm(ans["claude"][it]["answer"]), norm(ans["codex"][it]["answer"])
        if "some" not in (a_c, a_x):
            continue
        fid, panel = k["figure"], k["panel"]
        (batch,) = batch_of[fid]
        subj = k["subject_rows"].split(";")
        spx = [pixel(batch, fid, panel, rid) for rid in subj]

        def off_set(a, who):
            if a == "all yes":
                return set()
            if a == "all no":
                return set(range(len(subj)))
            if a == "some":
                rows = offl.get((it, who))
                if not rows or any(v == "unclear" for _, v in rows):
                    return None
                found = set()
                for (u, v), verdict in rows:
                    i = min(range(len(spx)), key=lambda j: (spx[j][0] - u) ** 2 + (spx[j][1] - v) ** 2)
                    if verdict == "off" and (spx[i][0] - u) ** 2 + (spx[i][1] - v) ** 2 <= 16:
                        found.add(i)
                return found
            return None

        oc, ox = off_set(a_c, "claude"), off_set(a_x, "codex")
        sr = k["subject_reader"]
        other = "codex" if sr == "claude" else "claude"
        tag = f"blind adjudication item {it} (Claude's adjudicator: {a_c}; Codex's: {a_x})"
        path, rows = decisions(batch, fid, panel)
        for i, rid in enumerate(subj):
            src, s, kind, seq = rid.split("|")
            if oc is None or ox is None or ((i in oc) != (i in ox)):
                want = None
            elif i in oc:
                want = ("excluded", f"off the drawn line (both adjudicators; on a symbol or in white space); {tag}")
            else:
                want = ("one-sided-verified", f"on the ink of the drawn line, verified on the page by {other}'s adjudicator; {tag}")
            ident = lambda d: (d["panel"], d["source"], d["series_id"], d["point_kind"], d["sequence"]) == (panel, src, s, kind, seq)
            mine = [d for d in rows if ident(d) and (m := TAG.search(d["note"] or "")) and m.group(1).zfill(3) == it
                    and norm(m.group(2)) == a_c and norm(m.group(3)) == a_x]
            others = [d for d in rows if ident(d) and d not in mine]
            note = " (corrected 2026-11-07, D-039: the `some` comment named this sample on the line)"
            if mine:
                d = mine[0]
                if want is None:
                    rows.remove(d)
                    changed[path].append(f"{fid} {rid}: {d['status']} removed, now undecided ({tag})")
                elif d["status"] != want[0]:
                    changed[path].append(f"{fid} {rid}: {d['status']} -> {want[0]} ({tag})")
                    d["status"], d["use"], d["note"] = want[0], "", want[1] + note
            elif want is not None and not others:
                rows.append({"panel": panel, "series_id": s, "point_kind": kind, "sequence": seq, "source": src,
                             "status": want[0], "use": "", "note": want[1] + note})
                changed[path].append(f"{fid} {rid}: undecided -> {want[0]} ({tag})")

lines = ["# Correction of decisions from `some` answers (D-039)", ""]
for path, ch in changed.items():
    rows = dec_cache[path]
    with open(path, "w", encoding="utf-8", newline="") as o:
        w = csv.DictWriter(o, fieldnames=F, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(rows, key=lambda d: (d["series_id"], d["point_kind"], d["source"], int(d["sequence"]))))
    lines += [f"## {path.relative_to(REPO).as_posix()}", ""] + [f"1. {c}" for c in ch] + [""]
lines.append(f"{sum(len(c) for c in changed.values())} rows changed in {len(changed)} files.")
out_report.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
print("\n".join(lines[-1:]))
