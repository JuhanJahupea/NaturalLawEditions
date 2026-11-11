# write_div.py <work> <screen dir> <verify dir> <text id> <out> [date]: kept verdicts -> divergence items (nle-pass/1) for the
# comments layer. Vattel's and the source's passages are placed exactly (or with free whitespace, or fuzzy >= 0.9) or the item is reported.
import sys, os, re, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
from merge_find import find
from corpus import unroman, roman
R = ROOT
B = WORK
work, sd, vd, tid, out = sys.argv[1:6]; date = sys.argv[6] if len(sys.argv) > 6 else '2026-11-11'
# per source: title for the locus, abbreviation for comments ("Grotius, DGP II.16.25"), family, copies, prologue name
WORKS = {'GRO24': {'title': 'Droit de la guerre et de la paix', 'abbr': 'DGP', 'family': 'G', 'prol': ('Discours préliminaire', 'Prol'),
                   'zot': {'GRO24T1': 'S9FQXVJC', 'GRO24T2': 'LL8RR8X3'},
                   'ia': {'GRO24T1': 'le-droit-de-la-guerre-t-1-grotius', 'GRO24T2': 'le-droit-de-la-guerre-t-2'},
                   'source': 'Grotius, Le droit de la guerre et de la paix, trad. Barbeyrac (Amsterdam 1724)'},
         'PUF34': {'title': 'Droit de la nature et des gens', 'abbr': 'DNG', 'family': 'P', 'prol': ('Préface du traducteur', 'Pref'),
                   'zot': {'PUF34T1': 'L42CQ82S', 'PUF34T2': 'S7XSE8FS'},
                   'ia': {'PUF34T1': 'ledroitdelanatur01pufe', 'PUF34T2': 'ledroitdelanatur02pufe'},
                   'source': 'Pufendorf, Le droit de la nature et des gens, trad. Barbeyrac (Amsterdam 1734)'}}
W = WORKS[work]
S = json.load(open(sd + '/sections.json'))
units = {u['id']: u for u in json.load(open('%s/editions/vattel-1773/text.json' % R))['units']}
P = {p['id']: p for p in json.load(open('%s/corpus/%s.json' % (B, work)))['pages']}
ins = {}
for f in sorted(glob.glob(vd + '/in/v*.json')):
    for it in json.load(open(f)): ins[(it['vattel_sec'], it['source_ref'])] = it
def sid(loc):
    m = re.match(r'Liv\. ([IVX]+) ch\. ([IVXL]+) § (\d+)', loc)
    if m: return '%s.%d.%d.%s' % (work, unroman(m.group(1)), unroman(m.group(2)), m.group(3))
    m = re.match(W['prol'][0] + r' § (\d+)', loc)
    return '%s.%s.%s' % (work, W['prol'][1], m.group(1)) if m else work + '.' + loc
def cite(loc):
    m = re.match(r'Liv\. ([IVX]+) ch\. ([IVXL]+) § (\d+)', loc)
    if m: return '%s, Liv. %s ch. %s § %s' % ((W['title'],) + m.groups())
    return '%s, %s' % (W['title'], loc)
def norm(c):
    # one citation form: book in roman, chapter and section in arabic ("DGP II.16.25")
    def fix(m):
        b, ch, sec = m.groups()
        b = roman(int(b)) if b.isdigit() else b
        ch = ch if ch.isdigit() else str(unroman(ch))
        return '%s %s.%s.%s' % (W['abbr'], b, ch, sec)
    return re.sub(W['abbr'] + r' (\d+|[IVX]+)\.(\d+|[IVXL]+)\.(\d+)', fix, c)
items = []; fails = collections.Counter(); order = list(units)
for f in sorted(glob.glob(vd + '/out/v*.json')):
    for v in json.load(open(f))['items']:
        if v.get('verdict') != 'keep': fails['rejected'] += 1; continue
        if float(v.get('confidence', 0)) < 0.5: fails['below 0.5'] += 1; continue
        key = (v['vattel_sec'], v['source_ref'])
        if key not in ins: fails['unknown pair'] += 1; continue
        u = units[v['vattel_sec']]
        vp = None
        for h in [u['text']] + [n['text'] for n in u.get('notes', [])]:
            r = find(h, v.get('vattel_passage', ''))
            if r: vp = h[r[0]:r[1]]; break
        if not vp: fails['vattel passage'] += 1; continue
        src = S['sec'][v['source_ref']]
        r = find(src, v.get('source_passage', ''))
        if not r: fails['source passage'] += 1; continue
        gp = src[r[0]:r[1]]
        pages = S['pages'][v['source_ref']]
        pg = next((p for p in pages if gp[:60] in P[p]['text']), pages[0])
        vol, scan = pg.split('.p'); scan = int(scan)
        items.append({'unit': u['id'], 'text': tid, 'locus': cite(v['source_ref']), 'sourceId': sid(v['source_ref']),
                      'relation': v['relation'], 'severity': int(v['severity']), 'question': ins[key]['screen']['question'],
                      'comment': norm(v['comment'].strip()), 'passage': vp, 'sourcePassage': gp,
                      'confidence': round(float(v['confidence']), 2), 'family': W['family'],
                      'links': [['Zotero p. %d' % scan, 'zotero://open-pdf/library/items/%s?page=%d' % (W['zot'][vol], scan)],
                                ['archive.org', 'https://archive.org/details/%s/page/n%d/mode/1up' % (W['ia'][vol], scan - 1)]]})
items.sort(key=lambda d: (order.index(d['unit']), -d['severity']))
json.dump({'format': 'nle-pass/1', 'edition': 'vattel-1773', 'text': tid, 'date': date,
           'source': W['source'] + ', from the transcription: pairs screened by one model, kept or rejected by a second',
           'items': items}, open(out, 'w'), ensure_ascii=False, indent=1)
print(len(items), 'items;', dict(collections.Counter(d['relation'] for d in items)), '; severity', dict(collections.Counter(d['severity'] for d in items)), '; dropped', dict(fails))
