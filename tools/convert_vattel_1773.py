# Convert the Vattel 1773 working edition (edition_data/*.json) into the collection format (docs/FORMAT.md).
# Usage: python tools/convert_vattel_1773.py <edition_data folder>
# Reads data.json, en_sections.json, align.json, flags.json, para_final.json. Writes editions/vattel-1773/, reuse/, catalogue.json.
import os, re, shutil, sys
from nle import ROOT, Split, dump, load, provenance, update_catalogue, write_tables, write_text

SRC = sys.argv[1]
ED = 'vattel-1773'
OUT = os.path.join(ROOT, 'editions', ED)
MAN = load(os.path.join(OUT, 'edition.json'))
OLD_TITLE = next(l for l in MAN['layers'] if l['kind'] == 'variants')['otherTitle']

D = load(os.path.join(SRC, 'data.json'))
EN = load(os.path.join(SRC, 'en_sections.json'))['en']
AL = load(os.path.join(SRC, 'align.json'))
FL = load(os.path.join(SRC, 'flags.json'))
LF_OFFSET = 27  # Liberty Fund page = PDF page index - 27 (method log, English layer)

# Source texts named by the reuse rows, keyed by the page-id prefix of the step tables.
TEXTS = [
    ('JG', 'wolff-jus-gentium-1749', 'Christian Wolff', 'Jus gentium methodo scientifica pertractatum', 'Halle, 1749', '1749', 'la',
     'Vision transcription of the Google Books copy (scans 28–876); Praefatio and Prolegomena from MDZ bsb10008059. Working French by machine.'),
    ('INST', 'wolff-institutiones-1750', 'Christian Wolff', 'Institutiones juris naturae et gentium', 'Halle, 1750', '1750', 'la',
     'Vision transcription of the Google Books copy (scans 30–811). Working French by machine.'),
    ('JN8', 'wolff-jus-naturae-8-1748', 'Christian Wolff', 'Jus naturae methodo scientifica pertractatum, pars VIII', '1748', '1748', 'la',
     'Google Books OCR, cleaned. Working French by machine.'),
    ('BUR47', 'burlamaqui-1747', 'Jean-Jacques Burlamaqui', 'Principes du droit naturel', 'Genève, 1747', '1747', 'fr',
     'Google Books PDF text layer.'),  # an edition in the collection
    ('BUR51', 'burlamaqui-droit-politique-1751', 'Jean-Jacques Burlamaqui', 'Principes du droit politique', 'Amsterdam, 1751. 2 vols', '1751', 'fr',
     'MDZ OCR (bsb10040032/33).'),
    ('GRO24', 'grotius-barbeyrac-1724', 'Hugo Grotius', 'Le droit de la guerre et de la paix, trad. Jean Barbeyrac', 'Amsterdam, 1724. 2 vols', '1724', 'fr',
     "archive.org OCR of the Gallica scans. Barbeyrac's notes are credited to Barbeyrac (family Bb)."),
    ('PUF34', 'pufendorf-barbeyrac-1734', 'Samuel Pufendorf', 'Le droit de la nature et des gens, trad. Jean Barbeyrac', 'Amsterdam, 1734. 2 vols', '1734', 'fr',
     "archive.org PDF text layer. Stands in for Basle 1732. Barbeyrac's notes are credited to Barbeyrac (family Bb)."),
    ('MON49', 'montesquieu-esprit-des-loix-1749', 'Montesquieu', "De l'esprit des loix", 'Genève: Barrillot, 1749', '1749', 'fr',
     'archive.org OCR (bub_gb_qq8hNilO1RkC). Stands in for 1748.'),
    ('WIC24', 'wicquefort-ambassadeur-1724', 'Abraham de Wicquefort', "L'ambassadeur et ses fonctions", 'La Haye, 1724', '1724', 'fr',
     'archive.org OCR (lambassadeuretse12wicq, scans 1–1532).'),
    ('BYN23', 'bynkershoek-juge-competent-1723', 'Cornelius van Bynkershoek', 'Traité du juge compétent des ambassadeurs, trad. Jean Barbeyrac', '1723', '1723', 'fr',
     'archive.org OCR (lambassadeuretse12wicq, scans 1533–1902; bound with Wicquefort 1724).'),
    ('BYN37', 'bynkershoek-quaestiones-1737', 'Cornelius van Bynkershoek', 'Quaestiones juris publici', 'Leiden, 1737', '1737', 'la',
     'archive.org OCR (corneliivanbynke00bijnx).'),
    ('FOR58', 'formey-principes-1758', 'Jean Henri Samuel Formey', 'Principes du droit de la nature et des gens', 'Amsterdam, 1758. 3 vols', '1758', 'fr',
     'archive.org OCR (principesdudroi00–03wolfgoog), chunked at about 1,800 characters.'),
    ('LOI47', 'vattel-loisir-1747', 'Emer de Vattel', 'Le loisir philosophique', '1747', '1747', 'fr',
     'Tesseract text layer of the library PDF.'),
    ('QUE62', 'vattel-questions-1762', 'Emer de Vattel', 'Questions de droit naturel, et observations sur le Traité du droit de la nature de M. le baron de Wolf', 'Berne, 1762', '1762', 'fr',
     'archive.org OCR (questionsdedroit00vatt). Written before 1758.'),
    ('POL57', 'vattel-poliergie-1757', 'Emer de Vattel', 'Poliergie', '1757', '1757', 'fr',
     'archive.org OCR (poliergieoumla00vattuoft).'),
    ('AMU65', 'vattel-amusemens-1765', 'Emer de Vattel', 'Amusemens de littérature, de morale et de politique', '1765', '1765', 'fr',
     'Text layer of the library PDF. Reissue of the Mélanges (1760).'),
]
TEXT_OF = {t[0]: t[1] for t in TEXTS}
TEXT_OF['WJG'] = TEXT_OF['JG']  # Wolff's Praefatio and Prolegomena to the Jus gentium (step 2 transcription)

def text_id(page):
    m = re.match(r'([A-Z]+?\d*?)(?:T\d|T3b)?\.(?:pdf|p|s|c)\d+$', page) or re.match(r'(WJG)\.', page)
    return TEXT_OF[m.group(1)]


def unit_head(s):
    sid = s['id']
    rec = {'id': sid, 'div': s['book'], 'chap': s['chap'], 'n': s['para'],
           'kind': 'heading' if sid.endswith('.0') else 'page' if s['book'] == 'Pref' else 'section'}
    if s['unnum']: rec['unnumbered'] = True
    if s['margin']: rec['margin'] = s['margin']
    rec['pages'] = [{'vol': p['vol'], 'scan': p['scan'], 'printed': p['printed']} for p in s['pages']]
    return rec


SECS = D['sections']; ROWS = D['rows']
X = Split(SECS, unit_head, MAN['viewer']['pageBreak'], OLD_TITLE)
write_text(ED, D['titles'], X.units)
var_at, whole, older = X.var_at, X.whole, X.older

# ---------- 1773 changes ----------
items = []; vids = set()
for s in SECS:
    for v in s['vars']:
        vids.add(v['id'])
        it = {'id': v['id'], 'unit': s['id'], 'type': v['type'], 'content': v['content'], 'placed': v['placed'],
              'passage': v['p1773'], 'otherPassage': v['p1758'], 'otherPages': v['pages1758'], 'otherLink': v['link1758']}
        if var_at.get(v['id']): it['at'] = var_at[v['id']]
        if whole.get(v['id']): it['wholeNotes'] = whole[v['id']]
        if older.get(v['id']): it['otherReadings'] = older[v['id']]
        items.append(it)
assert set(var_at) <= vids and set(older) <= vids and set(whole) <= vids
dump({'format': 'nle-layer/1', 'edition': ED, 'layer': 'changes-1773', 'kind': 'variants',
      'base': 'Neuchâtel 1773', 'other': 'Londres [Neuchâtel] 1758, Library copy; Leide 1758 as a check',
      'description': 'Changes between the first edition (1758) and 1773, found by collation of OCR against the 1773 transcription (method log, step 7). '
                     'Changes under 8 tokens are not detected. otherReadings are 1758 readings dropped in 1773, cleaned by hand from the OCR.',
      'items': items}, os.path.join(OUT, 'layers', 'changes-1773.json'))

# ---------- Wolff divergences ----------
div = []
for s in SECS:
    for d in s.get('div', []):
        div.append({'unit': s['id'], 'text': TEXT_OF['INST' if d['wid'].startswith('INST') else 'JG'], 'locus': d['w'], 'sourceId': d['wid'],
                    'relation': d['rel'], 'severity': d['sev'], 'question': d['q'], 'comment': d['c'],
                    'passage': d['vp'], 'sourcePassage': d['lat'], 'confidence': d['conf'], 'links': d['link']})
assert all(re.match(r'(JG|INST)\.', d['sourceId']) for d in div)
dump({'format': 'nle-layer/1', 'edition': ED, 'layer': 'wolff-divergences', 'kind': 'comments',
      'description': "Places where Wolff answers the question of a section and Vattel answers it differently (method log, divergence layer). "
                     "relation: diverges or partly. severity: 3 incompatible answers, 2 different ground or a condition that changes cases, 1 a qualification. "
                     "Machine judgements, not checked by hand.",
      'items': div}, os.path.join(OUT, 'layers', 'wolff-divergences.json'))

# ---------- English ----------
ens = {}
for s in SECS:
    sid = s['id']
    if sid not in EN: continue
    e = EN[sid]
    assert e['text'] == ' '.join(e['sents']) and sid in AL
    ens[sid] = {'page': e['page'] - LF_OFFSET, 'sents': e['sents'], 'fr': s['fs'], 'align': AL[sid], 'flags': FL.get(sid, [])}
    if e['notes']: ens[sid]['notes'] = e['notes']
    assert s['en'] == {'s': e['sents'], 'g': AL[sid], 'p': e['page'] - LF_OFFSET, 'f': FL.get(sid, [])}
assert set(EN) == set(ens) and set(FL) <= set(ens)
dump({'format': 'nle-layer/1', 'edition': ED, 'layer': 'english', 'kind': 'translation',
      'source': {'title': 'The Law of Nations', 'translation': 'London, 1797',
                 'edition': 'ed. Béla Kapossy and Richard Whatmore, Indianapolis: Liberty Fund, 2008'},
      'description': 'page: Liberty Fund page (PDF page index - 27). sents: English sentences of the main text. notes: English footnotes, not aligned. '
                     'fr: French sentence spans in the unit text. align: groups [[French sentence indices], [English sentence indices]], '
                     'by multilingual e5 embeddings and a monotone dynamic programme. flags: translation problems keyed by group (k), '
                     'machine judgements, not checked by hand.',
      'units': ens}, os.path.join(OUT, 'layers', 'english.json'))

# ---------- reuse tables ----------
tables = {}
for r in ROWS: tables.setdefault(text_id(r['page']), []).append(X.reuse_row(r))
assert set(X.reuse_at) == {r['id'] for r in ROWS}
STEPS = {'3b': 'Wolff re-scanned on a transcription (step 3b)', 4: 'Burlamaqui, Grotius and Pufendorf (step 4)',
         6: 'Montesquieu, Wicquefort, Bynkershoek, Formey, Loisir (step 6)', 8: "Vattel's other works (step 8)", 'P': 'Préface, all pools (Préface pass)'}
TX = [{'id': t[1], 'siglum': t[0], 'author': t[2], 'title': t[3], 'imprint': t[4], 'date': t[5], 'lang': t[6], 'layer': t[7]} for t in TEXTS]
cat_reuse = write_tables(ED, tables, TX, STEPS,
                         'Reuse of the source in the edition, found by retrieval and judged by a language model. '
                         'status match: confidence >= 0.5; possible: 0.3-0.5. Source passages are quoted from the text layer named in the catalogue.',
                         {'burlamaqui-1747': {'toLayer': 'Google Books PDF text layer (OCR) of the scan the burlamaqui-1747 edition was transcribed from.'}})
assert sum(c['rows'] for c in cat_reuse) == len(ROWS)

# ---------- provenance ----------
prov = os.path.join(OUT, 'provenance'); os.makedirs(prov, exist_ok=True)
shutil.copyfile(os.path.join(SRC, 'para_final.json'), os.path.join(prov, 'para_final.json'))
pf = load(os.path.join(SRC, 'para_final.json'))
provenance(ED, 'vattel-reuse/edition_data/', [(n, os.path.join(SRC, n)) for n in ['data.json', 'en_sections.json', 'align.json', 'flags.json', 'para_final.json']],
           '`para_final.json` lists the paragraph starts inside a § confirmed on the scans: %d breaks on %d pages, keyed by `<volume>:<scan>` '
           'with transcription line indices. `text.json` carries the breaks as `para` offsets.' % (sum(map(len, pf.values())), len(pf)))

# ---------- catalogue ----------
used = {c['to'] for c in cat_reuse} | {d['text'] for d in div}
entry = next(e for e in load(os.path.join(ROOT, 'catalogue.json'))['editions'] if e['id'] == ED)
update_catalogue(entry, [t for t in TX if t['id'] in used], cat_reuse)

units = X.units
print('units', len(units), 'notes', sum(len(u.get('notes', [])) for u in units),
      'para', sum(len(u.get('para', [])) for u in units), 'pb', sum(len(u.get('pb', [])) for u in units),
      'xr', sum(len(u.get('xr', [])) + sum(len(n.get('xr', [])) for n in u.get('notes', [])) for u in units))
print('variants', len(items), 'placed spans', sum(len(i.get('at', [])) for i in items), 'whole notes', sum(len(i.get('wholeNotes', [])) for i in items),
      '1758 readings', sum(len(i.get('otherReadings', [])) for i in items))
print('divergences', len(div), 'english units', len(ens), 'flags', sum(len(v['flags']) for v in ens.values()))
print('reuse rows', len(ROWS), 'tables', len(cat_reuse))
for c in cat_reuse: print('  ', c['to'], c['rows'])
