# essai_div_write.py <screen dir> <verify dir> <date> [--write]: the kept verdicts of the Essai divergence verify step ->
# editions/vattel-essai-1747/passes/divergences-<text id>.json (nle-pass/1, items of the comments layer). Vattel's and the
# source's passages are placed exactly (or with free whitespace, or fuzzy >= 0.9) or the item is reported. A source passage
# in a note gets the note's locus, and Barbeyrac's family and name when the note is his; Leibniz's Jugement and Barbeyrac's
# Réflexions get theirs.
import sys, os, re, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
from merge_find import find
from corpus import unroman
sd, vd, date = sys.argv[1:4]; WRITE = '--write' in sys.argv
ED = 'vattel-essai-1747'
TID = {'PPU1': 'wolff-philosophia-practica-1738', 'TN1': 'wolff-theologia-naturalis-1739', 'LOG40': 'wolff-discursus-praeliminaris-1740',
       'PUF34': 'pufendorf-barbeyrac-1734', 'DEV56': 'pufendorf-devoirs-barbeyrac-1756', 'GRO24': 'grotius-barbeyrac-1724', 'BUR47': 'burlamaqui-1747'}
TITLE = {'PPU1': 'Philosophia practica universalis I', 'TN1': 'Theologia naturalis I', 'LOG40': 'Discursus praeliminaris',
         'PUF34': 'Droit de la nature et des gens', 'DEV56': "Devoirs de l'homme et du citoyen", 'GRO24': 'Droit de la guerre et de la paix',
         'BUR47': 'Principes du droit naturel'}
FAM = {'PPU1': 'W', 'TN1': 'W', 'LOG40': 'W', 'PUF34': 'P', 'DEV56': 'P', 'GRO24': 'G', 'BUR47': 'Bu'}
MDZ = {'PPU1': 'bsb10008634', 'TN1': 'bsb10008642', 'LOG40': 'bsb10008633'}
ZOT = {'GRO24T1': 'S9FQXVJC', 'GRO24T2': 'LL8RR8X3', 'PUF34T1': 'L42CQ82S', 'PUF34T2': 'S7XSE8FS', 'BUR47': 'XKNMUHV3'}
IA = {'GRO24T1': 'le-droit-de-la-guerre-t-1-grotius', 'GRO24T2': 'le-droit-de-la-guerre-t-2', 'PUF34T1': 'ledroitdelanatur01pufe',
      'PUF34T2': 'ledroitdelanatur02pufe', 'DEV56T1': 'bub_gb_dDKCHraV9BoC', 'DEV56T2': 'bub_gb_unXpgRJJud0C'}
SOURCE = {'PPU1': 'Wolff, Philosophia practica universalis, pars prior (Frankfurt and Leipzig 1738)',
          'TN1': 'Wolff, Theologia naturalis, pars prior (Frankfurt and Leipzig 1739)',
          'LOG40': 'Wolff, Discursus praeliminaris de philosophia in genere (Frankfurt and Leipzig 1740)',
          'PUF34': 'Pufendorf, Le droit de la nature et des gens, trad. Barbeyrac (Amsterdam 1734), with his notes',
          'DEV56': "Pufendorf, Les devoirs de l'homme et du citoyen, trad. Barbeyrac (1756), with Leibniz's Jugement and Barbeyrac's Réflexions",
          'GRO24': 'Grotius, Le droit de la guerre et de la paix, trad. Barbeyrac (Amsterdam 1724), with his notes',
          'BUR47': 'Burlamaqui, Principes du droit naturel (Genève 1747), the burlamaqui-1747 edition'}
SEC = json.load(open(sd + '/sections.json'))
units = {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (ROOT, ED)))['units']}
order = list(units)
PG = {}
for c in ('PPU1', 'TN1', 'LOG40'):
    for p in json.load(open('%s/srcp/%s.json' % (WORK, c)))['pages']: PG[p['id']] = p['text']
for c in ('PUF34', 'DEV56', 'GRO24'):
    for p in json.load(open('%s/corpus/%s.json' % (WORK, c)))['pages']: PG[p['id']] = p['text'] + ' ' + ' '.join(n['text'] for n in p['notes'])
BU = {u['id']: u for u in json.load(open(ROOT + '/editions/burlamaqui-1747/text.json'))['units']}
def notes_of(s):
    """the notes of a source section: [(mark, who, text)]"""
    pat = r'\[([^,\]]+), (author|Barbeyrac)\] ' if s['code'] != 'BUR47' else r'\[([^\]]+)\] '
    parts = re.split(pat, s['notes'])
    if s['code'] == 'BUR47': return [(parts[i], 'author', parts[i + 1].strip()) for i in range(1, len(parts) - 1, 2)]
    return [(parts[i], parts[i + 1], parts[i + 2].strip()) for i in range(1, len(parts) - 2, 3)]
def part_of(loc):
    if loc.startswith("Jugement d'un anonyme"): return 'Lz', 'Leibniz'
    if loc.startswith(('Réflexions du traducteur', 'Préface du traducteur', 'Avertissement')): return 'Bb', 'Barbeyrac'
    return None, None
def sid(c, loc):
    m = re.match(r'Liv\. ([IVX]+) ch\. ([IVXL]+) § (\d+)', loc)
    if m: return '%s.%d.%d.%s' % (c, unroman(m.group(1)), unroman(m.group(2)), m.group(3))
    m = re.match(r'Part\. ([IVX]+) ch\. ([IVXL]+) § (\d+)', loc)
    if m: return '%s.P%d.%d.%s' % (c, unroman(m.group(1)), unroman(m.group(2)), m.group(3))
    m = re.match(r'§ (\d+)$', loc)
    if m: return '%s.%s' % (c, m.group(1))
    ab = {"Jugement d'un anonyme": 'Jug', 'Réflexions du traducteur': 'Refl', "Préface de l'auteur": 'Pref', 'Préface du traducteur': 'TrPref',
          'Discours préliminaire': 'Prol'}
    m = re.match(r'(.+?) § (\d+)$', loc)
    return '%s.%s.%s' % (c, ab.get(m.group(1), m.group(1)), m.group(2)) if m else c + '.' + loc
def page_of(s, gp):
    if s['code'] == 'BUR47':
        u = BU[s['unit']]; at = u['text'].find(gp[:60]); scan = u['pages'][0]['scan']
        for o, vol, sc, pr in u.get('pb', []):
            if at >= o: scan = sc
        return 'BUR47.p%d' % scan
    return next((p for p in s['pages'] if gp[:60] in PG.get(p, '')), s['pages'][0])
def links(c, pg):
    if c in MDZ:
        n = int(pg.split('pdf')[1]); return [['MDZ scan %d' % n, 'https://www.digitale-sammlungen.de/en/view/%s?page=%d' % (MDZ[c], n)]]
    vol, scan = pg.split('.p'); scan = int(scan); out = []
    if vol in ZOT: out.append(['Zotero p. %d' % scan, 'zotero://open-pdf/library/items/%s?page=%d' % (ZOT[vol], scan)])
    if vol in IA: out.append(['archive.org', 'https://archive.org/details/%s/page/n%d/mode/1up' % (IA[vol], scan - 1)])
    return out
ins = {}
for f in sorted(glob.glob(vd + '/in/v*.json')):
    for it in json.load(open(f)): ins[(it['vattel_sec'], it['source'], it['source_ref'])] = it
items = collections.defaultdict(list); fails = collections.Counter(); seen = set()
for f in sorted(glob.glob(vd + '/out/v*.json')):
    for v in json.load(open(f))['items']:
        if v.get('verdict') != 'keep': fails['rejected'] += 1; continue
        if float(v.get('confidence', 0)) < 0.5: fails['below 0.5'] += 1; continue
        key = (v['vattel_sec'], v['source'], v['source_ref'])
        if key not in ins or key in seen: fails['unknown or repeated pair'] += 1; continue
        seen.add(key); u = units[v['vattel_sec']]; s = SEC['%s|%s' % (v['source'], v['source_ref'])]
        vp = None
        for h in [u['text']] + [n['text'] for n in u.get('notes', [])]:
            r = find(h, v.get('vattel_passage', ''))
            if r: vp = h[r[0]:r[1]]; break
        if not vp: fails['vattel passage'] += 1; continue
        fam, author = part_of(s['locus']); loc = s['locus']; gp = None
        r = find(s['text'], v.get('source_passage', ''))
        if r: gp = s['text'][r[0]:r[1]]
        else:
            for mark, who, nt in notes_of(s):
                r = find(nt, v.get('source_passage', ''))
                if r:
                    gp = nt[r[0]:r[1]]; loc = '%s, n. %s' % (s['locus'], re.sub(r'\D', '', mark) or mark)
                    if who == 'Barbeyrac': fam, author = 'Bb', 'Barbeyrac'
                    break
        if not gp: fails['source passage'] += 1; continue
        pg = page_of(s, gp); c = v['source']
        it = {'unit': u['id'], 'text': TID[c], 'locus': loc if author in ('Leibniz', 'Barbeyrac') and not loc.startswith('Liv.') and c == 'DEV56' else '%s, %s' % (TITLE[c], loc),
              'sourceId': sid(c, s['locus']) + ('.n' + loc.split(', n. ')[1] if ', n. ' in loc else ''),
              'relation': v['relation'], 'severity': int(v['severity']), 'question': (v.get('question') or ins[key]['screen']['question']).strip(),
              'comment': v['comment'].strip(), 'passage': vp, 'sourcePassage': gp, 'confidence': round(float(v['confidence']), 2),
              'family': fam or FAM[c], 'links': links(c, pg)}
        if author: it['author'] = author
        items[c].append(it)
tot = 0
for c, its in items.items():
    its.sort(key=lambda d: (order.index(d['unit']), -d['severity'])); tot += len(its)
    P = {'format': 'nle-pass/1', 'edition': ED, 'text': TID[c], 'date': date,
         'source': SOURCE[c] + ', from the transcription: pairs screened by one model, kept or rejected by a second', 'items': its}
    print(c, len(its), dict(collections.Counter(d['relation'] for d in its)), 'families', dict(collections.Counter(d['family'] for d in its)))
    if WRITE: json.dump(P, open('%s/editions/%s/passes/divergences-%s.json' % (ROOT, ED, TID[c]), 'w'), ensure_ascii=False, indent=1)
print(tot, 'items; dropped', dict(fails))
