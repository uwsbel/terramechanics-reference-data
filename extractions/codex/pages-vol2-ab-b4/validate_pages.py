from pathlib import Path
import re

out = Path(__file__).parent
files = sorted(out.glob('p[0-9][0-9][0-9][0-9].md'))
assert len(files) == 25
questions, sics, figures = [], [], []
for n, p in zip(range(73, 98), files):
    s = p.read_text(encoding='utf-8')
    head, body = s.split('---', 2)[1:]
    assert p.name == f'p{n:04d}.md'
    for field in [f'pdf_page: {n}\n', f'printed_page: "A-{n-1}"',
                  'source: bendix-1968-vol2', 'transcriber: codex',
                  'review_status: single-reading',
                  f'image: corpus/1968-vol2/images/p{n:04d}.png']:
        assert field in head, (p, field)
    assert body.strip()
    assert body.count('$') % 2 == 0
    questions.extend([p.name] * body.count('[?]'))
    sics.extend([p.name] * body.count('[sic]'))
    blocks = re.findall(r'::: figure (FA-\d+)', body)
    figures.extend(blocks)
    for f in blocks:
        assert f'figures: [{f}]' in head
    assert body.count('\n:::') == 2 * len(blocks)
assert len(figures) == 12 and len(set(figures)) == 12
assert len(questions) == 3
assert len(sics) == 5
assert (out / 'notes.md').exists()
print('25 page files; 12 figure blocks; required headers and delimiters checked.')
print('Uncertainty markers:', ', '.join(questions))
print('Sic markers:', ', '.join(sics))
print('notes.md present.')
