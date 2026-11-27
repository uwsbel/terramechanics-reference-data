"""Merge the two blind source-hunt registers into sources/leads.csv and sources/searches-log.csv.

Usage: python tools/merge_leads.py <claude_leads> <codex_leads> <claude_searches> <codex_searches> <matches.json>

matches.json maps a Claude lead_id to the Codex lead_id of the same source (matched by report
number, DOI or URL during review). Shared leads keep the Codex id (author-year scheme), take
each field from whichever submission filled it, carry both agents' priority, rights and data-form
grades, take the lower priority number (acquire sooner) and the stricter rights reading until the
rights evidence is checked. One-sided leads are carried with found_by = claude or codex.
"""
import csv, json, sys, collections
from pathlib import Path

COLS = ['lead_id','title','authors','year','report_or_doi','archive','url','rights_assessment','rights_evidence',
        'test_types','materials','data_form','setup_recoverability','gravity_condition','relation_to_bendix','priority','notes']
ORDER = {'public_domain': 0, 'open_license': 1, 'unknown': 2, 'restricted': 3}

def read(p):
    with Path(p).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def main(a_path, b_path, sa_path, sb_path, match_path):
    A, B = read(a_path), read(b_path)
    match = json.loads(Path(match_path).read_text(encoding='utf-8'))
    Bd = {r['lead_id']: r for r in B}
    out, used, disagreements = [], set(), []
    for a in A:
        cid = match.get(a['lead_id'])
        if cid and cid in Bd:
            b = Bd[cid]; used.add(cid)
            row = {c: (b[c] if b[c] and b[c] != 'unknown' else a[c]) for c in COLS}
            row['lead_id'] = cid
            row['found_by'] = 'both'
            row['priority'] = str(min(int(a['priority']), int(b['priority'])))
            row['rights_assessment'] = max(a['rights_assessment'], b['rights_assessment'], key=lambda v: ORDER.get(v, 2))
            row['notes'] = ('claude: ' + a['notes'] + ' | codex: ' + b['notes']).strip(' |')
            row.update(claude_priority=a['priority'], codex_priority=b['priority'], claude_rights=a['rights_assessment'],
                       codex_rights=b['rights_assessment'], claude_data_form=a['data_form'], codex_data_form=b['data_form'])
            for c in ('rights_assessment', 'data_form', 'setup_recoverability', 'priority'):
                if a[c] != b[c] and 'unknown' not in (a[c], b[c]):
                    disagreements.append((cid, c, a[c], b[c]))
        else:
            row = {c: a[c] for c in COLS}
            row.update(found_by='claude', claude_priority=a['priority'], codex_priority='', claude_rights=a['rights_assessment'],
                       codex_rights='', claude_data_form=a['data_form'], codex_data_form='')
        out.append(row)
    for b in B:
        if b['lead_id'] in used:
            continue
        row = {c: b[c] for c in COLS}
        row.update(found_by='codex', claude_priority='', codex_priority=b['priority'], claude_rights='',
                   codex_rights=b['rights_assessment'], claude_data_form='', codex_data_form=b['data_form'])
        out.append(row)
    out.sort(key=lambda r: (int(r['priority']) if r['priority'].isdigit() else 9, r['year'], r['lead_id']))
    fields = COLS + ['found_by', 'claude_priority', 'codex_priority', 'claude_rights', 'codex_rights', 'claude_data_form', 'codex_data_form']
    with open('sources/leads.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(out)
    S = []
    for agent, p in (('claude', sa_path), ('codex', sb_path)):
        for r in read(p):
            r['agent'] = agent; S.append(r)
    with open('sources/searches-log.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['agent', 'archive', 'query', 'date', 'result_count', 'useful', 'notes']); w.writeheader(); w.writerows(S)
    print('leads', len(out), dict(collections.Counter(r['found_by'] for r in out)))
    print('priority', dict(collections.Counter(r['priority'] for r in out)), 'rights', dict(collections.Counter(r['rights_assessment'] for r in out)))
    print('searches', len(S), dict(collections.Counter(r['agent'] for r in S)))
    for d in disagreements:
        print('  grade disagreement', d)

if __name__ == '__main__':
    main(*sys.argv[1:6])
