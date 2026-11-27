# def41_cand.py <WORK>/def41/data.json <out dir> [units per batch] [cosine threshold]: judge batches for the reuse pass of Vattel's Défense
# du système leibnitien (1741) against its sources (step 4). Roques is not here: his letters exist only as Vattel's
# quotations (texts/roques-lettres-1737-1739/), which give the rows directly.
# Source segments (reading form: long s as s, line-end hyphens joined, line breaks as spaces):
#   EXA37.p<page>   Crousaz, Examen (1737), by printed page (Google OCR)
#   COM38.p<page>   Crousaz, Commentaire (1738), by printed page (Google OCR)
#   THEO.<id>       Leibniz, Théodicée, by section (Pref.n, Disc.n, T.n, Abr.n, Hob.n, King.n)
#   PSR34.<n>       Wolff, Psychologia rationalis, §§ 480-642, each § with its note ("[Nota]")
# Candidates per unit: (1) the loci Vattel cites (gold set, editions/vattel-defense-1741/provenance/citations.json);
# (2) segments sharing a run of 5+ folded words, rare in the source (a 5-word string in at most two segments), with at least
# three words of four letters or more; (3) for the French sources, the two nearest segments per source by TF-IDF cosine
# on folded words and word pairs, when the cosine reaches the threshold (default 0.12). Wolff's Latin is reached by (1), (2) and the readers'
# own search in the index of § summaries (<out>/PSR34_index.tsv). Units with no candidate are listed in
# <out>/no_candidates.json and not judged.
import sys, os, re, json, math, html, collections, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
DATA, OUT = sys.argv[1], sys.argv[2]; PER = int(sys.argv[3]) if len(sys.argv) > 3 else 8
COS = float(sys.argv[4]) if len(sys.argv) > 4 else 0.12
os.makedirs(OUT, exist_ok=True)
STOP = set('le la les de des du un une et en au aux que qui ne pas se sa son ses on il ils elle elles nous vous je est sont ce cette ces par pour dans sur plus ou mais si lui leur leurs tout tous toute comme dont etre avoir fait faire est et in ad cum non est quae quod ut sed per'.split())
def read(t):
    t = t.replace('ſ', 's'); t = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', t)
    return re.sub(r'\s+', ' ', t).strip()
def fold(t):
    t = unicodedata.normalize('NFD', re.sub(r'<[^>]+>|_', ' ', t).lower().replace('ſ', 's').replace('&', ' et ').replace('œ', 'oe').replace('æ', 'ae'))
    t = ''.join(c for c in t if not unicodedata.combining(c))
    t = t.replace('f', 's').replace('y', 'i').replace('oi', 'ai').replace('v', 'u').replace('j', 'i')
    return re.findall(r'[a-z]+', t)
# --- sources
SEG = {}                                         # id -> {src, locus, text}
for sig, tid, lab in (('EXA37', 'crousaz-examen-1737', 'Examen'), ('COM38', 'crousaz-commentaire-1738', 'Commentaire')):
    for p in json.load(open(os.path.join(ROOT, 'texts', tid, sig + '.json')))['pages']:
        if not p['page'] or len(p['text']) < 50: continue
        loc = '%s, %s p. %s' % (lab, 'Préface' if p['part'] in ('Préface', 'Avis du libraire', 'Avis au lecteur') else '', p['page'])
        SEG['%s.p%s' % (sig, p['page'])] = {'src': sig, 'locus': re.sub(r',\s+p', ', p', loc), 'part': p['part'], 'text': read(p['text'])}
for s in json.load(open(os.path.join(ROOT, 'texts', 'leibniz-theodicee-1734', 'THEO.json')))['sections']:
    SEG['THEO.' + s['id']] = {'src': 'THEO', 'locus': 'Théodicée, ' + s['label'], 'part': s['part'], 'text': re.sub(r'</?i>', '', s['text']).replace('\n', ' ')}
psr = ''.join(p['body'] + '\n' for p in json.load(open(os.path.join(ROOT, 'texts', 'wolff-psychologia-rationalis-1734', 'PSR34.json')))['pages'])
MARG = {}
for p in json.load(open(os.path.join(ROOT, 'texts', 'wolff-psychologia-rationalis-1734', 'PSR34.json')))['pages']:
    for m in p.get('margin', []):
        n = re.sub(r'\D', '', m.get('para', '')); MARG.setdefault(n, []).append(read(m.get('text', '')))
for m in re.finditer(r'<<§ (\d+)>>(.*?)(?=<<§ \d+>>|<<SECTIO|\Z)', psr, re.S):
    t = re.sub(r'<<NOTA>>', ' [Nota] ', m.group(2)); t = re.sub(r'<<[^>]*>>|</?i>', ' ', t)
    SEG['PSR34.%s' % m.group(1)] = {'src': 'PSR34', 'locus': 'Psychologia rationalis § %s' % m.group(1), 'part': '', 'text': read(t)}
with open(os.path.join(OUT, 'PSR34_index.tsv'), 'w') as f:
    for k, v in SEG.items():
        if v['src'] == 'PSR34': n = k.split('.')[1]; f.write('%s\t%s\n' % (k, ' / '.join(MARG.get(n, [])) or v['text'][:120]))
json.dump(SEG, open(os.path.join(OUT, 'segments.json'), 'w'), ensure_ascii=False)
# --- units
def plain(h):
    h = re.sub(r'<span class="pb" data-pg="\d+"> p\. ([^<]*) </span>', r'[p. \1]', h)
    h = h.replace('<i>', '_').replace('</i>', '_'); h = re.sub(r'<[^>]+>', '', h)
    return html.unescape(h)
U = json.load(open(DATA))['units']
items = [{'unit': u['id'], 'part': u['part'], 'chap': u['chap'], 'text': plain(u['html']),
          'notes': [{'mark': n['mark'], 'text': plain(n['html'])} for n in u['notes']]} for u in U if u['div'] != 'Tab']
# (1) cited loci
CIT = collections.defaultdict(set)
TH = {'Discours': 'Disc', 'Abrégé': 'Abr', 'Préface': 'Pref', 'King': 'King', 'Hobbes': 'Hob'}
for c in json.load(open(os.path.join(ROOT, 'editions', 'vattel-defense-1741', 'provenance', 'citations.json')))['citations']:
    w, loc = c['work'], c['locus'] or ''
    nums = [int(x) for x in re.findall(r'\d+', loc)]
    if len(nums) == 2 and nums[1] > nums[0] and nums[1] - nums[0] < 4: nums = list(range(nums[0], nums[1] + 1))
    if c['author'] == 'Crousaz' and nums:
        sig = 'EXA37' if w.startswith('Examen') else 'COM38' if w.startswith('Commentaire') else None
        if sig: CIT[c['unit']] |= {'%s.p%d' % (sig, n) for n in nums[:3] if '%s.p%d' % (sig, n) in SEG}
    elif c['author'] == 'Leibniz' and w.startswith(('Théodicée', 'Remarques sur le livre')) and nums:
        pre = next((v for k, v in TH.items() if k in w), 'T')
        if w.startswith('Remarques'): pre = 'King'
        CIT[c['unit']] |= {'THEO.%s.%d' % (pre, n) for n in nums[:3] if 'THEO.%s.%d' % (pre, n) in SEG}
    elif w == 'Psychologia rationalis' and nums:
        CIT[c['unit']] |= {'PSR34.%d' % n for n in nums[:2] if 'PSR34.%d' % n in SEG}
# (2) shared runs
G = collections.defaultdict(set); FW = {}
for k, v in SEG.items():
    ws = fold(v['text']); FW[k] = ws
    for i in range(len(ws) - 4): G[' '.join(ws[i:i + 5])].add(k)
def runs(ws):
    hits = collections.defaultdict(list)
    for i in range(len(ws) - 4):
        g = ' '.join(ws[i:i + 5]); segs = G.get(g)
        if segs and len(segs) <= 2 and sum(1 for w in ws[i:i + 5] if len(w) >= 4 and w not in STOP) >= 3:
            for s in segs: hits[s].append(i)
    out = {}
    for s, ii in hits.items():
        rr, start, prev = [], ii[0], ii[0]
        for i in ii[1:] + [None]:
            if i is not None and i == prev + 1: prev = i; continue
            rr.append(' '.join(ws[start:prev + 5]))
            if i is not None: start = prev = i
        out[s] = rr
    return out
# (3) TF-IDF over the French sources
def feats(ws):
    w = [x for x in ws if len(x) > 2 and x not in STOP]; return collections.Counter(w + [a + '_' + b for a, b in zip(w, w[1:])])
FR = [k for k, v in SEG.items() if v['src'] != 'PSR34']
F = {k: feats(FW[k]) for k in FR}
df = collections.Counter(); [df.update(set(f)) for f in F.values()]; N = len(F)
idf = {k: math.log(N / v) for k, v in df.items()}
def vec(c):
    v = {k: (1 + math.log(n)) * idf.get(k, math.log(N)) for k, n in c.items()}; z = math.sqrt(sum(x * x for x in v.values())) or 1
    return {k: x / z for k, x in v.items()}
V = {k: vec(f) for k, f in F.items()}
inv = collections.defaultdict(list)
for k, v in V.items():
    for t, x in v.items(): inv[t].append((k, x))
stats = collections.Counter()
for it in items:
    ws = fold(it['text'] + ' ' + ' '.join(n['text'] for n in it['notes']))
    cited = sorted(CIT.get(it['unit'], set()))
    sh = runs(ws)
    shared = sorted(sh, key=lambda s: -max(len(r.split()) for r in sh[s]))[:5]
    q = vec(feats(ws)); sc = collections.Counter()
    for t, x in q.items():
        for k, y in inv.get(t, ()): sc[k] += x * y
    near = []
    for src in ('EXA37', 'COM38', 'THEO'):
        best = [(k, s) for k, s in sc.most_common() if SEG[k]['src'] == src][:2]
        near += [k for k, s in best if s >= COS]
    cands = list(dict.fromkeys(cited + shared + near))
    it['candidates'] = cands; it['cited'] = cited
    it['shared'] = [{'id': s, 'words': r} for s in shared for r in sh[s][:3]]
    stats['cited'] += len(cited); stats['shared'] += len(shared); stats['near'] += len(near); stats['cands'] += len(cands)
    stats['no cand'] += not cands
json.dump([it['unit'] for it in items if not it['candidates']], open(os.path.join(OUT, 'no_candidates.json'), 'w'))
items = [it for it in items if it['candidates']]           # units with no candidate are not judged
batches = [items[i:i + PER] for i in range(0, len(items), PER)]
for b, its in enumerate(batches):
    ids = sorted({c for it in its for c in it['candidates']})
    json.dump({'segments': {k: SEG[k] for k in ids}, 'items': its},
              open(os.path.join(OUT, 'b%03d.json' % b), 'w'), ensure_ascii=False, indent=1)
words = [sum(len(SEG[k]['text'].split()) for k in {c for it in its for c in it['candidates']}) + sum(len(it['text'].split()) for it in its) for its in batches]
print(len(items), 'units;', len(batches), 'batches;', dict(stats), '; words per batch: mean %d, max %d' % (sum(words) / len(words), max(words)))
