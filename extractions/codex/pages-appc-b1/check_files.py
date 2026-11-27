from pathlib import Path
import csv

root = Path('out')
files = sorted(root.glob('p[0-9][0-9][0-9][0-9].md'))
assert len(files) == 23
with open('packet/figures-rows.csv', encoding='utf-8-sig', newline='') as f:
    ids = {int(r['pdf_page']): r['id'] for r in csv.DictReader(f)}
markers = []
for n in range(115, 138):
    p = root / f'p{n:04}.md'
    t = p.read_text(encoding='utf-8')
    assert t.startswith('---\n')
    fields = [f'pdf_page: {n}', f'printed_page: "C-{n-114}"',
              'source: bendix-1968-vol2', 'transcriber: codex',
              'review_status: single-reading',
              f'image: corpus/1968-vol2/images/p{n:04}.png',
              f'rotation: {90 if n >= 136 else 0}']
    for field in fields:
        assert field + '\n' in t, (p.name, field)
    if n > 115:
        assert f'figures: ["{ids[n]}"]\n' in t
        assert f'::: figure {ids[n]}\n' in t
        assert all(k in t for k in ('caption: ', 'axes: ', 'legend: ', 'description: '))
        assert t.count(':::') == 2
    for mark in ('[?]', '[sic]', '[illegible]'):
        if mark in t:
            markers.append((p.name, mark, t.count(mark)))
notes = (root / 'notes.md').read_text(encoding='utf-8')
assert len(notes) > 0
for name, mark, count in markers:
    assert name[:-3] in notes
print('Validated: 23 page files, 22 figure blocks, and notes.md.')
print('Markers:', markers)
