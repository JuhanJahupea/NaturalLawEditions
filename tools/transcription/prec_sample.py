# prec_sample.py <dir> [seed]: a random sample of reuse rows for the precision audit (PRECISION_PROMPT.md): per edition 160
# rows at status match and 40 at status possible, commonplaces left out; batches of 25 in <dir>/in, the sample in <dir>/sample.json.
import sys, os, json, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
d = sys.argv[1]; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20261117
cat = json.load(open(R + '/catalogue.json')); TX = {t['id']: t for t in cat['texts']}
for e in cat['editions']: TX.setdefault(e['id'], {'author': e['author'], 'title': e['title'], 'date': e['date']})
random.seed(seed); sample = []; pop = {}
for ed in ('vattel-1773', 'burlamaqui-1747'):
    U = {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units']}
    rows = []
    for c in cat['reuse']:
        if c['from'] != ed: continue
        for r in json.load(open(R + '/' + c['path']))['rows']: r['_to'] = c['to']; rows.append(r)
    M = [r for r in rows if r['status'] == 'match' and r['label'] != 'commonplace']
    P = [r for r in rows if r['status'] == 'possible' and r['label'] != 'commonplace']
    pop[ed] = {'match': len(M), 'possible': len(P), 'match_by_table': dict(collections.Counter(r['_to'] for r in M))}
    for kind, Rs, n in (('match', M, 160), ('possible', P, 40)):
        for r in random.sample(Rs, n):
            u = U[r['unit']]; part = r['at'][0][0] if r.get('at') else 't'
            src = u['text'] if part == 't' else (u.get('margin', '') if part == 'm' else u['notes'][int(part[1:])]['text'])
            a, b = (r['at'][0][1], r['at'][0][2]) if r.get('at') else (max(0, src.find(r['passage'][:40])), 0)
            if not b: b = a + len(r['passage'])
            t = TX[r['_to']]
            sample.append({'key': len(sample), 'edition': ed, 'stratum': kind, 'table': r['_to'], 'id': r['id'], 'unit': r['unit'],
                           'source': '%s, %s (%s)' % (t['author'], t['title'], t.get('date', '')), 'family': r['family'], 'locus': r.get('locus', ''),
                           'label': r['label'], 'confidence': r['confidence'], 'passage': r['passage'], 'context': src[max(0, a - 350):min(len(src), b + 350)],
                           'in': 'note' if part.startswith('n') else ('margin' if part == 'm' else 'text'), 'source_passage': r['source'],
                           'french': r.get('french', ''), 'reason': r.get('reason', '')})
os.makedirs(d + '/in', exist_ok=True); os.makedirs(d + '/out', exist_ok=True)
json.dump({'population': pop, 'sample': sample}, open(d + '/sample.json', 'w'), ensure_ascii=False)
items = [{k: v for k, v in s.items() if k not in ('stratum', 'id', 'confidence')} for s in sample]; random.shuffle(items)
for b in range(0, len(items), 25): json.dump(items[b:b + 25], open('%s/in/p%03d.json' % (d, b // 25), 'w'), ensure_ascii=False)
print(len(sample), 'rows')
