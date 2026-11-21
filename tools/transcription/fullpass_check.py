# fullpass_check.py <full dir> <out dir> [n match] [n possible]: second-reading batches after the full pass (FULL_PASS_PROMPT.md):
# every row the readers judged wrong (rows_wrong, in the Jus gentium, Institutiones and Pufendorf tables), and a random sample of
# the rows the pass added (step F in passes/additions.json), by status. Batches of 25 for PRECISION_PROMPT.md; <out>/items.json keeps
# for each key the row's table and id, why it was drawn, and the first reader's reason for a flagged row.
import sys, os, json, glob, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT; d, out = sys.argv[1], sys.argv[2]
NM = int(sys.argv[3]) if len(sys.argv) > 3 else 80; NP = int(sys.argv[4]) if len(sys.argv) > 4 else 40
cat = json.load(open(R + '/catalogue.json')); TX = {t['id']: t for t in cat['texts']}
for e in cat['editions']: TX.setdefault(e['id'], {'author': e['author'], 'title': e['title'], 'date': e['date']})
U = {u['id']: u for u in json.load(open(R + '/editions/vattel-1773/text.json'))['units']}
TAB = ['wolff-jus-gentium-1749', 'wolff-institutiones-1750', 'pufendorf-barbeyrac-1734']
rows = {}
for t in TAB:
    for r in json.load(open('%s/reuse/vattel-1773__%s.json' % (R, t)))['rows']: rows[r['id']] = (t, r)
flag = {}
for f in sorted(glob.glob(d + '/out/*.json')):
    for s in json.load(open(f)).get('sections', []):
        for w in s.get('rows_wrong', []):
            try: i = int(w['id'])
            except (TypeError, ValueError): continue
            if i in rows and rows[i][1]['status'] != 'rejected': flag.setdefault(i, w.get('why', ''))
F = [r for t, r in rows.values() if r.get('step') == 'F' and r['status'] != 'rejected']
random.seed(20261121)
pick = random.sample([r for r in F if r['status'] == 'match'], min(NM, sum(r['status'] == 'match' for r in F))) + \
       random.sample([r for r in F if r['status'] == 'possible'], min(NP, sum(r['status'] == 'possible' for r in F)))
def item(t, r, why, first=''):
    u = U[r['unit']]; part = r['at'][0][0] if r.get('at') else 'm'
    src = u['text'] if part == 't' else (u.get('margin', '') if part == 'm' else u['notes'][int(part[1:])]['text'])
    a, b = (r['at'][0][1], r['at'][0][2]) if r.get('at') else (max(0, src.find(r['passage'][:40])), 0)
    if not b: b = a + len(r['passage'])
    x = TX[t]
    return {'edition': 'vattel-1773', 'table': t, 'id': r['id'], 'why': why, 'first': first, 'status': r['status'], 'unit': r['unit'],
            'source': '%s, %s (%s)' % (x['author'], x['title'], x.get('date', '')), 'family': r['family'], 'locus': r.get('locus', ''),
            'label': r['label'], 'passage': r['passage'], 'context': src[max(0, a - 350):min(len(src), b + 350)],
            'in': 'note' if part.startswith('n') else ('margin' if part == 'm' else 'text'), 'source_passage': r['source'],
            'french': r.get('french', ''), 'reason': r.get('reason', '')}
items = [item(rows[i][0], rows[i][1], 'flagged', w) for i, w in sorted(flag.items())]
items += [item(next(t for t in TAB if rows.get(r['id'], (None,))[0] == t), r, 'sample') for r in pick if r['id'] not in flag]
for k, it in enumerate(items): it['key'] = k
os.makedirs(out + '/in', exist_ok=True); os.makedirs(out + '/out', exist_ok=True)
json.dump(items, open(out + '/items.json', 'w'), ensure_ascii=False)
show = [{k: v for k, v in s.items() if k not in ('id', 'why', 'first', 'status')} for s in items]; random.shuffle(show)
for b in range(0, len(show), 25): json.dump(show[b:b + 25], open('%s/in/q%03d.json' % (out, b // 25), 'w'), ensure_ascii=False)
print(len(flag), 'flagged,', len(items) - len(flag), 'sampled of', len(F), 'F rows;', (len(show) + 24) // 25, 'batches')
