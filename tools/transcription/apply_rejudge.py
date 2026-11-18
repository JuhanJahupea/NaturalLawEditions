"""Apply the re-judge of weak match tables (rej/) and the label check (lab/) to the editions.

Re-judge verdicts (right/weak/wrong) go in `audit` with date; weak match rows become `possible`, wrong rows `rejected`
(`audit.statusWas` keeps the old status); a label the judge would change is changed (`audit.labelWas`).
Label-check changes go in `labelCheck` {was, reason, date}. Rows of a later pass are edited in their pass file;
rows of data.json through corrections.json rowEdits (merged with the edits already there).

usage: apply_rejudge.py <scratch> <repo> <vattel data.json> <burlamaqui data.json> [--write]
"""
import json, os, sys, glob, collections

S, R, VD, BD = sys.argv[1:5]
WRITE = '--write' in sys.argv
DATE = '2026-11-18'
LABELS = {'verbatim', 'close paraphrase', 'loose paraphrase', 'translation', 'shared argument', 'citation',
          'open disagreement', 'commonplace'}

def load(p): return json.load(open(p, encoding='utf-8'))

def outs(d, pre):
    res = {}
    for f in sorted(glob.glob(f'{S}/{d}/out/{pre}*.json')):
        for it in load(f)['items']: res[it['key']] = it
    return res

rej_items = {x['key']: x for x in load(f'{S}/rej/items.json')}
lab_items = {x['key']: x for x in load(f'{S}/lab/items.json')}
rej = outs('rej', 'r'); lab = outs('lab', 'l')
# editor's corrections of a judge's verdict, by key
OVERRIDE = {147: {'verdict': 'right', 'label_ok': True, 'better_label': '',
                  'reason': "Vattel's note names Pufendorf V.XII.7, so the citation holds (corrected by the editor: the judge rated it wrong because "
                            "the paired source sentence, on arms in a capitulation, is not the one Vattel's examples follow)."}}
for k, v in OVERRIDE.items():
    if k in rej: rej[k] = dict(rej[k], **v)
print('re-judge', len(rej), 'of', len(rej_items), '| label check', len(lab), 'of', len(lab_items))

# where each row lives
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
    """A view on one row: a pass row edited in place, or a data.json row edited through rowEdits."""
    def __init__(self, ed, table, rid):
        self.ed, self.rid = ed, rid
        pr = pass_rows(ed, table)
        if pr is not None:
            self.p = pr[rid]; self.e = None
        else:
            base = data_ids[ed][rid]; self.p = None
            self.e = edits[ed].setdefault(rid, {'id': rid})
            self.base = {'label': base['label'], 'status': base['status'], 'audit': base.get('audit'), 'labelCheck': base.get('labelCheck')}
    def get(self, k):
        if self.p is not None: return self.p.get(k)
        return self.e[k] if k in self.e else self.base[k]
    def set(self, k, v):
        if self.p is not None: self.p[k] = v
        else: self.e[k] = v

stats = collections.Counter(); bytab = collections.defaultdict(collections.Counter); labch = collections.Counter()
rejlab = {}
for k, v in sorted(rej.items()):
    it = rej_items[k]; r = Row(it['edition'], it['table'], it['id'])
    assert r.get('status') == 'match', (k, r.get('status'))
    assert r.get('label') == it['label'], (k, r.get('label'), it['label'])
    verdict = v['verdict']; assert verdict in ('right', 'weak', 'wrong'), v
    old = r.get('audit') or {}
    a = {'verdict': verdict, 'reason': v['reason'], 'date': DATE}
    if old.get('labelWas'): a['labelWas'] = old['labelWas']
    if not v.get('label_ok', True) and v.get('better_label') and v['better_label'] != it['label']:
        bl = v['better_label'].strip().lower(); assert bl in LABELS, (k, bl)
        a.setdefault('labelWas', it['label'])
        r.set('label', bl); rejlab[k] = bl; labch[(it['label'], bl)] += 1
        if a['labelWas'] == bl: del a['labelWas']
    if verdict == 'weak': r.set('status', 'possible'); a['statusWas'] = 'match'
    if verdict == 'wrong': r.set('status', 'rejected'); a['statusWas'] = 'match'
    if old: a['earlier'] = {x: old[x] for x in ('verdict', 'reason', 'date') if x in old}
    r.set('audit', a)
    stats[verdict] += 1; bytab[it['table']][verdict] += 1

# label check
lstats = collections.Counter(); lch = collections.Counter(); conflicts = []
for k, v in sorted(lab.items()):
    it = lab_items[k]; r = Row(it['edition'], it['table'], it['id'])
    if not v.get('changed'): lstats['kept'] += 1; continue
    nl = v['label'].strip().lower(); assert nl in LABELS, (k, nl)
    cur = r.get('label')
    if cur != it['label']:
        conflicts.append((k, it['edition'], it['table'], it['id'], it['label'], cur, nl))
    if nl == cur: lstats['same as re-judge'] += 1; continue
    r.set('label', nl); r.set('labelCheck', {'was': it['label'], 'reason': v['reason'], 'date': DATE})
    lstats['changed'] += 1; lch[(it['label'], nl)] += 1

print('re-judge verdicts', dict(stats)); [print(' ', t, dict(c)) for t, c in bytab.items()]
print('re-judge label changes', sum(labch.values()), labch.most_common())
print('label check', dict(lstats), lch.most_common())
print('conflicts (label check vs re-judge)', conflicts)

if WRITE:
    for p, d in passes.items():
        with open(p, 'w', encoding='utf-8') as f: json.dump(d, f, ensure_ascii=False, indent=1); f.write('\n')
    for ed in corr:
        corr[ed]['rowEdits'] = sorted(edits[ed].values(), key=lambda e: e['id'])
        with open(f'{R}/editions/{ed}/corrections.json', 'w', encoding='utf-8') as f:
            json.dump(corr[ed], f, ensure_ascii=False, indent=1); f.write('\n')
    out = {'date': DATE, 'rejudge': [dict(rej_items[k], **{x: rej[k].get(x) for x in ('verdict', 'label_ok', 'better_label', 'reason')}) for k in sorted(rej)],
           'labelCheck': [dict(lab_items[k], **{x: lab[k].get(x) for x in ('label', 'changed', 'reason')}, labelBefore=lab_items[k]['label']) for k in sorted(lab)]}
    for x in out['rejudge'] + out['labelCheck']:
        for drop in ('context', 'passage', 'source_passage', 'source', 'family', 'word_overlap'): x.pop(drop, None)
    with open(f'{S}/rejudge_out.json', 'w', encoding='utf-8') as f: json.dump(out, f, ensure_ascii=False, indent=1)
    print('written')
