# add_merge.py <work> <first id> <date> <out> <kind:dir> [<kind:dir> ...] [--append]: rows written by the additions readers
# (ADD_PROMPT.md, kind A: dir/out/*.json {"rows"}), the recall readers (RECALL_PROMPT.md, kind C: rows found and not covered)
# the readers of the 1773 additions (ADDITIONS_1773_PROMPT.md, kind V: items[].found, rows not covered) and the full pass
# (FULL_PASS_PROMPT.md, kind F: as kind C) -> rows of
# editions/vattel-1773/passes/additions.json. --append: keep the rows <out> already has and add the new ones after them. Each passage is placed on the unit's text, notes or margin, each source passage
# on its page; the locus, family, page and links come from the page. Rows that fail, and rows a table already has, are reported.
import sys, os, re, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK
from merge_find import find
R = ROOT
S, first, date, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
APPEND = '--append' in sys.argv
srcs = [a.split(':', 1) for a in sys.argv[5:] if not a.startswith('--')]
ED = 'vattel-1773'
units = {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (R, ED)))['units']}
TABLE = {'JG': 'wolff-jus-gentium-1749', 'INST': 'wolff-institutiones-1750', 'GRO24': 'grotius-barbeyrac-1724', 'PUF34': 'pufendorf-barbeyrac-1734',
         'BUR47': 'burlamaqui-1747'}
WORK = {'JG': 'Wolff, Jus gentium (1749)', 'INST': 'Wolff, Institutiones (1750)',
        'GRO24': 'Grotius-Barbeyrac, Le droit de la guerre et de la paix (1724)', 'PUF34': 'Pufendorf-Barbeyrac, Le droit de la nature et des gens (1734)',
        'BUR47': 'Burlamaqui, Principes du droit naturel (1747)'}
PDF = {'JG': 'Ius_Gentium_Methodo_Scientifica_Pertract.pdf', 'INST': 'Institutiones_juris_naturae_et_gentium_i.pdf'}
ZOT = {'GRO24T1': 'S9FQXVJC', 'GRO24T2': 'LL8RR8X3', 'PUF34T1': 'L42CQ82S', 'PUF34T2': 'S7XSE8FS'}
IA = {'GRO24T1': 'le-droit-de-la-guerre-t-1-grotius', 'GRO24T2': 'le-droit-de-la-guerre-t-2', 'PUF34T1': 'ledroitdelanatur01pufe', 'PUF34T2': 'ledroitdelanatur02pufe'}
AUTH = {'GRO24': 'G', 'PUF34': 'P'}
LABELS = {'translation', 'verbatim', 'close paraphrase', 'loose paraphrase', 'shared argument', 'citation', 'open disagreement'}
PG = {}
for k in ('JG', 'INST'): PG.update({p['id']: (k, p) for p in json.load(open('%s/srcp/%s.json' % (S, k)))['pages']})
for k in ('GRO24', 'PUF34'): PG.update({p['id']: (k, p) for p in json.load(open('%s/corpus/%s.json' % (S, k)))['pages']})
# Wolff's Praefatio and Prolegomena from the second copy (texts/wolff-jus-gentium-1749/WJG_praef_prol.json): a page per unit, read with
# long s as s, italics dropped and line breaks as spaces (the form of the table's Praefatio rows); page ids WJG.Praef.<n> name the Praefatio
for u in json.load(open(R + '/texts/wolff-jus-gentium-1749/WJG_praef_prol.json'))['units']:
    t = re.sub(r' +', ' ', re.sub(r'</?i>', '', u['text'].replace('ſ', 's')).replace('\n', ' ')).strip()
    PG[u['id']] = ('JG', {'id': u['id'], 'text': t, 'margin': [], 'starts': [], 'carried': None, 'wjg': u['part'], 'para': u['para']})
# Burlamaqui: the burlamaqui-1747 edition; a page is a unit id (P1.6.9)
ROMAN = lambda n: ['', 'I', 'II', 'III', 'IV'][n]
def roman(n):
    out = ''
    for v, r in ((10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')):
        while n >= v: out += r; n -= v
    return out
for u in json.load(open(R + '/editions/burlamaqui-1747/text.json'))['units']: PG[u['id']] = ('BUR47', u)

def bur_source(u, sp):
    """(locus, family, inNote, quoted text, page id) of a passage of a Burlamaqui unit, or None."""
    for part, h in [('t', u['text'])] + [('n', n['text']) for n in u.get('notes', [])]:
        f = find(h, sp)
        if f:
            scan = u['pages'][0]['scan']
            for b in u.get('pb', []):
                if part == 't' and b[0] <= f[0]: scan = b[2]
            m = re.match(r'P(\d)\.(\d+)\.(\d+)$', u['id'])
            loc = 'Liv. %s ch. %s § %s' % (ROMAN(int(m.group(1))), roman(int(m.group(2))), m.group(3)) if m else u['id']
            return loc, 'Bu', part == 'n', h[f[0]:f[1]], 'BUR47.p%d' % scan
    return None

def place(u, passage):
    for p, h in [('t', u['text'])] + [('n%d' % i, n['text']) for i, n in enumerate(u.get('notes', []))]:
        f = find(h, passage)
        if f: return [[p, f[0], f[1]]], h[f[0]:f[1]]
    f = find(u.get('margin', ''), passage)
    if f: return [], u['margin'][f[0]:f[1]]
    return None, None

def source(k, p, sp):
    """(locus, family, inNote, quoted text) of a source passage on its page, or None."""
    if p.get('wjg'):
        f = find(p['text'], sp)
        return (('Prolegomena §. %d' % p['para']) if p['wjg'] == 'Prol' else '', 'W', False, p['text'][f[0]:f[1]]) if f else None
    if k in ('JG', 'INST'):
        f = find(p['text'], sp)
        if not f:
            for m in p['margin']:
                g = find(m, sp)
                if g:
                    n = re.match(r'§\.?\s*(\d+)', m)
                    return ('§ %s' % n.group(1) if n else ''), 'W', False, m[g[0]:g[1]]
            return None
        par = p['carried']
        for off, n in p['starts']:
            if off <= f[0] + 3: par = n
        return '§ %s' % par if par else '', 'W', False, p['text'][f[0]:f[1]]
    for a, b, loc in p['spans']:
        f = find(p['text'][a:b], sp)
        if f: return loc, AUTH[k], False, p['text'][a + f[0]:a + f[1]]
    f = find(p['text'], sp)
    if f:
        loc = next((l for a, b, l in p['spans'] if a <= f[0] < b), p['spans'][0][2] if p['spans'] else '')
        return loc, AUTH[k], False, p['text'][f[0]:f[1]]
    for n in p['notes']:
        f = find(n['text'], sp)
        if f: return n['locus'], (AUTH[k] if n['by'] == 'author' else 'Bb'), True, n['text'][f[0]:f[1]]
    for m in p['margin']:
        f = find(m['text'], sp)
        if f: return m['locus'], AUTH[k], False, m['text'][f[0]:f[1]]
    return None

# rows the tables already have, by unit and table: spans, for duplicates
cat = json.load(open(R + '/catalogue.json')); have = collections.defaultdict(list)
for c in cat['reuse']:
    if c['from'] != ED or c['to'] not in TABLE.values(): continue
    for r in json.load(open(R + '/' + c['path']))['rows']:
        if r['status'] != 'rejected': have[(r['unit'], c['to'])].append(r)
def dup(row):
    for o in have[(row['unit'], TABLE[row['_k']])]:
        if o.get('page') == row['page'] and o['at'] and row['at'] and o['at'][0][0] == row['at'][0][0]:
            a, b = o['at'][0][1:]; c, d = row['at'][0][1:]
            if min(b, d) - max(a, c) > 0.5 * min(b - a, d - c): return o['id']
        if o.get('source') == row['source'] and o.get('passage') == row['passage']: return o['id']
    return None

items = []
for kind, d in srcs:
    for f in sorted(glob.glob(d + '/out/*.json')):
        O = json.load(open(f))
        if kind == 'A':
            for r in O.get('rows', []): items.append(dict(r, _from='A', _file=os.path.basename(f)))
        elif kind == 'V':
            for x in O.get('items', []):
                for r in x.get('found', []):
                    if r.get('covered_by') is None: items.append(dict(r, unit=r.get('unit', x['unit']), _from='V', _file=os.path.basename(f)))
        else:
            for s in O.get('sections', []):
                for r in s.get('found', []):
                    if r.get('covered_by') is None: items.append(dict(r, unit=r.get('unit', s['unit']), _from=kind, _file=os.path.basename(f)))
rows = []; fails = collections.Counter(); failed = []; dups = []
for it in items:
    k = it.get('text'); u = units.get(it.get('unit'))
    if k not in TABLE or not u: fails['text or unit'] += 1; failed.append(it); continue
    if it.get('label') not in LABELS: fails['label'] += 1; failed.append(it); continue
    at, vp = place(u, it.get('passage', ''))
    if at is None: fails['passage'] += 1; failed.append(it); continue
    pg = PG.get(it.get('page')) or (PG.get('WJG.Praef') if str(it.get('page', '')).startswith('WJG.Praef') else None)
    if not pg or pg[0] != k: fails['page'] += 1; failed.append(it); continue
    if k == 'BUR47':
        s = bur_source(pg[1], it.get('source_passage', ''))
        if s: s, bpage = s[:4], s[4]
    else: s = source(k, pg[1], it.get('source_passage', ''))
    if not s: fails['source'] += 1; failed.append(it); continue
    loc, fam, innote, sp = s; conf = round(float(it.get('confidence', 0)), 2)
    if conf < 0.3: fails['below 0.3'] += 1; continue
    p = pg[1]
    row = {'table': TABLE[k], 'unit': u['id'], 'at': at}
    if not at: row['where'] = 'margin'
    row.update({'family': fam, 'work': WORK[k], 'locus': loc, 'page': bpage if k == 'BUR47' else (it['page'] if p.get('wjg') else p['id']), 'inNote': innote, 'label': it['label'], 'confidence': conf,
                'status': 'match' if conf >= 0.5 else 'possible', 'step': it['_from'], 'passage': vp, 'source': sp})
    if k in ('JG', 'INST'):
        if it.get('french'): row['french'] = it['french']
        row['reason'] = it.get('reason', '')
        row['links'] = [] if p.get('wjg') else [['PDF p. %d' % p['scan'], 'file:///C:/PhD_library/vattel-reuse/sources/%s#page=%d' % (PDF[k], p['scan'])]]
    elif k == 'BUR47':
        row['reason'] = it.get('reason', ''); scan = int(bpage.split('.p')[1])
        row['links'] = [['Zotero p. %d' % scan, 'zotero://open-pdf/library/items/XKNMUHV3?page=%d' % scan]]
    else:
        row['reason'] = it.get('reason', '')
        vol, scan = p['id'].split('.p'); scan = int(scan)
        row['links'] = [['Zotero p. %d' % scan, 'zotero://open-pdf/library/items/%s?page=%d' % (ZOT[vol], scan)],
                        ['archive.org', 'https://archive.org/details/%s/page/n%d/mode/1up' % (IA[vol], scan - 1)]]
    row['_k'] = k
    o = dup(row)
    if o is not None: dups.append((it['_from'], u['id'], o)); continue
    if any(x['unit'] == row['unit'] and x['page'] == row['page'] and x['passage'] == row['passage'] for x in rows): dups.append((it['_from'], u['id'], 'same new row')); continue
    rows.append(row)
order = {u: i for i, u in enumerate(units)}
rows.sort(key=lambda r: (order[r['unit']], r['at'][0][0] if r['at'] else 'm', r['at'][0][1] if r['at'] else 0, r['table']))
for i, r in enumerate(rows): r.pop('_k'); r_id = first + i; rows[i] = dict({'id': r_id}, **r)
print(len(items), 'items;', len(rows), 'rows', collections.Counter((r['step'], r['table'], r['status']) for r in rows))
print('failed', dict(fails), '| duplicates', len(dups))
for it in failed[:12]: print('  FAIL', it['_from'], it['_file'], it.get('unit'), it.get('text'), it.get('page'), (it.get('passage') or '')[:60], '|', (it.get('source_passage') or '')[:60])
old = json.load(open(out))['rows'] if APPEND and os.path.exists(out) else []
if old: assert first > max(r['id'] for r in old)
rows = old + rows
P = {'format': 'nle-additions/1', 'edition': ED, 'date': date,
     'description': 'Rows added to the reuse tables after the audits, judged by Claude Opus on the transcriptions. Each row names its table.',
     'steps': {'A': 'Additions: the passage of Wolff or Grotius that an audit reader named as the one Vattel follows (audit/README.md)',
               'C': 'Recall check: reuse a reader found in a random sample of sections that no row covered (audit/README.md)',
               'F': 'Full pass: Claude Opus read every section with the §§ of the Jus gentium it follows and pages of Barbeyrac\'s Pufendorf, and wrote the reuse no row covered (audit/README.md)',
               'V': 'Reading of the passages added in 1773: Claude Opus read each addition (layer changes-1773) with Wolff, Grotius, Pufendorf and Burlamaqui (audit/README.md)'},
     'rows': rows}
json.dump(P, open(out, 'w'), ensure_ascii=False, indent=1)
json.dump(failed, open(out + '.failed.json', 'w'), ensure_ascii=False, indent=1)
