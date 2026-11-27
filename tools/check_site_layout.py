"""Visit the rendered site in a headless browser and check the layout of every table (2026-11-19; Dan asked for a
step that visits the pages and makes sure the tables look right, after a squeezed soils table and a wide table
running under the page's table of contents).

    python tools/check_site_layout.py [--pages GLOB ...] [--widths 1280 390] [--shots] [--batch 40]

Serves site/_site (render it first: python tools/render_site.py) on a local port and opens a check page in headless
Microsoft Edge (Chrome as a fallback), with a profile of its own under work/site-check/, never the user's. The
check page loads each site page into a frame of each width and measures every table:

  toc-overlap  the table's visible box crosses the page's table of contents (the "On this page" column): side by
               side for a column that stays in view as the page scrolls, as Quarto's does; beside it otherwise
  overflow     the table's visible box reaches past the text column
  unwrapped    the table is wider than the text column and no box around it scrolls
  clipped      the table is wider than the nearest box that clips it, and that box does not scroll
  squeezed     a cell narrower than 7 em (about 110 px) whose text wraps to 6 lines or more
  page-scroll  the page itself scrolls sideways at that width (the widest element is named)
  no-content   the page has no main column, or it is empty (it failed to load or render)

Writes work/site-check/layout.csv (page, width, table, problem, detail), prints a summary and exits 1 on any
problem. With --shots it also takes a screenshot of one page of each kind (one per folder and one per test type)
at each width, into work/site-check/shots/, to be looked at by eye: the measurements catch overlap and squeezing,
not every table that reads badly. Uses only the standard library and the browser already on the machine.
"""
import argparse
import csv
import functools
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site" / "_site"
OUT = ROOT / "work" / "site-check"
BROWSERS = [Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
            Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
            Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")]

CHECK_PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>layout check</title></head><body>
<pre id="out">pending</pre>
<script>
const PAGES = %(pages)s, WIDTHS = %(widths)s;
function clipped(el) {
  // the part of an element that is visible: its box cut by every ancestor that clips or scrolls sideways
  const r = el.getBoundingClientRect(); let L = r.left, R = r.right;
  for (let a = el.parentElement; a; a = a.parentElement) {
    const ox = getComputedStyle(a).overflowX;
    if (ox !== "visible") { const q = a.getBoundingClientRect(); L = Math.max(L, q.left); R = Math.min(R, q.right); }
  }
  return {L, R, W: r.width};
}
function clipBox(el, stop) {
  // the nearest box inside the main column that clips the element sideways (null if none)
  for (let a = el.parentElement; a && a !== stop; a = a.parentElement)
    if (getComputedStyle(a).overflowX !== "visible") return a;
  return null;
}
function measure(doc, page, w, out) {
  const win = doc.defaultView;
  const main = doc.querySelector("main");
  if (!main || (main.textContent || "").trim().length < 40) {   // a page that failed to load or render (a 404 has no main)
    out.push([page, w, "", "no-content", "the page has no main column, or it is empty"]);
    return;
  }
  const mr = main.getBoundingClientRect();
  const toc = doc.querySelector("#quarto-margin-sidebar");
  const tr = toc && win.getComputedStyle(toc).display !== "none" && toc.getBoundingClientRect().width > 0
             && toc.querySelector("nav") ? toc.getBoundingClientRect() : null;
  // the contents column stays in view as the page scrolls (sticky), so a table to its side meets it at some scroll
  // position whatever its height on the page; a column that does not stay in view only meets tables beside it
  const tocSticky = tr && [toc, toc.querySelector("nav")].filter(Boolean)
                              .some(e => ["sticky", "fixed"].includes(win.getComputedStyle(e).position));
  if (doc.documentElement.scrollWidth > w + 1) {
    // name the element that reaches farthest right, outside any box that clips or scrolls
    let far = null;
    doc.querySelectorAll("body *").forEach(e => {
      const v = clipped(e);
      if (v.R > w + 1 && (!far || v.R > far[0])) far = [v.R, e];
    });
    const who = far ? far[1].tagName.toLowerCase() + (far[1].className ? "." + String(far[1].className).split(" ")[0] : "")
                      + ": " + far[1].textContent.trim().slice(0, 50) : "";
    out.push([page, w, "", "page-scroll", "page width " + doc.documentElement.scrollWidth + " px; widest: " + who]);
  }
  doc.querySelectorAll("main table").forEach((t, i) => {
    const v = clipped(t);
    const tb = t.getBoundingClientRect();
    if (tr && v.R > tr.left + 1 && v.L < tr.right && (tocSticky || (tb.bottom > tr.top && tb.top < tr.bottom)))
      out.push([page, w, i + 1, "toc-overlap", "table reaches " + Math.round(v.R) + " px, contents start at " + Math.round(tr.left)]);
    else if (v.R > mr.right + 2)
      out.push([page, w, i + 1, "overflow", "table reaches " + Math.round(v.R) + " px, text column ends at " + Math.round(mr.right)]);
    // the nearest clipping box must scroll if the table is wider than it: a farther scrolling box does not reach
    // columns a nearer `overflow: hidden` box cuts off; with no clipping box, the table must fit the column
    // (Codex's review, 2026-11-19)
    const cb = clipBox(t, main), tw = tb.width;
    if (cb) {
      const ox = win.getComputedStyle(cb).overflowX;
      if (tw > cb.clientWidth + 1 && ox !== "auto" && ox !== "scroll")
        out.push([page, w, i + 1, "clipped", "table " + Math.round(tw) + " px wide in a box of " + cb.clientWidth + " px that does not scroll"]);
    } else if (tw > mr.width + 2)
      out.push([page, w, i + 1, "unwrapped", "table " + Math.round(tw) + " px wide, column " + Math.round(mr.width)]);
    let worst = null;
    t.querySelectorAll("td, th").forEach(c => {
      const cs = win.getComputedStyle(c), fs = parseFloat(cs.fontSize) || 16;
      const lh = parseFloat(cs.lineHeight) || fs * 1.5, r = c.getBoundingClientRect();
      // the height of the cell's own text, not of the cell: a cell is as tall as its row
      const rg = doc.createRange(); rg.selectNodeContents(c);
      const lines = rg.getBoundingClientRect().height / lh, text = c.textContent.trim();
      if (r.width < 7 * fs && lines > 5.5 && text.length > 12 && (!worst || lines > worst[0]))
        worst = [lines, text.slice(0, 40), Math.round(r.width)];
    });
    if (worst)
      out.push([page, w, i + 1, "squeezed", Math.round(worst[0]) + " lines in a " + worst[2] + " px cell: " + worst[1]]);
  });
}
async function run() {
  const out = [];
  for (const w of WIDTHS) {
    const f = document.createElement("iframe");
    f.style.width = w + "px"; f.style.height = "900px"; f.style.border = "0";
    document.body.appendChild(f);
    for (const p of PAGES) {
      await new Promise(res => { f.onload = res; f.src = p; });
      await new Promise(res => setTimeout(res, 30));
      try { measure(f.contentDocument, p, w, out); } catch (e) { out.push([p, w, "", "error", String(e)]); }
    }
    f.remove();
  }
  document.getElementById("out").textContent = JSON.stringify({done: true, rows: out});
}
run();
</script></body></html>"""


def browser():
    b = next((p for p in BROWSERS if p.exists()), None)
    if not b:
        sys.exit("no Edge or Chrome found; this check needs one of them")
    return b


def serve(extra):
    """The rendered site on a free local port, plus the check pages in `extra` (path -> html)."""
    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            body = extra.get(self.path.split("?")[0])
            if body is None:
                return super().do_GET()
            data = body.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *args):
            pass
    srv = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Handler, directory=str(SITE)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def headless(args, timeout):
    """One headless browser run with a throwaway profile of its own: a browser left over from a run that timed out
    keeps its profile locked, and a second run on that profile stalled (2026-11-19)."""
    prof = Path(tempfile.mkdtemp(dir=OUT, prefix="profile-"))
    cmd = [str(browser()), "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
           "--disable-extensions", f"--user-data-dir={prof}", *args]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    finally:
        shutil.rmtree(prof, ignore_errors=True)


def sample(pages):
    """One page of each kind: the first page of every folder, and the first record page of every test type."""
    seen, out = set(), []
    for p in pages:
        parts = p.split("/")
        kind = parts[0] if len(parts) > 1 else p
        m = re.match(r"(experiments|review)/b68-([a-z]+)", p)
        if m:
            kind = f"{m.group(1)}-{m.group(2)}"
        if kind not in seen:
            seen.add(kind)
            out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pages", nargs="*", help="globs under site/_site (default: every page)")
    ap.add_argument("--widths", nargs="*", type=int, default=[1280, 390], help="frame widths in px (desktop, phone)")
    ap.add_argument("--batch", type=int, default=40, help="pages per browser run")
    ap.add_argument("--shots", action="store_true", help="also screenshot one page of each kind at each width")
    a = ap.parse_args()
    if not (SITE / "index.html").exists():
        sys.exit("site/_site is not rendered; run python tools/render_site.py first")
    globs = a.pages or ["**/*.html"]
    pages = sorted({p.relative_to(SITE).as_posix() for g in globs for p in SITE.glob(g)
                    if "site_libs" not in p.parts and p.suffix == ".html"})
    OUT.mkdir(parents=True, exist_ok=True)
    extra = {}
    srv = serve(extra)
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    rows = []

    def measure(chunk):
        """The problems of a run of pages; a run the browser does not finish is split in halves, and a single page
        that does not finish is reported as `no-load` (images are not loaded: they do not change a table's layout
        and made a run of 80 record pages take more than 9 minutes)."""
        name = f"/__layout_check_{len(extra)}.html"
        extra[name] = CHECK_PAGE % {"pages": json.dumps(["/" + p for p in chunk]), "widths": json.dumps(a.widths)}
        try:
            r = headless(["--dump-dom", "--virtual-time-budget=900000", "--window-size=1400,1000",
                          "--blink-settings=imagesEnabled=false", base + name], timeout=30 + 4 * len(chunk) * len(a.widths))
            m = re.search(r'<pre id="out">(.*?)</pre>', r.stdout, re.S)
            got = json.loads(html.unescape(m.group(1))) if m and m.group(1) != "pending" else None
        except subprocess.TimeoutExpired:
            got = None
        if got and got.get("done"):
            return got["rows"]
        if len(chunk) == 1:
            return [["/" + chunk[0], "", "", "no-load", "the browser did not finish this page"]]
        h = len(chunk) // 2
        return measure(chunk[:h]) + measure(chunk[h:])

    for k in range(0, len(pages), a.batch):
        chunk = pages[k:k + a.batch]
        got = measure(chunk)
        rows += got
        print(f"pages {k + 1} to {k + len(chunk)} of {len(pages)}: {len(got)} problems in this batch", flush=True)
    with (OUT / "layout.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["page", "width", "table", "problem", "detail"])
        w.writerows(rows)
    if a.shots:
        shots = OUT / "shots"
        shutil.rmtree(shots, ignore_errors=True)
        shots.mkdir(parents=True)
        for p in sample(pages):
            for wd in a.widths:
                png = shots / f"{p.replace('/', '__').removesuffix('.html')}-{wd}.png"
                # a browser window does not get narrower than about 500 px, so a narrower page is shot through a
                # frame of that width (the window laid the page out wider and cut it, 2026-11-19)
                url = f"{base}/{p}"
                if wd < 600:
                    shot = f"/__shot_{len(extra)}.html"
                    extra[shot] = ('<!doctype html><html><body style="margin:0">'
                                   f'<iframe src="/{p}" style="width:{wd}px;height:3200px;border:0"></iframe></body></html>')
                    url = base + shot
                try:   # a page with many full-size scans can take minutes to load: skip it rather than stop
                    headless([f"--screenshot={png}", f"--window-size={max(wd, 600)},3200", "--hide-scrollbars", url], timeout=90)
                except subprocess.TimeoutExpired:
                    print(f"screenshot skipped (did not load in 90 s): {p} at {wd} px")
        print(f"screenshots: {len(list(shots.glob('*.png')))} in {shots.relative_to(ROOT)}")
    srv.shutdown()
    from collections import Counter
    c = Counter((r[3], r[1]) for r in rows)
    print(f"{len(pages)} pages at widths {a.widths}: " + (", ".join(f"{k[0]} at {k[1]} px: {n}" for k, n in sorted(c.items())) or "no problems"))
    print(f"details: {(OUT / 'layout.csv').relative_to(ROOT)}")
    return 1 if rows else 0


if __name__ == "__main__":
    sys.exit(main())
