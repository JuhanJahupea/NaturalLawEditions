# essai_merge.py <work> <dir> <date> [--write] [--only K,K]: the rows the Essai reuse readers wrote (ESSAI_REUSE_PROMPT.md,
# ESSAI_WOLFF2_PROMPT.md; <dir>/out/*.json) -> one pass file per source text (editions/vattel-essai-1747/passes/<text id>.json) and
# passes/attributions.json. --only: write the pass files of these sources only, and replace only their attributions.
# Each passage is placed on the unit's text or a note, each source passage on its page; locus, family, source part and links
# come from the page. Rows that fail are reported and left out; duplicates (same unit, page and passages) are merged.
import sys, os, re, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
from merge_find import find
S, d, date = sys.argv[1:4]; WRITE = '--write' in sys.argv
ONLY = set(sys.argv[sys.argv.index('--only') + 1].split(',')) if '--only' in sys.argv else None
R = ROOT; ED = 'vattel-essai-1747'
units = {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (R, ED)))['units']}
TID = {'PPU1': 'wolff-philosophia-practica-1738', 'DEV56': 'pufendorf-devoirs-barbeyrac-1756', 'PUF34': 'pufendorf-barbeyrac-1734',
       'GRO24': 'grotius-barbeyrac-1724', 'BUR47': 'burlamaqui-1747', 'TN1': 'wolff-theologia-naturalis-1739', 'LOG40': 'wolff-discursus-praeliminaris-1740'}
BASE = {'PPU1': 1000, 'DEV56': 2000, 'PUF34': 3000, 'GRO24': 4000, 'BUR47': 5000, 'TN1': 6000, 'LOG40': 7000}
WOLFF = {'PPU1': 'bsb10008634', 'TN1': 'bsb10008642', 'LOG40': 'bsb10008633'}
WORK = {'PPU1': 'Wolff, Philosophia practica universalis I (1738)', 'DEV56': "Pufendorf, Devoirs de l'homme et du citoyen (Barbeyrac 1756)",
        'PUF34': 'Pufendorf-Barbeyrac, Le droit de la nature et des gens (1734)', 'GRO24': 'Grotius-Barbeyrac, Le droit de la guerre et de la paix (1724)',
        'BUR47': 'Burlamaqui, Principes du droit naturel (1747)', 'TN1': 'Wolff, Theologia naturalis I (1739)',
        'LOG40': 'Wolff, Discursus praeliminaris de philosophia in genere (1740)'}
LAYER = {'PPU1': 'Vision transcription of the MDZ scans of the Halle 1744 issue (bsb10008634), which keeps the setting of 1738 (texts/wolff-philosophia-practica-1738/).',
         'DEV56': 'Vision transcription of the archive.org scans (texts/pufendorf-devoirs-barbeyrac-1756/).',
         'PUF34': 'Vision transcription of the archive.org scans (texts/pufendorf-barbeyrac-1734/).',
         'GRO24': 'Vision transcription of the archive.org scans (texts/grotius-barbeyrac-1724/).',
         'BUR47': 'The burlamaqui-1747 edition (editions/burlamaqui-1747/text.json).',
         'TN1': 'Vision transcription of the MDZ scans (bsb10008642), §§ 948-1006 (texts/wolff-theologia-naturalis-1739/).',
         'LOG40': 'Vision transcription of the MDZ scans (bsb10008633), §§ 1-171 (texts/wolff-discursus-praeliminaris-1740/).'}
ZOT = {'GRO24T1': 'S9FQXVJC', 'GRO24T2': 'LL8RR8X3', 'PUF34T1': 'L42CQ82S', 'PUF34T2': 'S7XSE8FS'}
IA = {'GRO24T1': 'le-droit-de-la-guerre-t-1-grotius', 'GRO24T2': 'le-droit-de-la-guerre-t-2', 'PUF34T1': 'ledroitdelanatur01pufe',
      'PUF34T2': 'ledroitdelanatur02pufe', 'DEV56T1': 'bub_gb_dDKCHraV9BoC', 'DEV56T2': 'bub_gb_unXpgRJJud0C'}
AUTH = {'GRO24': 'G', 'PUF34': 'P', 'DEV56': 'P'}
PARTS = [("Jugement d'un anonyme", 'Lz', 'jugement'), ('Réflexions du traducteur', 'Bb', 'reflexions'), ('Discours', 'Bb', 'discours'),
         ("Préface de l'auteur", 'P', 'pufendorf_preface'), ('Préface du traducteur', 'Bb', 'barbeyrac_preface'),
         ('Avertissement', 'Bb', 'barbeyrac_preface'), ('Avis postérieur', 'Bb', 'barbeyrac_preface')]
LABELS = {'translation', 'verbatim', 'close paraphrase', 'loose paraphrase', 'shared argument', 'citation', 'open disagreement'}
ROMAN = lambda n: ['', 'I', 'II', 'III'][n]
def roman(n):
    out = ''
    for v, s in ((100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')):
        while n >= v: out += s; n -= v
    return out

PG = {}
for k in WOLFF: PG.update({p['id']: (k, p) for p in json.load(open('%s/srcp/%s.json' % (S, k)))['pages']})
for k in ('DEV56', 'PUF34', 'GRO24'): PG.update({p['id']: (k, p) for p in json.load(open('%s/corpus/%s.json' % (S, k)))['pages']})
BUR = {u['id']: u for u in json.load(open(R + '/editions/burlamaqui-1747/text.json'))['units']}

def place(u, passage):
    for p, h in [('t', u['text'])] + [('n%d' % i, n['text']) for i, n in enumerate(u.get('notes', []))]:
        f = find(h, passage)
        if f: return [[p, f[0], f[1]]], h[f[0]:f[1]]
    return None, None

def part_fam(k, locus, by, note):
    if k == 'DEV56':
        for pre, fam, sp in PARTS:
            if locus.startswith(pre): return fam, sp
    if note and by != 'author': return 'Bb', 'barbeyrac_note' if k == 'DEV56' else None
    return AUTH[k], None

def source(k, page, sp):
    """(locus, family, sourcePart, inNote, quoted text, page id) or None."""
    if k == 'BUR47':
        u = BUR.get(page)
        if not u: return None
        for part, h in [('t', u['text'])] + [('n', n['text']) for n in u.get('notes', [])]:
            f = find(h, sp)
            if f:
                scan = u['pages'][0]['scan']
                for b in u.get('pb', []):
                    if part == 't' and b[0] <= f[0]: scan = b[2]
                m = re.match(r'P(\d)\.(\d+)\.(\d+)$', u['id'])
                loc = 'Part. %s ch. %s § %s' % (ROMAN(int(m.group(1))), roman(int(m.group(2))), m.group(3)) if m else u['id']
                return loc, 'Bu', None, part == 'n', h[f[0]:f[1]], 'BUR47.p%d' % scan
        return None
    pg = PG.get(page)
    if not pg or pg[0] != k: return None
    p = pg[1]
    if k in WOLFF:
        f = find(p['text'], sp)
        if f:
            par = p['carried']
            for off, n in p['starts']:
                if off <= f[0] + 3: par = n
            return ('§ %s' % par if par else ''), 'W', None, False, p['text'][f[0]:f[1]], page
        for m in p['margin']:
            g = find(m, sp)
            if g:
                n = re.match(r'§\.?\s*(\d+)', m); return ('§ %s' % n.group(1) if n else ''), 'W', None, False, m[g[0]:g[1]], page
        return None
    for a, b, loc in p['spans']:
        f = find(p['text'][a:b], sp)
        if f:
            fam, part = part_fam(k, loc, '', False); return loc, fam, part, False, p['text'][a + f[0]:a + f[1]], page
    f = find(p['text'], sp)
    if f:
        loc = next((l for a, b, l in p['spans'] if a <= f[0] < b), p['spans'][0][2] if p['spans'] else '')
        fam, part = part_fam(k, loc, '', False); return loc, fam, part, False, p['text'][f[0]:f[1]], page
    for n in p['notes']:
        f = find(n['text'], sp)
        if f:
            fam, part = part_fam(k, n['locus'], n['by'], True); return n['locus'], fam, part, True, n['text'][f[0]:f[1]], page
    for m in p['margin']:
        f = find(m['text'], sp)
        if f:
            fam, part = part_fam(k, m['locus'], 'author', False); return m['locus'], fam, part, False, m['text'][f[0]:f[1]], page
    return None

def links(k, page):
    if k in WOLFF:
        c = int(page.split('.pdf')[1]); return [['MDZ scan %d' % c, 'https://www.digitale-sammlungen.de/en/view/%s?page=%d' % (WOLFF[k], c)]]
    if k == 'BUR47':
        s = int(page.split('.p')[1]); return [['Zotero p. %d' % s, 'zotero://open-pdf/library/items/XKNMUHV3?page=%d' % s]]
    vol, scan = page.split('.p'); scan = int(scan)
    out = [['Zotero p. %d' % scan, 'zotero://open-pdf/library/items/%s?page=%d' % (ZOT[vol], scan)]] if vol in ZOT else []
    return out + [['archive.org', 'https://archive.org/details/%s/page/n%d/mode/1up' % (IA[vol], scan - 1)]]

rows = collections.defaultdict(list); attrs = []; fails = collections.Counter(); failed = []; seen = set()
items = [r for f in sorted(glob.glob(d + '/out/*.json')) for r in json.load(open(f)).get('rows', [])]
for it in items:
    k = it.get('text'); u = units.get(it.get('unit'))
    lab = (it.get('label') or '').strip().lower()
    if lab == 'quotation': lab = 'verbatim'
    if k not in TID or not u or (ONLY and k not in ONLY): fails['text or unit'] += 1; failed.append(it); continue
    if lab not in LABELS: fails['label'] += 1; failed.append(it); continue
    at, vp = place(u, it.get('passage', ''))
    if at is None: fails['passage'] += 1; failed.append(it); continue
    s = source(k, it.get('page', ''), it.get('source_passage', ''))
    if not s: fails['source'] += 1; failed.append(it); continue
    loc, fam, part, innote, sp, page = s; conf = round(float(it.get('confidence', 0)), 2)
    if conf < 0.3: fails['below 0.3'] += 1; continue
    key = (u['id'], page, vp, sp)
    if key in seen: fails['duplicate'] += 1; continue
    seen.add(key)
    row = {'unit': u['id'], 'at': at, 'family': fam, 'work': WORK[k], 'locus': loc, 'page': page, 'inNote': innote, 'label': lab,
           'confidence': conf, 'status': 'match' if conf >= 0.5 else 'possible', 'step': 'R', 'passage': vp, 'source': sp}
    if k in WOLFF and it.get('french'): row['french'] = it['french']
    row['reason'] = it.get('reason', ''); row['links'] = links(k, page)
    if part: row['sourcePart'] = part
    rows[k].append(row)
    nm = it.get('named')
    if isinstance(nm, dict) and nm.get('cue'):
        cue = nm['cue']; part_of = next((p for p, h in [('t', u['text'])] + [('n%d' % i, n['text']) for i, n in enumerate(u.get('notes', []))] if cue in h), None)
        if part_of and nm.get('form') in ('quotation', 'reference'):
            attrs.append({'text': TID[k], 'unit': u['id'], 'page': page, 'passage': vp, 'source': sp, 'form': nm['form'], 'cue': cue, 'cuePart': part_of,
                          'confidence': conf, 'reason': it.get('reason', '')})
        else: fails['attribution cue not found'] += 1
order = {uid: i for i, uid in enumerate(units)}
print(len(items), 'items;', {k: len(v) for k, v in rows.items()}, 'attributions', len(attrs))
print('status', collections.Counter((k, r['status']) for k, v in rows.items() for r in v))
print('labels', collections.Counter(r['label'] for v in rows.values() for r in v))
print('failed', dict(fails))
for it in failed[:10]: print('  FAIL', it.get('unit'), it.get('text'), it.get('page'), (it.get('passage') or '')[:50], '|', (it.get('source_passage') or '')[:50])
if WRITE:
    pdir = '%s/editions/%s/passes' % (R, ED); os.makedirs(pdir, exist_ok=True)
    for k, rs in rows.items():
        rs.sort(key=lambda r: (order[r['unit']], r['at'][0][0], r['at'][0][1]))
        rs = [dict({'id': BASE[k] + i}, **r) for i, r in enumerate(rs)]
        P = {'format': 'nle-pass/1', 'edition': ED, 'text': TID[k], 'date': date, 'textLayer': LAYER[k],
             'table': {'pass': 'editions/%s/passes/%s.json' % (ED, TID[k]), 'steps': {'R': 'Reading pass: Claude Opus read each section of the Essai with the source and wrote the rows'},
                       'description': 'Reuse of the source in the edition, found by Claude Opus reading the whole edition with the source (candidate pages by vocabulary for the French sources; Wolff searched by the reader). '
                                      'status match: confidence >= 0.5; possible: 0.3-0.5. Source passages are quoted from the transcription (long s as s, line-end hyphens joined).',
                       'sourceLabel': 'source (transcription)'},
             'rows': rs}
        json.dump(P, open('%s/%s.json' % (pdir, TID[k]), 'w'), ensure_ascii=False, indent=1)
    if ONLY:
        keep = [a for a in json.load(open('%s/attributions.json' % pdir))['attributions'] if a['text'] not in {TID[k] for k in ONLY}]
        attrs = keep + attrs
    json.dump({'format': 'nle-pass/1', 'edition': ED, 'date': date,
               'description': 'Rows where Vattel names the source for the passage, as the reuse readers marked them: form quotation or reference; cue is Vattel\'s words that name the source, in part cuePart.',
               'attributions': attrs}, open('%s/attributions.json' % pdir, 'w'), ensure_ascii=False, indent=1)
    json.dump(failed, open('%s/ess_failed.json' % S, 'w'), ensure_ascii=False, indent=1)
    print('written')
