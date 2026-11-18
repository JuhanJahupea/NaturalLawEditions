# add_cand.py <work> <out dir> [units per batch]: weak or wrong rows of Vattel whose audit reason names the passage of Wolff
# or Grotius that Vattel follows; items whose named loci already have a row in the unit are left out. Batches by unit.
import sys, os, re, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
S, out = sys.argv[1:3]; per = int(sys.argv[3]) if len(sys.argv) > 3 else 14
TABLES = {'JG': 'wolff-jus-gentium-1749', 'INST': 'wolff-institutiones-1750', 'GRO24': 'grotius-barbeyrac-1724'}
ROM = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
def unroman(s):
    s = s.upper(); t = 0
    for i, c in enumerate(s):
        v = ROM.get(c, 0); t += -v if i + 1 < len(s) and ROM.get(s[i + 1], 0) > v else v
    return t
def num(x): return int(x) if x.isdigit() else unroman(x)
def nums(s):
    out = set()
    for a, b in re.findall(r'(\d+)\s*(?:[–-]\s*(\d+))?', s):
        a = int(a); b = int(b) if b else a
        if b - a <= 20: out |= set(range(a, b + 1))
    return out
def refs(reason):
    r = set()
    for m in re.finditer(r'(?:\bJG\b|Jus gentium|Jus Gentium|Wolff(?:\'s)?)\s*(?:Prol\.?\s*)?(§§?[\s\d–\-/,and]+)', reason):
        if 'Inst' not in reason[max(0, m.start() - 15):m.start()]: r |= {('JG', n) for n in nums(m.group(1))}
    for m in re.finditer(r'(?:Inst\.?|Institutiones)\s*(§§?[\s\d–\-/,and]+)', reason): r |= {('INST', n) for n in nums(m.group(1))}
    for m in re.finditer(r'Grotius[^.\d]{0,25}?\b([IVX]{1,4})[.\s]+([ivxlcIVXLC]+|\d+)[.\s]+(\d+)', reason):
        r.add(('GRO24', (unroman(m.group(1)), num(m.group(2)), int(m.group(3)))))
    return r
def row_ref(table, locus):
    if table in ('wolff-jus-gentium-1749', 'wolff-institutiones-1750'):
        m = re.match(r'§\s*(\d+)', locus or ''); return int(m.group(1)) if m else None
    m = re.match(r'Liv\. ([IVX]+) ch\. ([IVXLC]+) § (\d+)', locus or '')
    return (unroman(m.group(1)), unroman(m.group(2)), int(m.group(3))) if m else None
cat = json.load(open(R + '/catalogue.json'))
rows = collections.defaultdict(list)
for c in cat['reuse']:
    if c['from'] != 'vattel-1773': continue
    for r in json.load(open(R + '/' + c['path']))['rows']:
        r['_to'] = c['to']; rows[r['unit']].append(r)
have = collections.defaultdict(set)
for u, rs in rows.items():
    for r in rs:
        if r['status'] == 'rejected': continue
        for k, t in TABLES.items():
            if r['_to'] == t:
                x = row_ref(t, r.get('locus')); 
                if x is not None: have[u].add((k, x))
J = json.load(open(R + '/audit/rejudge-2026-11-18.json'))['rejudge']; P = json.load(open(R + '/audit/precision-2026-11-17.json'))['rows']
W = re.compile(r'Wolff|Jus gentium|\bJG\b|Institutiones|\bInst\b|Grotius')
src = [dict(x, audit='2026-11-18') for x in J if x['verdict'] in ('weak', 'wrong')] + \
      [dict(x, audit='2026-11-17') for x in P if x['edition'] == 'vattel-1773' and x['verdict'] in ('weak', 'wrong')]
U = {u['id']: u for u in json.load(open(R + '/editions/vattel-1773/text.json'))['units']}
items = []; stat = collections.Counter()
for x in src:
    if not W.search(x['reason']): stat['names neither'] += 1; continue
    rf = refs(x['reason']); miss = {r for r in rf if r not in have[x['unit']]}
    if rf and not miss: stat['all named loci covered'] += 1; continue
    r = next(r for r in rows[x['unit']] if r['id'] == x['id'])
    stat['candidate' if rf else 'candidate, no locus parsed'] += 1
    items.append({'unit': x['unit'], 'row': x['id'], 'table': x['table'], 'label': r['label'], 'passage': r['passage'], 'source_passage': r['source'],
                  'audit_reason': x['reason'], 'named_not_in_tables': sorted('%s %s' % (k, '.'.join(map(str, v)) if isinstance(v, tuple) else v) for k, v in miss)})
print(dict(stat), len(items), 'items in', len({i['unit'] for i in items}), 'units')
by = collections.defaultdict(list)
for it in items: by[it['unit']].append(it)
order = [u['id'] for u in json.load(open(R + '/editions/vattel-1773/text.json'))['units'] if u['id'] in by]
os.makedirs(out + '/in', exist_ok=True); os.makedirs(out + '/out', exist_ok=True)
batches = [order[i:i + per] for i in range(0, len(order), per)]
for b, us in enumerate(batches):
    units = []
    for u in us:
        un = U[u]
        units.append({'unit': u, 'text': un['text'], 'notes': [n['text'] for n in un.get('notes', [])], 'margin': un.get('margin', ''),
                      'weak_rows': by[u],
                      'rows_in_tables': [{'id': r['id'], 'table': r['_to'], 'locus': r.get('locus'), 'label': r['label'], 'status': r['status'],
                                          'passage': r['passage'][:240]} for r in rows[u] if r['_to'] in TABLES.values() and r['status'] != 'rejected']})
    json.dump({'units': units}, open('%s/in/a%03d.json' % (out, b), 'w'), ensure_ascii=False, indent=0)
print(len(batches), 'batches')
