"""Second-round packet: the round-1 items on which the Claude and Codex adjudicators split, same crops and
item numbers, with the brief extended by the conventions the project settled on 2026-10-15 (round 2 of that
adjudication), quoted, and the two measurement rules both round-1 adjudicators asked about.

Usage: make_round2.py <round1_work> <recheck-results.csv> <round2_work>
"""
import csv, shutil, sys
from pathlib import Path

r1, results, r2 = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
split = {r["item"] for r in csv.DictReader(open(results, encoding="utf-8")) if r["agree"] == "no"}
(r2 / "crops").mkdir(parents=True, exist_ok=True)
shutil.copytree(r1 / "pages", r2 / "pages", dirs_exist_ok=True)
shutil.copytree(r1 / "tools", r2 / "tools", dirs_exist_ok=True)
shutil.copy2(r1 / "figures.md", r2 / "figures.md")
with open(r1 / "items.csv", encoding="utf-8-sig", newline="") as f:
    rd = csv.DictReader(f); fields = rd.fieldnames; items = [r for r in rd if r["item"] in split]
with open(r2 / "items.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(items)
for r in items:
    shutil.copy2(r1 / r["crop"], r2 / r["crop"])
with open(r2 / "answers.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n"); w.writerow(["item", "A", "B", "confidence", "comment"])
    for r in items:
        w.writerow([r["item"], "", "", "", ""])
brief = (r1 / "BRIEF.md").read_text(encoding="utf-8")
brief = brief.replace("The points in this packet were singled out for a closer look.",
                      f"The {len(items)} points in this packet were singled out for a closer look; item numbers are not consecutive.")
brief += """
## This is a second round: settled conventions, apply them exactly

The items here are the ones on which a first round of adjudication did not agree. The project settled
the following conventions earlier (quoted from its adjudication of 2026-10-15); they take precedence
over anything above that seems to say otherwise.

1. A trace sample counts as on the line when it is on the line's ink or within 2 px of it at the
   line's height; within 2 px beyond the end of a dash also counts. A sample on a symbol's outline,
   or in the white gap between dashes or between a dash and a symbol, is off the line.
2. A line that runs into a plotted symbol without a gap: a trace sample in ink the line shares with
   the symbol's outline is off the line (the trace sample belongs on the line's own ink).
3. A curve that runs into a frame or grid line ends where its own ink can no longer be told from the
   line it meets: at the near edge of that line, not at its centre. A sample within 2 px of the
   curve's last visible ink counts as on the line; a sample further inside the frame or grid line
   does not.
4. The center of a triangle is its centroid (one third of the height from the base). A mark between
   the centroid and the middle of the triangle's bounding box is on the center.
5. A circle crossed by a grid line or a curve is still one circle; its center is the center of its
   ring. Two rings that overlap are two symbols only if both rings can be traced.
6. When you answer `neither`, give in the comment the pixel position you would put the point at.

Two measurement rules for this packet:

7. The 3 px tolerance of a symbol center is a straight-line (Euclidean) distance. When the center
   itself cannot be placed to better than about 1 px (a symbol merged with a grid line, the frame,
   its line or another symbol) and the answer would change within that uncertainty, answer
   `cannot tell` and give the distances in the comment.
8. Do not bridge a gap in a drawn line. Where the line stops at a symbol and a reading falls in the
   gap or on the symbol, that reading is off the line (convention 1), whatever the line would do if
   continued; if both readings are off the line, the answer is `neither`.
"""
(r2 / "BRIEF.md").write_text(brief, encoding="utf-8", newline="\n")
print(f"{len(items)} items in {r2}")
