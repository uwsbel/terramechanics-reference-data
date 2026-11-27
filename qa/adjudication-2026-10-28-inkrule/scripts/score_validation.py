"""Score the frozen off-ink check (D-031 v1) against the blind validation adjudication.

Truth per item is the adjudicators' agreement: both `yes` (on the line's own ink), both `no` (off it), or
unsettled (they differ or either cannot tell). Per stratum: how the check's verdicts meet the settled truth.
Population estimates weight each stratum by its size in all batches (the sample is stratified, not uniform).

Usage: score_validation.py <key_csv> <codex_answers> <claude_answers> [<claude_answers> ...] [--out <csv>]
"""
import argparse, csv
from collections import Counter, defaultdict

POP = {"excluded": 920, "eligible-near": 1529, "eligible-far": 11994, "review": 296}  # sizes at sampling (v1)


def load(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def norm(a):
    a = " ".join((a or "").strip().lower().strip("`'\"").split())
    return "cannot tell" if a in ("can't tell", "cant tell", "unclear", "not sure") else a


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("key"); ap.add_argument("codex"); ap.add_argument("claude", nargs="+")
    ap.add_argument("--out")
    a = ap.parse_args()
    key = {r["item"]: r for r in load(a.key)}
    cx = {r["item"].zfill(3): norm(r["A"]) for r in load(a.codex)}
    cl = {r["item"].zfill(3): norm(r["A"]) for f in a.claude for r in load(f)}
    rows, tab = [], defaultdict(Counter)
    for it, k in sorted(key.items()):
        c, x = cl.get(it, "missing"), cx.get(it, "missing")
        truth = "on" if c == x == "yes" else "off" if c == x == "no" else "unsettled"
        tab[k["stratum"]][truth] += 1
        rows.append(dict(k, claude=c, codex=x, truth=truth))
    print(f"answers: Claude {len(cl)}, Codex {len(cx)}; agreement {sum(r['truth'] != 'unsettled' for r in rows)} of {len(rows)}")
    print(f"{'stratum':15}{'n':>5}{'on':>6}{'off':>6}{'unsettled':>11}")
    for st in POP:
        t = tab[st]; print(f"{st:15}{sum(t.values()):>5}{t['on']:>6}{t['off']:>6}{t['unsettled']:>11}")
    # the check's errors on settled items
    exc = tab["excluded"]; near, far = tab["eligible-near"], tab["eligible-far"]
    fe = exc["on"]; settled_exc = exc["on"] + exc["off"]
    print(f"\nfalse exclusions (excluded, both say on the line): {fe} of {settled_exc} settled exclusions"
          + (f" = {100 * fe / settled_exc:.1f}%" if settled_exc else ""))
    print(f"misses near symbols (passed, both say off): {near['off']} of {near['on'] + near['off']} settled")
    print(f"misses elsewhere (passed, both say off): {far['off']} of {far['on'] + far['off']} settled")
    # population estimates from the settled share of each stratum
    est = {}
    for st, n in POP.items():
        t = tab[st]; s = t["on"] + t["off"]
        est[st] = (n * t["off"] / s if s else 0.0, n * t["on"] / s if s else 0.0)
    off_total = sum(v[0] for v in est.values())
    caught = est["excluded"][0]
    print(f"\nestimated off-line samples in all batches: {off_total:.0f}; caught by exclusion {caught:.0f} "
          f"({100 * caught / off_total:.0f}% recall), in review {est['review'][0]:.0f}, "
          f"missed {est['eligible-near'][0] + est['eligible-far'][0]:.0f}; estimated good samples excluded {est['excluded'][1]:.0f}")
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n"); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    main()
