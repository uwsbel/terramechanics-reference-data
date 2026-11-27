"""Render the site: regenerate pages, write the render-time footer and change list, run quarto.

Usage:
    python tools/render_site.py            # build_site.py, then quarto render site
    python tools/render_site.py --preview  # same, then quarto preview site

The footer (commit, dirty flag, render date) and the recent-changes list come from git at render
time and are written to site/_footer.html and site/_changes.md, both ignored by git, so the
committed pages stay deterministic (see tools/build_site.py).
"""

import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_site import DOWNLOAD_FILES  # noqa: E402


def copy_data_files(src, site):
    """Copy the data files the pages link to into <site>/_site/files/, at their repository paths: every record's CSV and
    JSON, and the files of the Downloads page. The committed sources hold only the links (the repository file is the one
    copy of a number). Used here and by tools/make_public_release.py, with <src> the tree the site was rendered from."""
    files = [p for p in (src / "data" / "experiments").glob("*/*") if p.suffix in (".csv", ".json")]
    missing = [f for f in DOWNLOAD_FILES if not (src / f).is_file()]
    if missing:
        sys.exit(f"listed on the Downloads page but not in {src}: {', '.join(missing)}")
    for p in files + [src / f for f in DOWNLOAD_FILES]:
        dst = site / "_site" / "files" / p.relative_to(src)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)
    return len(files) + len(DOWNLOAD_FILES)


def git(*args):
    # UTF-8, not the console's code page: a commit subject with "ρc²" (109885c) stopped the render under cp1252
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True).stdout.strip()


def main(argv):
    t0 = time.time()
    subprocess.run([sys.executable, str(ROOT / "tools" / "build_site.py")], check=True)
    commit = git("rev-parse", "--short", "HEAD")
    dirty = bool(git("status", "--porcelain", "--untracked-files=no"))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    (SITE / "_footer.html").write_text(
        '<div class="build-footer container">Repository revision <code>' + commit + ("</code> (with uncommitted changes)" if dirty else "</code>")
        + ", rendered " + now + ". Private working copy; not released. Every value traces to a source page, and "
        "each test page says how much of it a person has checked.</div>\n", encoding="utf-8")
    log = git("log", "--date=short", "--pretty=format:%ad %h %s", "-n", "12").splitlines()
    (SITE / "_changes.md").write_text("\n".join(f"- {l}" for l in log) + "\n", encoding="utf-8")
    cmd = ["quarto", "preview" if "--preview" in argv else "render", str(SITE)]
    r = subprocess.run(cmd, cwd=ROOT, shell=True)
    n = copy_data_files(ROOT, SITE)
    print(f"render finished in {time.time() - t0:.1f} s (exit {r.returncode}); {n} data files copied into _site/files")
    return r.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
