"""Match rows that an audit rated weak become possible (audit.statusWas = 'match'): the rule of the re-judge, applied to
the rows the first precision audit read. usage: demote_weak.py <repo> [--write]"""
import json, os, sys, glob, collections
R = sys.argv[1]; WRITE = '--write' in sys.argv
def load(p): return json.load(open(p, encoding='utf-8'))
passes, corr, n = {}, {}, collections.Counter()
for t in sorted(glob.glob(f'{R}/reuse/*__*.json')):
    ed, table = os.path.basename(t)[:-5].split('__')
    if not os.path.isdir(f'{R}/editions/{ed}'): continue
    for r in load(t)['rows']:
        a = r.get('audit') or {}
        if a.get('verdict') != 'weak' or r['status'] != 'match': continue
        a = dict(a, statusWas='match'); n[(ed, table)] += 1
        pp = f'{R}/editions/{ed}/passes/{table}.json'
        if os.path.exists(pp):
            if pp not in passes: passes[pp] = load(pp)
            row = next(x for x in passes[pp]['rows'] if x['id'] == r['id']); row['status'] = 'possible'; row['audit'] = a
        else:
            cp = f'{R}/editions/{ed}/corrections.json'
            if cp not in corr: corr[cp] = load(cp)
            e = next((x for x in corr[cp]['rowEdits'] if x['id'] == r['id']), None)
            if e is None: e = {'id': r['id']}; corr[cp]['rowEdits'].append(e)
            e['status'] = 'possible'; e['audit'] = a
print(sum(n.values()), dict(n))
if WRITE:
    for p, d in list(passes.items()) + list(corr.items()):
        if 'rowEdits' in d: d['rowEdits'].sort(key=lambda e: e['id'])
        with open(p, 'w', encoding='utf-8') as f: json.dump(d, f, ensure_ascii=False, indent=1); f.write('\n')
