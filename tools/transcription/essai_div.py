# essai_div.py <out dir> [chars per batch]: divergence screen batches for Vattel's Essai (ESSAI_DIV_SCREEN_PROMPT.md).
# Sources: Wolff PPU1, TN1, LOG40 (<WORK>/srcp), Pufendorf DNG and Devoirs, Grotius (<WORK>/corpus; Barbeyrac's notes, Leibniz's
# Jugement and Barbeyrac's Réflexions with them), Burlamaqui 1747 (the edition). Candidates for a § of the Essai: the source
# sections its reuse rows use (any status but rejected), those of the §§ on each side, and for each French source the two
# sections nearest by TF-IDF. At most 14, the §'s own first. Each candidate carries its text (cut at 2500 characters)
# and its notes (cut at 1500). <out>/sections.json holds every source section by key "<code>|<locus>", for the readers' own
# searches and for essai_div_verify.py and essai_div_write.py.
import sys, os, re, json, math, collections, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
from corpus import unroman
R = ROOT; out = sys.argv[1]; BUDGET = int(sys.argv[2]) if len(sys.argv) > 2 else 80000
ED = 'vattel-essai-1747'
CODE = {'wolff-philosophia-practica-1738': 'PPU1', 'wolff-theologia-naturalis-1739': 'TN1', 'wolff-discursus-praeliminaris-1740': 'LOG40',
        'pufendorf-barbeyrac-1734': 'PUF34', 'pufendorf-devoirs-barbeyrac-1756': 'DEV56', 'grotius-barbeyrac-1724': 'GRO24',
        'burlamaqui-1747': 'BUR47'}
SEC = {}   # "<code>|<locus>" -> {code, locus, pages, text, notes, margin}
# Wolff: § by § from the reading pages (starts: [offset, §])
for code in ('PPU1', 'TN1', 'LOG40'):
    J = json.load(open('%s/srcp/%s.json' % (WORK, code))); pages = J['pages']
    for i, p in enumerate(pages):
        for k, (o, n) in enumerate(p['starts']):
            txt, pg, j, a = '', [p['id']], i, o
            while j < len(pages):
                q = pages[j]; nxt = [x for x, m in q['starts'] if x > a] if j == i else [x for x, m in q['starts']]
                b = nxt[0] if nxt else len(q['text']); txt += (' ' if txt else '') + q['text'][a:b]
                if nxt or j + 1 >= len(pages): break
                j += 1; a = 0; pg.append(pages[j]['id'])
            marg = next((m for m in p['margin'] if re.match(r'§\.?\s*%d\b' % n, m)), '')
            SEC.setdefault('%s|§ %d' % (code, n), {'code': code, 'locus': '§ %d' % n, 'pages': pg, 'text': txt.strip(), 'notes': '', 'margin': marg})
# Pufendorf, Devoirs, Grotius: main text by locus across pages; notes by the locus they belong to, with their author
for code in ('PUF34', 'DEV56', 'GRO24'):
    T = collections.OrderedDict(); P = collections.defaultdict(list); N = collections.defaultdict(list)
    for p in json.load(open('%s/corpus/%s.json' % (WORK, code)))['pages']:
        for a, b, loc in p['spans']:
            if '§' not in loc: continue
            T.setdefault(loc, []).append(p['text'][a:b].strip())
            if p['id'] not in P[loc]: P[loc].append(p['id'])
        for n in p['notes']:
            base = n['locus'].split(', n.')[0]
            if '§' in base: N[base].append('[%s, %s] %s' % (n['mark'], 'author' if n.get('by') == 'author' else 'Barbeyrac', n['text']))
    for loc, parts in T.items():
        SEC['%s|%s' % (code, loc)] = {'code': code, 'locus': loc, 'pages': P[loc], 'text': ' '.join(parts), 'notes': ' '.join(N.get(loc, [])), 'margin': ''}
# Burlamaqui: the edition's units, locus "Part. I ch. VI § 12"
BU = json.load(open(R + '/editions/burlamaqui-1747/text.json'))['units']
def rom(n):
    o = ''
    for v, s in ((10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')):
        while n >= v: o += s; n -= v
    return o
for u in BU:
    m = re.match(r'P(\d)\.(\d+)\.(\d+)$', u['id'])
    if not m or u.get('kind') == 'heading': continue
    loc = 'Part. %s ch. %s § %s' % (rom(int(m.group(1))), rom(int(m.group(2))), m.group(3))
    SEC['BUR47|' + loc] = {'code': 'BUR47', 'locus': loc, 'unit': u['id'], 'pages': ['BUR47.p%d' % p['scan'] for p in u.get('pages', [])],
                           'text': u['text'], 'notes': ' '.join('[%s] %s' % (n['mark'], n['text']) for n in u.get('notes', [])), 'margin': u.get('margin', '')}
# the Essai and its reuse rows
units = [u for u in json.load(open('%s/editions/%s/text.json' % (R, ED)))['units'] if u.get('kind') != 'heading']
ids = [u['id'] for u in units]
rows = collections.defaultdict(list)
for t, c in CODE.items():
    for r in json.load(open('%s/reuse/%s__%s.json' % (R, ED, t)))['rows']:
        if r['status'] == 'rejected': continue
        k = '%s|%s' % (c, r['locus'].split(', n.')[0])
        if k in SEC: rows[r['unit']].append((k, r['label']))
# TF-IDF over the French sources' sections
def fold(s):
    s = unicodedata.normalize('NFD', s.replace('ſ', 's').replace('&', ' et ')); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()
    return [w for w in re.findall(r'[a-z]{4,}', s.replace('y', 'i').replace('oi', 'ai'))]
FR = [k for k, v in SEC.items() if v['code'] in ('PUF34', 'DEV56', 'GRO24', 'BUR47') and len(v['text']) > 200]
F = {k: collections.Counter(fold(SEC[k]['text'])) for k in FR}
df = collections.Counter(); [df.update(set(f)) for f in F.values()]; NN = len(F)
def vec(c):
    v = {w: (1 + math.log(n)) * math.log(NN / (1 + df.get(w, 0))) for w, n in c.items() if df.get(w, 0) < NN * 0.25}
    z = math.sqrt(sum(x * x for x in v.values())) or 1; return {w: x / z for w, x in v.items()}
V = {k: vec(f) for k, f in F.items()}
def near(text, code, k=2):
    q = vec(collections.Counter(fold(text)))
    sc = [(sum(x * V[s].get(w, 0) for w, x in q.items()), s) for s in FR if SEC[s]['code'] == code]
    return [s for _, s in sorted(sc, reverse=True)[:k]]
cap = lambda t, n: t if len(t) <= n else t[:n] + ' [...]'
items = []
for i, u in enumerate(units):
    own = list(dict.fromkeys(k for k, _ in rows[u['id']]))
    side = list(dict.fromkeys(k for j in (i - 1, i + 1) if 0 <= j < len(units) for k, _ in rows[ids[j]] if k not in own))
    full = u['text'] + ' ' + ' '.join(n['text'] for n in u.get('notes', []))
    tf = [k for c in ('PUF34', 'DEV56', 'GRO24', 'BUR47') for k in near(full, c) if k not in own and k not in side]
    cand = (own + side + list(dict.fromkeys(tf)))[:max(14, len(own))]
    labs = collections.defaultdict(list)
    for k, l in rows[u['id']]: labs[k].append(l)
    items.append({'vattel_id': u['id'], 'vattel_margin': u.get('margin', ''), 'vattel_text': u['text'],
                  'vattel_notes': ' '.join('%s %s' % (n['mark'], n['text']) for n in u.get('notes', [])),
                  'candidates': [{'key': k, 'source': SEC[k]['code'], 'locus': SEC[k]['locus'], 'margin': SEC[k]['margin'],
                                  'text': cap(SEC[k]['text'], 2500), 'notes': cap(SEC[k]['notes'], 1500),
                                  'reuse': labs.get(k, []), 'why': 'own rows' if k in own else 'rows of a neighbouring §' if k in side else 'vocabulary'}
                                 for k in cand]})
os.makedirs(out + '/in', exist_ok=True); os.makedirs(out + '/out', exist_ok=True)
json.dump(SEC, open(out + '/sections.json', 'w'), ensure_ascii=False)
batches, cur, n = [], [], 0
for it in items:
    size = len(json.dumps(it, ensure_ascii=False))
    if cur and n + size > BUDGET: batches.append(cur); cur, n = [], 0
    cur.append(it); n += size
if cur: batches.append(cur)
for b, bt in enumerate(batches): json.dump(bt, open('%s/in/d%03d.json' % (out, b), 'w'), ensure_ascii=False)
print(len(items), '§§;', len(batches), 'batches;', sum(len(i['candidates']) for i in items), 'pairs;', len(SEC), 'source sections')
