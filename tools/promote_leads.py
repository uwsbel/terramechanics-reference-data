"""Promote screened leads from a screening batch into sources/register.csv.

Usage:
    python tools/promote_leads.py <screened.csv> <leads.csv> <register.csv> --agent codex --date 2026-10-07

Each screened lead becomes (or replaces) a register row keyed by source_id = lead_id. The row's
identity fields (title, authors, report numbers, year, URLs) come from the screening, which
confirmed or corrected them against the archive record; the relation to the Bendix study comes
from the lead; the screening verdict, setup recoverability and text-layer assessment go to notes.

Status rule: a screened lead is `located` (identity confirmed, file not in hand). It becomes
`acquired` only when the file is downloaded and checksummed, which this tool does not do. The
screening verdict (acquire, acquire-with-caveat, lead-only) is recorded in notes so the next step
(download) can be chosen from the register alone. Existing rows whose source_id is not in the
screening batch are kept unchanged. Output is deterministic: rows sorted by status group then id.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

REGISTER_COLS = [
    "source_id", "status", "title", "authors", "organization", "contract", "report_numbers",
    "date", "ntrs_id", "url", "local_file", "sha256", "pages", "rights_evidence", "access_date",
    "holds", "relations", "notes",
]
STATUS_ORDER = {"acquired": 0, "screened": 1, "eligible": 1, "extracted": 1, "located": 2,
                "lead": 3, "not-located": 4}


def ntrs_ids(text: str) -> str:
    ids = re.findall(r"ntrs\.nasa\.gov/(?:api/)?citations/(\d{11})", text or "")
    seen = []
    for i in ids:
        if i not in seen:
            seen.append(i)
    return "; ".join(seen)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("screened")
    ap.add_argument("leads")
    ap.add_argument("register")
    ap.add_argument("--agent", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--model", default="gpt-6-astra")
    a = ap.parse_args()

    screened = list(csv.DictReader(open(a.screened, encoding="utf-8", newline="")))
    leads = {r["lead_id"]: r for r in csv.DictReader(open(a.leads, encoding="utf-8", newline=""))}
    reg_path = Path(a.register)
    existing = list(csv.DictReader(open(reg_path, encoding="utf-8", newline=""))) if reg_path.exists() else []
    rows = {r["source_id"]: r for r in existing}

    for s in screened:
        lid = s["lead_id"]
        lead = leads.get(lid)
        if lead is None:
            print(f"warning: {lid} not in leads.csv", file=sys.stderr)
            lead = {}
        urls = s.get("url_used", "")
        holds = "; ".join(x for x in [
            s.get("quantities_measured", ""),
            f"data form: {s.get('data_form', '')}" if s.get("data_form") else "",
            f"tests: {s.get('approx_tests', '')}" if s.get("approx_tests") else "",
            f"data pages: {s.get('data_pages', '')}" if s.get("data_pages") else "",
        ] if x)
        rights = s.get("rights_statement_quoted", "")
        if s.get("rights_assessment"):
            rights = f"{rights} ({s['rights_assessment']})" if rights else s["rights_assessment"]
        notes = (f"Screened {a.date} by {a.agent} ({a.model}), text and metadata only: "
                 f"verdict {s.get('verdict', '')}; setup recoverability {s.get('setup_recoverability', '')}; "
                 f"text layer: {s.get('text_layer', '')}. {s.get('notes', '')}").strip()
        if s.get("download_url"):
            notes += f" Download: {s['download_url']}"
        if lead.get("found_by"):
            notes += f" Lead found by {lead['found_by']}."
        # A row already acquired (tools/acquire_source.py) keeps its file, checksum, page count and
        # status; the screening only refreshes the descriptive fields.
        keep = {k: rows[lid][k] for k in ("status", "local_file", "sha256", "pages", "access_date")} \
            if lid in rows and rows[lid].get("status") == "acquired" else {}
        rows[lid] = {
            "source_id": lid,
            "status": "located",
            "title": s.get("confirmed_title", "") or lead.get("title", ""),
            "authors": s.get("confirmed_authors", "") or lead.get("authors", ""),
            "organization": "",
            "contract": "",
            "report_numbers": s.get("report_or_doi", "") or lead.get("report_or_doi", ""),
            "date": s.get("confirmed_year", "") or lead.get("year", ""),
            "ntrs_id": ntrs_ids(urls + " " + s.get("download_url", "")),
            "url": urls,
            "local_file": "",
            "sha256": "",
            "pages": s.get("pages_or_size", ""),
            "rights_evidence": rights,
            "access_date": a.date,
            "holds": holds,
            "relations": lead.get("relation_to_bendix", ""),
            "notes": notes,
        }
        rows[lid].update(keep)

    out = sorted(rows.values(), key=lambda r: (STATUS_ORDER.get(r["status"], 9), r["source_id"]))
    with open(reg_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=REGISTER_COLS, lineterminator="\n")
        w.writeheader()
        for r in out:
            w.writerow({c: r.get(c, "") for c in REGISTER_COLS})
    print(f"register: {len(out)} rows ({len(screened)} from this screening batch)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
