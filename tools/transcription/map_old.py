# map_old.py <old table> <work> <out>: old rows whose page id is not in the corpus (the Devoirs vol. II OCR was cut in chunks,
# DEV56T2.c105) get the corpus page that shares most 8-letter sequences with the row's source passage; page0 keeps the old id.
import os, sys, json, re, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK
B = WORK
old, work, out = sys.argv[1:4]
T = json.load(open(old)); P = json.load(open('%s/corpus/%s.json' % (B, work)))['pages']
def fold(s):
    o = []
    for ch in s.lower():
        c = unicodedata.normalize('NFD', ch)[0]
        if c in 'ſf': c = 's'
        if c in 'uv': c = 'u'
        if 'a' <= c <= 'z': o.append(c)
    return ''.join(o)
def sh(s): s = fold(s); return {s[i:i + 8] for i in range(len(s) - 7)}
ids = {p['id'] for p in P}
PS = {p['id']: sh(p['text'] + ' ' + ' '.join(n['text'] for n in p['notes']) + ' ' + ' '.join(m['text'] for m in p['margin'])) for p in P}
n = 0; weak = []
for r in T['rows']:
    if r['page'] in ids: continue
    q = sh(r['source'])
    if not q: continue
    best = max(PS, key=lambda k: len(q & PS[k]))
    share = len(q & PS[best]) / len(q)
    r['page0'] = r['page']; r['page'] = best; n += 1
    if share < 0.4: weak.append((r['id'], r['page0'], best, round(share, 2)))
json.dump(T, open(out, 'w'), ensure_ascii=False)
print(n, 'rows mapped;', len(weak), 'under 0.4:', weak[:10])
