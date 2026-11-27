from pathlib import Path
import json,re,csv
expected={p.stem for p in Path('packet').glob('p*.png')}
actual={p.stem for p in Path('out').glob('p*.md')}
assert expected == actual,(expected-actual,actual-expected)
ids={int(row['pdf_page']):row['id'] for row in csv.DictReader(Path('packet/figures-rows.csv').open(encoding='utf-8-sig'))}
for p in sorted(Path('out').glob('p*.md')):
    s=p.read_text(encoding='utf-8'); head,body=s.split('---',2)[1:]
    fields=dict(line.split(': ',1) for line in head.strip().splitlines())
    n=int(fields['pdf_page'])
    assert p.stem==f'p{n:04d}'
    assert fields['source']=='bendix-1968-vol1'
    assert fields['transcriber']=='codex'
    assert fields['review_status']=='single-reading'
    assert fields['image']==f'corpus/1968/images/p{n:04d}.png'
    assert fields['printed_page']==f'"2-{n-25}"'
    figs=json.loads(fields['figures'])
    assert figs==([ids[n]] if n in ids else [])
    assert body.count('::: figure ')==len(figs)
    assert body.count('$$')%2==0
    for fig in figs:
        assert f'::: figure {fig}\ncaption:' in body
        assert '\naxes:' in body and '\nlegend:' in body and '\ndescription:' in body
    print(f'{p.name}: {len(body.split())} words; [?]={body.count("[?]")}; [illegible]={body.count("[illegible]")}; [sic]={body.count("[sic]")}')
assert Path('out/notes.md').is_file()
print('PASS: 22 expected page files, required headers, figure IDs, figure block fields, and notes.md.')
