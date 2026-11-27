You are building the figure and table inventory of Section II of a scanned 1968 NASA report for Dan Negrut's Apollo-era soil-test data project. Work from the page images. Do not use em-dashes or en-dashes.

## The pages

`nasa-reports/1968-nasa-LunarModule-SoilMechanicsStudy.pdf` (read-only), Section II "Soil Selection and Control", printed pages 2-1 to 2-113, PDF pages 26 to 138 (printed = PDF minus 25). Table 1-1 on PDF 20 is also in scope. The list of illustrations (PDF 8 to 9) and list of tables (PDF 14) give the figure and table titles, but they are an index, not evidence: render and look at every page that holds a figure or table before classifying it. Render with Ghostscript (on PATH), for example

```
gswin64c -q -dNOPAUSE -dBATCH -sDEVICE=pnggray -r150 -dFirstPage=48 -dLastPage=48 -sOutputFile=<temp>/p0048.png nasa-reports/1968-nasa-LunarModule-SoilMechanicsStudy.pdf
```

(use -r300 when a plot is dense). Some pages are printed rotated; rotate the image before reading.

## Project context that defines the classification

The project recovers physical measurements as data and will reproduce the simple tests in a continuum soil simulator (Chrono CRM, mu(I) rheology baseline). Twelve test soils (soil numbers 1 to 12, families RS, PS, RSM-a, RSM-b, RC2, SS, LSM, at loose, intermediate and dense states). Scope: static tests (grain size, density, direct shear, triaxial, static load-penetration with cylinders and footpad, static penetrometer) plus dynamic penetration (dynamic penetrometer DPT). Priority 1 means a calibration or prediction target for the simulator; 2 means supporting data needed to set up or interpret a test (apparatus dimensions, bed density control, rate effects, bin-size effects); 3 means context. Apparatus drawings and photographs are not data but are in scope at priority 2 when they supply a dimension or a procedure a simulation needs. Flag `mcc_relevant` = yes for anything about compaction, densification during testing, bed reuse, or history dependence (that decides whether a second rheology, MCC, is needed).

## Output

Return in your final message ONE fenced CSV block, one row per figure or table in Section II (plus Table 1-1), with exactly these columns:

`id,kind,title_as_printed,printed_page,pdf_page,test_type,soils,states,apparatus,rate_or_dynamics,data_form,panels,curves,trace_classes,x_quantity,x_unit,x_axis_type,y_quantity,y_unit,y_axis_type,legend_entries,rotation,in_scope,priority,mcc_relevant,notes`

- `id`: F2-21 for Figure 2-21, T2-3 for Table 2-3, T1-1.
- `kind`: figure or table.
- `test_type`: one of grain size, density, direct shear, triaxial, load penetration, static penetrometer, dynamic penetrometer, drag test, impact test, soil model, soil properties, bed preparation, apparatus, other.
- `soils`: soil numbers or families shown (for example "RS (1,3,4)"), "all", "example", or "none".
- `states`: loose, intermediate, dense, Dr values, or "n/a".
- `apparatus`: e.g. "2 inch cylinder", "4 inch footpad", "shear box", "DPT", "sieve", "none".
- `rate_or_dynamics`: static, rate series, dynamic, derived, n/a.
- `data_form`: curve, table, schematic, photo, text, mixed.
- `panels`: number of plot panels on the page (0 for non-plots).
- `curves`: total number of distinct traces across panels (0 if none).
- `trace_classes`: for each trace or group, one of measurement-markers, recorded-trace, author-fit, computed, schematic, setup-evidence; list them separated by semicolons (e.g. "measurement-markers;author-fit").
- `x_quantity`, `x_unit`, `x_axis_type` (linear, log, normalized), and the same for y: verbatim from the axis labels; for tables, the column headers go in `notes` and these stay "n/a". If a page has panels with different axes, give the primary panel and list the others in `notes`.
- `legend_entries`: the legend text verbatim, entries separated by semicolons (abbreviate only if very long and say so in notes).
- `rotation`: 0 if the page reads upright, 90 or 270 if the figure is printed sideways.
- `in_scope`: yes, no, maybe. `priority`: 1, 2, 3. `mcc_relevant`: yes or no.
- `notes`: anything that matters for extracting the data later: multipliers on axes (e.g. "x 10^3 in."), inset tables, labels printed beside curves (normal stress, unit weight, rate), legibility problems, whether multiple figures share a page or one figure spans two pages, and for tables the column headers.

After the CSV, add a section "Observations" with: the figures you consider the most valuable for calibration and for prediction and why; any figure whose title misled you about its content; any page where the list of illustrations and the page disagree (number, title, or page); pages you could not read well; and anything that surprised you. Mark anything you did not actually look at.
