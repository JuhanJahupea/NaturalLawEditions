# gloss_merge.py <dir> <date> [--write]: the glosses the readers wrote (GLOSS_PROMPT.md; <dir>/out/*.json) -> editions/<ed>/layers/glosses.json
# for each edition, and the layer's entry in edition.json. Each passage is placed on its unit's text or note (exact, or by merge_find);
# a passage that overlaps one already placed in the same part is dropped (the longer stays). Ids: g1, g2, ... in reading order.
import sys, os, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
from merge_find import find
d, date = sys.argv[1:3]; WRITE = '--write' in sys.argv
R = ROOT
EDS = ['vattel-1773', 'burlamaqui-1747', 'vattel-essai-1747']
LAYER = {'id': 'glosses', 'file': 'layers/glosses.json', 'kind': 'glosses', 'label': 'Translations', 'default': True,
         'tooltip': 'English translations of the Latin, Greek and other foreign-language passages, by Claude Opus. '
                    'Dotted underline in the text: hover to read; the list follows each section.'}
G = [g for f in sorted(glob.glob(d + '/out/*.json')) for g in json.load(open(f)).get('glosses', [])]
fails = collections.Counter(); placed = collections.defaultdict(list)
for g in G:
    ed = g.get('edition')
    if ed not in EDS: fails['edition'] += 1; continue
    U = placed.setdefault('_units_' + ed, {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units']})
    u = U.get(g.get('unit'))
    if not u: fails['unit'] += 1; continue
    part = g.get('part', 't'); txt = (u.get('text', '') if part == 't' else (u.get('notes', [])[int(part[1:])]['text'] if part[1:].isdigit() and int(part[1:]) < len(u.get('notes', [])) else None))
    parts = [(part, txt)] if txt is not None else []
    parts += [(p, t) for p, t in [('t', u.get('text', ''))] + [('n%d' % i, n['text']) for i, n in enumerate(u.get('notes', []))] if p != part]
    hit = None
    for p, t in parts:
        i = t.find(g['text'])
        if i >= 0: hit = (p, i, i + len(g['text'])); break
    if not hit:
        for p, t in parts:
            f = find(t, g['text'])
            if f: hit = (p, f[0], f[1]); break
    if not hit: fails['text not found'] += 1; print('  NOT FOUND', ed, g['unit'], g['text'][:60]); continue
    if not g.get('translation'): fails['no translation'] += 1; continue
    placed[ed].append(dict(g, _at=hit))
out = {}
for ed in EDS:
    order = {u: i for i, u in enumerate(placed.get('_units_' + ed, {}))}
    rows = sorted(placed.get(ed, []), key=lambda g: (order[g['unit']], g['_at'][0] != 't', g['_at'][0], g['_at'][1], -(g['_at'][2] - g['_at'][1])))
    keep = []
    for g in rows:
        if any(k['unit'] == g['unit'] and k['_at'][0] == g['_at'][0] and k['_at'][1] < g['_at'][2] and g['_at'][1] < k['_at'][2] for k in keep):
            fails['overlap'] += 1; continue
        keep.append(g)
    items = []
    for i, g in enumerate(keep, 1):
        it = {'id': 'g%d' % i, 'unit': g['unit'], 'at': [list(g['_at'])], 'lang': g.get('lang', 'la'), 'text': g['text'], 'translation': g['translation'].strip()}
        if g.get('source'): it['source'] = g['source']
        if g.get('note'): it['note'] = g['note']
        items.append(it)
    out[ed] = items
    print(ed, len(items), dict(collections.Counter(x['lang'] for x in items)))
print('failed', dict(fails))
if WRITE:
    for ed, items in out.items():
        if not items: continue
        L = {'format': 'nle-layer/1', 'edition': ed, 'layer': 'glosses', 'kind': 'glosses', 'date': date,
             'description': 'English translations of the passages in Latin, Greek and other languages than French. at: the passage in the unit '
                            '(part, start, end); lang: ISO 639 code; text: the passage; translation: English; source: the author and work quoted, '
                            'where the edition names them; note: a misprint or a doubtful reading. Candidates found by a character-trigram model '
                            '(Latin, French, English) and Greek letters; passages fixed and translated by Claude Opus; not checked by hand.',
             'items': items}
        with open('%s/editions/%s/layers/glosses.json' % (R, ed), 'w') as f: json.dump(L, f, ensure_ascii=False, separators=(',', ':')); f.write('\n')
        p = '%s/editions/%s/edition.json' % (R, ed); M = json.load(open(p))
        if not any(l['id'] == 'glosses' for l in M['layers']):
            s = open(p).read()
            # the entry goes after the last layer; edition.json keeps its own layout
            k = s.index('"layers"'); j = s.index('\n  ]', k)
            ent = json.dumps(LAYER, ensure_ascii=False)
            s = s[:j] + ',\n    ' + ent + s[j:]
            open(p, 'w').write(s); assert any(l['id'] == 'glosses' for l in json.load(open(p))['layers'])
    print('written')
