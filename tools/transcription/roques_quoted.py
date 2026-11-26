# roques_quoted.py <WORK>/def41/data.json <reader output>...: Pierre Roques's letters on Leibniz's system (1737-1739), as
# Vattel quotes them in the Défense du système leibnitien (1741), Partie II ch. VIII. The letters themselves were not
# found; Vattel's quotations stand in for them. Readers (ROQUES_QUOTES_PROMPT.md) listed every passage of Roques with
# its exact words; each is placed here in the reading text of its unit (exact, or fuzzy at 0.9 or more), and written to
# texts/roques-lettres-1737-1739/ROQ.json (format nle-quoted/1).
import sys, os, re, json, html, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
DATA, OUTS = sys.argv[1], sys.argv[2:]
LETTERS = {1: {'title': 'Première lettre à M. Ruchat', 'journal': 'Mercure suisse', 'issue': 'décembre 1737'},
           2: {'title': 'Seconde lettre à M. Ruchat', 'journal': 'Journal helvétique', 'issue': 'janvier 1738'},
           3: {'title': 'Lettre à M. Bourguet', 'journal': 'Journal helvétique', 'issue': 'novembre 1738'},
           4: {'title': 'Seconde lettre à M. Bourguet', 'journal': 'Journal helvétique', 'issue': 'février et mars 1739'},
           0: {'title': 'Lettres à M. Bourguet', 'journal': 'Journal helvétique', 'issue': 'novembre 1738, février et mars 1739'}}
U = {u['id']: u for u in json.load(open(DATA))['units']}
def reading(h):                                  # the unit's reading text: tags, page-break spans and entities resolved
    h = re.sub(r'<span class="pb"[^>]*>[^<]*</span>', ' ', h)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()
def clean(t):                                    # a reader's passage in the same form
    t = re.sub(r'\[p\. [^\]]*\]', ' ', t).replace('_', '')
    return re.sub(r'\s+', ' ', t).strip()
def place(needle, hay):
    i = hay.find(needle)
    if i >= 0: return i, i + len(needle), 1.0
    sm = difflib.SequenceMatcher(None, hay, needle, autojunk=False)
    best = (None, None, 0)
    for blk in sm.get_matching_blocks():
        if blk.size < 8: continue
        a = max(0, blk.a - blk.b); seg = hay[a:a + len(needle) + 20]
        r = difflib.SequenceMatcher(None, seg[:len(needle)], needle, autojunk=False).ratio()
        if r > best[2]: best = (a, a + len(needle), r)
    return best
out, miss = [], []
for f in OUTS:
    for p in json.load(open(f))['passages']:
        u = U[p['unit']]
        if p.get('where', 'text') == 'text': hay = reading(u['html'])
        else:
            mk = re.sub(r'note\s*', '', p['where']).strip()
            hay = ' '.join(reading(n['html']) for n in u['notes'] if n['mark'].replace(' ', '') == mk.replace(' ', '')) or ' '.join(reading(n['html']) for n in u['notes'])
        t = clean(p['text']); a, b, r = place(t, hay)
        if r < 0.9: miss.append((p['unit'], round(r, 2), t[:70])); continue
        L = int(p.get('letter') or 0)
        q = {'id': 'ROQ.%d' % (len(out) + 1), 'letter': L, **LETTERS[L], 'page': str(p.get('page') or ''),
             'resolved': bool(p.get('resolved')), 'kind': p.get('kind', 'verbatim'),
             'text': hay[a:b] if r == 1.0 else t,
             'at': {'unit': p['unit'], 'where': p.get('where', 'text'), 'start': a, 'end': b, 'match': round(r, 3)},
             'embedded': p.get('embedded') or []}
        if p.get('note'): q['note'] = p['note']
        out.append(q)
doc = {'format': 'nle-quoted/1', 'text': 'roques-lettres-1737-1739',
       'source': 'Pierre Roques, letters on Leibniz\'s system to Abraham Ruchat (Mercure suisse, Dec. 1737; Journal helvétique, Jan. 1738) and to Louis Bourguet (Journal helvétique, Nov. 1738, Feb. and Mar. 1739), as quoted by Vattel, Défense du système leibnitien (1741), Partie II ch. VIII. The journals were not available; these passages stand in for the letters.',
       'letters': {str(k): v for k, v in LETTERS.items() if k},
       'passages': out}
d = os.path.join(ROOT, 'texts', 'roques-lettres-1737-1739'); os.makedirs(d, exist_ok=True)
json.dump(doc, open(os.path.join(d, 'ROQ.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(out), 'passages placed;', dict(Counter(q['kind'] for q in out)), dict(Counter(q['letter'] for q in out)),
      sum(1 for q in out if q['at']['match'] < 1), 'fuzzy;', sum(len(q['text'].split()) for q in out), 'words')
print('not placed:', len(miss)); [print('  ', m) for m in miss]
