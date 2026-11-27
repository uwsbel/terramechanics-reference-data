import csv
cols = ["nasa_test_no", "bendix_drop_no", "VV_in_s", "Vh_in_s", "tau_s", "soil", "Dr", "gamma_pcf", "phi_deg", "note"]
four = "the 4 prints with a broken or faint diagonal stroke; read with confidence"
rows = [
    ["1", "10", "-114.9", "0", ".298", "RS Loose", "0", "46.9", "41",
     f"gamma 46.9 and phi 41: {four}"],
    ["2", "11", "-60.5", "83.5", ".177", "RS Loose", "0", "46.9", "41",
     f"gamma 46.9 and phi 41: {four}"],
    ["3", "12", "-60.0", "84.0", ".156", "RS Loose", "0", "47.1", "41",
     "Soil: the S of RS is broken (its lower stroke is detached), still reads RS; "
     f"gamma 47.1 and phi 41: {four}; the column rule left of the Soil cell has a gap beside this row"],
    ["4", "13", "-117.3", "0", ".304", "RS Loose", "0", "47.1", "41",
     "gamma 47.1: the 4 and the 7 are lightly printed and broken; "
     f"phi 41: {four}; a short broken piece of the column rule left of the Soil cell looks like a mark before RS"],
    ["5", "16", "-60.8", "83.4", ".146", "RS Intermediate", ".3", "53.0", "42.5",
     "D_r printed .3 with no leading zero; gamma 53.0: the 5 prints with its top bar detached (typeface, as in other 5s); read with confidence"],
    ["6", "17", "-117.1", "0", ".303", "RS Intermediate", ".3", "53.0", "42.5",
     "V_v -117.1: the middle 1 has a break and a small spur in its stem; read with confidence; "
     "D_r printed .3 with no leading zero; gamma 53.0: 5 with detached top bar (typeface)"],
    ["7", "20", "-60.0", "84.0", ".154", "SS Loose", "0", "96.0", "30", ""],
    ["8", "21", "-118.0", "0", ".306", "SS Loose", "0", "96.0", "30", ""],
]
with open("out/table.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(cols)
    w.writerows(rows)
print(open("out/table.csv", encoding="utf-8").read())
