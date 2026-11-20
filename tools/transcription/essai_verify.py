# essai_verify.py <out dir> [status]: every row of the Essai's tables at status match (default) or possible, not commonplace and
# not yet read by a second reader, in batches of 25 for VERIFY_PROMPT_ESSAI.md (right, weak or wrong, and whether the label fits).
import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT; ED = 'vattel-essai-1747'; out = sys.argv[1]; STATUS = sys.argv[2] if len(sys.argv) > 2 else 'match'
cat = json.load(open(R + '/catalogue.json')); TX = {t['id']: t for t in cat['texts']}
for e in cat['editions']: TX.setdefault(e['id'], {'author': e['author'], 'title': e['title'], 'date': e['date']})
U = {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (R, ED)))['units']}
items = []
for c in cat['reuse']:
    if c['from'] != ED: continue
    for r in json.load(open(R + '/' + c['path']))['rows']:
        if r['status'] != STATUS or r['label'] == 'commonplace' or r.get('audit'): continue
        u = U[r['unit']]; part = r['at'][0][0] if r.get('at') else 't'
        src = u['text'] if part == 't' else u['notes'][int(part[1:])]['text']
        a, b = r['at'][0][1], r['at'][0][2]; t = TX[c['to']]
        items.append({'key': len(items), 'edition': ED, 'table': c['to'], 'id': r['id'], 'unit': r['unit'],
                      'source': '%s, %s (%s)' % (t['author'], t['title'], t.get('date', '')), 'family': r['family'], 'locus': r.get('locus', ''),
                      'label': r['label'], 'passage': r['passage'], 'context': src[max(0, a - 350):min(len(src), b + 350)],
                      'in': 'note' if part.startswith('n') else 'text', 'source_passage': r['source'], 'french': r.get('french', ''), 'reason': r.get('reason', '')})
os.makedirs(out + '/in', exist_ok=True); os.makedirs(out + '/out', exist_ok=True)
json.dump(items, open(out + '/items.json', 'w'), ensure_ascii=False)
sh = items[:]; random.seed(20261120); random.shuffle(sh)
for b in range(0, len(sh), 25):
    json.dump([{k: v for k, v in x.items() if k != 'id'} for x in sh[b:b + 25]], open('%s/in/v%03d.json' % (out, b // 25), 'w'), ensure_ascii=False)
print(len(items), 'rows', (len(items) + 24) // 25, 'batches')
