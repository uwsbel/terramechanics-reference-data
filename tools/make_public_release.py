"""Build the public release tree (D-034) from a commit of this private repository.

Usage:
    python tools/make_public_release.py <out_dir> --version 1.0.0 [--rev HEAD] [--render] [--allow-dirty]

The public repository (uwsbel/terramechanics-reference-data) gets a fresh tree per release, with no
history: this repository's history holds the student reviewers' names and e-mail addresses, and the
answer keys of audit waves still out. The tree is the committed files of <rev> (git archive, so nothing
uncommitted leaks), minus EXCLUDE, with each reviewer's name and initials replaced by a neutral code (R1
to R4, in the order of qa/audits/reviewers.csv) in the text files where they denote a reviewer, and in
file names. Code (*.py) and the readers' submissions (extractions/) keep their initials-like tokens: there
a two-letter token such as BR is a variable (a bottom-right corner), never a reviewer; only names are
replaced in them. A final scan fails the build if any reviewer's name, first name, last name, e-mail
address or ORCID iD is left anywhere in the tree, with one exception (Dan, 2026-11-21): a reviewer who
accepted co-authorship is named in the data set's author list, that is in CITATION.cff and in the BibTeX
the site builds from it (CITATION_FILES), in those citation forms only. The audit records keep the codes.
Three more rules since v1.0.0 (D-052, 2026-11-23):

1. The decision log is the curated one: docs/decisions-public.csv says for every decision whether it is published as it is
   or with edited text (people and logistics of the review left out), and the release's docs/decisions.csv holds id,
   date, question, options and decision, with no who or note column. A decision without a curation row fails the
   build, so a new one is published only by choice; every decision id cited anywhere in the tree must resolve.
2. Local paths are scrubbed: this repository's root becomes `<repository>` (the rest of the path kept) and any other path
   under a user folder `<local path>`, whole, in every text file, the readers' submissions included; a user path left
   anywhere fails the build, and so does a scrubbed JSON, CSV or Python file that no longer parses as it did.
3. The site's pages are generated again in the public form (tools/build_site.py generate with EXCLUDE as its private
   paths: no page for a left-out file, no link to one, the curated decisions), from the working copy, which must be
   clean and at <rev>, with no untracked file in a content folder (--allow-dirty for a trial build, recorded in
   RELEASE.json). A committed page the public form does not generate fails the build unless an exclusion explains it.
   The images under site/img come from the working copy too: regenerate them at the release commit before the build.

Writes <out_dir>/RELEASE.json (commit, date, exclusions, counts, the references public files still make to left-out
files). This repository is never modified.

With --render the site is rendered inside the tree (site/_site, ignored by git there too): the images
of this working copy's site/img (page thumbnails, plots, overlays; git-ignored, generated graphics) are
copied in, the footer names the release instead of a private revision, and the recent-changes list is
the release's CHANGELOG.md, never this repository's log (old commit subjects name the reviewers). The
rendered pages, search index included, are scanned for identities like the tree.
"""
import argparse
import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_site import read_cff  # noqa: E402
from render_site import copy_data_files  # noqa: E402

EXCLUDE = (
    "qa/audits/reviewers.csv",    # names and e-mail addresses
    "qa/audits/keys/",            # answer keys, with the seeded mistakes of waves still out
    "qa/audits/table-controls.csv",   # the same seeded mistakes for chunks of table cells, as plan chose them
    # the audit program's working files (D-052): who has which chunk and when, the returns as sent, the per-return
    # reports and the board, the sample (which points are asked, and so which are not yet), withdrawn assignments; the
    # outcomes themselves are public (qa/audits.csv, qa/audits/voided.csv)
    "qa/audits/assignments.csv", "qa/audits/returns/", "qa/audits/returns-log.csv", "qa/audits/reports/",
    "qa/audits/digests/", "qa/audits/status.md", "qa/audits/sample.csv", "qa/audits/withdrawn.csv",
    "docs/audit/EMAIL-",          # e-mails to the reviewers
    "docs/ROADMAP.md", "site/roadmap.qmd",           # the maintainers' plan and its page (D-052)
    "AGENTS.md", "site/methods/agents.qmd",          # the agent guide and its page (D-052)
    "docs/decisions-public.csv",  # the curation of the decision log; the release's docs/decisions.csv is built from it
    # While the audit runs (waves still out until its last wave, about January 2027): the program's manual and the packet
    # tool describe what the seeded attention checks look like and hold the sampling seed, and the pilot's key and its
    # dry-run answers mark the pilot's checks (Codex's review of the export, 2026-11-23). Published when the audit ends.
    "docs/audit/README.md", "tools/make_audit_packet.py",
    "qa/curves-pilot-b1/audit-packet-1-answer-key.csv", "qa/curves-pilot-b1/audit-packet-1-dan-2026-10-09.csv",
    "nasa-reports/plan-validation-chrono.md",   # the project lead's own planning notes
    # The reports from NASA's Technical Reports Server are linked, not copied (D-054, Dan, 2026-11-23): NASA asks that
    # its citation link be used instead of a full-text copy, and that copies of a withdrawn record be removed, which a
    # Zenodo record and a public history cannot do. sources/register.csv gives each one's NTRS link, local file name and
    # SHA-256. The Planetary Data System bundles (public domain) stay in.
    "nasa-reports/1968-nasa-LunarModule-SoilMechanicsStudy.pdf", "nasa-reports/volume2/",
    "nasa-reports/1970-nasa-load-analysis-report.pdf", "nasa-reports/wes-m71-10-rpt1/", "nasa-reports/wes-m71-10-rpt2/",
    "paper/",                     # notes for the data paper, unpublished
)
# Folders whose untracked files could enter a build through the working copy (rule 3): any untracked file in them makes
# the working copy dirty, like a modified tracked file (Codex's review: an untracked insight would enter a "clean" build).
CONTENT = ("data", "corpus", "docs", "insights", "site", "sources", "qa", "extractions", "tools", "schemas", "nasa-reports",
           "README.md", "CITATION.cff", "CHANGELOG.md", "LICENSE", "LICENSE-DATA.md", ".github")
TEXT = {".csv", ".md", ".json", ".qmd", ".txt", ".yml", ".yaml", ".html", ".tsv"}
# The data set's author list (Dan, 2026-11-21). Reviewers who accepted co-authorship appear by name in CITATION.cff and
# in the BibTeX the site builds from it, and nowhere else: the audit records keep the codes, so nothing in the tree ties
# a code to a person. Only these files may carry such a name, and only in a citation form (see main: `cited`).
CITATION_FILES = ("CITATION.cff", "site/downloads/index.qmd", "site/_site/downloads/index.html", "site/_site/search.json",
                  "site/.quarto/idx/downloads/index.qmd.json")   # the last: Quarto's index of the page, from a render


def decode(data):
    """A text file's content and encoding: UTF-8, or UTF-16 with its BOM (logs written by PowerShell)."""
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return data.decode("utf-16"), "utf-16"
    return data.decode("utf-8"), "utf-8"


# Local paths (rule 2): a drive, /c/ or /mnt/c/ form, then users, then the user name, with any of the separators the files
# hold (/, \, and the doubled or quadrupled backslashes of JSON and of JSON inside JSON). A path segment stops at white
# space, quotes, brackets, commas and semicolons, so a path inside a CSV field or a sentence never takes the next field.
SEP = r"(?:\\{1,4}|/)"
SEG = r"[^\\/\s\"'<>:*?|,;()\[\]`]+"
HOME_RE = re.compile(r"(?i)(?:\b[a-z]:|(?<![\w.])(?:/mnt)?/[a-z](?=/))" + SEP + r"users" + SEP + SEG)
_rest = ROOT.relative_to(Path.home()).parts if ROOT.is_relative_to(Path.home()) else ROOT.parts[1:]
ROOT_RE = re.compile(HOME_RE.pattern + SEP + SEP.join(re.escape(x) for x in _rest) + r"(?![\w-])", re.I)
# any other path under a user folder goes whole: a session folder, an installed tool's build folder, a scratch file
OTHER_RE = re.compile(HOME_RE.pattern + r"(?:" + SEP + SEG + r")*", re.I)
# the folder-name form some tools make of a path (the drive letter, two hyphens, then the path's folders joined by
# hyphens), wherever it appears
ENCODED_RE = re.compile(r"(?i)\b[a-z]--users-[\w.-]+")
# the alternatives are split across strings so that these lines do not match themselves in the scan of the tree
LEAK_RE = re.compile(r"(?i)\b[a-z]:(?:\\{1,4}|/)users(?:\\{1,4}|/)|(?<![\w.])(?:/mnt)?/c/" + "users/|\\b[a-z]-" + "-users-")
# Path forms the scrub does not rewrite, which the scan refuses so that a person looks at them (Codex's review, round 2):
# a network share or a Unix home folder at the start of a token, a URL-encoded drive or user folder, the rest of a user
# name with a space left after a scrubbed path, and the name of this lab's checkout folder.
LEAK2_RE = re.compile(r"(?:^|(?<=[\s\"'`(]))\\{2,8}[A-Za-z0-9][\w.-]*\\{1,4}[\w$.-]+"
                      r"|(?:^|(?<=[\s\"'`(]))/home/[a-z_][\w.-]*/"
                      r"|(?i:\b[a-z]%3a(?:%2f|%5c|[\\/])|%2fus" r"ers%2f|%5cus" r"ers%5c)"
                      r"|<local" + r" path>(?: [^\s\\/`'\")]+){1,3}[\\/]"
                      r"|\bWin" + r"Repos\b", re.M)
SCRUB = {".py", ".js", ".xml", ".cff", ".log", ".asc", ".tab", ".sh", ".lua", ".css", ".jsonl", ".md5"}
DECISION_RE = re.compile(r"\bD-(\d{3})\b")


def scrub(text):
    """This repository's root as <repository> (the rest of the path kept, so a reference stays readable), any other path
    under a user folder as <local path> (rule 2); the count of replacements."""
    text, a = ROOT_RE.subn("<repository>", text)
    text, b = OTHER_RE.subn("<local path>", text)
    text, c = ENCODED_RE.subn("<local path>", text)
    return text, a + b + c


def parses(text, suffix):
    """Whether a scrubbed file still parses as it did: JSON, CSV row shapes, Python. None when the type is not checked."""
    try:
        if suffix == ".json":
            json.loads(text)
            return True
        if suffix == ".csv":
            return tuple(len(r) for r in csv.reader(io.StringIO(text)))
        if suffix == ".py":
            compile(text, "<release>", "exec")
            return True
    except (ValueError, SyntaxError, csv.Error):
        return False
    return None


def curated_decisions(commit):
    """The public decision log (rule 1): every decision, as it is or with its curated text, without who and note."""
    full = list(csv.DictReader(io.StringIO(git("show", f"{commit}:docs/decisions.csv").decode("utf-8"))))
    try:   # strict: text after a closing quote is an error, not merged into the field (Codex's review, round 3)
        raw = list(csv.reader(io.StringIO(git("show", f"{commit}:docs/decisions-public.csv").decode("utf-8")), strict=True))
    except csv.Error as err:
        sys.exit(f"docs/decisions-public.csv: malformed CSV: {err}")
    head = ["id", "publish", "question", "options", "decision"]
    if not raw or raw[0] != head:
        sys.exit(f"docs/decisions-public.csv: the header must be exactly {','.join(head)}")
    short = [str(n) for n, row in enumerate(raw[1:], 2) if len(row) != len(head)]
    if short:   # a short row would read as empty fields, a long one would drop text (Codex's review, round 2)
        sys.exit(f"docs/decisions-public.csv: rows without exactly {len(head)} fields, lines {', '.join(short)}")
    cur_rows = [dict(zip(head, row)) for row in raw[1:]]
    # a doubled id would let the last row win silently (Codex's review): refused in both files
    for name, rs in (("docs/decisions.csv", full), ("docs/decisions-public.csv", cur_rows)):
        dup = sorted(i for i, n in Counter(r["id"] for r in rs).items() if n > 1)
        if dup:
            sys.exit(f"{name}: id listed more than once: {', '.join(dup)}")
    cur = {r["id"]: r for r in cur_rows}
    ids = [r["id"] for r in full]
    if set(ids) != set(cur):
        sys.exit("docs/decisions-public.csv must have one row per decision: missing "
                 + ", ".join(i for i in ids if i not in cur) + "; unknown " + ", ".join(i for i in cur if i not in ids))
    rows = []
    for r in full:
        c = cur[r["id"]]
        if c["publish"] not in ("as-is", "edited"):
            sys.exit(f"docs/decisions-public.csv: {r['id']}: publish is '{c['publish']}', not as-is or edited")
        e = c["publish"] == "edited"
        fields = ("question", "options", "decision")
        # an edited row gives every field: its public text, or "=" to keep the original (docs/DATA-ORGANIZATION.md), so a
        # field left empty by mistake can never bring back the private text (Codex's review, round 2); an edited row
        # that keeps everything, or an as-is row with text, is a mistake too
        if e and any(not c[k].strip() for k in fields):
            sys.exit(f"docs/decisions-public.csv: {r['id']} is edited but leaves a field empty (give its text, or = to keep it)")
        if e and all(c[k].strip() == "=" for k in fields):
            sys.exit(f"docs/decisions-public.csv: {r['id']} is marked edited but keeps every field")
        if not e and any(c[k].strip() for k in fields):
            sys.exit(f"docs/decisions-public.csv: {r['id']} is marked as-is but gives text")
        rows.append({"id": r["id"], "date": r["date"],
                     **{k: (c[k] if e and c[k].strip() != "=" else r[k]) for k in fields}})
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["id", "date", "question", "options", "decision"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return rows, buf.getvalue()


def public_pages(curated):
    """The site's pages in the public form (rule 3), generated from the working copy into a temporary folder."""
    import build_site
    d = build_site.load()
    missing = build_site.missing_images(d)   # the same check as build_site's own entry point (Codex's review, round 3)
    if missing:
        sys.exit(f"the image cache lacks {', '.join(missing[:8])}: regenerate it at the release commit first")
    d["decisions"] = curated
    tmp = Path(tempfile.mkdtemp(prefix="public-pages-"))
    try:
        pages = build_site.generate(tmp, d, private_paths=EXCLUDE)
        return {f"site/{rel}": (tmp / rel).read_bytes() for rel in pages}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def render(out, commit, version):
    """Render the release's site inside the tree (see the module docstring). Returns the count and a SHA-256 over the
    images copied in (each file's path and digest, in order), for RELEASE.json: the images come from the working copy,
    so the record shows which ones a candidate used, and a rebuild from images regenerated at the same commit can be
    compared with it (Codex's review of the export, round 2)."""
    site = out / "site"
    manifest = hashlib.sha256()
    n = 0
    for p in sorted((ROOT / "site" / "img").rglob("*")):
        if p.is_file():
            rel = p.relative_to(ROOT / "site" / "img").as_posix()
            t = site / "img" / rel
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, t)
            # the copy's bytes, so the record describes what was rendered even if the source changed meanwhile
            manifest.update(f"{rel}:{hashlib.sha256(t.read_bytes()).hexdigest()}\n".encode("utf-8"))
            n += 1
    (site / "_footer.html").write_text(
        f'<div class="build-footer container">Release {version} of Terramechanics Reference Data (maintainers\' '
        f"revision <code>{commit[:7]}</code>), rendered {date.today().isoformat()}. Every value traces to a source page, and "
        "each test page says how much of it a person has checked.</div>\n", encoding="utf-8")
    heads = [l[3:].strip() for l in (out / "CHANGELOG.md").read_text(encoding="utf-8").splitlines() if l.startswith("## ")]
    (site / "_changes.md").write_text("\n".join(f"- {h} (`CHANGELOG.md`)" for h in heads) + "\n", encoding="utf-8")
    r = subprocess.run(["quarto", "render", str(site)], cwd=out, shell=True)
    if r.returncode:
        sys.exit(f"quarto render failed (exit {r.returncode})")
    copy_data_files(out, site)   # from the release tree, so a linked file carries the reviewer codes, not names
    return {"files": n, "sha256": manifest.hexdigest()}


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--version", required=True, help="the release version, for example 1.0.0 (written to RELEASE.json)")
    ap.add_argument("--allow-dirty", action="store_true",
                    help="a trial build from a working copy that is not clean at --rev (recorded in RELEASE.json)")
    a = ap.parse_args()
    out = Path(a.out_dir).resolve()
    if ROOT == out or ROOT in out.parents:
        sys.exit("the release tree must be outside this repository")
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} is not empty")
    # ^{commit}: an annotated tag names a tag object, whose id is not the commit the tree comes from (Codex, 2026-11-18:
    # --rev pre-sim-split recorded the tag object 2449ae7 instead of commit 6e65a26 in RELEASE.json)
    commit = git("rev-parse", a.rev + "^{commit}").decode().strip()
    dirty = (bool(git("status", "--porcelain", "--untracked-files=all", "--", *CONTENT).strip())
             or git("rev-parse", "HEAD").decode().strip() != commit)
    if dirty and not a.allow_dirty:
        sys.exit("the site's pages are generated from the working copy: commit, and run at a clean HEAD (--rev HEAD), "
                 "or pass --allow-dirty for a trial build")
    curated, curated_csv = curated_decisions(commit)
    roster = list(csv.DictReader(io.StringIO(git("show", f"{commit}:qa/audits/reviewers.csv").decode("utf-8-sig"))))
    code = {r["initials"]: f"R{i + 1}" for i, r in enumerate(roster)}
    names = []   # (pattern, code), longest first so a full name goes before its parts
    for r in roster:
        last = r["name"].split()[-1]
        names += [(r["name"], code[r["initials"]]), (last, code[r["initials"]]), (r["first_name"], code[r["initials"]])]
    names.sort(key=lambda t: -len(t[0]))
    # case-insensitive like the final scan: a name also turns up in lower case inside a folder name (D-041's note
    # cites a repository path that starts with a reviewer's first name), and the scan then refused the whole tree
    name_re = [(re.compile(rf"\b{re.escape(n)}\b", re.I), c) for n, c in names]
    init_re = re.compile(r"\b(" + "|".join(map(re.escape, code)) + r")\b")
    forbidden = [r[k] for r in roster for k in ("name", "first_name", "email")] + [r["name"].split()[-1] for r in roster]
    forbidden += [r["orcid"] for r in roster if r.get("orcid")]   # an iD beside a code would tie the code to a person
    forbidden_re = re.compile("|".join(rf"\b{re.escape(f)}\b" for f in forbidden), re.I)
    # Reviewers the released CITATION.cff lists as authors, matched on the full name: a different spelling matches nobody,
    # and the scan then refuses the tree, the safe direction. Their names survive in CITATION_FILES only, in BibTeX's
    # "Family, Given" and in CITATION.cff's own lines; any other form, file, e-mail address or iD still fails the build.
    cited = [(a, r) for a in read_cff(git("show", f"{commit}:CITATION.cff").decode("utf-8"))[1] for r in roster
             if f"{a.get('given-names', '')} {a.get('family-names', '')}" == r["name"]]
    bib_forms = [f"{a['family-names']}, {a['given-names']}" for a, _ in cited]
    cff_lines = [re.compile(rf'(-\s+)?{k}:\s*"?{re.escape(v)}"?') for a, r in cited for k, v in
                 [("family-names", a["family-names"]), ("given-names", a["given-names"])]
                 + ([("orcid", f"https://orcid.org/{r['orcid']}")] if r.get("orcid") else [])]
    # A note such as "<first name> accepted co-authorship" comes out of the replacement with the reviewer's code in place
    # of the name, next to a CITATION.cff that names the authors, and so ties the code to a person (a draft of the 11-21
    # roadmap note did): a code within 80 characters of an authorship word fails the build too (a window, not the line: a
    # search index holds a whole page on one line).
    codes, words = "|".join(code.values()), r"(?i:co-?author|authorship|author list|orcid)"
    tie_re = re.compile(rf"\b({codes})\b.{{0,80}}{words}|{words}.{{0,80}}\b({codes})\b")

    tar = tarfile.open(fileobj=io.BytesIO(git("archive", "--format=tar", commit)))
    counts, excluded, renamed, scrubbed, broken = Counter(), Counter(), {}, Counter(), []
    out.mkdir(parents=True, exist_ok=True)
    pages = public_pages(curated)
    members = [(m.name, None) for m in tar.getmembers() if m.isfile()]
    have = {name for name, _ in members}
    members += [(rel, data) for rel, data in pages.items() if rel not in have]   # a page the committed site lacks
    dropped = [p for p, _ in members if p.startswith("site/") and p.endswith(".qmd") and p not in pages
               and not p.startswith(EXCLUDE)]
    if dropped:   # only the pages of left-out files may go (Codex's review: never a page silently)
        sys.exit("site pages the public form does not generate, and no exclusion explains: " + ", ".join(dropped[:20]))
    for path, generated in members:
        if path.startswith(EXCLUDE):
            excluded[next(e for e in EXCLUDE if path.startswith(e))] += 1
            continue
        data = generated if generated is not None else (pages.get(path) or tar.extractfile(path).read())
        if path == "docs/decisions.csv":
            data = curated_csv.encode("utf-8")
        suffix = Path(path).suffix.lower()
        if suffix in TEXT | SCRUB:
            try:
                text, enc = decode(data)
            except UnicodeDecodeError:
                text = None
            if text is not None:
                new, k = scrub(text)
                if k:
                    scrubbed[path.split("/")[0]] += k
                    before = parses(text, suffix)
                    if before not in (None, False) and parses(new, suffix) != before:
                        broken.append(path)   # the scrub changed how the file parses (a JSON value, a CSV row's fields)
                    data = new.encode(enc)
        reviewer_text = Path(path).suffix.lower() in TEXT and not path.startswith("extractions/")
        if Path(path).suffix.lower() in TEXT | {".py"}:
            (text, enc), n = decode(data), 0
            held = bib_forms if path in CITATION_FILES else []   # the author list's names, set aside while codes go in
            for i, f in enumerate(held):
                text = text.replace(f, f"\0{i}\0")
            for rx, c in name_re:
                text, k = rx.subn(c, text)
                n += k
            if reviewer_text:
                text, k = init_re.subn(lambda mo: code[mo.group(1)], text)
                n += k
            for i, f in enumerate(held):
                text = text.replace(f"\0{i}\0", f)
            if n:
                counts[path] = n
            data = text.encode(enc)
        dest = path
        if path.startswith("qa/audits/"):   # chunk files named by initials: checklist-BR-A.csv, ...-accept-SW-C.md
            dest = "/".join(init_re.sub(lambda mo: code[mo.group(1)], part) for part in path.split("/"))
            if dest != path:
                renamed[path] = dest
        target = out / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    images = render(out, commit, a.version) if a.render else None
    leaks, cited_ids, private_refs = [f"{p}: the path scrub changed how it parses" for p in broken], Counter(), {}
    public_ids = {r["id"] for r in curated}
    for p in out.rglob("*"):
        if p.is_file():
            rel = p.relative_to(out).as_posix()
            if forbidden_re.search(rel):
                leaks.append(f"{rel}: file name")
            if p.suffix.lower() in TEXT | SCRUB | {".py"}:
                try:
                    body = decode(p.read_bytes())[0]
                except UnicodeDecodeError:
                    continue
                for mo in DECISION_RE.finditer(body):
                    if f"D-{mo.group(1)}" not in public_ids:
                        cited_ids[f"D-{mo.group(1)} in {rel}"] += 1
                if not rel.startswith("tools/"):
                    for e in EXCLUDE:
                        if e in body:
                            private_refs.setdefault(e, []).append(rel)
                for i, line in enumerate(body.splitlines(), 1):
                    if LEAK_RE.search(line) or LEAK2_RE.search(line):
                        leaks.append(f"{rel}:{i}: a local path: {line.strip()[:100]}")
                    seen = line
                    if rel in CITATION_FILES:
                        for f in bib_forms:
                            seen = seen.replace(f, "")
                        if rel == "CITATION.cff" and any(rx.fullmatch(line.strip()) for rx in cff_lines):
                            seen = ""
                    if forbidden_re.search(seen):
                        leaks.append(f"{rel}:{i}: {line.strip()[:120]}")
                    elif tie_re.search(line):
                        leaks.append(f"{rel}:{i}: a reviewer code beside authorship: {line.strip()[:100]}")
    leaks += [f"{k}: a decision the public log does not hold" for k in sorted(cited_ids)]
    if leaks:
        shutil.rmtree(out)
        sys.exit("reviewer identities, local paths or unresolved decisions left in the tree (nothing written):\n"
                 + "\n".join(leaks[:50]))
    rel = {"commit": commit, "built": date.today().isoformat(), "tool": "tools/make_public_release.py",
           "version": a.version, "rendered": a.render, "site_images": images,
           "excluded": dict(excluded), "reviewer_codes": sorted(code.values()), "reviewers_named_as_authors": len(cited),
           "renamed_files": len(renamed),
           "files_with_replacements": len(counts),
           "dirty_working_copy": dirty, "local_paths_scrubbed": dict(scrubbed),
           "decisions_published": len(curated),
           # public files that still name a left-out file (historical briefs and notes, which are not edited), each with the
           # files that do, so a maintainer can tell a historical mention from a broken link; the README says what the
           # release leaves out and why
           "files_naming_a_left_out_file": {e: sorted(fs) for e, fs in sorted(private_refs.items(), key=lambda kv: -len(kv[1]))}}
    (out / "RELEASE.json").write_text(json.dumps(rel, indent=2) + "\n", encoding="utf-8")
    print(f"release tree of {commit[:7]} in {out}: {sum(1 for _ in out.rglob('*') if _.is_file())} files; "
          f"excluded {dict(excluded)}; {len(counts)} files with reviewer codes, {len(renamed)} renamed; "
          f"{sum(scrubbed.values())} local paths scrubbed; {len(curated)} decisions; no identities or local paths left"
          + ("; TRIAL BUILD from a working copy that is not clean at --rev" if dirty else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
