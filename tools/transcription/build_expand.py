# build_expand.py <edition> <WORK> <judge dir> <candidates.json> <out candidates.json>: second pass.
# For every unit, pages not yet judged for it from three sources:
#  1. cited: the pages of a source locus the unit's text or notes cite ("GROTIUS ... Liv. II. Chap. III. §. 15");
#  2. sections: the two source §§ nearest the unit by tf-idf over whole §§ (a chapter summary page often wins the
#     page retrieval while the matching § lies pages further on);
#  3. neighbours (units with no match in the first pass only): pages ±1 around the unit's own candidates and around
#     pages matched by units within two places in the same division.
# Keeps hinted and cited pages first, then the best others by word overlap, at most 3 pages per unit.
import sys, os, json, glob, re, math, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
from lex import toks
from corpus import unroman, roman
B = WORK
R = ROOT
ed, work, jd, cf, out = sys.argv[1:6]  # [hints.json]
AUTHS = {'GRO24': r'GROT|Grot|[Dd]roit de la [Gg](?:uerre|\.)|[Jj]ure [Bb](?:elli|\.)',
         'PUF34': r'PUF+END|Puf+end|[Dd]roit de la [Nn]at|[Jj]us [Nn]at'}
AUTH = AUTHS[work]
units = [u for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units'] if u['kind'] != 'heading']
pages = json.load(open('%s/corpus/%s.json' % (B, work)))['pages']
P = {p['id']: p for p in pages}
cand = json.load(open(cf))['cand']
judged = collections.defaultdict(set); matched = collections.defaultdict(set)
for f in glob.glob(jd + '/in/b*.json'):
    for it in json.load(open(f))['items']: judged[it['unit']].update(it['candidates'])
for f in glob.glob(jd + '/out/b*.json'):
    for m in json.load(open(f)).get('matches', []):
        if float(m.get('confidence', 0)) >= 0.5 and m.get('label') != 'commonplace': matched[m['unit']].add(m['page_id'])
# source §§: text and pages
SEC = collections.OrderedDict(); SECP = collections.defaultdict(list)
for p in pages:
    for a, b, loc in p['spans']:
        if '§' not in loc: continue
        SEC[loc] = SEC.get(loc, '') + ' ' + p['text'][a:b]
        if p['id'] not in SECP[loc]: SECP[loc].append(p['id'])
    for n in p['notes']:
        base = n['locus'].split(', n.')[0]
        if base in SECP and p['id'] not in SECP[base]: SECP[base].append(p['id'])
keys = list(SEC); ST = [toks(SEC[k]) for k in keys]
df = collections.Counter(w for t in ST for w in set(t)); N = len(ST)
idf = {w: math.log(N / (1 + c)) + 1 for w, c in df.items()}
def vec(t):
    c = collections.Counter(t); v = {w: n * idf.get(w, 1.0) for w, n in c.items()}
    nr = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {w: x / nr for w, x in v.items()}
SV = [vec(t) for t in ST]
inv = collections.defaultdict(list)
for i, v in enumerate(SV):
    for w, x in v.items(): inv[w].append((i, x))
# citations: Liv./Lib. n, Chap./cap. n, §. n (or the reverse order, or the Discours préliminaire). Each reference
# belongs to the nearest author or work named before it in the same text; a note that names none belongs to the
# work when the unit's text names it.
LOC = re.compile(r'(?:Liv|Lib|L)\.?\s*([IVXL]+|\d+)[.,]?\s*(?:Chap|chap|cap|Cap|ch|Ch|C)\.?\s*([IVXL]+|\d+)[.,]?\s*(?:§\.?\s*([IVXLC]+|\d+))?')
LOC2 = re.compile(r'§\.?\s*([IVXLC]+|\d+)[.,]?\s*(?:Chap|chap|ch|Ch)\.?\s*([IVXL]+|\d+)[.,]?\s*(?:Liv|Lib)\.?\s*([IVXL]+|\d+)')
DISC = re.compile(r'Disc(?:ours)?\.?\s*pr[ée]l[a-z]*\.?\s*§\.?\s*([IVXL]+|\d+)')
OTHER = re.compile('|'.join(v for k, v in AUTHS.items() if k != work) + r'|Wolf|WOLF|Hist|Ann\.|Annal|troubles|mare|Devoirs|'
                   r'Tite|TITE|Cicer|CICER|De Officiis|Plut|PLUT|Tacit|TACIT|Polyb|POLYB|Thucyd|THUCYD|Selden|SELDEN|Bynk|BYNK|'
                   r'Valere|VALERE|Locke|LOCKE|Cumberl|CUMBERL|Hobbes|HOBBES|Leibni|LEIBNI|Senec|SENEC|Barbeyrac sur')
def num(s): return int(s) if s.isdigit() else unroman(s)
def cited(u):
    out = []
    names = re.search(AUTH, u.get('margin', '') + ' ' + u['text'])
    for s in [u['text']] + [n['text'] for n in u.get('notes', [])]:
        marks = sorted([(m.start(), True) for m in re.finditer(AUTH, s)] + [(m.start(), False) for m in OTHER.finditer(s)])
        def ours(pos):
            prev = [w for p_, w in marks if p_ < pos]
            return prev[-1] if prev else bool(names) and not marks
        for m in LOC.finditer(s):
            if not ours(m.start()): continue
            lv, ch = num(m.group(1)), num(m.group(2)); pa = num(m.group(3)) if m.group(3) else None
            if not lv or not ch: continue
            out += SECP.get('Liv. %s ch. %s' % (roman(lv), roman(ch)) + (' § %d' % pa if pa else ' § 1'), [])[:2]
        for m in LOC2.finditer(s):
            if not ours(m.start()): continue
            pa, ch, lv = num(m.group(1)), num(m.group(2)), num(m.group(3))
            out += SECP.get('Liv. %s ch. %s § %d' % (roman(lv), roman(ch), pa), [])[:2]
        for m in DISC.finditer(s):
            if ours(m.start()): out += SECP.get('Discours préliminaire § %d' % num(m.group(1)), [])[:2]
    return out
def near(pid, d):
    vol, s = pid.split('.p'); s = int(s)
    return ['%s.p%d' % (vol, s + k) for k in range(-d, d + 1)]
# hints: pages judges named as the true source of an item they could not match (optional file)
HINT = json.load(open(sys.argv[6])) if len(sys.argv) > 6 else {}
T_UN, T_M, KEEP = 0.30, 0.40, 3
res = {}; why = collections.Counter()
for i, u in enumerate(units):
    full = ' '.join([u.get('margin', ''), u['text']] + [n['text'] for n in u.get('notes', [])])
    seen = set(judged.get(u['id'], ()))
    sure = [p for p in dict.fromkeys(HINT.get(u['id'], []) + cited(u)) if p in P and p not in seen]
    pool = set()
    v = vec(toks(full)); sc = collections.Counter()
    for w, x in v.items():
        for j, y in inv.get(w, ()): sc[j] += x * y
    top = sc.most_common(1)
    if top and top[0][1] >= (T_M if matched.get(u['id']) else T_UN): pool.update(SECP[keys[top[0][0]]][:2])
    if not matched.get(u['id']):
        for j in (i - 1, i + 1):
            if 0 <= j < len(units) and units[j]['div'] == u['div'] and units[j]['id'] in matched:
                for p in matched[units[j]['id']]: pool.update(near(p, 1)[1:])
    pool = [p for p in pool if p in P and (P[p]['text'] or P[p]['notes']) and p not in seen and p not in sure]
    W = set(toks(full))
    def ov(p):
        pw = set(toks(P[p]['text'] + ' ' + ' '.join(n['text'] for n in P[p]['notes'])))
        return len(W & pw) / (len(W | pw) or 1)
    pick = sure[:KEEP] + sorted(pool, key=ov, reverse=True)[:max(0, KEEP - len(sure[:KEEP]))]
    if pick:
        res[u['id']] = pick
        why['hint/cited' if sure else 'matched' if matched.get(u['id']) else 'unmatched'] += 1
json.dump({'cand': res}, open(out, 'w'))
print(len(res), 'units for the second pass;', dict(why), ';', sum(len(v) for v in res.values()), 'pages')
