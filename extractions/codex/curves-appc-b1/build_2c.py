import json
from pathlib import Path
d={'image':'packet/p0122.png','p1':{},'p2':{}}
def p(s,sym,pts,peak,end=None,path=None):
    path=path or [q[:2] for q in pts];end=end or path[-1]
    if end[0]>path[-1][0]:path.append(end)
    d['p1'][s]={'symbol':sym,'markers':pts,'path':path,'features':[[*path[0],'first curve / symbol interruption',5],[*peak,'maximum of author trace; broad maximum',5],[*end,'last visible trace',5]]}
p('n4400','asterisk',[[813,1812],[877,1695],[927,1621],[987,1544],[1049,1487],[1111,1432],[1164,1396],[1216,1370],[1281,1338],[1343,1322],[1400,1305],[1458,1296],[1513,1289],[1571,1291],[1628,1298],[1688,1317]], [1495,1288],end=[1680,1320])
p('n3660','x',[[719,2068],[757,1982],[813,1877],[872,1793],[932,1721],[990,1662],[1042,1637],[1100,1602],[1161,1571],[1219,1554],[1284,1539],[1344,1525],[1401,1516],[1458,1508],[1518,1501],[1582,1504],[1638,1506]],[1510,1503],end=[1635,1505])
p('n2995','square',[[751,2068],[786,2001],[822,1936],[875,1872],[987,1764],[1049,1721],[1102,1697],[1159,1676],[1222,1661],[1279,1635],[1458,1630],[1568,1642]],[1430,1628],end=[1570,1644])
p('n2200','triangle-up',[[734,2431],[791,2345],[820,2302],[872,2216],[932,2139],[1049,2037],[1164,1989],[1224,1963],[1286,1948],[1344,1948],[1401,1927]],[1390,1938],end=[1468,1939],path=[[734,2431],[791,2345],[820,2302],[872,2216],[932,2139],[1049,2037],[1164,1980],[1224,1957],[1286,1943],[1344,1938],[1401,1938],[1468,1939]])
p('n1468','circle',[[700,2680,6,'marker touches left frame'],[715,2558],[753,2453],[815,2355],[901,2288],[983,2249],[1049,2223],[1161,2223]],[1100,2218],end=[1150,2220])
p('n734','circle',[[720,2644,4,'solid filled circle'],[753,2529,4,'solid filled circle near horizontal grid'],[815,2453,4,'solid filled circle'],[925,2419,4,'solid filled circle'],[1040,2426,4,'solid filled circle']],[939,2416],end=[1087,2438])
def q(s,sym,pts):d['p2'][s]={'symbol':sym,'markers':pts}
q('n4400','asterisk',[[984,3231,9,'early star hidden in triangle and vertical/zero grid'],[1042,3235,9,'early star/zero line; weak assignment'],[1100,3230,8,'early star shares triangle/x ink'],[1164,3221],[1224,3227],[1279,3224,8,'star on vertical grid'],[1340,3217],[1397,3216],[1453,3199],[1519,3199],[1572,3191,6,'star on vertical grid'],[1629,3188],[1688,3179]])
q('n3660','x',[[984,3229,9,'early x hidden in triangle/grid cluster'],[1044,3226,9,'x/triangle cluster; weak assignment'],[1100,3227,8,'x/square/triangle shared ink'],[1166,3187,8,'x immediately under square'],[1227,3197,8,'x under triangle'],[1279,3206,8,'x and square beneath triangle on grid'],[1339,3199],[1396,3185,7,'x close to square/triangle'],[1450,3177,7,'x touches triangle/square'],[1519,3167],[1574,3162,7,'x on vertical grid'],[1629,3164]])
q('n2995','square',[[704,3226,6,'first square close to left frame'],[737,3212,6,'square shares adjacent early ink'],[920,3200],[985,3199,8,'square under circle on vertical grid'],[1043,3189],[1103,3187,7,'square is rounded; possible circle ambiguity'],[1167,3174,7,'square close to x and circle'],[1220,3163],[1271,3155,7,'square centered on vertical grid'],[1334,3187,8,'square/triangle overlap; identity uncertain'],[1392,3178,8,'square/triangle overlap'],[1452,3165,8,'square/triangle overlap']])
q('n2200','triangle-up',[[806,3224,8,'early triangle and circle/filled dot shared ink'],[864,3223,7,'small triangle'],[924,3221,8,'triangle sits near square'],[985,3220,8,'triangle touches x/star/frame grid'],[1044,3218],[1104,3212,8,'triangle/square/x shared ink'],[1166,3200,7,'triangle below x/square'],[1225,3189,7,'triangle beside x'],[1279,3180,8,'triangle and square share grid ink'],[1339,3172,8,'triangle and square overlap'],[1398,3163,8,'triangle and square overlap'],[1451,3153,8,'triangle and square overlap']])
q('n1468','circle',[[805,3216,9,'hollow circle hidden under dot and triangle; uncertain'],[894,3198],[984,3184,8,'circle/filled-circle/grid overlap'],[1040,3175],[1154,3153]])
q('n734','circle',[[805,3208,4,'solid filled circle'],[863,3196,4,'solid filled circle'],[984,3184,9,'filled circle hidden under hollow circle/grid; uncertain'],[1042,3148,4,'solid filled circle']])
Path('out/FC-2C/reading.json').write_text(json.dumps(d,indent=2))
