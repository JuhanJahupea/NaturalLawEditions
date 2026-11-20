# essai_cand.py <work> <out dir> [sections per batch]: batches for the Essai reuse readers (ESSAI_REUSE_PROMPT.md).
# Each section with its text and notes, and per French source (Pufendorf DNG and Devoirs in Barbeyrac's translation,
# Grotius-Barbeyrac, Burlamaqui 1747) the 8 pages (units for Burlamaqui) nearest by TF-IDF cosine on folded words and word
# pairs. Wolff's Philosophia practica universalis is Latin: the readers search it themselves, with its index of marginal
# summaries.
import sys, os, re, json, math, collections, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
S, out = sys.argv[1], sys.argv[2]; per = int(sys.argv[3]) if len(sys.argv) > 3 else 4
R = ROOT
STOP = set('le la les de des du un une et en a au aux que qui ne pas se sa son ses on il ils elle elles nous vous je est sont ce cette ces par pour dans sur plus ou mais si y l d qu n s c m t j lui leur leurs tout tous toute meme comme dont est etre avoir fait faire'.split())
def fold(s):
    s = unicodedata.normalize('NFD', s.replace('ſ', 's').replace('&', ' et ')); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()
    s = s.replace('y', 'i').replace('oi', 'ai')
    return [w for w in re.findall(r'[a-z]+', s) if len(w) > 2 and w not in STOP]
def feats(t):
    w = fold(t); return collections.Counter(w + [a + '_' + b for a, b in zip(w, w[1:])])
docs = []   # (source, id, text)
for k in ('PUF34', 'DEV56', 'GRO24'):
    for p in json.load(open('%s/corpus/%s.json' % (S, k)))['pages']:
        t = p['text'] + ' ' + ' '.join(n['text'] for n in p['notes'])
        if len(t) > 200: docs.append((k, p['id'], t))
for u in json.load(open(R + '/editions/burlamaqui-1747/text.json'))['units']:
    t = u['text'] + ' ' + ' '.join(n['text'] for n in u.get('notes', []))
    if len(t) > 100: docs.append(('BUR47', u['id'], t))
F = [feats(t) for _, _, t in docs]
df = collections.Counter(); [df.update(set(f)) for f in F]; N = len(F)
idf = {k: math.log(N / v) for k, v in df.items()}
def vec(c):
    v = {k: (1 + math.log(n)) * idf.get(k, math.log(N)) for k, n in c.items()}; z = math.sqrt(sum(x * x for x in v.values())) or 1
    return {k: x / z for k, x in v.items()}
V = [vec(f) for f in F]
units = [u for u in json.load(open(R + '/editions/vattel-essai-1747/text.json'))['units'] if u['kind'] == 'section']
os.makedirs(out + '/in', exist_ok=True); os.makedirs(out + '/out', exist_ok=True)
items = []
for u in units:
    q = vec(feats(u['text'] + ' ' + ' '.join(n['text'] for n in u.get('notes', []))))
    sc = collections.defaultdict(list)
    for (k, pid, _), v in zip(docs, V):
        s = sum(x * v.get(t, 0) for t, x in q.items())
        sc[k].append((round(s, 3), pid))
    cand = {k: [pid for s, pid in sorted(v, reverse=True)[:8]] for k, v in sc.items()}
    items.append({'unit': u['id'], 'text': u['text'], 'notes': [{'mark': n['mark'], 'text': n['text']} for n in u.get('notes', [])], 'candidates': cand})
for b in range(0, len(items), per):
    json.dump({'units': items[b:b + per]}, open('%s/in/e%03d.json' % (out, b // per), 'w'), ensure_ascii=False, indent=0)
print(len(items), 'sections', (len(items) + per - 1) // per, 'batches')
print({it['unit']: it['candidates']['DEV56'][:3] for it in items[28:33]})
