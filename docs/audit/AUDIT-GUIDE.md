---
title: "Figure Audit Guide"
---

## Summary

You will check points that were read off scanned graphs, and say whether each one is in the right place. You need a web browser and a spreadsheet, nothing else.

1. **Open the packet.** It has one folder per chunk (A, B, C, D, ...). Each folder has a spreadsheet (`checklist.csv`) with one row per point and `viewer.html`, a page that shows the scan in your web browser with our reading marked on it. (It also has a close-up picture per row and the full scanned pages, for when you prefer a plain image.)
2. **Open `viewer.html`** in any web browser (double-click it; it works without internet). Pick a row from its list and it jumps to that point on the scan, with the crosshair placed and the row's question shown above the picture. (Use the row list for the checking: typing a pixel x and y moves a plain crosshair, without the row's question and box.) Zoom in or out, click to center the view on a spot, and read the pixel under your mouse, which you can quote in a comment. The row's close-up picture (the `picture` column names the file) shows the same thing as a plain image. On a table row (kind `cell`), start from the close-up picture: it shows the row's number and the column heading beside the cell, which the viewer can leave out of view.
3. **For each row, read the column `what to check`** (the viewer shows it too) and fill in the three answer columns:
   - **A location**: for a symbol, is the center of the printed symbol nearest the crosshair inside the small blue box around it? (The center is the middle of the symbol's width and height; for a triangle, its centroid, a third of the height in from the wide side, counts as well.) If it is inside, the answer is `yes`, even when the crosshair is not dead center: the box is the tolerance. For a curve sample, does the drawn line pass through the box? Answer `yes`, `no` or `cannot tell`. A line that enters the box and ends inside it passes (the last reading on a line sits where the printed line stops); a line that stops before the box does not, and neither does one dash of a dashed or dotted line that carries on after a white gap. On a compare row, two marks are shown, a blue crosshair and an orange square; answer which one is on the curve: `blue`, `orange`, `both` if both are on it, or `cannot tell`. When the compare row is about a symbol, answer which mark is nearer the center of the symbol, `both` if they sit on the center equally well (on a triangle, also when one sits at the middle and one at the centroid), or `cannot tell`.
   - **B identity**: is that symbol the one the row names, the symbol of the test the row names (the legend gives each test's symbol; a lower panel uses the same symbols as the upper one)? Answer `yes`, `no` or `cannot tell`. Leave B empty on curve samples and compare rows.
   - **C comment**: anything you noticed. Leave it empty when all is fine.
   - **Table rows** (kind `cell`) check a number read off a printed table instead of a point on a graph. A asks whether the picture shows the row and the column the checklist names (the row's number at the left, the column heading at the top right); B asks whether that cell reads the value given, exactly as printed.
4. **When unsure about A or B, write `cannot tell`** in that column and a few words in C saying what made it hard. Never guess, and do not change anything else in the spreadsheet.
5. **Send each spreadsheet back** saved as `checklist-<your initials>-<folder letter>.csv` (for example `checklist-R1-A.csv`), as you finish the folders or all at once, by the due date in the email. If you work in Google Sheets, download the sheet as CSV before attaching it. Edit only the three answer columns (headed A location, B identity, C comment); answer in lower case.

That is the whole job. Part 2 explains each step in more detail and says where the data comes from, for when you want it.

## Part 2: Details

The same job step by step, then the background.

### What you receive

One packet a week, as a zip file, with one folder per chunk and this guide at the top. You do not need access to the project's code repository, and you do not install anything. Each chunk folder holds:

1. **The checklist**, a spreadsheet with one row per point to check, about 60 rows. Each row tells you where to look (which figure, which curve, which symbol, where on the page) and, in the column `what to check`, what to decide. You fill in three columns per row.
2. **The viewer** (`viewer.html`): open it in any web browser (double-click it); it works without internet. Pick a row from the list and it shows the scan there with the crosshair placed and the row's question (a pixel x and y typed in moves a plain crosshair, without the question and box); move the mouse over the picture to read the pixel under it, click to center the view on a spot, and use the arrows to move around. When a chunk covers two figures, the rows are grouped by figure and a figure selector appears.
3. **Close-up pictures**, one per row (`closeups/row-NN.png`): the scan around the point, enlarged four times, with our reading marked. For a table row, the picture puts the row's number (at the left) beside the column's heading and the cell under it (at the right), enlarged twice, with the row boxed in blue in both.
4. **The scanned pages** (`scans/`), the figures as printed, at full resolution, for context. (The packets do not include drawings of the readings over whole panels: judge each point from the printed page, not from the readings.)
5. **Notes on the figures** (`about-the-figures.txt`): what the figure shows, which symbol or line belongs to which test, and anything that makes reading it hard. Read it before starting the folder: it also says when the figure itself is wrong, for instance a printed legend with two symbols swapped, and the checklist then follows the correction.

The pixel coordinates in the checklist refer to the scanned page image, origin at the top left corner, x to the right and y downward. A figure printed sideways on its page is shown upright in the viewer and the close-ups; the pixel coordinates still refer to the page as scanned.

### How to check one point

Each row of the checklist is one point. Some rows are quick, others need a closer look.

1. Read the row: which figure, which curve (the `test` column, for example a normal stress of 1172 psf), which symbol (circle, triangle, square, plus, x, asterisk), and the column `what to check`, which says what this row asks.
2. Look at the point in `viewer.html` (pick the row from the list) or in the row's close-up picture. Both show the scan around that point enlarged, with our reading marked by a thin blue crosshair and its error bar drawn as a blue box; on compare rows an orange square marks the other agent's reading. The crosshair should sit on the center of the printed symbol. In the viewer you can zoom, move around, and follow a line to the legend or to the curve's other symbols.
3. Answer question A, **location**: is the center of the printed symbol nearest our crosshair inside the blue box around it? Answer about that symbol even if its shape is not the one the row names; the shape is question B. Answer `yes`, `no`, or `cannot tell`. The center of a symbol is the middle of its width and its height. A triangle has two valid centers: that middle, and its centroid (its center of mass), which sits a third of the height in from the wide side. Our readings may use either, so a triangle whose middle or centroid is inside the box is a `yes`. Do not try to be more precise than the drawing allows; the box is the tolerance, so a center inside the box is a `yes` even when the crosshair is a little off.
4. Answer question B, **identity**: is this symbol the one the row says, and does it belong to the curve the row says? Look at the symbol's shape and at the legend printed on the figure (each test has its own symbol; a lower panel uses the same symbols as the upper one). Answer `yes`, `no` or `cannot tell`. If the symbol is right but it sits on a different curve than the row claims, answer `no` and say which curve in the comment.
5. Answer question C, **comment**: anything you noticed. Leave it empty when A and B are both `yes` and nothing looked odd.
6. For rows marked `curve sample` instead of a symbol: the question is only whether the drawn line passes through the blue box. A line that passes anywhere through the box is a `yes`, even when it misses the center of the crosshair. At the end of a line, the last reading is meant to sit where the printed line stops, so a line that enters the box and ends inside it is a `yes`, even if the crosshair sits a little past the last bit of ink. It is a `no` if the line stops before it reaches the box, or if what ends in the box is one dash of a dashed or dotted line that carries on after a white gap. There is no symbol to identify; answer A, leave B empty.
7. For the handful of rows marked `compare`: both agents' readings are shown, the blue crosshair and the orange square, and they differ by more than usual. Follow the lines to the curve's own symbols (the row's test names the curve) to be sure which line is which, then answer A with `blue` or `orange` for the mark that is on that curve, `both` if both are on it, or `cannot tell`. Leave B empty and say in the comment what decided it. When the compare row is about a symbol (its question says so; the lower panels have symbols and no lines), answer with the mark nearer the center of the symbol, the middle of its width and height, or `both` if the two sit on the center equally well. On a triangle both the middle and the centroid are valid centers: when one mark sits on each, answer `both` too.

8. For rows marked `cell`, from a printed table: the row names a test (for example run 1-17), a column (for example F_V (Lb.)) and the value we read in that cell. Use the row's close-up picture first: it shows the row's number and the column heading beside the cell, while the viewer centers on the cell and can leave them out of view. Answer A: does the picture show that row and that column? Read the number at the left and the heading at the top. Answer B: does the boxed cell read the value given, digit for digit, with the decimal point and any minus sign where they are printed (a value printed .298 is not 0.298)? A digit with a break or a missing piece counts as printed if you can still read it with confidence; if you cannot, answer `cannot tell` and say which digit in the comment.

Work in the order of the rows. Do not skip a row you find hard; record `cannot tell` and move on.

### The checklist columns

Columns on the left are filled in for you; the three answer columns are yours.

| Column | Filled by | Meaning |
| --- | --- | --- |
| row | us | Row number |
| kind | us | `symbol`, `curve sample`, `compare` or `cell` (see the walk-through) |
| figure | us | The figure the point is on (its id in the report, for example FC-1C is Figure C-1C of Volume II) |
| panel | us | 1 = upper panel, 2 = lower panel (one-panel figures are always 1) |
| test | us | The test the point belongs to, as the legend names it (for example the normal stress in psf, with kPa in brackets); on a table row, the row and the column |
| symbol | us | The printed symbol we assigned to this test |
| what to check | us | The question of this row, in words |
| A location | you | `yes`, `no`, `cannot tell`; on compare rows `blue`, `orange`, `both`, `cannot tell` |
| B identity | you | `yes`, `no`, `cannot tell` (empty on curve samples and compare rows) |
| C comment | you | Free text; which curve, what looked odd, how confident you are |
| pixel x, pixel y | us | Where we say the symbol center (or the curve) is, on the scan; type them into the viewer |
| picture | us | The close-up image of this row in the closeups folder |
| point id | us | Our internal name for the point; leave it as it is |

Please type the answers exactly as `yes`, `no`, `cannot tell` (and `blue`, `orange`, `both` on compare rows), in lower case, so a script can read them. The comment is free.

### When you are not sure

Doubt is useful information; a guess is not. Three rules.

1. **Never guess.** If you cannot decide whether the crosshair is on the symbol, answer `cannot tell` and say why in the comment (two symbols overlap, the symbol sits on a grid line, the ink is broken, the scan is smeared).
2. **The scan is the authority, not us.** If what you see contradicts what the row says, trust your eyes and write it down. Our readings have already been wrong more than once; finding that kind of thing is the point.
3. **Do not fix anything.** You record what you see; you do not change the data or the row. We make the corrections in the data files from your comments, so that every change is traceable to your audit.

### Optional: digitize ten points yourself

This is a stronger test of our method than checking our points: a third reading made with a different tool by a person. Skip it if time is short.

1. Open [WebPlotDigitizer](https://automeris.io/) (free, runs in the browser) and load one of the scans from the packet.
2. Calibrate the axes of one panel from four grid intersections, using the values printed on the axes. Use the grid lines, not the frame, because these scans are tilted by up to a degree.
3. Pick ten plotted symbols spread over the curves (at least one near a curve's start, one near its peak, one at its end) and click their centers. Note each one's curve and symbol.
4. Export the points as CSV and send it with the checklist. Write in your note which figure and which ten symbols you picked (curve and rough position) so we can match them to ours.

We will compare your ten values with ours. If they fall inside our error bars, the method passes its acceptance test on that figure; if not, we learn how large the real uncertainty is.

### Handing it back

Reply to the packet email with the filled checklists attached, each saved as `checklist-<your initials>-<folder letter>.csv` (and the WebPlotDigitizer CSV if you did the second task). Your initials and the date go into the audit record as the person who checked.

What happens next: a script turns your rows into entries of the project's audit file, one per point. Every point is checked by two people. Points you both confirmed are marked as checked by a person; points either of you flagged are re-read on the scan and corrected in the data if you were right, with your comment kept as the reason. The web pages of the tests then change from "not yet checked by a person" to "checked by a person on a sample of N points".

Send the folders back as you finish them rather than waiting for all four; a folder returned early gets its second review matched sooner.

### Where the data comes from

In 1968, Bendix tested candidate lunar soils for NASA's Lunar Module program: direct shear, penetration and impact tests on a dozen simulated lunar soils. The results survive only as curves and plotted symbols on the scanned pages of two reports (AM-68-1, Volumes I and II).

Two AI agents, working separately and without seeing each other's work, read the points off each scan: the center of every plotted symbol and samples along every drawn curve, each with an error bar. A script compares the two readings; where they agree within the error bars the point is kept, where they disagree the page is re-read and the right reading is kept with credit. Nobody has yet looked at the result with human eyes. That is your job, on a sample of the points of every figure.

Your check does two things. It confirms (or not) that the symbols are where we say they are and belong to the curves we say they do. And it finds the mistakes two agents can make together, for example both following the wrong line where two curves cross. If you find mistakes, that is a good outcome.

### The graphs you are checking

Most of the first packets are **direct shear data sheets**. A direct shear test puts a soil sample in a split box, presses down on it with a known normal stress, then slides the lower half of the box sideways and records the force needed and the sample's change in height. A data sheet shows five to seven such tests on the same soil at the same density, each at a different normal stress, each with its own symbol given in the legend. The upper panel plots shear stress (psf) against shear displacement (thousandths of an inch); each test is a hand-drawn curve through its plotted symbols. The lower panel plots dilation, the change in sample height in thousandths of an inch, against the same displacement; there are usually symbols only, no curves, with the same symbols as above.

Later packets add other figure types from the same reports: failure envelopes (shear strength against normal stress), friction angle against relative density, grain-size curves on a logarithmic axis, density charts, and load against penetration depth for plates and footpads pushed into the soil. The question is always the same: is our mark on the printed symbol or line, and is it the symbol the row names.

Things that make reading hard, so you are not surprised: small asterisks look like blobs; near the origin several symbols overlap; symbols that sit on a grid line or on the frame are partly hidden; two curves sometimes merge for a stretch and share one line of ink; and the scans are tilted by up to a degree, so grid lines are not exactly horizontal. The `about-the-figures.txt` file in each folder lists what we know about that chunk's figures.
