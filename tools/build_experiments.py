"""Build data/experiments/index.csv from two blind experiment inventories.

Usage:
    python tools/build_experiments.py <claude.csv> <codex.csv> <qa_dir> data/experiments/index.csv
    python tools/build_experiments.py --batch <claude.csv> <codex.csv> <qa_dir> [--batch ...] \
        --out data/experiments/index.csv

With several batches (Volume I Section II, then Volume II Appendix C, ...) each is reconciled as
below and the rows are stacked in batch order. A later batch's row whose id is already in the index
(the same test or derived series printed again, relation `same-as`) is merged into the earlier row:
its evidence is added, the earlier row's cells stand, and every cell where the two volumes differ
is listed in the sidecar (`merged_rows`) and noted on the row. The columns `relation` and
`relation_target` (vocabulary `same-as | derived-from` or empty) are reconciled like the other
columns when a batch's submissions carry them, with one rule: a relation stated by one agent and
left empty by the other stands (absence of a relation is not a reading of one), status `rule`.

<qa_dir> holds three small files that record every human or rule decision:

- id-aliases.json: {submission_id: canonical_id} for rows one agent named differently from the
  documented id scheme. Applied before matching.
- row-decisions.csv: experiment_id, decision (include | exclude), reason. Required for every row
  present in only one submission; a one-sided row without a decision is reported and the script
  exits 1.
- resolutions.csv: experiment_id, column, value, status, note. Consulted for any reconciled cell
  the normalizers and pattern rules below do not settle.

Reconciled columns: kind, test_type, soil_family, soil_no, soil_no_status, dr_printed,
unit_weight_printed_pcf, gp_printed_g, penetrator_printed, bin_printed_in, rate_printed,
start_depth_printed_in, setup_status, mcc_relevant, priority. Two readings agree when equal after
normalization (spelling of units and penetrators, "approx" for the printed symbol, leading zeros,
"min a; max b" written "a to b"); the normalized form is what the index carries, with status
`agreed` or `normalized`. Pattern rules, status `rule`:

1. soil_no: when the readings differ and one is empty, the index carries no soil number and
   soil_no_status is `unknown`. A nominal soil number both agents did not assign is not assigned.
   Any row without a soil number has soil_no_status `unknown`.
2. dr_printed: an axis range (0 to 1.0) is not a printed relative density; it is dropped.
3. start_depth_printed_in: a series row (not kind single) carries no start depth unless both
   agents printed one.
4. setup_status: a series row read `pending` by one agent and `setup_incomplete` by the other is
   `pending`, the documented meaning for series whose underlying tests are not identified; a
   sample row so split is `setup_incomplete` (sample mass and sieve set are never given).
5. penetrator, bin and rate: a value one agent took from the text and the other left empty stands,
   status `one-sided-cell`, and such cells are listed for the audit sample.

Descriptive columns are not reconciled: state_printed and test_label_printed come from the second
submission (which kept the printed wording more strictly), apparatus, loading and
measured_channels from the first; evidence is the union of both lists; both notes are kept; the
sidecar lists the other agent's value for every descriptive cell that differs. From 2026-11-20 a row
of resolutions.csv for a descriptive column replaces that default with a value checked against the
page (batch experiments-t5-3-b1, after Codex's review: a fact only one reading states should not
enter the index unchecked).
"""

import csv
import json
import re
import sys
from pathlib import Path

RECONCILED = ["kind", "test_type", "soil_family", "soil_no", "soil_no_status", "dr_printed",
              "unit_weight_printed_pcf", "gp_printed_g", "penetrator_printed", "bin_printed_in",
              "rate_printed", "start_depth_printed_in", "setup_status", "mcc_relevant", "priority"]
FROM_B = ["state_printed", "test_label_printed"]
FROM_A = ["apparatus", "loading", "measured_channels"]
SERIES_KINDS = {"averaged-series", "derived-series", "correlation", "summary"}
WORDS = {"one": "1", "two": "2", "four": "4", "six": "6", "eight": "8"}


def read(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def lead_zero(s):
    return re.sub(r"(?<![\d.])\.(\d)", r"0.\1", s)


def norm_common(s):
    s = s.strip().replace("≈", "approx").replace("±", "plus or minus")
    s = re.sub(r"(\d)\s*'", r"\1 ft", s)
    s = re.sub(r"\babout\b|\bapproximately\b", "approx", s, flags=re.I)
    s = re.sub(r'(\d)\s*"', r"\1 inch", s)
    s = re.sub(r"\b(in\.|in|inches|inch)\b", "inch", s, flags=re.I)
    for w, d in WORDS.items():
        s = re.sub(rf"\b{w}\b", d, s, flags=re.I)
    s = re.sub(r"\s+", " ", s)
    return lead_zero(s)


def norm_rate(s):
    s = norm_common(s)
    s = re.sub(r"(?<!\d)\.|\.(?!\d)", "", s)   # drop the periods of In. and Min.
    m = re.search(r"(approx\s*)?(\d+/\d+|\d*\.?\d+)\s*inch\s*(?:/|per)\s*min", s.split(";")[0], flags=re.I)
    if not m:
        # not a push rate in in/min: keep every clause (a model drop prints V_v and V_h, separated by ';'; until
        # 2026-11-20 the text after the first ';' was dropped) and write In./Sec. as in/s, the unit the site converts
        return re.sub(r"\binch\s*/\s*sec\b", "in/s", s, flags=re.I)
    v = m.group(2)
    if "/" in v:
        a, b = v.split("/")
        v = str(float(a) / float(b)).rstrip("0").rstrip(".")
    return f"{'approx ' if m.group(1) else ''}{v} in/min"


def norm_bin(s):
    nums = re.findall(r"\d+(?:\.\d+)?", s)
    # a bed printed in feet keeps its unit (the model-drop bed, 18 by 12 ft; the full-scale pit, 12 by 18 by 5 ft):
    # without it the numbers read as inches, 12 times too small (Codex's review, 2026-11-19)
    if (len(nums) >= 2 and re.search(r"\bf(?:ee|oo)t\b|-foot|\bft\b", s, flags=re.I)
            and re.search(r"\bby\b|\blong\b|\bwide\b", s, flags=re.I)):   # dimensions, not a volume ('1/30 cu ft')
        if re.search(r"\binch|\bin\b|\"", s, flags=re.I):   # feet and inches mixed: keep the text as printed
            return norm_common(s)
        return " by ".join(nums[:3]) + " ft"
    if len(nums) >= 2 and re.search(r"\bby\b|x|inch", s, flags=re.I):
        return f"{nums[0]} by {nums[1]}"
    return norm_common(s)


def norm_penetrator(s):
    s = norm_common(s).lower()
    s = re.sub(r"\b(diameter|dia)\.?(?=\s|$|;)", "", s)
    s = re.sub(r"\bcyl\.?(?=\s|$)", "cylinder", s)
    s = re.sub(r"\bfp\b", "footpad", s)
    s = re.sub(r"-inch", " inch", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def norm_uw(s):
    s = norm_common(s)
    m = re.fullmatch(r"min\s*([\d.]+);\s*max\s*([\d.]+)", s, flags=re.I)
    if m:
        return f"{m.group(1)} to {m.group(2)}"
    return re.sub(r"\s*\([^)]*\)", "", s).strip()


def norm_generic(s):
    return norm_common(s).lower()


BATCH_SOURCE = {   # what each later batch covers, for the sidecar's source line
    "experiments-vol2c-b1": "Vol. II, Appendix C (PDF 115 to 159)",
    "experiments-vol2ab-b1": "Vol. II, Appendices A and B",
    "experiments-s3s5-b1": "Vol. I, Sections IV and V, the impact runs and model drops with histories (PDF 186 to 212, 280 to 344)",
    "experiments-drag-b1": "Vol. I, Section IV, the subscale drag tables (PDF 189 to 205, with Sections II and III for the setup)",
    "experiments-t5-3-b1": "Vol. I, Section V, Table 5-T3, the detail correlation drops (PDF 325, with Section V for the setup)",
}


def codex_model(batch):
    """The Codex model a batch's run recorded, or `gpt-6.1-sol high` (the model of the batches before run records)."""
    m = Path(__file__).resolve().parents[1] / "extractions" / "codex" / batch / "meta.json"
    if m.exists():
        j = json.loads(m.read_text(encoding="utf-8-sig"))
        return f"{j.get('model', '?')} {j.get('reasoning_effort', '')}".strip()
    return "gpt-6.1-sol high"


NORMALIZERS = {"rate_printed": norm_rate, "bin_printed_in": norm_bin, "penetrator_printed": norm_penetrator,
               "unit_weight_printed_pcf": norm_uw, "dr_printed": lambda s: norm_common(s).lower(),
               "gp_printed_g": norm_common}


def reconcile(a_path, b_path, qa_dir):
    """One batch: (rows, cells, alternates, excluded, problems, has_relations)."""
    qa = Path(qa_dir)
    aliases = json.loads((qa / "id-aliases.json").read_text(encoding="utf-8"))
    decisions = {r["experiment_id"]: r for r in read(qa / "row-decisions.csv")}
    res = {(r["experiment_id"], r["column"]): r for r in read(qa / "resolutions.csv")}
    A = {aliases.get(r["experiment_id"], r["experiment_id"]): r for r in read(a_path)}
    B = {aliases.get(r["experiment_id"], r["experiment_id"]): r for r in read(b_path)}
    has_rel = all("relation" in next(iter(D.values())) for D in (A, B))
    if has_rel:   # a relation target is a list of ids: alias each one, and the order of the list does not matter
        for D in (A, B):
            for r in D.values():
                ids = [aliases.get(x.strip(), x.strip()) for x in r["relation_target"].split(";") if x.strip()]
                r["relation_target"] = ";".join(sorted(dict.fromkeys(ids)))
    ids = sorted(set(A) | set(B))
    rows, cells, alternates, excluded, problems = [], [], [], [], []
    for i in ids:
        a, b = A.get(i), B.get(i)
        if a is None or b is None:
            d = decisions.get(i)
            if d is None:
                problems.append(f"one-sided row without decision: {i} ({'claude' if a else 'codex'} only)")
                continue
            if d["decision"] == "exclude":
                excluded.append({"experiment_id": i, "from": "claude" if a else "codex", "reason": d["reason"]})
                continue
            src = a or b
            row = {k: src[k] for k in src}
            for col, f in NORMALIZERS.items():   # one-sided rows get the same spelling as the rest
                row[col] = f(row[col])
            row["experiment_id"] = i
            row["status"] = "one-sided"
            row["notes_claude"], row["notes_codex"] = (a or {}).get("notes", ""), (b or {}).get("notes", "")
            rows.append(row)
            cells.append({"experiment_id": i, "cell_status": {"row": "one-sided: " + d["reason"]}})
            continue
        row, status = {"experiment_id": i, "source_id": a["source_id"]}, {}
        for col in RECONCILED + (["relation", "relation_target"] if has_rel else []):
            va, vb = a[col].strip(), b[col].strip()
            f = NORMALIZERS.get(col, norm_generic)
            na, nb = f(va), f(vb)
            if na.lower() == nb.lower():
                row[col], status[col] = (na if col in NORMALIZERS else va), ("agreed" if va == vb else "normalized")
                continue
            if col in ("relation", "relation_target") and "" in (va, vb):
                # a relation stated by one agent stands (absence of a relation is not a reading of one)
                row[col], status[col] = va or vb, "rule"
                continue
            if col == "dr_printed" and na.replace("approx", "").strip() == nb.replace("approx", "").strip():
                # One agent kept the printed approximately sign; the reading with it stands.
                row[col], status[col] = (na if "approx" in na else nb), "normalized"
                continue
            kind = res.get((i, "kind"), {}).get("value") or (a["kind"] if a["kind"] == b["kind"] else "")
            if col in ("penetrator_printed", "bin_printed_in", "rate_printed") and "" in (va, vb):
                # One agent found the setup fact in the text and the other left it empty: the
                # fact stands, and the sidecar marks the cell so the audit sample can check it.
                row[col], status[col] = f(va or vb), "one-sided-cell"
            elif col == "soil_no" and ("" in (va, vb)):
                row[col], status[col] = "", "rule"
            elif col == "soil_no_status" and row.get("soil_no", "x") == "":
                row[col], status[col] = "unknown", "rule"
            elif col == "dr_printed" and {re.sub(r"\s", "", na), re.sub(r"\s", "", nb)} & {"0to1.0", "0to1", ""} and ("" in (na, nb)):
                row[col], status[col] = "", "rule"
            elif col == "start_depth_printed_in" and kind in SERIES_KINDS and "" in (va, vb):
                row[col], status[col] = "", "rule"
            elif col == "setup_status" and {va, vb} == {"pending", "setup_incomplete"} and kind in SERIES_KINDS:
                row[col], status[col] = "pending", "rule"
            elif col == "setup_status" and {va, vb} == {"pending", "setup_incomplete"} and kind == "sample":
                row[col], status[col] = "setup_incomplete", "rule"
            elif (i, col) in res:
                row[col], status[col] = res[(i, col)]["value"], res[(i, col)]["status"]
            else:
                row[col], status[col] = "", "pending-review"
                problems.append(f"{i}.{col}: claude={va!r} codex={vb!r}")
        for col in FROM_B:
            row[col] = b[col]
        for col in FROM_A:
            row[col] = a[col]
        for col in FROM_A + FROM_B:
            if norm_generic(a[col]) != norm_generic(b[col]):
                alternates.append({"experiment_id": i, "column": col, "claude": a[col], "codex": b[col]})
            if (i, col) in res:   # a recorded resolution replaces the one-reader default (from 2026-11-20, Codex's review)
                row[col], status[col] = res[(i, col)]["value"], res[(i, col)]["status"]
        ev = []
        for v in (a["evidence"] + ";" + b["evidence"]).split(";"):
            v = v.strip()
            if v and v not in ev:
                ev.append(v)
        row["evidence"] = ";".join(sorted(ev, key=lambda t: (not t[0] in "FT", t)))
        status["evidence"] = "agreed" if a["evidence"] == b["evidence"] else "merged"
        row["notes_claude"], row["notes_codex"] = a["notes"], b["notes"]
        kinds = set(status.values())
        row["status"] = ("agreed" if kinds <= {"agreed", "normalized"} else
                         "pending-review" if "pending-review" in kinds else "resolved")
        rows.append(row)
        cells.append({"experiment_id": i, "cell_status": status,
                      "resolution_notes": {c: res[(i, c)]["note"] for c in status if (i, c) in res}})

    return rows, cells, alternates, excluded, problems, has_rel


def main(batches, out_path) -> int:
    rows, cells, alternates, excluded, problems, merged = [], [], [], [], [], []
    any_rel = False
    by_id = {}
    for a_path, b_path, qa_dir in batches:
        r_rows, r_cells, r_alt, r_exc, r_prob, has_rel = reconcile(a_path, b_path, qa_dir)
        any_rel |= has_rel
        cell_of = {c["experiment_id"]: c for c in r_cells}
        for r in r_rows:
            i = r["experiment_id"]
            if i in by_id:   # the same test or series printed again in a later volume: one row
                old = by_id[i]
                have = old["evidence"].split(";")
                old["evidence"] = ";".join(have + [e for e in r["evidence"].split(";") if e not in have])
                diffs = {c: {"kept": old.get(c, ""), "later": r.get(c, "")} for c in RECONCILED + FROM_A + FROM_B
                         if r.get(c, "") and norm_generic(old.get(c, "")) != norm_generic(r.get(c, ""))}
                merged.append({"experiment_id": i, "batch": Path(qa_dir).name, "evidence_added": r["evidence"],
                               "relation": r.get("relation", ""), "differences": diffs})
                printed = {c: v for c, v in diffs.items() if c in ("soil_family", "soil_no", "dr_printed",
                                                                    "unit_weight_printed_pcf", "gp_printed_g")}
                if printed:   # a printed fact that differs between volumes is noted on the row; wording stays in the sidecar
                    old["notes_claude"] = (old["notes_claude"] + f" | printed again ({Path(qa_dir).name}) with "
                                           + "; ".join(f"{c} {v['later']} (kept {v['kept']})" for c, v in printed.items())).strip(" |")
                continue
            by_id[i] = r
            rows.append(r)
            if i in cell_of:
                cells.append(cell_of[i])
        alternates += r_alt
        excluded += r_exc
        problems += r_prob

    fieldnames = ["experiment_id", "source_id", "kind", "test_type", "test_label_printed", "soil_family", "soil_no",
                  "soil_no_status", "state_printed", "dr_printed", "unit_weight_printed_pcf", "gp_printed_g",
                  "apparatus", "penetrator_printed", "bin_printed_in", "loading", "rate_printed",
                  "start_depth_printed_in", "measured_channels", "evidence", "setup_status", "mcc_relevant",
                  "priority"] + (["relation", "relation_target"] if any_rel else []) + ["status", "notes_claude", "notes_codex"]
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    first, later = batches[0], batches[1:]
    sidecar = {
        "file": out.name,
        "source": "Bendix AM-68-1 Vol. I, Section II (PDF 26 to 138) plus Table 1-1 (PDF 20)" + "".join(
            f"; {BATCH_SOURCE.get(Path(q).name, Path(q).name)}" for _, _, q in later),
        "method": "two independent experiment inventories from the page images (Claude, Codex gpt-6-astra high), "
                  "id aliasing, exact-match diff after normalization (tools/build_experiments.py), pattern rules, "
                  "resolutions and row decisions under qa/experiments-s2-b1/" + (
                      # each later batch with the Codex model its own run recorded (extractions/codex/<batch>/meta.json)
                      "; later batches: " + ", ".join(f"{q} (Codex {codex_model(Path(q).name)})" for _, _, q in later) if later else ""),
        "submissions": [str(first[0]), str(first[1])] + [str(x) for b in later for x in b[:2]],
        "rules": __doc__.split("Pattern rules, status `rule`:")[1].split("Descriptive columns")[0].strip(),
        "cells": cells, "excluded_rows": excluded, "descriptive_alternates": alternates,
    }
    if merged:
        sidecar["merged_rows"] = merged
    out.with_suffix(".json").write_text(json.dumps(sidecar, indent=2, ensure_ascii=False), encoding="utf-8")
    n = {k: sum(1 for r in rows if r["status"] == k) for k in ("agreed", "resolved", "one-sided", "pending-review")}
    print(f"wrote {out}: {len(rows)} rows {n}; excluded {len(excluded)}; alternates {len(alternates)}")
    for p in problems:
        print("  PENDING", p)
    return 1 if problems else 0


if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv and argv[0] == "--batch":
        batches, out = [], None
        while argv:
            if argv[0] == "--batch":
                batches.append(tuple(argv[1:4]))
                argv = argv[4:]
            elif argv[0] == "--out":
                out = argv[1]
                argv = argv[2:]
            else:
                sys.exit(f"unexpected argument {argv[0]}")
        sys.exit(main(batches, out))
    sys.exit(main([tuple(argv[0:3])], argv[3]))
