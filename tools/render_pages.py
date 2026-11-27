"""Render PDF pages to grayscale PNG with Ghostscript, for evidence packets and transcription.

Usage:
    python tools/render_pages.py <pdf> <out_dir> --pages 41,68,115-122 [--dpi 300] [--rotate 0|90|180|270]

Files are named pNNNN.png (4-digit 1-based PDF page). With --rotate the image is rotated after
rendering (Pillow if available, otherwise Ghostscript's -dAutoRotatePages is NOT used because it
guesses from text and misses rotated tables; we rotate explicitly and record it). A sidecar
pNNNN.json records dpi, rotation and the source file checksum so a reading can always be traced
to the exact image it was made from. Existing files are skipped unless --force.

Rendered images are regenerable and are not tracked in git (see .gitignore).
"""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

GS = "gswin64c"


def parse_pages(spec: str):
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-")
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return sorted(set(pages))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render(pdf: Path, out_dir: Path, page: int, dpi: int, rotate: int, force: bool, pdf_hash: str) -> Path:
    out = out_dir / f"p{page:04d}.png"
    if out.exists() and not force:
        return out
    args = [GS, "-q", "-dNOPAUSE", "-dBATCH", "-dSAFER", "-sDEVICE=pnggray", f"-r{dpi}",
            f"-dFirstPage={page}", f"-dLastPage={page}", f"-sOutputFile={out}"]
    if rotate:
        # Rotation is done by Ghostscript itself through the PostScript page-device Orientation
        # parameter (0, 1, 2, 3 = 0, 90, 180, 270 degrees), so no imaging library is needed. The
        # mapping to a clockwise angle was checked on Table 2-3 (PDF 41 of the 1968 report), whose
        # table reads upright with --rotate 90.
        orientation = {90: 3, 180: 2, 270: 1}[rotate]
        args += ["-c", f"<</Orientation {orientation}>> setpagedevice", "-f"]
    args.append(str(pdf))
    subprocess.run(args, check=True)
    (out_dir / f"p{page:04d}.json").write_text(json.dumps({
        "source_pdf": str(pdf), "source_sha256": pdf_hash, "pdf_page": page, "dpi": dpi,
        "rotation_deg_clockwise": rotate, "device": "pnggray", "renderer": "ghostscript"}, indent=2),
        encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("out_dir")
    ap.add_argument("--pages", required=True, help="e.g. 41,68,115-122")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--rotate", type=int, default=0, choices=[0, 90, 180, 270], help="clockwise degrees")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    pdf, out_dir = Path(args.pdf), Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_hash = sha256(pdf)
    for p in parse_pages(args.pages):
        out = render(pdf, out_dir, p, args.dpi, args.rotate, args.force, pdf_hash)
        print(f"  {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
