"""Apply the second precision sample (prec2/), the Wolff locus check (wolff_loci.json) and the rows the recall readers
judged wrong (rec/) to the editions.

Precision verdicts go in `audit` as in the first audit: weak match rows become possible, wrong rows rejected
(`audit.statusWas`), changed labels keep `audit.labelWas`. Wolff rows whose locus names a § that the source passage only
cites (the passage stands in another §) take the § where the passage stands (`locusCheck` {was, date}).
Rows of a later pass are edited in their pass file, rows of data.json through corrections.json rowEdits.

usage: apply_checks2.py <work> <repo> <vattel data.json> <burlamaqui data.json> [--write]
"""
import json, os, re, sys, glob, collections

S, R, VD, BD = sys.argv[1:5]
WRITE = '--write' in sys.argv
DATE = '2026-11-18'
LABELS = {'verbatim', 'close paraphrase', 'loose paraphrase', 'translation', 'shared argument', 'citation', 'open disagreement', 'commonplace'}
def load(p): return json.load(open(p, encoding='utf-8'))

data_ids = {'vattel-1773': {r['id']: r for r in load(VD)['rows']}, 'burlamaqui-1747': {r['id']: r for r in load(BD)['rows']}}
passes = {}
def pass_rows(ed, table):
    p = f'{R}/editions/{ed}/passes/{table}.json'
    if not os.path.exists(p): return None
    if p not in passes: passes[p] = load(p)
    return {r['id']: r for r in passes[p]['rows']}
corr = {ed: load(f'{R}/editions/{ed}/corrections.json') for ed in data_ids}
edits = {ed: {e['id']: e for e in corr[ed].get('rowEdits', [])} for ed in data_ids}

class Row:
    def __init__(self, ed, table, rid):
        pr = pass_rows(ed, table)
        if pr is not None: self.p = pr[rid]; self.e = None
        else:
            base = data_ids[ed][rid]; self.p = None
            self.e = edits[ed].setdefault(rid, {'id': rid})
            self.base = {'label': base['label'], 'status': base['status'], 'audit': base.get('audit'), 'labelCheck': base.get('labelCheck'),
                         'locus': base['locus']}
    def get(self, k):
        if self.p is not None: return self.p.get(k)
        return self.e[k] if k in self.e else self.base[k]
    def set(self, k, v):
        if self.p is not None: self.p[k] = v
        else: self.e[k] = v

# 1. second precision sample
smp = {s['key']: s for s in load(f'{S}/prec2/sample.json')['sample']}
V = {}
for f in sorted(glob.glob(f'{S}/prec2/out/*.json')):
    for it in load(f)['items']: V[it['key']] = it
st = collections.Counter(); labs = collections.Counter()
for k, v in sorted(V.items()):
    s = smp[k]; r = Row(s['edition'], s['table'], s['id'])
    assert r.get('status') == 'match' and not r.get('audit'), (k, r.get('status'))
    a = {'verdict': v['verdict'], 'reason': v['reason'], 'date': DATE}
    if not v.get('label_ok', True) and v.get('better_label') and v['better_label'].strip().lower() != r.get('label'):
        bl = v['better_label'].strip().lower(); assert bl in LABELS, (k, bl)
        a['labelWas'] = r.get('label'); r.set('label', bl); labs[(a['labelWas'], bl)] += 1
    if v['verdict'] == 'weak': r.set('status', 'possible'); a['statusWas'] = 'match'
    if v['verdict'] == 'wrong': r.set('status', 'rejected'); a['statusWas'] = 'match'
    r.set('audit', a); st[(s['edition'], v['verdict'])] += 1
print('precision 2:', dict(st), 'labels', sum(labs.values()), labs.most_common())

# 2. Wolff loci
lc = collections.Counter()
for x in load(f'{S}/wolff_loci.json'):
    m = re.match(r'§\s*(\d+)$', (x['locus'] or '').strip()); o = int(m.group(1)) if m else None
    if o is None or x['found_para'] is None or abs(o - x['found_para']) <= 1 or x['ratio'] < 0.95 or x['page'] != x['found_page']: continue
    r = Row(x['edition'], x['table'], x['id']); assert r.get('locus') == x['locus'], x
    r.set('locus', '§ %d' % x['found_para']); r.set('locusCheck', {'was': x['locus'], 'date': DATE}); lc[x['table']] += 1
print('loci:', dict(lc))

# 3. rows the recall readers judged wrong
TAB = {'wolff-jus-gentium-1749', 'wolff-institutiones-1750', 'grotius-barbeyrac-1724', 'pufendorf-barbeyrac-1734'}
cat = load(R + '/catalogue.json'); where = {}
for c in cat['reuse']:
    if c['from'] == 'vattel-1773' and c['to'] in TAB:
        for r in load(R + '/' + c['path'])['rows']: where[r['id']] = c['to']
rw = []
for f in sorted(glob.glob(f'{S}/rec/out/*.json')):
    for s in load(f)['sections']:
        for w in s.get('rows_wrong', []):
            t = where.get(w['id'])
            if not t: print('  rows_wrong: not in the four tables', w); continue
            r = Row('vattel-1773', t, w['id'])
            if r.get('status') == 'rejected': continue
            a = {'verdict': 'wrong', 'reason': w['why'], 'date': DATE, 'statusWas': r.get('status')}
            if r.get('audit'): a['earlier'] = {k: r.get('audit')[k] for k in ('verdict', 'reason', 'date') if k in r.get('audit')}
            r.set('status', 'rejected'); r.set('audit', a); rw.append((w['id'], t))
print('recall readers, rows wrong:', rw)

if WRITE:
    for p, d in passes.items():
        with open(p, 'w', encoding='utf-8') as f: json.dump(d, f, ensure_ascii=False, indent=1); f.write('\n')
    for ed in corr:
        corr[ed]['rowEdits'] = sorted(edits[ed].values(), key=lambda e: e['id'])
        with open(f'{R}/editions/{ed}/corrections.json', 'w', encoding='utf-8') as f: json.dump(corr[ed], f, ensure_ascii=False, indent=1); f.write('\n')
    print('written')
