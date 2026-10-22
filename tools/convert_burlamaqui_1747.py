# Convert the Burlamaqui 1747 working edition into the collection format (docs/FORMAT.md).
# Usage: python tools/convert_burlamaqui_1747.py <burlamaqui-reuse folder>
# Reads edition/data.json and step10_elemens1783/matches_step10.json (the same/expands relation). Writes editions/burlamaqui-1747/, reuse/, catalogue.json.
# The 1757 Latin translation (step 11) is not in data.json and stays out.
import collections, os, re, sys
from nle import ROOT, Split, load, provenance, update_catalogue, write_tables, write_text

SRC = sys.argv[1]
ED = 'burlamaqui-1747'
MAN = load(os.path.join(ROOT, 'editions', ED, 'edition.json'))
DATA = os.path.join(SRC, 'edition', 'data.json'); S10 = os.path.join(SRC, 'step10_elemens1783', 'matches_step10.json')
D = load(DATA)

# Source texts named by the reuse rows, keyed by the page-id prefix of the step tables.
TEXTS = [
    ('PUF34', 'pufendorf-barbeyrac-1734', 'Samuel Pufendorf', 'Le droit de la nature et des gens, trad. Jean Barbeyrac', 'Amsterdam, 1734. 2 vols', '1734', 'fr',
     "archive.org PDF text layer. Stands in for Basle 1732. Barbeyrac's notes are credited to Barbeyrac (family Bb)."),
    ('DEV56', 'pufendorf-devoirs-barbeyrac-1756', 'Samuel Pufendorf', "Les devoirs de l'homme et du citoyen, trad. Jean Barbeyrac", 'Amsterdam and Leipzig: Arkstée et Merkus, 1756. 2 vols', '1756', 'fr',
     "archive.org OCR (bub_gb_dDKCHraV9BoC, hOCR; bub_gb_unXpgRJJud0C, djvu text in 166 chunks). T. II holds Leibniz's Jugement d'un anonyme with Barbeyrac's Réflexions (family Lz for Leibniz)."),
    ('GRO24', 'grotius-barbeyrac-1724', 'Hugo Grotius', 'Le droit de la guerre et de la paix, trad. Jean Barbeyrac', 'Amsterdam, 1724. 2 vols', '1724', 'fr',
     "archive.org OCR of the Gallica scans. Barbeyrac's notes are credited to Barbeyrac (family Bb)."),
    ('LOC29', 'locke-coste-1729', 'John Locke', "Essai philosophique concernant l'entendement humain, trad. Pierre Coste", 'Amsterdam, 1729. 3rd ed.', '1729', 'fr',
     'archive.org OCR.'),
    ('MAL12', 'malebranche-recherche-1712', 'Nicolas Malebranche', 'De la recherche de la vérité', 'Paris, 1712. 4 vols', '1712', 'fr',
     'archive.org OCR.'),
    ('PRL85', 'port-royal-logique-1685', 'Antoine Arnauld and Pierre Nicole', "La logique ou l'art de penser", '1685', '1685', 'fr',
     'archive.org OCR.'),
    ('DES24', 'descartes-meditations-1724', 'René Descartes', 'Les méditations métaphysiques, T. I', 'Paris, 1724', '1724', 'fr',
     'archive.org OCR.'),
    ('POU49', 'pouilly-theorie-1749', 'Louis-Jean Lévesque de Pouilly', 'Théorie des sentimens agréables', '1749', '1749', 'fr',
     'archive.org OCR of the 1749 Dublin printing. Burlamaqui cites the Geneva 1747 edition; no text layer of it was found.'),
    ('CUM44', 'cumberland-barbeyrac-1744', 'Richard Cumberland', 'Traité philosophique des loix naturelles, trad. Jean Barbeyrac', 'Amsterdam, 1744', '1744', 'fr',
     "archive.org djvu text in 369 chunks of about 3,000 characters; Barbeyrac's notes mixed in."),
    ('HUT26', 'hutcheson-inquiry-1726', 'Francis Hutcheson', 'An Inquiry into the Original of our Ideas of Beauty and Virtue', '1726. 2nd ed.', '1726', 'en',
     'archive.org OCR.'),
    ('HUT30', 'hutcheson-passions-1730', 'Francis Hutcheson', 'An Essay on the Nature and Conduct of the Passions and Affections', '1730. 2nd ed.', '1730', 'en',
     'archive.org OCR.'),
    ('CLE16', 'leclerc-logica-1716', 'Jean Le Clerc', 'Logica, Ontologia et Pneumatologia', 'London, 1716. 5th ed.', '1716', 'la',
     'archive.org OCR.'),
    ('CIC', 'cicero-latin-library', 'Cicero', 'De officiis, Tusculanae disputationes, De finibus, De legibus, De natura deorum, De senectute, De amicitia', '', '', 'la',
     'Text of The Latin Library, chunked at 1,500 characters.'),
    ('SEN', 'seneca-latin-library', 'Seneca', 'Epistulae, De beneficiis, De ira, De clementia, De vita beata', '', '', 'la',
     'Text of The Latin Library, chunked at 1,500 characters.'),
    ('DIG', 'digest-latin-library', 'Justinian', 'Digest, Liv. I', '', '', 'la',
     'Text of The Latin Library, chunked at 1,500 characters.'),
    ('CLA', 'clarke-ricotier-1727', 'Samuel Clarke', "Traités de l'existence et des attributs de Dieu, trad. Pierre Ricotier", '1727–1728. 3 vols', '1727', 'fr',
     'archive.org OCR, chunked at about 2,500 characters.'),
    ('CRO', 'crousaz-logique-1720', 'Jean-Pierre de Crousaz', 'La Logique', '1720 and 1725', '1720', 'fr',
     'archive.org OCR, chunked at about 2,500 characters.'),
    ('SPE', 'spectateur-1716', 'Joseph Addison, Richard Steele and others', 'Le Spectateur ou le Socrate moderne', '1716–1721', '1716', 'fr',
     'archive.org OCR, chunked at about 2,500 characters.'),
    ('ELE83', 'burlamaqui-elemens-1783', 'Jean-Jacques Burlamaqui', 'Élémens du droit naturel', 'Lausanne: Grasset, 1783', '1783', 'fr',
     'MDZ OCR (bsb10040023, hOCR, one unit per scan). The lecture course; printed 35 years after the 1747 text from student copies.'),
    ('PDP51', 'burlamaqui-droit-politique-1751', 'Jean-Jacques Burlamaqui', 'Principes du droit politique', 'Amsterdam, 1751. 2 vols', '1751', 'fr',
     'MDZ OCR (bsb10040032/33).'),
]
TEXT_OF = {t[0]: t[1] for t in TEXTS}

def text_id(page):
    k = page.split('.')[0]
    for key in (re.sub(r'T\d$', '', k), re.sub(r'\d\d[A-Z]?$', '', k)):
        if key in TEXT_OF: return TEXT_OF[key]
    raise KeyError(page)


def unit_head(s):
    sid = s['id']
    div = 'AV' if sid == 'AV' else 'P%d' % s['part']
    rec = {'id': sid, 'div': div, 'chap': s['chap'], 'n': s['para'],
           'kind': 'front' if sid == 'AV' else 'heading' if s['para'] == 0 else 'section'}
    if s['margin']: rec['margin'] = s['margin']
    rec['pages'] = [{'scan': p['scan'], 'printed': p['printed']} for p in s['pages']]
    return rec


SECS = D['sections']; ROWS = D['rows']
X = Split(SECS, unit_head, MAN['viewer']['pageBreak'])
write_text(ED, {'P' + k: v for k, v in D['titles'].items()}, X.units)

# the same/expands relation of step 10, matched on unit, page and passage
REL = {}
for r in load(S10):
    if r['status'] in ('match', 'possible'):
        k = (r['bur_id'], r['page_id'], r['bur_passage']); assert k not in REL; REL[k] = r['relation']

tables = collections.defaultdict(list); miss = 0
for r in ROWS:
    row = X.reuse_row(r)
    if r['fam'] == 'El':
        rel = REL.get((r['sec'], r['page'], r['vp']))
        if rel: row['relation'] = rel
        else: miss += 1
    tables[text_id(r['page'])].append(row)
assert set(X.reuse_at) <= {r['id'] for r in ROWS} and miss == 0, miss
STEPS = {3: "Barbeyrac's Pufendorf, Droit de la nature et des gens (step 3)", 4: "Barbeyrac's Devoirs and Grotius (step 4)",
         6: 'Locke, Malebranche, Port-Royal, Descartes, Pouilly, Cumberland, Hutcheson, Le Clerc (step 6)',
         8: 'Principes du droit politique, 1751 (step 8)', 9: 'Ancient authors; Clarke, Crousaz, Spectateur, Abbadie (step 9)',
         10: 'The lecture course, Élémens du droit naturel, 1783 (step 10)'}
TX = [{'id': t[1], 'sigla': [t[0]], 'author': t[2], 'title': t[3], 'imprint': t[4], 'date': t[5], 'lang': t[6], 'layer': t[7]} for t in TEXTS]
EXTRA = {
    'burlamaqui-elemens-1783': {'relations': {'same': 'same text', 'pdn_expands': 'the 1747 text expands the lecture text',
                                              'pdn_abridges': 'the 1747 text abridges it', 'pdn_changes': 'the doctrine changes'}},
    'burlamaqui-droit-politique-1751': {'direction': 'derivative'},
}
cat_reuse = write_tables(ED, tables, TX, STEPS,
                         'Reuse between the edition and the text, found by retrieval and judged by a language model; hand checks as in the method log. '
                         'status match: confidence >= 0.5; possible: below. Source passages are quoted from the text layer named in the catalogue.',
                         EXTRA)
assert sum(c['rows'] for c in cat_reuse) == len(ROWS)

provenance(ED, 'burlamaqui-reuse/', [('edition/data.json', DATA), ('step10_elemens1783/matches_step10.json', S10)])
entry = {'id': ED, 'path': 'editions/%s/' % ED, 'author': MAN['author'], 'authorShort': 'Burlamaqui', 'title': MAN['title'], 'short': MAN['short'],
         'imprint': MAN['imprint'], 'date': MAN['date'], 'lang': MAN['lang'], 'status': 'working edition'}
used = {c['to'] for c in cat_reuse}
update_catalogue(entry, [t for t in TX if t['id'] in used], cat_reuse)

units = X.units
print('units', len(units), 'kinds', dict(collections.Counter(u['kind'] for u in units)), 'notes', sum(len(u.get('notes', [])) for u in units),
      'pb', sum(len(u.get('pb', [])) for u in units), 'xr', sum(len(u.get('xr', [])) + sum(len(n.get('xr', [])) for n in u.get('notes', [])) for u in units))
print('reuse rows', len(ROWS), 'tables', len(cat_reuse), 'where', dict(collections.Counter(r['where'][:1] or '-' for r in ROWS)))
for c in cat_reuse: print('  ', c['to'], c['rows'])
