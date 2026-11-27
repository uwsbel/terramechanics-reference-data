"""Build data/materials/specifications.csv from the Appendix A soil specification sheets, and the
cross-check of Volume I Table 2-3 against them (roadmap step 3d).

Usage:
    python tools/build_specifications.py            # write the CSV, its sidecar and the report
    python tools/build_specifications.py --check    # compare a fresh build with the files on disk

Input: the canonical pages corpus/1968-vol2/pages/p0002.md to p0098.md (Appendix A), every one of
them read by two agents and reconciled, and data/materials/materials.csv (Table 2-3).

Output:
    data/materials/specifications.csv    long format, one row per soil and quantity as printed in
                                          the specification of that soil number (each soil's own
                                          sheet, never a copy printed for another soil)
    data/materials/specifications.json   sidecar: units, factors, rules
    qa/specifications/table23-vs-appendix-a.md   every Table 2-3 value next to its specification
                                          value, and the relative density implied by the Table 2-3
                                          unit weight on the specification's density chart

Rules (also in the sidecar):
1. Values are taken from the page text exactly as printed; `value_native` is the printed number,
   `printed_text` the sentence or table row it came from. Words ("zero", "Small", "Large") become
   numbers only where the word is a number ("zero" -> 0).
2. Density chart end labels are split into minimum and maximum axis labels by their count on the
   page: 6 labels are 3 + 3; 5 labels (SS) are 2 + 3, the third minimum line starting at the 95
   tick, which is not a printed label; 4 labels (RSM-b) are 3 + 1, the three lines meeting at one
   maximum. Any other count stops the build.
3. SI: unit weights in pcf become mass density in kg/m^3 under standard gravity, moduli in psi
   become Pa, with the factors of tools/to_si.py. Grain sizes stay in mm, as in materials.csv.
4. The relative density implied by a unit weight is Vol. I equation 2-2 (printed 2-30, PDF 55),
   Dr = (g - gmin)/(gmax - gmin) * gmax/g, with the chart's middle labels as gmin and gmax.
"""
import csv
import io
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from to_si import FACTORS, to_si  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "corpus" / "1968-vol2" / "pages"
OUT = ROOT / "data" / "materials" / "specifications.csv"
SIDECAR = ROOT / "data" / "materials" / "specifications.json"
REPORT = ROOT / "qa" / "specifications" / "table23-vs-appendix-a.md"
SRC = "AM-68-1 Vol. II (NASA CR-92215)"
FIELDS = ["soil_no", "quantity", "qualifier", "value_native", "unit_native", "value_si", "unit_si",
          "printed_text", "source_locator", "status"]

SPEC = re.compile(r"^SPECIFICATION FOR SOIL NO\.?\s*(\d+)", re.M)
DESIG = re.compile(r"^1\. Bendix Designation:\s*(.+?)\.?$", re.M)
DR = re.compile(r"average relative density of Soil No\. (\d+) is (about )?(zero|\d*\.?\d+)")
PHI = re.compile(r"angle of internal friction for Soil No\. (\d+) is (about )?([\d.]+)°")
BAND = re.compile(r"essentially the same - about (\d+)° to (\d+)°")
MOD = re.compile(r"for Soil No\. (\d+) by this test (?:is )?(about )?([\d,]+) psi at a confining pressure of (\.?\d+)( \[\?\])? psi")
MOD_EST = re.compile(r"(?:estimated to be (?:in the vicinity of )?|estimated initial tangent modulus for this soil is )([\d,]+) psi")
PLACE = re.compile(r"^(Soil No\. (\d+) was placed.*)$", re.M)
ROLL = re.compile(r"(\d+) passes|rolled (two|six) times")
MIX = re.compile(r"mixed (?:in the ratio of )?(\d+:\d+)")
GRAIN = re.compile(r"^\| (Mean Size|Effective Diameter|Coefficient of Uniformity[^|]*|Coarseness) \| [^|]* \| ([^|]*) \| ([^|]*) \|$", re.M)
NUMBER_PARA = re.compile(r"^\d+\.\d+$")
GQ = {"Mean Size": "d50", "Effective Diameter": "d10", "Coarseness": "d95"}
WORDS = {"two": 2, "six": 6}


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    head = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            head[k.strip()] = v.strip().strip('"')
    return head, m.group(2)


def num(s):
    s = (s or "").strip().replace(",", "")
    s = re.sub(r"mm$", "", s)
    return float(s) if re.fullmatch(r"\d*\.?\d+", s) else None


def fmt(x):
    return f"{x:.6g}" if x is not None else ""


def loc(head, what):
    return f"{SRC}, {what}, printed {head['printed_page']}, PDF {head['pdf_page']}"


def sheets():
    """Pages of each soil's own specification, in order (Appendix A runs PDF 2 to 98)."""
    out, soil = {}, None
    for p in sorted(PAGES.glob("p0*.md")):
        n = int(p.stem[1:])
        if not 2 <= n <= 98:
            continue
        head, body = parse(p)
        s = SPEC.search(body)
        if s:
            soil = int(s.group(1))
        if soil:
            out.setdefault(soil, []).append((head, body))
    return out


def build():
    rows = []

    def add(soil, q, qual, val, unit, si, unit_si, text, where, head):
        rows.append({"soil_no": soil, "quantity": q, "qualifier": qual, "value_native": val, "unit_native": unit,
                     "value_si": si, "unit_si": unit_si, "printed_text": re.sub(r"\s+", " ", text).strip(),
                     "source_locator": loc(head, where), "status": head.get("review_status", "")})

    for soil, pages in sorted(sheets().items()):
        for head, body in pages:
            d = DESIG.search(body)
            if d and SPEC.search(body):
                add(soil, "bendix_designation", "", d.group(1), "", "", "", d.group(0), "item 1", head)
            for m in DR.finditer(body):
                v = "0" if m.group(3) == "zero" else m.group(3)
                add(soil, "relative_density", (m.group(2) or "").strip(), v, "", v, "", m.group(0), "item 10", head)
            for m in PHI.finditer(body):
                add(soil, "friction_angle", (m.group(2) or "").strip(), m.group(3), "deg", m.group(3), "deg", m.group(0), "item 11", head)
            for m in BAND.finditer(body):
                for q, v in (("friction_angle_band_low", m.group(1)), ("friction_angle_band_high", m.group(2))):
                    add(soil, q, "about", v, "deg", v, "deg", m.group(0), "item 14", head)
            for m in MOD.finditer(body):
                v = m.group(3).replace(",", "")
                add(soil, "elastic_modulus", (m.group(2) or "").strip() or "as printed", v, "psi", fmt(to_si(float(v), "psi", "Pa")), "Pa", m.group(0), "item 12", head)
                cp = m.group(4) + (m.group(5) or "")
                add(soil, "modulus_confining_pressure", "", cp, "psi", fmt(to_si(float(m.group(4)), "psi", "Pa")), "Pa", m.group(0), "item 12", head)
            for m in MOD_EST.finditer(body):
                v = m.group(1).replace(",", "")
                add(soil, "elastic_modulus", "estimated, not measured", v, "psi", fmt(to_si(float(v), "psi", "Pa")), "Pa", m.group(0), "item 12", head)
            for m in PLACE.finditer(body):
                if int(m.group(2)) != soil:
                    continue
                add(soil, "placement", "", "", "", "", "", m.group(1), "item 13", head)
                r = ROLL.search(m.group(1))
                if r:
                    v = r.group(1) or str(WORDS[r.group(2)])
                    add(soil, "roller_count", "passes" if r.group(1) else "rollings", v, "", v, "", r.group(0), "item 13", head)
            for m in MIX.finditer(body):
                add(soil, "mix_ratio_by_weight", "cinders : second component", m.group(1), "", m.group(1), "", m.group(0), "item 6", head)
            fig = re.search(r"^::: figure (FA-\d+)$", body, re.M)
            if fig and GRAIN.search(body):
                for m in GRAIN.finditer(body):
                    q = GQ.get(m.group(1), "cu")
                    unit = "" if q == "cu" else "mm"
                    for part, val in (("average", m.group(2).strip()), ("range", m.group(3).strip())):
                        si = fmt(num(val)) if part == "average" else val.replace("mm", "")
                        add(soil, f"{q}_{part}", "", val, unit, si, unit, m.group(0).strip("| "), f"Figure {fig.group(1)[1:]} inset", head)
            cap = re.search(r"^caption: .*Density [Vv]ersus Relative Density", body, re.M)
            if fig and cap:
                labels = [para.strip() for para in body.split(":::")[0].split("\n\n") if NUMBER_PARA.match(para.strip())]
                split = {6: 3, 5: 2, 4: 3}.get(len(labels))
                if split is None:
                    sys.exit(f"soil {soil}: {len(labels)} density labels on PDF {head['pdf_page']}; rule 2 covers 4, 5 or 6")
                for axis, vals in (("gamma_min", labels[:split]), ("gamma_max", labels[split:])):
                    for k, v in enumerate(vals):
                        add(soil, f"{axis}_label_{k + 1}", "printed end label, top to bottom", v, "pcf",
                            fmt(to_si(float(v), "pcf", "kg_m3")), "kg/m^3", f"{axis} labels {', '.join(vals)}",
                            f"Figure {fig.group(1)[1:]}", head)
    return rows


def mid(rows, soil, axis):
    vals = [float(r["value_native"]) for r in rows if r["soil_no"] == soil and r["quantity"].startswith(f"{axis}_label_")]
    if len(vals) == 3:
        return vals[1], ""
    if axis == "gamma_min" and len(vals) == 2:  # SS: the third line starts at the unlabeled 95 tick (rule 2)
        return vals[0], "middle line taken as the lower printed label (the third line starts at the 95 tick)"
    if axis == "gamma_max" and len(vals) == 1:
        return vals[0], "the three lines meet at one printed maximum"
    return None, "no labels"


def report(rows):
    t23 = {int(r["soil_no"]): r for r in csv.DictReader(open(ROOT / "data/materials/materials.csv", encoding="utf-8"))}

    def get(soil, q):
        return next((r for r in rows if r["soil_no"] == soil and r["quantity"] == q), None)

    lines = ["# Volume I Table 2-3 against the Appendix A specifications", "",
             "Generated by `tools/build_specifications.py` from `data/materials/materials.csv` (Table 2-3, printed 2-16, PDF 41)",
             "and `data/materials/specifications.csv` (each soil's own Appendix A sheet). Both come from pages read by two",
             "agents and reconciled; no human audit yet. A blank cell is a value the specification does not print.", "",
             "## Values side by side", "",
             "| soil | Dr T2-3 | Dr spec | φ T2-3 | φ spec | E T2-3 (psi) | E spec (psi) | mean size T2-3 | D50 spec | Cu T2-3 | Cu spec | D95 T2-3 | D95 spec |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    diffs = []
    for soil in sorted(t23):
        t = t23[soil]

        def sv(q):
            r = get(soil, q)
            return (r["value_native"] + (" (est.)" if r and "estimated" in r["qualifier"] else "")) if r else ""
        phi = sv("friction_angle")
        lo, hi = get(soil, "friction_angle_band_low"), get(soil, "friction_angle_band_high")
        if lo and hi:
            phi += f"; band {lo['value_native']}-{hi['value_native']}"
        cells = [str(soil), t["relative_density"], sv("relative_density"), t["friction_angle_deg"], phi,
                 t["elastic_modulus_native"], sv("elastic_modulus"), t["mean_grain_size_mm"], sv("d50_average"),
                 t["uniformity_coeff"], sv("cu_average"), t["d95_mm"], sv("d95_average")]
        lines.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
        for name, a, b in (("relative density", t["relative_density"], get(soil, "relative_density")),
                           ("friction angle (deg)", t["friction_angle_deg"], get(soil, "friction_angle")),
                           ("elastic modulus (psi)", t["elastic_modulus_native"], get(soil, "elastic_modulus")),
                           ("mean size / D50 (mm)", t["mean_grain_size_mm"], get(soil, "d50_average")),
                           ("uniformity Cu", t["uniformity_coeff"], get(soil, "cu_average")),
                           ("D95 (mm)", t["d95_mm"], get(soil, "d95_average"))):
            if b is None:
                continue
            x, y = num(a), num(b["value_native"])
            same = (x is not None and y is not None and abs(x - y) < 1e-9) or (x is None and y is None and a.strip().lower() == b["value_native"].strip().lower())
            if not same:
                diffs.append(f"| {soil} | {name} | {a} | {b['value_native']} | {b['source_locator']} |")
    lines += ["", "## Disagreements", "", "Every cell where the two sources print different values.", "",
              "| soil | quantity | Table 2-3 | specification | specification source |", "|---|---|---|---|---|"] + diffs
    lines += ["", "## Relative density implied by the Table 2-3 unit weight", "",
              "Vol. I equation 2-2 (printed 2-30, PDF 55) on the average (middle) line of each soil's own density chart.",
              "This is arithmetic on printed labels, not a printed value.", "",
              "| soil | unit weight T2-3 (pcf) | γmin (pcf) | γmax (pcf) | Dr implied | Dr stated | note |", "|---|---|---|---|---|---|---|"]
    for soil in sorted(t23):
        g = num(t23[soil]["unit_weight_native"])
        gmin, n1 = mid(rows, soil, "gamma_min")
        gmax, n2 = mid(rows, soil, "gamma_max")
        if None in (g, gmin, gmax):
            continue
        dr = (g - gmin) / (gmax - gmin) * gmax / g
        note = "; ".join(n for n in (n1, n2) if n)
        lines.append(f"| {soil} | {t23[soil]['unit_weight_native']} | {gmin:g} | {gmax:g} | {dr:.2f} | {t23[soil]['relative_density']} | {note} |")
    lines += ["", "## Ambiguities that persist on careful reading", "",
              "1. Roller passes: soils 3, 4, 8, 9 and 12 print a number of passes; soils 10 and 11 print rollings with",
              "   \"one pass back and forth\" for two rollings. Whether a pass on the other sheets is one direction or a",
              "   round trip is not stated, so the number of times the roller crossed a layer is uncertain by a factor of 2.",
              "2. Soil 1's modulus is printed \"at a confining pressure of .4 [?] psi\"; every other sheet and Table 2-3 say 4 psi.",
              "3. Soil 6's average uniformity is printed \"2 5\" with a range of 15-25; Table 2-3 gives 17.0.", ""]
    return "\n".join(lines)


def render(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=FIELDS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def sidecar():
    return json.dumps({
        "file": "specifications.csv",
        "source": "Bendix AM-68-1 Vol. II (NASA CR-92215), Appendix A, PDF 2 to 98",
        "method": "canonical page transcriptions (two independent readings, mechanical diff, decisions in qa/pages-vol2-ab-b1 to b5), parsed by tools/build_specifications.py",
        "units": {"pcf": "lbf/ft^3 as printed", "kg/m^3": "mass density under standard gravity 9.80665 m/s^2",
                  "psi": "as printed", "Pa": "SI", "mm": "grain size, as printed", "deg": "degrees"},
        "factors": {"pcf->kg_m3": FACTORS[("pcf", "kg_m3")], "psi->Pa": FACTORS[("psi", "Pa")]},
        "rules": [line.strip() for line in __doc__.split("Rules (also in the sidecar):")[1].strip().split("\n") if line.strip()],
    }, indent=2, ensure_ascii=False) + "\n"


def main(argv):
    rows = build()
    outputs = {OUT: render(rows), SIDECAR: sidecar(), REPORT: report(rows)}
    if "--check" in argv:
        bad = [str(p.relative_to(ROOT)) for p, t in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
        print("\n".join(f"differs: {b}" for b in bad) if bad else "specifications match a fresh build")
        return 1 if bad else 0
    for p, t in outputs.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(t, encoding="utf-8", newline="\n")
        print(f"{p.relative_to(ROOT).as_posix()}")
    print(f"{len(rows)} rows for {len({r['soil_no'] for r in rows})} soils")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
