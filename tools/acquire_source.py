"""Download a source into nasa-reports/<source_id>/, checksum it, and mark it acquired in the register.

Usage:
    python tools/acquire_source.py <source_id> <url> [<url> ...] [--crawl] [--register sources/register.csv]
                                   [--date 2026-10-08]

Each URL is saved under nasa-reports/<source_id>/ keeping the file name from the URL. With --crawl,
a URL ending in "/" is treated as a directory listing (PDS style): every link below that prefix is
fetched recursively, keeping the relative path. Downloaded files are untrusted data; this tool only
writes them and never opens them.

The register row for <source_id> is updated in place: status `acquired`, `local_file` (the folder,
or the file when there is one), `sha256` (one hex digest per file, "name:digest" joined by "; "
when several), `pages` (PDF page count via pdfinfo, or the file count), `access_date`. Nothing
else in the row changes. The row must already exist (promote the lead first).
"""
import argparse
import csv
import hashlib
import html.parser
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
# pdfinfo (Poppler, or the copy MiKTeX installs): the PDFINFO environment variable, else the one on PATH, else MiKTeX's
# per-user install; no machine path written here, so the tool runs as it is from the public release
PDFINFO = (os.environ.get("PDFINFO") or shutil.which("pdfinfo")
           or str(Path.home() / "AppData" / "Local" / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64" / "pdfinfo.exe"))
# A generic client name; whoever runs the tool may add a contact of their own through ACQUIRE_CONTACT (an archive that
# asks automated clients for one). No address is written here: the tool ships in the public release.
UA = {"User-Agent": "terramechanics-reference-data acquisition script"
                    + (f" ({os.environ['ACQUIRE_CONTACT']})" if os.environ.get("ACQUIRE_CONTACT") else "")}


class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    self.hrefs.append(v)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def crawl(url: str, prefix: str, out: Path, saved: list, seen=None) -> None:
    seen = set() if seen is None else seen
    if url in seen:
        return
    seen.add(url)
    page = fetch(url).decode("utf-8", errors="replace")
    p = Links()
    p.feed(page)
    for href in p.hrefs:
        full = urljoin(url, href)
        # Only descend: a link must be strictly below the page it sits on (listings carry links to
        # the parent, to sorting views and to themselves).
        if not full.startswith(url) or full == url or "?" in href or href.startswith("#") or len(full) <= len(url):
            continue
        rel = full[len(prefix):]
        if full.endswith("/"):
            crawl(full, prefix, out, saved, seen)
        else:
            dst = out / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                dst.write_bytes(fetch(full))
            saved.append(dst)
            print(f"  {rel} ({dst.stat().st_size} bytes)")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def pdf_pages(path: Path):
    try:
        out = subprocess.run([PDFINFO, str(path)], capture_output=True, text=True).stdout
        m = re.search(r"Pages:\s+(\d+)", out)
        return int(m.group(1)) if m else None
    except OSError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source_id")
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--crawl", action="store_true")
    ap.add_argument("--register", default="sources/register.csv")
    ap.add_argument("--date", required=True)
    a = ap.parse_args()

    out = ROOT / "nasa-reports" / a.source_id
    out.mkdir(parents=True, exist_ok=True)
    saved = []
    for url in a.urls:
        if a.crawl and url.endswith("/"):
            print(f"crawling {url}")
            crawl(url, url, out, saved)
        else:
            name = url.rstrip("/").split("/")[-1].split("?")[0]
            dst = out / name
            if not dst.exists():
                print(f"downloading {url}")
                dst.write_bytes(fetch(url))
            saved.append(dst)
            print(f"  {name} ({dst.stat().st_size} bytes)")
    saved = sorted(set(saved))
    if not saved:
        print("nothing downloaded", file=sys.stderr)
        return 1

    digests = {p.relative_to(out).as_posix(): sha256(p) for p in saved}
    pdfs = [p for p in saved if p.suffix.lower() == ".pdf"]
    if len(saved) == 1:
        local = saved[0].relative_to(ROOT).as_posix()
        sha = digests[saved[0].relative_to(out).as_posix()]
        pages = str(pdf_pages(saved[0]) or "")
    else:
        # Many files: the per-file digests go to a manifest in the folder and the register holds
        # the digest of the manifest, so one value still pins the whole bundle.
        local = out.relative_to(ROOT).as_posix() + "/"
        manifest = out / "SHA256SUMS.txt"
        manifest.write_text("".join(f"{v}  {k}\n" for k, v in sorted(digests.items())), encoding="utf-8", newline="\n")
        sha = f"manifest SHA256SUMS.txt ({len(digests)} files): {sha256(manifest)}"
        pages = "; ".join(f"{p.relative_to(out).as_posix()}: {pdf_pages(p)} pages" for p in pdfs) if pdfs else f"{len(saved)} files"

    reg = ROOT / a.register
    with reg.open(encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        cols, rows = rd.fieldnames, list(rd)
    hit = [r for r in rows if r["source_id"] == a.source_id]
    if not hit:
        print(f"{a.source_id} is not in the register; promote the lead first", file=sys.stderr)
        return 1
    r = hit[0]
    r.update({"status": "acquired", "local_file": local, "sha256": sha, "pages": pages, "access_date": a.date})
    order = {"acquired": 0, "screened": 1, "eligible": 1, "extracted": 1, "located": 2, "lead": 3, "not-located": 4}
    rows.sort(key=lambda x: (order.get(x["status"], 9), x["source_id"]))
    with reg.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{a.source_id}: {len(saved)} file(s) under {out.relative_to(ROOT).as_posix()}, register row set to acquired")
    return 0


if __name__ == "__main__":
    sys.exit(main())
