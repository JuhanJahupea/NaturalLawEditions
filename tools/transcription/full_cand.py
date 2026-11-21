# full_cand.py <out dir> [chars per batch]: batches for the full pass over Vattel 1773 (FULL_PASS_PROMPT.md): every section
# (Préface, Préliminaires, Livres I-IV) with Wolff's Jus gentium §§ it follows and Pufendorf pages (with Barbeyrac's notes).
# JG §§: those the section's Jus gentium rows cite, with their neighbours; for a section without such rows, the §§ between the
# nearest sections before and after that have them (at most 8). The text of each § (reading form) goes with it.
# Pufendorf: pages that Pufendorf rows of the section and the three sections on each side cite, pages of the loci Vattel cites
# for Pufendorf, and the 3 pages (text and notes) nearest the section by tf-idf over words of four letters or more.
# Each section also carries its rows in the JG, Institutiones and Pufendorf tables, so that readers can say what is covered.
import sys, os, re, json, math, collections, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
R = ROOT; out = sys.argv[1]; BUDGET = int(sys.argv[2]) if len(sys.argv) > 2 else 22000
units = json.load(open(R + '/editions/vattel-1773/text.json'))['units']
secs = [u for u in units if re.match(r'(Pref|Prelim|I|II|III|IV)\.\d+$', u['id'])]
order = {u['id']: i for i, u in enumerate(secs)}
T = {'wolff-jus-gentium-1749': 'JG', 'wolff-institutiones-1750': 'INST', 'pufendorf-barbeyrac-1734': 'PUF34'}
rows = collections.defaultdict(list)
for t in T:
    for r in json.load(open('%s/reuse/vattel-1773__%s.json' % (R, t)))['rows']:
        if r['status'] != 'rejected': r['_t'] = T[t]; rows[r['unit']].append(r)
# Jus gentium §§: reading pages, with the text of each §
JG = json.load(open(WORK + '/srcp/JG.json')); pages = JG['pages']; pidx = {p['id']: i for i, p in enumerate(pages)}
def jg_text(n, cap=3000):
    pid = JG['first_page_of'].get(str(n))
    if not pid: return None
    i = pidx[pid]; p = pages[i]; st = next(o for o, k in p['starts'] if k == n)
    txt = ''; j = i; a = st
    while j < len(pages) and len(txt) < cap:
        q = pages[j]; nxt = [o for o, k in q['starts'] if o > a and k != n] if j == i else [o for o, k in q['starts']]
        b = nxt[0] if nxt else len(q['text'])
        txt += (' ' if txt else '') + q['text'][a:b]
        if nxt: break
        j += 1; a = 0
    marg = [m for m in p['margin'] if re.match(r'§\.?\s*%d\b' % n, m)]
    return {'s': n, 'page': pid, 'margin': marg[0] if marg else '', 'text': txt[:cap]}
anch = {}
for u in secs:
    s = set()
    for r in rows[u['id']]:
        m = re.match(r'§ ?(\d+)', r.get('locus') or '')
        if r['_t'] == 'JG' and m: s.add(int(m.group(1)))
    anch[u['id']] = s
def jg_for(i):
    u = secs[i]; s = anch[u['id']]
    if s:
        lo, hi = min(s), max(s)
        want = sorted(set(s) | {x + d for x in s for d in (-1, 1)})
        if len(want) > 10: want = sorted(s)[:10]
        return want
    # nearest anchored sections before and after, in the same book
    book = u['id'].split('.')[0]
    prev = next((anch[secs[j]['id']] for j in range(i - 1, -1, -1) if anch[secs[j]['id']] and secs[j]['id'].split('.')[0] == book), None)
    nxt = next((anch[secs[j]['id']] for j in range(i + 1, len(secs)) if anch[secs[j]['id']] and secs[j]['id'].split('.')[0] == book), None)
    if prev and nxt:
        a, b = max(prev), min(nxt)
        if a > b: a, b = b, a
        rng = list(range(a, b + 1))
        return rng if len(rng) <= 8 else sorted(set(range(a, a + 4)) | set(range(b - 3, b + 1)))
    if prev: return list(range(max(prev), max(prev) + 4))
    if nxt: return list(range(max(1, min(nxt) - 3), min(nxt) + 1))
    return []
# Pufendorf pages: tf-idf over text and notes
PUF = json.load(open(WORK + '/corpus/PUF34.json'))['pages']
def toks(s):
    s = unicodedata.normalize('NFD', s.lower().replace('ſ', 's')); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return [w for w in re.findall(r'[a-z]{4,}', s)]
docs = {p['id']: collections.Counter(toks(p['text'] + ' ' + ' '.join(n['text'] for n in p['notes']))) for p in PUF if p['text']}
df = collections.Counter(w for c in docs.values() for w in c); N = len(docs)
idf = {w: math.log(N / (1 + n)) for w, n in df.items()}
def vec(c):
    v = {w: (1 + math.log(k)) * idf.get(w, math.log(N)) for w, k in c.items() if df.get(w, 0) < N * 0.3}
    norm = math.sqrt(sum(x * x for x in v.values())) or 1; return {w: x / norm for w, x in v.items()}
DV = {k: vec(c) for k, c in docs.items()}
inv = collections.defaultdict(list)
for k, v in DV.items():
    for w, x in v.items(): inv[w].append((k, x))
def nearest(text, k=3):
    q = vec(collections.Counter(toks(text))); sc = collections.Counter()
    for w, x in q.items():
        for d, y in inv.get(w, []): sc[d] += x * y
    return [d for d, _ in sc.most_common(k)]
locpage = {}
for p in PUF:
    for a, b, loc in p['spans']: locpage.setdefault(loc, p['id'])
ROM = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
def unrom(s):
    v = 0
    for i, c in enumerate(s):
        x = ROM[c]; v += -x if i + 1 < len(s) and ROM[s[i + 1]] > x else x
    return v
def roman(n):
    o = ''
    for v, s in ((100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')):
        while n >= v: o += s; n -= v
    return o
def cited_puf(u):
    """Pages of the loci Vattel cites for Pufendorf: 'PUFENDORF ... Liv. VIII, chap. VI, §. 14'."""
    out = set()
    for t in [u.get('text', '')] + [n['text'] for n in u.get('notes', [])]:
        for m in re.finditer(r'P[uU][fF]+[eE][nN]+[dD][oO][rR][fF][^.]{0,40}?[Ll]iv\.?\s*([IVXL]+)[^§]{0,25}?ch(?:ap)?\.?\s*([IVXL]+)[^§]{0,12}?§\.?\s*(\d+)', t):
            loc = 'Liv. %s ch. %s § %s' % (m.group(1), m.group(2), m.group(3))
            if loc in locpage: out.add(locpage[loc])
    return out
items = []
for i, u in enumerate(secs):
    near = secs[max(0, i - 3): i + 4]
    pp = set(r['page'] for s in near for r in rows[s['id']] if r['_t'] == 'PUF34' and r.get('page'))
    pp |= cited_puf(u)
    full = u.get('text', '') + ' ' + ' '.join(n['text'] for n in u.get('notes', []))
    pp |= set(nearest(full))
    js = [x for x in (jg_text(n) for n in jg_for(i)) if x]
    jpages = sorted(set(r['page'] for r in rows[u['id']] if r['_t'] == 'JG' and not re.match(r'§', r.get('locus') or '')))
    items.append({'unit': u['id'], 'text': u.get('text', ''), 'notes': [n['text'] for n in u.get('notes', [])], 'margin': u.get('margin', ''),
                  'rows': [{'id': r['id'], 'table': r['_t'], 'locus': r.get('locus'), 'label': r['label'], 'status': r['status'],
                            'passage': r['passage'], 'source_passage': r['source'][:300]} for r in rows[u['id']]],
                  'jus_gentium': js, 'jus_gentium_pages': jpages, 'pufendorf_pages': sorted(pp)})
os.makedirs(out + '/in', exist_ok=True); os.makedirs(out + '/out', exist_ok=True)
batches = []; cur = []; n = 0
for it in items:
    size = len(it['text']) + sum(map(len, it['notes']))
    if cur and n + size > BUDGET: batches.append(cur); cur = []; n = 0
    cur.append(it); n += size
if cur: batches.append(cur)
for b, bt in enumerate(batches): json.dump({'units': bt}, open('%s/in/f%03d.json' % (out, b), 'w'), ensure_ascii=False, indent=0)
print(len(items), 'sections', len(batches), 'batches', 'JG §§ per section', round(sum(len(i['jus_gentium']) for i in items) / len(items), 1),
      'Pufendorf pages per section', round(sum(len(i['pufendorf_pages']) for i in items) / len(items), 1),
      'without JG §§', sum(1 for i in items if not i['jus_gentium']))
