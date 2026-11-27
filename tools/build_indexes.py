"""Build the corpus indexes from the transcribed pages (roadmap step 2d).

Usage:
    python tools/build_indexes.py [--check]

For every source with page files (corpus/<source>/pages/pNNNN.md) writes, next to its figures.csv:

    contents.csv   source, section, title, level, pdf_page, printed_page, review_status
                   one row per printed heading (section numbers as printed; unnumbered appendix
                   titles carry the appendix letter)
    equations.csv  source, number, latex, pdf_page, printed_page, context, review_status
                   one row per display equation ($$...$$), with its printed number when one is
                   printed beside it and the sentence that introduces it as context
    symbols.csv    source, symbol, meaning, units, pdf_page, printed_page, equation, review_status
                   one row per entry of a printed "where" list (SYMBOL = meaning (units)), linked to
                   the numbered equation above the list when there is one
    glossary.csv   source, term, definition, pdf_page, printed_page, review_status
                   the report's own list of abbreviations and names (Vol. I section 2.1.1);
                   a definition printed without its term keeps the term empty

Vol. II Appendix A specification sheets carry no numbered headings; each sheet title (SPECIFICATION FOR
SOIL NO. n) is listed in contents.csv with section "A/soil n". A lettered heading inside an appendix
("C. RESULTS" in the IITRI report reproduced as Appendix B) gets section "B/C", so it is not read as
Appendix C.

Every row carries the page's review_status, so an agent quoting an index row knows how far the
page has been checked. Printed duplicates are kept as printed (for example two different
equations both numbered 3-1 in Vol. I Section II). The output is deterministic (sorted by PDF page
and position, LF, UTF-8); --check compares a fresh build with the files on disk.
"""
import csv
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {"1968": "bendix-1968-vol1", "1968-vol2": "bendix-1968-vol2"}
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
NUMBERED = re.compile(r"^((?:[IVX]+|[A-Z]|\d+(?:\.\d+)*))\.?\s+(.*)$")
EQ = re.compile(r"^\$\$(.+?)\$\$\s*(?:\(([^)]+)\))?\s*$")
WHERE = re.compile(r"^where\b", re.I)
DEF = re.compile(r"^(.{1,40}?)\s+=\s+(.+)$")
UNITS = re.compile(r"\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)\s*$")
SPEC = re.compile(r"^SPECIFICATION FOR SOIL NO\.?\s*(\d+)", re.I)
LETTERED = re.compile(r"^([A-Z])\.\s+(.+)$")
# a where-list entry printed as a sentence ("E is the initial tangent modulus", Vol. II Appendix B)
DEF_IS = re.compile(r"^(\S{1,6})\s+is\s+(the\s+.+?)\.?$")
GLOSS = re.compile(r"^(.{1,40}?)\s+-{1,2}\s*(.+)$")


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    head = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            head[k.strip()] = v.strip().strip('"')
    paras = [p.strip() for p in re.split(r"\n\s*\n", m.group(2)) if p.strip()]
    return head, paras


def build(source_dir, source_id):
    pages = sorted((source_dir / "pages").glob("p[0-9]*.md"))
    contents, equations, symbols, glossary = [], [], [], []
    in_glossary = False
    appendix = ""  # letter of the appendix being read, so lettered sections inside it are not mistaken for appendices
    for p in pages:
        head, paras = parse(p)
        loc = {"source": source_id, "pdf_page": int(head["pdf_page"]), "printed_page": head.get("printed_page", ""),
               "review_status": head.get("review_status", "")}
        where_eq, in_where, prev = "", False, ""
        last_eq = ""
        for para in paras:
            h = HEADING.match(para)
            if h:
                level, title = len(h.group(1)), h.group(2).strip()
                n = NUMBERED.match(title)
                section, name = (n.group(1), n.group(2)) if n and any(c.isdigit() for c in n.group(1)) or (n and n.group(1).isupper() and len(n.group(1)) <= 4 and " " in title and title.split()[0] in ("SECTION", "APPENDIX")) else ("", title)
                if title.split()[0] in ("SECTION", "APPENDIX") and len(title.split()) == 2:
                    section, name = title.split()[1], title
                    appendix = section if title.split()[0] == "APPENDIX" else ""
                elif appendix and LETTERED.match(title):
                    # "C. RESULTS" inside Appendix B (the IITRI report) is section B/C, not Appendix C
                    section = f"{appendix}/{LETTERED.match(title).group(1)}"
                    name = LETTERED.match(title).group(2)
                contents.append({**loc, "section": section, "title": name, "level": level})
                in_glossary = section == "2.1.1"
                in_where = False
                continue
            s = SPEC.match(para)
            if s:  # a soil specification sheet of Vol. II Appendix A: its title is the heading of the sheet
                contents.append({**loc, "section": f"A/soil {s.group(1)}", "title": para.strip(), "level": 2})
                prev = para
                continue
            e = EQ.match(para)
            if e:
                last_eq = e.group(2) or ""
                ctx = re.sub(r"\s+", " ", prev)[-160:]
                equations.append({**loc, "number": last_eq, "latex": e.group(1).strip(), "context": ctx})
                prev = para
                continue
            if WHERE.match(para):
                in_where, where_eq = True, last_eq
                rest = WHERE.sub("", para).lstrip(",: ").strip()
                if rest and DEF.match(rest):
                    para = rest
                else:
                    prev = para
                    continue
            if in_where:
                d = DEF.match(para)
                if d and "." not in d.group(1).strip("$ ")[:0]:
                    meaning = d.group(2).strip()
                    u = UNITS.search(meaning)
                    units = u.group(1) if u and re.search(r"units|[FLT]\W|[FLT]$|L\)|L⁻|\^", u.group(1)) else ""
                    if units:
                        meaning = meaning[:u.start()].strip()
                    symbols.append({**loc, "symbol": d.group(1).strip(), "meaning": meaning, "units": units, "equation": where_eq})
                    prev = para
                    continue
                if para.startswith("= "):  # a printed continuation line of the previous definition (e = V_v/V_s)
                    if symbols:
                        symbols[-1]["meaning"] += " " + para
                    continue
                d = DEF_IS.match(para)
                if d:
                    symbols.append({**loc, "symbol": d.group(1), "meaning": d.group(2).strip(), "units": "", "equation": where_eq})
                    prev = para
                    continue
                in_where = False
            if in_glossary and not para.startswith("Footnotes"):
                g = GLOSS.match(para)
                if g and len(g.group(1).split()) <= 5:
                    glossary.append({**loc, "term": g.group(1).strip(), "definition": g.group(2).strip()})
                else:
                    glossary.append({**loc, "term": "", "definition": para})
            prev = para
    return {"contents": (contents, ["source", "section", "title", "level", "pdf_page", "printed_page", "review_status"]),
            "equations": (equations, ["source", "number", "latex", "pdf_page", "printed_page", "context", "review_status"]),
            "symbols": (symbols, ["source", "symbol", "meaning", "units", "pdf_page", "printed_page", "equation", "review_status"]),
            "glossary": (glossary, ["source", "term", "definition", "pdf_page", "printed_page", "review_status"])}


def render(rows, fields):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def main(argv):
    check = "--check" in argv
    bad = []
    for d, sid in SOURCES.items():
        sdir = ROOT / "corpus" / d
        if not (sdir / "pages").exists():
            continue
        for name, (rows, fields) in build(sdir, sid).items():
            text = render(rows, fields)
            path = sdir / f"{name}.csv"
            if not rows:
                if path.exists() and not check:
                    path.unlink()
                continue
            if check:
                if not path.exists() or path.read_text(encoding="utf-8") != text:
                    bad.append(str(path.relative_to(ROOT)))
            else:
                path.write_text(text, encoding="utf-8", newline="\n")
                print(f"{path.relative_to(ROOT).as_posix()}: {len(rows)} rows")
    if check:
        print("\n".join(f"differs: {b}" for b in bad) if bad else "indexes match a fresh build")
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
