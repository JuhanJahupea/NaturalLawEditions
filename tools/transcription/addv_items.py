# addv_items.py <dir>: every row of editions/vattel-1773/passes/additions.json (steps A, C, V), for a second reading with
# PRECISION_PROMPT.md; batches of 25. Items keep the row id and table in <dir>/items.json; the readers see neither.
import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT; d = sys.argv[1]
cat = json.load(open(R + '/catalogue.json')); TX = {t['id']: t for t in cat['texts']}
for e in cat['editions']: TX.setdefault(e['id'], {'author': e['author'], 'title': e['title'], 'date': e['date']})
U = {u['id']: u for u in json.load(open(R + '/editions/vattel-1773/text.json'))['units']}
rows = json.load(open(R + '/editions/vattel-1773/passes/additions.json'))['rows']
items = []
for r in rows:
    u = U[r['unit']]; part = r['at'][0][0] if r.get('at') else 'm'
    src = u['text'] if part == 't' else (u.get('margin', '') if part == 'm' else u['notes'][int(part[1:])]['text'])
    a, b = (r['at'][0][1], r['at'][0][2]) if r.get('at') else (max(0, src.find(r['passage'][:40])), 0)
    if not b: b = a + len(r['passage'])
    t = TX[r['table']]
    items.append({'key': len(items), 'edition': 'vattel-1773', 'table': r['table'], 'id': r['id'], 'step': r['step'], 'status': r['status'], 'unit': r['unit'],
                  'source': '%s, %s (%s)' % (t['author'], t['title'], t.get('date', '')), 'family': r['family'], 'locus': r.get('locus', ''),
                  'label': r['label'], 'passage': r['passage'], 'context': src[max(0, a - 350):min(len(src), b + 350)],
                  'in': 'note' if part.startswith('n') else ('margin' if part == 'm' else 'text'), 'source_passage': r['source'],
                  'french': r.get('french', ''), 'reason': r.get('reason', '')})
os.makedirs(d + '/in', exist_ok=True); os.makedirs(d + '/out', exist_ok=True)
json.dump(items, open(d + '/items.json', 'w'), ensure_ascii=False)
show = [{k: v for k, v in s.items() if k not in ('id', 'step', 'status')} for s in items]; random.seed(20261121); random.shuffle(show)
for b in range(0, len(show), 25): json.dump(show[b:b + 25], open('%s/in/q%03d.json' % (d, b // 25), 'w'), ensure_ascii=False)
print(len(items), 'rows', (len(show) + 24) // 25, 'batches')
