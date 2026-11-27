# def41_div_verify.py <batches dir> <screen dir> <out dir> [pairs per batch]: the pairs the divergence screen flagged
# (relation partly or diverges) with the whole unit and the whole source segment, for DEF41_DIV_VERIFY_PROMPT.md.
import sys, os, json, glob
BD, SD, OUT = sys.argv[1:4]; PER = int(sys.argv[4]) if len(sys.argv) > 4 else 13
os.makedirs(OUT, exist_ok=True)
SEG = json.load(open(os.path.join(BD, 'segments.json')))
ITEMS = {}
for f in glob.glob(os.path.join(BD, 'b*.json')):
    for it in json.load(open(f))['items']: ITEMS[it['unit']] = it
out = []
for f in sorted(glob.glob(os.path.join(SD, 's*.json'))):
    for it in json.load(open(f))['items']:
        for p in it.get('pairs', []):
            if not p.get('same_question') or p.get('relation') not in ('partly', 'diverges') or p.get('key') not in SEG: continue
            u = ITEMS[it['vattel_id']]
            out.append({'vattel_sec': it['vattel_id'], 'vattel_text': u['text'], 'vattel_notes': u['notes'],
                        'source': p['key'].split('.')[0], 'source_key': p['key'], 'source_ref': SEG[p['key']]['locus'],
                        'source_text': SEG[p['key']]['text'][:15000],
                        'screen': {k: p.get(k) for k in ('relation', 'source_answer', 'vattel_answer', 'source_passage', 'vattel_passage', 'confidence')} | {'question': it.get('question')}})
for k in range(0, len(out), PER):
    json.dump({'items': out[k:k + PER]}, open(os.path.join(OUT, 'v%02d.json' % (k // PER)), 'w'), ensure_ascii=False, indent=1)
print(len(out), 'flagged pairs in', (len(out) + PER - 1) // PER, 'batches')
