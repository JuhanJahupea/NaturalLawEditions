# essai_div_verify.py <screen dir> <out dir> [min confidence]: the pairs the Essai divergence screen flagged (diverges or partly,
# same question, confidence >= 0.5 by default) -> verify batches of 8 for ESSAI_DIV_VERIFY_PROMPT.md, each with the whole source
# section (cut at 15000 characters) and its notes (cut at 6000). A pair flagged twice (two readers, or own and added) goes once.
import sys, os, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
sd, out = sys.argv[1:3]; mc = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
SEC = json.load(open(sd + '/sections.json'))
units = {u['id']: u for u in json.load(open(ROOT + '/editions/vattel-essai-1747/text.json'))['units']}
cap = lambda t, n: t if len(t) <= n else t[:n] + ' [...]'
items, seen, n, st = [], set(), 0, collections.Counter()
for f in sorted(glob.glob(sd + '/out/d*.json')):
    for it in json.load(open(f))['items']:
        for pr in it.get('pairs', []):
            n += 1; st[pr.get('relation') if pr.get('same_question') else 'other'] += 1
            if not pr.get('same_question') or pr.get('relation') not in ('diverges', 'partly'): continue
            if float(pr.get('confidence', 0)) < mc or pr.get('key') not in SEC: continue
            k = (it['vattel_id'], pr['key'])
            if k in seen: continue
            seen.add(k); u = units[it['vattel_id']]; s = SEC[pr['key']]
            items.append({'vattel_sec': u['id'], 'vattel_margin': u.get('margin', ''), 'vattel_text': u['text'],
                          'vattel_notes': ' '.join('%s %s' % (x['mark'], x['text']) for x in u.get('notes', [])),
                          'source': s['code'], 'source_ref': s['locus'], 'source_margin': s.get('margin', ''),
                          'source_text': cap(s['text'], 15000), 'source_notes': cap(s['notes'], 6000),
                          'screen': {'question': it.get('question', ''), **{x: pr.get(x, '') for x in
                                     ('relation', 'source_answer', 'vattel_answer', 'source_passage', 'vattel_passage')}}})
os.makedirs(out + '/in', exist_ok=True); os.makedirs(out + '/out', exist_ok=True)
for b in range(0, len(items), 8): json.dump(items[b:b + 8], open('%s/in/v%03d.json' % (out, b // 8), 'w'), ensure_ascii=False)
print(n, 'pairs screened', dict(st), ';', len(items), 'flagged;', (len(items) + 7) // 8, 'batches')
