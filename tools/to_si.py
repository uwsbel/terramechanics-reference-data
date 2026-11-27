"""Unit conversion to SI for the recovered data. The constants here are THE constants; the table in
docs/DATA-ORGANIZATION.md is a copy of this one and must be kept identical.

Library use:
    from to_si import to_si, FACTORS
    to_si(41.4, "pcf", "kg_m3")   -> 663.16...
    to_si(5500, "psi", "Pa")      -> 37921165.1...

Command line (adds SI columns to a CSV according to a column map):
    python tools/to_si.py in.csv out.csv --map unit_weight_native:pcf:kg_m3:bulk_density_kg_m3 \
        --map unit_weight_native:pcf:N_m3:unit_weight_N_m3 --map elastic_modulus_native:psi:Pa:elastic_modulus_Pa

Each --map is source_column:from_unit:to_unit:new_column. Non-numeric cells (words such as "large",
inequalities such as "<3%") are copied through unchanged into the new column with the suffix
"_asis" so nothing is silently dropped. The output carries a `si_conversion` note column naming
the factors used, so a reader can audit the arithmetic.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

G0 = 9.80665  # standard gravity, m/s^2 (exact by definition)

# Exact or CODATA-derived factors. Key: (from, to) -> multiplicative factor.
FACTORS = {
    ("inch", "m"): 0.0254,
    ("in", "m"): 0.0254,
    ("ft", "m"): 0.3048,
    ("lbf", "N"): 4.4482216152605,
    ("lb", "kg"): 0.45359237,
    ("lbm", "kg"): 0.45359237,
    ("psi", "Pa"): 6894.757293168,
    ("ksi", "Pa"): 6894757.293168,  # kips per square inch (the moduli of Appendix B)
    ("psf", "Pa"): 47.880258980336,
    ("pcf", "N_m3"): 4.4482216152605 / 0.3048**3,          # 157.08746...
    ("pcf", "kg_m3"): 0.45359237 / 0.3048**3,               # 16.018463... (mass density under g0)
    ("in_min", "m_s"): 0.0254 / 60.0,
    ("in_s", "m_s"): 0.0254,
    ("ft_s", "m_s"): 0.3048,
    ("g", "m_s2"): G0,
    ("deg", "deg"): 1.0,
    ("none", "none"): 1.0,  # dimensionless quantities kept as printed (relative density Dr)
    ("percent", "none"): 0.01,  # percent (percent finer on the grain-size curves) as a fraction, SI unit one
    ("mm", "m"): 1.0e-3,
    ("mm", "mm"): 1.0,
    ("mil", "m"): 0.0254e-3,  # thousandths of an inch (the "x 10^3 in." axes)
    # time histories and rates of the dynamic tests (Volume I Sections IV and V, D-050)
    ("ms", "s"): 1.0e-3,
    ("s", "s"): 1.0,
    ("in_s2", "m_s2"): 0.0254,
    ("deg_s", "deg_s"): 1.0,
}

NUM = re.compile(r"^[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$")   # scientific notation too (small grain sizes)


def to_si(value: float, from_unit: str, to_unit: str) -> float:
    try:
        return value * FACTORS[(from_unit, to_unit)]
    except KeyError:
        raise KeyError(f"no conversion {from_unit} -> {to_unit}; add it to FACTORS and to docs/DATA-ORGANIZATION.md")


def convert_cell(cell: str, from_unit: str, to_unit: str):
    s = (cell or "").strip().replace(",", "")
    if NUM.match(s):
        return f"{to_si(float(s), from_unit, to_unit):.6g}", None
    return "", s  # not a number: pass through as-is


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("infile")
    ap.add_argument("outfile")
    ap.add_argument("--map", action="append", required=True,
                    help="source_column:from_unit:to_unit:new_column (repeatable)")
    args = ap.parse_args()
    maps = []
    for m in args.map:
        parts = m.split(":")
        if len(parts) != 4:
            raise SystemExit(f"bad --map {m!r}; expected source:from:to:new")
        maps.append(tuple(parts))
        _ = FACTORS[(parts[1], parts[2])]  # fail early on an unknown conversion

    with Path(args.infile).open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []
    new_cols = []
    for src, fu, tu, new in maps:
        if new not in fieldnames and new not in new_cols:
            new_cols.append(new)
        asis = new + "_asis"
        if asis not in fieldnames and asis not in new_cols:
            new_cols.append(asis)
    note = "; ".join(f"{new} = {src} [{fu}] x {FACTORS[(fu, tu)]:.10g} [{tu}]" for src, fu, tu, new in maps)
    for r in rows:
        for src, fu, tu, new in maps:
            val, passthrough = convert_cell(r.get(src, ""), fu, tu)
            r[new] = val
            r[new + "_asis"] = passthrough or ""
        r["si_conversion"] = note
    with Path(args.outfile).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames + new_cols + ["si_conversion"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {args.outfile}: {len(rows)} rows, added {new_cols}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
