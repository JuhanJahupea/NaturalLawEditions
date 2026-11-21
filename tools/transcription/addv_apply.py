# addv_apply.py <dir> <date> [--write]: the second reading of the rows of editions/vattel-1773/passes/additions.json
# (PRECISION_PROMPT.md; <dir>/out/*.json) into the rows: audit {verdict, reason, date, labelWas, statusWas}; right rows are (or
# become) match, weak rows possible, wrong rows rejected; a label the reader would change is changed.
import sys, os, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
d, date = sys.argv[1:3]; WRITE = '--write' in sys.argv
p = ROOT + '/editions/vattel-1773/passes/additions.json'; P = json.load(open(p)); by = {r['id']: r for r in P['rows']}
items = {x['key']: x for x in json.load(open(d + '/items.json'))}
V = {int(it['key']): it for f in sorted(glob.glob(d + '/out/*.json')) for it in json.load(open(f))['items']}
LABELS = {'verbatim', 'close paraphrase', 'loose paraphrase', 'translation', 'shared argument', 'citation', 'open disagreement', 'commonplace'}
st = collections.Counter(); bystep = collections.defaultdict(collections.Counter); bytab = collections.defaultdict(collections.Counter); labs = collections.Counter()
for k, v in sorted(V.items()):
    x = items[k]; r = by[x['id']]; was = r['status']
    a = {'verdict': v['verdict'], 'reason': v['reason'], 'date': date}
    if not v.get('label_ok', True) and v.get('better_label') and v['better_label'].strip().lower() != r['label']:
        bl = v['better_label'].strip().lower(); assert bl in LABELS, bl
        a['labelWas'] = r['label']; r['label'] = bl; labs[(a['labelWas'], bl)] += 1
    new = {'right': 'match', 'weak': 'possible', 'wrong': 'rejected'}[v['verdict']]
    if new != was: r['status'] = new; a['statusWas'] = was
    r['audit'] = a; st[v['verdict']] += 1; bystep[(r['step'], was)][v['verdict']] += 1; bytab[r['table']][v['verdict']] += 1
print(len(V), 'of', len(items), dict(st))
for k, c in sorted(bystep.items()): print(' ', k, dict(c))
for k, c in sorted(bytab.items()): print(' ', k, dict(c))
print('labels', sum(labs.values()), labs.most_common(6))
if WRITE:
    json.dump(P, open(p, 'w'), ensure_ascii=False, indent=1)
    rows = [{'table': items[k]['table'], 'id': items[k]['id'], 'step': items[k]['step'], 'statusWas': items[k]['status'], 'unit': items[k]['unit'],
             'locus': items[k]['locus'], 'label': items[k]['label'], 'verdict': v['verdict'], 'labelOk': v.get('label_ok', True),
             'betterLabel': v.get('better_label') or '', 'reason': v['reason']} for k, v in sorted(V.items())]
    json.dump({'format': 'nle-audit/1', 'date': date, 'kind': 'second reading', 'edition': 'vattel-1773',
               'description': 'Every row of passes/additions.json (steps A, C and V), read by a second reader (Claude Opus, tools/transcription/PRECISION_PROMPT.md): right, weak or wrong, and whether the label fits.',
               'rows': rows}, open(ROOT + '/audit/additions-second-reading-%s.json' % date, 'w'), ensure_ascii=False, indent=1)
    print('written')
