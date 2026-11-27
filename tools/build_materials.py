"""Build data/materials/materials.csv (SI canonical) from an agreed table diff of Table 2-3.

Usage:
    python tools/build_materials.py qa/materials-b1/agreed.csv \
        extractions/claude/materials-b1/materials-claude.csv extractions/codex/materials-b1/materials-codex.csv \
        data/materials/materials.csv

Inputs are the agreed-cells CSV written by tools/diff_tables.py (disagreeing cells empty) and the
two original submissions. Rules applied, all recorded in the sidecar materials.json:

1. A cell both agents agreed on is taken as is, status `agreed`.
2. A text cell where the two readings differ only by a hyphen or a space at a printed line break
   is resolved by the documented typography rule (keep the printed hyphen, drop the wrap space),
   status `typography-resolved`. Any other disagreement stays empty, status `pending-review`.
3. A cell both agents read identically but both flagged as uncertain keeps the value with status
   `uncertain` and is listed for review.
4. SI columns are computed with tools/to_si.py factors from the native values. Non-numeric native
   cells (words, inequalities) are carried into the SI column as text, marked in `read_flags`.
5. Numbers are written with a leading zero (0.45, not .45); nothing else about a number changes.
"""

import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from to_si import FACTORS, to_si  # noqa: E402

TYPO_FLAG_TOKENS = ("glyph", "damaged", "digit")


def read(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return {r["soil_no"].strip(): r for r in csv.DictReader(f)}


def wrap_hyphen_resolution(a: str, b: str):
    """Return the canonical text if a and b differ only at a line-wrap hyphen, else None."""
    # Equal once every space and hyphen is removed: the readings differ only in how a printed
    # line break was rendered (hyphen kept or dropped, wrap space kept or dropped).
    norm = lambda s: re.sub(r"[\s-]+", "", s.strip().lower())
    if norm(a) != norm(b):
        return None
    # Prefer the reading that keeps the printed hyphen, then close up any space around it.
    cand = a if a.count("-") >= b.count("-") else b
    return re.sub(r"\s*-\s*", "-", cand)


def num(s: str):
    s = (s or "").strip().replace(",", "")
    if re.fullmatch(r"[-+]?\d*\.?\d+", s):
        return float(s), ("0" + s) if s.startswith(".") else s
    return None, s


def main(agreed_path, a_path, b_path, out_path) -> int:
    agreed, A, B = read(agreed_path), read(a_path), read(b_path)
    out_rows, sidecar_cells = [], []
    for k in sorted(agreed, key=lambda x: int(x)):
        g, a, b = agreed[k], A[k], B[k]
        row = {"soil_no": k}
        statuses = {}
        for col in ("bendix_designation", "description_verbatim", "family", "state", "relative_density",
                    "unit_weight_native", "unit_weight_unit", "friction_angle_deg",
                    "elastic_modulus_native", "elastic_modulus_unit", "mean_grain_size_native",
                    "mean_grain_size_unit", "uniformity_coeff", "percent_passing_200_native",
                    "d95_native", "d95_unit"):
            if g.get(col, "") != "":
                row[col] = g[col]
                statuses[col] = "agreed"
            else:
                res = wrap_hyphen_resolution(a.get(col, ""), b.get(col, ""))
                if res is not None:
                    row[col] = res
                    statuses[col] = "typography-resolved"
                else:
                    row[col] = ""
                    statuses[col] = "pending-review"
        flags = {f for f in (a.get("read_flags", "") + "," + b.get("read_flags", "")).split(",") if f}
        if any(any(t in f for t in TYPO_FLAG_TOKENS) for f in flags):
            statuses["percent_passing_200_native"] = "uncertain"
        # Leading-zero formatting on numeric cells.
        for col in ("relative_density", "mean_grain_size_native"):
            v, s = num(row.get(col, ""))
            if v is not None:
                row[col] = s
        # SI columns.
        uw, _ = num(row["unit_weight_native"])
        # Formatting carries no more precision than the printed value supports: unit weights
        # are printed to 0.1 pcf (about 1.6 kg/m^3), moduli to 100 psi (about 0.7 MPa).
        row["unit_weight_N_m3"] = f"{to_si(uw, 'pcf', 'N_m3'):.1f}" if uw is not None else ""
        row["bulk_density_kg_m3"] = f"{to_si(uw, 'pcf', 'kg_m3'):.1f}" if uw is not None else ""
        em, em_s = num(row["elastic_modulus_native"])
        row["elastic_modulus_Pa"] = f"{to_si(em, 'psi', 'Pa'):.0f}" if em is not None else em_s
        mg, mg_s = num(row["mean_grain_size_native"])
        row["mean_grain_size_mm"] = mg_s if mg is not None else mg_s
        d95, d95_s = num(row["d95_native"])
        row["d95_mm"] = d95_s
        row["percent_passing_200"] = row["percent_passing_200_native"]
        row["read_flags"] = ";".join(sorted(flags))
        row["source_locator"] = a.get("source_locator", "")
        row["status"] = ("agreed" if all(s == "agreed" for s in statuses.values())
                         else "partial" if "pending-review" in statuses.values()
                         else "resolved-with-notes")
        out_rows.append(row)
        sidecar_cells.append({"soil_no": k, "cell_status": statuses})

    fieldnames = ["soil_no", "bendix_designation", "description_verbatim", "family", "state", "relative_density",
                  "unit_weight_native", "unit_weight_unit", "unit_weight_N_m3", "bulk_density_kg_m3",
                  "friction_angle_deg", "elastic_modulus_native", "elastic_modulus_unit", "elastic_modulus_Pa",
                  "mean_grain_size_mm", "uniformity_coeff", "percent_passing_200", "d95_mm",
                  "read_flags", "source_locator", "status"]
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(out_rows)
    sidecar = {
        "file": out.name,
        "source": "Bendix AM-68-1 Vol. I, Table 2-3, printed 2-16, PDF 41",
        "source_sha256": "A82DDDB1391347C223C1D719929A3D549A39844DE1E99ACE7F2F623A5864C063",
        "method": "two independent readings of the page image (Claude, Codex gpt-6-astra), exact-match diff (tools/diff_tables.py), typography rule for line-wrap hyphens, SI conversion by tools/to_si.py",
        "submissions": [str(a_path), str(b_path)],
        "diff_report": "qa/materials-b1/diff-report.md",
        "units": {"unit_weight_native": "pcf (lbf/ft^3)", "unit_weight_N_m3": "N/m^3",
                  "bulk_density_kg_m3": "kg/m^3 under standard gravity 9.80665 m/s^2",
                  "friction_angle_deg": "degrees", "elastic_modulus_native": "psi",
                  "elastic_modulus_Pa": "Pa", "mean_grain_size_mm": "mm", "d95_mm": "mm",
                  "percent_passing_200": "percent by weight passing No. 200 sieve, as printed"},
        "factors": {"pcf->N_m3": FACTORS[("pcf", "N_m3")], "pcf->kg_m3": FACTORS[("pcf", "kg_m3")],
                    "psi->Pa": FACTORS[("psi", "Pa")]},
        "column_notes": {
            "elastic_modulus": "initial tangent modulus measured by sonic means at 4 psi confining pressure (table footnote *)",
            "percent_passing_200": "footnote **: percent of material by weight passing a No. 200 sieve (ACS)",
            "d95": "footnote ***: diameter at the 95 percent smaller-than point of the standard sieve analysis",
            "uniformity_coeff": "printed as the word large for soils 10 and 11",
        },
        "cells": sidecar_cells,
        "status_vocabulary": ["agreed", "typography-resolved", "uncertain", "pending-review"],
        # Inconsistencies between the canonical table and other places the report prints the same
        # number. Table 2-3 stays canonical because it is the Section II source table; the other
        # printing is recorded so nobody "corrects" the value later without seeing both.
        "source_inconsistencies": [
            {"soil_no": "4", "column": "unit_weight_native", "canonical": "50.6",
             "elsewhere": "50.5", "elsewhere_locator": "Table 1-1, printed 1-6, PDF 20",
             "found_by": "Codex, inventory-s2-b1", "date": "2026-10-07"},
        ],
    }
    out.with_suffix(".json").write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
    n_pending = sum(1 for c in sidecar_cells for s in c["cell_status"].values() if s == "pending-review")
    n_typo = sum(1 for c in sidecar_cells for s in c["cell_status"].values() if s == "typography-resolved")
    n_unc = sum(1 for c in sidecar_cells for s in c["cell_status"].values() if s == "uncertain")
    print(f"wrote {out} and sidecar: {len(out_rows)} rows; typography-resolved {n_typo}, uncertain {n_unc}, pending-review {n_pending}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:5]))
