# add73_cand.py <out dir> [items per batch]: the passages the 1773 edition of Vattel added (layers/changes-1773.json), each with
# the text around it and the rows (all tables) that already overlap it, in batches for ADD73_PROMPT.md.
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT; ED = 'vattel-1773'
out = sys.argv[1]; per = int(sys.argv[2]) if len(sys.argv) > 2 else 8
L = json.load(open('%s/editions/%s/layers/changes-1773.json' % (R, ED)))['items']
U = {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (R, ED)))['units']}
cat = json.load(open(R + '/catalogue.json')); rows = collections.defaultdict(list)
for c in cat['reuse']:
    if c['from'] != ED: continue
    for r in json.load(open(R + '/' + c['path']))['rows']:
        if r['status'] != 'rejected': r['_to'] = c['to']; rows[r['unit']].append(r)
def part_text(u, p): return u['text'] if p == 't' else u['notes'][int(p[1:])]['text']
items = []
for x in L:
    at = x.get('at') or []
    if x.get('type') == 'deleted phrase' or not at: continue
    u = U[x['unit']]; spans = []
    for p, a, b in at: spans.append({'part': p, 'text': part_text(u, p)[a:b]})
    if sum(len(s['text']) for s in spans) < 40: continue
    ov = []
    for r in rows[x['unit']]:
        for p, a, b in at:
            if any(q[0] == p and min(q[2], b) - max(q[1], a) > 0 for q in r.get('at', [])):
                ov.append({'id': r['id'], 'table': r['_to'], 'locus': r.get('locus'), 'label': r['label'], 'status': r['status'], 'passage': r['passage'][:300]}); break
    items.append({'unit': x['unit'], 'change': x['id'], 'type': x['type'], 'content': x.get('content', ''), 'added': spans,
                  'unit_text': u['text'], 'notes': [n['text'] for n in u.get('notes', [])], 'rows_overlapping': ov})
os.makedirs(out + '/in', exist_ok=True); os.makedirs(out + '/out', exist_ok=True)
for b in range(0, len(items), per): json.dump({'items': items[b:b + per]}, open('%s/in/d%03d.json' % (out, b // per), 'w'), ensure_ascii=False, indent=0)
print(len(items), 'additions', sum(len(i['rows_overlapping']) for i in items), 'overlapping rows', (len(items) + per - 1) // per, 'batches')
