# recall_cand.py <out dir> [n] [seed]: a random sample of Vattel's sections (Préliminaires and Livres I-IV, by §) for the
# recall check (RECALL_PROMPT.md): each with its text, notes, margin, every row it has (not rejected), and the pages of Wolff
# (JG, INST), Grotius (GRO24) and Pufendorf (PUF34) that rows of the sections around it cite. Three sections per batch.
import sys, os, re, json, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
out = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 24; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 20261118
T = {'wolff-jus-gentium-1749': 'JG', 'wolff-institutiones-1750': 'INST', 'grotius-barbeyrac-1724': 'GRO24', 'pufendorf-barbeyrac-1734': 'PUF34'}
units = json.load(open(R + '/editions/vattel-1773/text.json'))['units']
secs = [u for u in units if re.match(r'(Prelim|I|II|III|IV)\.\d+$', u['id'])]
order = {u['id']: i for i, u in enumerate(secs)}
cat = json.load(open(R + '/catalogue.json')); rows = collections.defaultdict(list)
for c in cat['reuse']:
    if c['from'] != 'vattel-1773': continue
    for r in json.load(open(R + '/' + c['path']))['rows']:
        if r['status'] != 'rejected': r['_to'] = c['to']; rows[r['unit']].append(r)
random.seed(seed); pick = sorted(random.sample(secs, n), key=lambda u: order[u['id']])
os.makedirs(out + '/in', exist_ok=True); os.makedirs(out + '/out', exist_ok=True)
items = []
for u in pick:
    i = order[u['id']]; near = [s['id'] for s in secs[max(0, i - 4): i + 5]]
    pages = collections.defaultdict(set)
    for v in near:
        for r in rows[v]:
            if r['_to'] in T and r.get('page'): pages[T[r['_to']]].add(r['page'])
    items.append({'unit': u['id'], 'text': u['text'], 'notes': [x['text'] for x in u.get('notes', [])], 'margin': u.get('margin', ''),
                  'rows': [{'id': r['id'], 'table': r['_to'], 'locus': r.get('locus'), 'label': r['label'], 'status': r['status'],
                            'passage': r['passage'], 'source_passage': r['source'][:300]} for r in rows[u['id']]],
                  'pages_cited_nearby': {k: sorted(v) for k, v in pages.items()}})
for b in range(0, len(items), 3):
    json.dump({'units': items[b:b + 3]}, open('%s/in/c%03d.json' % (out, b // 3), 'w'), ensure_ascii=False, indent=0)
json.dump([it['unit'] for it in items], open(out + '/sample.json', 'w'))
print([it['unit'] for it in items], sum(len(it['text']) + sum(map(len, it['notes'])) for it in items) // n, 'chars per section')
