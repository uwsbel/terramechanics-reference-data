from pathlib import Path
import re

root=Path(__file__).parent
files=sorted(root.glob('p[0-9][0-9][0-9][0-9].md'))
assert len(files)==24
marks=[]
figures=0
tables=0
for n,p in zip(range(49,73),files):
    s=p.read_text(encoding='utf-8')
    assert p.name==f'p{n:04d}.md'
    h,b=s.split('---',2)[1:]
    assert f'pdf_page: {n}' in h
    assert f'printed_page: "A-{n-1}"' in h
    assert 'transcriber: codex' in h and 'review_status: single-reading' in h
    assert f'image: corpus/1968-vol2/images/p{n:04d}.png' in h
    assert s.count('$')%2==0
    assert '\ufffd' not in s
    blocks=re.findall(r'::: figure (.*?)\n(.*?)\n:::',b,re.S)
    for fid,body in blocks:
        assert f'figures: [{fid}]' in h
        assert [x.split(':',1)[0] for x in body.splitlines()]==['caption','axes','legend','description']
    figures+=len(blocks)
    tables+=int('tables: [TA-' in h)
    if '[?]' in s or '[sic]' in s or '[illegible]' in s:
        marks.append((p.name,s.count('[?]'),s.count('[sic]'),s.count('[illegible]')))
assert (root/'notes.md').is_file()
assert figures==13 and tables==4
print('Validated: 24 page files, 13 figure blocks, 4 table locators, notes.md')
print('Marker counts (file, doubtful, sic, illegible):')
print(*marks,sep='\n')
