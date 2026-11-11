# prep_earlier.py <old table> <new rows> <out cand> <out earlier>: old match rows that no new row overlaps,
# as candidates (unit -> the old row's page) and pointers (unit -> [{page_id, passage, source}]) for a recheck batch.
import sys, json, collections
old = json.load(open(sys.argv[1]))['rows']; new = json.load(open(sys.argv[2]))['rows']
by = collections.defaultdict(list)
for r in new: by[r['unit']].append(r)
def ov(a, b):
    if not a['at'] or not b['at'] or a['at'][0][0] != b['at'][0][0]: return 0
    x, y = a['at'][0][1:]; c, d = b['at'][0][1:]; return max(0, min(y, d) - max(x, c))
cand, ear = collections.defaultdict(list), collections.defaultdict(list)
for o in old:
    if o['status'] != 'match' or any(ov(r, o) > 0 for r in by[o['unit']]): continue
    p = o['page']
    for q in [p] + ['%s.p%d' % (p.split('.p')[0], int(p.split('.p')[1]) + d) for d in (1,)]:
        if q not in cand[o['unit']]: cand[o['unit']].append(q)
    ear[o['unit']].append({'page_id': p, 'passage': o['passage'], 'source': o['source']})
json.dump({'cand': cand}, open(sys.argv[3], 'w')); json.dump(ear, open(sys.argv[4], 'w'), ensure_ascii=False)
print(len(ear), 'units,', sum(map(len, ear.values())), 'old rows')
