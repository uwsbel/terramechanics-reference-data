import json
from pathlib import Path
d={'image':'packet/p0119.png','p1':{},'p2':{}}
def p(s,sym,pts,peak,path=None,end=None):
    path=path or [q[:2] for q in pts];end=end or path[-1]
    if end[0]>path[-1][0]:path.append(end)
    d['p1'][s]={'symbol':sym,'markers':pts,'path':path,'features':[[*path[0],'first trace / symbol interruption',5],[*peak,'peak of author trace; broad maximum',6],[*end,'last visible trace',5]]}
p('n3520','x',[[629,2135],[748,1827],[857,1667],[976,1548],[1093,1479],[1207,1443],[1320,1435],[1445,1456],[1564,1525],[1739,1576,6,'marker above author curve'],[1856,1672,5,'marker below author curve'],[2039,1699]], [1268,1431],path=[[629,2135],[748,1827],[857,1667],[976,1548],[1093,1479],[1207,1443],[1268,1431],[1320,1435],[1445,1456],[1564,1525],[1739,1603],[1856,1651],[2039,1699]])
p('n2935','asterisk',[[637,2185],[742,1922],[975,1665],[1095,1598],[1215,1594],[1331,1613],[1446,1642],[1623,1686],[1740,1712],[2039,1761]],[1175,1596])
p('n2345','square',[[682,2160],[794,1930,5,'square above rising author fit'],[919,1862],[1031,1814],[1149,1794],[1263,1797],[1386,1815],[1501,1840],[1623,1848,5,'square above author fit'],[1739,1843,6,'square well above fit on vertical grid'],[1865,1969],[2050,2039]], [1165,1794],path=[[699,2134],[794,1960],[919,1862],[1031,1814],[1149,1794],[1263,1797],[1386,1815],[1501,1840],[1623,1873],[1739,1915],[1865,1969],[2039,2034]],end=[2039,2034])
p('n1468','triangle-down',[[642,2520],[750,2309],[866,2199],[980,2149],[1104,2138],[1221,2140],[1280,2142],[1396,2143],[1514,2144],[1644,2141,6,'triangle above declining author fit'],[1760,2259],[1878,2260]], [1105,2138],path=[[642,2520],[750,2309],[866,2199],[980,2149],[1104,2138],[1221,2140],[1396,2143],[1514,2144],[1644,2174],[1760,2229],[1878,2263],[2039,2275]],end=[2039,2275])
p('n587','triangle-up',[[639,2699],[760,2564],[873,2510],[986,2491],[1107,2487],[1279,2527],[1397,2541],[1519,2567],[1635,2582],[1756,2593],[1874,2625],[2047,2631]], [1060,2488],end=[2039,2625])
p('n294','circle',[[620,2794],[709,2694],[824,2634],[936,2614],[1054,2607],[1174,2624],[1407,2669],[1537,2694]],[1030,2607],end=[1531,2691])
p('n0','circle',[[698,2814,3,'solid filled circle'],[822,2780,3,'solid filled circle'],[929,2770,3,'solid filled circle'],[1003,2768,3,'solid filled circle'],[1119,2771,3,'solid filled circle'],[1233,2781,3,'solid filled circle'],[1353,2794,3,'solid filled circle']],[1000,2768],end=[1431,2799])
def q(s,sym,pts):d['p2'][s]={'symbol':sym,'markers':pts}
q('n3520','x',[[598,3410,10,'x/star origin cluster on frame; uncertain assignment'],[651,3385,7,'near overlapping triangles'],[756,3367],[820,3354],[882,3355,7,'grid and star overlap'],[999,3337],[1120,3310],[1234,3286],[1350,3278],[1474,3255],[1587,3234],[1764,3198],[1881,3188],[2055,3173]])
q('n2935','asterisk',[[598,3395,10,'x/star origin cluster on frame; uncertain assignment'],[610,3358,8,'close symbols on frame'],[676,3358],[735,3358],[883,3340,8,'symbols on vertical grid'],[1000,3312],[1121,3284],[1249,3253],[1352,3245],[1479,3254],[1586,3189],[1763,3178],[1881,3160],[2056,3130]])
q('n2345','square',[[566,3363,6,'outside left frame; negative displacement'],[632,3333],[704,3360],[760,3330],[820,3327],[940,3315],[1063,3287],[1178,3262],[1291,3240],[1410,3218],[1524,3189],[1645,3163],[1763,3159],[1881,3135,6,'right square edge fragmented'],[2056,3100]])
q('n1468','triangle-down',[[583,3339,7,'frame cluster'],[649,3369,8,'overlap up triangle and x'],[894,3320],[998,3279,8,'up/down triangles share ink'],[1178,3216],[1291,3177,8,'up/down triangles overlap'],[1409,3168],[1524,3145],[1645,3124],[1758,3095],[1879,3078],[2054,3058]])
q('n587','triangle-up',[[589,3378,8,'frame cluster'],[648,3358,8,'up/down triangles overlap'],[878,3307],[998,3262,8,'up/down triangles share ink'],[1179,3244,8,'up/down triangles share ink'],[1292,3164,8,'up/down triangles overlap'],[1407,3135],[1524,3103],[1645,3076],[1755,3059],[1879,3025,6,'above +100; touches top frame'],[2054,2999,5,'above +100 frame']])
q('n294','circle',[[705,3330],[821,3277],[936,3239],[1051,3182],[1175,3139],[1289,3095],[1407,3053],[1521,3017,5,'above +100 frame']])
q('n0','circle',[[706,3294,3,'solid filled circle'],[823,3229,3,'solid filled circle'],[943,3162,3,'solid filled circle'],[990,3124,3,'solid filled circle'],[1113,3065,3,'solid filled circle'],[1228,3005,3,'solid filled circle above +100'],[1347,2956,3,'solid filled circle above +100']])
Path('out/FC-1D/reading.json').write_text(json.dumps(d,indent=2))
