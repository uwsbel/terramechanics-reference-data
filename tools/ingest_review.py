"""Score returned reviewer checklists, record the audits, and print the status board (roadmap 4c).

Usage:
    python tools/ingest_review.py [--returns qa/audits/returns] [--returned BR-D=path ...] \
        [--date 2026-10-20] [--write] [--accept BR-D ...] [--digest] [--qa-root qa]

Returned files are named checklist-<INIT>-<L>.csv (the reviewer's initials and the chunk letter: A to Z,
then AA, AB and on);
a misnamed file is passed as --returned INIT-L=path. Each return is matched to its answer key
qa/audits/keys/key-<INIT>-<L>.csv and to its chunk in qa/audits/assignments.csv.

For every return:

1. **Controls first.** The chunk's seeded mistakes (key rows whose kind starts with `control-`) have
   known answers: a location control must be answered A = no, an identity control B = no, and so must a
   value control (on a table cell, D-050); a control row absent from
   the return, or returned more than once, counts as missed, and any other row returned more than once is not
   recorded until the reviewer sends one answer (both since 2026-11-21). A
   reviewer who misses a control is reported and that return's answers are not recorded until Dan
   accepts it (--accept INIT-L). When Dan declines it instead (--decline INIT-L), the return is
   logged as `declined`, never recorded, and its points wait for another reviewer in a later wave.
2. **Answers per point.** Each audited point gets a verdict (ok, problem, cannot tell, unreadable).
   The pair outcome of a point combines this return with every other reviewer's verdict on the same
   point (the chunk partner, or for a second-review chunk the reviewers of the chunk it repeats),
   taken from this run or from qa/audits.csv if those returns came earlier: `confirmed` (all ok),
   `flagged` (all problem), `split` (one reviewer ok, another problem), `cannot-tell` (all cannot
   tell), a mix without a contradiction named by its verdicts (`ok + cannot tell`, `problem + cannot
   tell`, `ok + unreadable`; `split` until 2026-11-23), or `single (<verdict>)` while the second
   review is missing.
3. **Recording.** With --write, one row per reviewer and point is appended to qa/audits.csv (batch,
   object, column, auditor, date, outcome, note) for returns whose controls passed or were accepted;
   rows already present for the same object and auditor are not written twice, so a re-run is safe.
   The object is `<figure>/<panel>/<series>/<kind>/<source>/<sequence>` (`sequence` numbers the points
   of the reading named in `source`); the note starts with the chunk and
   letter. qa/audits/returns-log.csv gets one row per return (replaced on re-ingest).
4. **Voided answers.** A symbol point listed in qa/audits/voided.csv with column `identity` is scored,
   in the chunk the list names, on its location answer alone and recorded with column `position`; the
   void B answer goes in the note, and the identity question is asked again in the wave the list names
   (the same point in another chunk, such as a second review, is scored normally).

The report goes to qa/audits/reports/ingest-<date>.md, the status board (per reviewer: returned,
overdue, controls; per chunk: returns and pair outcomes; a reviewer with a `left` date in
qa/audits/reviewers.csv shows that date instead of overdue chunks; an assignment listed in
qa/audits/withdrawn.csv no longer counts as the reviewer's, and a return for it is reported and not
recorded) to qa/audits/status.md, and with --digest a
copy of both plus the points marked as a problem to qa/audits/digests/<date>.md for the Saturday
email to Dan.

Answers are read case-insensitively; can't tell, not sure and unclear (and their typos) read as cannot
tell; anything other than yes, no, cannot tell (or empty where the guide says to leave B empty) is
reported as unreadable. A compare row is answered in A with blue (the
kept reading is on the curve), orange (the other reading is) or cannot tell; an empty A is read from
the comment: the word blue or orange, or a number equal to one of the two values the key records.
"""
import argparse
import csv
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALID = {"yes", "no", "cannot tell", ""}
# both: the two marks are equally well on the curve or the symbol's center (until wave 3, one mark at each
# valid center of a triangle only)
VALID_COMPARE = {"blue", "orange", "both", "cannot tell", ""}
AUDIT_FIELDS = ["batch", "object", "column", "auditor", "date", "outcome", "note"]
LOG_FIELDS = ["reviewer", "letter", "chunk", "received", "rows", "controls", "unreadable", "recorded"]


def compare_answer(A, C, k):
    """The compare answer of a row: A when given, otherwise read from the comment (see the docstring)."""
    if A:
        return A, ""
    words = re.findall(r"\b(blue|orange)\b", C.lower())
    if len(set(words)) == 1:
        return words[0], " (from the comment)"
    nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", C)]
    vals = {}
    for colour in ("blue", "orange"):
        m = re.match(r"\s*(-?\d+(?:\.\d+)?)", k.get(colour) or "")
        if m:
            vals[colour] = float(m.group(1))
    hits = {c for c, val in vals.items() for n in nums if abs(n - val) <= 1.0}
    if len(hits) == 1:
        return hits.pop(), " (from the comment)"
    return "", ""


def load(p):
    p = Path(p)
    if not p.exists():
        return []
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(p, rows, fields):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with Path(p).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


# Wave 1 returns spelled "cannot tell" as can't tell (108 answers), not sure (31), unclear, and with typos
# (note sure, ncannot tell). The guide asks for cannot tell whenever the reviewer is unsure, so these read
# as cannot tell; anything else that is not a valid answer stays unreadable and is reported (2026-10-27).
CANNOT_TELL = re.compile(r"(can'?t|cannot|can not) ?tell|\bnote? sure\b|\bunsure\b|\bunclear\b")


def norm(v):
    v = " ".join((v or "").strip().lower().replace("’", "'").split())
    return "cannot tell" if CANNOT_TELL.search(v) else v


def verdict(kind, A, B):
    if kind == "compare":  # blue: the kept reading is on the curve; orange: the other reading is
        return {"blue": "ok", "both": "ok", "orange": "problem", "cannot tell": "cannot tell"}.get(A, "unreadable")
    if kind in ("curve sample", "position only"):  # position only: a symbol whose identity answer is void
        return {"yes": "ok", "no": "problem", "cannot tell": "cannot tell"}.get(A, "unreadable")
    if kind == "cell" and "no" in (A, B) and {A, B} <= {"yes", "no", "cannot tell", ""}:
        # a table cell: an explicit no on either question is a definite problem, even beside a cannot tell or an empty
        # answer (recorded as cannot tell or unreadable it would drop a known failure from the digest; Codex's review,
        # 2026-11-21, rounds 1 and 2); score_return reports the empty answer separately
        return "problem"
    if A == "cannot tell" or B == "cannot tell":
        return "cannot tell"
    if A == "yes" and B == "yes":
        return "ok"
    if A in ("yes", "no") and B in ("yes", "no"):
        return "problem"
    return "unreadable"


OUTCOME_ORDER = ("ok", "problem", "cannot tell", "unreadable")


def pair_outcome(verdicts):
    """The outcome of one point from every reviewer's verdict on it. `split` is kept for a real contradiction, one
    reviewer ok and another problem. A point where the definite answers agree and the other reviewers could not tell
    (or wrote an unreadable answer) is named by its verdicts, `ok + cannot tell`, `problem + cannot tell`, `ok +
    unreadable`: until 2026-11-23 these were all `split`, which made one reviewer's honest uncertainty read as a
    disagreement (143 of the 228 splits then on record were ok + cannot tell; Dan asked for them apart). The mixes still
    go to adjudication: it takes every point with two or more reviews that is not `confirmed`, and every single review
    that says problem, as wave 1's re-check did (docs/audit/README.md)."""
    if not verdicts:
        return "none"
    if len(verdicts) == 1:
        return f"single ({verdicts[0]})"
    kinds = set(verdicts)
    if kinds == {"ok"}:
        return "confirmed"
    if kinds == {"problem"}:
        return "flagged"
    if kinds == {"cannot tell"}:
        return "cannot-tell"
    if {"ok", "problem"} <= kinds:
        return "split"
    return " + ".join([v for v in OUTCOME_ORDER if v in kinds] + sorted(kinds - set(OUTCOME_ORDER)))


def score_return(rows, key, voided=frozenset()):
    """(controls_ok, control_notes, answers, unreadable) for one returned checklist against its key;
    voided holds (object, column, chunk) from qa/audits/voided.csv."""
    ctrl_ok, notes, answers, unreadable = True, [], [], []
    # every control row of the key must come back exactly once: until 2026-11-21 a return with its control rows deleted
    # passed, since only the rows present were scored (Codex's review of the table-cell tools)
    seen = defaultdict(int)
    for r in rows:
        seen[r.get("row", "")] += 1
    for n, k in key.items():
        if k["kind"].startswith("control-") and seen.get(n, 0) != 1:
            ctrl_ok = False
            notes.append(f"row {n} {k['kind'][len('control-'):]} control: "
                         f"{'missing from the return' if not seen.get(n) else 'returned ' + str(seen[n]) + ' times'} (missed)")
    for n, c in seen.items():
        if c > 1 and n in key and not key[n]["kind"].startswith("control-"):
            # copies of one row may disagree (round 2: B = yes, then B = no); none is recorded until the reviewer
            # sends one answer
            unreadable.append(f"row {n}: returned {c} times; not recorded until one answer is sent")
    for r in rows:
        k = key.get(r.get("row", ""))
        if k and seen.get(r.get("row", "")) != 1:
            continue   # a missing or doubled control, or a doubled row: reported above
        if not k:
            unreadable.append(f"row {r.get('row')}: not in the answer key")
            continue
        A, B, C = norm(r.get("A location")), norm(r.get("B identity")), (r.get("C comment") or "").strip()
        if k["kind"] == "compare":
            A, how = compare_answer(A, C, k)
            if how:
                C = f"{C}; A read as {A}{how}"
            if A not in VALID_COMPARE:
                unreadable.append(f"row {r['row']} column A: '{A}' (a compare row is answered blue, orange or cannot tell)")
            C = f"{C}; blue {k.get('blue') or '?'}, orange {k.get('orange') or '?'}".lstrip("; ")
        else:
            for col, v in (("A", A), ("B", B)):
                if v not in VALID:
                    unreadable.append(f"row {r['row']} column {col}: '{v}'")
                elif not v and k["kind"] == "cell":   # a table row asks both questions
                    unreadable.append(f"row {r['row']} column {col}: empty (a table row is answered in A and B)")
        if k["kind"] == "control-location":
            ok = A == "no"
            ctrl_ok &= ok
            notes.append(f"row {r['row']} location control: A = '{A or 'empty'}' ({'caught' if ok else 'missed'})")
            continue
        if k["kind"] in ("control-identity", "control-value"):   # control-value: a table cell's value check (D-050)
            ok = B == "no"
            ctrl_ok &= ok
            what = "value" if k["kind"] == "control-value" else "identity"
            notes.append(f"row {r['row']} {what} control: B = '{B or 'empty'}' ({'caught' if ok else 'missed'})")
            continue
        obj = f"{k['figure_id']}/{k['panel']}/{k['series_id']}/{k['point_kind']}/{k['source']}/{k['sequence']}"
        kind = k["kind"]
        if kind == "symbol" and (obj, "identity", k["chunk"]) in voided:
            # the reviewer was shown something that made the identity question unanswerable (wave 2 showed
            # FC-7B and FC-7C upside down); the location answer stands, B is kept in the note only
            kind = "position only"
            C = f"{C}; identity answer B = '{B or 'empty'}' void (qa/audits/voided.csv)".lstrip("; ")
        if kind == "cell" and (A, B) != ("yes", "yes"):
            C = f"{C}; A = {A or 'empty'}, B = {B or 'empty'}".lstrip("; ")   # which question failed, for the digest
        answers.append({"object": obj, "batch": k["batch"], "kind": kind, "A": A, "B": B, "C": C,
                        "verdict": verdict(kind, A, B), "row": r["row"]})
    return ctrl_ok, notes, answers, unreadable


def status_board(assign, log, audits, today, people, left=None, withdrawn=frozenset()):
    """The board: per reviewer and per chunk; left maps a reviewer who left the program to the date;
    withdrawn holds (reviewer, letter) assignments taken back before a return (qa/audits/withdrawn.csv),
    which no longer count as that reviewer's chunks."""
    left = left or {}
    returned = {(r["reviewer"], r["letter"]): r for r in log}
    out = ["| reviewer | returned | overdue | controls passed | next due |", "|---|---|---|---|---|"]
    for who in people:
        mine = [(a["letter1"] if a["reviewer1"] == who else a["letter2"], a) for a in assign if who in (a["reviewer1"], a["reviewer2"])]
        mine = [(l, a) for l, a in mine if (who, l) not in withdrawn]
        mine.sort(key=lambda x: (len(x[0]), x[0]))   # Z before AA
        got = [l for l, _ in mine if (who, l) in returned]
        over = [l for l, a in mine if (who, l) not in returned and a["deadline"] < today]
        passed = [l for l in got if returned[(who, l)]["controls"] in ("passed", "accepted")]
        pending = [(a["deadline"], l) for l, a in mine if (who, l) not in returned]
        if who in left:
            # nothing more is expected from this reviewer; the open chunks stand with one review (D-033, D-036)
            out.append(f"| {who} | {len(got)}/{len(mine)} | left {left[who]} | {len(passed)}/{len(got)} |  |")
            continue
        nxt = ""
        if pending:
            d = min(x[0] for x in pending)
            nxt = f"{d}: " + " ".join(l for dd, l in pending if dd == d)
        out.append(f"| {who} | {len(got)}/{len(mine)} | {len(over)}{' (' + ' '.join(over) + ')' if over else ''} | {len(passed)}/{len(got)} | {nxt} |")
    out += ["", "| chunk | reviewers | deadline | returned | pair outcomes |", "|---|---|---|---|---|"]
    by_obj = defaultdict(dict)
    for r in audits:
        by_obj[r["object"]][r["auditor"]] = r["outcome"]
    for a in assign:
        revs = [(w, l) for w, l in ((a["reviewer1"], a["letter1"]), (a["reviewer2"], a["letter2"])) if w]
        got = [f"{w}-{l}" for w, l in revs if (w, l) in returned]
        tally = defaultdict(int)
        for obj, who_v in by_obj.items():
            if obj in a.get("_objects", ()):  # filled in main from the keys
                # every reviewer of the point counts: a second-review chunk completes the chunk it repeats
                tally[pair_outcome(list(who_v.values()))] += 1
        tal = ", ".join(f"{k} {v}" for k, v in sorted(tally.items())) or "-"
        name = a["chunk"] + (f" (second review of {a['repeats']})" if a.get("repeats") else "")
        shown = " ".join(f"{w}-{l}" + (" (withdrawn)" if (w, l) in withdrawn else "") for w, l in revs)
        out.append(f"| {name} | {shown} | {a['deadline']} | {' '.join(got) or '-'} | {tal} |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--returns", help="folder of checklist-<INIT>-<L>.csv files (default qa/audits/returns)")
    ap.add_argument("--returned", nargs="*", default=[], help="INIT-L=path for a misnamed file")
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--accept", nargs="*", default=[], help="INIT-L returns to record although a control was missed")
    ap.add_argument("--decline", nargs="*", default=[], help="INIT-L returns with a missed control that Dan declined")
    ap.add_argument("--digest", action="store_true", help="also write qa/audits/digests/<date>.md")
    ap.add_argument("--qa-root", default=str(ROOT / "qa"))
    ap.add_argument("--out", help="report path (default qa/audits/reports/ingest-<date>.md)")
    a = ap.parse_args()
    qa = Path(a.qa_root)
    audits_dir = qa / "audits"
    returns_dir = Path(a.returns) if a.returns else audits_dir / "returns"
    assign = load(audits_dir / "assignments.csv")
    # a second-review chunk has one reviewer (reviewer2 empty)
    chunk_of = {(r[f"reviewer{i}"], r[f"letter{i}"]): r for r in assign for i in (1, 2) if r[f"reviewer{i}"]}
    people = sorted({r[k] for r in assign for k in ("reviewer1", "reviewer2")} - {""})
    left = {r["initials"]: r["left"] for r in load(audits_dir / "reviewers.csv") if r.get("left")}
    audits = load(qa / "audits.csv")
    existing = {(r["object"], r["auditor"]) for r in audits}
    log = {(r["reviewer"], r["letter"]): r for r in load(audits_dir / "returns-log.csv")}
    voided = {(r["object"], r["column"], r["chunk"]) for r in load(audits_dir / "voided.csv")}
    # an assignment taken back before its return (D-047): its points are asked again in a later chunk, so
    # a late return of the old packet is not recorded
    withdrawn = {(r["reviewer"], r["letter"]) for r in load(audits_dir / "withdrawn.csv")}

    files = []
    if returns_dir.exists():
        for p in sorted(returns_dir.glob("checklist-*-*.csv")):
            # after Z a reviewer's chunks go on as AA, AB (make_audit_packet.letter_of, wave 7)
            m = re.fullmatch(r"checklist-([A-Za-z]+)-([A-Z]{1,3})\.csv", p.name)
            if m:
                files.append((m.group(1).upper(), m.group(2), p))
            else:
                print(f"skipped (name not checklist-<INIT>-<L>.csv): {p.name}")
    for item in a.returned:
        tag, path = item.split("=", 1)
        who, letter = tag.split("-")
        files.append((who.upper(), letter.upper(), Path(path)))
    # in chunk order, Z before AA: a point answered in two of one reviewer's chunks is recorded from the earlier
    # chunk first (a lexical file listing put AA before Z; Codex's review, 2026-11-18)
    files.sort(key=lambda f: (f[0], len(f[1]), f[1]))

    rep = [f"# Audit returns, {a.date}", ""]
    new_rows, run_verdicts = [], defaultdict(dict)  # object -> auditor -> verdict (this run, recorded ones)
    problems, unreadable_all = [], []
    for who, letter, path in files:
        ch = chunk_of.get((who, letter))
        if not ch:
            rep += [f"## {who}-{letter}: no such chunk in assignments.csv (file {path.name})", ""]
            continue
        if (who, letter) in withdrawn:
            rep += [f"## {who}-{letter} (chunk {ch['chunk']}): assignment withdrawn (qa/audits/withdrawn.csv); not recorded", ""]
            continue
        key = {k["row"]: k for k in load(audits_dir / "keys" / f"key-{who}-{letter}.csv")}
        if not key:
            rep += [f"## {who}-{letter}: answer key missing", ""]
            continue
        rows = load(path)
        ctrl_ok, notes, answers, unreadable = score_return(rows, key, voided)
        prev = log.get((who, letter))  # logged by an earlier run
        accepted = f"{who}-{letter}" in a.accept or (prev or {}).get("controls") == "accepted"
        declined = f"{who}-{letter}" in a.decline or (prev or {}).get("controls") == "declined"
        state = "passed" if ctrl_ok else ("accepted" if accepted else ("declined" if declined else "missed"))
        rep += [f"## {who}-{letter} (chunk {ch['chunk']}, {ch['figures']})", "",
                f"Controls: {state}" + (f", answers not recorded until accepted (--accept {who}-{letter})" if state == "missed" else "")
                + (", answers never recorded; the points wait for another reviewer" if state == "declined" else "") + ".", ""]
        rep += [f"- {n}" for n in notes] + [""]
        unreadable_all += [f"{who}-{letter} {u}" for u in unreadable]
        recorded = 0
        if state not in ("missed", "declined"):
            for ans in answers:
                run_verdicts[ans["object"]][who] = ans["verdict"]
                if ans["verdict"] == "problem":
                    problems.append((ans["object"], who, letter, ans["C"]))
                if (ans["object"], who) not in existing:
                    existing.add((ans["object"], who))  # two returns of one run can hold the same point
                    new_rows.append({"batch": ans["batch"], "object": ans["object"],
                                     "column": {"symbol": "position+identity", "cell": "position+value"}.get(ans["kind"], "position"),
                                     "auditor": who, "date": a.date, "outcome": ans["verdict"],
                                     "note": f"chunk {ch['chunk']} ({who}-{letter})" + (f"; {ans['C']}" if ans["C"] else "")})
                    recorded += 1
        # a re-run over the whole returns folder keeps each logged return's date, acceptance and count; until
        # 2026-11-05 it reset them, which turned an accepted return back into a missed one
        log[(who, letter)] = {"reviewer": who, "letter": letter, "chunk": ch["chunk"],
                              "received": prev["received"] if prev else a.date, "rows": len(rows),
                              "controls": state, "unreadable": len(unreadable),
                              "recorded": int(prev["recorded"]) + recorded if prev else recorded}
        # pair outcomes for this chunk's points: this return with every other reviewer of the point, from
        # this run or from audits.csv (until wave 3 only the chunk partner, which missed the reviewers of
        # the chunk a second-review chunk repeats)
        prior = defaultdict(dict)
        for r in audits:
            if r["auditor"] != who:
                prior[r["object"]][r["auditor"]] = r["outcome"]
        tally = defaultdict(int)
        table = []
        for ans in answers:
            vs = [ans["verdict"]] if state not in ("missed", "declined") else []
            others = {**prior[ans["object"]], **{w: v for w, v in run_verdicts.get(ans["object"], {}).items() if w != who}}
            vs += list(others.values())
            oc = pair_outcome(vs)
            tally[oc] += 1
            if oc not in ("confirmed",) and not oc.startswith("single (ok)"):
                table.append(f"| {ans['object']} | {ans['kind']} | A {ans['A'] or '-'}, B {ans['B'] or '-'}{(' (' + ans['C'] + ')') if ans['C'] else ''} | {oc} |")
        rep += ["Outcomes: " + ", ".join(f"{k} {v}" for k, v in sorted(tally.items())) + "."]
        if table:
            rep += ["", "| point | kind | this reviewer | pair outcome |", "|---|---|---|---|"] + table
        rep.append("")

    if problems:
        rep += [f"## Points marked as a problem by a reviewer whose controls passed ({len(problems)}); re-read on the scan", ""]
        rep += [f"- {o} ({who}-{l}{': ' + c if c else ''})" for o, who, l, c in problems] + [""]
    if unreadable_all:
        rep += ["## Unreadable answers", ""] + [f"- {u}" for u in unreadable_all] + [""]

    if a.write:
        if new_rows:
            write_csv(qa / "audits.csv", audits + new_rows, AUDIT_FIELDS)
        write_csv(audits_dir / "returns-log.csv", sorted(log.values(), key=lambda r: (r["reviewer"], len(r["letter"]), r["letter"])), LOG_FIELDS)
        audits = audits + new_rows
        print(f"{len(new_rows)} new audit rows written, {sum(1 for r in log.values()) } returns logged")
    else:
        print(f"{len(new_rows)} audit rows would be written (no --write)")

    # objects per chunk, from the keys, for the board
    for ch in assign:
        objs = set()
        for i in (1, 2) if ch["reviewer2"] else (1,):
            for k in load(audits_dir / "keys" / f"key-{ch[f'reviewer{i}']}-{ch[f'letter{i}']}.csv"):
                if not k["kind"].startswith("control"):
                    # the same id as score_return; without the source (added to the id 2026-10-14) no audit row
                    # matched and the board's pair outcomes read "-" for every chunk until 2026-11-05
                    objs.add(f"{k['figure_id']}/{k['panel']}/{k['series_id']}/{k['point_kind']}/{k['source']}/{k['sequence']}")
        ch["_objects"] = objs
    board = status_board(assign, list(log.values()), audits, a.date, people, left, withdrawn)
    rep += ["## Status board", "", board, ""]
    text = "\n".join(rep) + "\n"
    out = Path(a.out) if a.out else audits_dir / "reports" / f"ingest-{a.date}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8", newline="\n")
    (audits_dir / "status.md").write_text(f"# Audit status, {a.date}\n\n{board}\n", encoding="utf-8", newline="\n")
    if a.digest:
        d = audits_dir / "digests" / f"{a.date}.md"
        d.parent.mkdir(parents=True, exist_ok=True)
        flagged = [r for r in audits if r["outcome"] == "problem"]
        dig = [f"# Audit digest, {a.date}", "", board, "", f"## Points marked as a problem so far ({len(flagged)})", ""]
        dig += [f"- {r['object']} ({r['auditor']}, {r['date']}): {r['note']}" for r in flagged] + [""]
        if unreadable_all:
            dig += ["## Unreadable answers in this run", ""] + [f"- {u}" for u in unreadable_all] + [""]
        d.write_text("\n".join(dig) + "\n", encoding="utf-8", newline="\n")
        print(f"digest written to {d}")
    print(f"report written to {out}")
    print(board)
    return 0


if __name__ == "__main__":
    sys.exit(main())
