import csv
cols = ("experiment_id,source_id,kind,test_type,test_label_printed,soil_family,soil_no,soil_no_status,state_printed,"
        "dr_printed,unit_weight_printed_pcf,gp_printed_g,apparatus,penetrator_printed,bin_printed_in,loading,rate_printed,"
        "start_depth_printed_in,measured_channels,evidence,setup_status,mcc_relevant,priority,relation,relation_target,notes").split(",")

apparatus = ("modified Langley-Grumman 1/6-scale dynamic model of LM (Figs. 5-1 to 5-3; honeycomb shock struts, 37 sensors) "
             "launched by the six-degree-of-freedom drop test rig (Figs. 5-12, 5-13) of the Bendix spacecraft model dynamic drop test laboratory")
penetrator = ("scaled LM footpads on all four legs (text 5-4; round simulated LM footpads, text 5-33); No. 1 footpad instrumented, "
              "on a non-yawing universal joint, the other three on ball joints; pad angle limited to 24 degrees, set against the stop "
              "two degrees up at touchdown (text 5-9); footpad diameter not printed in Section V")
loading_common = ("free-body landing after release from the drop rig on a level landing surface (zero slope); zero angular rates, "
                  "zero pitch and roll, 45-degree yaw (2-2 landings) (text 5-44); total model weight 68.4 Lbs. (text 5-22); "
                  "two nominal conditions: pure vertical drop at nominal V_v ten (printed teen) feet per second, or nominal V_v five "
                  "and V_h seven feet per second (text 5-44); Table 5-T2: V_V, V_H 10, 0 or 5, 7 (no unit printed), ground slope 0, yaw 45")
bin_rs = ("18 by 12 by 5 ft (soil bed 18 feet long and 12 feet wide, maximum below ground depth five feet, soil depth adjusted to "
          "the test, text 5-22); RS intermediate beds 18 inches thick (text 5-44); depth of the loose beds not printed")
bin_ss = ("18 by 12 by 5 ft (soil bed 18 feet long and 12 feet wide, maximum below ground depth five feet, soil depth adjusted to "
          "the test, text 5-22); depth of the SS loose beds not printed")
chan_common = ("per drop (table): V_v and V_h (In./Sec.) calculated from tau; tau (Sec.), release to touchdown, measured from the "
               "x accelerometer record; bed D_r, gamma (Lb./Ft.^3), phi (Deg.)")
chan_rs = (chan_common + "; Section V prints time histories only for NASA Tests 1 and 2 (Bendix drops 10 and 11): absolute footpad "
           "velocity, footpad heading theta, footpad penetration depth, axial loads on struts 1 to 3, CG vertical acceleration, "
           "velocity and displacement (Figs. 5-22 to 5-28, Test 1; Figs. 5-29 to 5-35, Test 2) and for Test 2 also CG horizontal "
           "velocity and displacement, vehicle pitch velocity and pitch angle (Figs. 5-36 to 5-39); none for Tests 3 to 6")
chan_ss = chan_common + "; Section V prints no loads, penetration or accelerations for Tests 7 and 8"

text_common = ["text 5-2 (PDF 281)", "text 5-4 (PDF 283)", "text 5-9 (PDF 289)", "text 5-17 (PDF 297)", "text 5-18 (PDF 298)", "text 5-22 (PDF 302)",
               "text 5-33 (PDF 313)", "text 5-38 (PDF 318)", "text 5-39 (PDF 319)", "text 5-41 (PDF 321)", "text 5-43 (PDF 323)",
               "text 5-44 (PDF 324)", "text 5-46 (PDF 326)"]
figs_common = ["F5-1", "F5-2", "F5-3", "F5-5", "F5-6", "F5-9", "F5-10", "F5-11", "F5-12", "F5-13", "F5-21", "T5-1", "T5-2", "T5-3"]
figs_rs = figs_common + [f"F5-{n}" for n in range(22, 40)]
figs_ss = figs_common + ["T2-3"]

def ev(figs):
    def key(s):
        p, n = s[0], s[1:]
        a, b = n.split("-")
        return (p, int(a), int(b))
    return ";".join(sorted(figs, key=key) + text_common)

missing = ("setup_incomplete: footpad diameter and mass not printed in Section V; depth of the loose beds not printed; test "
           "gravity not stated (Table 5-T1 scale factors imply 1 g model drops); formula and g used to calculate V_v, V_h from tau not printed")

rs = {
    "experiment_id": "b68-mdrop-t5-3-rs", "source_id": "bendix-1968-vol1", "kind": "run-table", "test_type": "mdrop",
    "test_label_printed": "DETAIL CORRELATION DROPS", "soil_family": "RS", "soil_no": "", "soil_no_status": "unknown",
    "state_printed": "RS Loose; RS Intermediate", "dr_printed": "0 to .3", "unit_weight_printed_pcf": "46.9 to 53.0",
    "gp_printed_g": "", "apparatus": apparatus, "penetrator_printed": penetrator, "bin_printed_in": bin_rs,
    "loading": loading_common + "; RS beds: NASA Tests 1, 4, 6 vertical, Tests 2, 3, 5 vertical plus horizontal",
    "rate_printed": "V_v -117.3 to -60.0 In./Sec.; V_h 0 to 84.0 In./Sec.", "start_depth_printed_in": "",
    "measured_channels": chan_rs, "evidence": ev(figs_rs), "setup_status": "setup_incomplete", "mcc_relevant": "no",
    "priority": "1", "relation": "same-as", "relation_target": "b68-mdrop-10;b68-mdrop-11",
    "notes": ("6 drops: NASA Tests 1 to 6 = Bendix drops 10, 11, 12, 13, 16, 17 (Table 5-T2: NASA Drop No. 1 to 6); 4 on RS Loose, "
              "2 on RS Intermediate; Test 4 duplicates Test 1 and Test 3 duplicates Test 2 (text 5-46). Printed differently: Table 5-T2 "
              "D_r 0.3 (T5-3 .3) and nominal V_V, V_H; Fig. 5-25 inset V_v = -114.93 in. sec. for Test 1 (T5-3 -114.9); Fig. 5-32 inset "
              "V_v = -?0.55, V_h = ?3.75 In. Sec. for Test 2 (T5-3 -60.5, 83.5; first digits broken). Bed gamma and phi differ from "
              "Table 2-3 RS Loose (41.4 pcf, 40 deg) and RS Inter. (.45, 45.9 pcf, 44.5 deg). Text 5-44: after each drop the soil was completely removed "
              "before a new bed was prepared; no reuse stated. " + missing),
}
ss = dict(rs)
ss.update({
    "experiment_id": "b68-mdrop-t5-3-ss", "soil_family": "SS", "soil_no": "7", "soil_no_status": "inferred",
    "state_printed": "SS Loose", "dr_printed": "0", "unit_weight_printed_pcf": "96.0", "bin_printed_in": bin_ss,
    "loading": loading_common + "; SS beds: NASA Test 8 vertical, Test 7 vertical plus horizontal",
    "rate_printed": "V_v -118.0 to -60.0 In./Sec.; V_h 0 to 84.0 In./Sec.", "measured_channels": chan_ss,
    "evidence": ev(figs_ss), "relation": "", "relation_target": "",
    "notes": ("2 drops: NASA Tests 7 and 8 = Bendix drops 20 and 21 (Table 5-T2: NASA Drop No. 7 and 8), SS Loose. soil_no 7 "
              "matched by family and state (Table 2-3 SS Loose); T5-3 gamma 96.0 and phi 30 differ from Table 2-3 soil 7 (94.7 pcf, "
              "29 deg). Table 5-T2 prints the same D_r, gamma, phi and nominal V_V, V_H 5, 7 and 10, 0; the repeated SS Loose drops 18 "
              "(Bad recording) and 19 (Bad release) print 95.2 pcf. Text 5-44: after each drop the soil was completely removed before a new bed was prepared; no reuse stated. " + missing),
})
with open("out/experiments.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    w.writeheader(); w.writerow(rs); w.writerow(ss)
for r in csv.DictReader(open("out/experiments.csv", encoding="utf-8")):
    print(len(r), r["experiment_id"]); print(r["evidence"])
