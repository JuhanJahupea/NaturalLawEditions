# issue_cand.py <out dir> [items per batch]: candidates for the pilot issue "the ground of obligation" (ISSUE_TAG_PROMPT.md).
# Reuse rows (not rejected) and divergence notes of: the whole Essai; Burlamaqui 1747, Partie I ch. VI-IX and Partie II ch. II,
# VII, VIII, XII; the Droit des gens, Préface and Préliminaires, and its divergence notes elsewhere whose question or comment
# names obligation, a superior or utility. Each item: key, edition, unit, kind (row or note), source, locus, label or relation,
# Vattel's or Burlamaqui's passage, the source passage, and for a note its question and comment.
import os, sys, re, json, glob
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
out = sys.argv[1]; BS = int(sys.argv[2]) if len(sys.argv) > 2 else 60
cat = json.load(open(ROOT + '/catalogue.json'))
TX = {t['id']: t for t in cat['texts']}; TX.update({e['id']: e for e in cat['editions']})
name = lambda t: '%s, %s' % ((TX.get(t) or {}).get('author', t), (TX.get(t) or {}).get('title', ''))
BUR = re.compile(r'P1\.(6|7|8|9)\.|P2\.(2|7|8|12)\.')
def want(ed, unit, note=None):
    if ed == 'vattel-essai-1747': return True
    if ed == 'burlamaqui-1747': return bool(BUR.match(unit))
    if unit.split('.')[0] in ('Pref', 'Prelim'): return True
    return note is not None and bool(re.search(r'oblig|superior|utilit', note.get('question', '') + ' ' + note.get('comment', ''), re.I))
items = []
for ed in ('vattel-essai-1747', 'burlamaqui-1747', 'vattel-1773'):
    for f in sorted(glob.glob('%s/reuse/%s__*.json' % (ROOT, ed))):
        tb = json.load(open(f))
        for r in tb['rows']:
            if r['status'] == 'rejected' or r['label'] == 'commonplace' or not want(ed, r['unit']): continue
            items.append({'key': 'r:%s:%d' % (ed, r['id']), 'edition': ed, 'unit': r['unit'], 'kind': 'row', 'source': name(tb['to']),
                          'locus': r.get('locus', ''), 'label': r['label'], 'status': r['status'], 'passage': r['passage'][:700],
                          'source_passage': r['source'][:900], 'french': (r.get('french') or '')[:600]})
    for k, d in enumerate(json.load(open('%s/editions/%s/layers/divergences.json' % (ROOT, ed)))['items']):
        if not want(ed, d['unit'], d): continue
        items.append({'key': 'n:%s:%d' % (ed, k), 'edition': ed, 'unit': d['unit'], 'kind': 'note', 'source': d.get('author') or name(d['text']),
                      'locus': d['locus'], 'label': d['relation'], 'passage': d['passage'][:700], 'source_passage': d['sourcePassage'][:900],
                      'question': d['question'], 'comment': d['comment']})
os.makedirs(out + '/in', exist_ok=True); os.makedirs(out + '/out', exist_ok=True)
json.dump(items, open(out + '/items.json', 'w'), ensure_ascii=False)
for b in range(0, len(items), BS): json.dump(items[b:b + BS], open('%s/in/t%03d.json' % (out, b // BS), 'w'), ensure_ascii=False)
import collections
print(len(items), 'items', dict(collections.Counter((i['edition'], i['kind']) for i in items)), (len(items) + BS - 1) // BS, 'batches')
