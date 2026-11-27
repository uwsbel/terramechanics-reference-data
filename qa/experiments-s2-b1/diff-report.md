# Table diff: claude vs codex

Files: `qa/experiments-s2-b1/aligned-claude.csv` (claude), `extractions/codex/experiments-s2-b1/experiments-codex.csv` (codex). Key: `experiment_id`.

Rows: 139 in claude, 180 in codex. Compared columns: 17.
Cells compared: 2244. Agreed: 1605 (71.5 percent).
Disagreements: 694 (90 numeric, 549 text, 55 missing rows).

| key | column | kind | claude | codex |
|---|---|---|---|---|
| b68-dens-13 | state_printed | text | used RS soil | used |
| b68-dens-13 | unit_weight_printed_pcf | text | 50 to 56 (range of axis) |  |
| b68-dens-13 | penetrator_printed | text |  | 1-1/4 inch diameter tamping foot |
| b68-dens-13 | bin_printed_in | text | Proctor mold 1/30 cu ft |  |
| b68-dens-13 | evidence | text | F2-18 | F2-18;text 2-38 (PDF 63) |
| b68-dens-14 | state_printed | text | used RS soil | used |
| b68-dens-14 | penetrator_printed | text |  | 1-1/4 inch diameter tamping foot |
| b68-dens-14 | bin_printed_in | text | Proctor mold 1/30 cu ft |  |
| b68-dens-14 | evidence | text | F2-18 | F2-18;text 2-38 (PDF 63) |
| b68-dens-15 | state_printed | text | used RS soil | used |
| b68-dens-15 | penetrator_printed | text |  | 1-1/4 inch diameter tamping foot |
| b68-dens-15 | bin_printed_in | text | Proctor mold 1/30 cu ft |  |
| b68-dens-15 | evidence | text | F2-18 | F2-18;text 2-38 (PDF 63) |
| b68-lpt-022 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-022 | rate_printed | text | 4 in/min | 4"/min. |
| b68-lpt-023 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-023 | rate_printed | text | 1 in/min | 1"/min. |
| b68-lpt-024 | dr_printed | text |  | about 0.96 |
| b68-lpt-024 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-024 | bin_printed_in | text | 18 by 36 | 18 Inch by 36 Inch |
| b68-lpt-024 | rate_printed | text | 1 in/min | 1"/min. |
| b68-lpt-024 | evidence | text | F2-42;F2-44 | F2-42;F2-44;text 2-74 (PDF 99);text 2-56 (PDF 81) |
| b68-lpt-024 | setup_status | text | setup_incomplete | complete |
| b68-lpt-025 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-025 | rate_printed | text | 2 in/min | 2"/min. |
| b68-lpt-026 | state_printed | text | RS Intermediate (F2-43) vs RS Dense 52.0 pcf (F2-54 record 54-65) | RS Intermediate; RS-Dense |
| b68-lpt-026 | unit_weight_printed_pcf | number | 52.0 (F2-54) | 52.0 |
| b68-lpt-026 | penetrator_printed | text | 2 inch cylinder | Two-Inch Cylinder |
| b68-lpt-026 | rate_printed | text | 2 in/min | 2 In./Min. |
| b68-lpt-027 | state_printed | text | RS Dense (F2-29) vs RS Intermediate (F2-43) | Dense; Intermediate |
| b68-lpt-027 | penetrator_printed | text | 2 inch cylinder | 2" Diameter Cylinder |
| b68-lpt-027 | rate_printed | text | 1/2 in/min | 1/2" Per Min.; 0.5 In./Min. |
| b68-lpt-028 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-028 | rate_printed | text | 0.5 in/min | 0.5 In./Min. |
| b68-lpt-028 | priority | number | 1 | 2 |
| b68-lpt-029 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-029 | rate_printed | text | 2 in/min | 2 In./Min. |
| b68-lpt-029 | priority | number | 1 | 2 |
| b68-lpt-052 | state_printed | text | RS Loose (Soil No. 1) | RS Loose |
| b68-lpt-052 | dr_printed | number | 0.0 | approx 0.0 |
| b68-lpt-052 | penetrator_printed | text | 2 inch cylinder | Two-Inch Diameter Cylinder |
| b68-lpt-052 | start_depth_printed_in | number | 2 | 1 |
| b68-lpt-052 | evidence | text | F2-32 | F2-32;text 2-61 (PDF 86) |
| b68-lpt-053 | state_printed | text | RS Loose (Soil No. 1) | RS Loose |
| b68-lpt-053 | dr_printed | number | 0.0 | approx 0.0 |
| b68-lpt-053 | penetrator_printed | text | 2 inch cylinder | Two-Inch Diameter Cylinder |
| b68-lpt-053 | start_depth_printed_in | number | 1 | 2 |
| b68-lpt-053 | evidence | text | F2-32 | F2-32;text 2-61 (PDF 86) |
| b68-lpt-063 | <row> | missing | present | absent |
| b68-lpt-069 | soil_no | number | 4 |  |
| b68-lpt-069 | soil_no_status | text | inferred | unknown |
| b68-lpt-069 | dr_printed | text | approx 0.96 | about 0.96 |
| b68-lpt-069 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-069 | bin_printed_in | text | 54 by 36 | 54 Inch by 36 Inch |
| b68-lpt-069 | evidence | text | F2-44 | F2-44;text 2-74 (PDF 99) |
| b68-lpt-073 | soil_no | number | 4 |  |
| b68-lpt-073 | soil_no_status | text | inferred | unknown |
| b68-lpt-073 | dr_printed | text | approx 0.97 | approx 0.97; about 0.96 |
| b68-lpt-073 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-073 | bin_printed_in | text | 18 by 36 | 18 Inches by 36 Inches |
| b68-lpt-073 | evidence | text | F2-35;F2-44 | F2-35;F2-44;text 2-74 (PDF 99) |
| b68-lpt-074 | soil_no | number | 4 |  |
| b68-lpt-074 | soil_no_status | text | inferred | unknown |
| b68-lpt-074 | dr_printed | text | approx 0.94 | approx 0.94; about 0.96 |
| b68-lpt-074 | penetrator_printed | text | 4 inch cylinder | Four-Inch Dia. Cyl. |
| b68-lpt-074 | bin_printed_in | text | 36 by 36 | 36" by 36" |
| b68-lpt-074 | evidence | text | F2-33;F2-44 | F2-33;F2-44;text 2-74 (PDF 99) |
| b68-lpt-075 | soil_no | number | 4 |  |
| b68-lpt-075 | soil_no_status | text | inferred | unknown |
| b68-lpt-075 | penetrator_printed | text | 4 inch cylinder | Four-Inch Dia. Cyl. |
| b68-lpt-075 | bin_printed_in | text | 36 by 36 | 36" by 36" |
| b68-lpt-076 | soil_no | number | 4 |  |
| b68-lpt-076 | soil_no_status | text | inferred | unknown |
| b68-lpt-076 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-076 | bin_printed_in | text | 18 by 36 | 18 Inches by 36 Inches |
| b68-lpt-079 | state_printed | text | RS Loose (Soil No. 1) | RS Loose |
| b68-lpt-079 | penetrator_printed | text | 4 inch footpad | Four-Inch Footpad |
| b68-lpt-085 | state_printed | text | SS Dense (Soil No. 9) | SS Dense |
| b68-lpt-085 | penetrator_printed | text | 4 inch footpad | Four-Inch Footpad |
| b68-lpt-087 | state_printed | text | SS Dense (Soil No. 9) | SS Dense |
| b68-lpt-087 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-087 | bin_printed_in | text | 108 by 36 | 108 Inches by 36 Inches |
| b68-lpt-088 | state_printed | text | SS Dense (Soil No. 9) |  |
| b68-lpt-088 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-088 | bin_printed_in | text | 108 by 36 | 108 Inches by 36 Inches |
| b68-lpt-089 | state_printed | text | RS Intermediate (Soil No. 3) | RS Intermediate |
| b68-lpt-089 | penetrator_printed | text | 4 inch footpad | Four-Inch Footpad |
| b68-lpt-091 | state_printed | text | RS Dense (Soil No. 4) | RS Dense |
| b68-lpt-091 | penetrator_printed | text | 4 inch footpad | Four-Inch Footpad |
| b68-lpt-093 | <row> | missing | absent | present |
| b68-lpt-095 | state_printed | text | RS Loose (Soil No. 1) | RS Loose |
| b68-lpt-095 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-098 | state_printed | text | RS Intermediate (Soil No. 3) | RS Intermediate |
| b68-lpt-098 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-101 | state_printed | text | RS Dense (Soil No. 4) | RS Dense |
| b68-lpt-101 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-064a | soil_no | number | 4 |  |
| b68-lpt-064a | soil_no_status | text | inferred | unknown |
| b68-lpt-064a | dr_printed | text | approx 0.96 | about 0.96 |
| b68-lpt-064a | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-064a | bin_printed_in | text | 54 by 36 | 54 Inch by 36 Inch |
| b68-lpt-064a | evidence | text | F2-44 | F2-44;text 2-74 (PDF 99) |
| b68-dpt-r53958 | state_printed | text | RS Loose 41.1 pcf | RS-Loose |
| b68-dpt-r53958 | penetrator_printed | text |  | 2-3/4 inches diameter; full radius nose |
| b68-dpt-r53958 | bin_printed_in | text | 2 ft box | 2' Box |
| b68-dpt-r53958 | evidence | text | F2-54 | F2-53;F2-54;text 2-90 (PDF 115) |
| b68-dpt-r54-65 | state_printed | text | RS Dense 52.0 pcf (F2-54) vs RS Intermediate (LPT 26 caption F2-43) | RS-Dense |
| b68-dpt-r54-65 | penetrator_printed | text |  | 2-3/4 inches diameter; full radius nose |
| b68-dpt-r54-65 | bin_printed_in | text | LPT bin |  |
| b68-dpt-r54-65 | evidence | text | F2-54;F2-43 | F2-53;F2-54;text 2-90 (PDF 115) |
| b68-dpt-r54025 | state_printed | text | RS Intermediate 44.1 pcf | RS-Intermediate |
| b68-dpt-r54025 | penetrator_printed | text |  | 2-3/4 inches diameter; full radius nose |
| b68-dpt-r54025 | bin_printed_in | text | 2 ft box | 2' Box |
| b68-dpt-r54025 | evidence | text | F2-54 | F2-53;F2-54;text 2-90 (PDF 115) |
| b68-dpt-r54074 | <row> | missing | present | absent |
| b68-ds-t2-3-10 | <row> | missing | absent | present |
| b68-ds-t2-3-11 | <row> | missing | absent | present |
| b68-gs-ssd-6-1 | kind | text | single | sample |
| b68-gs-ssd-6-1 | soil_no | number | 6 |  |
| b68-gs-ssd-6-1 | soil_no_status | text | reported | unknown |
| b68-gs-ssd-6-1 | state_printed | text | used RC2 soil (drag bed 6-1) | used for test bed |
| b68-gs-ssd-6-1 | setup_status | text | complete | setup_incomplete |
| b68-gs-t2-3-12 | <row> | missing | absent | present |
| b68-sonic-t2-3 | <row> | missing | present | absent |
| b68-ds-f2-22-rs | state_printed | text | RS Intermediate (Dr approx 0.55; gamma avg 46.9 pcf) |  |
| b68-ds-f2-22-rs | rate_printed | text |  | approx 0.07 In./Min. |
| b68-ds-f2-22-rs | evidence | text | F2-22 | F2-21;F2-22 |
| b68-ds-f2-22-rs | setup_status | text | pending | setup_incomplete |
| b68-ds-f2-22-rs | priority | number | 2 | 1 |
| b68-ds-f2-23-ps | kind | text | derived-series | correlation |
| b68-ds-f2-23-ps | state_printed | text | all states |  |
| b68-ds-f2-23-ps | dr_printed | text | 0 to 1.0 |  |
| b68-ds-f2-23-ps | rate_printed | text |  | approx 0.07 In./Min. |
| b68-ds-f2-23-ps | evidence | text | F2-23 | F2-23;text 2-45 (PDF 70) |
| b68-ds-f2-23-rs | kind | text | derived-series | correlation |
| b68-ds-f2-23-rs | state_printed | text | all states |  |
| b68-ds-f2-23-rs | dr_printed | text | 0 to 1.0 |  |
| b68-ds-f2-23-rs | rate_printed | text |  | approx 0.07 In./Min. |
| b68-ds-f2-23-rs | evidence | text | F2-23 | F2-23;text 2-45 (PDF 70) |
| b68-ds-f2-23-ss | kind | text | derived-series | correlation |
| b68-ds-f2-23-ss | state_printed | text | all states |  |
| b68-ds-f2-23-ss | dr_printed | text | 0 to 1.0 |  |
| b68-ds-f2-23-ss | rate_printed | text |  | approx 0.07 In./Min. |
| b68-ds-f2-23-ss | evidence | text | F2-23 | F2-23;text 2-45 (PDF 70) |
| b68-gs-f2-14-ps | soil_no | number | 2 |  |
| b68-gs-f2-14-ps | soil_no_status | text | inferred | unknown |
| b68-gs-f2-14-ps | state_printed | text |  | previously unused; undegraded |
| b68-gs-f2-14-rs | soil_no | number | 1 |  |
| b68-gs-f2-14-rs | soil_no_status | text | inferred | unknown |
| b68-gs-f2-14-rs | state_printed | text |  | previously unused; undegraded |
| b68-gs-f2-14-ss | soil_no | number | 7 |  |
| b68-gs-f2-14-ss | soil_no_status | text | inferred | unknown |
| b68-gs-f2-14-ss | state_printed | text |  | previously unused; undegraded |
| b68-smp-ssd-1-1 | soil_no | number | 1 |  |
| b68-smp-ssd-1-1 | soil_no_status | text | reported | unknown |
| b68-smp-ssd-1-1 | state_printed | text | unused | Unused soil |
| b68-smp-ssd-1-1 | unit_weight_printed_pcf | text | 41.1 to 53.6 | min 41.1; max 53.6 |
| b68-smp-ssd-1-1 | evidence | text | F2-56 | F2-56;text 2-94 (PDF 119);text 2-98 (PDF 123) |
| b68-smp-ssd-1-1 | setup_status | text | pending | setup_incomplete |
| b68-smp-ssd-3-1 | soil_no_status | text | reported | unknown |
| b68-smp-ssd-3-1 | state_printed | text | used; shoveled | Shoveled soil |
| b68-smp-ssd-3-1 | unit_weight_printed_pcf | text | 44.8 to 55.2 | min 44.8; max 55.2 |
| b68-smp-ssd-3-1 | evidence | text | F2-56 | F2-56;text 2-94 (PDF 119);text 2-98 (PDF 123) |
| b68-smp-ssd-3-1 | setup_status | text | pending | setup_incomplete |
| b68-smp-ssd-4-3 | soil_no_status | text | reported | unknown |
| b68-smp-ssd-4-3 | state_printed | text | used; 31 cycles | 31 cycles |
| b68-smp-ssd-4-3 | unit_weight_printed_pcf | text | 61.1 to 72.8 | min 61.1; max 72.8 |
| b68-smp-ssd-4-3 | evidence | text | F2-56 | F2-56;text 2-94 (PDF 119);text 2-98 (PDF 123) |
| b68-smp-ssd-4-3 | setup_status | text | pending | setup_incomplete |
| b68-smp-ssd-5-1 | soil_no_status | text | reported | unknown |
| b68-smp-ssd-5-1 | state_printed | text | used; 2 cycles | 2 cycles through vacuum system |
| b68-smp-ssd-5-1 | unit_weight_printed_pcf | text | 58.0 to 70.4 | min 64.4; max 75.3 |
| b68-smp-ssd-5-1 | evidence | text | F2-58 | F2-58;text 2-94 (PDF 119);text 2-98 (PDF 123) |
| b68-smp-ssd-5-1 | setup_status | text | pending | setup_incomplete |
| b68-smp-ssd-5-6 | soil_no_status | text | reported | unknown |
| b68-smp-ssd-5-6 | state_printed | text | used; 8 cycles | 8 cycles |
| b68-smp-ssd-5-6 | unit_weight_printed_pcf | text | 64.4 to 75.3 | min 62.9; max 74.4 |
| b68-smp-ssd-5-6 | evidence | text | F2-58 | F2-58;text 2-94 (PDF 119);text 2-98 (PDF 123) |
| b68-smp-ssd-5-6 | setup_status | text | pending | setup_incomplete |
| b68-dpt-f2-55-ps | state_printed | text | all states |  |
| b68-dpt-f2-55-ps | dr_printed | text | 0 to 1.0 |  |
| b68-dpt-f2-55-ps | penetrator_printed | text |  | 2-3/4 inches diameter; full radius nose |
| b68-dpt-f2-55-ps | bin_printed_in | text | calibration bins |  |
| b68-dpt-f2-55-ps | evidence | text | F2-55 | F2-53;F2-55;text 2-90 (PDF 115) |
| b68-dpt-f2-55-rs | state_printed | text | all states |  |
| b68-dpt-f2-55-rs | dr_printed | text | 0 to 1.0 |  |
| b68-dpt-f2-55-rs | penetrator_printed | text |  | 2-3/4 inches diameter; full radius nose |
| b68-dpt-f2-55-rs | bin_printed_in | text | calibration bins |  |
| b68-dpt-f2-55-rs | evidence | text | F2-55 | F2-53;F2-55;text 2-90 (PDF 115) |
| b68-dpt-f2-55-ss | state_printed | text | all states |  |
| b68-dpt-f2-55-ss | dr_printed | text | 0 to 1.0 |  |
| b68-dpt-f2-55-ss | penetrator_printed | text |  | 2-3/4 inches diameter; full radius nose |
| b68-dpt-f2-55-ss | bin_printed_in | text | calibration bins |  |
| b68-dpt-f2-55-ss | evidence | text | F2-55 | F2-53;F2-55;text 2-90 (PDF 115) |
| b68-ds-f2-23-rc2 | kind | text | derived-series | correlation |
| b68-ds-f2-23-rc2 | state_printed | text | all states |  |
| b68-ds-f2-23-rc2 | dr_printed | text | 0 to 1.0 |  |
| b68-ds-f2-23-rc2 | rate_printed | text |  | approx 0.07 In./Min. |
| b68-ds-f2-23-rc2 | evidence | text | F2-23 | F2-23;text 2-45 (PDF 70) |
| b68-gs-f2-14-lsm | soil_no | number | 10 |  |
| b68-gs-f2-14-lsm | soil_no_status | text | inferred | unknown |
| b68-gs-f2-14-lsm | state_printed | text |  | previously unused; undegraded |
| b68-gs-f2-14-rc2 | soil_no | number | 6 |  |
| b68-gs-f2-14-rc2 | soil_no_status | text | inferred | unknown |
| b68-gs-f2-14-rc2 | state_printed | text |  | previously unused; undegraded |
| b68-smp-ssd-2-10 | soil_no_status | text | reported | unknown |
| b68-smp-ssd-2-10 | state_printed | text | used; 10 cycles | 10 cycles through vacuum system |
| b68-smp-ssd-2-10 | unit_weight_printed_pcf | text | 27.3 to 34.2 | min 27.3; max 34.2 |
| b68-smp-ssd-2-10 | evidence | text | F2-57 | F2-57;text 2-94 (PDF 119);text 2-98 (PDF 123) |
| b68-smp-ssd-2-10 | setup_status | text | pending | setup_incomplete |
| b68-smp-ssd-2-41 | soil_no_status | text | reported | unknown |
| b68-smp-ssd-2-41 | state_printed | text | used; 13 cycles plus shoveling | 13 cycles plus shoveled for 27 tests |
| b68-smp-ssd-2-41 | unit_weight_printed_pcf | text | 27.2 to 33.8 | min 27.2; max 33.8 |
| b68-smp-ssd-2-41 | evidence | text | F2-57 | F2-57;text 2-94 (PDF 119);text 2-98 (PDF 123) |
| b68-smp-ssd-2-41 | setup_status | text | pending | setup_incomplete |
| b68-smp-ssd-3-10 | soil_no_status | text | reported | unknown |
| b68-smp-ssd-3-10 | state_printed | text | used; 10 cycles through the vacuum system | 10 cycles through vacuum system |
| b68-smp-ssd-3-10 | unit_weight_printed_pcf | text | 51.1 to 63.3 | min 51.1; max 63.3 |
| b68-smp-ssd-3-10 | evidence | text | F2-56 | F2-56;text 2-94 (PDF 119);text 2-98 (PDF 123) |
| b68-smp-ssd-3-10 | setup_status | text | pending | setup_incomplete |
| b68-smp-ssd-4-18 | soil_no_status | text | reported | unknown |
| b68-smp-ssd-4-18 | state_printed | text | used; 46 cycles | 46 cycles |
| b68-smp-ssd-4-18 | unit_weight_printed_pcf | text | 63.6 to 76.6 | min 63.6; max 76.6 |
| b68-smp-ssd-4-18 | evidence | text | F2-56 | F2-56;text 2-94 (PDF 119);text 2-98 (PDF 123) |
| b68-smp-ssd-4-18 | setup_status | text | pending | setup_incomplete |
| b68-smp-ssd-4-26 | soil_no_status | text | reported | unknown |
| b68-smp-ssd-4-26 | state_printed | text | used; 54 cycles | 54 cycles |
| b68-smp-ssd-4-26 | unit_weight_printed_pcf | text | 62.3 to 74.2 | min 62.3; max 74.2 |
| b68-smp-ssd-4-26 | evidence | text | F2-56 | F2-56;text 2-94 (PDF 119);text 2-98 (PDF 123) |
| b68-smp-ssd-4-26 | setup_status | text | pending | setup_incomplete |
| b68-smp-ssd-5-15 | soil_no_status | text | reported | unknown |
| b68-smp-ssd-5-15 | state_printed | text | used; 17 cycles | 17 cycles |
| b68-smp-ssd-5-15 | unit_weight_printed_pcf | text | 62.9 to 74.4 | min 72.9; max 86.2 |
| b68-smp-ssd-5-15 | evidence | text | F2-58 | F2-58;text 2-94 (PDF 119);text 2-98 (PDF 123) |
| b68-smp-ssd-5-15 | setup_status | text | pending | setup_incomplete |
| b68-smp-ssd-5-23 | soil_no_status | text | reported | unknown |
| b68-smp-ssd-5-23 | state_printed | text | used; 25 cycles | 25 cycles |
| b68-smp-ssd-5-23 | unit_weight_printed_pcf | text | 72.9 to 87.3 | min 74.3; max 87.3 |
| b68-smp-ssd-5-23 | evidence | text | F2-58 | F2-58;text 2-94 (PDF 119);text 2-98 (PDF 123) |
| b68-smp-ssd-5-23 | setup_status | text | pending | setup_incomplete |
| b68-sonic-t2-3-1 | <row> | missing | absent | present |
| b68-sonic-t2-3-2 | <row> | missing | absent | present |
| b68-sonic-t2-3-3 | <row> | missing | absent | present |
| b68-sonic-t2-3-4 | <row> | missing | absent | present |
| b68-sonic-t2-3-5 | <row> | missing | absent | present |
| b68-sonic-t2-3-6 | <row> | missing | absent | present |
| b68-sonic-t2-3-7 | <row> | missing | absent | present |
| b68-sonic-t2-3-8 | <row> | missing | absent | present |
| b68-sonic-t2-3-9 | <row> | missing | absent | present |
| b68-dens-mmdt-lsm | <row> | missing | present | absent |
| b68-dpt-f2-55-lsm | state_printed | text | all states |  |
| b68-dpt-f2-55-lsm | dr_printed | text | 0 to 1.0 |  |
| b68-dpt-f2-55-lsm | penetrator_printed | text |  | 2-3/4 inches diameter; full radius nose |
| b68-dpt-f2-55-lsm | bin_printed_in | text | calibration bins |  |
| b68-dpt-f2-55-lsm | evidence | text | F2-55 | F2-53;F2-55;text 2-90 (PDF 115) |
| b68-dpt-f2-55-rc2 | state_printed | text | all states |  |
| b68-dpt-f2-55-rc2 | dr_printed | text | 0 to 1.0 |  |
| b68-dpt-f2-55-rc2 | penetrator_printed | text |  | 2-3/4 inches diameter; full radius nose |
| b68-dpt-f2-55-rc2 | bin_printed_in | text | calibration bins |  |
| b68-dpt-f2-55-rc2 | evidence | text | F2-55 | F2-53;F2-55;text 2-90 (PDF 115) |
| b68-dpt-f2-55-rsm | state_printed | text | all states |  |
| b68-dpt-f2-55-rsm | dr_printed | text | 0 to 1.0 |  |
| b68-dpt-f2-55-rsm | penetrator_printed | text |  | 2-3/4 inches diameter; full radius nose |
| b68-dpt-f2-55-rsm | bin_printed_in | text | calibration bins |  |
| b68-dpt-f2-55-rsm | evidence | text | F2-55 | F2-53;F2-55;text 2-90 (PDF 115) |
| b68-ds-f2-21-n294 | state_printed | text | RS Intermediate |  |
| b68-ds-f2-21-n294 | dr_printed | text | 0.5 to 0.57 | .5 to .57 |
| b68-ds-f2-21-n294 | rate_printed | text | approx 0.07 in/min | approx 0.07 In./Min. |
| b68-ds-f2-21-n294 | evidence | text | F2-21;F2-22 | F2-20;F2-21;F2-22;text 2-40 (PDF 65) |
| b68-ds-f2-21-n587 | state_printed | text | RS Intermediate |  |
| b68-ds-f2-21-n587 | dr_printed | text | 0.5 to 0.57 | .5 to .57 |
| b68-ds-f2-21-n587 | rate_printed | text | approx 0.07 in/min | approx 0.07 In./Min. |
| b68-ds-f2-21-n587 | evidence | text | F2-21;F2-22 | F2-20;F2-21;F2-22;text 2-40 (PDF 65) |
| b68-lpt-f2-31-s01 | <row> | missing | absent | present |
| b68-lpt-f2-31-s02 | <row> | missing | absent | present |
| b68-lpt-f2-31-s03 | <row> | missing | absent | present |
| b68-lpt-f2-31-s04 | <row> | missing | absent | present |
| b68-lpt-f2-31-s05 | <row> | missing | absent | present |
| b68-lpt-f2-31-s06 | <row> | missing | absent | present |
| b68-lpt-f2-36-s01 | state_printed | text | RS Dense |  |
| b68-lpt-f2-36-s01 | penetrator_printed | text | 2 inch cylinder | 2" Cyl. |
| b68-lpt-f2-36-s01 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-36-s01 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-36-s01 | evidence | text | F2-36 | F2-36;text 2-69 (PDF 94) |
| b68-lpt-f2-36-s02 | state_printed | text | RS Dense |  |
| b68-lpt-f2-36-s02 | penetrator_printed | text | 4 inch cylinder | 4" Cyl. |
| b68-lpt-f2-36-s02 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-36-s02 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-36-s02 | evidence | text | F2-36 | F2-36;text 2-69 (PDF 94) |
| b68-lpt-f2-36-s03 | state_printed | text | RS Intermediate |  |
| b68-lpt-f2-36-s03 | penetrator_printed | text | 4 inch cylinder | 4" Cyl. |
| b68-lpt-f2-36-s03 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-36-s03 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-36-s03 | evidence | text | F2-36 | F2-36;text 2-69 (PDF 94) |
| b68-lpt-f2-36-s04 | state_printed | text | RS Intermediate |  |
| b68-lpt-f2-36-s04 | penetrator_printed | text | 2 inch cylinder | 2" Cyl. |
| b68-lpt-f2-36-s04 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-36-s04 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-36-s04 | evidence | text | F2-36 | F2-36;text 2-69 (PDF 94) |
| b68-lpt-f2-36-s04 | mcc_relevant | text | no | yes |
| b68-lpt-f2-36-s05 | state_printed | text | RS Loose |  |
| b68-lpt-f2-36-s05 | penetrator_printed | text | 4 inch cylinder | 4" Cyl. |
| b68-lpt-f2-36-s05 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-36-s05 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-36-s05 | evidence | text | F2-36 | F2-36;text 2-69 (PDF 94) |
| b68-lpt-f2-36-s06 | state_printed | text | RS Loose |  |
| b68-lpt-f2-36-s06 | penetrator_printed | text | 2 inch cylinder | 2" Cyl. |
| b68-lpt-f2-36-s06 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-36-s06 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-36-s06 | evidence | text | F2-36 | F2-36;text 2-69 (PDF 94) |
| b68-lpt-f2-37-s01 | kind | text | averaged-series | single |
| b68-lpt-f2-37-s01 | state_printed | text | RS Dense |  |
| b68-lpt-f2-37-s01 | penetrator_printed | text | 2 inch cylinder | 2" Cyl. |
| b68-lpt-f2-37-s01 | bin_printed_in | text | 54 by 36 | 54" x 36" |
| b68-lpt-f2-37-s01 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-37-s01 | evidence | text | F2-37 | F2-37;text 2-69 (PDF 94) |
| b68-lpt-f2-37-s01 | setup_status | text | pending | setup_incomplete |
| b68-lpt-f2-37-s02 | kind | text | averaged-series | single |
| b68-lpt-f2-37-s02 | state_printed | text | RS Dense |  |
| b68-lpt-f2-37-s02 | penetrator_printed | text | 2 inch cylinder | 2" Cyl. |
| b68-lpt-f2-37-s02 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-37-s02 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-37-s02 | evidence | text | F2-37 | F2-37;text 2-69 (PDF 94) |
| b68-lpt-f2-37-s02 | setup_status | text | pending | setup_incomplete |
| b68-lpt-f2-37-s03 | kind | text | averaged-series | single |
| b68-lpt-f2-37-s03 | soil_no | number | 4 |  |
| b68-lpt-f2-37-s03 | soil_no_status | text | inferred | unknown |
| b68-lpt-f2-37-s03 | state_printed | text | RS Dense |  |
| b68-lpt-f2-37-s03 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-37-s03 | evidence | text | F2-37 | F2-37;text 2-69 (PDF 94) |
| b68-lpt-f2-37-s03 | setup_status | text | pending | setup_incomplete |
| b68-lpt-f2-37-s04 | kind | text | averaged-series | single |
| b68-lpt-f2-37-s04 | state_printed | text | RS Dense |  |
| b68-lpt-f2-37-s04 | penetrator_printed | text | 4 inch cylinder | 4" Cyl. |
| b68-lpt-f2-37-s04 | bin_printed_in | text | 54 by 36 | 54" x 36" |
| b68-lpt-f2-37-s04 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-37-s04 | evidence | text | F2-37 | F2-37;text 2-69 (PDF 94) |
| b68-lpt-f2-37-s04 | setup_status | text | pending | setup_incomplete |
| b68-lpt-f2-37-s05 | kind | text | averaged-series | single |
| b68-lpt-f2-37-s05 | state_printed | text | RS Dense |  |
| b68-lpt-f2-37-s05 | penetrator_printed | text | 4 inch cylinder | 4" Cyl. |
| b68-lpt-f2-37-s05 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-37-s05 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-37-s05 | evidence | text | F2-37 | F2-37;text 2-69 (PDF 94) |
| b68-lpt-f2-37-s05 | setup_status | text | pending | setup_incomplete |
| b68-lpt-f2-37-s06 | kind | text | averaged-series | single |
| b68-lpt-f2-37-s06 | soil_no | number | 4 |  |
| b68-lpt-f2-37-s06 | soil_no_status | text | inferred | unknown |
| b68-lpt-f2-37-s06 | state_printed | text | RS Dense |  |
| b68-lpt-f2-37-s06 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-37-s06 | evidence | text | F2-37 | F2-37;text 2-69 (PDF 94) |
| b68-lpt-f2-37-s06 | setup_status | text | pending | setup_incomplete |
| b68-lpt-f2-37-s07 | kind | text | averaged-series | single |
| b68-lpt-f2-37-s07 | state_printed | text | RS Dense |  |
| b68-lpt-f2-37-s07 | penetrator_printed | text | 1 inch cylinder | 1" Cyl. |
| b68-lpt-f2-37-s07 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-37-s07 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-37-s07 | evidence | text | F2-37 | F2-37;text 2-69 (PDF 94) |
| b68-lpt-f2-37-s07 | setup_status | text | pending | setup_incomplete |
| b68-lpt-f2-37-s08 | kind | text | averaged-series | single |
| b68-lpt-f2-37-s08 | state_printed | text | RS Dense |  |
| b68-lpt-f2-37-s08 | penetrator_printed | text | 4 inch cylinder | 4" Cyl. |
| b68-lpt-f2-37-s08 | bin_printed_in | text | 108 by 36 | 108" x 36" |
| b68-lpt-f2-37-s08 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-37-s08 | evidence | text | F2-37 | F2-37;text 2-69 (PDF 94) |
| b68-lpt-f2-37-s08 | setup_status | text | pending | setup_incomplete |
| b68-lpt-f2-37-s09 | kind | text | averaged-series | single |
| b68-lpt-f2-37-s09 | state_printed | text | RS Dense |  |
| b68-lpt-f2-37-s09 | penetrator_printed | text | 2 inch cylinder | 2" Cyl. |
| b68-lpt-f2-37-s09 | bin_printed_in | text | 108 by 36 | 108" x 36" |
| b68-lpt-f2-37-s09 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-37-s09 | evidence | text | F2-37 | F2-37;text 2-69 (PDF 94) |
| b68-lpt-f2-37-s09 | setup_status | text | pending | setup_incomplete |
| b68-lpt-f2-37-s10 | kind | text | averaged-series | single |
| b68-lpt-f2-37-s10 | state_printed | text | RS Intermediate |  |
| b68-lpt-f2-37-s10 | penetrator_printed | text | 4 inch cylinder | 4" Cyl. |
| b68-lpt-f2-37-s10 | bin_printed_in | text | 108 by 36 | 108" x 36" |
| b68-lpt-f2-37-s10 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-37-s10 | evidence | text | F2-37 | F2-37;text 2-69 (PDF 94) |
| b68-lpt-f2-37-s10 | setup_status | text | pending | setup_incomplete |
| b68-lpt-f2-37-s10 | mcc_relevant | text | no | yes |
| b68-lpt-f2-37-s11 | kind | text | averaged-series | single |
| b68-lpt-f2-37-s11 | state_printed | text | RS Intermediate |  |
| b68-lpt-f2-37-s11 | penetrator_printed | text | 2 inch cylinder | 2" Cyl. |
| b68-lpt-f2-37-s11 | bin_printed_in | text | 108 by 36 | 108" x 36" |
| b68-lpt-f2-37-s11 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-37-s11 | evidence | text | F2-37 | F2-37;text 2-69 (PDF 94) |
| b68-lpt-f2-37-s11 | setup_status | text | pending | setup_incomplete |
| b68-lpt-f2-37-s11 | mcc_relevant | text | no | yes |
| b68-lpt-f2-38-s01 | state_printed | text | SS Dense |  |
| b68-lpt-f2-38-s01 | penetrator_printed | text | 2 inch cylinder | 2" Cylinder |
| b68-lpt-f2-38-s01 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-38-s01 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-38-s01 | evidence | text | F2-38 | F2-38;text 2-69 (PDF 94) |
| b68-lpt-f2-38-s02 | state_printed | text | SS Dense |  |
| b68-lpt-f2-38-s02 | penetrator_printed | text | 4 inch cylinder | 4" Cylinder |
| b68-lpt-f2-38-s02 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-38-s02 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-38-s02 | evidence | text | F2-38 | F2-38;text 2-69 (PDF 94) |
| b68-lpt-f2-38-s03 | state_printed | text | SS Intermediate |  |
| b68-lpt-f2-38-s03 | penetrator_printed | text | 2 inch cylinder | 2" Cylinder |
| b68-lpt-f2-38-s03 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-38-s03 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-38-s03 | evidence | text | F2-38 | F2-38;text 2-69 (PDF 94) |
| b68-lpt-f2-38-s04 | state_printed | text | SS Intermediate |  |
| b68-lpt-f2-38-s04 | penetrator_printed | text | 4 inch cylinder | 4" Cylinder |
| b68-lpt-f2-38-s04 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-38-s04 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-38-s04 | evidence | text | F2-38 | F2-38;text 2-69 (PDF 94) |
| b68-lpt-f2-38-s05 | state_printed | text | SS Loose |  |
| b68-lpt-f2-38-s05 | penetrator_printed | text | 4 inch cylinder | 4" Cylinder |
| b68-lpt-f2-38-s05 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-38-s05 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-38-s05 | evidence | text | F2-38 | F2-38;text 2-69 (PDF 94) |
| b68-lpt-f2-38-s06 | state_printed | text | SS Loose |  |
| b68-lpt-f2-38-s06 | penetrator_printed | text | 2 inch cylinder | 2" Cylinder |
| b68-lpt-f2-38-s06 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-38-s06 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-38-s06 | evidence | text | F2-38 | F2-38;text 2-69 (PDF 94) |
| b68-lpt-f2-39-s01 | state_printed | text | PS Dense |  |
| b68-lpt-f2-39-s01 | penetrator_printed | text | 2 inch cylinder | 2" Cylinder |
| b68-lpt-f2-39-s01 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-39-s01 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-39-s01 | evidence | text | F2-39 | F2-39;text 2-69 (PDF 94) |
| b68-lpt-f2-39-s02 | state_printed | text | PS Dense |  |
| b68-lpt-f2-39-s02 | penetrator_printed | text | 4 inch cylinder | 4" Cylinder |
| b68-lpt-f2-39-s02 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-39-s02 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-39-s02 | evidence | text | F2-39 | F2-39;text 2-69 (PDF 94) |
| b68-lpt-f2-39-s03 | state_printed | text | PS Intermediate |  |
| b68-lpt-f2-39-s03 | penetrator_printed | text | 4 inch cylinder | 4" Cylinder |
| b68-lpt-f2-39-s03 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-39-s03 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-39-s03 | evidence | text | F2-39 | F2-39;text 2-69 (PDF 94) |
| b68-lpt-f2-39-s04 | state_printed | text | PS Intermediate |  |
| b68-lpt-f2-39-s04 | penetrator_printed | text | 2 inch cylinder | 2" Cylinder |
| b68-lpt-f2-39-s04 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-39-s04 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-39-s04 | evidence | text | F2-39 | F2-39;text 2-69 (PDF 94) |
| b68-lpt-f2-39-s05 | state_printed | text | PS Loose |  |
| b68-lpt-f2-39-s05 | penetrator_printed | text | 2 inch cylinder | 2" Cylinder |
| b68-lpt-f2-39-s05 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-39-s05 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-39-s05 | evidence | text | F2-39 | F2-39;text 2-69 (PDF 94) |
| b68-lpt-f2-39-s06 | state_printed | text | PS Loose |  |
| b68-lpt-f2-39-s06 | penetrator_printed | text | 4 inch cylinder | 4" Cylinder |
| b68-lpt-f2-39-s06 | bin_printed_in | text | 18 by 36 | 18" x 36" |
| b68-lpt-f2-39-s06 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-39-s06 | evidence | text | F2-39 | F2-39;text 2-69 (PDF 94) |
| b68-lpt-f2-40-s01 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-f2-40-s01 | bin_printed_in | text | 36 by 18 | 36" x 18" |
| b68-lpt-f2-40-s01 | rate_printed | text | static (stepped load increments) |  |
| b68-lpt-f2-40-s01 | evidence | text | F2-40 | F2-40;text 2-74 (PDF 99) |
| b68-lpt-f2-40-s02 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-f2-40-s02 | bin_printed_in | text | 36 by 18 | 36" x 18" |
| b68-lpt-f2-40-s02 | rate_printed | text | 1 in/min | One Inch per Min. |
| b68-lpt-f2-40-s02 | evidence | text | F2-40 | F2-40;text 2-74 (PDF 99) |
| b68-lpt-f2-40-s02 | setup_status | text | setup_incomplete | complete |
| b68-lpt-f2-40-s03 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-f2-40-s03 | bin_printed_in | text | 36 by 18 | 36" x 18" |
| b68-lpt-f2-40-s03 | rate_printed | text | 2 in/min | Two Inches per Min. |
| b68-lpt-f2-40-s03 | evidence | text | F2-40 | F2-40;text 2-74 (PDF 99) |
| b68-lpt-f2-40-s03 | setup_status | text | setup_incomplete | complete |
| b68-lpt-f2-40-s04 | penetrator_printed | text | 4 inch cylinder | Four-Inch Cylinder |
| b68-lpt-f2-40-s04 | bin_printed_in | text | 36 by 18 | 36" x 18" |
| b68-lpt-f2-40-s04 | rate_printed | text | 4 in/min | Four Inches per Min. |
| b68-lpt-f2-40-s04 | evidence | text | F2-40 | F2-40;text 2-74 (PDF 99) |
| b68-lpt-f2-40-s04 | setup_status | text | setup_incomplete | complete |
| b68-lpt-f2-49-s01 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-49-s01 | state_printed | text | RS Dense |  |
| b68-lpt-f2-49-s01 | penetrator_printed | text | 4 inch footpad | 4" FP |
| b68-lpt-f2-49-s01 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-49-s01 | evidence | text | F2-49 | F2-49;text 2-80 (PDF 105) |
| b68-lpt-f2-49-s02 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-49-s02 | state_printed | text | RS Dense |  |
| b68-lpt-f2-49-s02 | penetrator_printed | text | 4 inch cylinder | 4" Cyl. |
| b68-lpt-f2-49-s02 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-49-s02 | evidence | text | F2-49 | F2-49;text 2-80 (PDF 105) |
| b68-lpt-f2-49-s03 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-49-s03 | state_printed | text | RS Dense |  |
| b68-lpt-f2-49-s03 | penetrator_printed | text | 6 inch footpad | 6" FP |
| b68-lpt-f2-49-s03 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-49-s03 | evidence | text | F2-49 | F2-49;text 2-80 (PDF 105) |
| b68-lpt-f2-49-s04 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-49-s04 | state_printed | text | RS Intermediate |  |
| b68-lpt-f2-49-s04 | penetrator_printed | text | 4 inch cylinder | 4" Cyl. |
| b68-lpt-f2-49-s04 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-49-s04 | evidence | text | F2-49 | F2-49;text 2-80 (PDF 105) |
| b68-lpt-f2-49-s05 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-49-s05 | state_printed | text | RS Intermediate |  |
| b68-lpt-f2-49-s05 | penetrator_printed | text | 4 inch footpad | 4" FP |
| b68-lpt-f2-49-s05 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-49-s05 | evidence | text | F2-49 | F2-49;text 2-80 (PDF 105) |
| b68-lpt-f2-49-s06 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-49-s06 | state_printed | text | RS Intermediate |  |
| b68-lpt-f2-49-s06 | penetrator_printed | text | 6 inch footpad | 6" FP |
| b68-lpt-f2-49-s06 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-49-s06 | evidence | text | F2-49 | F2-49;text 2-80 (PDF 105) |
| b68-lpt-f2-49-s07 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-49-s07 | state_printed | text | RS Loose |  |
| b68-lpt-f2-49-s07 | penetrator_printed | text | 4 inch cylinder | 4" Cyl. |
| b68-lpt-f2-49-s07 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-49-s07 | evidence | text | F2-49 | F2-49;text 2-80 (PDF 105) |
| b68-lpt-f2-49-s08 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-49-s08 | state_printed | text | RS Loose |  |
| b68-lpt-f2-49-s08 | penetrator_printed | text | 6 inch footpad | 4" FP |
| b68-lpt-f2-49-s08 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-49-s08 | evidence | text | F2-49 | F2-49;text 2-80 (PDF 105) |
| b68-lpt-f2-49-s09 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-49-s09 | state_printed | text | RS Loose |  |
| b68-lpt-f2-49-s09 | penetrator_printed | text | 4 inch footpad | 6" FP |
| b68-lpt-f2-49-s09 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-49-s09 | evidence | text | F2-49 | F2-49;text 2-80 (PDF 105) |
| b68-lpt-f2-49-s10 | <row> | missing | present | absent |
| b68-lpt-f2-50-s01 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-50-s01 | state_printed | text | SS Dense |  |
| b68-lpt-f2-50-s01 | dr_printed | number | 0.75 | approx 0.75 |
| b68-lpt-f2-50-s01 | penetrator_printed | text | 4 inch cylinder | 4" Cyl. |
| b68-lpt-f2-50-s01 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-50-s01 | evidence | text | F2-50 | F2-50;text 2-80 (PDF 105) |
| b68-lpt-f2-50-s02 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-50-s02 | state_printed | text | SS Dense |  |
| b68-lpt-f2-50-s02 | dr_printed | number | 0.75 | approx 0.75 |
| b68-lpt-f2-50-s02 | penetrator_printed | text | 4 inch footpad | 4" FP |
| b68-lpt-f2-50-s02 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-50-s02 | evidence | text | F2-50 | F2-50;text 2-80 (PDF 105) |
| b68-lpt-f2-50-s03 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-50-s03 | state_printed | text | SS Dense |  |
| b68-lpt-f2-50-s03 | dr_printed | number | 0.75 | approx 0.75 |
| b68-lpt-f2-50-s03 | penetrator_printed | text | 6 inch footpad | 6" FP |
| b68-lpt-f2-50-s03 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-50-s03 | evidence | text | F2-50 | F2-50;text 2-80 (PDF 105) |
| b68-lpt-f2-50-s04 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-50-s04 | state_printed | text | SS Intermediate |  |
| b68-lpt-f2-50-s04 | dr_printed | number | 0.63 | approx 0.63 |
| b68-lpt-f2-50-s04 | penetrator_printed | text | 4 inch footpad | 4" FP |
| b68-lpt-f2-50-s04 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-50-s04 | evidence | text | F2-50 | F2-50;text 2-80 (PDF 105) |
| b68-lpt-f2-50-s05 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-50-s05 | state_printed | text | SS Intermediate |  |
| b68-lpt-f2-50-s05 | dr_printed | number | 0.63 | approx 0.63 |
| b68-lpt-f2-50-s05 | penetrator_printed | text | 6 inch footpad | 6" FP |
| b68-lpt-f2-50-s05 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-50-s05 | evidence | text | F2-50 | F2-50;text 2-80 (PDF 105) |
| b68-lpt-f2-50-s06 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-50-s06 | state_printed | text | SS Loose |  |
| b68-lpt-f2-50-s06 | dr_printed | number | 0.0 | approx 0.0 |
| b68-lpt-f2-50-s06 | penetrator_printed | text | 6 inch footpad | 6" FP |
| b68-lpt-f2-50-s06 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-50-s06 | evidence | text | F2-50 | F2-50;text 2-80 (PDF 105) |
| b68-lpt-f2-50-s07 | kind | text | averaged-series | derived-series |
| b68-lpt-f2-50-s07 | state_printed | text | SS Loose |  |
| b68-lpt-f2-50-s07 | dr_printed | number | 0.0 | approx 0.0 |
| b68-lpt-f2-50-s07 | penetrator_printed | text | 4 inch footpad | 4" FP |
| b68-lpt-f2-50-s07 | start_depth_printed_in | number | 0 |  |
| b68-lpt-f2-50-s07 | evidence | text | F2-50 | F2-50;text 2-80 (PDF 105) |
| b68-lpt-f2-51-cms | <row> | missing | present | absent |
| b68-lpt-f2-51-s01 | <row> | missing | absent | present |
| b68-lpt-f2-51-s02 | <row> | missing | absent | present |
| b68-lpt-f2-51-s03 | <row> | missing | absent | present |
| b68-lpt-f2-51-s04 | <row> | missing | absent | present |
| b68-lpt-f2-51-s05 | <row> | missing | absent | present |
| b68-lpt-f2-52-s01 | state_printed | text | all states |  |
| b68-lpt-f2-52-s01 | penetrator_printed | text | 4 inch cylinder | 4" Cyl. |
| b68-lpt-f2-52-s02 | state_printed | text | all states |  |
| b68-lpt-f2-52-s02 | penetrator_printed | text | 4 inch footpad | 4" Footpad |
| b68-lpt-f2-52-s03 | state_printed | text | all states |  |
| b68-lpt-f2-52-s03 | penetrator_printed | text | 6 inch footpad | 6" Footpad |
| b68-lpt-f2-52-s04 | state_printed | text | all states |  |
| b68-lpt-f2-52-s04 | penetrator_printed | text | 4 inch footpad | 4" Footpad |
| b68-lpt-f2-52-s05 | state_printed | text | all states |  |
| b68-lpt-f2-52-s05 | penetrator_printed | text | 6 inch footpad | 6" Footpad |
| b68-sonic-t2-3-10 | <row> | missing | absent | present |
| b68-sonic-t2-3-11 | <row> | missing | absent | present |
| b68-sonic-t2-3-12 | <row> | missing | absent | present |
| b68-dens-f2-17-s01 | kind | text | summary | averaged-series |
| b68-dens-f2-17-s01 | soil_no | number | 2 |  |
| b68-dens-f2-17-s01 | soil_no_status | text | reported | unknown |
| b68-dens-f2-17-s01 | state_printed | text | loose to dense | previously unused; undegraded |
| b68-dens-f2-17-s01 | dr_printed | text | 0 to 1.0 |  |
| b68-dens-f2-17-s01 | unit_weight_printed_pcf | text | 23.8 to 30.2 | min 23.8; max 30.2 |
| b68-dens-f2-17-s01 | penetrator_printed | text |  | 3-1/2-inch tamping foot |
| b68-dens-f2-17-s01 | bin_printed_in | text | Soiltest CN404 mold |  |
| b68-dens-f2-17-s01 | evidence | text | F2-17;T2-3 | F2-17;T2-3;text 2-35 (PDF 60) |
| b68-dens-f2-17-s01 | mcc_relevant | text | no | yes |
| b68-dens-f2-17-s01 | priority | number | 1 | 2 |
| b68-dens-f2-17-s02 | kind | text | summary | averaged-series |
| b68-dens-f2-17-s02 | soil_no | number | 1 |  |
| b68-dens-f2-17-s02 | soil_no_status | text | reported | unknown |
| b68-dens-f2-17-s02 | state_printed | text | loose to dense | previously unused; undegraded |
| b68-dens-f2-17-s02 | dr_printed | text | 0 to 1.0 |  |
| b68-dens-f2-17-s02 | unit_weight_printed_pcf | text | 41.3 to 52.9 | min 41.3; max 52.9 |
| b68-dens-f2-17-s02 | penetrator_printed | text |  | 3-1/2-inch tamping foot |
| b68-dens-f2-17-s02 | bin_printed_in | text | Soiltest CN404 mold |  |
| b68-dens-f2-17-s02 | evidence | text | F2-17;T2-3;F2-56 | F2-17;T2-3;text 2-35 (PDF 60) |
| b68-dens-f2-17-s02 | mcc_relevant | text | no | yes |
| b68-dens-f2-17-s02 | priority | number | 1 | 2 |
| b68-dens-f2-17-s03 | kind | text | summary | averaged-series |
| b68-dens-f2-17-s03 | soil_no | number | 5 |  |
| b68-dens-f2-17-s03 | soil_no_status | text | inferred | unknown |
| b68-dens-f2-17-s03 | state_printed | text | loose to dense | previously unused; undegraded |
| b68-dens-f2-17-s03 | dr_printed | text | 0 to 1.0 |  |
| b68-dens-f2-17-s03 | unit_weight_printed_pcf | text | 57.9 to 70.3 | min 57.9; max 70.3 |
| b68-dens-f2-17-s03 | penetrator_printed | text |  | 3-1/2-inch tamping foot |
| b68-dens-f2-17-s03 | bin_printed_in | text | Soiltest CN404 mold |  |
| b68-dens-f2-17-s03 | evidence | text | F2-17;T2-3 | F2-17;T2-3;text 2-35 (PDF 60) |
| b68-dens-f2-17-s03 | mcc_relevant | text | no | yes |
| b68-dens-f2-17-s03 | priority | number | 1 | 2 |
| b68-dens-f2-17-s04 | kind | text | summary | averaged-series |
| b68-dens-f2-17-s04 | soil_no | number | 6 |  |
| b68-dens-f2-17-s04 | soil_no_status | text | inferred | unknown |
| b68-dens-f2-17-s04 | state_printed | text | loose to dense | previously unused; undegraded |
| b68-dens-f2-17-s04 | dr_printed | text | 0 to 1.0 |  |
| b68-dens-f2-17-s04 | unit_weight_printed_pcf | text | 61.4 to 83.1 | min 61.4; max 83.1 |
| b68-dens-f2-17-s04 | penetrator_printed | text |  | 3-1/2-inch tamping foot |
| b68-dens-f2-17-s04 | bin_printed_in | text | Soiltest CN404 mold |  |
| b68-dens-f2-17-s04 | evidence | text | F2-17;T2-3 | F2-17;T2-3;text 2-35 (PDF 60) |
| b68-dens-f2-17-s04 | mcc_relevant | text | no | yes |
| b68-dens-f2-17-s04 | priority | number | 1 | 2 |
| b68-dens-f2-17-s05 | <row> | missing | absent | present |
| b68-dens-f2-17-s06 | kind | text | summary | averaged-series |
| b68-dens-f2-17-s06 | soil_no | number | 7 |  |
| b68-dens-f2-17-s06 | soil_no_status | text | inferred | unknown |
| b68-dens-f2-17-s06 | state_printed | text | loose to dense | previously unused; undegraded |
| b68-dens-f2-17-s06 | dr_printed | text | 0 to 1.0 |  |
| b68-dens-f2-17-s06 | unit_weight_printed_pcf | text | 95.4 to 112.7 | min 95.4; max 112.7 |
| b68-dens-f2-17-s06 | penetrator_printed | text |  | 3-1/2-inch tamping foot |
| b68-dens-f2-17-s06 | bin_printed_in | text | Soiltest CN404 mold |  |
| b68-dens-f2-17-s06 | evidence | text | F2-17;T2-3 | F2-17;T2-3;text 2-35 (PDF 60) |
| b68-dens-f2-17-s06 | mcc_relevant | text | no | yes |
| b68-dens-f2-17-s06 | priority | number | 1 | 2 |
| b68-dens-f2-60-s01 | <row> | missing | absent | present |
| b68-dens-f2-60-s02 | <row> | missing | absent | present |
| b68-dens-f2-60-s03 | <row> | missing | absent | present |
| b68-dens-f2-60-s04 | <row> | missing | absent | present |
| b68-ds-f2-21-n1172 | state_printed | text | RS Intermediate |  |
| b68-ds-f2-21-n1172 | dr_printed | text | 0.5 to 0.57 | .5 to .57 |
| b68-ds-f2-21-n1172 | rate_printed | text | approx 0.07 in/min | approx 0.07 In./Min. |
| b68-ds-f2-21-n1172 | evidence | text | F2-21;F2-22 | F2-20;F2-21;F2-22;text 2-40 (PDF 65) |
| b68-ds-f2-21-n1760 | state_printed | text | RS Intermediate |  |
| b68-ds-f2-21-n1760 | dr_printed | text | 0.5 to 0.57 | .5 to .57 |
| b68-ds-f2-21-n1760 | rate_printed | text | approx 0.07 in/min | approx 0.07 In./Min. |
| b68-ds-f2-21-n1760 | evidence | text | F2-21;F2-22 | F2-20;F2-21;F2-22;text 2-40 (PDF 65) |
| b68-ds-f2-21-n2345 | state_printed | text | RS Intermediate |  |
| b68-ds-f2-21-n2345 | dr_printed | text | 0.5 to 0.57 | .5 to .57 |
| b68-ds-f2-21-n2345 | rate_printed | text | approx 0.07 in/min | approx 0.07 In./Min. |
| b68-ds-f2-21-n2345 | evidence | text | F2-21;F2-22 | F2-20;F2-21;F2-22;text 2-40 (PDF 65) |
| b68-ds-f2-21-n2935 | state_printed | text | RS Intermediate |  |
| b68-ds-f2-21-n2935 | dr_printed | text | 0.5 to 0.57 | .5 to .57 |
| b68-ds-f2-21-n2935 | rate_printed | text | approx 0.07 in/min | approx 0.07 In./Min. |
| b68-ds-f2-21-n2935 | evidence | text | F2-21;F2-22 | F2-20;F2-21;F2-22;text 2-40 (PDF 65) |
| b68-ds-f2-21-n3520 | state_printed | text | RS Intermediate (Dr 0.5 to 0.57) |  |
| b68-ds-f2-21-n3520 | dr_printed | text | 0.5 to 0.57 | .5 to .57 |
| b68-ds-f2-21-n3520 | rate_printed | text | approx 0.07 in/min | approx 0.07 In./Min. |
| b68-ds-f2-21-n3520 | evidence | text | F2-21;F2-22 | F2-20;F2-21;F2-22;text 2-40 (PDF 65) |
| b68-ds-f2-23-rsm-a | kind | text | derived-series | correlation |
| b68-ds-f2-23-rsm-a | state_printed | text | all states |  |
| b68-ds-f2-23-rsm-a | dr_printed | text | 0 to 1.0 |  |
| b68-ds-f2-23-rsm-a | rate_printed | text |  | approx 0.07 In./Min. |
| b68-ds-f2-23-rsm-a | evidence | text | F2-23 | F2-23;text 2-45 (PDF 70) |
| b68-ds-f2-23-rsm-b | kind | text | derived-series | correlation |
| b68-ds-f2-23-rsm-b | state_printed | text | all states |  |
| b68-ds-f2-23-rsm-b | dr_printed | text | 0 to 1.0 |  |
| b68-ds-f2-23-rsm-b | rate_printed | text |  | approx 0.07 In./Min. |
| b68-ds-f2-23-rsm-b | evidence | text | F2-23 | F2-23;text 2-45 (PDF 70) |
| b68-gs-f2-14-rsm-a | soil_no | number | 5 |  |
| b68-gs-f2-14-rsm-a | soil_no_status | text | inferred | unknown |
| b68-gs-f2-14-rsm-a | state_printed | text |  | previously unused; undegraded |
| b68-smp-f2-57-unused | <row> | missing | absent | present |
| b68-smp-f2-58-unused | <row> | missing | absent | present |
| b68-dens-p2-101-scoop | <row> | missing | absent | present |
| b68-dens-p2-103-slope | <row> | missing | absent | present |
| b68-dens-p2-104-scoop | <row> | missing | absent | present |
| b68-dens-p2-113-plate | <row> | missing | absent | present |
| b68-ds-p2-66-rs-dense | <row> | missing | absent | present |
| b68-tx-p2-49-rs-dense | state_printed | text | RS Dense | dense |
| b68-tx-p2-49-rs-dense | evidence | text | text 2-49 (PDF 74);F2-26 | text 2-49 (PDF 74) |
| b68-tx-p2-49-rs-dense | priority | number | 2 | 1 |
| b68-dens-p2-104-hopper | <row> | missing | absent | present |
| b68-dens-p2-110-soil-3 | <row> | missing | absent | present |
| b68-dens-p2-110-soil-8 | <row> | missing | absent | present |
| b68-dens-p2-113-soil-4 | <row> | missing | absent | present |
| b68-dens-p2-113-soil-9 | <row> | missing | absent | present |
| b68-dens-p2-110-soil-10 | <row> | missing | absent | present |
| b68-dens-p2-113-soil-11 | <row> | missing | absent | present |
| b68-dens-p2-113-soil-12 | <row> | missing | absent | present |
| b68-dens-f2-60-drag-beds | <row> | missing | present | absent |
| b68-dpt-p2-90-rs-49-beds | gp_printed_g | number | 11.76 | 11.76 ± 0.14 |
| b68-dpt-p2-90-rs-49-beds | penetrator_printed | text |  | 2-3/4 inches diameter; full radius nose |
| b68-dpt-p2-90-rs-49-beds | priority | number | 2 | 1 |
| b68-tx-p2-49-rs-intermediate | state_printed | text | RS Intermediate | intermediate |
| b68-tx-p2-49-rs-intermediate | evidence | text | text 2-49 (PDF 74);F2-26 | text 2-49 (PDF 74) |
| b68-tx-p2-49-rs-intermediate | priority | number | 2 | 1 |
| b68-lpt-f2-33-bearing-capacity | <row> | missing | absent | present |
