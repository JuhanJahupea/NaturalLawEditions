# gloss_cand.py <out dir>: candidate foreign-language stretches (Latin, Greek, English) in the units of the three editions, for the
# gloss readers (GLOSS_PROMPT.md). A character-trigram model of Latin (Wolff's JG, INST, PPU1, TN1, LOG40 transcriptions), French (the
# editions' own text) and English (the English layers) scores each word with its neighbours; runs of three or more words where Latin
# or English beats French are candidates, and so is any Greek letter. Batches hold the units with candidates, about 40 stretches each.
import sys, os, re, json, math, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
R = ROOT
B = WORK
out = sys.argv[1]; os.makedirs(out + '/in', exist_ok=True)
EDS = ['vattel-1773', 'burlamaqui-1747', 'vattel-essai-1747']
norm = lambda s: re.sub(r'\s+', ' ', s.lower().replace('ſ', 's').replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i').replace('v', 'u'))
def model(texts):
    c = collections.Counter(); 
    for t in texts:
        t = ' ' + norm(t) + ' '
        for i in range(len(t) - 2): c[t[i:i + 3]] += 1
    tot = sum(c.values()); V = 30000
    return lambda g: math.log((c[g] + 0.5) / (tot + 0.5 * V))
lat = []
for k in ('JG', 'INST', 'PPU1', 'TN1', 'LOG40'): lat += [p['text'] for p in json.load(open('%s/srcp/%s.json' % (B, k)))['pages']]
fr = []; en = []
for ed in EDS:
    fr += [u.get('text', '') for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units']]
    L = json.load(open('%s/editions/%s/layers/english.json' % (R, ed)))
    en += [' '.join(v.get('sents', [])) for v in L['units'].values()]
M = {'la': model(lat), 'fr': model(fr), 'en': model(en)}
GR = re.compile(r'[Ͱ-Ͽἀ-῿]')
def stretches(t):
    words = [(m.start(), m.end()) for m in re.finditer(r'\S+', t)]
    sc = []
    for a, b in words:
        w = ' ' + norm(t[a:b]) + ' '
        sc.append({k: sum(f(w[i:i + 3]) for i in range(len(w) - 2)) for k, f in M.items()})
    lab = []
    for i in range(len(words)):
        win = sc[max(0, i - 2):i + 3]
        tot = {k: sum(x[k] for x in win) for k in M}
        best = max(tot, key=tot.get)
        lab.append(best if best != 'fr' and tot[best] - tot['fr'] > 2.0 * len(win) else 'fr')
    out = []; i = 0
    while i < len(words):
        if lab[i] == 'fr': i += 1; continue
        j = i
        while j + 1 < len(words) and lab[j + 1] == lab[i]: j += 1
        if j - i + 1 >= 3: out.append([words[i][0], words[j][1], lab[i]])
        i = j + 1
    for m in GR.finditer(t):
        if not any(a <= m.start() < b for a, b, _ in out):
            a = t.rfind(' ', 0, max(0, m.start() - 40)) + 1; b = t.find(' ', m.start() + 40); b = len(t) if b < 0 else b
            out.append([a, b, 'grc'])
    return sorted(out)
batches = []; cur = []; n = 0; stats = collections.Counter()
for ed in EDS:
    for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units']:
        parts = [('t', u.get('text', ''))] + [('n%d' % i, x['text']) for i, x in enumerate(u.get('notes', []))]
        cands = []
        for p, t in parts:
            for a, b, lg in stretches(t):
                cands.append({'part': p, 'lang_guess': lg, 'text': t[a:b], 'context': t[max(0, a - 150):b + 150]})
                stats[(ed, lg)] += 1
        if not cands: continue
        cur.append({'edition': ed, 'unit': u['id'], 'text': u.get('text', ''), 'notes': [{'mark': x.get('mark', ''), 'text': x['text']} for x in u.get('notes', [])], 'candidates': cands})
        n += len(cands)
        if n >= 40: batches.append(cur); cur = []; n = 0
if cur: batches.append(cur)
for i, b in enumerate(batches): json.dump({'units': b}, open('%s/in/g%03d.json' % (out, i), 'w'), ensure_ascii=False, indent=1)
print(len(batches), 'batches', sum(len(b) for b in batches), 'units', dict(stats))
