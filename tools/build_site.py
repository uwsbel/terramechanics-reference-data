"""Generate the Quarto site pages under site/ from the repository's CSV and JSON files.

Usage:
    python tools/build_site.py            # write site/**/*.qmd and copy thumbnails from the cache
    python tools/build_site.py --check    # regenerate into a temporary directory and compare
                                          # byte for byte with site/; exit 1 on any difference

Rules (docs/DATA-ORGANIZATION.md, "Site"): every page is a generated view; no fact is typed here.
Each page ends with a note naming its inputs and the regeneration command. Nothing time- or
commit-dependent is written into a page body: the footer with commit and render date is written
at render time by tools/render_site.py into site/_footer.html, which is not committed. Output is
deterministic: sorted keys, fixed formatting, LF line endings, UTF-8.

Thumbnails: page images are rendered by tools/render_pages.py into work/site-cache/<source>/thumb110/
(outside git) and copied into site/img/<source>/ (ignored by git through *.png) so Quarto can
include them. A missing thumbnail is reported, never invented.
"""

import csv
import json
import math
import re
import shutil
import statistics
import sys
import tempfile
from collections import Counter, OrderedDict
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from to_si import FACTORS, to_si  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CACHE = ROOT / "work" / "site-cache" / "bendix-1968-vol1" / "thumb110"
IMG_REL = "img/1968"
# Volume II (NASA CR-92215) thumbnails live in their own cache and image folder.
CACHE2 = ROOT / "work" / "site-cache" / "bendix-1968-vol2" / "thumb110"
IMG_REL2 = "img/1968-vol2"
# Files the public release leaves out (tools/make_public_release.py passes its EXCLUDE to generate): the pages that render
# or link them are left out of the public site, so no page points at a file a reader cannot open. Empty for this
# repository's own site, which shows everything. A file that is not there counts as left out too, so this script also
# builds the public site from a checkout of the public repository (Codex's review of the export, 2026-11-23).
PRIVATE = ()


def private(rel):
    return (bool(PRIVATE) and rel.startswith(PRIVATE)) or not (ROOT / rel).exists()


# Plots of recovered observations and overlays of the readings on the page, built by
# tools/figures/build_plot_cache.py (needs matplotlib), copied like the thumbnails.
PLOTS = ROOT / "work" / "site-cache" / "plots"
IMG_PLOTS = "img/plots"
OVERLAYS = ROOT / "work" / "site-cache" / "overlays"
IMG_OVERLAYS = "img/overlays"
REGEN = "python tools/build_site.py"
SOURCE_CITE = "AM-68-1 Vol. I"

# ----------------------------------------------------------------------------- helpers

def read_csv(rel):
    with (ROOT / rel).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def esc(s):
    """Escape a cell for a Markdown pipe table."""
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def status_span(s):
    s = (s or "").strip()
    return f'[{s}]{{.status .status-{s}}}' if s else ""


LONG_CODE = re.compile(r"(?<![^\s|])[\w;,.\-]{25,}(?![^\s|])")   # a code with no space, such as a list of read flags


def breakable(cell):
    """A long code with no spaces gets line-break opportunities after `_`, `;` and `,`, so it cannot force its
    column wide and squeeze the others (2026-11-19, Dan's look at the soils table). Only plain text: a cell with a
    code span, a link or HTML is left alone, since a `<wbr>` inside a code span shows literally and one inside an
    attribute changes it (Codex's review)."""
    if any(ch in cell for ch in "`<>[]="):
        return cell
    return LONG_CODE.sub(lambda m: re.sub(r"([_;,])", r"\1<wbr>", m.group(0)), cell)


def table(headers, rows, caption=None, num_cols=(), widths=None):
    """A pipe table. site/table-wrap.lua puts every table in a box that scrolls sideways when the table is wider
    than the text column, so a wide table never runs under the page's table of contents (2026-11-19), and sets the
    column widths from the content (2026-11-20); Pandoc's equal widths from the separator dashes stay off
    (`tbl-colwidths: false` in site/_quarto.yml). `widths` is kept for the callers' record of the intended proportions
    and only orders the separator dashes."""
    seps = ["-" * max(4, int(w)) for w in widths] if widths else ["----"] * len(headers)
    out = ["| " + " | ".join(headers) + " |",
           "| " + " | ".join(sp[:-1] + ":" if h in num_cols else sp[:-1] if not widths else sp for h, sp in zip(headers, seps)) + " |"]
    for r in rows:
        out.append("| " + " | ".join(c if c.startswith(("[", "![")) else breakable(esc(c)) for c in r) + " |")
    if caption:
        out += ["", f": {caption}"]
    return "\n".join(out)


def page(title, body, inputs, extra_yaml=None, depth=0, reader=False):
    # the sonic modulus as the plots write it (2026-11-21, Dan); the data files keep the ASCII name "rho c^2"
    title, body = str(title).replace("rho c^2", "ρc²"), body.replace("rho c^2", "ρc²")
    front = ["---", f"title: {json.dumps(str(title))}"]
    if extra_yaml:
        for k, v in extra_yaml.items():
            if isinstance(v, (list, dict)):
                front.append(f"{k}:")
                if isinstance(v, list):
                    front += [f"  - {json.dumps(x)}" for x in v]
                else:
                    front += [f"  {kk}: {json.dumps(vv)}" for kk, vv in v.items()]
            elif isinstance(v, bool):
                front.append(f"{k}: {str(v).lower()}")
            else:
                front.append(f"{k}: {json.dumps(str(v))}")
    front += ["---", ""]
    text = (f"Generated view. Inputs: {', '.join('`' + i + '`' for i in inputs)}. "
            f"Regenerate with `{REGEN}`; do not edit this file, fix the inputs.")
    # a reader page keeps the maintainers' note in its source only, as a comment (plan v3, A6.8)
    note = (f"\n\n<!-- {text} -->\n" if reader else f"\n\n::: {{.generated-note}}\n{text}\n:::\n")
    return "\n".join(front) + body.rstrip() + note


MISSING = {"nr": "*not reported*", "nye": "*not yet extracted*", "unr": "*unreadable*",
           "conf": "*conflicting evidence*", "na": "*not applicable*"}


def missing(v, key="nr"):
    return v if (v or "").strip() else MISSING[key]


def nums(s):
    return [float(x) for x in re.findall(r"\d+\.?\d*", s or "")]


def fmt(v, nd):
    return f"{v:.{nd}f}"


def conv_text(s, from_unit, to_unit, nd, to_label):
    """Convert every number in a printed string; keep the words (to, approx) between them."""
    if not (s or "").strip():
        return ""
    out = s
    for x in sorted(set(re.findall(r"\d+\.?\d*", s)), key=len, reverse=True):
        out = out.replace(x, "\u0000" + x + "\u0000")
    parts = out.split("\u0000")
    res = []
    for p in parts:
        if re.fullmatch(r"\d+\.?\d*", p):
            res.append(fmt(to_si(float(p), from_unit, to_unit), nd))
        else:
            res.append(p)
    return "".join(res).strip() + f" {to_label}"


def inch_text(s):
    """'18 by 36' -> '0.457 by 0.914 m'; '4 inch cylinder' -> '0.102 m cylinder'."""
    if not (s or "").strip():
        return ""
    if re.search(r"\bft\b", s):   # a bed printed in feet ('18 by 12 ft', the model-drop bed): feet, not inches
        t = re.sub(r"\d+(?:\.\d+)?(?=\s*(?:by|ft\b))", lambda m: fmt(float(m.group(0)) * 0.3048, 4) + " m", s)
        t = re.sub(r" m ft\b", " m", t)
        # a depth in inches beside it ('soil depth 11 to 12 in', the drag bins): both ends of a range converted
        t = re.sub(r"(\d+(?:\.\d+)?)(\s+to\s+)(\d+(?:\.\d+)?)\s*(?:in|inch|inches)\b",
                   lambda m: f"{fmt(float(m.group(1)) * 0.0254, 4)} m{m.group(2)}{fmt(float(m.group(3)) * 0.0254, 4)} m", t)
        # and a single depth in inches ('RS intermediate beds 18 in thick', the model-drop table, 2026-11-20), a mixed
        # fraction whole ('2 1/2 in' is 2.5 in, not 2 and 1/(2 in): Codex's review)
        return re.sub(r"(?<![\d./-])(\d+(?:\s+|-)\d+/\d+|\d+/\d+|\d+(?:\.\d+)?)\s*(?:in|inch|inches)\b",   # '2 1/2', '2-1/2'
                      lambda m: f"{fmt(sum(float(Fraction(p)) for p in re.split(r'\s+|-', m.group(1))) * 0.0254, 4)} m", t)
    def rep(m):
        v = m.group(0).replace("-", " ")
        tot = 0.0
        for tok in v.split():
            if "/" in tok:
                a, b = tok.split("/"); tot += float(a) / float(b)
            else:
                tot += float(tok)
        return fmt(tot * 0.0254, 4) + " m"
    # the last number of '108 by 36' is followed by nothing; without the $ it stayed in inches
    t = re.sub(r"\d+(?:-\d+/\d+)?(?:\.\d+)?(?=\s*(?:inch|in\b|by|$))", rep, s)
    t = t.replace(" inch", "").replace(" m by ", " m by ")
    return t

# ----------------------------------------------------------------------------- data

def load():
    d = {}
    d["experiments"] = read_csv("data/experiments/index.csv")
    d["experiments_meta"] = read_json("data/experiments/index.json")
    d["materials"] = read_csv("data/materials/materials.csv")
    d["materials_meta"] = read_json("data/materials/materials.json")
    d["figures"] = read_csv("corpus/1968/figures.csv")
    d["figures_meta"] = read_json("corpus/1968/figures.json")
    d["figures_vol2"] = read_csv("corpus/1968-vol2/figures.csv")
    d["figures_vol2_meta"] = read_json("corpus/1968-vol2/figures.json")
    d["register"] = read_csv("sources/register.csv")
    d["leads"] = read_csv("sources/leads.csv")
    d["audits"] = read_csv("qa/audits.csv")
    d["decisions"] = read_csv("docs/decisions.csv")
    d["insights"] = sorted(p.name for p in (ROOT / "insights").glob("*.md"))
    d["observation_files"] = sorted(p.relative_to(ROOT).as_posix()
                                    for p in (ROOT / "data" / "experiments").glob("*/observations.csv"))
    d["reviews"] = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "qa").glob("*/review.md"))
    d["fig_by_id"] = {r["id"]: r for r in d["figures"]}
    d["fig2_by_id"] = {r["id"]: r for r in d["figures_vol2"]}
    d["mat_by_no"] = {m["soil_no"]: m for m in d["materials"]}
    d["cells_by_id"] = {c["experiment_id"]: c for c in d["experiments_meta"]["cells"]}
    alts = {}
    for a in d["experiments_meta"]["descriptive_alternates"]:
        alts.setdefault(a["experiment_id"], []).append(a)
    d["alts_by_id"] = alts
    d["thumbs"] = {p.stem: p for p in CACHE.glob("p*.png")} if CACHE.exists() else {}
    d["thumbs2"] = {p.stem: p for p in CACHE2.glob("p*.png")} if CACHE2.exists() else {}
    d["plots"] = {p.stem: p for p in PLOTS.glob("*.png")} if PLOTS.exists() else {}
    d["overlays"] = {p.stem: p for p in OVERLAYS.glob("*.png")} if OVERLAYS.exists() else {}
    d["observations"] = {}
    for p in (ROOT / "data" / "experiments").glob("*/observations.csv"):
        meta_p = p.with_name("series.json")
        d["observations"][p.parent.name] = {"rows": read_csv(p.relative_to(ROOT).as_posix()),
                                             "meta": read_json(meta_p.relative_to(ROOT).as_posix()) if meta_p.exists() else {}}
    d["runs"] = {}   # records of kind run-table: a printed table of runs (tools/build_run_table.py, D-050)
    for p in (ROOT / "data" / "experiments").glob("*/runs.csv"):
        meta_p = p.with_name("runs.json")
        d["runs"][p.parent.name] = {"rows": read_csv(p.relative_to(ROOT).as_posix()),
                                    "meta": read_json(meta_p.relative_to(ROOT).as_posix()) if meta_p.exists() else {}}
    return d


def counters(d):
    ex = d["experiments"]
    single = [r for r in ex if r["kind"] == "single"]
    return OrderedDict([
        ("Indexed records", (len(ex), "rows in the experiment index: single tests, averaged and derived series, correlations, text summaries and bin samples")),
        ("Single physical tests", (len(single), "rows of kind `single`: one physical test on one bed")),
        ("Tests with complete printed setup", (sum(1 for r in ex if r["setup_status"] == "complete"), "rows whose bed state, apparatus geometry, bin and loading rate are all printed in the source")),
        ("Observation series extracted", (len(d["observation_files"]), "experiments with an `observations.csv` (digitized points) in `data/experiments/`")),
        ("Human audits recorded", (len(d["audits"]), "rows in `qa/audits.csv`; agreement between the two agents is not an audit")),
    ])


def state_of_row(d, r):
    if r["soil_no"] in d["mat_by_no"]:
        m = d["mat_by_no"][r["soil_no"]]
        return m["family"], m["state"]
    fam = r["soil_family"] or "unknown"
    if r["soil_no_status"] == "conflict":
        return fam, "conflicting evidence"
    sp = r["state_printed"].lower()
    # every state the printed text names, in printed order: a record of several beds (a run table) names each
    found = sorted({{"inter": "intermediate"}.get(w, w): sp.find(w) for w in ("dense", "intermediate", "inter", "loose")
                    if w in sp and not (w == "inter" and "intermediate" in sp)}.items(), key=lambda kv: kv[1])
    words = [w for w, _ in found]
    state = (" and ".join(words) + " (printed; not a numbered soil)") if words else "state not printed"
    return fam, state


def coverage(d):
    cells = Counter(); types = set()
    for r in d["experiments"]:
        if r["kind"] != "single":
            continue
        fam, state = state_of_row(d, r)
        for t in r["test_type"].split(";"):
            cells[(fam, state, t)] += 1; types.add(t)
    types = sorted(types)
    keys = sorted({(f, s) for (f, s, _) in cells})
    return types, keys, cells


def thumb(d, pdf_page, width=None, depth=1, vol=1):
    name = f"p{int(pdf_page):04d}"
    thumbs, img_rel = (d["thumbs"], IMG_REL) if vol == 1 else (d["thumbs2"], IMG_REL2)
    if name not in thumbs:
        return f"*thumbnail not rendered (PDF {pdf_page})*"
    rel = "../" * depth + f"{img_rel}/{name}.png"
    # a sized thumbnail opens full size on click too: the figures page says so (Codex's review, 2026-11-20)
    w = f"{{width={width} .lightbox}}" if width else "{.lightbox}"
    return f"![{'' if vol == 1 else 'Vol. II '}PDF page {pdf_page}]({rel}){w}"


def copy_thumbs(d, out_dir):
    copied, missing = 0, []
    for figs, thumbs, img_rel in ((d["figures"], d["thumbs"], IMG_REL), (d["figures_vol2"], d["thumbs2"], IMG_REL2)):
        dst = out_dir / img_rel
        dst.mkdir(parents=True, exist_ok=True)
        needed = {f"p{int(r['pdf_page']):04d}" for r in figs}
        for name in sorted(needed):
            src = thumbs.get(name)
            if src and not (dst / src.name).exists():
                shutil.copy2(src, dst / src.name); copied += 1
        missing += sorted(f"{img_rel}/{n}" for n in needed if n not in thumbs)
    # Plots and overlays: every cached image is copied (they are regenerated with the data).
    for cache, img_rel in ((d["plots"], IMG_PLOTS), (d["overlays"], IMG_OVERLAYS)):
        dst = out_dir / img_rel
        dst.mkdir(parents=True, exist_ok=True)
        for src in cache.values():
            if not (dst / src.name).exists() or (dst / src.name).stat().st_mtime < src.stat().st_mtime:
                shutil.copy2(src, dst / src.name); copied += 1
    for vol, pdf in sorted(LINKED_PAGES):   # pages a citation opens (page_link); rendered by tools/render_pages.py
        thumbs, img_rel = (d["thumbs"], IMG_REL) if vol == 1 else (d["thumbs2"], IMG_REL2)
        src = thumbs.get(f"p{pdf:04d}")
        if src and not (out_dir / img_rel / src.name).exists():
            shutil.copy2(src, out_dir / img_rel / src.name); copied += 1
        elif not src:
            missing.append(f"{img_rel}/p{pdf:04d}")
    for exp in d["observations"]:
        if exp not in d["plots"]:
            missing.append(f"{IMG_PLOTS}/{exp}")
    return copied, missing


def observations_section(d, i):
    """The recovered-data section of an experiment page: plots, overlays, counts, calibrations, files."""
    obs = d["observations"].get(i)
    if not obs:
        return []
    rows, meta = obs["rows"], obs["meta"]
    fig_id = meta.get("figure_id", "")
    figs = meta.get("figures") or [fig_id]   # a record from several figures (series.json `figures`, 2026-11-19)
    panels_m = meta.get("panels", {})
    if len(figs) > 1:
        per = {f: sum(1 for r in rows if panels_m.get(r["panel"], {}).get("figure_id") == f) for f in figs}
        src = "; ".join(f"{n} from {f}" for f, n in per.items())
    else:
        src = f"from {fig_id or 'the figure'}"
    b = ["## Recovered observations", ""]
    b.append(f"{len(rows)} points ({src}) read by two readings made separately and reconciled "
             f"(batch `{meta.get('batch', '')}`, rules `{meta.get('reading_rules', '')}`). Values are SI; the printed-unit "
             "values and the pixel coordinates on the page image are kept beside them so every point can be checked "
             "against the scan. " + (meta.get("bounds") or "Bounds are reading bounds, not standard deviations."))
    b.append("")
    ov = sorted(k for f in figs for k in d["overlays"] if k.startswith(f + "-"))
    if ov:
        b.append("Both readings drawn on the page image (filled circles: Claude's reading; hollow squares: Codex's; bars: "
                 "pixel bounds; the canonical reading of each panel is named in the batch review). Click to enlarge.")
        b.append("")
        for k in ov:
            b.append(f"![Overlay {k}](../{IMG_OVERLAYS}/{k}.png){{.lightbox}}")
            b.append("")
    pts = meta.get("points", {})
    b.append(table(["panel", "quantity (x)", "quantity (y)", "points"],
                   [[p + (f" ({v['figure_id']} panel {v['figure_panel']})" if v.get("figure_id") else ""),
                     f"{v['x_quantity']} ({v['x_unit_si']}, from {v['x_unit_native']})", f"{v['y_quantity']} ({v['y_unit_si']}, from {v['y_unit_native']})",
                     str(pts.get("by_panel", {}).get(p, ""))] for p, v in sorted(meta.get("panels", {}).items(), key=lambda kv: int(kv[0]))]))
    for p, v in sorted(panels_m.items(), key=lambda kv: int(kv[0])):   # a panel's relation and note (series.json)
        extra = "; ".join(x for x in (f"{v['relation']}" if v.get("relation") else "", v.get("note", "")) if x)
        if extra:
            b.append(f"Panel {p}: {extra.rstrip('.')}.")
            b.append("")
    for br in meta.get("breaks", []):
        b.append(f"Panel {br['panel']}, {br['series_id']}: the line is broken after {br['after']['source']} sample "
                 f"{br['after']['sequence']}: {br['reason']}.")
        b.append("")
    b.append("")
    b.append("Points by status: " + ", ".join(f"{status_span(k)} {v}" for k, v in sorted(pts.get("by_status", {}).items()))
             + "; by kind: " + ", ".join(f"`{k}` {v}" for k, v in sorted(pts.get("by_kind", {}).items())) + ".")
    b.append("")
    cal_rows = []
    for reader, panels in meta.get("calibrations", {}).items():
        for pname, c in panels.items():
            cal_rows.append([reader, pname, str(c["n_anchors"]), f"{c['rms_residual_x']:.3g} / {c['max_residual_x']:.3g}",
                             f"{c['rms_residual_y']:.3g} / {c['max_residual_y']:.3g}"])
    if cal_rows:
        b.append(table(["reader", "panel", "anchors", "x residual rms / max (printed units)", "y residual rms / max"], cal_rows,
                       caption="Axis calibration of each reading: affine fit on the grid intersections; residuals in the printed units."))
        b.append("")
    b.append(f"Files: [observations.csv](../files/data/experiments/{i}/observations.csv), "
             f"[series.json](../files/data/experiments/{i}/series.json) (repository paths `data/experiments/{i}/`).")
    b.append("")
    return b

# ----------------------------------------------------------------------------- pages

# ----------------------------------------------------------------------------- reader-facing pages
# Plan v3, Part A (approved by Dan 2026-11-05): the site is rewritten for human readers, pilot first. The
# pilot is the navbar, the landing page, the Glossary, "Simulate a test", About, Contribute, Project records
# and ONE record page built around the virtual experiment card (PILOT_RECORD); the other record pages keep
# the older template until Dan has looked at the pilot. Codes (soil names, test names, symbols) are spelled
# out at first use and carry a hover definition (term()); undefined_terms() fails the build when a page of
# PILOT_PAGES uses a code without defining it on that page (A2.3).

PILOT_RECORD = "b68-lpt-024"
START_OVERLAY = "F2-42-p1"   # the overlay the home page's Start here links (the pilot record's figure)
GITHUB = "https://github.com/uwsbel/terramechanics-reference-data"
ISSUE_FORM = f"{GITHUB}/issues/new?template=report-a-value.yml"   # .github/ISSUE_TEMPLATE/report-a-value.yml
CONTACT = "Dan Negrut, [negrut@wisc.edu](mailto:negrut@wisc.edu)"

# Plain names of the test soils, worded from the report's own glossary (AM-68-1 Vol. I, printed 2-2 and 2-3,
# PDF 27 and 28) and, for SS, from its soil table (Table 2-3, printed 2-16, PDF 41).
SOIL_NAMES = OrderedDict([
    ("RS", "red crushed volcanic scoria, narrowly graded"),
    ("PS", "white crushed pumice, narrowly graded"),
    ("RSM-a", "RS mixed with crushed marble, 5 to 7 by weight, narrowly graded"),
    ("RSM-b", "RS mixed with crushed marble, 1 to 3 by weight, narrowly graded"),
    ("RC2", "red crushed volcanic scoria, broadly graded"),
    ("SS", "white silica sand (Wedron 4040), narrowly graded"),
    ("LSM", "broadly graded scoria (RC2) mixed with air-floated clay"),
])
SOIL_SHORT = {"RS": "red scoria", "PS": "white pumice", "RSM-a": "scoria and marble mix", "RSM-b": "scoria and marble mix",
              "RC2": "broadly graded red scoria", "SS": "silica sand", "LSM": "scoria and clay mix", "RSM": "scoria and marble mix"}
# Hover definitions. A title attribute is plain text: no double quotes, no markup.
TERMS = dict(SOIL_NAMES)
TERMS.update({
    "RSM": "RS mixed with crushed marble (RSM-a or RSM-b)",
    "LPT": "load-penetration test: a tool is pushed into a soil bed and the load is recorded against depth",
    "DPT": "dynamic penetrometer test: a probe of fixed mass falls from a fixed height into the bed and its peak deceleration is recorded",
    "Dr": "relative density: 0 at the soil's maximum void ratio (loosest) and 1 at its minimum (densest), from the reference void-ratio limits; a bed packed past the reference densest state reads above 1",
    "Gp": "peak deceleration of the dynamic penetrometer, in g: the report's index of the density and uniformity of a bed",
    "D50": "grain size that half of the soil, by weight, is finer than",
    "D95": "grain size that 95 percent of the soil, by weight, is finer than",
    "Cu": "uniformity coefficient: D60 divided by D10; near 1 for a narrowly graded soil",
    "D10": "effective size: the grain size that 10 percent of the soil, by weight, is finer than",
    "D60": "the grain size that 60 percent of the soil, by weight, is finer than",
    # the model-drop symbols, worded from the legend of Table 5-T3 (AM-68-1 Vol. I, printed 5-45, PDF 325) and the text
    # beside it (printed 5-44, PDF 324); Dan, 2026-11-20: hover definitions for the new families' symbols too
    "V_v": "vertical velocity of the LM model at touchdown; Table 5-T3 prints it negative, the downward direction",
    "V_h": "horizontal velocity of the LM model at touchdown",
    "tau": "time from the release of the LM model to its touchdown, measured from an accelerometer record",
    "phi": "angle of internal friction of the soil",
})
# Plain names used at a code's first use on a page ("mean grain size (D50)").
SHORT = dict(SOIL_SHORT, LPT="load-penetration test", DPT="dynamic penetrometer test", Dr="relative density",
             Gp="dynamic penetrometer reading", D50="mean grain size", D95="95 percent size", Cu="uniformity coefficient",
             D10="effective size", D60="60 percent size")
PILOT_PAGES = ("index.qmd", "about/index.qmd", "contribute/index.qmd", "glossary/index.qmd", "simulate/index.qmd",
               "records/index.qmd", f"experiments/{PILOT_RECORD}.qmd")


def term(code, text=None):
    """A code with its definition: a tooltip on hover, and on tap or keyboard focus (tabindex; site.css shows the
    title on :focus). A code with no definition is returned as it is."""
    return f'[{text or code}]{{.term title="{TERMS[code]}" tabindex="0"}}' if code in TERMS else (text or code)


def define(code):
    """First use of a code on a page: the plain name, then the code with its definition."""
    return f"{SHORT.get(code) or TERMS[code].split(':')[0]} ({term(code)})"


def undefined_terms(text):
    """Problems with codes on a reader page (plan v3, A2.3), in reading order over the title, the subtitle and the body
    (link text and image descriptions included; code spans, link targets, attributes and comments left out):
    1. a definition span whose text is not a known code, or whose definition is not that code's;
    2. a code whose first use is neither a definition span nor written in parentheses after its plain name, as in
       'red scoria (RS)'. Later uses may be bare: the definition is on the page."""
    front, body = (text.split("\n---\n", 1) + [""])[:2] if text.startswith("---") else ("", text)
    heads = " ".join(json.loads(v) for k, v in re.findall(r"^(title|subtitle): (\".*\")$", front, re.M))
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S).split("::: {.generated-note}")[0]
    problems = []
    for m in re.finditer(r"\[([^\[\]]*)\]\{\.term title=\"([^\"]*)\"[^}]*\}", body):
        if TERMS.get(m.group(1)) != m.group(2):
            problems.append(f"definition span [{m.group(1)}] does not define it")
    seq = heads + "\n" + body
    seq = re.sub(r"\[([^\[\]]*)\]\{\.term [^}]*\}", lambda m: "\x01" + m.group(1) + "\x02", seq)
    seq = re.sub(r"`[^`]*`", " ", seq)
    seq = re.sub(r"\]\([^)]*\)", "]", seq)
    seq = re.sub(r"\{[^}]*\}", " ", seq)
    for c in TERMS:
        m = re.search(rf"(?<![\w-]){re.escape(c)}(?![\w-])", seq)
        if m and not (seq[m.start() - 1: m.start()] == "\x01" or (seq[m.start() - 1: m.start()] == "(" and seq[m.end(): m.end() + 1] == ")")):
            problems.append(f"{c} used before it is defined")
    return problems


def btn(text, href, primary=False):
    return f"[{text}]({href}){{.btn {'.btn-primary' if primary else '.btn-outline-primary'} .me-2 .mb-2}}"


def fig_label(fid):
    """'F2-42' -> 'Fig. 2-42', 'FC-7B' -> 'Fig. C-7B', 'T2-3' -> 'Table 2-3'."""
    return ("Table " + fid[1:]) if fid.startswith("T") else ("Fig. " + fid[1:])


def fig_cite(d, fid):
    """A figure cited in the AGENTS.md form: report, volume, figure, printed page, PDF page."""
    f, vol = (d["fig_by_id"].get(fid), "Vol. I") if fid in d["fig_by_id"] else (d["fig2_by_id"].get(fid), "Vol. II")
    return f"AM-68-1 {vol}, {fig_label(fid)}, printed {f['printed_page']}, PDF {f['pdf_page']}" if f else fid


TEST_PLURAL = {"ds": "direct shear tests", "lpt": "load-penetration tests", "sonic": "sonic modulus tests",
               "dpt": "dynamic penetrometer tests", "dens": "density tests", "gs": "grain size analyses", "tx": "triaxial tests",
               "imp": "footpad impact tests", "mdrop": "drops of a 1/6-scale Lunar Module model"}
# setup_status in words, for the Find a test listing (2026-11-21, Dan: no raw codes in a reader's table)
SETUP_WORDS = {"complete": "complete", "setup_incomplete": "incomplete", "pending": "tests not identified"}


def soil_codes(d):
    """The soil codes of the report's soil table, in table order (from the designations, 'RS Loose' -> 'RS')."""
    return list(dict.fromkeys(m["bendix_designation"].split()[0] for m in d["materials"]))


def page_index(d):
    with_data = Counter(r["test_type"] for r in d["experiments"] if r["kind"] == "single" and r["experiment_id"] in d["observations"])
    parts = [f"{n} {TEST_PLURAL.get(t, t)}" for t, n in sorted(with_data.items(), key=lambda kv: (-kv[1], kv[0]))]
    counts = ", ".join(parts[:-1]) + (" and " if len(parts) > 1 else "") + parts[-1]
    b = []
    # Approved wording (plan v3, A5.2), kept as written.
    b.append("This site provides laboratory soil tests as numbers: for example, the force needed to push a cylinder into "
             "sand as it goes deeper, or the stress at which a soil sample fails in shear. Each test comes with what one "
             "would need to set up the same test in a simulator (the soil, how its bed was prepared, the tool and how it "
             "moved), and states what the original report leaves out. Every number links to the page of the report it "
             "was read from.")
    b.append("")
    b.append("This is the beginning of an effort to collect, curate and share well-documented test data that can be used "
             "to judge the simulation tools used in terramechanics. To that end, the site also shows how the data are "
             "meant to be used with an open-source simulator to gauge its accuracy.")
    b.append("")
    b.append("For instance, one set of tests comes from a 1968 NASA study for the Apollo Lunar Module, in which twelve soil "
             "conditions were tested on Earth to predict how the lander's footpads would behave on the Moon.")
    b.append("")
    b.append("The collection will grow with further tests, and contributions are welcome of two kinds: data from new "
             "physical tests, and scripts that run virtual experiments mirroring the physical tests hosted here.")
    b.append("")
    b.append(" ".join([btn("Find a test", "experiments/index.qmd", primary=True), btn("Simulate a test", "simulate/index.qmd"),
                       btn("Contribute", "contribute/index.qmd"),
                       btn("How the numbers were read and checked", "about/index.qmd#how-the-numbers-were-read-and-checked")]))
    b.append("")
    b.append("## Start here")
    b.append("")
    b.append(f"One test, from its setup to its citation: [{term('LPT')} 24](experiments/{PILOT_RECORD}.qmd), a 4-inch (102 mm) "
             "cylinder pushed into a bed of dense red scoria.")
    b.append("")
    b.append("1. Its page gives the setup as a virtual experiment card: the soil, the bed, the tool and the motion, each value "
             "with the page it is printed on, and what the report leaves out.")
    b.append(f"2. Its points are in [observations.csv](files/data/experiments/{PILOT_RECORD}/observations.csv): load against "
             "penetration in SI units, with the value as printed kept beside each one.")
    b.append("3. Each point carries a reading bound, how precisely it could be read off the printed figure (not the scatter of "
             "the experiment), and a status that says how it was checked; the [Glossary](glossary/index.qmd) defines both.")
    anchor = "#check-f2-42" if START_OVERLAY in d["overlays"] else ""   # the anchor exists only with its overlay
    b.append(f"4. Each point traces to the scan: the [Figures](figures/index.qmd{anchor}) page draws the two readings over "
             "the printed figure, Fig. 2-42.")
    b.append(f"5. To cite it: the release by its DOI, and the record by its id and source page, for example record "
             f"`{PILOT_RECORD}`, AM-68-1 Vol. I, Fig. 2-42, printed 2-77, PDF 102 ([Download](downloads/index.qmd#how-to-cite) "
             "gives the entries).")
    b.append("")
    b.append("[Simulate a test](simulate/index.qmd) walks through setting this test up in a simulator.")
    b.append("")
    b.append("## In the collection")
    b.append("")
    b.append(f"Measured data for {counts}, on these test soils:")
    b.append("")
    b.append(table(["code", "soil"], [[term(c), SOIL_NAMES.get(c, c)] for c in soil_codes(d)]))
    return page("Terramechanics Reference Data", "\n".join(b), ["data/experiments/index.csv", "data/materials/materials.csv"],
                extra_yaml={"subtitle": "Measured soil tests for judging terramechanics simulations.", "toc": False}, reader=True)


def page_records(d):
    """Project records: the maintainers' material, public but off the reader's path (plan v3, A1.4)."""
    c = counters(d)
    types, keys, cells = coverage(d)
    b = ["How the collection is built and checked, kept public because the project is open and invites help. "
         "None of this is needed to use the data.", ""]
    items = ([] if private("docs/ROADMAP.md") else ["[Roadmap](../roadmap.qmd): what comes next and how far along it is."]) + [
        "[Decisions](../decisions.qmd): " + ("the decisions that shaped the method, with their options." if PRIVATE
                                             else "every decision taken, with its options and reasons."),
        "[Review](../review/index.qmd): the record of human checks, and every value that rests on one reading only.",
        "[Open questions](../open-questions.qmd): what could not be settled, with the evidence, and how to help.",
        "[Methods](../methods/index.qmd): data organization, the reading rules and how the agents work.",
        "[Insights](../insights/index.qmd): judgment and caveats the report authors recorded.",
        "[Figures](../figures/index.qmd) and [Sources](../sources/index.qmd): every figure of the report sections indexed, and the register of sources."]
    b += [f"{n}. {s}" for n, s in enumerate(items, 1)]
    b.append("")
    b.append("## Coverage")
    b.append("")
    b.append("Single physical tests by soil and state (rows) and test type (columns). A zero means the report documents "
             "no such test in the pages inventoried so far. A state marked `printed; not a numbered soil` is printed "
             "beside the test but is not one of the twelve soils of the report's soil table (for example dense "
             f"{define('RS')} at a {define('Dr')} of 0.94 to 0.97).")
    b.append("")
    headers = ["soil", "state"] + types + ["all"]
    rows = []
    for (f, s) in keys:
        vals = [cells.get((f, s, t), 0) for t in types]
        rows.append([term(f), s] + [str(v) for v in vals] + [str(sum(vals))])
    tot = [sum(cells.get((f, s, t), 0) for (f, s) in keys) for t in types]
    rows.append(["**all**", "", *[f"**{v}**" for v in tot], f"**{sum(tot)}**"])
    b.append("::: {.coverage}")
    b.append(table(headers, rows, num_cols=types + ["all"]))
    b.append(":::")
    b.append("")
    b.append(": Test types: `lpt` load penetration, `ds` direct shear, `dpt` dynamic penetrometer, `dens` density "
             "(compaction time study), `gs` grain size, `tx` triaxial, `sonic` sonic modulus. Source: "
             "`data/experiments/index.csv`, kind = single.")
    b.append("")
    b.append("## Five counts that measure different things")
    b.append("")
    b.append(table(["count", "value", "what it counts"], [[k, str(v), w] for k, (v, w) in c.items()], num_cols=["value"]))
    b.append("")
    b.append("## Open decisions")
    b.append("")
    open_d = [r for r in d["decisions"] if not r["decision"].strip()]
    b += [f"- **{r['id']}** ({r['date']}): {r['question']} Options: {r['options']}. {r.get('note', '')}".rstrip() for r in open_d] or ["None open."]
    b.append("")
    b.append("## Recent changes")
    b.append("")
    b.append("{{< include ../_changes.md >}}")
    return page("Project records", "\n".join(b),
                ["data/experiments/index.csv", "data/materials/materials.csv", "qa/audits.csv", "docs/decisions.csv"], reader=True)


def page_about(d):
    reg = [r for r in d["register"] if r["status"] == "acquired"]
    b = ["Terramechanics Reference Data collects measured soil tests and the setup of each, so that a simulation of the "
         "same test can be compared with the measurement. It is maintained by the Simulation-Based Engineering Laboratory "
         "(SBEL), University of Wisconsin-Madison.", ""]
    b.append("## Sources")
    b.append("")
    b.append("The tests come from published reports. Those in this release come from the Bendix "
             "\"Lunar Module (LM) Soil Mechanics Study\" (NASA, 1968, report AM-68-1), in two volumes: Volume I, Sections II "
             "to V (soil selection and the basic tests, the drag and impact tests, and the 1/6-scale Lunar Module model "
             "drops) and Volume II, Appendices A to C (soil specifications, sonic moduli and "
             "the full direct shear program). NASA's technical reports server lists it for public distribution, with public use permitted. The page images "
             "on this site come from it, courtesy of NASA; the report itself is linked, not copied: "
             "[Volume I](https://ntrs.nasa.gov/citations/19680021852) and [Volume II](https://ntrs.nasa.gov/citations/19680021853) "
             "(D-054). The "
             f"[Sources](../sources/index.qmd) page lists the {len(reg)} reports acquired for the collection and the leads being considered.")
    b.append("")
    b.append("## How the numbers were read and checked")
    b.append("")
    b.append("Most numbers in the reports exist only as printed figures. Each figure whose numbers are in the data was read "
             "twice, separately, by two readers (the AI systems Claude and Codex), each from the scanned page and without "
             "seeing the other's reading. In some early batches both readers also saw notes from an earlier step, so "
             "those readings were not fully independent; the review record of each batch says where. "
             "A script compared the two readings point by point. Where they disagreed, a fresh reading of the page, made "
             "without knowing which reading was whose, settled it, or the point was left marked as unsettled. Then student "
             "reviewers compare a sample of the points with the scan, and every check they make is recorded.")
    b.append("")
    b.append("Every point carries:")
    b.append("")
    b.append("1. its source: the report, the figure or table, the printed page and the page of the PDF file;")
    b.append("2. a reading bound: how precisely it could be read from the printed figure (not the scatter of the "
             "experiment, which the reports rarely give);")
    b.append("3. a status word that says which of the checks above it passed (see the [Glossary](../glossary/index.qmd#status-words)).")
    b.append("")
    b.append("Values are given in SI units, with the printed value kept beside them. On the [Figures](../figures/index.qmd) "
             "page both readings are drawn over the scanned page, so any point can be checked by eye. The detailed rules are "
             "in [Methods](../methods/index.qmd).")
    b.append("")
    b.append("## Known limitations")
    b.append("")
    b.append("1. The numbers are read from scans more than half a century old; each point's reading bound says how precisely.")
    b.append("2. The reports rarely give the uncertainty of the experiments themselves. Tests repeated on similar beds "
             "show how much results can differ.")
    b.append("3. Some setups are incomplete: the depth of a soil bed, or how it was placed, is often not printed. Each "
             "test page lists what is missing as choices left to the user.")
    b.append("4. Only a sample of the points is checked by a person; each test page says how many.")
    b.append("5. Where the report contradicts itself (a test labeled differently in two figures), the record says so "
             "rather than choosing. The open questions, under [Project records](../records/index.qmd), list every such case.")
    b.append("")
    b.append("## Using the data")
    b.append("")
    b.append("1. Find a test: [Find a test](../experiments/index.qmd) lists every record; each test's page gives its setup, its "
             "plot and its source pages.")
    b.append("2. Download its values: the buttons under the plot give the points in SI (CSV) and how they were read (JSON); "
             "[Download](../downloads/index.qmd) gives the index files.")
    b.append("3. Trace a number: each value names the report, figure or table, printed page and PDF page; the scanned page is "
             "on the test's page, and the [Figures](../figures/index.qmd) page draws the readings over it.")
    b.append("4. Cite it: the release used, the record id, and the page of the report (each test's page shows how).")
    b.append("")
    b.append("## Contribute, cite, follow the work")
    b.append("")
    b.append("1. [Contribute](../contribute/index.qmd): data from new tests, scripts that run virtual experiments, corrections.")
    b.append("2. [Download](../downloads/index.qmd): the files, the license and how to cite.")
    b.append("3. [Project records](../records/index.qmd): " + ("" if private("docs/ROADMAP.md") else "roadmap, ")
             + "decisions, the review record and the open questions.")
    return page("About", "\n".join(b), ["sources/register.csv"], reader=True)


def page_contribute(d):
    b = ["The collection is open to contributions of two kinds, and to corrections. The maintainers review each one; "
         "once accepted, it is credited and listed in the changelog of the release that adds it.", ""]
    b.append("## Data from a physical test")
    b.append("")
    b.append("A test is useful for judging a simulator when its setup can be rebuilt. A submission contains:")
    b.append("")
    b.append("1. the measured quantities, as numbers, in SI or with their units stated;")
    b.append("2. the soil: what it is, its grain size, and its density in the test;")
    b.append("3. the bed: container size, fill depth, and how the soil was placed;")
    b.append("4. the tool or vehicle: shape, size, mass where it matters;")
    b.append("5. the motion: how the tool moved or was loaded, and how fast;")
    b.append("6. what was measured, with which instrument, and anything known about its accuracy;")
    b.append("7. what is not known, said plainly;")
    b.append("8. the source (a report, a paper, or the laboratory that ran the test) and permission to share the data.")
    b.append("")
    b.append("## A script that runs a virtual experiment")
    b.append("")
    b.append("A virtual experiment script mirrors one of the tests hosted here in a simulator. A submission states:")
    b.append("")
    b.append("1. which test it mirrors (the record id on the test's page);")
    b.append("2. the simulator and its version;")
    b.append("3. the inputs chosen where the record is silent (the choices left to the user on the test's card), with "
             "the reason for each;")
    b.append("4. its output, in the quantity that was measured (for a load-penetration test, the load on the tool against "
             "its penetration).")
    b.append("")
    b.append("## Corrections")
    b.append("")
    b.append("A point that looks wrong, a better scan of a page, or an answer to one of the open questions (under "
             "[Project records](../records/index.qmd)): give the page and, for a point, where it is on the scan. For a value "
             f"that looks wrong, the [Report a problem with a value]({ISSUE_FORM}) form asks for the release, the record id, "
             "the figure or table, the printed and PDF pages, and the evidence.")
    b.append("")
    b.append("## How to send it, and how it is reviewed")
    b.append("")
    b.append(f"Open an issue on the project's [GitHub repository]({GITHUB}). The maintainers check data against its "
             "source, and run a script to confirm that it gives the output it states. Accepted contributions enter "
             "under the same rules as everything else here: every number traceable to its source. Feedback not meant to be "
             f"public goes to {CONTACT}.")
    return page("Contribute", "\n".join(b), ["tools/build_site.py"], reader=True)


def page_glossary(d):
    gl = {r["term"]: r for r in read_csv("corpus/1968/glossary.csv")}
    def cite_gl(r):
        return f"AM-68-1 Vol. I, printed {r['printed_page']}, PDF {r['pdf_page']}"
    b = ["The codes, symbols and status words used on the pages for readers of this site. Where the 1968 report defines "
         "a term itself, its own definition is quoted with the page it is printed on.", ""]
    b.append("## Soils {#soils}")
    b.append("")
    rows = []
    for code, name in SOIL_NAMES.items():
        r = gl.get(code)
        if r:
            rows.append([term(code), name, esc(r["definition"]), cite_gl(r)])
        else:
            m = next((m for m in d["materials"] if m["bendix_designation"].split()[0] == code), None)
            rows.append([term(code), name, esc(m["description_verbatim"]) if m else "", "AM-68-1 Vol. I, Table 2-3, printed 2-16, PDF 41"])
    b.append(table(["code", "soil", "the report's definition", "where printed"], rows, widths=(9, 25, 44, 22)))
    b.append("")
    lm = gl.get("LM SMS")
    b.append("A *narrowly graded* soil has grains of nearly one size; a *broadly graded* one mixes a wide range of sizes. "
             f"{term('RSM')} stands for either mixture of {term('RS')} and crushed marble. The report's soil table "
             "gives each soil at one or more states, numbered 1 to 12 (the [Soils](../materials/index.qmd) page)."
             + (f" In the report's definitions, LM SMS is the study itself: the {lm['definition'].rstrip('.')} ({cite_gl(lm)})." if lm else ""))
    b.append("")
    b.append("## Soil states {#states}")
    b.append("")
    states = []
    for key, word in (("LOOSE", "loose"), ("INTER", "intermediate")):
        if key in gl:
            states.append([word, esc(gl[key]["definition"]), cite_gl(gl[key])])
    dense = next((r for r in gl.values() if r["definition"].startswith("Dense")), None)
    if dense:
        states.append(["dense", esc(dense["definition"]), cite_gl(dense)])
    b.append(f"A state is a range of {define('Dr')}: 0 at the soil's loosest reference state and 1 at its densest "
             "reference state (the maximum and minimum void ratios found by the minimum-maximum density tests); a bed packed past the densest "
             "reference state reads above 1.")
    b.append("")
    b.append(table(["state", "the report's definition", "where printed"], states, widths=(15, 60, 25)))
    b.append("")
    b.append("## Test types {#tests}")
    b.append("")
    b.append(table(["code on this site", "test", "what is measured"], [
        ["`lpt`", f"load-penetration test, {term('LPT')}", "the load on a tool (a cylinder or a footpad) pushed into a soil bed, against how deep it has gone"],
        ["`ds`", "direct shear test", "the shear stress that makes a soil sample slide along a plane, at a set normal stress, and how much the sample swells or shrinks"],
        ["`dpt`", f"dynamic penetrometer test, {term('DPT')}", f"the peak deceleration of a probe dropped into the bed, {term('Gp')}"],
        ["`dens`", "density test", "the density a soil reaches with a given compaction, or its loosest and densest states"],
        ["`gs`", "grain size analysis", "the fraction of the soil, by weight, finer than each sieve size"],
        ["`sonic`", "sonic modulus test", "the stiffness of a soil sample from the speed of a sound wave through it"],
        ["`tx`", "triaxial test", "the strength of a soil cylinder under a confining pressure"]], widths=(14, 30, 56)))
    b.append("")
    b.append("## Symbols {#symbols}")
    b.append("")
    sym = {r["symbol"]: r for r in read_csv("corpus/1968/symbols.csv")}
    def scite(s):
        r = sym.get(s)
        return f"AM-68-1 Vol. I, printed {r['printed_page']}, PDF {r['pdf_page']}" if r else ""
    b.append(table(["symbol", "meaning", "where the report defines it"], [
        [term("Dr"), "relative density: 0 at the soil's maximum void ratio (loosest reference state), 1 at its minimum (densest reference state); computed from the void ratio and those two limits, so a bed packed past the densest reference state reads above 1 (Vol. II reports up to 1.16)", scite("$D_r$")],
        ["unit weight, γ", "weight of soil per unit volume; the report prints it in pcf (pounds per cubic foot). This site gives the bulk density, mass per unit volume, in kg/m³", scite("γ")],
        ["friction angle, φ", "the angle of internal friction of the soil, from the direct shear tests", scite("φ")],
        ["E", "elastic (Young's) modulus", scite("E")],
        ["", "the soil table's modulus is measured by sonic means at 27.6 kPa (4 psi) confinement", "AM-68-1 Vol. I, Table 2-3, printed 2-16, PDF 41"],
        ["C", "cohesive strength, as used in the bearing capacity equation", scite("C")],
        ["", "the report found the apparent cohesion from its shear tests too large to match its bearing tests", "AM-68-1 Vol. I, printed 2-47, PDF 72"],
        [term("Gp"), "peak deceleration of the dynamic penetrometer, in g (one g is 9.81 m/s²)", "AM-68-1 Vol. I, Fig. 2-52, printed 2-89, PDF 114"],
        [term("D50"), "mean grain size: the grain size that half of the soil, by weight, is finer than", "AM-68-1 Vol. I, printed 2-26, PDF 51"],
        [term("D10"), "effective size: the grain size that 10 percent of the soil, by weight, is finer than", "AM-68-1 Vol. I, printed 2-26, PDF 51"],
        [term("D60"), "the grain size that 60 percent of the soil, by weight, is finer than", "AM-68-1 Vol. I, printed 2-26, PDF 51"],
        [term("Cu"), "uniformity coefficient, D60 divided by D10; near 1 for a narrowly graded soil", "AM-68-1 Vol. I, printed 2-26, PDF 51"],
        [term("D95"), "the grain size that 95 percent of the soil, by weight, is finer than", "AM-68-1 Vol. I, Table 2-3, printed 2-16, PDF 41"]],
        widths=(15, 58, 27)))
    b.append("")
    b.append("## Units {#units}")
    b.append("")
    b.append("Values are in SI. The reports use customary units; the value as printed is kept beside each converted one. "
             "The conversions use exact factors, shown here rounded to seven significant digits.")
    b.append("")
    b.append(table(["printed unit", "SI"], [
        ["inch (in)", f"{FACTORS[('in', 'm')] * 1000:g} mm"],
        ["pound-force (lb, lbf)", f"{FACTORS[('lbf', 'N')]:.6f} N"],
        ["pound per square inch (psi)", f"{FACTORS[('psi', 'Pa')] / 1000:.6f} kPa"],
        ["pound per square foot (psf)", f"{FACTORS[('psf', 'Pa')]:.6f} Pa"],
        ["pound per cubic foot (pcf), as a bulk density", f"{FACTORS[('pcf', 'kg_m3')]:.6f} kg/m³"],
        ["inch per minute (in/min)", f"{FACTORS[('in_min', 'm_s')] * 1000:.6f} mm/s"]]))
    b.append("")
    b.append("## Status words {#status-words}")
    b.append("")
    b.append("Each point of data carries one status, which says how it was checked.")
    b.append("")
    b.append(table(["status", "meaning"], [
        ["agreed", "the two readings, made separately, matched within their reading bounds"],
        ["resolved", "the readings differed, and a further reading of the page settled which was right"],
        ["one-sided-verified", "only one reading has the point, and the other reader confirmed it on the page"],
        ["one-sided", "only one reading has the point, and the other reader has not confirmed it; a person may or may not have checked it (audited and confirmed say so)"],
        ["pending-review", "unsettled; not yet decided"],
        ["audited", "the readings agreed, and two student reviewers also confirmed the point on the scan"],
        ["confirmed", "the point rested on a rule, a further reading or one reading, and two student reviewers confirmed it on the scan"]]))
    b.append("")
    b.append("The lists of tests and soils also carry a status for each row of the index, built the same way: agreed, "
             "normalized (matched once units or spelling were made the same), resolved or resolved-with-notes (settled by a "
             "further reading, with a note), rule or convention (settled by a documented rule), provisional (a count to be "
             "redone), conflict (the report gives two different values) and one-sided.")
    b.append("")
    b.append("A **reading bound** is how precisely a point could be read from the printed figure: a half-width, not a "
             "standard deviation, and not the uncertainty of the experiment.")
    b.append("")
    b.append("## Missing values {#missing}")
    b.append("")
    b.append("A value the data do not have is never shown as a blank or a zero, but as one of these:")
    b.append("")
    b.append(table(["shown as", "meaning"], [
        ["not reported", "the report does not give it"], ["not yet extracted", "the report gives it, but it is not in the data yet"],
        ["unreadable", "the scan does not allow a reading"], ["conflicting evidence", "the report gives two different values"],
        ["not applicable", "the quantity has no meaning for this test"]]))
    b.append("")
    b.append("## Kinds of record {#kinds}")
    b.append("")
    b.append(table(["kind", "meaning", "an independent test?"], [
        ["single", "one physical test on one soil bed", "yes"],
        ["averaged-series", "a curve the report says is averaged from several tests", "no"],
        ["derived-series", "a result the authors drew from identified tests, such as a failure envelope from several shear tests", "no"],
        ["correlation", "a fitted curve drawn without the points behind it", "no"],
        ["summary", "a number that exists only in the text", "no"],
        ["sample", "a sample from a soil bin, analyzed for grain size and density", "a measurement, not a test on a bed"],
        ["run-table", "a printed table of separate runs, one physical test per row (the subscale drag tests; the detail "
                      "correlation drops of the LM model, one record per soil family)", "yes, each run"]]))
    return page("Glossary", "\n".join(b), ["corpus/1968/glossary.csv", "corpus/1968/symbols.csv", "data/materials/materials.csv", "tools/to_si.py"], reader=True)


# ---- the virtual experiment card (plan v3, A3): docs/DATA-ORGANIZATION.md, "Virtual experiment card"

CARD_GROUPS = (("terrain", "Soil"), ("domain", "Bed"), ("body", "Tool"), ("motion", "Motion"),
               ("environment", "Environment"), ("measured", "Measured"), ("choices", "Missing: choices left to the user"))
KIND_TAG = {"test": "[reported]{.vk .vk-test}", "ref": "[soil reference]{.vk .vk-ref}",
            "choice": "[left to the user]{.vk .vk-choice}"}
# The report's density chart for each soil family (Vol. II, Appendix A): unit weight against relative density, with the
# 95 percent confidence limits. Used to read a bed's relative density from its printed unit weight (RS only so far).
DENSITY_CHART = {"RS": "b68-dens-fa-3"}
LINKED_PAGES = set()   # (volume, PDF page) of every page a reader page links to; copy_thumbs() copies their images


def page_link(pdf, label, vol=1, depth=1):
    """A citation that opens the page image (a rendered page in the thumbnail cache), never split across lines."""
    LINKED_PAGES.add((vol, int(pdf)))
    return f"[{label}]({'../' * depth}{IMG_REL if vol == 1 else IMG_REL2}/p{int(pdf):04d}.png){{.nw}}"


def fig_cite_short(d, fid):
    """A figure cited briefly inside the card (the card's lead names the report), linked to its page image."""
    if fid in d["fig_by_id"]:
        f = d["fig_by_id"][fid]
        return page_link(f["pdf_page"], f"{fig_label(fid)}, p. {f['printed_page']} (PDF {f['pdf_page']})")
    f = d["fig2_by_id"].get(fid)
    return page_link(f["pdf_page"], f"Vol. II, {fig_label(fid)}, p. {f['printed_page']} (PDF {f['pdf_page']})", vol=2) if f else fid


def text_page(printed, pdf, prefix=""):
    """A Volume I text page cited briefly inside the card, linked to its page image."""
    return page_link(pdf, f"{prefix}p. {printed} (PDF {pdf})")


def inches_mm(s):
    """'4 inch cylinder' -> (101.6, '4 in'); the first number of a printed length in inches."""
    m = re.search(r"\d+(?:\.\d+)?", s or "")
    return (float(m.group(0)) * 25.4, f"{m.group(0)} in") if m else (None, "")


def rate_mm_s(r):
    m = re.fullmatch(r"(\d+(?:\.\d+)?) in/min", (r["rate_printed"] or "").strip())
    return to_si(float(m.group(1)), "in_min", "m_s") * 1000.0 if m else None


def page_text(pdf_page):
    p = ROOT / "corpus" / "1968" / "pages" / f"p{int(pdf_page):04d}.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def printed_in(d, r, figs, pattern):
    """The record's figures that print a value matching `pattern` for THIS test, cited: first in the legend entry
    that names the test (from its label to the next test or entry), else anywhere on the page. An empty string when
    no page prints it, so a missing citation shows instead of a guess."""
    num = re.sub(r"^LPT No\. ?", "", r["test_label_printed"])
    label = re.compile(rf"LPT No\.?\s*{re.escape(num)}\b")
    def entries(f):
        legend = next((l for l in page_text(d["fig_by_id"][f]["pdf_page"]).splitlines() if l.startswith("legend:")), "")
        out = []
        for m in label.finditer(legend):
            rest = legend[m.end():]
            stop = min([k for k in (rest.find(";"), rest.find("LPT No")) if k >= 0] or [len(rest)])
            out.append(legend[m.start(): m.end() + stop])
        return out
    hit = [f for f in figs if any(re.search(pattern, e, re.I) for e in entries(f))]
    hit = hit or [f for f in figs if re.search(pattern, page_text(d["fig_by_id"][f]["pdf_page"]), re.I)]
    return "; ".join(fig_cite_short(d, f) for f in hit)


def density_chart_dr(d, family, gamma):
    """Relative density at unit weight `gamma` (N/m^3) on the report's density chart of the soil family: the mean
    curve and the two 95 percent confidence limits, by linear interpolation; None where a curve does not reach it."""
    rec = DENSITY_CHART.get(family)
    obs = d["observations"].get(rec) if rec else None
    if not obs:
        return None, {}
    out = {}
    for sid in ("mean", "lower", "upper"):
        pts = sorted((float(x["x_si"]), float(x["y_si"])) for x in obs["rows"] if x["series_id"] == sid and x["point_kind"] == "trace")
        out[sid] = next((x0 + (gamma - y0) / (y1 - y0) * (x1 - x0) for (x0, y0), (x1, y1) in zip(pts, pts[1:])
                         if min(y0, y1) <= gamma <= max(y0, y1) and y1 != y0), None)
    return rec, out


def card_lpt(d, r):
    """The card of a load-penetration test: {group: [(kind, text, where), ...]}. From the index row, the soil table,
    the figures index, the record's points, the page transcriptions and the report's sections on the apparatus and
    the procedure (facts that hold for the LPT bin and its beds in general are said to be general, and cited there)."""
    m = d["mat_by_no"].get(r["soil_no"])
    figs = [t for t in fig_ids(r) if t in d["fig_by_id"]]
    where = "; ".join(fig_cite_short(d, f) for f in figs)
    code = r["soil_family"]
    std_bin = (r["bin_printed_in"] or "").strip() == "18 by 36"
    obs = d["observations"].get(r["experiment_id"])
    c = {g: [] for g, _ in CARD_GROUPS}
    # soil
    state = state_of_row(d, r)[1].split(" (")[0]
    c["terrain"].append(("test", f"{SOIL_NAMES.get(code, code)} ({term(code)}), {state}; printed as *{esc(r['state_printed'])}*", where))
    gamma = None
    if r["unit_weight_printed_pcf"]:
        kg = to_si(float(r["unit_weight_printed_pcf"]), "pcf", "kg_m3")
        gamma = to_si(float(r["unit_weight_printed_pcf"]), "pcf", "N_m3")
        c["terrain"].append(("test", f"bulk density {kg:.0f} kg/m³ (unit weight {r['unit_weight_printed_pcf']} pcf as printed)",
                             printed_in(d, r, figs, re.escape(r["unit_weight_printed_pcf"]) + r"\s*pcf")))
    if r["dr_printed"]:
        c["terrain"].append(("test", f"{define('Dr')} {esc(r['dr_printed'])}", where))
    if r["gp_printed_g"]:
        c["terrain"].append(("test", f"{define('Gp')} {r['gp_printed_g']} g",
                             printed_in(d, r, figs, r"\(" + re.escape(r["gp_printed_g"]) + r"\)|Gp\s*=\s*" + re.escape(r["gp_printed_g"]))))
    if m:
        match = "matched to the test by the soil and its state, not printed with it" if r["soil_no_status"] == "inferred" else "printed with the test"
        c["terrain"].append(("ref", f"[soil No. {m['soil_no']}](../materials/index.qmd) of the report's soil table, *{m['bendix_designation']}* "
                                    f"({match}), at its nominal state: relative density {m['relative_density']}, bulk density "
                                    f"{m['bulk_density_kg_m3']} kg/m³, {define('D50')} {m['mean_grain_size_mm']} mm, {define('Cu')} "
                                    f"{m['uniformity_coeff']}, {define('D95')} {m['d95_mm']} mm, fines (finer than 0.075 mm) "
                                    f"{m['percent_passing_200'].replace('<', 'under ').replace('%', ' percent')}", text_page("2-16", 41, "Table 2-3, ")))
        c["terrain"].append(("ref", f"at that nominal state: friction angle {m['friction_angle_deg']} degrees (direct shear); modulus "
                                    f"{float(m['elastic_modulus_Pa']) / 1e6:.1f} MPa, measured with sound waves at 27.6 kPa (4 psi) "
                                    "confinement. The report warns that static and wave-based moduli can differ by an order of magnitude",
                             f"{text_page('2-16', 41, 'Table 2-3, ')}; {page_link(104, 'Vol. II, App. B, p. 1 (PDF 104)', vol=2)}"))
    c["terrain"].append(("ref", "air dried, as were all the test soils: 0.2 to 0.3 percent water by weight, occasionally 0.6",
                         text_page("2-103", 128)))
    # bed
    if r["bin_printed_in"]:
        wl = nums(r["bin_printed_in"])
        plan = " by ".join(f"{x * 0.0254:.3f} m" for x in wl)
        pat = r"\s*(?:inch|in\.?|\")?\s*by\s*".join(f"{x:g}" for x in wl)
        c["domain"].append(("test", f"bin {plan} in plan ({r['bin_printed_in']} in as printed)", printed_in(d, r, figs, pat)))
    if std_bin:
        c["domain"].append(("test", "the load-penetration bin: a box of 25 mm (1 in) plywood, 0.457 m wide, 0.914 m long and 0.914 m deep, "
                                    "with a front of plate glass 25 mm (1 in) thick and 0.457 m (18 in) deep, standing on load cells that "
                                    "weigh the soil", text_page("2-56", 81, "Sec. 2.6.1, ")))
    # tool
    dia, dia_in = inches_mm(r["penetrator_printed"])
    if dia:
        c["body"].append(("test", f"{r['penetrator_printed'].split()[-1]}, {dia:.1f} mm ({dia_in}) in diameter, pushed down into the bed by a "
                                  "hydraulic cylinder", f"{where}; {text_page('2-56', 81, 'Sec. 2.6.1, ')}"))
        if std_bin:
            c["body"].append(("test", f"in the standard setup the nearest wall of the bin is 229 mm (9 in, 4.5 radii) from the axis of a "
                                      f"{dia:.1f} mm cylinder, so the cylinder sits midway across the bin's width", text_page("2-59", 84)))
    # motion
    if r["start_depth_printed_in"] == "0":
        c["motion"].append(("test", "starts at the soil surface (start depth 0 in the test's record)", ""))
    elif r["start_depth_printed_in"]:
        c["motion"].append(("test", f"starts {float(r['start_depth_printed_in']) * 25.4:.1f} mm ({r['start_depth_printed_in']} in) below the surface", where))
    v = rate_mm_s(r)
    if v:
        rate_pat = re.escape(r["rate_printed"].split()[0]) + r"\s*(?:\"|in\.?)\s*/\s*min"   # 1"/min. or 1 in./min
        c["motion"].append(("test", f"pushed at a constant {v:.3f} mm/s ({r['rate_printed']} as printed); the operator keeps the rate by making "
                                    "the plotting pen follow a line of penetration against time",
                             f"{printed_in(d, r, figs, rate_pat)}; {text_page('2-57', 82)}; {text_page('2-59', 84)}"))
    if std_bin:
        c["motion"].append(("test", "the procedure pushes the cylinder 203 mm (8 in), or until the hydraulic supply reaches its capacity; "
                                    "how far this test went is not printed", text_page("2-59", 84)))
    # environment
    # the tests ran in a laboratory on Earth, and the report's glossary gives g for Earth, 32.2 ft/s^2 (printed 2-2,
    # PDF 27; Codex's second review, 2026-11-20, correcting the first, which had it unstated)
    c["environment"].append(("test", "laboratory test on Earth", ""))
    c["environment"].append(("test", "gravity: 9.81456 m/s², the report's value for Earth, 32.2 ft/s², converted exactly",
                             text_page("2-2", 27, "glossary, ")))
    # measured
    c["measured"].append(("test", "the load on the cylinder, from the test load cell, against its penetration, from a stroke wire, both "
                                  "drawn by an x-y plotter", text_page("2-56", 81, "Sec. 2.6.1, ")))
    if obs:
        pts = sorted(obs["rows"], key=lambda x: float(x["x_si"]))
        lo, hi = pts[0], pts[-1]
        frame = " (where it meets the frame of the plot)" if "frame" in hi["note"] else ""
        c["measured"].append(("test", f"the printed curve, read into the data, runs from {float(lo['x_si']) * 1000:.1f} to "
                                      f"{float(hi['x_si']) * 1000:.1f} mm of penetration{frame}",
                              fig_cite_short(d, obs["meta"].get("figure_id", ""))))
    # missing: each input the report does not give for this test, with what it says around it
    if std_bin:
        c["choices"].append(("choice", "fill depth: not printed. The procedure fills the box in stages and weighs the bed at six volume "
                                       "marks up to the full box (13.78 cubic feet, 0.390 m³) to check that its density is uniform",
                             text_page("2-57", 82, "Sec. 2.6.2, ")))
    if std_bin and state == "dense":
        c["choices"].append(("choice", "how the bed was placed and compacted: not printed for this test. The dense beds of these tests were "
                                       "generally made with a vibratory plate compactor, three passes per layer about 76 mm (3 in) thick, "
                                       "giving relative densities of 0.85 to 0.95", text_page("2-113", 138)))
    if obs and float(pts[0]["x_si"]) > 0:
        c["choices"].append(("choice", f"the zero of penetration: the printed load leaves zero at {float(pts[0]['x_si']) * 1000:.1f} mm; whether "
                                       "the cylinder touched the surface there or at zero is not stated",
                             fig_cite_short(d, obs["meta"].get("figure_id", ""))))
    if not r["dr_printed"]:
        txt, cites = "relative density of this bed: not printed", []
        avg_fig = next((f for f in figs if re.search(r"Dr approx (\d\.\d+)", d["fig_by_id"][f]["states"])), None)
        if avg_fig:
            val = re.search(r"Dr approx (\d\.\d+)", d["fig_by_id"][avg_fig]["states"]).group(1)
            txts = [t for t in r["evidence"].split(";") if t.strip().startswith("text")
                    and val in page_text(re.search(r"PDF (\d+)", t).group(1))]
            txt += f". The tests of {fig_label(avg_fig)}, this one among them, average about {val}"
            cites += [fig_cite_short(d, avg_fig)] + [text_page(*re.match(r"\s*text (\S+) \(PDF (\d+)\)", t).groups()) for t in txts]
        rec, dr = density_chart_dr(d, code, gamma) if gamma else (None, {})
        if dr.get("mean") is not None:
            lim = sorted(v for k, v in dr.items() if k != "mean" and v is not None)
            txt += (f". Read at this bed's density on the report's density chart for the soil, it is about {dr['mean']:.2f}"
                    + (f" ({lim[0]:.2f} to {'above 1' if len(lim) < 2 else f'{lim[1]:.2f}'} within the chart's 95 percent limits)" if lim else ""))
            cites.append(fig_cite_short(d, d["observations"][rec]["meta"]["figure_id"]))
        if m:
            txt += f". The soil table's {m['relative_density']} belongs to the soil's nominal state, not to this bed"
            cites.append(text_page("2-16", 41, "Table 2-3, "))
        c["choices"].append(("choice", txt, "; ".join(cites)))
    if m:
        c["choices"].append(("choice", "soil strength at this bed's density: the report plots friction angle against relative density",
                             fig_cite_short(d, "F2-23")))
    c["choices"].append(("choice", "cohesion: a bearing-capacity interpretation in the report, not a measured input. It found that the apparent "
                                   "cohesion of its shear tests predicts higher bearing loads than observed, and that about 0.7 kPa (0.1 psi), "
                                   "some 50 times less, explains some of the size effects in these tests", text_page("2-47", 72)))
    c["choices"].append(("choice", "the cylinder's end shape, length, material and surface, and where it stood along the bin: not printed", ""))
    c["choices"].append(("choice", "friction between the soil and the cylinder, and between the soil and the walls"
                                   + (" (plywood, glass)" if std_bin else "") + ": not reported", ""))
    c["choices"].append(("choice", "any model parameter the report does not measure, such as a static stiffness or the properties of "
                                   "grains", ""))
    return c


def card_table(card):
    rows = []
    for g, label in CARD_GROUPS:
        items = card[g] or [("choice", "*not given*", "")]   # an empty group is shown, never dropped
        for k, (kind, text, where) in enumerate(items):
            rows.append([f"**{label}**" if k == 0 else "", f"{KIND_TAG[kind]} {text}", where])
    return table(["", "what the record gives", "where printed"], rows, widths=(14, 60, 26))


def lpt_title(d, r):
    dia, dia_in = inches_mm(r["penetrator_printed"])
    tool = r["penetrator_printed"].split()[-1] if r["penetrator_printed"] else "tool"
    state = state_of_row(d, r)[1].split(" (")[0]
    num = re.sub(r"^LPT No\. ?", "", r["test_label_printed"])
    soil = f"{state} {SOIL_SHORT.get(r['soil_family'], 'soil')} ({r['soil_family']})"
    return f"Load-penetration test (LPT) {num}: {dia_in.replace(' in', '-inch')} ({dia:.0f} mm) {tool} pushed into {soil}"


def record_link(s):
    if s["test_label_printed"].startswith("LPT"):
        return f"[{term('LPT')} {re.sub(r'^LPT No. ?', '', s['test_label_printed'])}]({s['experiment_id']}.qmd)"
    return f"[{s['experiment_id']}]({s['experiment_id']}.qmd)"


def related_records(d, r):
    """(dependencies that must stay together, neighbors that are useful comparisons, the figures of the record)."""
    i = r["experiment_id"]
    figs = [t for t in fig_ids(r) if t in d["fig_by_id"] or t in d["fig2_by_id"]]
    by_id = {s["experiment_id"]: s for s in d["experiments"]}
    deps = []
    if len(figs) > 1:
        times = {2: "twice", 3: "three times"}.get(len(figs), f"{len(figs)} times")
        deps.append(f"This test is printed {times}, in {' and '.join(fig_label(f) for f in figs)}: one test, one record.")
    for t in (r.get("relation_target") or "").split(";"):
        if t.strip() in by_id:
            deps.append(f"This record is {r['relation'].replace('-', ' ')} {record_link(by_id[t.strip()])}.")
    for s in d["experiments"]:
        if i in (s.get("relation_target") or "").split(";"):
            deps.append(f"{record_link(s)} is {s['relation'].replace('-', ' ')} this record.")
    neighbors = []
    for f in figs:
        others = [s for s in d["experiments"] if s["experiment_id"] != i and f in fig_ids(s)]
        if others:
            title = (d["fig_by_id"].get(f) or d["fig2_by_id"].get(f))["title_as_printed"]
            neighbors.append(f"In {fig_label(f)} ({title}): {', '.join(record_link(s) for s in others)}.")
    return deps, neighbors, figs


def page_experiment_card(d, r):
    """The record page of the pilot, built around the virtual experiment card (plan v3, A3)."""
    i = r["experiment_id"]
    obs = d["observations"].get(i)
    card = card_lpt(d, r)
    b = []
    dia, dia_in = inches_mm(r["penetrator_printed"])
    v = rate_mm_s(r)
    kg = to_si(float(r["unit_weight_printed_pcf"]), "pcf", "kg_m3") if r["unit_weight_printed_pcf"] else None
    state = state_of_row(d, r)[1].split(" (")[0]
    b.append(f"A cylinder {dia:.1f} mm ({dia_in}) in diameter was pushed into a bed of {state} "
             f"{SOIL_SHORT.get(r['soil_family'], r['soil_family'])} ({term(r['soil_family'])}), and the load on it was recorded "
             f"against its penetration. This is a load-penetration test ({term('LPT')})" + (f", run at {v:.3f} mm/s" if v else "")
             + (f" in a bed of bulk density {kg:.0f} kg/m³" if kg else "") + ".")
    b.append("")
    if obs:
        rows = obs["rows"]
        pend = sum(1 for x in rows if x["status"] in ("pending-review", "one-sided"))
        n_aud, n_samp = audit_counts(rows)
        word = {1: "One"}.get(pend, str(pend))
        status = (f"**Data available:** {len(rows)} points read from the printed figure. "
                  + (f"{word} of them {'is' if pend == 1 else 'are'} still under review. " if pend else "All of them are settled. ")
                  + (f"Student reviewers have checked {n_samp} of them on the scan, and two reviewers confirmed {n_aud}." if n_samp
                     else "No person has checked them yet."))
    else:
        status = "**Data available:** not yet; the measurements of this test have not been read from the figure."
    b.append('::: {.callout-note appearance="simple"}')
    b.append(status)
    b.append(":::")
    b.append("")
    b.append("## Virtual experiment card")
    b.append("")
    b.append("What one would need to set up the same test in a simulator. Each value carries one of three marks: "
             f"{KIND_TAG['test']} given by the report for this test or its apparatus, or for the procedure of these tests in "
             f"general where the text says so; {KIND_TAG['ref']} a property of the soil from another table of the report, for "
             f"the soil's nominal state; {KIND_TAG['choice']} an input the report does not give, with what it says around it. "
             "Each citation opens the page of the report, AM-68-1 Volume I unless noted: the printed page number, then the "
             "page of the PDF file in parentheses.")
    b.append("")
    b.append("::: {.vx-card}")
    b.append(card_table(card))
    b.append(":::")
    b.append("")
    used = [c for c in TERMS if any(f"[{c}]{{.term" in t for g in card.values() for _, t, _ in g)]
    b.append("Codes on this card: " + "; ".join(f"{c}, {TERMS[c].split(':')[0]}" for c in used) + ".")
    b.append("")
    b.append("A simulation of this test is compared with the measurement through the axial force the soil exerts on the "
             "cylinder, the force the load cell measured, against the cylinder's penetration below the original soil surface. "
             "A comparison states where it puts the zero of force and of penetration, and whether the cylinder's own weight "
             "is included. The [Simulate a test](../simulate/index.qmd) page walks through the steps.")
    b.append("")
    if obs:
        meta = obs["meta"]
        fig_id = meta.get("figure_id", "")
        b.append("## Measured data")
        b.append("")
        trough = [x for x in obs["rows"] if x["point_kind"] == "feature" and "minimum" in x["note"]]
        b.append(f"![Load against penetration: this test in red, the other tests printed in {fig_label(fig_id)} in gray. The error "
                 "bars on the red curve are its reading bounds. The round markers are the curve's marked features (start, peaks, "
                 "troughs, end); filled ones were agreed by both readings, hollow ones were not."
                 + (f" The {({2: 'two', 3: 'three'}).get(len(trough), len(trough))} hollow markers near {statistics.mean(float(x['x_si']) for x in trough) * 1000:.0f} mm are "
                    "competing readings of the same trough, still being settled; they are one feature, not two."
                    if len(trough) > 1 else "")
                 + f" Click to enlarge.](../{IMG_PLOTS}/{i}.png){{.lightbox}}")
        b.append("")
        b.append(" ".join([btn("Download the points (CSV)", f"../files/data/experiments/{i}/observations.csv", primary=True),
                           btn("Download the reading record (JSON)", f"../files/data/experiments/{i}/series.json")]))
        b.append("")
        rows = obs["rows"]
        bx = statistics.median(float(x["x_bound_si"]) for x in rows)
        by = statistics.median(float(x["y_bound_si"]) for x in rows)
        b.append(f"The CSV file gives penetration in m (`x_si`) and load in N (`y_si`), each with its reading bound "
                 f"(`x_bound_si`, `y_bound_si`), and the status of each point. The JSON file gives the units, the conversion "
                 f"factors and how the points were read. A reading bound says how precisely a point could be read from the "
                 f"printed figure, typically {bx * 1000:.2f} mm in penetration and {by:.0f} N in load here. It is not the scatter "
                 "of the experiment, which the report does not give. "
                 f"[Both readings drawn over the scanned figure](../figures/index.qmd#check-{re.sub(r'[^a-z0-9]+', '-', fig_id.lower())}).")
        b.append("")
    deps, neighbors, figs = related_records(d, r)
    b.append("## Source pages")
    b.append("")
    b.append("; ".join(f"{fig_label(f)}, *{esc(d['fig_by_id'][f]['title_as_printed'])}*, {fig_cite(d, f)}" for f in figs if f in d["fig_by_id"])
             + "." + (f" The points were read from {fig_label(obs['meta'].get('figure_id', ''))}." if obs and len(figs) > 1 else "")
             + " Click a page to enlarge it.")
    b.append("")
    b.append("::: {layout-ncol=2}")
    for f in figs:
        if f in d["fig_by_id"]:
            b.append(thumb(d, d["fig_by_id"][f]["pdf_page"]))
            b.append("")
    b.append(":::")
    b.append("")
    if deps or neighbors:
        b.append("## Related tests")
        b.append("")
        if deps:
            b.append("Kept together whenever some tests tune a model and others check it:")
            b.append("")
            b += [f"{k + 1}. {x}" for k, x in enumerate(deps)]
            b.append("")
        if neighbors:
            b.append("Printed in the same figures, and useful for comparison. They are other tests, on other beds, and may differ "
                     "in rate, density or bin; they are not repeats of this test:")
            b.append("")
            b += [f"{k + 1}. {x}" for k, x in enumerate(neighbors)]
            b.append("")
    b.append("## How to cite")
    b.append("")
    src = obs["meta"].get("figure_id", "") if obs else ""
    b.append(f"Cite the release of this collection used, the record id `{i}`, and the source"
             + (f": the points come from {fig_cite(d, src)}" if src in d["fig_by_id"] else ": " + "; ".join(fig_cite(d, f) for f in figs))
             + "".join(f"; the same test is also printed in {fig_cite(d, f)}" for f in figs if f != src and f in d["fig_by_id"]) + ".")
    b.append("")
    b.append(f"<small>The full review record of these points (both readings, the decisions, the checks) is on the "
             f"[provenance page](../review/{i}.qmd).</small>")
    yaml = OrderedDict([("subtitle", f"{r['test_label_printed']} in the report; record {i}"), ("record", i), ("kind", r["kind"]),
                        ("test-type", TYPE_NAME.get(r["test_type"], r["test_type"])), ("family", r["soil_family"]),
                        ("state", state_of_row(d, r)[1]), ("printed-label", r["test_label_printed"]), ("evidence", r["evidence"]),
                        ("setup", SETUP_WORDS.get(r["setup_status"], r["setup_status"])),
                        ("record-status", r["status"]), ("priority", r["priority"]), ("mcc", r["mcc_relevant"])])
    return page(lpt_title(d, r), "\n".join(b), ["data/experiments/index.csv", "data/materials/materials.csv", "corpus/1968/figures.csv",
                                                "corpus/1968/pages/", "data/experiments/<id>/observations.csv"], extra_yaml=yaml, reader=True)


def page_simulate(d):
    r = next(x for x in d["experiments"] if x["experiment_id"] == PILOT_RECORD)
    m = d["mat_by_no"].get(r["soil_no"])
    card = card_lpt(d, r)
    obs = d["observations"].get(PILOT_RECORD)
    dia, dia_in = inches_mm(r["penetrator_printed"])
    v = rate_mm_s(r)
    kg = to_si(float(r["unit_weight_printed_pcf"]), "pcf", "kg_m3")
    gamma = to_si(float(r["unit_weight_printed_pcf"]), "pcf", "N_m3")
    label = re.sub(r"^LPT No\. ?", "", r["test_label_printed"])
    rec = f"../experiments/{PILOT_RECORD}.qmd"
    figs = [t for t in fig_ids(r) if t in d["fig_by_id"]]
    b = ["How to set up a virtual experiment of a test in this collection and compare it with the measurement, worked "
         f"through on one test. The steps do not depend on the simulator, and no simulation result is shown. The example is "
         f"load-penetration test [{term('LPT')} {label}]({rec}), chosen because its record gives the density of the bed, the "
         "tool, the bin and the loading rate.", ""]
    b.append("## 1. Choose a test")
    b.append("")
    b.append(f"[Find a test](../experiments/index.qmd) lists every test. In a load-penetration test a tool is pushed into a "
             f"prepared bed of soil and the load on it is recorded against depth. In {term('LPT')} {label}, a cylinder "
             f"{dia:.1f} mm ({dia_in}) in diameter was pushed at {v:.3f} mm/s into dense {define(r['soil_family'])} with a bulk density "
             f"of {kg:.0f} kg/m³.")
    b.append("")
    b.append("## 2. Read its virtual experiment card")
    b.append("")
    b.append("The card on the test's page lists what the report gives about the soil, the bed, the tool, the motion and the "
             f"measurement, and what it leaves out. Each value is marked {KIND_TAG['test']}, {KIND_TAG['ref']} or "
             f"{KIND_TAG['choice']}, and each citation opens the page of the report it comes from.")
    b.append("")
    b.append("## 3. Gather the soil properties")
    b.append("")
    if m:
        b.append(f"The [Soils](../materials/index.qmd) page gives the report's soil table. The row that matches this test is soil "
                 f"No. {m['soil_no']}, *{m['bendix_designation']}*: {define('D50')} {m['mean_grain_size_mm']} mm, friction angle "
                 f"{m['friction_angle_deg']} degrees and modulus {float(m['elastic_modulus_Pa']) / 1e6:.1f} MPa. These values belong "
                 f"to the soil's nominal state, {define('Dr')} {m['relative_density']} and {m['bulk_density_kg_m3']} kg/m³; the bed of "
                 f"this test is denser, {kg:.0f} kg/m³. Two cautions follow. Properties that depend on density are read at the bed's "
                 f"own state where the report allows it: it plots friction angle against relative density ({fig_cite(d, 'F2-23')}). "
                 "And the modulus was measured with sound waves; the report warns that static and wave-based moduli can differ by "
                 "an order of magnitude (AM-68-1 Vol. II, Appendix B, printed 1, PDF 104), so it is a reference, not a static "
                 "stiffness.")
    b.append("")
    b.append("## 4. Build the geometry")
    b.append("")
    b.append(f"From the card: the bin is 0.457 m wide, 0.914 m long and 0.914 m deep, of plywood with a glass front; the "
             f"cylinder is {dia:.1f} mm in diameter, its axis 229 mm from the nearest wall, and starts at the soil surface; "
             "gravity is 9.81456 m/s², the report's value for Earth, 32.2 ft/s², converted exactly (glossary, printed 2-2, PDF 27). The bin is part of the test. The report found that tests of the same soil in larger bins "
             "tended to reach higher peak loads (AM-68-1 Vol. I, printed 2-74, PDF 99), and that in one test in dense sand a "
             "failure plane reached the glass front of this bin (printed 2-59, PDF 84). A model that makes the bin smaller to "
             "save computing time has to show that this does not change the load.")
    b.append("")
    b.append("## 5. Choose the missing inputs and bracket them")
    b.append("")
    b.append("Every input marked as left to the user needs a value. For each one, choose a plausible low and a plausible high "
             "value, run the virtual experiment at both, and report the spread of the result next to the result itself. For "
             "this test the card lists:")
    b.append("")
    b += [f"{k + 1}. {text[0].upper() + text[1:]}." for k, (_, text, _) in enumerate(card["choices"])]
    b.append("")
    rec_dr, dr = density_chart_dr(d, r["soil_family"], gamma)
    avg_fig = next((f for f in figs if re.search(r"Dr approx (\d\.\d+)", d["fig_by_id"][f]["states"])), None)
    if dr.get("mean") is not None and avg_fig:
        avg = re.search(r"Dr approx (\d\.\d+)", d["fig_by_id"][avg_fig]["states"]).group(1)
        lim = sorted(x for k, x in dr.items() if k != "mean" and x is not None)
        chart = d["observations"][rec_dr]["meta"]["figure_id"]
        b.append(f"A worked example: the relative density of this bed. The report's average for the tests of "
                 f"{fig_label(avg_fig)} is about {avg} (AM-68-1 Vol. I, printed 2-74, PDF 99). Reading this bed's density, "
                 f"{gamma / 1000:.2f} kN/m³ ({r['unit_weight_printed_pcf']} pcf), on the report's density chart for the soil "
                 f"({fig_cite(d, chart)}) gives about {dr['mean']:.2f} on the mean curve"
                 + (f", and {lim[0]:.2f} to {'above 1' if len(lim) < 2 else f'{lim[1]:.2f}'} within its 95 percent confidence "
                    "limits" if lim else "")
                 + f". The two sources do not agree exactly, so a bracket of {min(lim[0], dr['mean']):.2f} to {float(avg):.2f}, with "
                 f"{dr['mean']:.2f} as a baseline, is one defensible choice; the soil strength at each end is then read at that "
                 "relative density.")
        b.append("")
    b.append("## 6. Decide the output and the loading speed")
    b.append("")
    if obs:
        pts = sorted(obs["rows"], key=lambda x: float(x["x_si"]))
        lo, hi = float(pts[0]["x_si"]) * 1000, float(pts[-1]["x_si"]) * 1000
        b.append(f"Record the quantity that was measured: the axial force the soil exerts on the cylinder (what the load cell "
                 f"read) against the cylinder's penetration below the original soil surface. The printed curve covers {lo:.1f} "
                 f"to {hi:.1f} mm; the test itself went further, but the figure does not show how far. State where the zero of "
                 "force and of penetration are, and whether the cylinder's weight is included. "
                 f"The test ran at {v:.3f} mm/s. A faster virtual push saves computing time, but it has to be shown not to change "
                 "the load, for example by running two speeds and comparing.")
    b.append("")
    b.append("## 7. Compare with the measurement")
    b.append("")
    if obs:
        peak = next((x for x in obs["rows"] if x["point_kind"] == "feature" and x["note"].startswith("peak")), None)
        b.append(f"Download the measured points from the [test's page]({rec}): penetration and load in SI, each with its reading "
                 "bound, the precision with which the printed figure could be read.")
        if peak:
            b.append("")
            b.append(f"A worked example. The first peak of the measured curve is the point at {float(peak['x_si']) * 1000:.1f} mm and "
                     f"{float(peak['y_si']):,.0f} N, read to within {float(peak['x_bound_si']) * 1000:.2f} mm and "
                     f"{float(peak['y_bound_si']):.0f} N. A simulated curve is compared with it at the same penetration, by "
                     "interpolating the simulated force there. A difference smaller than the reading bound cannot be told apart "
                     "from a reading error; a larger one still has to be weighed against how much tests on similar beds "
                     "differ, which the reading bound does not include.")
        b.append("")
        b.append("The report gives no repeat of this test. The other tests printed in the same figure ran on other beds, at "
                 "other rates or densities, so the spread between them mixes those differences with the test-to-test scatter "
                 "and gives only a rough idea of it.")
    b.append("")
    b.append("## 8. Keep related records together")
    b.append("")
    b.append(f"When some tests are used to tune a model and others to check it, three kinds of relation keep records on the same "
             f"side: two printings of one test ({term('LPT')} {label} is printed in {' and '.join(fig_label(f) for f in figs)}: one "
             "test, not two); a result derived from tests, such as a failure envelope drawn from several shear tests; and tests "
             "run on one shared bed, where the report says so. Tests that only share a figure, a soil or a bin size are "
             "neighbors for comparison, not dependencies. Each test's page lists both.")
    b.append("")
    b.append("## 9. Share it")
    b.append("")
    b.append("A script that runs a virtual experiment of a test hosted here is welcome; the [Contribute](../contribute/index.qmd) "
             "page says what it should state.")
    return page("Simulate a test", "\n".join(b), ["data/experiments/index.csv", "data/materials/materials.csv", "corpus/1968/figures.csv",
                                                  f"data/experiments/{PILOT_RECORD}/observations.csv",
                                                  f"data/experiments/{DENSITY_CHART['RS']}/observations.csv"], reader=True)


def page_decisions(d):
    # the public release's log has no who and note columns (the curated log of D-052, written by make_public_release.py)
    cols = [c for c in ("id", "date", "question", "options", "decision", "who", "note") if c in (d["decisions"][0] if d["decisions"] else {})]
    rows = [[(r[c] if r[c].strip() else "*open*") if c == "decision" else r[c] for c in cols] for r in d["decisions"]]
    intro = ("Decisions taken on this project, oldest first. Answer or reopen one by its id." if "note" in cols else
             "The decisions that shaped the method, oldest first, under the numbers the data and the documents cite. "
             "Decisions about the people and the logistics of the review are summarized.")
    body = intro + "\n\n" + table(cols, rows)
    return page("Decisions", body, ["docs/decisions.csv"])


def page_experiments_index(d):
    by_kind = Counter(r["kind"] for r in d["experiments"])
    b = ["One row per indexed record; click the test name for the record's page. `kind` says what a row is: a single "
         "physical test, a series averaged from unidentified tests, a series derived from identified tests, an "
         "author's correlation, a text-only summary, or a bin sample. Rows are not independent tests unless "
         "`kind` is `single`. Sort by any column; the filter box matches any field, including printed labels "
         "such as `LPT 27` or `SSD 4-18`.", "",
         table(["kind", "rows"], [[k, str(v)] for k, v in sorted(by_kind.items())], num_cols=["rows"]), "",
         "::: {#experiments-listing}", ":::"]
    yaml = {"listing": {"id": "experiments-listing", "contents": ["b68-*.qmd"], "type": "table",
                        "sort": "title", "sort-ui": True, "filter-ui": True, "page-size": 60,
                        "fields": ["title", "kind", "test-type", "family", "state", "printed-label", "evidence", "setup", "record-status", "priority"],
                        "field-display-names": {"title": "id", "test-type": "type", "printed-label": "printed label",
                                                "setup": "setup", "record-status": "status", "priority": "pri"}}}
    text = page("Experiments", "\n".join(b), ["data/experiments/index.csv", "data/experiments/index.json"], extra_yaml=None)
    # listing YAML needs nesting beyond the simple front-matter helper; write it directly
    listing = (
        "listing:\n  id: experiments-listing\n  contents:\n    - \"b68-*.qmd\"\n  type: table\n  sort: record\n"
        "  sort-ui: true\n  filter-ui: true\n  page-size: 60\n  fields: [record, title, kind, test-type, family, state, printed-label, setup, record-status, priority]\n"
        "  field-display-names:\n    record: id\n    title: test\n    test-type: type\n    printed-label: printed label\n    record-status: status\n    priority: pri\n")
    return text.replace('title: "Experiments"\n---', 'title: "Experiments"\n' + listing + '---', 1)


# ----------------------------------------------------------------------------- record pages
# The record page is written for a user of the data (what was tested, the numbers, how to reproduce
# the test, where it is printed). Everything written for the maintainers (reconciliation record,
# status counts, calibration residuals, the two agents' notes) is on the record's provenance page
# under review/. Decided with Dan 2026-10-08 (D-019): keep separate things separate.

DYNAMIC = ("imp", "mdrop")   # test types with an impact or touchdown velocity and a moving mass (D-050)
TYPE_NAME = {"ds": "Direct shear", "lpt": "Load penetration", "dpt": "Dynamic penetration (DPT)", "dens": "Density measurement",
             "gs": "Grain size analysis", "gs;dens": "Grain size and density", "sonic": "Sonic modulus", "tx": "Triaxial compression",
             "imp": "Footpad impact", "mdrop": "LM model drop (1/6 scale)", "drag": "Footpad drag"}


def mm_text(s):
    """Lengths under one meter written in millimeters (0.0635 m becomes 63.5 mm)."""
    return re.sub(r"(?<![\d.])0\.(\d+)\s*m(?![a-z])", lambda m: f"{float('0.' + m.group(1)) * 1000:g} mm", s or "")


def psf_of(text):
    m = re.search(r"(\d+(?:\.\d+)?)\s*psf", text or "")
    return float(m.group(1)) if m else None


def finite_or_none(s):
    """A number from a data cell, or None when the cell is blank or not finite (a page then says 'not available')."""
    try:
        v = float(s)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def median_or_none(cells):
    vals = [v for v in map(finite_or_none, cells) if v is not None]
    return statistics.median(vals) if vals else None


SI_WORDS = {"m_s2": "m/s^2", "N_m3": "N/m^3", "kg_m3": "kg/m^3", "m_s": "m/s"}   # the SI unit codes of data/ in prose


def agree(n, singular, plural):
    """The verb (or noun) that agrees with a count: '1 is', '2 are' (2026-11-21, Dan: '1 are still under review')."""
    return singular if n == 1 else plural


def si_quantity(v, unit, quantity="", bound=False):
    """A value in SI base units written with a sensible prefix, for prose. A dimensionless value (unit code `none`,
    the SI unit one) is the bare number, or a percent when the quantity is one (percent finer is stored as a fraction):
    until 2026-11-20 the code itself was printed, as in '1.012 none relative density'. A bound on a percent is in
    percentage points, an absolute difference, not a percent of the value (Codex's review, 2026-11-20)."""
    if v is None or not math.isfinite(v):   # never 'nan percent' on a page
        return "not available"
    if unit == "none":
        if "percent" in quantity.lower():
            return f"{v * 100:.3g} percentage points" if bound else f"{v * 100:.3g} percent"
        return f"{v:.4g}"
    if unit == "m":
        return f"{v * 1e6:.0f} micrometers" if abs(v) < 1e-3 else f"{v * 1e3:.2f} mm"
    if unit == "Pa":   # MPa from 1 MPa up, as the plots draw a modulus (until 2026-11-21: '90279.2 kPa')
        if abs(v) >= 1e6:
            return f"{v / 1e6:.2f} MPa"
        return f"{v / 1e3:.1f} kPa" if abs(v) >= 1e3 else f"{v:.0f} Pa"
    if unit == "s" and abs(v) < 1:   # the time histories: milliseconds read better than 0.01318 s
        return f"{v * 1e3:.3g} ms"
    return f"{v:.4g} " + SI_WORDS.get(unit, unit)


def unit_phrase(unit, quantity):
    """How the download text names a column's SI unit: a dimensionless column has none to name, and a percent is
    stored as a fraction (until 2026-11-20 the text read 'relative density in none')."""
    if unit == "none":
        return " (a fraction of 1)" if "percent" in quantity.lower() else " (dimensionless)"
    return f" in {SI_WORDS.get(unit, unit)}"


def record_title(d, r):
    fam, state = state_of_row(d, r)
    tt, label = r["test_type"], r["test_label_printed"]
    soil = f"{r['soil_family']} soil" if r["soil_family"] else "unnamed soil"
    if tt == "ds":
        psf = psf_of(r["loading"]) or psf_of(label)
        if psf:
            return f"Direct shear of {soil} at {psf * 47.880258980336 / 1000:.1f} kPa normal stress"
        return f"Direct shear of {soil}" + (f", {label}" if label else "")
    name = TYPE_NAME.get(tt, tt)
    if r["kind"] == "run-table" and label.isupper():   # a table caption printed in capitals (Table 5-T3): the figures
        # index's title of the table, whose case keeps acronyms (Codex's review: .capitalize() would write 'Lm')
        fig = d["runs"].get(r["experiment_id"], {}).get("meta", {}).get("figure_id", "")
        label = d["fig_by_id"].get(fig, {}).get("title_as_printed") or label
    bits = [soil]
    # the state, unless the printed label already names it ('RS soil, loose, Loose, Dr = 0.30' until 2026-11-21)
    if state and not state.startswith("state not") and state != "conflicting evidence" and \
            state.split(" (")[0].lower() not in (label or "").lower():
        bits.append(state.split(" (")[0])
    if label and label.lower() not in (name.lower(),):
        bits.append(label)
    return f"{name}: " + ", ".join(bits)


def fig_ids(r):
    return tuple(t.strip() for t in r["evidence"].split(";") if t.strip() and t.strip()[0] in "FT")


def family_of(d, r):
    """Single tests of the same type drawn from the same figures (the record's family)."""
    me = fig_ids(r)
    if not me or r["kind"] != "single":
        return [r]
    return [s for s in d["experiments"] if s["kind"] == "single" and s["test_type"] == r["test_type"] and fig_ids(s) == me]


def table_runs_of(d, r):
    """The rows of a printed table of drops (Table 5-T3) that concern a record, as [(run-table record id, run row)]: a
    run-table record's own runs, or the run whose `same_test_as` names a single record (tools/build_run_table.py)."""
    i = r["experiment_id"]
    if i in d["runs"]:
        return [(i, x) for x in d["runs"][i]["rows"]]
    return [(k, x) for k, v in sorted(d["runs"].items()) for x in v["rows"] if x.get("same_test_as") == i]


def num_text(s, spec, printed=None, unit=""):
    """A number of a run table formatted by `spec` (with its unit), or, when the cell is not a number, the site's word
    for it: *unreadable* where the printed value holds a `?` the readings could not read, *not yet extracted* where
    the readings agreed on no value; never a blank, and a pending cell never stops the build (Codex's review,
    2026-11-20)."""
    try:
        return format(float(s), spec) + (f" {unit}" if unit else "")
    except (TypeError, ValueError):
        return MISSING["unr"] if "?" in (s or "") + (printed or "") else MISSING["nye"]


def mdrop_phi(add, t53, r, aside):
    """The friction angle Table 5-T3 prints for a drop's bed: the value of a single drop, or the range over a table's drops
    (each drop's own value is in the record's data block)."""
    where = "Table 5-T3, printed 5-45, PDF 325"
    table_rec = r["kind"] == "run-table"
    q = ("friction angle of each bed" if table_rec
         else "friction angle printed for this bed" + (f" ({aside})" if aside else ""))
    vals = sorted({float(x["phi_deg"]) for _, x in t53 if re.fullmatch(r"\d+(?:\.\d+)?", x.get("phi_deg") or "")})
    if not vals:
        add("soil strength", q, "", "", where, "not yet extracted")
    elif table_rec:
        add("soil strength", q, (f"{vals[0]:g} degrees" if len(vals) == 1 else f"{vals[0]:g} to {vals[-1]:g} degrees")
            + " (each drop's value is in the table above)", "", where)
    else:
        k, x = t53[0]
        add("soil strength", q, f"{x['phi_deg']} degrees", f"{x['phi_deg']} Deg.",
            f"{where} (NASA Test No. {x['run_number']} of [{k}]({k}.qmd))")


def setup_rows(d, r):
    """The reproduce-this-test block: rows (group, quantity, value, as printed, where) and the list
    of quantities a simulator needs that the source does not give."""
    m = d["mat_by_no"].get(r["soil_no"])
    ev_fig = list(fig_ids(r))
    fig_cite = ", ".join(ev_fig) if ev_fig else "text"
    rows, gaps = [], []
    def add(group, q, value, printed, where, status="reported", essential=False):
        shown = value if value else MISSING["nye" if status == "not yet extracted" else "nr"]
        if not value and status in ("not reported", "unknown") and essential:
            gaps.append(q)
        rows.append([group, q, shown, printed or "", where])
    # material
    if m:
        add("material", "soil", f"{m['bendix_designation']}, {m['description_verbatim']} (soil No. {m['soil_no']} of Table 2-3)", r["soil_family"], "Vol. I Table 2-3, printed 2-16, PDF 41")
        add("material", "mean grain size D50", f"{m['mean_grain_size_mm']} mm", f"{m['mean_grain_size_mm']} mm", "Table 2-3")
        add("material", "uniformity coefficient Cu", m["uniformity_coeff"], m["uniformity_coeff"], "Table 2-3")
        add("material", "D95", f"{m['d95_mm']} mm", f"{m['d95_mm']} mm", "Table 2-3")
        add("material", "fines (passing No. 200 sieve)", m["percent_passing_200"].replace("<", "under ").replace("%", " percent"), m["percent_passing_200"], "Table 2-3")
        add("material", "grain size curve", "", "", "Vol. II Appendix A (one curve per soil); Vol. I Fig. 2-14 (family averages)", "not yet extracted")
    else:
        add("material", "soil family", r["soil_family"], r["soil_family"], fig_cite, "reported" if r["soil_family"] else "unknown", essential=True)
        add("material", "gradation", "", "", "F2-14 average curve for the family; individual analyses in Vol. II Appendix A", "not yet extracted" if r["soil_family"] else "unknown")
    # state
    add("state", "relative density Dr", r["dr_printed"], r["dr_printed"], fig_cite, "reported" if r["dr_printed"] else "unknown", essential=True)
    uw = r["unit_weight_printed_pcf"]
    if uw:
        add("state", "unit weight", conv_text(uw, "pcf", "N_m3", 0, "N/m^3") + f" (bulk density {conv_text(uw, 'pcf', 'kg_m3', 1, 'kg/m^3')})", f"{uw} pcf", fig_cite)
    elif m:
        add("state", "unit weight of the nominal soil state", f"{m['unit_weight_N_m3']} N/m^3 ({m['bulk_density_kg_m3']} kg/m^3 at Dr {m['relative_density']})", "", "Table 2-3; the bed's own Dr may differ")
    else:
        add("state", "unit weight", "", "", fig_cite, "unknown", essential=True)
    add("state", "minimum and maximum density of the batch", "", "", "Fig. 2-17; Vol. II Appendix A; degraded values for used soil in Figs. 2-56 to 2-58", "not yet extracted")
    if r["test_type"] in ("lpt", "dpt"):
        add("state", "DPT index Gp", (r["gp_printed_g"] + " g") if r["gp_printed_g"] else "", (r["gp_printed_g"] + " g") if r["gp_printed_g"] else "", fig_cite + "; density read through the Fig. 2-55 correlation", "reported" if r["gp_printed_g"] else "not reported")
    add("state", "moisture", "air dried, 0.2 to 0.3 percent by weight (occasionally 0.6)", "0.2 to 0.3%", "text 2-103, PDF 128 (applies to all soils)")
    # apparatus and loading, per test type
    tt = r["test_type"]
    obs = d["observations"].get(r["experiment_id"])
    dig_fig = (obs["meta"].get("figure_id") if obs else "") or fig_cite
    if tt == "ds":
        dia = inch_text(r["apparatus"]) if re.search(r"\d", r["apparatus"] or "") else r["apparatus"]
        dia = mm_text(dia)
        add("apparatus", "shear box", dia, r["apparatus"], "text 2-40, PDF 65; Fig. 2-20", "reported" if r["apparatus"] else "unknown", essential=True)
        add("apparatus", "specimen height", "", "", "", "not reported", essential=True)
        psf = psf_of(r["loading"])
        add("loading", "normal stress, held constant", f"{psf * 47.880258980336 / 1000:.2f} kPa" if psf else "", f"{psf:.0f} psf" if psf else "", dig_fig + " legend", "reported" if psf else "unknown", essential=True)
    else:
        add("geometry", "tool", mm_text(inch_text(r["penetrator_printed"])), r["penetrator_printed"], fig_cite, "reported" if r["penetrator_printed"] else "unknown", essential=True)
        bin_ = r["bin_printed_in"]
        # the standard LPT container (text 2-56: 18 in wide, 36 in long, 36 in deep, a glass front 18 in deep), only where
        # the test used it, or as the report's standard where an LPT test's bin is not stated; never for the larger
        # bins (54 by 36, 108 by 36 in), a 2 ft box, a mold or the calibration bins (Codex's review, 2026-11-19)
        std = "the standard LPT container is 18 by 36 in (0.457 by 0.914 m) and 36 in (0.914 m) deep (text 2-56, PDF 81)"
        b_norm = re.sub(r"\s+", " ", (bin_ or "").strip().lower())
        lpt_bin = ("; " + std if b_norm in ("18 by 36", "36 by 18", "lpt bin") else
                   "; " + std.replace("the standard", "the report's standard") + "; this test's bin is not stated"
                   if tt == "lpt" and not b_norm else "")
        add("geometry", "bin or mold", mm_text(inch_text(bin_)) if re.search(r"\d", bin_ or "") else bin_, bin_, fig_cite + lpt_bin, "reported" if bin_ else "unknown", essential=True)
        # a fill depth printed for some beds of the record ('RS intermediate beds 18 in thick', Table 5-T3's drops): that
        # value, and the other beds named as the gap (Codex's review, 2026-11-20); otherwise not reported
        fd = re.search(r"([A-Za-z][A-Za-z ]*?) beds (\d+(?:\.\d+)?) in thick(?: \(([^)]*)\))?", bin_ or "")
        if fd:
            rest = re.search(r"depth of the ([A-Za-z ]+?) beds not printed", bin_ or "")
            add("geometry", "fill depth", f"{float(fd.group(2)) * 25.4:g} mm for the {fd.group(1)} beds"
                + (f"; not reported for the {rest.group(1)} beds" if rest else ""), f"{fd.group(2)} in", fd.group(3) or fig_cite)
            if rest:
                gaps.append(f"fill depth of the {rest.group(1)} beds")
        else:
            add("geometry", "fill depth", "", "", "", "not reported", essential=True)
        add("loading", "control", r["loading"], "", fig_cite, "reported" if r["loading"] else "unknown", essential=True)
        if tt in DYNAMIC:   # the moving mass of an impact or a drop, printed as a weight in pounds
            mw = re.search(r"(?:M1|Weight)\s*=?\s*(\d+(?:\.\d+)?)\s*lbs?\b", r["loading"] or "", re.I)
            add("loading", "moving mass" if tt == "imp" else "model mass",
                f"{float(mw.group(1)) * 0.45359237:.4g} kg" if mw else "", f"{mw.group(1)} lb" if mw else "", fig_cite,
                "reported" if mw else "not reported", essential=True)
        sd = r["start_depth_printed_in"]
        if tt not in DYNAMIC and tt != "drag":   # a drag run is held at its depth d (in the runs table)
            add("loading", "start depth below surface", ("0 m (started at the surface)" if sd == "0" else fmt(float(sd) * 0.0254, 4) + " m") if sd else "", (sd + " in") if sd else "", fig_cite, "reported" if sd else "unknown")
    rate = r["rate_printed"]
    if tt in DYNAMIC or tt == "drag":   # impact, touchdown and drag velocities, printed in ft/s ("fps") or in./sec.
        f = {"fps": 0.3048, "in./sec.": 0.0254, "in/s": 0.0254}
        # a range ('V_H 2.76 to 15.05 fps', the drag tables) has both ends converted, then a single value
        rate_si = re.sub(r"(-?\d+(?:\.\d+)?)(\s+to\s+)(-?\d+(?:\.\d+)?)\s*(fps|in\./sec\.|in/s)",
                         lambda m: f"{float(m.group(1)) * f[m.group(4)]:.4g}{m.group(2)}{float(m.group(3)) * f[m.group(4)]:.4g} m/s", rate or "")
        rate_si = re.sub(r"(-?\d+(?:\.\d+)?)\s*(fps|in\./sec\.|in/s)",
                         lambda m: f"{float(m.group(1)) * f[m.group(2)]:.4g} m/s", rate_si)
    elif re.search(r"\d", rate or "") and "in/min" in rate:
        rate_si = " ".join(fmt(to_si(float(x), "in_min", "m_s") * 1000.0, 3) if re.fullmatch(r"\d+\.?\d*", x) else x
                           for x in rate.replace(" in/min", "").split()) + " mm/s"
    else:
        rate_si = rate
    add("loading", "displacement rate" if tt == "ds" else "rate", rate_si, rate, "text 2-40, PDF 65" if tt == "ds" else fig_cite, "reported" if rate else "unknown", essential=True)
    t53 = table_runs_of(d, r) if tt == "mdrop" else []
    if tt == "mdrop" and r["kind"] != "run-table":   # the row above is the strut-load figure's inset; the table prints the
        # same velocities to one decimal less, and for NASA Test No. 2 a different Vh (Codex's review, 2026-11-19). A
        # run-table record shows each drop's velocities in its data block, and their range in the row above.
        q = ("touchdown velocities and time from release to touchdown, printed in the table of the detail correlation drops "
             "(the line above is the strut-load figure's inset)")
        if t53:
            k, x = t53[0]
            add("loading", q, f"{term('V_v')} {num_text(x['VV_m_s'], '.4g', x['VV_in_s'], 'm/s')}, "
                f"{term('V_h')} {num_text(x['Vh_m_s'], '.4g', x['Vh_in_s'], 'm/s')}; {term('tau')} {num_text(x['tau_s'], 'g', unit='s')}",
                f"V_v {x['VV_in_s']} In./Sec., V_h {x['Vh_in_s']} In./Sec., tau {x['tau_s']} Sec.",
                f"Table 5-T3, printed 5-45, PDF 325 (NASA Test No. {x['run_number']} of [{k}]({k}.qmd))")
        else:
            add("loading", q, "", "", "Table 5-T3, printed 5-45, PDF 325", "not yet extracted")
    add("loading", "gravity", "9.81456 m/s^2, the report's value for Earth, 32.2 ft/s^2, converted exactly; the tests ran "
        "in a laboratory on Earth",
        "earth = 32.2 fps²", "AM-68-1 Vol. I, glossary, printed 2-2, PDF 27")
    # measured
    add("measured", "channels", r["measured_channels"], "", fig_cite, "reported" if r["measured_channels"] else "unknown", essential=True)
    if tt == "ds":
        p2 = in_order([x for x in obs["rows"] if x["panel"] == "2"]) if obs else []
        if p2:
            y0, b0 = float(p2[0]["y_si"]), float(p2[0]["y_bound_si"])
            if abs(y0) > b0:
                add("measured", "dilation zero", f"*not stated.* Our observation from the digitized points: the first dilation reading of this test is "
                    f"{si_quantity(y0, 'm')} ({'above' if y0 > 0 else 'below'} zero by more than its reading bound), so the gauge zero may have been set before the normal load was applied",
                    "", dig_fig + ", lower panel")
            else:
                add("measured", "dilation zero", "*not stated*; the first dilation reading of this test is at zero within its reading bound", "", dig_fig + ", lower panel")
        else:
            add("measured", "dilation zero", "", "", dig_fig + ", lower panel", "not reported")
    # strength of the soil, for context
    if m:
        add("soil strength", "friction angle at this density (report's direct shear average)", f"{m['friction_angle_deg']} degrees", f"{m['friction_angle_deg']} deg", "Table 2-3; Fig. 2-23 gives phi against Dr")
        if tt == "mdrop":   # the detail correlation drops print their bed's own angle (Codex's review, 2026-11-19)
            mdrop_phi(add, t53, r, "the line above is the soil's average at this density")
        add("soil strength", "sonic modulus E at 4 psi confinement", f"{float(m['elastic_modulus_Pa']) / 1e6:.1f} MPa", "", "Table 2-3 (measurements in Vol. II Appendix B)")
    elif tt == "mdrop":   # a table of drops on beds of several states: the angles its rows print
        mdrop_phi(add, t53, r, "")
    else:
        add("soil strength", "friction angle", "", "", "Fig. 2-23 for the family against Dr", "not yet extracted")
    add("soil strength", "apparent cohesion", "*not reported*: the report declines to use direct-shear apparent cohesion as a descriptor; about 0.1 psi explains the LPT size effects", "", "text 2-47, PDF 72")
    return rows, gaps


def in_order(rows):
    """A panel's points in the order of the measurement: the drawn line's samples in drawing order (the file's order;
    `sequence` is each reading's own numbering), or, for a panel of plotted symbols only, by x, since the other
    reading's extra symbols are appended at the end of the file (Codex's review, 2026-11-19: a dilation "at the end"
    read from an appended symbol near zero shear)."""
    tr = [x for x in rows if x["point_kind"] in ("trace", "gridline")]
    return tr if tr else sorted([x for x in rows if x["point_kind"] == "marker"], key=lambda x: float(x["x_si"]))


def note_fragments(notes):
    """The fragments of several panel notes in panel order, each given once. A panel note may hold several sentences,
    one per line (`qa/<batch>/panel-map.csv`, from curves-s5-b1), so that panels sharing a sentence (the strut panels'
    sign convention, a time axis extrapolated past its last line) state it once; a note without line breaks is one
    fragment. No sentence is ever split by guessing (Codex's reviews, 2026-11-19: an abbreviation such as "Mt." or an
    initial would cut a sentence in two and lose a piece)."""
    return list(dict.fromkeys(f.strip() for n in notes for f in n.splitlines() if f.strip()))


def end_of(rows, series_id):
    """A series' end: its `last` feature (where the reader marked the drawn line's ink ending) when it lies at or beyond
    the last trace sample, else None (the caller takes the last sample in drawing order). On LPT 87 the end is a peak
    feature beyond the last trace sample, and the page had called an earlier sample the end (Codex's review)."""
    ser = [x for x in rows if x["series_id"] == series_id]
    tr = [x for x in ser if x["point_kind"] in ("trace", "gridline")]
    lasts = [x for x in ser if x["point_kind"] == "feature" and (x.get("note") or "").lower().lstrip().startswith("last")]
    if not lasts:
        # no `last` feature: a feature beyond the trace's last sample (LPT 87's end is its peak) is the drawn end
        beyond = [x for x in ser if x["point_kind"] == "feature" and tr and float(x["x_si"]) > float(tr[-1]["x_si"])]
        return max(beyond, key=lambda x: float(x["x_si"])) if beyond else None
    lf = max(lasts, key=lambda x: float(x["x_si"]))
    return lf if not tr or float(lf["x_si"]) >= float(tr[-1]["x_si"]) else None


def run_table_section(d, r):
    """The data block of a run-table record: downloads, the check, and the runs in SI (D-050, roadmap 6b)."""
    i = r["experiment_id"]
    if i not in d["runs"]:
        return []
    rows, meta = d["runs"][i]["rows"], d["runs"][i]["meta"]
    b = ["## Data", ""]
    if r["test_type"] == "mdrop":   # Table 5-T3, the detail correlation drops (tools/build_run_table.py --family mdrop)
        b.append(f"Download: [runs.csv](../files/data/experiments/{i}/runs.csv) ({len(rows)} drops, one physical drop per row: "
                 "every printed value in SI and as printed, and the record of the drop's time histories where this collection "
                 f"holds one) and [runs.json](../files/data/experiments/{i}/runs.json) (units, conversion factors, how the table "
                 "was read).")
        b.append("")
        if meta.get("definitions"):
            b.append(meta["definitions"])
            b.append("")
        ar = meta.get("arithmetic", {})   # tools/check_mdrop_table.py: |V_v| against g tau, over the whole printed table
        if ar.get("vertical"):
            fit_vh = [x["run"] for x in ar.get("drops_detail", [])[ar["vertical"]:] if x["fits"]]   # vertical drops listed first
            done, total = ar["vertical"] + ar.get("with_vh", 0), ar.get("drops", 0)   # drops with an unreadable cell skipped
            scope = (f"over all {total} drops of the table" if done == total else
                     f"over the {done} drops of the table's {total} whose cells are all readable "
                     f"({total - done} left out)")
            st = ar.get("standard") or {}
            fit_vh_std = [x["run"] for x in st.get("drops_detail", [])[st.get("vertical", 0):] if x["fits"]]
            b.append(f"Our arithmetic, not the report's, {scope}, against |V_v| = g tau (the speed of a free fall from rest "
                     "over tau) within the rounding of both printed numbers. With the report's g for Earth, 32.2 ft/s² "
                     "(9.81456 m/s²; glossary, printed 2-2, PDF 27), "
                     f"{ar['vertical_fit']} of the {ar['vertical']} vertical drops (V_h 0) and {ar['with_vh_fit']} of the "
                     f"{ar['with_vh']} drops with a horizontal velocity"
                     + (f" (NASA Test No. {', '.join(fit_vh)})" if fit_vh else "") + " are consistent with it"
                     + (f"; with standard gravity, 9.80665 m/s², {st['vertical_fit']} of {st['vertical']} and "
                        f"{st['with_vh_fit']} of {st['with_vh']}"
                        + (f" (NASA Test No. {', '.join(fit_vh_std)})" if fit_vh_std else "")
                        + ". The two values of g differ by 0.08 percent, about the rounding of a printed tau, so at this "
                        "precision the verdicts depend on the g used" if st else "")
                     + ". This shows consistency, not the method, which the report does not state.")
            b.append("")
        known = {s["experiment_id"] for s in d["experiments"]}
        linked = [x for x in rows if x.get("same_test_as") in known]
        if linked:   # the drops whose time histories are records of their own (the table stays narrow enough to read)
            b.append("Time histories: " + "; ".join(f"NASA Test No. {x['run_number']} in [{x['same_test_as']}]({x['same_test_as']}.qmd)"
                                                    for x in linked)
                     + (f"; for the other drops they are {meta['no_histories']}." if meta.get("no_histories") and len(linked) < len(rows) else "."))
        elif meta.get("no_histories"):
            b.append(f"Time histories of these drops: {meta['no_histories']}.")
        b.append("")
        printed_of = {"VV_m_s": "VV_in_s", "Vh_m_s": "Vh_in_s", "bulk_density_kg_m3": "gamma_pcf"}   # the column it came from
        num = lambda x, k: num_text(x.get(k), ".4g", x.get(printed_of.get(k, k)))
        asis = lambda x, k: num_text(x.get(k), "g")   # a number kept as printed ('.298'), shown as 0.298
        # seven columns, as many as the text column shows without scrolling sideways (the drag table's count)
        tbl = [[f"{x['run_number']} ({x['bendix_drop_no']})", f"{x['soil_printed']} ({asis(x, 'Dr')})", num(x, "VV_m_s"),
                num(x, "Vh_m_s"), asis(x, "tau_s"), num(x, "bulk_density_kg_m3"), x["phi_deg"]] for x in rows]
        b.append(table(["NASA test (Bendix drop)", f"bed as printed ({term('Dr')})", f"{term('V_v')} (m/s)", f"{term('V_h')} (m/s)",
                        f"{term('tau')} (s)", "bulk density (kg/m^3)", f"{term('phi')} (deg)"], tbl))
        b.append("")
        return b
    b.append(f"Download: [runs.csv](../files/data/experiments/{i}/runs.csv) ({len(rows)} runs, one physical test per row: every "
             "printed value in SI and as printed, the four derived columns the report prints, and the arithmetic check of each "
             f"row) and [runs.json](../files/data/experiments/{i}/runs.json) (units, conversion factors, how the table was read).")
    b.append("")
    f = meta.get("arithmetic", {}).get("factor") or {}
    if f.get("common"):
        arith = (f"Checked against each other, the two pressure columns agree only with a common factor of {f['low']:.4f} to "
                 f"{f['high']:.4f}, which every run fits: the factor a unit weight of {f['effective_gamma_pcf'][0]:.2f} to "
                 f"{f['effective_gamma_pcf'][1]:.2f} rather than the printed {f['printed_gamma_pcf']:g} pcf would give in the "
                 "authors' arithmetic; which input differs, the page does not say. ")
    elif f:
        arith = (f"Checked against each other, the two pressure columns fit no single factor; the runs outside the median one "
                 f"({f['used']:.4f}) are named in `check`. ")
    else:
        arith = ""
    b.append("The report defines the areas in the derived columns only by name (A_ft the total horizontal frontal area, A_pt the "
             "vertical frontal area of the footpad, Fig. 4-4); the depth d is measured from the soil surface to the bottom of the "
             "pad at zero pitch. " + arith + "The `check` column names the runs outside the printed rounding and the heuristic "
             "flags of the areas each run implies.")
    b.append("")
    num = lambda x, k, f: (f"{float(x[k]) * f:.3g}" if x.get(k) else "")
    tbl = [[x["run_number"], num(x, "d_m", 1000), num(x, "VH_m_s", 1), num(x, "FD_N", 1), num(x, "FV_N", 1), x.get("alpha_deg", ""),
            "yes" if x.get("check") else ""] for x in rows]
    b.append(table(["run", "depth d (mm)", "velocity V_H (m/s)", "drag load F_D (N)", "vertical load F_V (N)", "pitch angle (deg)",
                    "check note"], tbl))
    b.append("")
    return b


def data_section(d, r):
    """The data block of a record page: plot, key values, downloads, accuracy, link to the scan check."""
    i = r["experiment_id"]
    obs = d["observations"].get(i)
    if not obs:
        return [], None
    rows, meta = obs["rows"], obs["meta"]
    fig_id = meta.get("figure_id", "")
    panels = meta.get("panels", {})
    b = ["## Data", ""]
    fam = family_of(d, r)
    if i in d["plots"]:
        # one x quantity for all panels (the usual figure), or each panel named (a record from several figures)
        xs = list(dict.fromkeys(v["x_quantity"] for _, v in sorted(panels.items(), key=lambda kv: int(kv[0]))))
        what = (f"{' and '.join(v['y_quantity'] for _, v in sorted(panels.items(), key=lambda kv: int(kv[0])))} against {xs[0]}" if len(xs) == 1 else
                "; ".join(f"{v['y_quantity']} against {v['x_quantity']}" for _, v in sorted(panels.items(), key=lambda kv: int(kv[0]))))
        cap = (f"{what}, SI units"
               + (f", this test in red and the other tests printed in {fig_label(fig_id)} in gray" if len(fam) > 1 else "")
               + ". Error bars are reading bounds (half-widths from the digitization), not standard deviations. Filled markers "
               "were agreed by both readings, hollow ones were not.")
        b.append(f"![{cap}](../{IMG_PLOTS}/{i}.png){{.lightbox}}")
        b.append("")
    # key values from panel 1 traces (or markers)
    # file order is drawing order; `sequence` is each reading's own numbering (Codex's review, 2026-11-19)
    p1 = [x for x in rows if x["panel"] == min(panels)]
    tr = in_order(p1)
    pm = panels[min(panels)]
    sentences = []
    # the peak is read where it was digitized: a `peak` feature as well as the line's samples, which pass beside a
    # sharp apex (Codex's review, 2026-11-19: 272.4 against the agreed peak of 284.6 m/s^2)
    peaks = [x for x in p1 if x["point_kind"] == "feature" and (x.get("note") or "").lower().lstrip().startswith(("peak", "maximum", "crest"))]
    pk = max(tr + peaks, key=lambda x: float(x["y_si"])) if tr else None
    # a panel can hold several curves (the bounds and mean of an envelope): the end is that of the peak's own curve
    own = lambda xs: in_order([x for x in xs if x["series_id"] == pk["series_id"]]) if pk else []
    if tr:
        end = end_of(p1, pk["series_id"]) or (own(p1) or tr)[-1]
        peak = f"Peak {pm['y_quantity']} {si_quantity(float(pk['y_si']), pm['y_unit_si'], pm['y_quantity'])} at {si_quantity(float(pk['x_si']), pm['x_unit_si'], pm['x_quantity'])}"
        # a record whose peak is its last point (a failure envelope's top normal stress) says so once: the same row, or
        # the same values on the same curve, never two points that only round alike (Codex's review, 2026-11-19)
        same = pk is end or (pk["series_id"] == end["series_id"] and
                             (float(pk["x_si"]), float(pk["y_si"])) == (float(end["x_si"]), float(end["y_si"])))
        sentences.append(f"{peak} {pm['x_quantity']}, the end of the record." if same else
                         f"{peak} {pm['x_quantity']}; {si_quantity(float(end['y_si']), pm['y_unit_si'], pm['y_quantity'])} at "
                         f"{si_quantity(float(end['x_si']), pm['x_unit_si'], pm['x_quantity'])}, the end of the record.")
    for p, v in sorted(panels.items()):
        if p == min(panels) or v.get("relation"):   # a panel that re-plots another adds no end value of its own
            continue
        pr = [x for x in rows if x["panel"] == p]
        pp = own(pr) or in_order(pr)
        if pp:
            last = (end_of(pr, pk["series_id"]) if pk else None) or pp[-1]
            q = v['y_quantity'].split(' (')[0]
            sentences.append(f"{q[:1].upper() + q[1:]} {si_quantity(float(last['y_si']), v['y_unit_si'], v['y_quantity'])} at the end.")   # keeps "strut No. 3"
    if sentences:
        b.append(" ".join(sentences))
        b.append("")
    n_marker = sum(1 for x in rows if x["point_kind"] == "marker")
    n_trace = sum(1 for x in rows if x["point_kind"] in ("trace", "gridline"))
    fig_of = lambda v: f" (Fig. {v['figure_id'][1:]})" if v.get("figure_id") else ""   # set on a record from several figures
    cols = "; ".join(f"panel {p}{fig_of(v)}: {v['y_quantity']}{unit_phrase(v['y_unit_si'], v['y_quantity'])} against "
                     f"{v['x_quantity']}{unit_phrase(v['x_unit_si'], v['x_quantity'])}" for p, v in sorted(panels.items()))
    b.append(f"Download: [observations.csv](../files/data/experiments/{i}/observations.csv) ({len(rows)} points: {n_marker} plotted symbols, "
             f"{n_trace} samples of the drawn curve; columns `x_si`, `y_si` with bounds `x_bound_si`, `y_bound_si`; {cols}; the printed-unit "
             f"values, the pixel position on the scan and the review status of each point are kept in further columns) and "
             f"[series.json](../files/data/experiments/{i}/series.json) (units, conversion factors, how the points were read).")
    b.append("")
    # the x bound per x quantity (time and displacement on a record from several figures), then the y bound per panel
    acc = []
    for xq in dict.fromkeys(v["x_quantity"] for _, v in sorted(panels.items(), key=lambda kv: int(kv[0]))):
        ps = [p for p, v in panels.items() if v["x_quantity"] == xq]
        bx = median_or_none(x["x_bound_si"] for x in rows if x["panel"] in ps)
        acc.append(f"typical bound {si_quantity(bx, panels[ps[0]]['x_unit_si'], xq, bound=True)} in {xq}")
    for p, v in sorted(panels.items(), key=lambda kv: int(kv[0])):
        pp = [x for x in rows if x["panel"] == p]
        by = median_or_none(x["y_bound_si"] for x in pp)
        extra = ""
        if p == min(panels) and tr:
            ys = [v for v in (finite_or_none(x["y_si"]) for x in tr + peaks) if v is not None]
            pk = max(ys) if ys else None
            extra = f" ({by / pk * 100:.1f} percent of the peak)" if pk and by is not None else ""
        acc.append(f"{si_quantity(by, v['y_unit_si'], v['y_quantity'], bound=True)} in {v['y_quantity'].split(' (')[0]}{fig_of(v)}{extra}")
    # agreement is the readings' own comparison (agreed, or agreed and then audited); a point settled against the scan
    # (resolved, one reader verified by the other, confirmed by people) is counted apart, never as agreement (Codex's
    # review, 2026-11-20: five one-sided points of b68-ds-fa-4 were called agreed)
    n_pts = len(rows)
    n_ag = sum(x["status"] in ("agreed", "audited") for x in rows)
    n_open = sum(x["status"] not in ("agreed", "audited", "resolved", "one-sided-verified", "confirmed") for x in rows)
    if n_ag == n_pts:
        agree_text = "Both independent readings agree within these bounds at every point. "
    else:
        agree_text = (f"Both independent readings agree within these bounds at {n_ag} of the {n_pts} points; "
                      + (f"the other {n_pts - n_ag} {agree(n_pts - n_ag, 'was', 'were')} settled against the scan (read by "
                         "one reader and verified by the other, or decided between two readings). " if not n_open else
                         f"{n_open} {agree(n_open, 'is', 'are')} still under review (hollow in the plot)"
                         + (f" and {n_pts - n_ag - n_open} {agree(n_pts - n_ag - n_open, 'was', 'were')} settled against the "
                            "scan. " if n_pts - n_ag - n_open else ". ")))
    figs = meta.get("figures") or [fig_id]   # a record from several figures links each figure's check
    checks = ", ".join(f"[{f}](../figures/index.qmd#check-{re.sub(r'[^a-z0-9]+', '-', f.lower())})" for f in figs)
    # 'reading bounds', the data's own term: the uncertainty of our reading of the printed figure, not of the test
    # (Codex's suggestion, 2026-11-19; Dan, 2026-11-20: fix now)
    b.append(f"Reading bounds on {'this figure' if len(figs) == 1 else 'these figures'} (how far our reading of the printed "
             f"figure may be off, not the uncertainty of the test): {', '.join(acc)}. "
             + agree_text
             + (f"[Check the digitized points against the scan](../figures/index.qmd#check-{re.sub(r'[^a-z0-9]+', '-', fig_id.lower())})." if len(figs) == 1
                else f"Check the digitized points against the scan: {checks}."))
    b.append("")
    # what a user of the values must know about an axis or a gap in a line (series.json panel `note`, `breaks`): shown
    # beside the data, not only in the sidecar (Codex's review, 2026-11-19: the misprinted time labels of Fig. 4-19)
    notes = list(dict.fromkeys(v["note"] for _, v in sorted(panels.items(), key=lambda kv: int(kv[0])) if v.get("note")))
    gaps = list(dict.fromkeys(br["reason"].split(";")[0] for br in meta.get("breaks", [])))
    notes = note_fragments(notes)   # a sentence shared by several panels once
    if notes or gaps:
        b.append("**About these values.** " + " ".join(n.rstrip(".") + "." for n in notes)
                 + (" Where the scan has no ink the line is left open: " + "; ".join(gaps) + "." if gaps else ""))
        b.append("")
    return b, fig_id


def audit_counts(rows):
    """(points two reviewers confirmed, points the reviewers sampled) from the audit notes of observations.csv."""
    sampled = [x for x in rows if " | audit: " in x["note"] or x["note"].startswith("audit: ")]
    return sum(1 for x in sampled if x["status"] in ("audited", "confirmed")), len(sampled)


def run_audit_counts(d, i):
    """(cells two reviewers confirmed, cells the reviewers sampled, cells of the record) of a run-table record, from the
    `audit` summary tools/build_run_table.py writes in runs.json."""
    au = d["runs"][i]["meta"].get("audit", {})
    return au.get("cells_confirmed", 0), au.get("cells_sampled", 0), au.get("cells", 0)


def page_experiment(d, r):
    i = r["experiment_id"]
    fam, state = state_of_row(d, r)
    ev = [t.strip() for t in r["evidence"].split(";") if t.strip()]
    figs = [d["fig_by_id"][t] for t in ev if t in d["fig_by_id"]]
    texts = [t for t in ev if t not in d["fig_by_id"]]
    members = family_of(d, r)
    title = record_title(d, r)
    b = []
    # summary paragraph
    soil = f"{r['soil_family']} soil" if r["soil_family"] else "an unnamed soil"
    s = []
    s.append(f"{TYPE_NAME.get(r['test_type'], r['test_type'])} test on {soil}"
             + (f" ({d['mat_by_no'][r['soil_no']]['description_verbatim']})" if r["soil_no"] in d["mat_by_no"] else "")
             + (f" at relative density {r['dr_printed']}" if r["dr_printed"] else (f", {state}" if state and not state.startswith("state not") and state != "conflicting evidence" else ""))
             + (f"; apparatus: {r['apparatus']}" if r["apparatus"] else "") + (f"; loading: {r['loading']}" if r["loading"] else "") + ".")
    if r["measured_channels"]:
        s.append(f"Recorded: {r['measured_channels']}.")
    if len(members) > 1:
        if r["test_type"] == "ds":
            ps = sorted(p for p in (psf_of(x["loading"]) for x in members) if p)
            if ps:
                s.append(f"One of {len(members)} tests of this soil and density at normal stresses from {ps[0] * 47.880258980336 / 1000:.1f} to {ps[-1] * 47.880258980336 / 1000:.1f} kPa, the family the report used to draw the failure envelope.")
        else:
            s.append(f"One of {len(members)} tests drawn from the same figures.")
    b.append(" ".join(s))
    b.append("")
    # trust note
    setup, gaps = setup_rows(d, r)
    obs = d["observations"].get(i)
    note = []
    if obs:
        # the same counts as the reading-bounds sentence of the Data section (Codex's second review, 2026-11-20)
        statuses = Counter(x["status"] for x in obs["rows"])
        n_obs = len(obs["rows"])
        n_ag = statuses.get("agreed", 0) + statuses.get("audited", 0)
        pend = statuses.get("pending-review", 0) + statuses.get("one-sided", 0)
        note.append("The numbers below were digitized from the published figure by two readings made separately"
                    + (" that agree within the stated reading bounds at every point." if n_ag == n_obs else
                       f"; they agree within the stated reading bounds at {n_ag} of the {n_obs} points"
                       + (f", and {pend} {agree(pend, 'is', 'are')} still under review." if pend else
                          ", and the rest were settled against the scan.")))
    elif i in d["runs"]:
        rt = d["runs"][i]["rows"]
        flagged = sum(1 for x in rt if x.get("check"))
        pend = sum(1 for x in rt if x.get("status") != "agreed")   # a run with a cell the readings did not agree on or could not read
        one = "drop" if r["test_type"] == "mdrop" else "run"
        noun = one + "s"
        note.append(f"The {len(rt)} {noun} below were transcribed from the printed table by two readings made separately, which "
                    + ("agree in every cell" if not pend else
                       f"agree in every cell of {len(rt) - pend} {agree(len(rt) - pend, one, noun)}; {pend} "
                       f"{agree(pend, one + ' has', noun + ' have')} a cell still under review")
                    + (f"; {flagged} {agree(flagged, one + ' carries', noun + ' carry')} a note from the arithmetic check of the printed "
                       + ("derived columns." if r["test_type"] == "drag" else "columns.") if flagged else "."))
    else:
        note.append("The measurements of this test have not been digitized yet; the setup and the source pages are indexed.")
    audited = any(a["object"] == i for a in d["audits"])   # an audit of the index row itself (none recorded yet)
    if obs:
        n_aud, n_samp = audit_counts(obs["rows"])
        # in words, without status codes (2026-11-21: "and two of them confirmed 0 (status `audited` or `confirmed`...)")
        conf = ("two reviewers confirmed all of them" if n_aud == n_samp else
                "none has yet been confirmed by two reviewers" if n_aud == 0 else f"two reviewers confirmed {n_aud} of them")
        note.append(f"Student reviewers have looked at {n_samp} of the {len(obs['rows'])} points on the scan; {conf} (see the "
                    "provenance page)." if n_samp else "They have not yet been checked by a person.")
    elif i in d["runs"]:   # a printed table of runs: its cells are audited (D-050, from wave 7)
        n_aud, n_samp, n_cells = run_audit_counts(d, i)
        conf = ("two reviewers confirmed all of them" if n_aud == n_samp else
                "none has yet been confirmed by two reviewers" if n_aud == 0 else f"two reviewers confirmed {n_aud} of them")
        unit = "drops" if r["test_type"] == "mdrop" else "runs"
        # the population named: the agreed values of these runs, run numbers aside (a Table 5-T3 record holds one soil
        # family's drops; Codex's review, round 5)
        note.append(f"Student reviewers have checked {n_samp} of the {n_cells} values of these {unit} (run numbers aside) "
                    f"against the scan; {conf} (see the provenance page)." if n_samp else
                    f"No person has yet checked the values of these {unit} against the scan.")
    else:
        note.append("The setup below rests on two agent readings of the report that were reconciled; no person has checked it yet." if not audited else "A person has checked the setup against the report (see the provenance page).")
    if r["soil_no_status"] == "conflict":
        note.append(f"The report labels the soil state differently in two places ({esc(r['state_printed'])}).")
    if gaps:
        note.append(f"The test setup is incomplete: {', '.join(gaps)} {'is' if len(gaps) == 1 else 'are'} not reported.")
    elif r["setup_status"] == "complete":
        note.append("The test setup is complete as printed.")
    b.append('::: {.callout-note appearance="simple"}')
    b.append(" ".join(note))
    b.append(":::")
    b.append("")
    ds, fig2_id = data_section(d, r)
    b += ds
    b += run_table_section(d, r)
    # reproduce
    b.append("## Reproduce this test")
    b.append("")
    b.append("Every value a simulator needs, with the printed value it was converted from and where it is printed. "
             "Fields the report does not give are marked; a few rows state our own observation and say so.")
    b.append("")
    b.append(table(["group", "quantity", "value", "as printed", "where"], setup))
    b.append("")
    # family
    if len(members) > 1:
        b.append("## The other tests of this family")
        b.append("")
        rows = []
        for x in sorted(members, key=lambda x: (psf_of(x["loading"]) or 0, x["experiment_id"])):
            psf = psf_of(x["loading"]) if r["test_type"] == "ds" else None
            what = f"{psf * 47.880258980336 / 1000:.1f} kPa ({psf:.0f} psf)" if psf else (x["test_label_printed"] or x["experiment_id"])
            rows.append([what, f"**{x['experiment_id']}** (this page)" if x["experiment_id"] == i else f"[{x['experiment_id']}]({x['experiment_id']}.qmd)"])
        b.append(table(["normal stress" if r["test_type"] == "ds" else "test", "record"], rows))
        b.append("")
        if r["test_type"] == "ds":
            b.append("The failure envelope drawn from the peaks of these tests is a derived result, not an extra measurement; "
                     "see the envelope figures in the [figures index](../figures/index.qmd).")
            b.append("")
    # source pages
    b.append("## Source pages")
    b.append("")
    cites = [f"{f['id']}, *{esc(f['title_as_printed'])}*, AM-68-1 Vol. I, printed {f['printed_page']}, PDF {f['pdf_page']}" for f in figs]
    f2 = d["fig2_by_id"].get(fig2_id) if fig2_id else None
    if f2:
        cites.append(f"{f2['id']}, *{esc(f2['title_as_printed'])}*, AM-68-1 Vol. II (NASA CR-92215), printed {f2['printed_page']}, PDF {f2['pdf_page']}")
    if cites:
        b.append("; ".join(cites) + "." + (" The Volume II printing is the one digitized; the Volume I printing shows the same tests." if f2 and figs else ""))
    for t in texts:
        b.append(f"Text: {t}.")
    b.append("")
    imgs = [thumb(d, f["pdf_page"]) for f in figs] + ([thumb(d, f2["pdf_page"], vol=2)] if f2 else [])
    if imgs:
        b.append("::: {layout-ncol=2}")
        for im in imgs:
            b.append(im)
            b.append("")
        b.append(":::")
        b.append("")
    # cite
    b.append("## How to cite")
    b.append("")
    b.append(f"Record `{i}` in `data/experiments/index.csv` of this repository, and the source: "
             + ("; ".join(cites) if cites else SOURCE_CITE + ", text") + ".")
    b.append("")
    b.append(f"<small>Maintainers: the [provenance and review record](../review/{i}.qmd) of this record holds the reconciliation of the two "
             "readings, the point statuses, the calibration residuals and the audit status.</small>")
    yaml = OrderedDict([("record", i), ("kind", r["kind"]), ("test-type", TYPE_NAME.get(r["test_type"], r["test_type"])),
                        ("family", r["soil_family"]), ("state", state), ("printed-label", r["test_label_printed"]), ("evidence", r["evidence"]),
                        ("setup", SETUP_WORDS.get(r["setup_status"], r["setup_status"])), ("record-status", r["status"]), ("priority", r["priority"]),
                        ("mcc", r["mcc_relevant"])])
    return page(title, "\n".join(b), ["data/experiments/index.csv", "data/experiments/index.json", "corpus/1968/figures.csv",
                                      "corpus/1968-vol2/figures.csv", "data/materials/materials.csv", "data/experiments/<id>/observations.csv"],
                extra_yaml=yaml)


def page_record_provenance(d, r):
    """Maintainers' page of a record: what the two agents read, how it was reconciled, what a person has checked."""
    i = r["experiment_id"]
    cells = d["cells_by_id"].get(i, {"cell_status": {}}); cells.setdefault("resolution_notes", {})
    b = [f"Provenance and review record of [{i}](../experiments/{i}.qmd). Written for the maintainers and the student auditors; "
         "the record page itself carries only what a user of the data needs.", ""]
    b.append("## Status")
    b.append("")
    st = [["setup completeness", {"complete": "complete: bed state, tool, bin and rate are printed", "setup_incomplete": "incomplete: see the reproduce block on the record page", "pending": "pending: a series whose underlying tests are not identified"}.get(r["setup_status"], r["setup_status"])],
          ["observations", (f"{len(d['observations'][i]['rows'])} points recovered, "
                            + ", ".join(f"{k} {v}" for k, v in sorted(Counter(x["status"] for x in d["observations"][i]["rows"]).items()))) if i in d["observations"]
           else (f"{len(d['runs'][i]['rows'])} runs transcribed from the printed table (`runs.csv`), "
                 + ", ".join(f"{k} {v}" for k, v in sorted(Counter(x["status"] for x in d["runs"][i]["rows"]).items()))
                 + f"; batch review `qa/{d['runs'][i]['meta'].get('batch', '')}/review.md`"
                 + (f", arithmetic check `{d['runs'][i]['meta']['arithmetic']['report']}`"
                    if d["runs"][i]["meta"].get("arithmetic", {}).get("report") else "")) if i in d["runs"]
           else MISSING["nye"] + " (no `observations.csv` for this record)"],
          ["index row reconciliation", f"{status_span(r['status'])}: " + ", ".join(f"{k} {v}" for k, v in sorted(Counter(cells["cell_status"].values()).items()))],
          ["human audit", (lambda n, s: f"{s} points sampled by the student reviewers, {n} confirmed by two of them (status audited or confirmed); "
                                       "see the audits table on the Review page" if s else "No human audit recorded")(
              *audit_counts(d["observations"][i]["rows"])) if i in d["observations"] else
           (lambda n, s, c: f"{s} of the {c} agreed values of these {'drops' if r['test_type'] == 'mdrop' else 'runs'} (run numbers aside) sampled by the student reviewers, {n} confirmed by two of them; each "
                            "run's audited cells are in the `audit` column of `runs.csv`, and the audits table is on the Review page"
                            if s else "No human audit recorded")(*run_audit_counts(d, i)) if i in d["runs"] else
           "No human audit recorded"],
          ["benchmark eligibility", "not yet assigned (no benchmark protocol declared)"]]
    if r["soil_no_status"] == "conflict":
        st.insert(0, ["conflict", MISSING["conf"] + f": {esc(r['state_printed'])}"])
    b.append(table(["aspect", "state"], st))
    b.append("")
    b += observations_section(d, i)
    b.append("## Printed values (not converted)")
    b.append("")
    b.append(table(["field", "as printed"], [
        ["state", missing(r["state_printed"])], ["Dr", missing(r["dr_printed"])],
        ["unit weight, pcf", missing(r["unit_weight_printed_pcf"])], ["Gp, g", missing(r["gp_printed_g"])],
        ["tool", missing(r["penetrator_printed"])], ["bin, inches", missing(r["bin_printed_in"])],
        ["rate", missing(r["rate_printed"])], ["start depth, inches", missing(r["start_depth_printed_in"])]]))
    b.append("")
    b.append("## Reconciliation record of the index row")
    b.append("")
    rows = []
    for col, stt in sorted(cells["cell_status"].items()):
        rows.append([col, status_span(stt.split(":")[0].strip()), cells["resolution_notes"].get(col, "")])
    b.append(table(["column", "status", "resolution note"], rows) if rows else "One-sided row: present in one submission only.")
    alts = d["alts_by_id"].get(i, [])
    if alts:
        b.append("")
        b.append("Descriptive fields where the two readings differ in wording (the first is used on the record page):")
        b.append("")
        b.append(table(["column", "Claude", "Codex"], [[a["column"], a["claude"], a["codex"]] for a in alts]))
    b.append("")
    b.append("## Notes from the two readings")
    b.append("")
    b.append(f"- Claude: {r['notes_claude'] or '(none)'}")
    b.append(f"- Codex: {r['notes_codex'] or '(none)'}")
    b.append("")
    return page(f"{i}: provenance", "\n".join(b), ["data/experiments/index.csv", "data/experiments/index.json", "qa/audits.csv",
                                                   "data/experiments/<id>/observations.csv", "data/experiments/<id>/series.json"])


def overlays_section(d):
    """Figures page: the digitized points of both readings drawn on the scan, one subsection per figure."""
    by_fig = {}
    for k in sorted(d["overlays"]):
        fig = k.rsplit("-p", 1)[0]
        by_fig.setdefault(fig, []).append(k)
    if not by_fig:
        return []
    b = ["", "## Digitized figures checked against the scan", "",
         "For every figure whose curves have been digitized, both independent readings are drawn on the page image "
         "(filled circles: the canonical reading; hollow squares: the other; bars: pixel bounds). Click to enlarge. "
         "Record pages link here; the review of each batch is under `qa/<batch>/review.md`.", ""]
    for fig, keys in by_fig.items():
        anchor = "check-" + re.sub(r"[^a-z0-9]+", "-", fig.lower())
        b.append(f"### {fig} {{#{anchor}}}")
        b.append("")
        for k in keys:
            b.append(f"![{fig}, panel {k.rsplit('-p', 1)[1]}: both readings on the scan](../{IMG_OVERLAYS}/{k}.png){{.lightbox}}")
            b.append("")
    return b


def page_figures(d):
    rows = []
    for r in d["figures"]:
        rows.append([thumb(d, r["pdf_page"], width=90), r["id"], r["kind"], r["title_as_printed"], r["printed_page"], r["pdf_page"],
                     r["test_type"], r["data_form"], r["panels"], r["curves"], r["in_scope"], r["priority"], r["mcc_relevant"],
                     status_span(r["status"])])
    body = ["Every figure and table the two inventories reconciled, one section per volume. Click a thumbnail to "
            "enlarge; the full-resolution scan is the PDF page named in the row. `in scope` means the item carries "
            "numbers to extract; `pri` is the protocol priority (1 first); `MCC` flags history-dependent behaviour.", "",
            "## Volume I, Table 1-1 and Sections II to VI (NASA CR-92208)", "",
            table(["page", "id", "kind", "title as printed", "printed", "PDF", "type", "form", "panels", "curves",
                   "in scope", "pri", "MCC", "status"], rows,
                  caption="Source: `corpus/1968/figures.csv`; cell statuses and both agents' notes in `corpus/1968/figures.json`. Thumbnails at 110 dpi from the NTRS copy of Volume I ([19680021852](https://ntrs.nasa.gov/citations/19680021852)), courtesy of NASA.",
                  num_cols=["PDF", "panels", "curves"])]
    rows2 = []
    for r in d["figures_vol2"]:
        rel = r["relation"] if r["relation"] == "none" else f"{r['relation']} {r['relation_target']}".strip()
        rows2.append([thumb(d, r["pdf_page"], width=90, vol=2), r["id"], r["kind"], r["title_as_printed"], r["printed_page"], r["pdf_page"],
                      r["test_type"], r["data_form"], r["panels"], r["curves"], r["in_scope"], r["priority"], r["mcc_relevant"],
                      rel, status_span(r["status"])])
    n2 = Counter(r["appendix"] for r in d["figures_vol2"])
    body += ["", "## Volume II, Appendices A, B and C (NASA CR-92215)", "",
             f"Appendix A, soil specifications ({n2['A']} items: a chemical analysis, a photomicrograph, a grain-size "
             f"curve, a density chart and a friction-angle chart per soil, repeated under each soil of a material); "
             f"Appendix B, the IITRI sonic modulus report ({n2['B']}); Appendix C, the direct shear program ({n2['C']}: "
             "85 single tests on 15 soil and density series as data sheets, hand-drawn and computer-fitted envelopes, "
             "and friction angle versus relative density). `relation` links a figure to the one it reproduces or "
             "derives from, in either volume; `reproduces` rows hold no new numbers and are out of scope.", "",
             table(["page", "id", "kind", "title as printed", "printed", "PDF", "type", "form", "panels", "curves",
                    "in scope", "pri", "MCC", "relation", "status"], rows2,
                   caption="Source: `corpus/1968-vol2/figures.csv`; cell statuses, both agents' notes and the id aliases in `corpus/1968-vol2/figures.json`. Thumbnails at 110 dpi from the NTRS copy of Volume II ([19680021853](https://ntrs.nasa.gov/citations/19680021853)), courtesy of NASA.",
                   num_cols=["PDF", "panels", "curves"])]
    body += overlays_section(d)
    return page("Figures", "\n".join(body), ["corpus/1968/figures.csv", "corpus/1968/figures.json",
                                               "corpus/1968-vol2/figures.csv", "corpus/1968-vol2/figures.json", "qa/<batch>/overlays.csv"])


def page_materials(d):
    m, meta = d["materials"], d["materials_meta"]
    rows = [[r["soil_no"], r["bendix_designation"], r["family"], r["state"], r["relative_density"], r["unit_weight_N_m3"],
             r["bulk_density_kg_m3"], r["friction_angle_deg"], r["elastic_modulus_Pa"], r["mean_grain_size_mm"],
             r["uniformity_coeff"], r["percent_passing_200"], r["d95_mm"], status_span(r["status"])] for r in m]
    body = [f"The twelve test soils of Table 2-3 ({meta['source']}). SI canonical; the printed values are in the traceability table below.", "",
            # the codes in the header carry their hover definitions (Dan, 2026-11-20); num_cols matches the same strings
            table(["no.", "designation", "family", "state", term("Dr"), "unit weight, N/m^3", "bulk density, kg/m^3",
                   term("phi") + ", deg", "E, Pa", term("D50") + ", mm", term("Cu"), "passing No. 200", term("D95") + ", mm",
                   "status"], rows,
                  caption="Source: `data/materials/materials.csv`. E is the initial tangent modulus by sonic means at 4 psi confinement.",
                  num_cols=[term("Dr"), "unit weight, N/m^3", "bulk density, kg/m^3", term("phi") + ", deg", "E, Pa", term("D50") + ", mm", term("Cu"), term("D95") + ", mm"]),
            "", "## Traceability: values as printed", "",
            table(["no.", "description as printed", "unit weight", "modulus", "read flags", "source"],
                  [[r["soil_no"], r["description_verbatim"], r["unit_weight_native"] + " " + r["unit_weight_unit"],
                    r["elastic_modulus_native"] + " " + r["elastic_modulus_unit"], r["read_flags"] or "", r["source_locator"]] for r in m]),
            "", "## Conversion factors and source inconsistencies", ""]
    body += [f"- `{k}`: {v}" for k, v in meta["factors"].items()]
    body += [f"- Soil {s['soil_no']}, {s['column']}: canonical {s['canonical']} (Table 2-3) against {s['elsewhere']} in "
             f"{s['elsewhere_locator']} (found by {s['found_by']}, {s['date']})." for s in meta.get("source_inconsistencies", [])]
    return page("Materials", "\n".join(body), ["data/materials/materials.csv", "data/materials/materials.json"])


def page_sources(d):
    st = Counter(r["status"] for r in d["register"])
    body = ["## Register", "",
            f"{len(d['register'])} sources: {st.get('acquired', 0)} acquired (file in hand, checksummed), {st.get('located', 0)} located "
            f"(identity confirmed against the archive record by the 2026-10-07 screening, file not yet downloaded; the screening "
            f"verdict is in the notes), {st.get('lead', 0)} leads not yet located. Status moves to `acquired` only with a file and a checksum.", "",
            table(["id", "status", "title", "report numbers", "date", "pages", "rights evidence", "holds", "notes"],
                  [[r["source_id"], r["status"], r["title"], r["report_numbers"], r["date"], r["pages"], r["rights_evidence"], r["holds"], r["notes"]] for r in d["register"]],
                  caption="Source: `sources/register.csv`; the screening submission is `extractions/codex/leads-screen-b1/` and its review `qa/leads-screen-b1/review.md`.", num_cols=["pages"]),
            "", "## Leads from the broadened hunt", "",
            f"{len(d['leads'])} candidate sources graded by two independent searches (Claude and Codex, 2026-10-07). "
            "`found_by` says who found it; where both did, both grades are kept and the lower priority number and the stricter "
            "rights reading stand until the document is screened. Rights: `public_domain`, `open_license`, `restricted`, `unknown`. "
            "Data form: `raw`, `tables`, `curves`, `parameters-only`.", ""]
    rows = []
    for r in d["leads"]:
        link = f"[{esc(r['title'])}]({r['url']})" if r["url"].startswith("http") else esc(r["title"])
        rows.append([r["lead_id"], r["year"], link, r["report_or_doi"], r["rights_assessment"], r["data_form"], r["setup_recoverability"],
                     r["test_types"], r["materials"], r["gravity_condition"], r["priority"], r["found_by"]])
    body.append(table(["lead", "year", "title", "report or DOI", "rights", "data form", "setup", "tests", "materials", "gravity", "pri", "found by"],
                      rows, caption="Source: `sources/leads.csv`; every search run is in `sources/searches-log.csv`."))
    return page("Sources", "\n".join(body), ["sources/register.csv", "sources/leads.csv"])


def page_review(d):
    body = ["## Human audits recorded", ""]
    if d["audits"]:
        body.append(table(["batch", "object", "column", "auditor", "date", "outcome", "note"],
                          [[a["batch"], a["object"], a["column"], a["auditor"], a["date"], a["outcome"], a["note"]] for a in d["audits"]]))
    else:
        body.append("**No human audit recorded.** Every value on this site rests on agreement between two agent readings or on a "
                    "documented rule; none has been checked by a person yet.")
    body += ["", "## Batch reviews", ""] + [f"- `{p}`" for p in d["reviews"]]
    body += ["", "## Per-record provenance pages", "",
             f"Every record page links to its provenance page under `review/<record>` ({len(d['experiments'])} pages): the status of the "
             "index row and of the digitized points, the reconciliation of the two readings, the calibration residuals, the as-printed "
             "values and the two agents' notes. The record pages themselves carry only what a user of the data needs.",
             "", "## Cells that one agent supplied and nobody checked", ""]
    one = [[c["experiment_id"], col, st] for c in d["experiments_meta"]["cells"] for col, st in c["cell_status"].items()
           if st.startswith("one-sided") and col != "row"]
    rows_one = [c["experiment_id"] for c in d["experiments_meta"]["cells"] if c["cell_status"].get("row", "").startswith("one-sided")]
    body.append(f"{len(one)} cells and {len(rows_one)} whole rows in the experiment index come from one agent's reading (the other "
                "left the field empty or did not list the row). They are candidates for the audit sample.")
    body.append("")
    if one:
        body.append(table(["experiment", "column", "status"], [[f"[{e}](../experiments/{e}.qmd) ([provenance]({e}.qmd))", c, s] for e, c, s in one]))
    body += ["", "## Provisional and conflicting", "", "Rows whose state the report labels differently in two places:", "",
             table(["experiment", "soil status", "state as printed", "evidence"],
                   [[f"[{r['experiment_id']}](../experiments/{r['experiment_id']}.qmd)", r["soil_no_status"], r["state_printed"], r["evidence"]]
                    for r in d["experiments"] if r["soil_no_status"] == "conflict"]),
             "", "Figure rows with a provisional count:", "",
             table(["figure", "title", "curves", "status"], [[r["id"], r["title_as_printed"], r["curves"], r["status"]] for r in d["figures"] if r["status"] == "provisional"], num_cols=["curves"])]
    return page("Review", "\n".join(body), ["qa/audits.csv", "data/experiments/index.json", "data/experiments/index.csv", "corpus/1968/figures.csv"])

def md_body(rel):
    """A repository Markdown file as a page body: the H1 dropped (the page has a title), other headings kept."""
    text = (ROOT / rel).read_text(encoding="utf-8")
    lines = [l for l in text.splitlines() if not l.startswith("# ")]
    return "\n".join(lines).strip()


def page_insights_index(d):
    b = ["Judgment, caveats and recommendations the report authors recorded, as distinct from the numbers. "
         "Each note cites its pages; each note carries `review_status: pending` until the transcription of those "
         "pages is reconciled.", ""]
    for name in d["insights"]:
        stem = name[:-3]
        title = (ROOT / "insights" / name).read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        b.append(f"- [{title}]({stem}.qmd)")
    return page("Insights", "\n".join(b), ["insights/*.md"])


def page_insight(d, name):
    stem = name[:-3]
    title = (ROOT / "insights" / name).read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
    body = ("::: {.callout-note}\nReview status: **pending**. Written from a first read of the pages; quote with that caveat "
            "until the page transcriptions are reconciled.\n:::\n\n" + md_body(f"insights/{name}"))
    return page(title, body, [f"insights/{name}"])


def page_methods_index(d):
    b = ["How the data are organized and how agents and people work on them. These pages are the repository's own "
         "documents, rendered as they are.", "",
         "- [Data organization and conventions](data-organization.qmd): layout, identifiers, units, status vocabularies, the reading-bound and agreement rules, the site rules.",
         *([] if private("AGENTS.md") else [
             "- [Guide for agents](agents.qmd): how an agent answers a question from the corpus, works on the data, and how the two-agent protocol runs."]),
         "", "## The two-agent method in one paragraph", "",
         "Every inventory or extraction is made twice, by Claude and by Codex, each from the same evidence (the PDF, the page map, "
         "the agreed indexes) and without seeing the other's output. A script compares the two mechanically; cells that match are "
         "`agreed`; cells that differ are settled by a documented rule, a convention, or a re-read of the page, and the resolution is "
         "written down with credit to whichever reading was right. Agreement between two agents is not confirmation: a student "
         "reviews every disagreement and audits a 5 to 10 percent sample of agreements, and only recorded audits count (`qa/audits.csv`)."]
    return page("Methods", "\n".join(b), ["docs/DATA-ORGANIZATION.md"] + ([] if private("AGENTS.md") else ["AGENTS.md"]))


def page_methods_doc(d, title, rel):
    return page(title, md_body(rel), [rel])


# The files the Downloads page lists and links. tools/render_site.py and tools/make_public_release.py copy them into
# _site/files/ after the render, so a link there opens the file of the commit the site was rendered from.
DOWNLOAD_FILES = ["data/experiments/index.csv", "data/experiments/index.json", "data/materials/materials.csv",
                  "data/materials/materials.json", "corpus/1968/figures.csv", "corpus/1968/figures.json", "corpus/1968/page-map.csv",
                  "corpus/1968-vol2/figures.csv", "corpus/1968-vol2/figures.json", "corpus/1968-vol2/page-map.csv",
                  "corpus/1968-vol2/page-map-corrections.csv", "sources/register.csv", "sources/leads.csv",
                  "sources/searches-log.csv", "qa/audits.csv", "docs/decisions.csv"]

# The two volumes of the source report, as in the lab's uwsbel/BibFiles (refsTerramech.bib), same keys.
REPORT_BIBTEX = """@techreport{bendix68vol1,
  title       = {Lunar Module ({LM}) Soil Mechanics Study, Volume {I}, Final Report},
  author      = {{Bendix Corporation, Energy Controls Division}},
  institution = {Bendix Corporation, Energy Controls Division},
  address     = {South Bend, IN},
  number      = {AM-68-1, Vol. I; NASA CR-92208},
  note        = {Prepared for NASA under contract NAS 9-5759},
  month       = {May},
  year        = {1968},
  url         = {https://ntrs.nasa.gov/citations/19680021852}
}

@techreport{bendix68vol2,
  title       = {Lunar Module ({LM}) Soil Mechanics Study, Volume {II}, Final Report},
  author      = {{Bendix Corporation, Energy Controls Division}},
  institution = {Bendix Corporation, Energy Controls Division},
  address     = {South Bend, IN},
  number      = {AM-68-1, Vol. II; NASA CR-92215},
  note        = {Prepared for NASA under contract NAS 9-5759},
  month       = {May},
  year        = {1968},
  url         = {https://ntrs.nasa.gov/citations/19680021853}
}"""


def read_cff(text=None):
    """The top-level scalars and the authors of CITATION.cff (this repository's, or the given text: the release tool reads
    the file of the commit it releases). A small reader for this file's flat layout (no YAML library in the tools'
    environment): top-level `key: value` lines, and the `authors:` list of `key: value` items."""
    top, authors, in_authors = {}, [], False
    for line in (text if text is not None else (ROOT / "CITATION.cff").read_text(encoding="utf-8")).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            in_authors = line.startswith("authors:")
            m = re.match(r"([\w-]+):\s*(.*)$", line)
            if m and m.group(2) and m.group(2) not in (">-", ">", "|", "|-"):
                top[m.group(1)] = m.group(2).strip().strip('"')
        elif in_authors:
            m = re.match(r"\s*(-\s+)?([\w-]+):\s*(.*)$", line)
            if m:
                if m.group(1) or not authors:
                    authors.append({})
                authors[-1][m.group(2)] = m.group(3).strip().strip('"')
    return top, authors


def release_bibtex():
    """A BibTeX entry for the data release, from CITATION.cff, so the two never disagree. The DOI (and Zenodo as the
    publisher, for a Zenodo DOI) appears once CITATION.cff carries a `doi:` line."""
    top, authors = read_cff()
    names = [f"{a['family-names']}, {a['given-names']}" if "family-names" in a else "{" + a.get("name", "") + "}" for a in authors]
    year = top.get("date-released", "")[:4]
    key = re.sub(r"[^a-z]", "", (authors[0].get("family-names") or authors[0].get("name", "data")).lower()) + year + "terramechanics"
    doi = top.get("doi", "")
    fields = [("author", " and ".join(names)), ("title", "{" + top["title"] + "}"),
              ("howpublished", f"Data set, version {top['version']}"), ("year", year)]
    if doi:
        fields += [("publisher", "Zenodo")] if doi.startswith("10.5281/zenodo") else []
        fields += [("doi", doi), ("url", f"https://doi.org/{doi}")]
    else:
        fields += [("url", top["repository-code"])]
    w = max(len(k) for k, _ in fields)
    return f"@misc{{{key},\n" + ",\n".join(f"  {k:<{w}} = {{{v}}}" for k, v in fields) + "\n}", bool(doi)


def page_downloads(d):
    files = DOWNLOAD_FILES
    what = {"data/experiments/index.csv": "experiment index (one row per record; printed values as index fields)",
            "data/experiments/index.json": "sidecar: per-cell statuses, resolution notes, both agents' wording, rules applied",
            "data/materials/materials.csv": "twelve soils in SI with the printed values beside them",
            "data/materials/materials.json": "sidecar: source, conversion factors, per-cell statuses, source inconsistencies",
            "corpus/1968/figures.csv": "figures index of Vol. I, Table 1-1 and Sections II to VI", "corpus/1968/figures.json": "sidecar: rules, per-cell statuses, both agents' notes",
            "corpus/1968/page-map.csv": "PDF page to printed label",
            "corpus/1968-vol2/figures.csv": "figures and tables index of Vol. II Appendices A, B, C (with relations to Vol. I)",
            "corpus/1968-vol2/figures.json": "sidecar: rules, per-cell statuses, id aliases, both agents' notes",
            "corpus/1968-vol2/page-map.csv": "PDF page to printed label, Vol. II",
            "corpus/1968-vol2/page-map-corrections.csv": "labels read from the page image where OCR and inference failed (scrambled binding, IITRI pages)",
            "sources/register.csv": "acquired and screened sources with rights evidence",
            "sources/leads.csv": "graded leads from the broadened hunt", "sources/searches-log.csv": "every search run, including dead ends",
            "qa/audits.csv": "human audits recorded", "docs/decisions.csv": "decision log"}
    rows = []
    for f in files:
        p = ROOT / f
        n = ""
        if f.endswith(".csv"):
            with p.open(encoding="utf-8-sig", newline="") as fh:
                n = str(sum(1 for _ in csv.reader(fh)) - 1) + " rows"
        rows.append([f"[`{f}`](../files/{f})", what.get(f, ""), n])
    bib, has_doi = release_bibtex()
    b = ["Every file on this page is the repository file itself, as of the revision named in the footer; the site never holds "
         "a separate copy of a number. Select a file name to open or download it. Each CSV has a JSON sidecar beside it that "
         "carries source, conversion factors, status definitions and the two submissions it was reconciled from.", "",
         table(["file", "what it contains", "size"], rows), "",
         "## Files of each record", "",
         f"- `data/experiments/<id>/observations.csv` and `series.json`: the digitized points of a figure, with pixel coordinates, "
         f"calibration residuals and reading bounds. Available for the {len(d['observations'])} records whose figures have been read, "
         "and linked from each of their pages; the figures of the other records have not been read yet.",
         f"- `data/experiments/<id>/runs.csv` and `runs.json`: a printed table of runs, one physical test per row. Available for the "
         f"{sum(1 for p in (ROOT / 'data' / 'experiments').glob('*/runs.csv'))} records that are tables of runs, and linked from their pages.",
         "", "## Not yet available", "",
         "- `data/experiments/<id>/setup.json`: the setup of each test as machine-readable fields. Until it exists, each record "
         "page gives the setup as a table.",
         "", "## How to cite", "",
         "Cite the data release used and the report the numbers come from. Where numbers are used, give the record id and "
         "the source page as well, for example `b68-lpt-027`, AM-68-1 Vol. I, Fig. 2-29, printed 2-55, PDF 80.", "",
         "Record ids are permanent: a record keeps its id and its page address from one release to the next. A record that "
         "is merged into another or withdrawn keeps a page that says where its data went, and the changelog of the release "
         "lists the change. A citation of a release by its DOI always reaches the files of that release.", "",
         "The data release" + ("" if has_doi else " (the entry gains a DOI when the release is archived)") + ":", "",
         "```bibtex", bib, "```", "",
         "The source report, AM-68-1, in two volumes:", "",
         "```bibtex", REPORT_BIBTEX, "```"]
    return page("Downloads", "\n".join(b), files + ["CITATION.cff"])


# ----------------------------------------------------------------------------- main

def generate(out_dir: Path, d, private_paths=()):
    """Write every page under out_dir. private_paths: the public release's exclusions (see PRIVATE)."""
    global PRIVATE
    PRIVATE = tuple(private_paths)
    pages = {"index.qmd": page_index(d), "decisions.qmd": page_decisions(d), "experiments/index.qmd": page_experiments_index(d),
             "figures/index.qmd": page_figures(d), "materials/index.qmd": page_materials(d), "sources/index.qmd": page_sources(d),
             "review/index.qmd": page_review(d), "records/index.qmd": page_records(d), "about/index.qmd": page_about(d),
             "contribute/index.qmd": page_contribute(d), "glossary/index.qmd": page_glossary(d), "simulate/index.qmd": page_simulate(d)}
    for r in d["experiments"]:
        card = r["experiment_id"] == PILOT_RECORD   # the pilot of the card template; the rest after Dan's look
        pages[f"experiments/{r['experiment_id']}.qmd"] = page_experiment_card(d, r) if card else page_experiment(d, r)
        pages[f"review/{r['experiment_id']}.qmd"] = page_record_provenance(d, r)
    pages["insights/index.qmd"] = page_insights_index(d)
    for name in d["insights"]:
        pages[f"insights/{name[:-3]}.qmd"] = page_insight(d, name)
    pages["methods/index.qmd"] = page_methods_index(d)
    pages["methods/data-organization.qmd"] = page_methods_doc(d, "Data organization and conventions", "docs/DATA-ORGANIZATION.md")
    if not private("AGENTS.md"):
        pages["methods/agents.qmd"] = page_methods_doc(d, "Guide for agents", "AGENTS.md")
    if not private("docs/ROADMAP.md"):
        pages["roadmap.qmd"] = page_methods_doc(d, "Roadmap", "docs/ROADMAP.md")
    pages["open-questions.qmd"] = page_methods_doc(d, "Open questions", "docs/OPEN-QUESTIONS.md")
    pages["downloads/index.qmd"] = page_downloads(d)
    bad = {rel: undefined_terms(pages[rel]) for rel in PILOT_PAGES}
    bad = {rel: codes for rel, codes in bad.items() if codes}
    if bad:
        sys.exit("codes used without a definition on the page (plan v3, A2.3): "
                 + "; ".join(f"{rel}: {', '.join(c)}" for rel, c in bad.items()))
    for rel, text in pages.items():
        p = out_dir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text.replace("\r\n", "\n") + "\n", encoding="utf-8", newline="\n")
    return pages


def missing_images(d):
    """What the image cache lacks that the pages link (an empty list when it is complete enough to write them). Pages link
    page images, plots and the overlay anchors only when the cache holds them, so pages written without them would silently
    lose those links (Codex's review of the export, 2026-11-23, rounds 2 and 3). Shared by main and by
    tools/make_public_release.py. A checkout of the public repository has no images (they are generated, git ignores them)."""
    need = [n for n, k in (("Volume I page thumbnails", "thumbs"), ("Volume II page thumbnails", "thumbs2"), ("plots", "plots"),
                           ("overlays", "overlays")) if not d[k]]
    need += [f"the overlay {k}" for k in (START_OVERLAY,) if d["overlays"] and k not in d["overlays"]]
    need += [f"the plot of {i}" for i in d["observations"] if d["plots"] and i not in d["plots"]]
    return need


def main(argv):
    d = load()
    missing = missing_images(d)
    if missing and "--allow-missing-images" not in argv:
        sys.exit(f"the image cache under work/site-cache lacks {', '.join(missing[:8])}"
                 + (f" and {len(missing) - 8} more" if len(missing) > 8 else "") + ": render the page images "
                 "(tools/render_pages.py, into work/site-cache/<source>/thumb110/) and the plots and overlays "
                 "(tools/figures/build_plot_cache.py) first, or pass --allow-missing-images to write pages without them")
    if "--check" in argv:
        tmp = Path(tempfile.mkdtemp(prefix="site-check-"))
        try:
            pages = generate(tmp, d)
            bad = []
            for rel in pages:
                a, b = (SITE / rel), (tmp / rel)
                if not a.exists():
                    bad.append(f"missing in site/: {rel}")
                elif a.read_bytes() != b.read_bytes():
                    bad.append(f"differs: {rel}")
            for p in SITE.rglob("*.qmd"):
                rel = p.relative_to(SITE).as_posix()
                if rel not in pages and not rel.startswith("_"):
                    bad.append(f"not generated by this script: {rel}")
            print("\n".join(bad) if bad else f"site/ matches a fresh generation ({len(pages)} pages)")
            return 1 if bad else 0
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    pages = generate(SITE, d)
    copied, missing_thumbs = copy_thumbs(d, SITE)
    print(f"wrote {len(pages)} pages under {SITE.relative_to(ROOT)}; copied {copied} thumbnails; "
          f"{len(missing_thumbs)} thumbnails missing from the cache" + (f": {', '.join(missing_thumbs)}" if missing_thumbs else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
