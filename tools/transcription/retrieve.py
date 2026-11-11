# retrieve.py <edition> <WORK> <old table> <out>: candidate source pages for every unit of an edition.
# Scores: skip-bigrams on stemmed French (best window pair on the page) and tf-idf cosine (unit vs page),
# z-scored per unit over the pages of the work. Candidates: top 2 by (zSK+zTF)/2, top 1 by zSK, and the pages of the
# old table's rows for the unit (so the new pass reads at least what the OCR pass read).
import os, sys, json, re, math, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
from lex import toks, skipbigrams, zscores
B = WORK
R = ROOT
ed, work, old, out = sys.argv[1:5]

def sents(s):
    return [x for x in re.split(r'(?<=[.;:?!])\s+', s) if x.strip()]
def windows(s, step):
    ss = sents(s)
    return [' '.join(ss[i:i + 2]) for i in range(0, max(1, len(ss) - 1), step)] if ss else []

units = [u for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units'] if u['kind'] != 'heading']
pages = [p for p in json.load(open('%s/corpus/%s.json' % (B, work)))['pages'] if p['text'] or p['notes']]
pids = [p['id'] for p in pages]

# source windows, inverted index of skip-bigrams
SW = []  # (page index, sb set)
for i, p in enumerate(pages):
    parts = [p['text']] + [n['text'] for n in p['notes']] + [m['text'] for m in p['margin']]
    for part in parts:
        for w in windows(part, 2):
            sb = skipbigrams(toks(w))
            if len(sb) >= 6: SW.append((i, sb))
inv = collections.defaultdict(list)
for k, (i, sb) in enumerate(SW):
    for g in sb: inv[g].append(k)
maxdf = 0.02 * len(SW)
# page tf-idf
PT = [toks(p['text'] + ' ' + ' '.join(n['text'] for n in p['notes']) + ' ' + ' '.join(m['text'] for m in p['margin'])) for p in pages]
df = collections.Counter(w for t in PT for w in set(t)); N = len(PT)
idf = {w: math.log(N / (1 + c)) + 1 for w, c in df.items()}
def vec(t):
    c = collections.Counter(t); v = {w: n * idf.get(w, 1.0) for w, n in c.items()}
    nr = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {w: x / nr for w, x in v.items()}
PV = [vec(t) for t in PT]
pinv = collections.defaultdict(list)
for i, v in enumerate(PV):
    for w, x in v.items(): pinv[w].append((i, x))

oldrows = collections.defaultdict(list)
for r in json.load(open(old))['rows']: oldrows[r['unit']].append(r['page'])

cand = {}; best = {}
for u in units:
    full = ' '.join([u.get('margin', ''), u['text']] + [n['text'] for n in u.get('notes', [])])
    sk = [0.0] * N
    for w in windows(full, 1):
        sb = skipbigrams(toks(w))
        if len(sb) < 6: continue
        hit = collections.Counter()
        for g in sb:
            l = inv.get(g)
            if l and len(l) <= maxdf:
                for k in l: hit[k] += 1
        for k, c in hit.items():
            s = c / min(len(sb), len(SW[k][1])); i = SW[k][0]
            if s > sk[i]: sk[i] = s
    v = vec(toks(full)); tf = [0.0] * N
    for w, x in v.items():
        for i, y in pinv.get(w, ()): tf[i] += x * y
    zs, zt = zscores(sk), zscores(tf); zc = [(a + b) / 2 for a, b in zip(zs, zt)]
    order = sorted(range(N), key=lambda i: -zc[i])
    sel = order[:2]
    j = max(range(N), key=lambda i: zs[i])
    if j not in sel: sel.append(j)
    c = [pids[i] for i in sel]
    for p in oldrows.get(u['id'], []):
        if p in pids and p not in c: c.append(p)
    cand[u['id']] = c
    best[u['id']] = [[pids[i], round(zc[i], 2), round(sk[i], 3)] for i in order[:5]]
json.dump({'cand': cand, 'best': best}, open(out, 'w'), ensure_ascii=False)
print(ed, work, len(units), 'units;', len(pages), 'pages;', len(SW), 'windows; mean cands', round(sum(len(c) for c in cand.values()) / len(cand), 2),
      '; old pages missing from corpus', sum(1 for u in oldrows for p in oldrows[u] if p not in pids))
