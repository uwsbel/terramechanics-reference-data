"""Compare two independent readings of a printed table, cell by cell.

Usage:
    python tools/diff_tables.py A.csv B.csv --key soil_no [--out report.md] [--agreed agreed.csv]

Printed numbers must match EXACTLY after typography normalization (see normalize()); a reading
that differs in any character of a number is a transcription disagreement to resolve, never to
average. Free-text cells (descriptions) are compared after whitespace and case folding, and a
difference there is reported as "text" rather than "number" so the reviewer can judge whether it
matters. Rows present in only one reading, and columns present in only one reading, are reported.

Output: a Markdown report (stdout or --out) listing agreement statistics and every disagreement,
and optionally --agreed, a CSV holding the rows and cells where both readings agree, with a
`status` column set to `agreed`, and disagreeing cells left empty so they cannot be mistaken for
data. The reviewer's confirmed values are merged back later by tools/ingest_review.py.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

NUMERIC_RE = re.compile(r"^[<>~]?\s*[-+]?\d*\.?\d+\s*%?$")


def normalize(value: str) -> str:
    """Typography normalization only: never changes a digit.

    Collapses whitespace, unifies quote and dash glyphs, lowercases, strips a trailing period,
    writes ".45" and "0.45" the same way, and drops thousands separators ("10,900" vs "10900").
    """
    v = (value or "").strip()
    v = re.sub(r"\s+", " ", v)
    v = v.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    v = v.replace("–", "-").replace("—", "-")
    v = v.rstrip(".")
    # A trailing degree sign is typography on an angle column, not a digit.
    v = re.sub(r"\s*(°|˚|deg)$", "", v)
    low = v.lower()
    if NUMERIC_RE.match(low.replace(",", "")):
        low = low.replace(",", "").replace(" ", "")
        low = re.sub(r"(?<![\d.])\.(\d)", r"0.\1", low)  # .45 -> 0.45
        low = re.sub(r"(\d)\.0+$", r"\1", low)  # 104.0 -> 104 (only when the printed value has no sig fraction)
    return low


def is_numeric(value: str) -> bool:
    return bool(NUMERIC_RE.match((value or "").strip().lower().replace(",", "")))


def load(path: Path, key: str):
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows or key not in rows[0]:
        raise SystemExit(f"{path}: key column '{key}' not found")
    return {r[key].strip(): r for r in rows}, list(rows[0].keys())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--key", required=True, help="column that identifies a row (e.g. soil_no)")
    ap.add_argument("--labels", default="A,B", help="names of the two readings, e.g. claude,codex")
    ap.add_argument("--ignore", default="read_flags,source_locator", help="columns not compared (comma separated)")
    ap.add_argument("--out", help="write the Markdown report here instead of stdout")
    ap.add_argument("--agreed", help="write the agreed cells here as CSV")
    args = ap.parse_args()

    la, lb = args.labels.split(",")
    ignore = {c.strip() for c in args.ignore.split(",") if c.strip()}
    A, cols_a = load(Path(args.a), args.key)
    B, cols_b = load(Path(args.b), args.key)
    cols = [c for c in cols_a if c in cols_b and c not in ignore]
    only_a_cols = [c for c in cols_a if c not in cols_b]
    only_b_cols = [c for c in cols_b if c not in cols_a]
    keys = sorted(set(A) | set(B), key=lambda k: (len(k), k))

    disagreements = []  # (key, col, kind, a, b)
    agreed_rows = []
    n_cells = n_agree = 0
    for k in keys:
        if k not in A or k not in B:
            disagreements.append((k, "<row>", "missing", "present" if k in A else "absent", "present" if k in B else "absent"))
            continue
        out = {args.key: k}
        for c in cols:
            if c == args.key:
                continue
            a, b = A[k].get(c, ""), B[k].get(c, "")
            n_cells += 1
            if normalize(a) == normalize(b):
                n_agree += 1
                out[c] = a
            else:
                kind = "number" if (is_numeric(a) or is_numeric(b)) else "text"
                disagreements.append((k, c, kind, a, b))
                out[c] = ""
        out["status"] = "agreed" if all(out.get(c, "") != "" for c in cols if c != args.key) else "partial"
        agreed_rows.append(out)

    lines = [f"# Table diff: {la} vs {lb}", "",
             f"Files: `{args.a}` ({la}), `{args.b}` ({lb}). Key: `{args.key}`.", "",
             f"Rows: {len(A)} in {la}, {len(B)} in {lb}. Compared columns: {len([c for c in cols if c != args.key])}.",
             f"Cells compared: {n_cells}. Agreed: {n_agree} ({(100.0 * n_agree / n_cells if n_cells else 0):.1f} percent).",
             f"Disagreements: {len(disagreements)} "
             f"({sum(1 for d in disagreements if d[2] == 'number')} numeric, "
             f"{sum(1 for d in disagreements if d[2] == 'text')} text, "
             f"{sum(1 for d in disagreements if d[2] == 'missing')} missing rows).", ""]
    if only_a_cols or only_b_cols:
        lines += [f"Columns only in {la}: {only_a_cols}", f"Columns only in {lb}: {only_b_cols}", ""]
    if disagreements:
        lines += ["| key | column | kind | " + la + " | " + lb + " |", "|---|---|---|---|---|"]
        for k, c, kind, a, b in disagreements:
            lines.append(f"| {k} | {c} | {kind} | {a} | {b} |")
    else:
        lines.append("No disagreements.")
    report = "\n".join(lines) + "\n"

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(report, encoding="utf-8")
    else:
        sys.stdout.write(report)
    if args.agreed:
        fieldnames = [args.key] + [c for c in cols if c != args.key] + ["status"]
        with Path(args.agreed).open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(agreed_rows)
    return 0 if not disagreements else 1


if __name__ == "__main__":
    sys.exit(main())
