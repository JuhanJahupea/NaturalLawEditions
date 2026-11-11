# build_review.py <edition> <WORK> <rows.json> <outdir> [batch size]: rows at status possible -> second-judge batches
# (REVIEW_POSSIBLE_PROMPT.md). Each item: the edition part holding the passage and the source part holding the source
# passage, each cut to 6000 characters around the passage. keys.json maps each key to the row's unit, page and passages,
# so the verdicts can be applied to a later merge whose row ids differ (apply_review.py).
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
from merge_find import find
B = WORK
R = ROOT
ed, work, rf, outdir = sys.argv[1:5]; size = int(sys.argv[5]) if len(sys.argv) > 5 else 12
EDN = {'vattel-1773': 'Vattel, Le droit des gens (Neuchâtel 1773)', 'burlamaqui-1747': 'Burlamaqui, Principes du droit naturel (Genève 1747)'}
SRC = {'GRO24': 'Grotius, Le droit de la guerre et de la paix, trad. Barbeyrac (Amsterdam 1724)',
       'PUF34': 'Pufendorf, Le droit de la nature et des gens, trad. Barbeyrac (Amsterdam 1734)'}
AUTH = {'GRO24': 'Grotius', 'PUF34': 'Pufendorf'}
units = {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units']}
P = {p['id']: p for p in json.load(open('%s/corpus/%s.json' % (B, work)))['pages']}
rows = [r for r in json.load(open(rf))['rows'] if r['status'] == 'possible']
def cut(t, a, b, n=6000):
    if len(t) <= n: return t
    s = max(0, min(a - (n - (b - a)) // 2, len(t) - n)); return ('[...] ' if s else '') + t[s:s + n] + (' [...]' if s + n < len(t) else '')
items, keys = [], {}
for r in rows:
    u = units[r['unit']]
    if r['at']:
        w = r['at'][0][0]
        if w == 't': part, et = 'text', u['text']
        else:
            n = u['notes'][int(w[1:])]; part, et = 'note %s' % n['mark'], n['text']
    else: part, et = 'margin', u.get('margin', '')
    a = find(et, r['passage']) or [0, 0]
    p = P[r['page']]
    parts = [('text', p['text'][x:y]) for x, y, _ in p['spans']] + \
            [('note by %s' % (AUTH[work] if n['by'] == 'author' else 'Barbeyrac'), n['text']) for n in p['notes']] + \
            [('margin', m['text']) for m in p['margin']]
    sp, st, sa = 'text', p['text'], [0, 0]
    for kind, t in parts:
        f = find(t, r['source'])
        if f: sp, st, sa = kind, t, f; break
    k = str(r['id'])
    keys[k] = {'unit': r['unit'], 'page': r['page'], 'passage': r['passage'], 'source': r['source']}
    items.append({'key': k, 'unit': r['unit'], 'part': part, 'edition_text': cut(et, a[0], a[1]), 'passage': r['passage'],
                  'source_locus': r['locus'], 'source_part': sp, 'source_text': cut(st, sa[0], sa[1]), 'source_passage': r['source'],
                  'label': r['label'], 'confidence': r['confidence'], 'reason': r.get('reason', '')})
os.makedirs(outdir + '/in', exist_ok=True); os.makedirs(outdir + '/out', exist_ok=True)
json.dump(keys, open(outdir + '/keys.json', 'w'), ensure_ascii=False)
for b in range(0, len(items), size):
    json.dump({'edition': EDN[ed], 'source': SRC[work], 'items': items[b:b + size]}, open('%s/in/r%03d.json' % (outdir, b // size), 'w'), ensure_ascii=False)
ch = [len(json.dumps(items[b:b + size], ensure_ascii=False)) for b in range(0, len(items), size)]
print(len(items), 'rows;', len(ch), 'batches; chars per batch mean', sum(ch) // len(ch), 'max', max(ch))
