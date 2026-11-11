# shared_scan.py <edition> <work> <out>: every unit against every source part; runs of shared words.
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
import shared
B = WORK
R = ROOT
ed, work, out = sys.argv[1:4]
units = [u for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units'] if u['kind'] != 'heading']
pages = json.load(open('%s/corpus/%s.json' % (B, work)))['pages']
parts = []
for p in pages:
    if not p.get('text') and not p['notes']: continue
    k = 0
    for a, b, loc in p['spans']: parts.append(((p['id'], k), p['text'][a:b])); k += 1
    for m in p['margin']: parts.append(((p['id'], k), m['text'])); k += 1
    for n in p['notes']: parts.append(((p['id'], k), n['text'])); k += 1
idx, T = shared.index(parts)
EF = collections.Counter()
for u in units:
    full = ' '.join([u.get('margin', '')] + [u['text']] + [n['text'] for n in u.get('notes', [])])
    a = [w for w, _ in shared.toks(full)]
    for g in set(tuple(a[i:i + shared.N]) for i in range(len(a) - shared.N + 1)): EF[g] += 1
def rare(a, i, L):
    return any(len(idx.get(tuple(a[x:x + shared.N]), ())) <= 2 and EF[tuple(a[x:x + shared.N])] <= 2 for x in range(i, i + L - shared.N + 1))
res = {}
for u in units:
    full = ' '.join([u.get('margin', '')] + [u['text']] + [n['text'] for n in u.get('notes', [])])
    a = [w for w, _ in shared.toks(full)]
    rs = [r for r in shared.runs(a, idx, T) if rare(a, r[0], r[1])]
    if rs: res[u['id']] = [{'page': key[0], 'k': key[1], 'n': L, 'words': ' '.join(a[i:i + L])} for i, L, key, j in rs]
json.dump(res, open(out, 'w'), ensure_ascii=False)
L = collections.Counter(min(r['n'], 12) for v in res.values() for r in v)
print(ed, 'units with runs', len(res), 'runs', sum(map(len, res.values())), 'by length', sorted(L.items()))
