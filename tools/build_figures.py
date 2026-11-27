"""Build corpus/<source>/figures.csv from two blind inventory submissions and a resolutions file.

Usage:
    python tools/build_figures.py <claude.csv> <codex.csv> <resolutions.csv> <out.csv>
        [--aliases qa/<batch>/id-aliases.json] [--row-decisions qa/<batch>/row-decisions.csv]
        [--source "<what the index covers>"] [--batch <qa batch name>]

    Volume I Section II (the first batch) is built with the four positional arguments only;
    Volume II adds the alias file (Claude's table ids mapped to the page-locator ids) and the
    row-decisions file (rows present in one submission only).

Rules, all recorded in the sidecar figures.json:

1. Identity and classification columns (kind, printed_page, pdf_page, panels, curves, rotation,
   data_form, test_type, axis types, in_scope, priority, mcc_relevant, and when the batch has them
   appendix, relation, relation_target) are taken as is when the two submissions agree, status
   `agreed`. When they differ, the value comes from the resolutions file (status as recorded
   there: resolved, convention, rule, provisional); with no resolution the cell is left empty,
   status `pending-review`, and the script exits 1.
2. Vocabulary rules apply automatically before the resolutions file is consulted, status
   `vocabulary-resolved`: (a) a dimensionless axis read `linear` by one agent and `normalized` by
   the other is `normalized`; (b) an axis read `reciprocal ...` by one agent and `n/a` by the other
   is `reciprocal`; (c) a test_type read `other` or `apparatus` by one agent and a finer label by
   the other takes the finer label; (d) a relation read `none` by one agent and a stated relation
   by the other takes the stated relation (absence of a relation is not a reading of one), and
   relation_target follows it.
3. Units: `x_unit` and `y_unit` are normalized to the controlled list in UNIT_MAP after an axis
   multiplier such as "x 10^-3" or "(x 10^1)" is stripped (the multiplier belongs to the
   quantity, not the unit); the printed spelling is kept in `x_unit_as_printed` and
   `y_unit_as_printed` (from whichever submission kept the printed form; empty when the reader wrote a
   controlled code with an underscore, such as in_s, whose printed form is then in the notes). A normalized mismatch
   goes to the resolutions file like any other cell.
4. Descriptive text columns (title_as_printed, soils, states, apparatus, rate_or_dynamics,
   trace_classes, legend_entries, notes) are not reconciled: the first submission's text is used
   for all but legend_entries (second submission, which kept printed spelling), and the sidecar
   carries the other agent's value for every descriptive cell that differs. Both notes columns are
   kept in the CSV.
5. `transcribe` is `yes` for every row: the whole section is transcribed in phase b. `in_scope`
   keeps the narrow meaning (numbers to extract into data/).
6. A row present in one submission only enters the index only through the row-decisions file
   (decision `include`, status `one-sided-verified`, with the note saying how it was verified
   against the page image); its cells come from that submission, overridden by any resolution for
   that id. Without a decision the id is listed as missing and the script exits 1.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ID_COLS = ["kind", "printed_page", "pdf_page", "panels", "curves", "rotation", "data_form",
           "test_type", "x_axis_type", "y_axis_type", "in_scope", "priority", "mcc_relevant"]
OPTIONAL_ID_COLS = ["appendix", "section", "relation", "relation_target"]
UNIT_COLS = ["x_unit", "y_unit"]
DESC_COLS = ["title_as_printed", "soils", "states", "apparatus", "rate_or_dynamics", "trace_classes",
             "x_quantity", "y_quantity", "legend_entries"]

# Printed spelling (lower case, punctuation removed) -> controlled unit. "none" is the unit of a
# dimensionless or unitless axis; "n/a" marks a row with no axes at all (tables, photos).
UNIT_MAP = {
    "lb": "lb", "lbs": "lb", "pounds": "lb", "lbsx100": "lb",
    "in": "inch", "inch": "inch", "inches": "inch", "inchthousandths": "inch",
    "psf": "psf", "psi": "psi", "pcf": "pcf", "lbft3": "pcf", "poundsft3": "pcf",
    "g": "g", "gs": "g", "sec": "s", "seconds": "s", "s": "s", "mm": "mm", "percent": "percent",
    "deg": "deg", "degrees": "deg", "none": "none", "na": "n/a", "count": "none",
    "kipsin2": "ksi", "ksi": "ksi",
    # Volume I Sections III to V (inventory-s3s5-b1, 2026-11-19): time histories, rates and gage strain
    "milliseconds": "ms", "msec": "ms", "ms": "ms", "degree": "deg",
    "ftsec": "ft_s", "fps": "ft_s",
    "insec": "in_s", "inchsecond": "in_s", "inchseconds": "in_s", "inchessecond": "in_s", "inchesseconds": "in_s",
    "insec2": "in_s2", "inchsecond2": "in_s2", "inchseconds2": "in_s2", "inchesseconds2": "in_s2",
    "degsec": "deg_s", "degreessecond": "deg_s", "degreesseconds": "deg_s",
    "muinin": "ustrain", "microinin": "ustrain",
    # Volume I Section VI (inventory-s6-b1, 2026-11-20): pitch acceleration in degrees per second squared, printed
    # "Degrees Second^2", which no earlier batch met. A controlled code written by a reader (ft_s, in_s, deg_s2) is
    # matched as is in norm_unit, before punctuation is stripped: stripped, "in_s" would become "ins", which a
    # printed "Ins." (inches) also becomes (Codex's review, 2026-11-20)
    "degsec2": "deg_s2", "degreessecond2": "deg_s2", "degreesseconds2": "deg_s2",
}
UNIT_VOCAB = ["inch", "lb", "psf", "psi", "pcf", "g", "s", "mm", "percent", "deg", "none", "n/a"]
# units first met in a later batch: listed in a sidecar's vocabulary only when a row uses them, so the indexes
# built before them rebuild byte for byte
LATER_UNITS = ["ms", "ft_s", "in_s", "in_s2", "deg_s", "ustrain", "deg_s2"]
MULTIPLIER = re.compile(r"\(?\s*x\s*10\s*\^?\s*-?\d+\s*\)?|^\s*1,?000\s+")  # "x 10^3", "(x 10^1)", a leading "1,000"


def read(path, page_aliases=None):
    """Rows keyed by id. A page-qualified alias "<id>@<pdf_page>" renames a row of either submission before it
    is keyed, for an agent that gave several printed pages of one item the same id (Table 5-T2, PDF 308 to
    312, in inventory-s3s5-b1); without it the later rows would overwrite the first."""
    page_aliases = page_aliases or {}
    out = {}
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            i = r["id"].strip()
            i = page_aliases.get(f"{i}@{r['pdf_page'].strip()}", i)
            if i in out:
                sys.exit(f"{path}: id {i} appears twice; give its pages page-qualified aliases (id@pdf_page)")
            out[i] = r
    return out


def split_panels(s: str):
    """Split a unit string on semicolons outside parentheses ("psf; in." is two panels,
    "lb (printed as Lbs. x 100; see notes)" is one unit with a remark)."""
    parts, depth, cur = [], 0, ""
    for ch in s:
        depth += (ch == "(") - (ch == ")")
        if ch == ";" and depth <= 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return parts


def norm_unit(s: str):
    if (s or "").strip() in UNIT_VOCAB + LATER_UNITS:   # a controlled code as written (see UNIT_MAP)
        return s.strip()
    parts = split_panels(s or "")
    if len(parts) > 1:
        # Two-panel figure: one unit per panel, each normalized on its own (F2-21, FC-1B).
        normed = [norm_unit(p) for p in parts]
        return None if any(p is None for p in normed) else ";".join(normed)
    low = MULTIPLIER.sub("", (s or "").replace("μ", "mu").replace("²", "2").lower())
    head = low.split("(")[0]
    key = re.sub(r"[^a-z0-9]", "", head if re.search(r"[a-z]", head) else low)
    if "psf" in key and "inch" in key:          # two-panel data sheet written without a separator
        return "psf;inch"
    return UNIT_MAP.get(key)


# Spellings of a test type that both agents may use for the same thing, mapped to the vocabulary.
TEST_TYPE_MAP = {"drag test": "drag", "impact test": "impact", "dpt": "dynamic penetrometer",
                 "lpt": "load penetration", "sieve": "grain size", "density control": "density"}


def canon_test_type(s: str) -> str:
    return TEST_TYPE_MAP.get(s.strip().lower(), s.strip())


def vocab_rule(col, a, b):
    la, lb = a.strip().lower(), b.strip().lower()
    if col in ("x_axis_type", "y_axis_type"):
        if {la, lb} == {"linear", "normalized"}:
            return "normalized"
        if (la.startswith("reciprocal") and lb == "n/a") or (lb.startswith("reciprocal") and la == "n/a"):
            return "reciprocal"
    if col == "test_type":
        if la in ("other", "apparatus") and lb not in ("other", "apparatus"):
            return b.strip()
        if lb in ("other", "apparatus") and la not in ("other", "apparatus"):
            return a.strip()
    if col == "relation":
        if la in ("none", "") and lb not in ("none", ""):
            return b.strip()
        if lb in ("none", "") and la not in ("none", ""):
            return a.strip()
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("resolutions")
    ap.add_argument("out")
    ap.add_argument("--aliases", help="JSON mapping of first-submission ids to canonical ids")
    ap.add_argument("--row-decisions", help="CSV id,decision,status,note for rows present in one submission only")
    ap.add_argument("--source", default="Bendix AM-68-1 Vol. I, Section II (PDF 26 to 138) plus Table 1-1 (PDF 20)")
    ap.add_argument("--batch", default="inventory-s2-b1")
    ap.add_argument("--codex-model", default="gpt-6-astra high", help="the Codex model and effort of the second submission")
    ap.add_argument("--unit-codes", action="store_true",
                    help="the batch brief asked the readers for the controlled unit codes, not the printed spelling: "
                         "*_unit_as_printed stays empty (the printed form is in the notes); inventory-s6-b1 on")
    ap.add_argument("--base", help="an index of the same source built earlier by its own command; its rows come first")
    ap.add_argument("--corrections", help="CSV id,column,value,evidence,note: source-cited corrections applied last, "
                                          "for a value both inventories got wrong (recorded in the sidecar with the value replaced)")
    args = ap.parse_args()
    a_path, b_path, res_path, out_path = args.a, args.b, args.resolutions, args.out

    aliases = {}
    if args.aliases:
        aliases = {k: v for k, v in json.loads(Path(args.aliases).read_text(encoding="utf-8")).items()
                   if not k.startswith("_")}
    page_aliases = {k: v for k, v in aliases.items() if "@" in k}
    aliases = {k: v for k, v in aliases.items() if "@" not in k}
    A, B = read(a_path, page_aliases), read(b_path, page_aliases)
    if aliases:
        A = {aliases.get(k, k): v for k, v in A.items()}
    aliases.update(page_aliases)
    decisions = {}
    if args.row_decisions:
        with Path(args.row_decisions).open(encoding="utf-8-sig", newline="") as f:
            decisions = {r["id"]: r for r in csv.DictReader(f)}
    res = {}
    with Path(res_path).open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            res[(r["id"], r["column"])] = r
    a_cols = next(iter(A.values())).keys()
    b_cols = next(iter(B.values())).keys()
    extra_cols = [c for c in OPTIONAL_ID_COLS if c in a_cols and c in b_cols]
    id_cols = ID_COLS + extra_cols

    order = list(A) + [i for i in B if i not in A]      # the first submission's page order
    ids = [i for i in order if i in A and i in B]
    one_sided = [i for i in order if (i in A) != (i in B)]
    missing = sorted(i for i in one_sided if decisions.get(i, {}).get("decision") != "include")
    rows, cells, alternates, pending = [], [], [], 0

    def finish(i, row, status, a_notes, b_notes, row_status=None):
        row["transcribe"] = "yes"
        row["notes_claude"], row["notes_codex"] = a_notes, b_notes
        kinds = set(status.values())
        row["status"] = row_status or ("agreed" if kinds == {"agreed"} else "pending-review" if "pending-review" in kinds
                                       else "provisional" if "provisional" in kinds else "resolved")
        rows.append(row)
        cells.append({"id": i, "cell_status": status,
                      "resolution_notes": {c: res[(i, c)]["note"] for c in status if (i, c) in res}})

    for i in order:
        if i in ids:
            a, b = A[i], B[i]
            row, status = {"id": i}, {}
            relation_side = None
            for col in id_cols:
                va, vb = a[col].strip(), b[col].strip()
                if col == "test_type":
                    va, vb = canon_test_type(va), canon_test_type(vb)
                if col == "relation_target" and relation_side is not None and (i, col) not in res:
                    # The target follows the relation when the relation came from one side by rule.
                    row[col], status[col] = (va if relation_side == "a" else vb), "vocabulary-resolved"
                    continue
                if va.lower() == vb.lower():
                    row[col], status[col] = va, "agreed"
                    continue
                v = vocab_rule(col, va, vb)
                if v is not None:
                    row[col], status[col] = v, "vocabulary-resolved"
                    if col == "relation":
                        relation_side = "a" if v == va else "b"
                elif (i, col) in res:
                    row[col], status[col] = res[(i, col)]["value"], res[(i, col)]["status"]
                else:
                    row[col], status[col] = "", "pending-review"
                    pending += 1
            for col in UNIT_COLS:
                na, nb = norm_unit(a[col]), norm_unit(b[col])
                printed = b[col].strip() if b[col].strip().lower() != "n/a" else a[col].strip()
                # a code with an underscore (in_s, deg_s2) is the reader's code, never a printed spelling: the
                # printed form is then in the notes, and the column stays empty rather than claim the code was printed
                row[col + "_as_printed"] = "" if args.unit_codes or "_" in printed else printed
                if na is not None and na == nb:
                    row[col], status[col] = na, "agreed" if a[col].strip() == b[col].strip() else "vocabulary-resolved"
                elif (i, col) in res:
                    row[col], status[col] = res[(i, col)]["value"], res[(i, col)]["status"]
                elif na is not None and nb == "n/a" or nb is not None and na == "n/a":
                    # One agent wrote n/a for an axis the other read; the read unit stands.
                    row[col], status[col] = (na if nb == "n/a" else nb), "vocabulary-resolved"
                else:
                    row[col], status[col] = "", "pending-review"
                    pending += 1
            for col in DESC_COLS:
                row[col] = b[col] if col == "legend_entries" else a[col]
                if re.sub(r"[^a-z0-9]", "", a[col].lower()) != re.sub(r"[^a-z0-9]", "", b[col].lower()):
                    alternates.append({"id": i, "column": col, "claude": a[col], "codex": b[col]})
            finish(i, row, status, a["notes"], b["notes"])
        elif i in one_sided and i not in missing:
            src, side = (A[i], "claude") if i in A else (B[i], "codex")
            row, status = {"id": i}, {}
            for col in id_cols:
                if (i, col) in res:
                    row[col], status[col] = res[(i, col)]["value"], res[(i, col)]["status"]
                else:
                    row[col], status[col] = (canon_test_type(src[col]) if col == "test_type" else src[col].strip()), "one-sided-verified"
            for col in UNIT_COLS:
                row[col + "_as_printed"] = "" if args.unit_codes or "_" in src[col] else src[col].strip()   # a code is not a spelling
                if (i, col) in res:
                    row[col], status[col] = res[(i, col)]["value"], res[(i, col)]["status"]
                else:
                    n = norm_unit(src[col])
                    row[col], status[col] = (n if n is not None else ""), ("one-sided-verified" if n is not None else "pending-review")
                    pending += 0 if n is not None else 1
            for col in DESC_COLS:
                row[col] = src[col]
            finish(i, row, status, src["notes"] if side == "claude" else "", src["notes"] if side == "codex" else "",
                   row_status="one-sided-verified")
            cells[-1]["one_sided"] = {"submission": side, "decision_note": decisions[i]["note"]}

    # Corrections come last: a cell both inventories read the same wrong way agrees (or is the second
    # submission's descriptive text), so no other rule can reach it. Each one cites its evidence, and the
    # sidecar keeps the value it replaced. First used for the PS legends of FC-2B and FC-2C (2935 read
    # as 2995 by both inventories, 2026-10-13).
    corrections = []
    if args.corrections:
        by_id = {r["id"]: r for r in rows}
        with Path(args.corrections).open(encoding="utf-8-sig", newline="") as f:
            correction_rows = list(csv.DictReader(f))
        for c in correction_rows:
            r = by_id[c["id"]]
            corrections.append({"id": c["id"], "column": c["column"], "replaced": r[c["column"]], "value": c["value"],
                                "evidence": c["evidence"], "note": c["note"]})
            r[c["column"]] = c["value"]
            # a row a page check changed is no longer as the readings agreed it (Codex's review, 2026-11-20: the
            # reprinted tables of Section VI kept `agreed`); the sidecar's cell statuses keep what the readings gave
            if r.get("status") == "agreed":
                r["status"] = "resolved"

    fieldnames = ["id", "kind", "title_as_printed", "printed_page", "pdf_page"]
    fieldnames += [c for c in ("appendix", "section") if c in extra_cols]
    fieldnames += ["test_type", "soils", "states", "apparatus", "rate_or_dynamics", "data_form", "panels", "curves",
                   "trace_classes", "x_quantity", "x_unit", "x_unit_as_printed", "x_axis_type",
                   "y_quantity", "y_unit", "y_unit_as_printed", "y_axis_type",
                   "legend_entries", "rotation", "in_scope", "transcribe", "priority", "mcc_relevant"]
    fieldnames += [c for c in ("relation", "relation_target") if c in extra_cols]
    fieldnames += ["status", "notes_claude", "notes_codex"]
    # --base: an index built earlier for the same source by its own command (Volume I Section II, built into
    # qa/inventory-s2-b1/figures.csv) comes first, so one figures.csv covers the volume while no build reads its own
    # output; a column the base lacks (section, relation) is empty on its rows
    base_rows, base_meta = [], None
    if args.base:
        new_ids = {r["id"] for r in rows}
        with Path(args.base).open(encoding="utf-8-sig", newline="") as f:
            base_reader = csv.DictReader(f)
            missing_cols = [c for c in base_reader.fieldnames if c not in fieldnames]
            if missing_cols:
                sys.exit(f"--base has columns this batch does not write: {missing_cols}")
            base_rows = [r for r in base_reader if r["id"] not in new_ids]
        base_meta = json.loads(Path(args.base).with_suffix(".json").read_text(encoding="utf-8"))
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore", restval="")
        w.writeheader()
        w.writerows(base_rows + rows)
    statuses = ["agreed", "vocabulary-resolved", "resolved", "convention", "rule", "provisional", "pending-review"]
    if decisions:
        statuses.append("one-sided-verified")
    sidecar = {
        "file": out.name,
        "source": args.source,
        "method": f"two independent inventories from the page images (Claude, Codex {args.codex_model}), "
                  "exact-match diff (tools/diff_tables.py), vocabulary rules and a resolutions file "
                  f"(qa/{args.batch}/resolutions.csv) applied by tools/build_figures.py",
        "submissions": [str(a_path), str(b_path)],
        "resolutions": str(res_path),
        "scope_rule": "in_scope: the item carries numbers to extract into data/ (yes | maybe | no). "
                      "transcribe: the page is transcribed in phase b (yes for all of Section II).",
        "priority_rule": "1: needed for the first calibration and prediction protocols (shear family, LPT records "
                         "with known bed state, DPT signatures and correlation, materials tables). 2: needed to set up "
                         "or interpret those tests (bed preparation, boundary and bin effects, rate series, "
                         "degradation). 3: context only.",
        "mcc_rule": "mcc_relevant yes only for figures showing the same material after different loading or handling "
                    "histories with a different response, plus the state maps needed to read them; maybe for the "
                    "direct shear dilation panel.",
        "curve_count_convention": "every drawn line is a trace, including each boundary of a shaded or bracketed "
                                  "range; markers and the fitted line through them are one response series; "
                                  "construction guides are not counted.",
        "vocabularies": {
            "axis_type": ["linear", "log", "normalized", "reciprocal", "n/a"],
            "unit": UNIT_VOCAB + (["ksi"] if any(r.get("y_unit") == "ksi" for r in rows) else [])
                    + [u for u in LATER_UNITS if any(u in (r.get("x_unit", "") + ";" + r.get("y_unit", "")).split(";") for r in rows)],
            "test_type": ["grain size", "density", "bed preparation", "direct shear", "triaxial", "load penetration",
                          "dynamic penetrometer", "drag", "impact", "sonic", "soil model", "soil properties",
                          "apparatus", "other"] + (["model drop"] if any(r.get("test_type") == "model drop" for r in rows) else []),
            "data_form": ["table", "curve", "schematic", "photo", "text", "mixed"],
            "status": statuses,
        },
        "missing_ids": missing,
        "cells": cells,
        "descriptive_alternates": alternates,
    }
    if corrections:
        sidecar["corrections_file"] = args.corrections
        sidecar["corrections"] = corrections
    if args.unit_codes:
        sidecar["unit_codes"] = ("The brief asked both readers for the controlled unit codes, with the printed spelling in "
                                 "the notes; x_unit_as_printed and y_unit_as_printed are left empty.")
    if extra_cols:
        sidecar["id_aliases"] = aliases
        sidecar["relation_vocabulary"] = ["same-as", "derived-from", "reproduces", "unresolved", "none"]
        sidecar["table_id_rule"] = ("Unnumbered tables are identified by page locator TA-pNNN (NNN = PDF page where the "
                                    "table starts); numbered figures keep the printed number (FA-12, FB-3, FC-1B).")
    if base_meta is not None:
        sidecar["base_file"] = str(args.base)
        sidecar["rows_from_base"] = len(base_rows)
        sidecar["base"] = base_meta
    out.with_suffix(".json").write_text(json.dumps(sidecar, indent=2, ensure_ascii=False), encoding="utf-8")
    n = {k: sum(1 for r in rows if r["status"] == k) for k in ("agreed", "resolved", "provisional", "pending-review", "one-sided-verified")}
    print(f"wrote {out} and sidecar: {len(rows)} rows, row status {n}; pending cells {pending}; "
          f"descriptive alternates {len(alternates)}; ids missing on one side without a decision {missing}")
    return 1 if pending or missing else 0


if __name__ == "__main__":
    sys.exit(main())
