# write_div.py <screen dir> <verify dir> <text id> <out>: kept verdicts -> divergence items (nle-pass/1) for the comments layer.
# Vattel's and Grotius's passages are placed exactly (or with free whitespace, or fuzzy >= 0.9) or the item is reported.
import sys, os, re, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
from merge_find import find
from corpus import unroman, roman
R = ROOT
sd, vd, tid, out = sys.argv[1:5]
S = json.load(open(sd + '/sections.json'))
B = WORK
units = {u['id']: u for u in json.load(open('%s/editions/vattel-1773/text.json' % R))['units']}
P = {p['id']: p for p in json.load(open('%s/corpus/GRO24.json' % B))['pages']}
ZOT = {'GRO24T1': 'S9FQXVJC', 'GRO24T2': 'LL8RR8X3'}
IA = {'GRO24T1': 'le-droit-de-la-guerre-t-1-grotius', 'GRO24T2': 'le-droit-de-la-guerre-t-2'}
ins = {}
for f in sorted(glob.glob(vd + '/in/v*.json')):
    for it in json.load(open(f)): ins[(it['vattel_sec'], it['grotius_ref'])] = it
def sid(loc):
    m = re.match(r'Liv\. ([IVX]+) ch\. ([IVXL]+) § (\d+)', loc)
    if m: return 'GRO24.%d.%d.%s' % (unroman(m.group(1)), unroman(m.group(2)), m.group(3))
    m = re.match(r'Discours préliminaire § (\d+)', loc)
    return 'GRO24.Prol.%s' % m.group(1) if m else 'GRO24.' + loc
def cite(loc):
    m = re.match(r'Liv\. ([IVX]+) ch\. ([IVXL]+) § (\d+)', loc)
    if m: return 'Droit de la guerre et de la paix, Liv. %s ch. %s § %s' % m.groups()
    return 'Droit de la guerre et de la paix, ' + loc
def dgp(c):
    # one citation form: book in roman, chapter and section in arabic ("Grotius, DGP II.16.25")
    def fix(m):
        b, ch, sec = m.groups()
        b = roman(int(b)) if b.isdigit() else b
        ch = ch if ch.isdigit() else str(unroman(ch))
        return 'DGP %s.%s.%s' % (b, ch, sec)
    return re.sub(r'DGP (\d+|[IVX]+)\.(\d+|[IVXL]+)\.(\d+)', fix, c)
items = []; fails = collections.Counter(); order = list(units)
for f in sorted(glob.glob(vd + '/out/v*.json')):
    for v in json.load(open(f))['items']:
        if v.get('verdict') != 'keep': fails['rejected'] += 1; continue
        if float(v.get('confidence', 0)) < 0.5: fails['below 0.5'] += 1; continue
        key = (v['vattel_sec'], v['grotius_ref'])
        if key not in ins: fails['unknown pair'] += 1; continue
        u = units[v['vattel_sec']]
        vp = None
        for h in [u['text']] + [n['text'] for n in u.get('notes', [])]:
            r = find(h, v.get('vattel_passage', ''))
            if r: vp = h[r[0]:r[1]]; break
        if not vp: fails['vattel passage'] += 1; continue
        src = S['sec'][v['grotius_ref']]
        r = find(src, v.get('grotius_passage', ''))
        if not r: fails['grotius passage'] += 1; continue
        gp = src[r[0]:r[1]]
        pages = S['pages'][v['grotius_ref']]
        pg = next((p for p in pages if gp[:60] in P[p]['text']), pages[0])
        vol, scan = pg.split('.p'); scan = int(scan)
        items.append({'unit': u['id'], 'text': tid, 'locus': cite(v['grotius_ref']), 'sourceId': sid(v['grotius_ref']),
                      'relation': v['relation'], 'severity': int(v['severity']), 'question': ins[key]['screen']['question'],
                      'comment': dgp(v['comment'].strip()), 'passage': vp, 'sourcePassage': gp,
                      'confidence': round(float(v['confidence']), 2), 'family': 'G',
                      'links': [['Zotero p. %d' % scan, 'zotero://open-pdf/library/items/%s?page=%d' % (ZOT[vol], scan)],
                                ['archive.org', 'https://archive.org/details/%s/page/n%d/mode/1up' % (IA[vol], scan - 1)]]})
items.sort(key=lambda d: (order.index(d['unit']), -d['severity']))
json.dump({'format': 'nle-pass/1', 'edition': 'vattel-1773', 'text': tid, 'date': '2026-10-23', 'source': 'Grotius, Le droit de la guerre et de la paix, trad. Barbeyrac (Amsterdam 1724), from the transcription: pairs screened by one model, kept or rejected by a second',
           'items': items}, open(out, 'w'), ensure_ascii=False, indent=1)
print(len(items), 'items;', dict(collections.Counter(d['relation'] for d in items)), '; severity', dict(collections.Counter(d['severity'] for d in items)), '; dropped', dict(fails))
