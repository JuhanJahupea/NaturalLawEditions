# apply_review.py <rows.json> <review dir[,review dir...]> <out> [date]: second-judge verdicts on possible rows (build_review.py,
# REVIEW_POSSIBLE_PROMPT.md) -> rows. Rows are matched by unit, page and both passages, so the verdicts survive a re-merge.
# drop: the row goes. commonplace: label commonplace, the first judge's confidence, status possible.
# keep: the second judge's label and confidence; status match >= 0.5, possible 0.3-0.5; under 0.3 the row goes.
# Each reviewed row gets "review": {"step": "R", "verdict", "confidence", "reason", "date"} and keeps the first judge's reason.
import sys, json, glob, collections
rf, dirs, out = sys.argv[1:4]; date = sys.argv[4] if len(sys.argv) > 4 else '2026-11-11'
D = json.load(open(rf)); rows = D['rows']
V = {}
for d in dirs.split(','):
    keys = json.load(open(d + '/keys.json'))
    for f in sorted(glob.glob(d + '/out/r*.json')):
        for v in json.load(open(f))['items']:
            k = keys[str(v['key'])]; V[(k['unit'], k['page'], k['passage'], k['source'])] = v
LABELS = {'verbatim', 'close paraphrase', 'loose paraphrase', 'citation', 'open disagreement'}
c = collections.Counter(); kept = []
for r in rows:
    v = V.get((r['unit'], r['page'], r['passage'], r['source']))
    if not v or r['status'] != 'possible': kept.append(r); continue
    verdict = v['verdict']; conf = round(float(v.get('confidence', 0)), 2)
    if verdict == 'keep' and v.get('label') not in LABELS: verdict = 'keep?'
    c[verdict] += 1
    r['review'] = {'step': 'R', 'verdict': verdict, 'confidence': conf, 'reason': v.get('reason', ''), 'date': date}
    if verdict == 'drop': continue
    if verdict == 'commonplace': r['label'] = 'commonplace'
    elif verdict == 'keep':
        if conf < 0.3: c['keep under 0.3'] += 1; continue
        r['label'] = v['label']; r['confidence'] = conf; r['status'] = 'match' if conf >= 0.5 else 'possible'
        c['keep -> ' + r['status']] += 1
    kept.append(r)
D['rows'] = kept
json.dump(D, open(out, 'w'), ensure_ascii=False)
print(len(rows), '->', len(kept), 'rows; reviewed', sum(v for k, v in c.items() if k in ('keep', 'commonplace', 'drop', 'keep?')), dict(c),
      '; status', dict(collections.Counter(r['status'] for r in kept)))
