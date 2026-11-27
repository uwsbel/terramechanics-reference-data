"""Combine the two blind adjudications of the audit re-check with the key and the student reviews.

Each answer is first translated through the key into what it says about the kept reading:
  kept        the kept reading is right (compare: the mark chosen is the kept one; check: A yes and B yes)
  other       the other reading is right and the kept one is not (compare only)
  both        both readings are acceptable (compare only)
  neither     neither is (compare), or the kept reading fails its check (check: A no or B no)
  cannot tell
The Claude and Codex verdicts agree or split (D-023: agreement settles, a split goes to a second round).
For each agreed point the proposed action is: keep (kept, both), switch to the other reading (other),
re-read (neither), or leave as unresolved with a widened bound (cannot tell).

Usage: compare_recheck.py <key_csv> <claude_answers_csv> [<more claude csv> ...] --codex <codex_answers_csv> --out <dir>
"""
import argparse, csv, json
from collections import Counter
from pathlib import Path

VALID = {"p", "q", "both", "neither", "cannot tell", "yes", "no", ""}


def load(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def norm(v):
    v = " ".join((v or "").strip().lower().strip("`'\"").split())
    return "cannot tell" if v in ("can't tell", "cant tell", "unclear", "not sure") else v


def verdict(kind, k, ans):
    A, B = norm(ans.get("A")), norm(ans.get("B"))
    if kind.startswith("compare"):
        if A in ("p", "q"):
            return "kept" if k[A.upper()] == "kept" else "other"
        return A if A in ("both", "neither", "cannot tell") else f"unreadable:{A}"
    if kind == "check-marker":
        if "cannot tell" in (A, B):
            return "cannot tell"
        if A == "yes" and B == "yes":
            return "kept"
        if A in ("yes", "no") and B in ("yes", "no"):
            return "neither"
        return f"unreadable:{A}/{B}"
    if A == "yes":
        return "kept"
    if A == "no":
        return "neither"
    return "cannot tell" if A == "cannot tell" else f"unreadable:{A}"


ACTION = {"kept": "keep", "both": "keep", "other": "switch to the other reading", "neither": "re-read",
          "cannot tell": "unresolved (widen the bound)"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("key"); ap.add_argument("claude", nargs="+")
    ap.add_argument("--codex", required=True); ap.add_argument("--items", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    key = {r["item"]: r for r in load(a.key)}
    kind = {r["item"]: r["kind"] for r in load(a.items)}
    cl = {r["item"].strip().zfill(3): r for f in a.claude for r in load(f)}
    cx = {r["item"].strip().zfill(3): r for r in load(a.codex)}
    rows, tally, by_review = [], Counter(), Counter()
    for item in sorted(kind):  # the items of this round's packet (a second round holds a subset of the key)
        k = key[item]
        vc = verdict(kind[item], k, cl.get(item, {})) if item in cl else "missing"
        vx = verdict(kind[item], k, cx.get(item, {})) if item in cx else "missing"
        agree = vc == vx and not vc.startswith(("unreadable", "missing"))
        action = ACTION.get(vc, "") if agree else "second round"
        reviews = json.loads(k["reviews"])
        rows.append({"item": item, "object": k["object"], "kind": kind[item], "review_outcome": k["review_outcome"],
                     "reviews": " ".join(f"{a}:{v}" for a, v in sorted(reviews.items())),
                     "claude": vc, "codex": vx, "agree": "yes" if agree else "no", "action": action,
                     "claude_comment": cl.get(item, {}).get("comment", ""), "codex_comment": cx.get(item, {}).get("comment", "")})
        tally[action] += 1
        by_review[(k["review_outcome"], action)] += 1
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    fields = ["item", "object", "kind", "review_outcome", "reviews", "claude", "codex", "agree", "action", "claude_comment", "codex_comment"]
    with open(out / "recheck-results.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} items; Claude and Codex agree on {sum(r['agree'] == 'yes' for r in rows)}")
    print("actions:", dict(tally))
    for ro in ("flagged", "split", "both cannot tell", "single-problem"):
        print(f"  {ro:18}", {act: n for (r, act), n in sorted(by_review.items()) if r == ro})
    print("by kind:", dict(Counter((r["kind"], r["action"]) for r in rows)))


if __name__ == "__main__":
    main()
