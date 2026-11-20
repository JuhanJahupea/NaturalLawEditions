# essai_apply_verify.py <dir> <date> [--write]: the second reading of the Essai's match rows (VERIFY_PROMPT_ESSAI.md) into the
# pass files: audit {verdict, reason, date, labelWas, statusWas}; weak rows become possible, wrong rows rejected; a label the
# reader would change is changed.
import os, sys, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
d, date = sys.argv[1:3]; WRITE = '--write' in sys.argv
R = ROOT; ED = 'vattel-essai-1747'
items = {x['key']: x for x in json.load(open(d + '/items.json'))}
V = {}
for f in glob.glob(d + '/out/*.json'):
    for it in json.load(open(f))['items']: V[it['key']] = it
LABELS = {'verbatim', 'close paraphrase', 'loose paraphrase', 'translation', 'shared argument', 'citation', 'open disagreement', 'commonplace'}
passes = {}; st = collections.Counter(); bytab = collections.defaultdict(collections.Counter); labs = collections.Counter()
for k, v in sorted(V.items()):
    x = items[k]; p = '%s/editions/%s/passes/%s.json' % (R, ED, x['table'])
    if p not in passes: passes[p] = json.load(open(p))
    r = next(r for r in passes[p]['rows'] if r['id'] == x['id'])
    assert r['status'] == 'match'
    a = {'verdict': v['verdict'], 'reason': v['reason'], 'date': date}
    if not v.get('label_ok', True) and v.get('better_label') and v['better_label'].strip().lower() != r['label']:
        bl = v['better_label'].strip().lower(); assert bl in LABELS, bl
        a['labelWas'] = r['label']; r['label'] = bl; labs[(a['labelWas'], bl)] += 1
    if v['verdict'] == 'weak': r['status'] = 'possible'; a['statusWas'] = 'match'
    if v['verdict'] == 'wrong': r['status'] = 'rejected'; a['statusWas'] = 'match'
    r['audit'] = a; st[v['verdict']] += 1; bytab[x['table']][v['verdict']] += 1
print(len(V), 'of', len(items), dict(st)); [print(' ', t, dict(c)) for t, c in bytab.items()]
print('labels', sum(labs.values()), labs.most_common())
if WRITE:
    for p, P in passes.items(): json.dump(P, open(p, 'w'), ensure_ascii=False, indent=1)
    print('written')
