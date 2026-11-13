# div_already.py <batch dir> <divergence pass> <field>: adds to every item of <batch dir>/in/*.json the comments that an
# earlier divergence pass holds for the item's unit (field name e.g. dng_notes), so the screen and the verifier can leave them out.
import sys, json, glob, collections
d, pf, field = sys.argv[1:4]
P = json.load(open(pf)); C = collections.defaultdict(list)
for it in P['items']: C[it['unit']].append('%s (%s, severity %d) %s' % (it['question'], it['relation'], it['severity'], it['comment']))
n = 0
for f in sorted(glob.glob(d + '/in/*.json')):
    items = json.load(open(f))
    for it in items:
        uid = next(v for k, v in it.items() if k.endswith('_id') or k.endswith('_sec'))
        it[field] = C.get(uid, []); n += bool(it[field])
    json.dump(items, open(f, 'w'), ensure_ascii=False)
print(n, 'items carry', field)
