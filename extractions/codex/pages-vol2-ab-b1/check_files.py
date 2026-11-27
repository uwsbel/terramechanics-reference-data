from pathlib import Path
import re

folder = Path(__file__).parent
files = sorted(folder.glob('p[0-9][0-9][0-9][0-9].md'))
assert len(files) == 23
assert [p.stem for p in files] == [f'p{n:04d}' for n in range(2,25)]
expected = {'source', 'pdf_page', 'printed_page', 'sections', 'figures', 'tables', 'equations', 'rotation', 'image', 'transcriber', 'review_status'}
figures = []
for p in files:
    s = p.read_text(encoding='utf-8')
    header, body = s.split('---')[1:3]
    fields = dict(line.split(': ', 1) for line in header.strip().splitlines())
    assert set(fields) == expected
    assert fields['source'] == 'bendix-1968-vol2'
    assert fields['transcriber'] == 'codex'
    assert fields['review_status'] == 'single-reading'
    assert int(fields['pdf_page']) == int(p.stem[1:])
    assert fields['image'] == f'corpus/1968-vol2/images/{p.stem}.png'
    assert fields['printed_page'].startswith('"') and fields['printed_page'].endswith('"')
    blocks = re.findall(r'::: figure (FA-\d+)\ncaption: .+\naxes:.*\nlegend:.*\ndescription: .+\n:::', s)
    assert len(blocks) == s.count('::: figure')
    assert fields['figures'] == '[' + ', '.join(blocks) + ']'
    figures.extend(blocks)
    assert s.count('$') % 2 == 0
    print(p.name, fields['printed_page'], 'rotation='+fields['rotation'], 'doubts='+str(s.count('[?]')))
assert set(figures) == {f'FA-{n}' for n in range(1,13)}
assert (folder/'notes.md').exists()
print('PASS: 23 page files, all required headers, 12 figure blocks, notes.md.')
