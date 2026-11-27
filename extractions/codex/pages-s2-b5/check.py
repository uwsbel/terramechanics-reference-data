from pathlib import Path
import json,re
expected={117,118,119,120,121,122,123,124,125,126,127,129,130,131,132,133,134,135,136,137,138}
files=sorted(Path('out').glob('p[0-9][0-9][0-9][0-9].md'))
assert {int(p.stem[1:]) for p in files}==expected
figs=[]
markers=[]
for p in files:
 s=p.read_text(encoding='utf-8')
 bits=s.split('---\n',2)
 assert len(bits)==3,p
 h={k:json.loads(v.strip()) for k,v in (line.split(':',1) for line in bits[1].splitlines())}
 n=int(p.stem[1:])
 assert h['pdf_page']==n
 assert h['source']=='bendix-1968-vol1'
 assert h['printed_page']==f'2-{n-25}'
 assert h['image']==f'corpus/1968/images/p{n:04}.png'
 assert h['transcriber']=='codex' and h['review_status']=='single-reading'
 assert h['rotation'] in [0,90]
 body=bits[2]
 ids=re.findall(r'^::: figure (\S+)$',body,re.M)
 assert ids==h['figures'],(p,ids)
 for field in ['caption','axes','legend','description']:
  assert len(re.findall('^'+field+':',body,re.M))==len(ids),(p,field)
 assert body.count(':::')==2*len(ids)
 assert body.count('$')%2==0,p
 assert '\ufffd' not in s,p
 for marker in ['[?]','[sic]','[illegible]']:
  if marker in s: markers.append((p.name,marker,s.count(marker)))
 figs.extend(ids)
print(f'Validated {len(files)} page files and {len(figs)} figure blocks.')
print('Markers:',markers)
print('Notes present:',Path('out/notes.md').is_file())
print('Pages:',', '.join(p.name for p in files))
