# def41_div_write.py <batches dir> <verify dir>: the kept divergences of Vattel's Défense (1741) from Leibniz and Wolff into
# editions/vattel-defense-1741/provenance/divergences.json (the items of an nle-layer/1 comments layer; the edition build
# places them). Each passage is checked in its unit and segment.
import sys, os, json, glob, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
BD, VD = sys.argv[1:3]
SEG = json.load(open(os.path.join(BD, 'segments.json')))
ITEMS = {}
for f in glob.glob(os.path.join(BD, 'b*.json')):
    for it in json.load(open(f))['items']: ITEMS[it['unit']] = it
TEXT = {'THEO': ('leibniz-theodicee-1734', 'L'), 'PSR34': ('wolff-psychologia-rationalis-1734', 'W')}
norm = lambda t: re.sub(r'\s+', ' ', re.sub(r'\[p\. [^\]]*\]', ' ', t).replace('_', '')).strip()
out, bad, rej = [], [], 0
for f in sorted(glob.glob(os.path.join(VD, 'v*.json'))):
    for v in json.load(open(f))['items']:
        if v.get('verdict') != 'keep': rej += 1; continue
        u = ITEMS[v['vattel_sec']]; seg = SEG[v['source_key']]
        hay = norm(u['text'] + ' ' + ' '.join(n['text'] for n in u['notes']))
        if norm(v['vattel_passage']) not in hay or norm(v['source_passage']) not in norm(seg['text']):
            bad.append(v['vattel_sec']); continue
        tid, fam = TEXT[v['source']]
        out.append({'unit': v['vattel_sec'], 'text': tid, 'locus': seg['locus'], 'sourceId': v['source_key'],
                    'relation': v['relation'], 'severity': v['severity'], 'question': v['question'], 'comment': v['comment'],
                    'passage': norm(v['vattel_passage']), 'sourcePassage': norm(v['source_passage']),
                    'confidence': v['confidence'], 'family': fam})
out.sort(key=lambda x: int(re.sub(r'\D', '', x['unit']) or 0))
doc = {'format': 'nle-layer-items/1', 'edition': 'vattel-defense-1741', 'layer': 'divergences', 'kind': 'comments',
       'description': 'Places where Vattel, defending Leibniz and Wolff, answers a question of the Théodicée or the Psychologia rationalis differently. Pairs from the units that reuse these sources, screened by Claude Sonnet (DEF41_DIV_SCREEN_PROMPT.md), kept or rejected by Claude Opus (DEF41_DIV_VERIFY_PROMPT.md). relation: diverges or partly. severity: 3 incompatible answers, 2 different ground or a changed scope, 1 a qualification. Disagreements with Crousaz and Roques are in the reuse rows (stance rejects). Machine judgements, not checked by hand.',
       'items': out}
json.dump(doc, open(os.path.join(ROOT, 'editions', 'vattel-defense-1741', 'provenance', 'divergences.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(out), 'kept', dict(Counter(x['relation'] for x in out)), dict(Counter(x['severity'] for x in out)), '; rejected', rej, '; passage not found', bad)
for x in out: print(' ', x['unit'], x['sourceId'], x['relation'], x['severity'], '|', x['comment'][:150])
