from pathlib import Path
p=Path('out/write_pages.py')
s=p.read_text(encoding='utf-8')
s=s.replace('11.80- |','11.80- [sic] |')
s=s.replace('Knowledge of all these values','Knowledge of all these-values [sic]')
s=s.replace('The values for the grain size curve characteristics described above','The-values [sic] for the grain size curve characteristics described above')
s=s.replace('Make-three or four','Make-three [sic] or four')
p.write_text(s,encoding='utf-8')
