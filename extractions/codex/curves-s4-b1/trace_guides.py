"""Visual centerline guides in the coordinates of reading_tiles.py.

Only guide the ink search. Native data and output pixel coordinates are measured
from the scan. Empty sections in the scan are supplied separately below.
"""
# Each route is in drawing order. Features are separately flagged by location.
ROUTES = {
("F4-19",1,"run4"): (
    "296,795 299,775 301,750 302,727 303,704 304,684 306,673 309,675 318,686 330,700 "
    "340,713 348,721 355,725 360,726 368,724 380,718 394,710 406,702 416,698 432,694 "
    "455,689 475,684 505,677 530,672 560,668 590,665 620,659 640,656 655,655 670,656 "
    "685,659 700,666 711,675 720,687 727,701 734,719 744,740 751,750 762,760 772,766 "
    "783,770 796,772 810,772 825,769 842,763 860,756 875,751 893,749 913,748 925,748",
    [(296,795,"first"),(306,673,"peak, impact peak"),
     (356,725,"knee, minimum after impact peak"),(406,702,"knee, decline in slope near 100 lb"),
     (655,655,"peak, broad secondary maximum"),(727,701,"knee, steep unloading"),
     (751,750,"knee, unloading starts to flatten"),(796,772,"knee, minimum after secondary peak"),
     (881,750,"knee, late recovery flattens"),(925,748,"last")]),
("F4-19",1,"run10"): (
    "296,794 296,779 297,766 298,750 299,735 299,719 299,702 300,686 300,670 300,654 "
    "300,630 300,610 301,593 302,573 303,555 306,539 308,527 309,519 315,525 321,540 "
    "326,552 331,565 336,581 342,595 349,611 356,628 364,646 375,665 388,683 400,695 "
    "413,711 430,725 445,732 461,733 480,731 500,726 520,721 540,715 558,712 575,713 "
    "596,718 616,724 636,731 660,738 686,744 709,750 731,758 750,764 766,769 782,771 "
    "800,769 820,765 840,763 861,763 880,763 902,762.8 916,763 924.8,763",
    [(296,794,"first"),(309,519,"peak, highest identified dot"),
     (457,733,"knee, minimum after impact peak"),(567,712,"peak, broad secondary maximum"),
     (781,771,"knee, probable minimum after secondary peak within overlap"),
     (843,763,"peak, weak late crest into plateau within overlap"),(924.8,763,"last")]),
("F4-19",1,"run12"): (
    "294,794 294,773 294,751 294,732 294,713 294,693 294,673 294,650 294,627 294,603 "
    "294,580 295,550 295,525 296,500 296,475 296,450 297,422 297,397 297,375 298,350 "
    "298,327 299,305 300,285 302,269 304,249 306,232 309,222 312,234 315,250 319,273 "
    "323,302 326,330 330,365 334,400 337,435 340,471 343,507 347,546 351,575 "
    "358,610 366,651 374,688 380,718 388,746 398,761 409,773 421,779 435,785 "
    "450,789 466,793 480,789 495,786 510,779 530,768 550,753 569,741 588,735 "
    "601,733 617,735 637,741 654,747 675,754 696,763 718,767 735,768 751,767 "
    "769,765 788,763 808,762 827,762 845,765 864,768 884,768 907,769 929,768",
    [(294,794,"first"),(309,222,"peak, impact peak"),
     (389,747,"knee, steep fall rounds into shallow decline"),
     (467,793,"knee, minimum after impact peak against baseline"),
     (600,733,"peak, secondary maximum"),
     (724,768,"knee, minimum after secondary peak"),
     (806,762,"peak, shallow late crest within overlap"),
     (894,768,"knee, shallow late minimum into plateau within overlap"),(929,768,"last")]),
("F4-19",2,"run4"): (
    "303,1308 310,1295 325,1270 345,1238 367,1206 391,1171 417,1132 444,1090 "
    "470,1056 494,1028 516,1005 542,981 564,964 587,949 614,934 643,920 669,911 "
    "694,905 721,902 750,903 779,905 807,906 838,905 870,904 900,904 928,903",
    [(303,1308,"first"),(447,1086,"knee, gradual reduction in penetration rate"),
     (722,902,"peak, maximum penetration"),(805,906,"knee, shallow minimum during recovery"),
     (928,903,"last")]),
("F4-19",2,"run10"): (
    "300,1303 311,1289 323,1278 336,1262 347,1245 359,1226 376,1206 400,1188 "
    "426,1170 450,1154 471,1141 494,1130 519,1121 546,1115 574,1112 600,1111 "
    "630,1111 656,1112 678,1113",
    [(300,1303,"first"),(536,1117,"knee, leveling off"),
     (609,1111,"peak, maximum penetration on broad plateau"),(678,1113,"last")]),
("F4-19",2,"run12"): (
    "301,1295 309,1284 318,1276 326,1266 335,1258 346,1253 356,1246 372,1240 "
    "391,1235 409,1231 432,1227 450,1223 474,1219 495,1214 518,1209 540,1204 "
    "562,1199 583,1195 606,1192 625,1189 649,1187 674,1186 702,1186 732,1186 "
    "761,1186 790,1186 817,1186 845,1186 874,1186 906,1185 934,1185",
    [(301,1295,"first"),(346,1253,"knee, rapid initial rise tapers"),
     (490,1215,"knee, penetration rate picks up gradually"),
     (667,1186,"knee, leveling off"),(905,1185,"peak, representative point on late plateau"),
     (934,1185,"last")]),
("F4-20",1,"run4"): (
    "213,636 215,622 216,605 218,593 220,581 224,570 227,557 230,550 234,542 "
    "242,537 254,533 264,534 278,538 295,544 311,551 328,560 344,567 362,573 "
    "379,575 396,574 421,570 445,567 463,564 478,561 500,553 520,548 540,547 "
    "575,544 610,540 650,535 690,530 730,526 770,523 810,520 850,515 890,511 "
    "912,509 921,511 927,516 929,523 930,539 931,556 931,576 931,597 "
    "928,603 925,609 924,612 924,603 924,591",
    [(213,636,"first"),(253,533,"peak, impact peak"),(380,575,"knee, minimum after impact peak"),
     (518,548,"knee, slope decreases near blank strip"),
     (913,509,"peak, broad secondary crest"),
     (928,519,"knee, steep unloading near maximum displacement"),
     (931,598,"knee, bends left"),(924,612,"knee, minimum after secondary crest and reversal"),
     (924,591,"last")]),
("F4-20",1,"run10"): (
    "213,635 213,625 215,612 215,601 216,591 218,580 220,569 221,557 224,545 "
    "226,536 227,523 230,508 234,490 237,473 243,450 249,431 256,411 263,394 "
    "276,396 288,398 292,403 297,410 305,421 314,434 321,445 331,460 339,470 "
    "350,484 364,500 375,509 392,515 405,520 416,528 430,540 444,551 "
    "458,563 471,579 475,584 486,583 544,577 550,578 554,584 556,590 557,594 "
    "558,598 560,603 561,608 560,612",
    [(213,635,"first"),(264,394,"peak, highest identified dot"),(291,399,"knee, shoulder after peak"),
     (375,508,"knee, decline flattens"),(404,520,"knee, decline steepens"),
     (477,584,"knee, last low dots before the blank strip"),
     (544,577,"peak, highest visible dot after blank strip"),(554,584,"knee, steep unloading"),
     (560,612,"last")]),
("F4-20",1,"run12"): (
    "212,637 212,623 212,603 212,584 213,565 213,545 214,526 215,507 216,488 "
    "218,468 219,447 221,429 222,409 223,389 225,371 227,353 230,331 232,310 "
    "234,290 236,275 239,247 242,227 246,206 250,185 256,163 264,145 273,127 "
    "279,128 286,145 293,162 298,180 303,200 306,220 309,239 312,260 315,281 "
    "316,302 320,323 322,344 324,366 325,397 326,421 327,444 330,465 330,485 "
    "332,507 334,528 336,550 340,572 345,593 350,611 356,629 368,630 378,628 "
    "387,625 397,614 402,603 406,590 413,585 418,583 422,586 425,594 427,601 428,610 429,617",
    [(212,637,"first"),(275,127,"peak, impact peak"),(294,167,"knee, slope changes below crest"),
     (324,367,"knee, descent steepens with displacement"),
     (364,630,"knee, minimum after impact peak"),
     (401,605,"knee, secondary rise steepens"),(419,583,"peak, secondary crest"),
     (429,617,"last")]),
}
# Guide gaps where the paper shows no separable curve. Values are local guide x
# except for the almost vertical loading and unloading branches marked by y.
VOID = {
    ("F4-20",1,"run4"): [("x",520,529,540,556)],
    ("F4-20",1,"run10"): [("x",490,544,568,595)],
}
# Printed crossings/overlaps and measurement ambiguity close to the frames.
REGIONS = {
("F4-19",1,"run4"): [
    (293,307,668,800,7,"left-edge onset shares ink with other runs and frame"),
    (372,383,711,728,4,"crosses Run 12"),
    (401,410,696,709,4,"crosses Run 10"),
    (758,775,754,775,7,"crosses Runs 10 and 12 during unloading"),
    (775,843,754,778,6,"close to Runs 10 and 12; late branches partly merge"),
    (828,857,750,774,5,"returns across Runs 10 and 12")],
("F4-19",1,"run10"): [
    (292,304,597,800,8,"rising pulse close to frame and Run 4"),
    (355,370,621,660,5,"crosses Run 12"),
    (400,412,697,712,4,"crosses Run 4"),
    (740,875,752,779,7,"late dots close to Runs 4 and 12 and partially merge"),
    (850,929,758,775,4,"dots lie just above or against Run 12 late line")],
("F4-19",1,"run12"): [
    (291,299,498,800,8,"left-edge onset and rising pulse share frame and other runs"),
    (354,369,620,662,5,"crosses Run 10"),
    (372,383,710,729,5,"crosses Run 4"),
    (455,479,785,800,5,"minimum touches baseline"),
    (743,859,752,777,7,"late branches close to Runs 4 and 10 and partly merge"),
    (850,932,759,775,4,"against Run 10 late dots")],
("F4-19",2,"run4"): [
    (291,339,1256,1313,8,"origin crowded by frame and Runs 10 and 12"),
    (338,354,1227,1261,4,"close to Run 10")],
("F4-19",2,"run10"): [
    (290,347,1249,1313,8,"origin crowded by frame and Runs 4 and 12"),
    (342,365,1223,1260,5,"close to Run 4"),
    (530,684,1105,1120,3,"dots close to the 2 in grid line")],
("F4-19",2,"run12"): [
    (292,350,1242,1308,8,"origin crowded by frame and Runs 4 and 10")],
("F4-20",1,"run4"): [
    (207,229,553,641,8,"left-edge onset shares ink with frame and other runs"),
    (334,349,558,579,5,"crosses Run 12"),
    (448,465,558,573,5,"crosses Run 10"),
    (515,534,541,554,3,"short break through the adjacent blank strip"),
    (921,934,595,615,4,"unloading downstroke and return stroke approach")],
("F4-20",1,"run10"): [
    (208,230,539,642,8,"left-edge onset shares ink with frame and other runs"),
    (320,341,444,469,5,"crosses Run 12"),
    (447,465,552,575,5,"crosses Run 4"),
    (471,489,576,589,3,"left edge of wide blank strip"),
    (543,552,573,582,3,"right edge of wide blank strip"),
    (552,565,585,616,4,"final dots overlie the 2 in grid line")],
("F4-20",1,"run12"): [
    (206,220,493,641,8,"left-edge ascent nearly coincides with frame and other runs"),
    (324,340,442,470,5,"crosses Run 10"),
    (334,350,555,579,5,"crosses Run 4")],
}
