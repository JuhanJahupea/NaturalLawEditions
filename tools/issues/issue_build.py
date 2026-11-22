# issue_build.py <tag dir> <issue id> [--write]: one issue's genealogy (issues/<id>.json) from the tagged candidates
# (issue_cand.py, ISSUE_TAG_PROMPT.md). Nodes are passages: a unit of an edition, or a § (or a note) of a source text.
# Edges run from the later passage to the earlier one: reuse rows (takes over, cites, rejects) and divergence notes
# (diverges, partly), each with its sub-issues, plus "note on" from a Barbeyrac note to the § it annotates when both are
# in the issue. Nodes sit in columns, one per text or part of a volume (Barbeyrac's notes, Leibniz's Jugement, his
# Réflexions), dated by first printing.
import os, sys, re, json, glob, collections
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
td, IID = sys.argv[1], sys.argv[2]; WRITE = '--write' in sys.argv
load = lambda p: json.load(open(os.path.join(ROOT, p), encoding='utf-8'))
cat = load('catalogue.json'); TX = {t['id']: t for t in cat['texts']}; ED = {e['id']: e for e in cat['editions']}
items = {it['key']: it for it in json.load(open(td + '/items.json'))}
tags = {t['key']: t for f in sorted(glob.glob(td + '/out/*.json')) for t in json.load(open(f))['items']}
SUBS = [('definition', 'What obligation is'), ('superior', "A superior's will"), ('utility', 'Utility and our own good'),
        ('reason', 'Reason and the nature of things'), ('god', 'Obligation without God'), ('self', 'Obliging oneself'),
        ('law', 'What a law is'), ('sanction', 'Rewards and punishments')]
# columns: a text, or a part of a volume; first printing, author
FIRST = {'grotius-barbeyrac-1724': 1625, 'pufendorf-barbeyrac-1734': 1672, 'pufendorf-devoirs-barbeyrac-1756': 1673,
         'wolff-discursus-praeliminaris-1740': 1728, 'wolff-theologia-naturalis-1739': 1736, 'wolff-philosophia-practica-1738': 1738,
         'burlamaqui-1747': 1747, 'vattel-essai-1747': 1747, 'vattel-1773': 1758, 'cicero-latin-library': -45, 'seneca-latin-library': 60,
         'digest-latin-library': 533, 'burlamaqui-elemens-1783': 1740}
SHORT = {'grotius-barbeyrac-1724': 'Grotius, DGP', 'pufendorf-barbeyrac-1734': 'Pufendorf, DNG', 'pufendorf-devoirs-barbeyrac-1756': 'Pufendorf, Devoirs',
         'wolff-discursus-praeliminaris-1740': 'Wolff, Disc. prael.', 'wolff-theologia-naturalis-1739': 'Wolff, TN I',
         'wolff-philosophia-practica-1738': 'Wolff, PPU I', 'burlamaqui-1747': 'Burlamaqui, Principes', 'vattel-essai-1747': 'Vattel, Essai',
         'vattel-1773': 'Vattel, Droit des gens', 'wolff-jus-gentium-1749': 'Wolff, Jus gentium', 'wolff-institutiones-1750': 'Wolff, Institutiones',
         'formey-principes-1758': 'Formey, Principes', 'burlamaqui-elemens-1783': 'Burlamaqui, Élémens (lectures; printed 1783)',
         'burlamaqui-droit-politique-1751': 'Burlamaqui, Droit politique'}
AUTHOR = {'G': 'Grotius', 'P': 'Pufendorf', 'Bb': 'Barbeyrac', 'Lz': 'Leibniz', 'W': 'Wolff', 'Bu': 'Burlamaqui', 'V': 'Vattel'}
def column(text, locus, fam):
    """(column key, label, date, author) of a source passage"""
    if text == 'pufendorf-devoirs-barbeyrac-1756':
        if locus.startswith("Jugement d'un anonyme"): return 'LzJ', "Leibniz, Jugement d'un anonyme", 1706, 'Leibniz'
        if locus.startswith('Réflexions du traducteur'): return 'BbR', 'Barbeyrac, Réflexions du traducteur', 1718, 'Barbeyrac'
        if fam == 'Bb' or ', n.' in locus: return 'BbOFF', "Barbeyrac's notes to the Devoirs", 1707, 'Barbeyrac'
    if text == 'pufendorf-barbeyrac-1734' and (fam == 'Bb' or ', n.' in locus or locus.startswith('Préface du traducteur')):
        return 'BbDNG', "Barbeyrac's notes and preface to the DNG", 1706, 'Barbeyrac'
    if text == 'grotius-barbeyrac-1724' and (fam == 'Bb' or ', n.' in locus):
        return 'BbDGP', "Barbeyrac's notes to the DGP", 1724, 'Barbeyrac'
    t = TX.get(text) or ED.get(text) or {}
    m = re.search(r'\d{4}', str(t.get('date', ''))); date = FIRST.get(text) or (int(m.group(0)) if m else 0)
    au = (t.get('authorShort') or str(t.get('author', text)).split(' and ')[0].split(' ')[-1])
    return text, SHORT.get(text, '%s, %s' % (au, t.get('title', text)[:40])), date, au
nodes, edges = {}, collections.defaultdict(lambda: {'n': 0, 'subs': set(), 'items': []})
units = {e: {u['id']: u for u in load('editions/%s/text.json' % e)['units']} for e in ('vattel-essai-1747', 'burlamaqui-1747', 'vattel-1773')}
unitlab = {e: load('editions/%s/edition.json' % e) for e in units}
ROM = {'I': 1, 'V': 5, 'X': 10, 'L': 50}
def unrom(s):
    v = 0
    for i, c in enumerate(s): x = ROM[c]; v += -x if i + 1 < len(s) and ROM[s[i + 1]] > x else x
    return v
def short(loc):
    m = re.match(r'(?:Liv|Part)\. ([IVX]+) ch\. ([IVXL]+) § (\d+)(?:, n\. (\S+))?', loc)
    if m: return '%s.%d.%s%s' % (m.group(1), unrom(m.group(2)), m.group(3), ' n. ' + m.group(4) if m.group(4) else '')
    loc = re.sub(r"^(Réflexions du traducteur|Jugement d'un anonyme) ", '', loc)
    loc = loc.replace('Discours préliminaire § ', 'Prol. ').replace('Préface du traducteur', 'Préface').replace("Préface de l'auteur", 'Préface')
    return loc
def ulabel(ed, uid):
    p = uid.split('.')
    if ed == 'burlamaqui-1747' and len(p) == 3: return '%s.%s § %s' % ('I' if p[0] == 'P1' else 'II', p[1], p[2])
    if ed == 'vattel-1773': return ('Prél. § ' + p[1]) if p[0] == 'Prelim' else ('Préf. p. ' + p[1]) if p[0] == 'Pref' else '%s § %s' % (p[0], p[-1])
    d = next((x for x in unitlab[ed]['divisions'] if x['key'] == uid.split('.')[0]), None); p = uid.split('.')
    return (d['unitLabel'].replace('{n}', p[-1]).replace('{chap}', p[1] if len(p) > 2 else '') if d else uid)
def ed_node(ed, uid):
    k = 'ed:%s#%s' % (ed, uid)
    if k not in nodes:
        u = units[ed][uid]; t = re.sub(r'\s+', ' ', u.get('text', '')).strip()
        col = {'vattel-essai-1747': ('vattel-essai-1747', 'Vattel, Essai', 1747, 'Vattel'), 'burlamaqui-1747': ('burlamaqui-1747', 'Burlamaqui, Principes', 1747, 'Burlamaqui'),
               'vattel-1773': ('vattel-1773', 'Vattel, Droit des gens', 1758, 'Vattel')}[ed]
        nodes[k] = {'id': k, 'col': col[0], 'label': ulabel(ed, uid), 'sort': list(units[ed]).index(uid), 'text': t[:220],
                    'link': '../viewer/?ed=%s#%s' % (ed, uid), 'subs': set(), '_col': col}
    return k
def loc_sort(loc):
    nums = [unrom(m) if not m.isdigit() else int(m) for m in re.findall(r'\b([IVXL]+|\d+)\b', loc)]
    return nums or [0]
def src_node(text, locus, fam, passage, link):
    c = column(text, locus, fam); k = 'src:%s|%s' % (c[0], locus)
    if k not in nodes:
        nodes[k] = {'id': k, 'col': c[0], 'label': short(locus), 'full': locus, 'sort': loc_sort(locus), 'text': re.sub(r'\s+', ' ', passage).strip()[:220],
                    'link': link, 'subs': set(), '_col': c}
    return k
REL = {'translation': 'takes', 'verbatim': 'quotes', 'close paraphrase': 'takes', 'loose paraphrase': 'takes', 'shared argument': 'takes',
       'citation': 'cites', 'open disagreement': 'rejects', 'diverges': 'diverges', 'partly': 'partly'}
rows = {}
for f in glob.glob(ROOT + '/reuse/*.json'):
    tb = json.load(open(f))
    for r in tb['rows']: rows['r:%s:%d' % (tb['from'], r['id'])] = (tb, r)
divs = {e: load('editions/%s/layers/divergences.json' % e)['items'] for e in units}
on = 0
for key, tg in tags.items():
    if not tg.get('on_issue') or key not in items: continue
    it = items[key]; sub = tg.get('sub') or ''; on += 1
    if it['kind'] == 'row':
        tb, r = rows[key]
        a = ed_node(tb['from'], r['unit'])
        if tb['to'] in units and r.get('toUnit'): b = ed_node(tb['to'], r['toUnit'])
        elif tb['to'] == 'vattel-loisir-1747' and re.match(r'§ ?\d+$', r.get('locus') or '') and 'E.' + re.sub(r'\D', '', r['locus']) in units['vattel-essai-1747']:
            b = ed_node('vattel-essai-1747', 'E.' + re.sub(r'\D', '', r['locus']))
        else: b = src_node(tb['to'], r.get('locus') or r.get('page', ''), r['family'], r['source'], (r.get('links') or [[None, '']])[0][1])
        rel = REL.get(r['label'], 'takes'); pa, sp, lab, conf = r['passage'], r['source'], r['label'], r['confidence']
    else:
        ed, k = key.split(':')[1], int(key.split(':')[2]); d = divs[ed][k]
        a = ed_node(ed, d['unit'])
        loc = d['locus'].split(', ', 1)[1] if ', ' in d['locus'] and not d['locus'].startswith(("Jugement", "Réflexions")) else d['locus']
        b = src_node(d['text'], loc, d.get('family', ''), d['sourcePassage'], (d.get('links') or [[None, '']])[0][1])
        rel = d['relation']; pa, sp, lab, conf = d['passage'], d['sourcePassage'], d['question'], d['confidence']
    e = edges[(a, b, rel)]; e['n'] += 1; e['subs'].add(sub)
    e['items'].append({'kind': it['kind'], 'label': lab, 'conf': conf, 'sub': sub, 'passage': pa[:400], 'source': sp[:400],
                       **({'comment': divs[ed][k]['comment']} if it['kind'] == 'note' else {})})
    nodes[a]['subs'].add(sub); nodes[b]['subs'].add(sub)
# a Barbeyrac note points to the § it annotates, when that § is in the issue
for k, n in list(nodes.items()):
    m = re.match(r'src:(BbDNG|BbDGP|BbOFF)\|(.+?), n\. ', k)
    if not m: continue
    text = {'BbDNG': 'pufendorf-barbeyrac-1734', 'BbDGP': 'grotius-barbeyrac-1724', 'BbOFF': 'pufendorf-devoirs-barbeyrac-1756'}[m.group(1)]
    base = 'src:%s|%s' % (text, m.group(2))
    if base in nodes: e = edges[(k, base, 'note')]; e['n'] += 1; e['subs'] |= n['subs']
cols = {}
for n in nodes.values():
    c = n.pop('_col'); cols[c[0]] = {'id': c[0], 'label': c[1], 'date': c[2], 'author': c[3]}
order = sorted(cols.values(), key=lambda c: (c['date'], c['label']))
out = {'format': 'nle-issue/1', 'id': IID, 'title': 'The ground of obligation',
       'question': 'What is obligation, and what makes it binding?',
       'description': "Grotius, Pufendorf, Leibniz, Barbeyrac, Wolff, Burlamaqui and Vattel answer the question differently. "
                      "The passages are the reuse rows and divergence notes of the collection's editions that model readers tagged with the issue "
                      "(tools/issues/ISSUE_TAG_PROMPT.md); a passage counts for every sub-issue its rows carry.",
       'subs': [{'id': s, 'label': l} for s, l in SUBS],
       'versions': {e: load('editions/%s/edition.json' % e)['version'] for e in units},
       'columns': order,
       'nodes': sorted(({**n, 'subs': sorted(n['subs'] - {''})} for n in nodes.values()), key=lambda n: ([c['id'] for c in order].index(n['col']), n['sort'] if isinstance(n['sort'], list) else [n['sort']])),
       'edges': [{'from': a, 'to': b, 'rel': rel, 'n': e['n'], 'subs': sorted(e['subs'] - {''}), 'items': e['items']} for (a, b, rel), e in edges.items()]}
for n in out['nodes']: n.pop('sort', None)
print(on, 'tagged items on the issue;', len(out['nodes']), 'nodes;', len(out['edges']), 'edges;', len(order), 'columns')
print(collections.Counter(e['rel'] for e in out['edges']), [(c['label'], c['date'], sum(1 for n in out['nodes'] if n['col'] == c['id'])) for c in order])
if WRITE:
    os.makedirs(ROOT + '/issues', exist_ok=True)
    json.dump(out, open('%s/issues/%s.json' % (ROOT, IID), 'w'), ensure_ascii=False, indent=0)
    ip = ROOT + '/issues/index.json'
    I = json.load(open(ip)) if os.path.exists(ip) else {'format': 'nle-issues/1', 'issues': []}
    I['issues'] = [x for x in I['issues'] if x['id'] != IID] + [{'id': IID, 'title': out['title'], 'question': out['question'],
                   'nodes': len(out['nodes']), 'edges': len(out['edges']), 'authors': sorted({c['author'] for c in order}), 'versions': out['versions']}]
    json.dump(I, open(ip, 'w'), ensure_ascii=False, indent=1)
    print('written')
