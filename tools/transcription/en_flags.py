# en_flags.py batches <layer> <plain_fr> <dir> [28] | merge <layer> <dir>: the translation check of an aligned English layer.
# batches: one item per unit with its aligned pairs (French sentences of a group, English sentences of the group) for the agent
# prompt TRANSLATE_CHECK_PROMPT_BURLAMAQUI.md. merge: the flags whose phrases stand in their pair go into the layer's units as flags.
import sys, json, glob, collections
mode = sys.argv[1]
if mode == 'batches':
    lf, pf, d = sys.argv[2:5]; bs = int(sys.argv[5]) if len(sys.argv) > 5 else 28
    L = json.load(open(lf))['units']; PL = json.load(open(pf)); items = []
    for sid, u in L.items():
        t = PL[sid]; fr = [t[a:b] for a, b in u['fr']]
        items.append({'sid': sid, 'pairs': [{'k': k, 'fr': ' '.join(fr[i] for i in g[0]), 'en': ' '.join(u['sents'][j] for j in g[1])} for k, g in enumerate(u['align'])]})
    import os; os.makedirs(d + '/in', exist_ok=True); os.makedirs(d + '/out', exist_ok=True)
    for b in range(0, len(items), bs): json.dump(items[b:b + bs], open('%s/in/t%03d.json' % (d, b // bs), 'w'), ensure_ascii=False)
    print(len(items), 'units', (len(items) + bs - 1) // bs, 'batches')
else:
    lf, d = sys.argv[2:4]; L = json.load(open(lf))
    pairs = {(it['sid'], pr['k']): pr for f in glob.glob(d + '/in/*.json') for it in json.load(open(f)) for pr in it['pairs']}
    T = {'mistranslation', 'shift', 'omission', 'addition', 'terminology', 'false friend'}; fl = collections.defaultdict(list); bad = collections.Counter()
    for f in sorted(glob.glob(d + '/out/*.json')):
        for x in json.load(open(f))['flags']:
            pr = pairs.get((x['sid'], x['k']))
            if not pr or (x['fr'] and x['fr'] not in pr['fr']) or (x['en'] and x['en'] not in pr['en']) or x['type'] not in T: bad['dropped'] += 1; continue
            fl[x['sid']].append({'k': x['k'], 'fr': x['fr'], 'en': x['en'], 'type': x['type'], 'sev': int(x.get('severity', x.get('sev', 1))), 'note': x['note']})
    for sid, u in L['units'].items(): u['flags'] = sorted(fl.get(sid, []), key=lambda f: f['k'])
    with open(lf, 'w', encoding='utf-8') as f: json.dump(L, f, ensure_ascii=False, separators=(',', ':')); f.write('\n')
    print(sum(len(v) for v in fl.values()), 'flags in', len(fl), 'units', dict(bad))
