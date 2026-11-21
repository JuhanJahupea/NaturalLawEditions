# fullpass_apply.py <check dir> <date> <vattel data.json> [--write]: the second reading after the full pass (fullpass_check.py,
# PRECISION_PROMPT.md) into the rows, wherever they live: rows of data.json through corrections.json rowEdits, rows of a pass in its
# pass file, added rows in passes/additions.json. Every read row carries `audit` {verdict, reason, date, statusWas, labelWas}.
# Flagged rows: wrong -> rejected, weak match -> possible, right stays. Sampled rows of the pass: right -> match, weak -> possible,
# wrong -> rejected. A label the reader would change is changed. Also writes audit/fullpass-second-reading-<date>.json.
import sys, os, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT; d, date, VD = sys.argv[1:4]; WRITE = '--write' in sys.argv; ED = 'vattel-1773'
LABELS = {'verbatim', 'close paraphrase', 'loose paraphrase', 'translation', 'shared argument', 'citation', 'open disagreement', 'commonplace'}
load = lambda p: json.load(open(p, encoding='utf-8'))
data = {r['id']: r for r in load(VD)['rows']}
corr = load(f'{R}/editions/{ED}/corrections.json'); edits = {e['id']: e for e in corr.get('rowEdits', [])}
add = load(f'{R}/editions/{ED}/passes/additions.json'); addby = {r['id']: r for r in add['rows']}
passes = {}
class Row:
    def __init__(self, table, rid):
        p = f'{R}/editions/{ED}/passes/{table}.json'
        if rid in addby: self.p = addby[rid]; return
        if os.path.exists(p):
            if p not in passes: passes[p] = load(p)
            pr = {r['id']: r for r in passes[p]['rows']}
            if rid in pr: self.p = pr[rid]; return
        base = data[rid]; self.p = None; self.e = edits.setdefault(rid, {'id': rid})
        self.base = {k: base.get(k) for k in ('label', 'status', 'audit', 'locus')}
    def get(self, k): return self.p.get(k) if self.p is not None else (self.e[k] if k in self.e else self.base.get(k))
    def set(self, k, v):
        if self.p is not None: self.p[k] = v
        else: self.e[k] = v
items = {x['key']: x for x in load(d + '/items.json')}
V = {int(it['key']): it for f in sorted(glob.glob(d + '/out/*.json')) for it in load(f)['items']}
st = collections.Counter(); labs = collections.Counter(); out = []
for k, v in sorted(V.items()):
    x = items[k]; r = Row(x['table'], x['id']); was = r.get('status')
    a = {'verdict': v['verdict'], 'reason': v['reason'], 'date': date}
    if x['why'] == 'flagged': a['flaggedBy'] = x['first']
    if not v.get('label_ok', True) and v.get('better_label') and v['better_label'].strip().lower() != r.get('label'):
        bl = v['better_label'].strip().lower(); assert bl in LABELS, bl
        a['labelWas'] = r.get('label'); r.set('label', bl); labs[(a['labelWas'], bl)] += 1
    if x['why'] == 'flagged': new = {'wrong': 'rejected', 'weak': 'possible' if was == 'match' else was, 'right': was}[v['verdict']]
    else: new = {'right': 'match', 'weak': 'possible', 'wrong': 'rejected'}[v['verdict']]
    if new != was: r.set('status', new); a['statusWas'] = was
    if r.get('audit'): a['earlier'] = {kk: r.get('audit')[kk] for kk in ('verdict', 'reason', 'date') if kk in r.get('audit')}
    r.set('audit', a); st[(x['why'], was, v['verdict'])] += 1
    out.append({'table': x['table'], 'id': x['id'], 'why': x['why'], 'statusWas': was, 'unit': x['unit'], 'locus': x['locus'], 'label': x['label'],
                'verdict': v['verdict'], 'labelOk': v.get('label_ok', True), 'betterLabel': v.get('better_label') or '', 'reason': v['reason']})
print(len(V), 'of', len(items)); [print(' ', k, n) for k, n in sorted(st.items())]
print('labels', sum(labs.values()), labs.most_common(5))
if WRITE:
    for p, P in passes.items(): json.dump(P, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(add, open(f'{R}/editions/{ED}/passes/additions.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    corr['rowEdits'] = sorted(edits.values(), key=lambda e: e['id'])
    with open(f'{R}/editions/{ED}/corrections.json', 'w', encoding='utf-8') as f: json.dump(corr, f, ensure_ascii=False, indent=1); f.write('\n')
    json.dump({'format': 'nle-audit/1', 'date': date, 'kind': 'second reading', 'edition': ED,
               'description': 'After the full pass (step F): the rows its readers judged wrong, and a random sample of the rows it added, read by a second reader (Claude Opus, tools/transcription/PRECISION_PROMPT.md).',
               'rows': out}, open(f'{R}/audit/fullpass-second-reading-{date}.json', 'w'), ensure_ascii=False, indent=1)
    print('written')
