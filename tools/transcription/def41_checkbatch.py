# def41_checkbatch.py <batches dir> <judge dir> <out dir> [rows per batch]: the judges' doubtful rows for a second reading
# (DEF41_CHECK_PROMPT.md, Claude Opus): confidence under 0.75, or label shared argument, loose paraphrase or open
# disagreement. Each item carries the whole unit and the whole source segment. Keys are <batch>.<row index>, as in
# def41_merge.py.
import sys, os, json, glob
BD, JD, OUT = sys.argv[1:4]; PER = int(sys.argv[4]) if len(sys.argv) > 4 else 20
os.makedirs(OUT, exist_ok=True)
SEG = json.load(open(os.path.join(BD, 'segments.json')))
ITEMS = {}
for f in glob.glob(os.path.join(BD, 'b*.json')):
    for it in json.load(open(f))['items']: ITEMS[it['unit']] = it
DOUBT = {'shared argument', 'loose paraphrase', 'open disagreement'}
items = []
for f in sorted(glob.glob(os.path.join(JD, 'b*.json'))):
    b = os.path.basename(f)[:-5]
    for i, r in enumerate(json.load(open(f)).get('rows', [])):
        if float(r.get('confidence', 0)) >= 0.75 and r.get('label') not in DOUBT: continue
        it = ITEMS.get(r.get('unit')); seg = SEG.get(r.get('seg', ''))
        if not it or not seg: continue
        ut = it['text'] + ('\nNOTES: ' + ' '.join('%s %s' % (n['mark'], n['text']) for n in it['notes']) if it['notes'] else '')
        items.append({'key': '%s.%d' % (b, i), 'unit': r['unit'], 'where': r.get('where', 'text'), 'passage': r['passage'],
                      'seg': r['seg'], 'locus': seg['locus'], 'source_passage': r['source_passage'], 'label': r.get('label'),
                      'confidence': r.get('confidence'), 'reason': r.get('reason', ''), 'unit_text': ut, 'segment_text': seg['text']})
for k in range(0, len(items), PER):
    json.dump({'items': items[k:k + PER]}, open(os.path.join(OUT, 'c%02d.json' % (k // PER)), 'w'), ensure_ascii=False, indent=1)
print(len(items), 'doubtful rows in', (len(items) + PER - 1) // PER, 'batches')
