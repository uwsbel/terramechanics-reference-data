"""Follow each visible stroke in an upright working view and emit scan coordinates."""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from strut_calibration import axes, write_csv


# Coordinates in the gridded inspection images. These guides limit the ink search.
# They are not exported as observations.
GUIDES = {
    329: (850, 550, .7194, [[
        (54, 1268), (79, 1246), (170, 1150), (229, 1092), (317, 1015),
        (402, 937), (490, 863), (575, 792), (660, 724), (746, 665),
        (845, 612), (923, 576), (1000, 543), (1100, 512), (1190, 496),
        (1276, 486), (1360, 479), (1452, 474), (1510, 475), (1630, 480),
        (1730, 484), (1803, 487),
    ]]),
    330: (925, 710, .9188, [
        [(52, 497), (72, 493), (93, 486), (103, 477), (120, 450), (145, 408),
         (167, 369), (183, 348), (208, 328), (236, 314), (275, 306), (300, 306),
         (340, 314), (380, 326), (410, 330), (475, 329), (530, 332), (565, 334),
         (620, 329), (710, 314), (780, 303), (850, 296), (920, 293), (975, 291),
         (1030, 294), (1100, 307), (1160, 315), (1225, 313), (1260, 314),
         (1310, 324), (1353, 343), (1400, 372), (1455, 408), (1510, 439),
         (1570, 469), (1620, 498)],
        [(50, 882), (75, 881), (110, 878), (120, 873), (134, 854), (148, 830),
         (159, 800), (172, 766), (185, 738), (211, 718), (256, 710), (320, 704),
         (355, 702), (435, 706), (510, 712), (565, 715), (650, 714), (760, 709),
         (870, 703), (950, 701), (1020, 701), (1120, 710), (1230, 722),
         (1330, 733), (1420, 751), (1480, 770), (1540, 802), (1617, 851)],
        [],
    ]),
    336: (930, 560, .750, [[
        (53, 1048), (82, 1027), (160, 971), (230, 923), (326, 863),
        (417, 802), (505, 744), (600, 683), (690, 631), (780, 584),
        (875, 537), (960, 492), (1050, 447), (1145, 408), (1250, 374),
        (1330, 351), (1430, 324), (1515, 301), (1600, 283), (1697, 267),
        (1790, 262), (1874, 258),
    ]]),
    337: (945, 720, .884, [
        [(53, 563), (67, 558), (89, 539), (113, 513), (132, 494), (140, 492),
         (151, 496), (172, 517), (195, 543), (224, 571), (233, 578), (240, 576),
         (265, 560), (290, 548), (320, 543), (370, 547), (418, 551),
         (460, 550), (515, 544), (557, 541), (600, 543), (650, 549), (711, 555),
         (771, 556), (825, 552), (880, 550), (945, 542), (1010, 528),
         (1100, 508), (1180, 491), (1260, 473), (1310, 462), (1370, 454),
         (1440, 451), (1494, 450), (1560, 452), (1606, 457)],
        [(55, 937), (74, 932), (96, 923), (110, 911), (127, 883), (138, 860),
         (151, 832), (163, 818), (181, 813), (190, 814), (212, 827),
         (239, 848), (247, 852), (270, 853), (294, 850), (340, 837),
         (371, 831), (425, 826), (465, 820), (509, 806), (550, 795),
         (615, 784), (700, 773), (800, 763), (900, 756), (980, 753),
         (1080, 753), (1180, 750), (1260, 751), (1340, 753), (1410, 754),
         (1480, 751), (1550, 742), (1604, 732)],
        [(57, 1371), (66, 1340), (76, 1307), (87, 1276), (98, 1253),
         (110, 1242), (126, 1237), (160, 1234), (195, 1230), (226, 1225),
         (244, 1225), (276, 1231), (315, 1239), (360, 1244), (397, 1244),
         (435, 1239), (468, 1230), (500, 1216), (536, 1201), (570, 1193),
         (625, 1188), (700, 1182), (790, 1174), (885, 1165), (980, 1155),
         (1050, 1152), (1140, 1150), (1220, 1149), (1300, 1152),
         (1375, 1156), (1450, 1164), (1530, 1174), (1607, 1182)],
    ]),
}

F25_P3 = [
    (983, 2288), (1010, 2269), (1021, 2245), (1045, 2187), (1065, 2128),
    (1077, 2088), (1090, 2025), (1100, 1981), (1110, 1954), (1125, 1935),
    (1138, 1929), (1148, 1931), (1170, 1941), (1205, 1956), (1240, 1975),
    (1280, 1991), (1325, 2007), (1350, 2016), (1390, 2034), (1420, 2042),
    (1460, 2044), (1480, 2040), (1510, 2025), (1540, 2011), (1570, 1999),
    (1610, 1989), (1675, 1976), (1750, 1961), (1840, 1942), (1920, 1925),
    (1990, 1914), (2070, 1905), (2140, 1900), (2195, 1903), (2250, 1912),
    (2300, 1926), (2330, 1939), (2360, 1956), (2375, 1971), (2390, 1989),
    (2405, 2015), (2418, 2043), (2430, 2074), (2441, 2111), (2450, 2133),
    (2465, 2155), (2483, 2172), (2509, 2189), (2550, 2208), (2600, 2226),
    (2650, 2242), (2680, 2254),
]

FIGURES = {
    329: ("F5-24", ["pen"], .2),
    330: ("F5-25", ["strut3", "strut2", "strut1"], 5),
    336: ("F5-31", ["pen"], .2),
    337: ("F5-32", ["strut3", "strut2", "strut1"], 5),
}


def runs(mask):
    indices = np.flatnonzero(mask)
    return [a for a in np.split(indices, np.where(np.diff(indices) > 1)[0] + 1) if len(a)]


def rules_at(cal, x, vmax):
    return [r["u_at_v0"] + r["slope_du_dv"] * (vmax - x) for r in cal["vertical_lines"]]


def nearby_frame(cal, x, y, vmax):
    on_full_grid = cal["image"].endswith(("0329.png", "0336.png"))
    lines = cal["horizontal_lines"] if on_full_grid else cal["horizontal_lines"][:1]
    return any(abs(vmax - x - r["v_at_u0"] - r["slope_dv_du"]*y) < 5 for r in lines)


def read_track(gray, cal, guide):
    vmax = gray.shape[1] - 1
    columns = np.arange(round(guide[0, 0]), round(guide[-1, 0]) + 1)
    guess = np.interp(columns, guide[:, 0], guide[:, 1])
    measured = np.full(len(columns), np.nan)
    projected = guess.copy()
    for pass_no in range(3):
        measured[:] = np.nan
        slopes = np.gradient(guess)
        for i, (x, y0) in enumerate(zip(columns, projected)):
            y_near = round(y0)
            if nearby_frame(cal, x, y0, vmax):
                continue
            radius = (24, 14, 11)[pass_no] + round(abs(slopes[i])*6)
            top, bot = y_near-radius, y_near+radius+1
            rows = rules_at(cal, x, vmax)
            cand = []
            for span in runs(gray[top:bot, x] < 150):
                if (len(span) < 2 or len(span) > max(21, 12*np.hypot(1, slopes[i]))
                        or span[0] == 0 or span[-1] == bot-top-1):
                    continue
                yc = (span[0] + span[-1]) / 2 + top
                # A horizontal ruling often continues through the search window.
                # Skip a merged trace/ruling run and bridge from the visible stroke on both sides.
                if min(abs(yc - y_rule) for y_rule in rows) < 3.2:
                    continue
                cand.append((abs(yc - y0) - 0.18*min(len(span), 8), yc))
            if cand:
                measured[i] = min(cand)[1]
        good = np.isfinite(measured)
        projected = np.interp(columns, columns[good], measured[good])
        # Refine the guide with a short median filter to suppress broken scan pixels.
        p = np.pad(projected, 2, mode="edge")
        projected = np.median(np.lib.stride_tricks.sliding_window_view(p, 5), axis=1)
        # At the endpoints the eyeballed stroke can reach the frame before the fit can.
        first, last = np.flatnonzero(good)[[0, -1]]
        projected[:first] = guess[:first]
        projected[last+1:] = guess[last+1:]
    return columns, projected, measured


def make_previews():
    for page, (fig, series, _) in FIGURES.items():
        original = f"packet/p{page:04}.png"
        im = Image.open(original).convert("L").transpose(Image.Transpose.ROTATE_270)
        gray = np.array(im)
        x0, y0, scale, guides = GUIDES[page]
        for panel, (name, guide) in enumerate(zip(series, guides), 1):
            cal_dir = Path("out") / fig / f"cal-p{panel}"
            cal = json.loads((cal_dir / "calibration.json").read_text())
            guide = np.array(guide) / scale + [x0, y0] if guide else np.array(F25_P3)
            columns, projected, measured = read_track(gray, cal, guide)
            top = int(projected.min()-25)
            bottom = int(projected.max()+28)
            left, right = columns[0]-12, columns[-1]+20
            pic = im.crop((left, top, right, bottom)).convert("RGB")
            d = ImageDraw.Draw(pic)
            for i, (x, y) in enumerate(zip(columns, projected)):
                if i % 4 == 0:
                    d.point((int(x-left), round(y-top)), fill="#e0008a" if np.isnan(measured[i]) else "#0087ff")
                if i % 50 == 0:
                    d.text((int(x-left), 2), str(x), fill="#0087ff")
            pic.save(Path("out") / f"trace-preview-{page}-p{panel}.png")
            np.savez(Path("out") / f"track-{page}-p{panel}.npz", columns=columns,
                     projected=projected, measured=measured)


if __name__ == "__main__":
    make_previews()
