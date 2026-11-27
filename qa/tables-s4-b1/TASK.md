# Blind transcription of a printed table: Figure 4-6a of a 1968 NASA report (batch tables-s4-b1)

You are one of two independent readers of a printed table from a 1968 NASA report (Bendix AM-68-1 Vol. I, Lunar
Module soil mechanics study). The other reader works elsewhere; do not look for or use any other reading. Your
transcription will be compared with the other cell by cell; every number must match the page exactly, and
disagreements are settled from the page image with credit to whichever reading was right. Read carefully, and say
what you could not read rather than guess. US English; no em-dashes or en-dashes.

## Evidence (folder `packet/`)

- `p0193.png`: Figure 4-6a, "Subscale Drag Test Results - Soil No. 1 - RS Loose", printed page 4-8. The page is
  printed **sideways**: turn it to read it (the 300 dpi scan is unrotated).
- `p0191.png` (printed 4-6: Figure 4-4, the nomenclature of the constant-penetration drag tests, and Figure 4-5, a drag
  test record) and `p0192.png` (printed 4-7: how the records were read). Context only; nothing on them is a cell.
- `tools/plot_grid.py crop <image> --box u0 v0 u1 v1 --zoom 3 --out <png>` makes a zoomed crop with a pixel grid
  (run `--help` first). Python: `<local path>`. Look at crops with your image
  viewer. Work only inside your workspace; write everything under `out/`.

## What to produce

1. `out/table.csv`: one row per printed run, in printed order, with these columns:

   ```
   run_number,D_in,d_in,VH_fps,gp_bar,Dr,gamma_pcf,FD_lb,FV_lb,FD_over_d_gamma_Aft,VH_over_sqrt_dg,FD_over_Aft,FV_over_Apt,alpha_deg,note
   ```

   The columns are the table's 14 columns from left to right: Run Number; D (Inch); d (Inch); V_H (fps); g_p with a
   bar (mean DPT reading); D_r; gamma (Lb./Ft.^3); F_D (Lb.); F_V (Lb.); F_D / (d gamma A_ft); V_H / sqrt(d g);
   F_D / A_ft; F_V / A_pt; alpha (Deg.). If the page's columns differ from this list, follow the page and say so.

2. Rules for cells:
   - Every value **exactly as printed**: keep the decimals printed ("2.82", "12.0", "0.43"); write fractions as
     printed with a space between whole and fraction ("1 1/2", "1/2", "3 3/4"); do not compute or round.
   - A blurred or broken digit you can still read with confidence: write the digit and say in `note` which cell and
     why. A digit you cannot read: write `?` in its place (for example `4?.1`) and explain in `note`. Never guess.
   - Run numbers as printed ("1-1", "1-10"). Note any gap in the sequence (a run number not printed) in `note` of the
     row after it.
   - `note`: anything about that row (a cell damaged, a mark on the page); empty otherwise.

3. `out/notes.md`:
   - the table's caption and header as printed, column by column (units, symbols as you read them);
   - the definitions of A_ft and A_pt and of any symbol in the derived columns, as printed on PDF 191 or 192 (quote
     them with their location), or say that they are not printed there;
   - every cell you were unsure of, with its pixel position on the scan;
   - anything else a careful reader should know (stray marks, the scan's quality).

When you finish, report briefly: rows and columns transcribed, the cells you were unsure of, and the definitions found.
