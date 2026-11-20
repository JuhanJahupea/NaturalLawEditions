# Convert Vattel's Essai sur le fondement du droit naturel (Le loisir philosophique, Genève 1747) into the collection format
# (docs/FORMAT.md). Usage: python tools/convert_vattel_essai_1747.py <data.json>
# data.json is built from the page transcription by tools/transcription/essai_data.py (texts/vattel-loisir-1747/LOI47.json).
# The edition has no working-edition reuse rows: every table comes from a pass (editions/vattel-essai-1747/passes/).
import collections, os, sys
from nle import ROOT, Split, apply_row_edits, dump, load, load_pass, provenance, update_catalogue, write_tables, write_text

DATA = sys.argv[1]
ED = 'vattel-essai-1747'
MAN = load(os.path.join(ROOT, 'editions', ED, 'edition.json'))
D = load(DATA)
TEXTS = [
    ('PPU1', 'wolff-philosophia-practica-1738', 'Christian Wolff', 'Philosophia practica universalis, methodo scientifica pertractata, pars prior', 'Frankfurt and Leipzig, 1738', '1738', 'la',
     'Vision transcription of the MDZ scans of the Halle 1744 issue, which keeps the setting of 1738 (texts/wolff-philosophia-practica-1738/). Working French by machine.'),
    ('PUF34', 'pufendorf-barbeyrac-1734', 'Samuel Pufendorf', 'Le droit de la nature et des gens, trad. Jean Barbeyrac', 'Amsterdam, 1734. 2 vols', '1734', 'fr',
     "Vision transcription (texts/pufendorf-barbeyrac-1734/). Barbeyrac's notes are credited to Barbeyrac (family Bb)."),
    ('DEV56', 'pufendorf-devoirs-barbeyrac-1756', 'Samuel Pufendorf', "Les devoirs de l'homme et du citoyen, trad. Jean Barbeyrac", 'Amsterdam and Leipzig: Arkstée et Merkus, 1756. 2 vols', '1756', 'fr',
     "Vision transcription (texts/pufendorf-devoirs-barbeyrac-1756/). Stands in for the 4th edition, Amsterdam: de Coup, 1718, which Vattel cites. T. II holds Leibniz's Jugement d'un anonyme (family Lz) with Barbeyrac's Réflexions (family Bb)."),
    ('GRO24', 'grotius-barbeyrac-1724', 'Hugo Grotius', 'Le droit de la guerre et de la paix, trad. Jean Barbeyrac', 'Amsterdam, 1724. 2 vols', '1724', 'fr',
     "Vision transcription (texts/grotius-barbeyrac-1724/). Barbeyrac's notes are credited to Barbeyrac (family Bb)."),
    ('BUR47', 'burlamaqui-1747', 'Jean-Jacques Burlamaqui', 'Principes du droit naturel', 'Genève, 1747', '1747', 'fr',
     'The burlamaqui-1747 edition of this collection.'),
    ('TN1', 'wolff-theologia-naturalis-1739', 'Christian Wolff', 'Theologia naturalis, methodo scientifica pertractata, pars prior', 'Frankfurt and Leipzig: Renger, 1739', '1739', 'la',
     'Vision transcription of the MDZ scans, §§ 948-1006 (texts/wolff-theologia-naturalis-1739/). Working French by machine.'),
    ('LOG40', 'wolff-discursus-praeliminaris-1740', 'Christian Wolff', 'Discursus praeliminaris de philosophia in genere', 'In Philosophia rationalis sive Logica, Frankfurt and Leipzig: Renger, 1740', '1740', 'la',
     'Vision transcription of the MDZ scans (texts/wolff-discursus-praeliminaris-1740/). Working French by machine.'),
]
EXTRA = {'burlamaqui-1747': {'toLayer': "The burlamaqui-1747 edition's transcription (editions/burlamaqui-1747/text.json)."}}

def unit_head(s):
    rec = {'id': s['id'], 'div': 'E', 'chap': 0, 'n': s['para'], 'kind': 'heading' if s['para'] == 0 else 'section'}
    if s['margin']: rec['margin'] = s['margin']
    rec['pages'] = [{'scan': p['scan'], 'printed': p['printed']} for p in s['pages']]
    return rec

SECS = D['sections']; ROWS = D['rows']; assert not ROWS
X = Split(SECS, unit_head, MAN['viewer']['pageBreak'])
write_text(ED, D['titles'], X.units)
TX = [{'id': t[1], 'sigla': [t[0]], 'author': t[2], 'title': t[3], 'imprint': t[4], 'date': t[5], 'lang': t[6], 'layer': t[7]} for t in TEXTS]
cat_reuse, replaced = write_tables(ED, {}, TX, {}, '', EXTRA)
assert replaced == 0
provenance(ED, 'texts/vattel-loisir-1747/LOI47.json via tools/transcription/essai_data.py', [('data.json', DATA)])
entry = {'id': ED, 'path': 'editions/%s/' % ED, 'author': MAN['author'], 'authorShort': 'Vattel', 'title': MAN['title'], 'short': MAN['short'],
         'imprint': MAN['imprint'], 'date': MAN['date'], 'lang': MAN['lang'], 'status': 'working edition', 'menu': 'Vattel, Essai 1747'}
used = {c['to'] for c in cat_reuse}
update_catalogue(entry, [t for t in TX if t['id'] in used], cat_reuse)
print('units', len(X.units), dict(collections.Counter(u['kind'] for u in X.units)), 'notes', sum(len(u.get('notes', [])) for u in X.units),
      'pb', sum(len(u.get('pb', [])) for u in X.units), 'tables', [(c['to'], c['rows']) for c in cat_reuse])
