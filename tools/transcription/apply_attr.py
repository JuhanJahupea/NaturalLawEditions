# apply_attr.py <items.json> <verify dir> [date]: second reading of the attributions (ATTR_VERIFY_PROMPT.md).
# wrong: the item leaves editions/<ed>/passes/attributions.json. correct: kept, with the second reader's form and cue (when the
# cue is found in the unit). unsure: kept and marked, for a decision by hand. Each kept item gets "review": {verdict, reason, date}.
import sys, os, json, re, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
from merge_find import find
R = ROOT
itf, d = sys.argv[1:3]; date = sys.argv[3] if len(sys.argv) > 3 else '2026-11-13'
items = {i['id']: i for i in json.load(open(itf))}
V = {v['id']: v for f in sorted(glob.glob(d + '/out/*.json')) for v in json.load(open(f))['items']}
def strip(h): return re.sub(r'<[^>]+>', '', h)
c = collections.Counter(); unsure = []
for ed in ('vattel-1773', 'burlamaqui-1747'):
    p = '%s/editions/%s/passes/attributions.json' % (R, ed); P = json.load(open(p))
    U = {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units']}
    byk = {(i['key']['text'], i['key']['unit'], i['key']['page'], i['key']['passage'], i['key']['source']): i['id'] for i in items.values() if i['ed'] == ed}
    out = []
    for a in P['attributions']:
        iid = byk[(a['text'], a['unit'], a['page'], a['passage'], a['source'])]; v = V.get(iid)
        if not v: c['not read'] += 1; out.append(a); continue
        verdict = v.get('verdict'); c[verdict] += 1
        if verdict == 'wrong': continue
        if verdict == 'correct':
            if v.get('form') in ('quotation', 'reference') and v['form'] != a['form']: a['form'] = v['form']; c['form changed'] += 1
            cue = (v.get('cue') or '').strip()
            if cue and cue != a['cue']:
                u = U[a['unit']]; parts = [('t', strip(u['text'])), ('m', u.get('margin', ''))] + [('n%d' % k, strip(n['text'])) for k, n in enumerate(u.get('notes', []))]
                for pt, h in parts:
                    r = find(h, cue)
                    if r: a['cue'], a['cuePart'] = h[r[0]:r[1]], pt; c['cue changed'] += 1; break
                else: c['new cue not found'] += 1
        a['review'] = {'verdict': verdict, 'reason': v.get('reason', ''), 'date': date}
        if verdict == 'unsure': unsure.append(iid)
        out.append(a)
    P['attributions'] = out
    P['description'] = re.sub(r' Judged by a language model, not checked by hand\.| Judged by a language model; a second model read each item.*?(?= Rows labelled| $)', '', P['description'])
    P['description'] += ' A second model (Claude Opus) read each item with the whole unit: wrong items were removed; review holds its verdict (correct, or unsure: left for a decision by hand) and reason.' if 'second model' not in P['description'] else ''
    with open(p, 'w', encoding='utf-8') as f: json.dump(P, f, ensure_ascii=False, indent=1); f.write('\n')
    print(ed, len(out), 'kept')
json.dump(unsure, open(d + '/unsure.json', 'w'))
print(dict(c), 'unsure', len(unsure))
