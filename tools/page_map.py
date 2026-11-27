"""Build a PDF-page to printed-page-label map for a scanned report.

Usage:
    python tools/page_map.py nasa-reports/1968-nasa-LunarModule-SoilMechanicsStudy.pdf corpus/1968/page-map.csv

For every PDF page, the existing OCR text layer is read with pdftotext and the printed page
label is looked for: a section-style label such as "2-35" or "4-66", a roman numeral front-matter
label such as "vii", or a plain number such as "137". The OCR layers in these reports are poor, so
the label is taken only when it appears as a short standalone token near the top or bottom of the
page text; otherwise the row says "unknown" and a later pass (or a person) fills it in. Appendix
headings are also recorded when they appear.

If a file named page-map-corrections.csv sits next to the output (columns pdf_page,
printed_label, note), its labels are applied last: a corrected page gets that printed label in
both printed_label and inferred_label with label_source "corrected". Corrections record labels
read from the page image by a person or agent where the OCR and the per-section inference both
fail, for example where a scan is bound out of order (Volume II, PDF 147 to 149) or where a
reproduced report keeps its own page numbers (Volume II, Appendix B).

Output CSV columns: pdf_page, printed_label, label_source, inferred_label, appendix_heading
"""

import csv
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Poppler's tools: an environment variable, else PATH, else the copies Git for Windows and MiKTeX install; no user's
# folder written here, so the tool runs as it is from the public release
PDFTOTEXT = (os.environ.get("PDFTOTEXT") or shutil.which("pdftotext") or r"C:\Program Files\Git\mingw64\bin\pdftotext.exe")
PDFINFO = (os.environ.get("PDFINFO") or shutil.which("pdfinfo")
           or str(Path.home() / "AppData" / "Local" / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64" / "pdfinfo.exe"))

# Section-style labels: "2-35" in the body volumes, "A-5" or "C-12" in appendix volumes.
SECTION_LABEL = re.compile(r"^\s*([1-9A-H]-\d{1,3})\s*$")
ROMAN_LABEL = re.compile(r"^\s*([ivxl]{1,6})\s*$")
PLAIN_LABEL = re.compile(r"^\s*(\d{1,3})\s*$")
APPENDIX = re.compile(r"APPENDIX\s+([A-H])\b")


def page_count(pdf: Path) -> int:
    out = subprocess.run([PDFINFO, str(pdf)], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    if not m:
        raise SystemExit(f"pdfinfo could not read the page count of {pdf}")
    return int(m.group(1))


def page_text(pdf: Path, n: int) -> str:
    out = subprocess.run([PDFTOTEXT, "-f", str(n), "-l", str(n), "-layout", str(pdf), "-"],
                         capture_output=True, text=True, errors="replace")
    return out.stdout


def find_label(text: str):
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return "unknown", "blank-ocr"
    # Page labels sit in the first few or last few non-empty lines.
    candidates = lines[:4] + lines[-4:]
    for where, group in (("bottom", reversed(lines[-4:])), ("top", lines[:4])):
        for line in group:
            # The label may share a line with noise; test each whitespace token.
            for tok in line.split():
                if SECTION_LABEL.match(tok):
                    return tok, f"section-{where}"
            for tok in line.split():
                if ROMAN_LABEL.match(tok) and len(line.split()) <= 2:
                    return tok, f"roman-{where}"
            if PLAIN_LABEL.match(line):
                return line.strip(), f"plain-{where}"
    return "unknown", "no-match"


def main(pdf_path: str, out_path: str) -> None:
    pdf = Path(pdf_path)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    n_pages = page_count(pdf)
    rows = []
    for n in range(1, n_pages + 1):
        text = page_text(pdf, n)
        label, source = find_label(text)
        app = APPENDIX.search(text)
        rows.append({"pdf_page": n, "printed_label": label, "label_source": source,
                     "appendix_heading": f"APPENDIX {app.group(1)}" if app else ""})
    infer_section_labels(rows)
    apply_corrections(rows, out.parent / "page-map-corrections.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["pdf_page", "printed_label", "label_source",
                                          "inferred_label", "appendix_heading"])
        w.writeheader()
        w.writerows(rows)
    known = sum(1 for r in rows if r["printed_label"] != "unknown")
    inferred = sum(1 for r in rows if r["inferred_label"] not in ("", "unknown"))
    print(f"{pdf.name}: {n_pages} pages, {known} labels recognised, "
          f"{inferred} labels after inference, written to {out}")


def apply_corrections(rows, path: Path) -> None:
    """Overlay labels read from the page images (see the module docstring)."""
    if not path.exists():
        return
    with path.open(encoding="utf-8-sig", newline="") as f:
        fixes = {int(r["pdf_page"]): r["printed_label"].strip() for r in csv.DictReader(f)}
    for r in rows:
        p = int(r["pdf_page"])
        if p in fixes:
            r["printed_label"] = r["inferred_label"] = fixes[p]
            r["label_source"] = "corrected"


def infer_section_labels(rows) -> None:
    """Fill `inferred_label` for every row using per-section page offsets.

    Within a section the printed number advances one per PDF page, so pdf_page minus the printed
    number is a constant offset per section. The modal offset over the recognised labels of each
    section is taken (OCR misreads are outvoted), and a page with no recognised label is assigned
    to the section whose recognised labels surround it. Pages before the first section keep their
    roman or plain label; pages between sections that cannot be placed stay "unknown".
    """
    import collections
    offsets = collections.defaultdict(collections.Counter)
    section_of = {}
    label_re = re.compile(r"^([1-9A-H])-(\d+)$")
    for r in rows:
        m = label_re.match(r["printed_label"])
        if m:
            sec, num = m.group(1), int(m.group(2))
            offsets[sec][int(r["pdf_page"]) - num] += 1
            section_of[int(r["pdf_page"])] = sec
    modal = {sec: c.most_common(1)[0][0] for sec, c in offsets.items()}
    # Drop recognised labels whose offset disagrees with the section's modal offset: OCR misreads.
    for r in rows:
        m = label_re.match(r["printed_label"])
        if m and int(r["pdf_page"]) - int(m.group(2)) != modal[m.group(1)]:
            section_of.pop(int(r["pdf_page"]), None)
    known_pages = sorted(section_of)
    for r in rows:
        p = int(r["pdf_page"])
        if p in section_of:
            sec = section_of[p]
            r["inferred_label"] = f"{sec}-{p - modal[sec]}"
            continue
        before = [q for q in known_pages if q < p]
        after = [q for q in known_pages if q > p]
        if before and after and section_of[before[-1]] == section_of[after[0]]:
            sec = section_of[before[-1]]
            r["inferred_label"] = f"{sec}-{p - modal[sec]}"
        elif r["printed_label"] != "unknown" and not re.match(r"^[1-9A-H]-", r["printed_label"]):
            r["inferred_label"] = r["printed_label"]
        else:
            r["inferred_label"] = "unknown"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
