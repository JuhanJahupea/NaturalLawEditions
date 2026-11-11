# cmp_old.py <old table> <new rows>: how many old rows a new row covers (same unit, overlapping span).
import sys, json, collections
old = json.load(open(sys.argv[1]))['rows']; new = json.load(open(sys.argv[2]))['rows']
def ov(r, o):
    if not r['at'] or not o['at'] or r['at'][0][0] != o['at'][0][0]: return 0
    a, b = r['at'][0][1:]; c, d = o['at'][0][1:]
    return max(0, min(b, d) - max(a, c)) / max(1, min(b - a, d - c))
byu = collections.defaultdict(list)
for r in new: byu[r['unit']].append(r)
for st in ('match', 'possible'):
    O = [o for o in old if o['status'] == st]
    cov = [o for o in O if any(ov(r, o) > 0 for r in byu[o['unit']])]
    unit = [o for o in O if byu[o['unit']]]
    print(st, len(O), 'old rows; span covered', len(cov), '; unit has new rows', len(unit))
lost = [o for o in old if o['status'] == 'match' and not byu[o['unit']]]
print('old match rows on units with no new row:', len(lost))
for o in lost[:int(sys.argv[3]) if len(sys.argv) > 3 else 0]:
    print(' ', o['id'], o['unit'], o['label'], o['confidence'], o.get('locus'), '|', o['passage'][:90].replace('\n', ' '))
print('new units', len(byu), 'old units', len({o['unit'] for o in old}))
