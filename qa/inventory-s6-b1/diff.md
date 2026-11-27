# Table diff: claude vs codex

Files: `extractions/claude/inventory-s6-b1/inventory.csv` (claude), `extractions/codex/inventory-s6-b1/inventory.csv` (codex). Key: `id`.

Rows: 83 in claude, 83 in codex. Compared columns: 28.
Cells compared: 2324. Agreed: 1929 (83.0 percent).
Disagreements: 395 (9 numeric, 386 text, 0 missing rows).

| key | column | kind | claude | codex |
|---|---|---|---|---|
| F6-1 | apparatus | text | LM Landing Dynamics Computer Program (NASA-MSC) | LM Landing Dynamics Computer Program |
| F6-2 | apparatus | text | LM Landing Dynamics Computer Program, subroutine SOIL | LM Landing Dynamics Computer Program |
| F6-3 | apparatus | text | LM Landing Dynamics Computer Program, subroutine BEN | LM Landing Dynamics Computer Program |
| F6-4 | apparatus | text | 1/6-scale LM model with spiked footpads; rigid surface | 1/6-scale LM model with spiked footpads; plywood surface |
| F6-4 | rate_or_dynamics | text | free drop, 22.5 deg yaw, slope 10 deg, VV 6 to 12, VH 4.5 to 7 | free drop, 22.5 deg yaw, slope 10 deg, level vehicle at impact |
| F6-5 | soils | text | none (wooden surface) | plywood blocks |
| F6-5 | apparatus | text | 1/6-scale LM model with spiked feet; LM Landing Dynamics Computer Program (rigid surface) | 1/6-scale LM model with spiked footpads; plywood surface |
| F6-5 | rate_or_dynamics | text | free drop, 22.5 deg yaw, ground slope 10 deg, level vehicle | free drop, 22.5 deg yaw, slope 10 deg, level vehicle at impact |
| F6-5 | curves | number | 5 | 4 |
| F6-5 | in_scope | text | maybe | yes |
| F6-5 | priority | number | 2 | 1 |
| F6-5 | relation_target | text | F6-4;F5-20 | F5-20;F6-4 |
| F6-6 | states | text | dense (Dr 0.71 to 0.81, 56.7 to 59.3 pcf) | dense |
| F6-6 | apparatus | text | 1/6-scale LM model; 15 deg sloped soil box | 1/6-scale LM model; six degree of freedom drop rig |
| F6-6 | rate_or_dynamics | text | free drop, 45 deg yaw, slope 15 deg, VV 7 to 14, VH 4 to 7.5 | free drop, 45 deg yaw, slope 15 deg, level vehicle at impact |
| F6-6 | relation_target | text | T5-2 | T5-2-p309;T5-2-p310 |
| F6-7 | states | text | dense (Dr 0.71 to 0.81 per F6-6) | dense |
| F6-7 | apparatus | text | 1/6-scale LM model; LM Landing Dynamics Computer Program (rigid surface and soil versions) | 1/6-scale LM model; six degree of freedom drop rig |
| F6-7 | rate_or_dynamics | text | free drop, 45 deg yaw (2-2), slope 15 deg downhill, level vehicle; computed with original damping 10 Sdot and increased damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | free drop, 45 deg yaw, slope 15 deg, level vehicle at impact |
| F6-7 | curves | number | 7 | 6 |
| F6-7 | in_scope | text | maybe | yes |
| F6-7 | priority | number | 2 | 1 |
| F6-7 | relation_target | text | F6-6;F5-40 | F5-40;F6-6 |
| F6-8 | states | text | rolled (10 rolls); not rolled (drop 68, Dr 0.10); Dr 0.10 to 0.86 | rolled; not rolled |
| F6-8 | apparatus | text | 1/6-scale LM model; 15 deg sloped soil box | 1/6-scale LM model; six degree of freedom drop rig |
| F6-8 | rate_or_dynamics | text | free drop, 45 deg yaw (drop 63 at 22.5), slope 15 deg, VV 7 to 14, VH 4 to 7.5 | free drop, 22.5 or 45 deg yaw, slope 15 deg |
| F6-9 | states | text | rolled, dense (Dr 0.65 to 0.86 per F6-8) | dense; rolled |
| F6-9 | apparatus | text | 1/6-scale LM model; LM Landing Dynamics Computer Program (rigid surface and soil versions) | 1/6-scale LM model; six degree of freedom drop rig |
| F6-9 | rate_or_dynamics | text | free drop, 45 deg yaw (2-2), slope 15 deg downhill, level vehicle; computed with original and increased strut damping | free drop, 45 deg yaw, slope 15 deg, level vehicle at impact |
| F6-9 | curves | number | 8 | 6 |
| F6-9 | in_scope | text | maybe | yes |
| F6-9 | priority | number | 2 | 1 |
| F6-9 | relation_target | text | F6-8;F5-41 | F5-41;F6-8 |
| F5-40 | states | text | dense (Dr 0.71 to 0.81 per F6-6) | dense |
| F5-40 | apparatus | text | 1/6-scale LM model; 15 deg sloped soil box | 1/6-scale LM model; six degree of freedom drop rig |
| F5-40 | rate_or_dynamics | text | free drop, 45 deg yaw (2-2 landing), level vehicle, ground slope 15 deg downhill | free drop, 45 deg yaw, slope 15 deg, level vehicle at impact |
| F5-40 | curves | number | 4 | 2 |
| F5-40 | relation_target | text | F6-6 | T5-2-p309;T5-2-p310 |
| F5-41 | states | text | rolled, dense (Dr 0.65 to 0.86 per F6-8) | dense; rolled |
| F5-41 | apparatus | text | 1/6-scale LM model; 15 deg sloped soil box | 1/6-scale LM model; six degree of freedom drop rig |
| F5-41 | rate_or_dynamics | text | free drop, 45 deg yaw (2-2 landing), level vehicle, ground slope 15 deg downhill | free drop, 45 deg yaw, slope 15 deg, level vehicle at impact |
| F5-41 | curves | number | 4 | 2 |
| F5-41 | relation_target | text | F6-8 | T5-2-p311;T5-2-p312 |
| F5-42 | apparatus | text | 1/6-scale LM model; 15 deg sloped soil box | 1/6-scale LM model; six degree of freedom drop rig |
| F5-42 | rate_or_dynamics | text | free drop, 22.5 deg yaw, level vehicle, ground slope 15 deg downhill | free drop, 22.5 deg yaw, slope 15 deg, level vehicle at impact |
| F5-42 | curves | number | 1 | 0 |
| F5-42 | legend_entries | text | n/a | All Drops Stable |
| F5-42 | relation_target | text | T5-2 | T5-2-p310 |
| F5-43 | apparatus | text | 1/6-scale LM model | 1/6-scale LM model; six degree of freedom drop rig |
| F5-43 | rate_or_dynamics | text | exploratory drop (secondary strut tension), slope 3 1/2 deg: yaw -160 deg (strut 7 leading, strut 1 trailing), VV 7 fps, VH 4 fps; three 4 inch deep depressions under footpads 2 to 4 | VV 7 ft/s, VH 4 ft/s, yaw -160 deg, slope 3.5 deg |
| F5-43 | relation | text | same-as | none |
| F5-43 | relation_target | text | T5-2 |  |
| F5-44 | apparatus | text | 1/6-scale LM model | 1/6-scale LM model; six degree of freedom drop rig |
| F5-44 | rate_or_dynamics | text | exploratory drop (secondary strut tension), slope 3 1/2 deg: yaw +140 deg, VV 6 fps, VH 2.46 fps; one 4 inch depression under footpad 2 | VV 6 ft/s, VH 2.46 ft/s, yaw +140 deg, slope 3.5 deg |
| F5-44 | relation | text | same-as | none |
| F5-44 | relation_target | text | T5-2 |  |
| F5-45 | apparatus | text | 1/6-scale LM model | 1/6-scale LM model; six degree of freedom drop rig |
| F5-45 | rate_or_dynamics | text | exploratory drop (secondary strut tension), slope 3 1/2 deg: same ground and attitude as drop 3, VV 10 fps, VH 2.45 fps | VV 10 ft/s, VH 2.45 ft/s, yaw +140 deg, slope 3.5 deg |
| F5-45 | relation | text | same-as | none |
| F5-45 | relation_target | text | T5-2 |  |
| F5-46 | apparatus | text | 1/6-scale LM model | 1/6-scale LM model; six degree of freedom drop rig |
| F5-46 | rate_or_dynamics | text | exploratory drop (secondary strut tension), slope 3 1/2 deg: yaw +50 deg, VV 5 fps, VH 2.46 fps; waxed hard blocks under pads 2 and 4, sandpaper pad 3 on hard surface, pad 1 into 4 1/2 inch depression | VV 5 ft/s, VH 2.46 ft/s, yaw +50 deg, slope 3.5 deg |
| F5-46 | relation | text | same-as | none |
| F5-46 | relation_target | text | T5-2 |  |
| F5-47 | apparatus | text | 1/6-scale LM model | 1/6-scale LM model; six degree of freedom drop rig |
| F5-47 | rate_or_dynamics | text | exploratory drop (secondary strut tension), slope 3 1/2 deg: same ground as drop 5, VV 10 fps, VH 2.46 fps | VV 10 ft/s, VH 2.46 ft/s, slope 3.5 deg |
| F5-47 | relation | text | same-as | none |
| F5-47 | relation_target | text | T5-2 |  |
| F6-10 | states | text | loose (Dr 0); intermediate (Dr 0.3) | loose; intermediate |
| F6-10 | apparatus | text | 1/6-scale LM model; level soil bed | 1/6-scale LM model; leg set 1 instrumented |
| F6-10 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground; VV 10 fps VH 0 (drops 1, 4, 6, 8) or VV 5 fps VH 7 fps (drops 2, 3, 5, 7) | free drop, 45 deg yaw (2-2 landing), level ground, VV/VH 10/0 or 5/7 ft/s |
| F6-11 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-11 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-11 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -60.5 in/s and VH 83.5 in/s |
| F6-11 | x_quantity | text | elapsed time | time |
| F6-11 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-11 | relation_target | text | F6-10;F5-29;F5-30;F5-31 | F5-29;F5-30;F5-31 |
| F6-12 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-12 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-12 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -60.5 in/s and VH 83.5 in/s |
| F6-12 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-12 | in_scope | text | maybe | no |
| F6-13 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-13 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-13 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -114.9 in/s and VH 0 |
| F6-13 | x_quantity | text | elapsed time | time |
| F6-13 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-13 | relation_target | text | F6-10;F5-22;F5-23;F5-24 | F5-22;F5-23;F5-24 |
| F6-14 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-14 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-14 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-14 | x_quantity | text | elapsed time | time |
| F6-14 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-15 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-15 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-15 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-15 | x_quantity | text | elapsed time | time |
| F6-15 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-16 | states | text | intermediate (Dr printed "3", 53.0 pcf, phi 42.5) | intermediate (53.0 pcf) |
| F6-16 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-16 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-16 | x_quantity | text | elapsed time | time |
| F6-16 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-17 | states | text | intermediate (Dr 0.3, 53.0 pcf, phi 42.5) | intermediate (Dr 0.3, 53.0 pcf) |
| F6-17 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-17 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-17 | x_quantity | text | elapsed time | time |
| F6-17 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-18 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-18 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-18 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-18 | x_quantity | text | elapsed time | time |
| F6-18 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-19 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-19 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-19 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-19 | x_quantity | text | elapsed time | time |
| F6-19 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-20 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-20 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-20 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -114.9 in/s and VH 0 |
| F6-20 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-20 | in_scope | text | maybe | no |
| F6-21 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-21 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-21 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-21 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-21 | in_scope | text | maybe | no |
| F6-22 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-22 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-22 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-22 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-22 | in_scope | text | maybe | no |
| F6-23 | states | text | intermediate (Dr printed "3", 53.0 pcf, phi 42.5) | intermediate (53.0 pcf) |
| F6-23 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-23 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-23 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-23 | in_scope | text | maybe | no |
| F6-24 | states | text | intermediate (Dr 0.3, 53.0 pcf, phi 42.5) | intermediate (Dr 0.3, 53.0 pcf) |
| F6-24 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-24 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-24 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-24 | in_scope | text | maybe | no |
| F6-25 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-25 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-25 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-25 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-25 | in_scope | text | maybe | no |
| F6-26 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-26 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-26 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-26 | y_quantity | text | Footpad Velocity Vap | footpad velocity (Vap) |
| F6-26 | in_scope | text | maybe | no |
| F6-27 | states | text | loose (Dr 0); intermediate (Dr 0.3) | loose; intermediate |
| F6-27 | apparatus | text | 1/6-scale LM model; LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-27 | rate_or_dynamics | text | NASA drops 1 to 8 (F6-10); damping of the computation not stated | NASA 1 to 8 per F6-10, nominal VV/VH 10/0 or 5/7 ft/s |
| F6-27 | trace_classes | text | recorded-trace;computed | computed |
| F6-27 | legend_entries | text | Drop No. 1 Dmax = 4.3 in.;Drop No. 2 Dmax = 4.2 in.;Drop No. 3 Dmax = 4.2 in.;Drop No. 4 Dmax = 5.3 in.;Drop No. 5 Dmax = 3.4 in.;Drop No. 6 Dmax = 3.0 in.;Drop No. 7 Dmax = 3.3 in.;Drop No. 8 Dmax = 3.7 in. | Drop No. 1;Drop No. 2;Drop No. 3;Drop No. 4;Drop No. 5;Drop No. 6;Drop No. 7;Drop No. 8 |
| F6-27 | in_scope | text | maybe | yes |
| F6-11-p376 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-11-p376 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-11-p376 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -60.5 in/s and VH 83.5 in/s |
| F6-11-p376 | x_quantity | text | elapsed time | time |
| F6-11-p376 | relation_target | text | F6-10;F5-38;F5-39;F5-35;F5-37 | F5-38;F5-39;F5-35;F5-37 |
| F6-11-p377 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-11-p377 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-11-p377 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -60.5 in/s and VH 83.5 in/s |
| F6-11-p377 | x_quantity | text | elapsed time | time |
| F6-11-p377 | y_quantity | text | c.g. Vertical Velocity Xdot | vehicle c.g. vertical velocity (X dot) |
| F6-11-p377 | relation_target | text | F6-10;F5-34;F5-36;F5-33 | F5-34;F5-36;F5-33 |
| F6-11-p378 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-11-p378 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-11-p378 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -60.5 in/s and VH 83.5 in/s |
| F6-11-p378 | x_quantity | text | elapsed time | time |
| F6-11-p378 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-12-p381 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-12-p381 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-12-p381 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -60.5 in/s and VH 83.5 in/s |
| F6-12-p381 | y_unit | text | deg_s2 | n/a |
| F6-12-p381 | in_scope | text | maybe | no |
| F6-12-p382 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-12-p382 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-12-p382 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -60.5 in/s and VH 83.5 in/s |
| F6-12-p382 | y_quantity | text | c.g. Horizontal Velocity Ydot | vehicle c.g. horizontal velocity (Y dot) |
| F6-12-p382 | in_scope | text | maybe | no |
| F6-12-p383 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-12-p383 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-12-p383 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -60.5 in/s and VH 83.5 in/s |
| F6-12-p383 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-12-p383 | in_scope | text | maybe | no |
| F6-13-p385 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-13-p385 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-13-p385 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -114.9 in/s and VH 0 |
| F6-13-p385 | x_quantity | text | elapsed time | time |
| F6-13-p385 | relation_target | text | F6-10;F5-28 | F5-28 |
| F6-13-p386 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-13-p386 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-13-p386 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -114.9 in/s and VH 0 |
| F6-13-p386 | x_quantity | text | elapsed time | time |
| F6-13-p386 | y_quantity | text | c.g. Vertical Velocity Xdot | vehicle c.g. vertical velocity (X dot) |
| F6-13-p386 | relation_target | text | F6-10;F5-27;F5-26 | F5-27;F5-26 |
| F6-13-p387 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-13-p387 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-13-p387 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -114.9 in/s and VH 0 |
| F6-13-p387 | x_quantity | text | elapsed time | time |
| F6-13-p387 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-14-p389 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-14-p389 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-14-p389 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-14-p389 | x_quantity | text | elapsed time | time |
| F6-14-p390 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-14-p390 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-14-p390 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-14-p390 | x_quantity | text | elapsed time | time |
| F6-14-p390 | y_quantity | text | c.g. Vertical Velocity Xdot | vehicle c.g. vertical velocity (X dot) |
| F6-14-p391 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-14-p391 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-14-p391 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-14-p391 | x_quantity | text | elapsed time | time |
| F6-14-p391 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-15-p393 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-15-p393 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-15-p393 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-15-p393 | x_quantity | text | elapsed time | time |
| F6-15-p394 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-15-p394 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-15-p394 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-15-p394 | x_quantity | text | elapsed time | time |
| F6-15-p394 | y_quantity | text | c.g. Vertical Velocity Xdot | vehicle c.g. vertical acceleration (X double dot) |
| F6-15-p395 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-15-p395 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-15-p395 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-15-p395 | x_quantity | text | elapsed time | time |
| F6-15-p395 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-16-p397 | states | text | intermediate (Dr printed "3", 53.0 pcf, phi 42.5) | intermediate (53.0 pcf) |
| F6-16-p397 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-16-p397 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-16-p397 | x_quantity | text | elapsed time | time |
| F6-16-p397 | y_quantity | text | Vehicle Pitch Rate | vehicle pitch angle |
| F6-16-p398 | states | text | intermediate (Dr printed "3", 53.0 pcf, phi 42.5) | intermediate (53.0 pcf) |
| F6-16-p398 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-16-p398 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-16-p398 | x_quantity | text | elapsed time | time |
| F6-16-p398 | y_quantity | text | c.g. Vertical Velocity Xdot | vehicle c.g. vertical velocity (X dot) |
| F6-16-p399 | states | text | intermediate (Dr printed "3", 53.0 pcf, phi 42.5) | intermediate (53.0 pcf) |
| F6-16-p399 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-16-p399 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-16-p399 | x_quantity | text | elapsed time | time |
| F6-16-p399 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-17-p401 | states | text | intermediate (Dr 0.3, 53.0 pcf, phi 42.5) | intermediate (Dr 0.3, 53.0 pcf) |
| F6-17-p401 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-17-p401 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-17-p401 | x_quantity | text | elapsed time | time |
| F6-17-p402 | states | text | intermediate (Dr 0.3, 53.0 pcf, phi 42.5) | intermediate (Dr 0.3, 53.0 pcf) |
| F6-17-p402 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-17-p402 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-17-p402 | x_quantity | text | elapsed time | time |
| F6-17-p402 | y_quantity | text | c.g. Vertical Velocity Xdot | vehicle c.g. vertical velocity (X dot) |
| F6-17-p403 | states | text | intermediate (Dr 0.3, 53.0 pcf, phi 42.5) | intermediate (Dr 0.3, 53.0 pcf) |
| F6-17-p403 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-17-p403 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-17-p403 | x_quantity | text | elapsed time | time |
| F6-17-p403 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-18-p405 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-18-p405 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-18-p405 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-18-p405 | x_quantity | text | elapsed time | time |
| F6-18-p406 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-18-p406 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-18-p406 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-18-p406 | x_quantity | text | elapsed time | time |
| F6-18-p406 | y_quantity | text | c.g. Vertical Velocity Xdot | vehicle c.g. vertical velocity (X dot) |
| F6-18-p407 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-18-p407 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-18-p407 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); computed with strut damping 10 Sdot | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-18-p407 | x_quantity | text | elapsed time | time |
| F6-18-p407 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-19-p409 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-19-p409 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-19-p409 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-19-p409 | x_quantity | text | elapsed time | time |
| F6-19-p410 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-19-p410 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-19-p410 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-19-p410 | x_quantity | text | elapsed time | time |
| F6-19-p410 | y_quantity | text | c.g. Vertical Velocity Xdot | vehicle c.g. vertical velocity (X dot) |
| F6-19-p411 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-19-p411 | apparatus | text | 1/6-scale LM model (No. 1 footpad); LM Landing Dynamics Computer Program | 1/6-scale LM model; leg set 1 instrumented; LM Landing Dynamics Computer Program |
| F6-19-p411 | rate_or_dynamics | text | free drop, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); computed with strut damping 10 Sdot | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-19-p411 | x_quantity | text | elapsed time | time |
| F6-19-p411 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-20-p413 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-20-p413 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-20-p413 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -114.9 in/s and VH 0 |
| F6-20-p413 | y_unit | text | deg_s2 | n/a |
| F6-20-p413 | in_scope | text | maybe | no |
| F6-20-p414 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-20-p414 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-20-p414 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -114.9 in/s and VH 0 |
| F6-20-p414 | y_quantity | text | c.g. Horizontal Velocity Ydot | vehicle c.g. horizontal velocity (Y dot) |
| F6-20-p414 | in_scope | text | maybe | no |
| F6-20-p415 | states | text | loose (Dr 0, 46.9 pcf, phi 41) | loose (Dr 0, 46.9 pcf) |
| F6-20-p415 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-20-p415 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground, T5-3 VV -114.9 in/s and VH 0 |
| F6-20-p415 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-20-p415 | in_scope | text | maybe | no |
| F6-21-p417 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-21-p417 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-21-p417 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-21-p417 | y_unit | text | inch | n/a |
| F6-21-p417 | in_scope | text | maybe | no |
| F6-21-p418 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-21-p418 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-21-p418 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-21-p418 | y_quantity | text | c.g. Horizontal Velocity Ydot | vehicle c.g. horizontal velocity (Y dot) |
| F6-21-p418 | in_scope | text | maybe | no |
| F6-21-p419 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-21-p419 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-21-p419 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-21-p419 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-21-p419 | in_scope | text | maybe | no |
| F6-22-p421 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-22-p421 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-22-p421 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-22-p421 | y_unit | text | deg_s2 | n/a |
| F6-22-p421 | in_scope | text | maybe | no |
| F6-22-p422 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-22-p422 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-22-p422 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-22-p422 | y_quantity | text | c.g. Horizontal Velocity Ydot | vehicle c.g. horizontal velocity (Y dot) |
| F6-22-p422 | in_scope | text | maybe | no |
| F6-22-p423 | states | text | loose (Dr 0, 47.1 pcf, phi 41) | loose (Dr 0, 47.1 pcf) |
| F6-22-p423 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-22-p423 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-22-p423 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-22-p423 | in_scope | text | maybe | no |
| F6-23-p425 | states | text | intermediate (Dr printed "3", 53.0 pcf, phi 42.5) | intermediate (53.0 pcf) |
| F6-23-p425 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-23-p425 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-23-p425 | y_unit | text | deg_s2 | n/a |
| F6-23-p425 | in_scope | text | maybe | no |
| F6-23-p426 | states | text | intermediate (Dr printed "3", 53.0 pcf, phi 42.5) | intermediate (53.0 pcf) |
| F6-23-p426 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-23-p426 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-23-p426 | y_quantity | text | c.g. Horizontal Velocity Ydot | vehicle c.g. horizontal velocity (Y dot) |
| F6-23-p426 | in_scope | text | maybe | no |
| F6-23-p427 | states | text | intermediate (Dr printed "3", 53.0 pcf, phi 42.5) | intermediate (53.0 pcf) |
| F6-23-p427 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-23-p427 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-23-p427 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-23-p427 | in_scope | text | maybe | no |
| F6-24-p429 | states | text | intermediate (Dr 0.3, 53.0 pcf, phi 42.5) | intermediate (Dr 0.3, 53.0 pcf) |
| F6-24-p429 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-24-p429 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-24-p429 | y_unit | text | deg_s2 | n/a |
| F6-24-p429 | in_scope | text | maybe | no |
| F6-24-p430 | states | text | intermediate (Dr 0.3, 53.0 pcf, phi 42.5) | intermediate (Dr 0.3, 53.0 pcf) |
| F6-24-p430 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-24-p430 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-24-p430 | y_quantity | text | c.g. Horizontal Velocity Ydot | vehicle c.g. horizontal velocity (Y dot) |
| F6-24-p430 | in_scope | text | maybe | no |
| F6-24-p431 | states | text | intermediate (Dr 0.3, 53.0 pcf, phi 42.5) | intermediate (Dr 0.3, 53.0 pcf) |
| F6-24-p431 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-24-p431 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-24-p431 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-24-p431 | in_scope | text | maybe | no |
| F6-25-p433 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-25-p433 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-25-p433 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-25-p433 | in_scope | text | maybe | no |
| F6-25-p434 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-25-p434 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-25-p434 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-25-p434 | y_quantity | text | c.g. Horizontal Velocity Ydot | vehicle c.g. horizontal velocity (Y dot) |
| F6-25-p434 | in_scope | text | maybe | no |
| F6-25-p435 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-25-p435 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-25-p435 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 5 fps, VH 7 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 5 ft/s, VH 7 ft/s nominal, 45 deg yaw, level ground |
| F6-25-p435 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-25-p435 | in_scope | text | maybe | no |
| F6-26-p437 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-26-p437 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-26-p437 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-26-p437 | y_unit | text | deg_s2 | n/a |
| F6-26-p437 | in_scope | text | maybe | no |
| F6-26-p438 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-26-p438 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-26-p438 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-26-p438 | y_quantity | text | c.g. Horizontal Velocity Ydot | vehicle c.g. horizontal velocity (Y dot) |
| F6-26-p438 | in_scope | text | maybe | no |
| F6-26-p439 | states | text | loose (Dr 0, 96.0 pcf, phi 30) | loose (Dr 0, 96.0 pcf) |
| F6-26-p439 | apparatus | text | LM Landing Dynamics Computer Program with semi-empirical footpad/soil force laws | LM Landing Dynamics Computer Program |
| F6-26-p439 | rate_or_dynamics | text | computed landing, 45 deg yaw, level ground, VV 10 fps, VH 0 fps (F6-10); strut damping 10 Sdot^1/2 primary, 30 Sdot^1/2 secondary | VV 10 ft/s, VH 0 ft/s nominal, 45 deg yaw, level ground |
| F6-26-p439 | y_quantity | text | Footpad Pitch Angle alpha | footpad pitch angle (alpha) |
| F6-26-p439 | in_scope | text | maybe | no |
