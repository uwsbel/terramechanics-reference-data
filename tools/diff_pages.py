"""Compare two independent transcriptions of report pages (docs/PAGE-TRANSCRIPTION.md, section 4).

Usage:
    python tools/diff_pages.py <dir_a> <dir_b> --labels claude,codex --out <report.md>
        [--decisions <decisions.csv>] [--canonical <out_dir>] [--batch <name>]

<dir_a> and <dir_b> hold pNNNN.md files of the same pages. The report lists, per page, header
differences and body differences (id pNNNN-dK, class number | reference | symbol | wording, both
readings with a few words of context). number, reference and symbol differences block the page;
wording differences do not. With --canonical, each page is written from reading A with the
decisions applied (use a | b | text) and review_status agreed | resolved | pending.
"""
import argparse
import csv
import difflib
import re
import sys
from pathlib import Path

REF = re.compile(r"^(Figure|Figures|Fig\.|Table|Tables|Section|Sections|Appendix|Eq\.|Equation|\(\d+-\d+\)|\(\d+,|pp?\.)", re.I)
SYM = re.compile(r"[Ͱ-Ͽ_$\\^±°≤≥≈×]")


def split(text):
    """Front matter (dict of raw strings) and body."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        return {}, text
    head = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            head[k.strip()] = v.strip()
    return head, m.group(2)


def hnorm(v):
    """A header value without the YAML quotes a transcriber may or may not put around a scalar or around
    the items of a flow list ([A] and ["A"] are the same list)."""
    v = (v or "").strip()
    if v.startswith("[") and v.endswith("]"):
        items = [x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip()]
        return "[" + ", ".join(f'"{x}"' for x in items) + "]"
    return v[1:-1] if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'" else v


def head_value(k, v):
    """Canonical header value: plain scalars unquoted, lists with quoted items, the printed page always
    quoted (it can look like a number)."""
    v = hnorm(v)
    return f'"{v}"' if k == "printed_page" else v


def norm_tokens(body):
    b = body.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    b = re.sub(r"\[\?\]", "", b)
    b = re.sub(r"\[cont\.[^\]]*\]", "", b)
    b = re.sub(r"\r\n", "\n", b)
    # a Markdown table's separator row is layout, not reading: |---|---| and | --- | --- | are the same row
    b = re.sub(r"^[ \t]*\|(?:[ \t]*:?-{3,}:?[ \t]*\|)+[ \t]*$", lambda m: "|" + "---|" * len(re.findall(r"-{3,}", m.group(0))), b, flags=re.M)
    # a table row starts on its own line; keep that break as a token so the canonical page keeps its table
    b = re.sub(r"(?<!\n)\n(?=\|)", " ↵ ", b)
    # paragraphs stay distinguishable: a blank line becomes a paragraph token
    b = re.sub(r"\n\s*\n", " ¶ ", b)
    b = re.sub(r"\s+", " ", b).strip()
    return b.split(" ")


def classify(a_tokens, b_tokens):
    # the same words with and without math delimiters are a markup difference, not a reading difference
    if [t.replace("$", "") for t in a_tokens] == [t.replace("$", "") for t in b_tokens]:
        return "markup"
    joined = " ".join(a_tokens + b_tokens)
    if re.search(r"\d", joined):
        if any(REF.match(t) for t in a_tokens + b_tokens) or re.search(r"\b(Figure|Table|Section|Eq)", joined):
            return "reference"
        return "number"
    if SYM.search(joined):
        return "symbol"
    return "wording"


def diff_page(name, ta, tb, la, lb):
    """Return (header_diffs, body_diffs) where body_diffs are dicts with id, cls, a, b, ctx, opcode."""
    ha, ba = split(ta)
    hb, bb = split(tb)
    hd = []
    for k in sorted(set(ha) | set(hb)):
        if k in ("transcriber", "review_status"):
            continue
        if hnorm(ha.get(k, "")) != hnorm(hb.get(k, "")):
            hd.append((k, ha.get(k, ""), hb.get(k, "")))
    A, B = norm_tokens(ba), norm_tokens(bb)
    sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
    diffs = []
    k = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        k += 1
        a_run, b_run = A[i1:i2], B[j1:j2]
        ctx = " ".join(A[max(0, i1 - 4):i1])
        diffs.append({"id": f"{name}-d{k}", "cls": classify(a_run, b_run), "a": " ".join(a_run), "b": " ".join(b_run),
                      "ctx": ctx, "i1": i1, "i2": i2, "j1": j1, "j2": j2})
    return hd, diffs, A, B


def apply_decisions(name, A, B, diffs, decisions):
    """Canonical token list from A with decided differences applied; returns (tokens, n_decided, n_blocking_open)."""
    out = []
    pos = 0
    decided = 0
    open_blocking = 0
    for d in diffs:
        out += A[pos:d["i1"]]
        dec = decisions.get((name, d["id"]))
        if dec:
            decided += 1
            if dec["use"] == "b":
                out += B[d["j1"]:d["j2"]]
            elif dec["use"] == "text":
                m = re.search(r"text=(.*)$", dec.get("note", ""))
                out += (m.group(1).strip().split(" ") if m else A[d["i1"]:d["i2"]])
            else:
                out += A[d["i1"]:d["i2"]]
        else:
            if d["cls"] not in ("wording", "markup"):
                open_blocking += 1
            out += A[d["i1"]:d["i2"]]
        pos = d["i2"]
    out += A[pos:]
    return out, decided, open_blocking


SYMBOL_TOKEN = re.compile(r"^([(\[]*)([A-Za-z\u0370-\u03ff]_[A-Za-z0-9]+)([)\].,;:]*)$")


def wrap_symbols(tokens):
    """A bare subscripted symbol (D_r, G_p, sigma_n) becomes $D_r$ unless it already sits inside a
    $...$ span. Protocol rule 4: math in dollars with Unicode inside, so the rendered page shows
    subscripts and a text search still finds the symbol."""
    # display math ($$...$$) and inline math ($...$) are tracked separately: a $$ token toggles display
    # mode and must not be read as two inline toggles, or symbols inside an equation get wrapped
    out, inline, display = [], False, False
    for t in tokens:
        if "$" in t:
            n_display = t.count("$$")
            n_inline = t.count("$") - 2 * n_display
            if n_display % 2 == 1:
                display = not display
            if n_inline % 2 == 1:
                inline = not inline
            out.append(t)
            continue
        m = SYMBOL_TOKEN.match(t)
        out.append(f"{m.group(1)}${m.group(2)}${m.group(3)}" if m and not inline and not display else t)
    return out


def render_body(tokens):
    text = " ".join(wrap_symbols(tokens))
    return text.replace(" \u00b6 ", "\n\n").replace(" \u21b5 ", "\n").strip() + "\n"



FIG_BLOCK = re.compile(r"^::: figure (\S+)\n(.*?)^:::\s*$", re.M | re.S)
NUM = re.compile(r"[-+]?\d+(?:\.\d+)?(?:\^-?\d+)?")
GREEK = re.compile(r"[\u0370-\u03ff]")


def figure_view(body):
    """For a figure page: (captions by figure id, numbers outside descriptions, greek symbols, text outside blocks)."""
    caps, rest = {}, body
    for m in FIG_BLOCK.finditer(body):
        fid, inner = m.group(1), m.group(2)
        for line in inner.splitlines():
            if line.startswith("caption:"):
                caps[fid] = line[len("caption:"):].strip()
        # axis lines are compared by their symbols only: a transcriber may or may not note the tick range
        rest = rest.replace(m.group(0), "\n".join(l for l in inner.splitlines() if not l.startswith(("description:", "axes:"))))
    nums = sorted(NUM.findall(re.sub(r"\by2\b", "", rest.replace("³", "^3").replace("$", " "))))
    greek = sorted(set(GREEK.findall(rest)))
    return caps, nums, greek


def diff_figure_page(name, ta, tb, la, lb):
    """Differences of a figure page: header, caption tokens per figure, numbers, symbols."""
    ha, ba = split(ta)
    hb, bb = split(tb)
    hd = [(k, ha.get(k, ""), hb.get(k, "")) for k in sorted(set(ha) | set(hb))
          if k not in ("transcriber", "review_status") and hnorm(ha.get(k, "")) != hnorm(hb.get(k, ""))]
    ca, na, ga = figure_view(ba)
    cb, nb, gb = figure_view(bb)
    diffs, k = [], 0
    for fid in sorted(set(ca) | set(cb)):
        A, B = norm_tokens(ca.get(fid, "")), norm_tokens(cb.get(fid, ""))
        sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            k += 1
            diffs.append({"id": f"{name}-d{k}", "cls": classify(A[i1:i2], B[j1:j2]), "a": " ".join(A[i1:i2]), "b": " ".join(B[j1:j2]),
                          "ctx": f"caption {fid}: " + " ".join(A[max(0, i1 - 3):i1])})
    from collections import Counter
    onlya, onlyb = Counter(na) - Counter(nb), Counter(nb) - Counter(na)
    if onlya or onlyb:
        k += 1
        diffs.append({"id": f"{name}-d{k}", "cls": "number", "a": " ".join(sorted(onlya.elements())), "b": " ".join(sorted(onlyb.elements())),
                      "ctx": "numbers printed on the page (outside descriptions), present in one reading only"})
    if set(ga) != set(gb):
        k += 1
        diffs.append({"id": f"{name}-d{k}", "cls": "symbol", "a": " ".join(sorted(set(ga) - set(gb))), "b": " ".join(sorted(set(gb) - set(ga))),
                      "ctx": "Greek symbols present in one reading only"})
    return hd, diffs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--labels", default="A,B")
    ap.add_argument("--out")
    ap.add_argument("--decisions")
    ap.add_argument("--canonical")
    ap.add_argument("--batch", default="")
    ap.add_argument("--canonical-from", default="a", choices=["a", "b"],
                    help="which reading the canonical page is written from (figure pages: the one whose block layout follows the protocol)")
    a = ap.parse_args()
    la, lb = a.labels.split(",")
    da, db = Path(a.a), Path(a.b)
    names = sorted({p.stem for p in da.glob("p[0-9]*.md")} | {p.stem for p in db.glob("p[0-9]*.md")})
    decisions = {}
    if a.decisions:
        with Path(a.decisions).open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                decisions[(r["page"], r["diff_id"])] = r
    rep = [f"# Page diff: {la} vs {lb}", "", f"Submissions: `{a.a}` ({la}), `{a.b}` ({lb}).", ""]
    totals = {"pages": 0, "agreed": 0, "resolved": 0, "pending": 0, "number": 0, "reference": 0, "symbol": 0, "wording": 0, "markup": 0, "header": 0}
    exit_code = 0
    for name in names:
        pa, pb = da / f"{name}.md", db / f"{name}.md"
        rep.append(f"## {name}")
        rep.append("")
        if not pa.exists() or not pb.exists():
            rep.append(f"Only in {la if pa.exists() else lb}.")
            rep.append("")
            exit_code = 1
            continue
        totals["pages"] += 1
        ta, tb = pa.read_text(encoding="utf-8"), pb.read_text(encoding="utf-8")
        is_fig = bool(FIG_BLOCK.search(ta) or FIG_BLOCK.search(tb))
        if is_fig:
            hd, diffs = diff_figure_page(name, ta, tb, la, lb)
            A = B = None
        else:
            hd, diffs, A, B = diff_page(name, ta, tb, la, lb)
        totals["header"] += len(hd)
        for d in diffs:
            totals[d["cls"]] += 1
        if hd:
            rep.append("Header differences:")
            rep.append("")
            rep += [f"- `{k}`: {la} `{va}` | {lb} `{vb}`" for k, va, vb in hd]
            rep.append("")
        if diffs:
            rep.append(f"| id | class | after | {la} | {lb} | decision |")
            rep.append("|---|---|---|---|---|---|")
            for d in diffs:
                dec = decisions.get((name, d["id"]))
                dtxt = f"{dec['use']}: {dec.get('note', '')}" if dec else ""
                cell = lambda s: (s or "(nothing)").replace("|", "\\|").replace("¶", "[paragraph break]")
                rep.append(f"| {d['id']} | {d['cls']} | ...{cell(d['ctx'])} | {cell(d['a'])} | {cell(d['b'])} | {dtxt} |")
            rep.append("")
        if is_fig:
            decided = sum(1 for d in diffs if (name, d["id"]) in decisions)
            open_blocking = sum(1 for d in diffs if d["cls"] not in ("wording", "markup") and (name, d["id"]) not in decisions)
            # a decision row "<page>,<page>-canonical,a|b,note" picks the reading this one page is written from
            page_dec = decisions.get((name, f"{name}-canonical"))
            page_from = page_dec["use"] if page_dec and page_dec["use"] in ("a", "b") else a.canonical_from
            src_text = tb if page_from == "b" else ta
            tokens = None
        else:
            tokens, decided, open_blocking = apply_decisions(name, A, B, diffs, decisions)
        if not diffs and not hd:
            status = "agreed"
        elif open_blocking or hd and not all((name, f"{name}-h{k}") in decisions for k, _ in enumerate(hd)):
            status = "pending"
        else:
            status = "resolved"
        totals[status] += 1
        n_block = sum(1 for d in diffs if d["cls"] not in ("wording", "markup"))
        rep.append(f"{'Figure page (caption, numbers, symbols compared; descriptions ignored). ' if is_fig else ''}"
                   f"Body differences: {len(diffs)} ({n_block} blocking, {len(diffs) - n_block} wording or markup); decided {decided}; status **{status}**.")
        rep.append("")
        if status == "pending":
            exit_code = 1
        if a.canonical:
            if is_fig:
                ha, body_text = split(src_text)
                for d in diffs:
                    dec = decisions.get((name, d["id"]))
                    if not dec:
                        continue
                    mine, other = (d["b"], d["a"]) if page_from == "b" else (d["a"], d["b"])
                    if dec["use"] == "text":
                        m = re.search(r"text=(.*)$", dec.get("note", ""))
                        new = m.group(1).strip() if m else None
                    elif dec["use"] in ("a", "b") and dec["use"] != page_from:
                        # a figure page is written whole from one reading, so a cell decided for the other
                        # reading must be swapped in here, or the decision is recorded but never applied
                        # (found in pages-vol2-ab-b2, PDF 31). An insertion (mine empty) cannot be placed.
                        new = other.strip()
                    else:
                        new = None
                    if new is not None and mine.strip() and (d["cls"] != "number" or " " not in mine.strip()):
                        body_text = body_text.replace(mine.strip(), new, 1)
                # recorded substitutions settle a cell neither reading has right: "replace: OLD => NEW ;; OLD2 => NEW2"
                if page_dec:
                    m = re.search(r"replace:\s*(.*)$", page_dec.get("note", ""))
                    for pair in (m.group(1).split(";;") if m else []):
                        old, _, new = pair.partition("=>")
                        if old.strip() and old.strip() in body_text:
                            body_text = body_text.replace(old.strip(), new.strip(), 1)
            else:
                ha, _ = split(ta)
            head = dict(ha)
            # header decisions: the header above comes from one reading, so a field decided for the other
            # reading is set here (found 2026-10-08: PDF 115's sections and PDF 23's page label had been
            # recorded as decisions and never applied)
            for k, (key, va, vb) in enumerate(hd):
                hdec = decisions.get((name, f"{name}-h{k}"))
                if hdec and hdec["use"] in ("a", "b"):
                    head[key] = va if hdec["use"] == "a" else vb
            head.pop("transcriber", None)
            head["transcribers"] = f"[{la}, {lb}]"
            head["review_status"] = status
            if a.batch:
                head["batch"] = a.batch
            head["differences"] = str(len(diffs))
            out = Path(a.canonical) / f"{name}.md"
            out.parent.mkdir(parents=True, exist_ok=True)
            body_out = render_body(tokens) if tokens is not None else body_text.rstrip("\n") + "\n"
            out.write_text("---\n" + "\n".join(f"{k}: {head_value(k, v)}" for k, v in head.items()) + "\n---\n" + body_out, encoding="utf-8", newline="\n")
    rep.insert(4, f"Pages {totals['pages']}: agreed {totals['agreed']}, resolved {totals['resolved']}, pending {totals['pending']}. "
                  f"Differences: number {totals['number']}, reference {totals['reference']}, symbol {totals['symbol']}, wording {totals['wording']}, markup {totals['markup']}; "
                  f"header fields {totals['header']}.")
    rep.insert(5, "")
    text = "\n".join(rep) + "\n"
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8", newline="\n")
    else:
        print(text)
    print(rep[4])
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
