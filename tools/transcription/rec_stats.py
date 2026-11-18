# rec_stats.py <dir>: recall of the tables for Wolff (JG, INST), Grotius and Pufendorf on the sample of Vattel's sections:
# the share of the reuse a reader found that a row covers (any status; and a match row), all reuse and reuse at 0.5 or more.
import sys, json, glob, collections
d = sys.argv[1]
status = {}
for f in glob.glob(d + '/in/*.json'):
    for u in json.load(open(f))['units']:
        for r in u['rows']: status[r['id']] = r['status']
T = collections.defaultdict(collections.Counter); secs = 0; per = []
for f in sorted(glob.glob(d + '/out/*.json')):
    for s in json.load(open(f))['sections']:
        secs += 1; c = collections.Counter()
        for x in s['found']:
            strong = float(x.get('confidence', 0)) >= 0.5; cov = x.get('covered_by')
            st = status.get(cov) if cov is not None else None
            for key in ('all', x['text']) + (('strong', 'strong ' + x['text']) if strong else ()):
                T[key]['found'] += 1
                if cov is not None: T[key]['covered'] += 1
                if st == 'match': T[key]['covered by match'] += 1
            c['found'] += 1; c['covered'] += cov is not None
        per.append((s['unit'], c['found'], c['covered']))
print(secs, 'sections')
for k in sorted(T, key=lambda k: (k.startswith('strong'), k)):
    v = T[k]; print('%-14s found %3d  covered %3d (%.0f%%)  by match %3d (%.0f%%)' % (k, v['found'], v['covered'], 100 * v['covered'] / v['found'], v['covered by match'], 100 * v['covered by match'] / v['found']))
print(per)
json.dump({'sections': secs, 'totals': {k: dict(v) for k, v in T.items()}, 'per_section': per}, open(d + '/stats.json', 'w'), indent=1)
