# FC-7B reading notes (Claude reader, batch curves-appc-b4)

Source: AM-68-1 Vol. II (NASA CR-92215), Figure C-7B, printed C-22, PDF page 136, `packet/p0136.png`
(3213 x 4221 px, bilevel). One panel; plotted symbols only, no drawn lines, no dilation panel.

## Orientation and calibration

1. The figure is printed sideways. On the page as scanned the horizontal-motion axis (x, inches)
   runs UP the page (0 at v 3284, .32 at v 1317) and the horizontal-load axis (y, psi) runs from
   right (0 at u 2317) to left (35 at u 604). Read on the unrotated page.
2. Command: `tools/calibrate_axes.py detect packet/p0136.png --box 575 1305 2335 3305
   --x-values 0,0.04,...,0.32 --y-values 0,5,...,35 --x-direction up --y-direction left`.
   All 9 x lines and 8 y lines detected in 5/5 bands (no `predicted` line); 72 anchors.
3. Residuals: x RMS 0.00015 in (0.047 % of the 0.32 in span), max 0.00042 in; y RMS 0.022 psi
   (0.063 % of the 35 psi span), max 0.056 psi. Both well under the 0.5 % limit.
4. By-eye label check (`calibration-eye-checks.csv`): all 8 load labels (35 ... 0) and all 9
   motion labels (.32 ... 0) were located and each sits next to its own fitted line (offsets
   -6 to +9 px for the load labels, -6 to +20 px for the motion labels; the larger offsets come
   from the leading "." of the sideways motion labels and from typesetting, the line spacing is
   245 px, so no label is ambiguous). The printed values increase to the left (load) and up the
   page (motion), which confirms `--y-direction left` and `--x-direction up`.

## Series identity

1. The legend box (top of the frame) prints no symbols, only "(PSI)(PCF)" and the pairs
   27.1/89, 13.8/89, 10.2/89, 6.6/89, 5.1/89, 3.4/89. Each pair is printed at the load where one
   curve ends (27.1 near u 1080 where the quarter-circles end at about 25 psi, 13.8 near u 1700
   where the stars end, 10.2 near the last triangle, 6.6, 5.1, 3.4 near the last diamond, square,
   circle). So: quarter-circle = n27p1psi, star = n13p8psi, triangle = n10p2psi, diamond =
   n6p6psi, square = n5p1psi, circle = n3p4psi. The printed values agree with `series.csv`; the
   first digit of "3.4" is partly broken in the scan and is read as 3.
2. Cross-check only (not used for the reading): the peak of each series' markers (33.3, 20.6,
   15.3, 10.0, 8.9, 7.5 psi) is close to the triangle points of Figure C-7A (p0135, gamma 89),
   read roughly from a downscaled view; the differences are 0.1 to about 0.6 psi.
3. Symbol shapes as printed on the page: quarter-circle with flat top, flat right side and the
   arc at lower left (the open D-shape); triangle pointing LEFT on the page, which is
   `triangle-up` with the figure upright; star, diamond, square, circle as named.

## Marker centers and bounds

1. Every center is the center of the symbol's bounding box, read on zoomed crops and on ASCII
   pixel maps (`helpers/ascii.py`, `helpers/ascii2.py`, the latter marks grid-line pixels).
   Convention that matters for the comparison:
   - Triangle: midpoint between the tip and the outer edge of the vertical side (not the
     centroid, which would be about 5 px toward the vertical side).
   - Quarter-circle: bounding-box center, not the right-angle corner (the corner is about 15 px
     up and to the right on the page).
   - The quarter-circle centers sit 3 to 6 px below the x grid lines they are drawn on
     (x about 0.001 in below .04, .12, .16), while the other symbols sit on the lines within
     about 1 px; recorded as read, not adjusted.
2. Bounds: 2 px for a clean center; 3 px in the direction where an edge lies inside a grid-line
   band or a neighbor symbol; 4 to 5 px in v for the symbols near the origin whose lower part is
   hidden in the thick x = 0 frame line (center v = visible top plus half the usual symbol height).
3. The candidate blob list from `helpers/candidates.py` was used only to make sure no symbol was
   missed; about 40 of its bounding boxes were wrong (grid-line removal cut an edge, or a stray
   dot or dash was merged) and were re-read by eye. The final centers are in
   `helpers/build_points.py`.

## Crowding near the origin (x below about 0.01 in): what was read and how sure

1. Bottom strip u 1520 to 2275, v 3230 to 3285 holds 17 symbols, many overlapping and cut by
   the x = 0 frame line. Identified by shape (straight vs slanted sides, pointed vs round):
   - quarter-circles at u 1542, 1671.5, 1800 (flat top and flat right side, slanted arc on the
     left; only the top 20 to 25 px visible) and at u 1348.5 (top-left corner on the 20 psi line);
   - stars at u 1557.5 (sitting on the quarter-circle at u 1542), 1712, 1856 (overlapping a
     triangle above it);
   - triangles at u 1835 (on the 10 psi line), 1942, 2134 (tip merged with a circle);
   - diamond at u 2022 overlapping a circle at u 2037.5: first looked like two circles or a
     quarter-circle plus circle; the pointed top vertex at (2022, 3235), the pointed left vertex
     at u 2003 and the absence of a vertical right side below v 3262 make it a diamond;
   - circle at u 2108 overlapping the square at u 2098: the round top and right arc favor a
     circle, a diamond is the alternative reading (noted on the point, bound 3 px);
   - squares at u 2098, 2194.5, 2256.5 (vertical left sides), circle at u 2211.5.
2. The diamond series shows two markers below x = 0.01 in, where the triangle, star and circle
   series show three; a diamond hidden in the frame line or under another symbol is possible but
   nothing visible supports one, so none is recorded.
3. Sequence numbers follow increasing displacement (decreasing v); near the origin this is also
   increasing load in every series, so the order is unambiguous.

## Ink that is not data

1. Short horizontal strokes (constant v, 10 to 90 px long) sit next to several symbols, for
   example at (1230-1292, 1460), (1468-1565, 2808), (1635-1805, 2686), (2033-2065, 2559), and a
   horizontal stroke to the left of the quarter-circle at x = .08. They look like drafting or
   leader marks; none is a symbol, none is recorded.
2. Isolated dots and ticks (for example above the quarter-circles at v 1431 and 2043, above the
   square at v 3020, inside the square at u 2261) are not recorded.

## Counts

quarter-circle n27p1psi 22, star n13p8psi 19, triangle n10p2psi 16, diamond n6p6psi 16, square
n5p1psi 17, circle n3p4psi 17; total 107 markers, panel 1, no trace or feature rows.

## Files

`cal-p1/` (anchors.csv, calibration.json), `calibration-eye-checks.csv`, `points-p1.csv`,
`points-p1-native.csv` (from `calibrate_axes.py apply`; note the tool rounds x_native and the
bounds to 0.001 in, so x bounds print as 0.0 or 0.001), `overlay-p1.png`, helpers under
`helpers/`, working crops under `crops/`.
