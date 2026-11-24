# gold_def41.py: the gold set of Vattel's Défense du système leibnitien (1741), every explicit citation in the text and
# the notes, from the four reader batches <WORK>/def41/gold/o0..o3.json (prompt GOLD_PROMPT_DEF41.md, Claude Sonnet, one
# batch per quarter of the units of <WORK>/def41/data.json) into editions/vattel-defense-1741/provenance/citations.json.
# Author and work names are normalized here; the readers' raw, locus, container, kind, resolved and note are kept.
import os, sys, json, glob
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT, WORK

HOS = "Réponse aux objections de Bayle (Histoire des ouvrages des savans, juillet 1698)"
ROQ3 = "Lettres à Bourguet (Journal helvétique, nov. 1738 - mars 1739)"
REMK = "Remarques sur le livre de l'origine du mal (King)"
WORK_MAP = {
    ('Leibniz', 'Réponse aux objections de M. Bayle'): HOS,
    ('Leibniz', 'Éclaircissement des difficultés de Bayle'): HOS,
    ('Leibniz', 'Réponse à Bayle (Histoire des ouvrages des savans, juillet 1698)'): HOS,
    ('Leibniz', 'De ipsa natura, sive de vi insita'): 'De ipsa natura',
    ('Leibniz', 'Leibniz-Clarke'): 'Leibniz-Clarke (no écrit named)',
    ("Leibniz", "Remarques sur le livre de l'Origine du mal (de King)"): REMK,
    ("Leibniz", "Remarques sur le livre de l'origine du mal"): REMK,
    ("Leibniz", "Remarques sur le livre de l'origine du mal (King)"): REMK,
    ('Leibniz', 'Réplique aux réflexions de Bayle (Recueil Des Maizeaux)'): 'Réplique aux réflexions de Bayle',
    ('Leibniz', 'Réplique aux réflexions de M. Bayle'): 'Réplique aux réflexions de Bayle',
    ('Leibniz', 'Réponse au P. Lamy (Supplément du Journal des Sçavans, juin 1709)'): 'Réponse au P. Lamy',
    ('Leibniz', 'Réponse au P. Lamy (exemple des deux pendules)'): 'Réponse au P. Lamy',
    ('Leibniz', 'Système nouveau de la nature'): 'Système nouveau de la nature et de la communication des substances',
    ('Leibniz', 'Théodicée, Discours de la conformité de la foi avec la raison'): 'Théodicée, Discours de la conformité',
    ('Leibniz', 'Éclaircissement du nouveau système (réponse à Foucher)'): 'Éclaircissement du nouveau système',
    ('Leibniz', ''): '(no work named)',
    ('Bayle', 'Dictionnaire historique et critique (objection citée par Leibniz)'): 'Dictionnaire historique et critique',
    ('Bourguet', 'Journal helvétique, mai 1738'): 'Journal helvétique, mai 1738',
    ('Bourguet', 'Journal helvétique, Mai 1738'): 'Journal helvétique, mai 1738',
    ('Béguelin', 'Journal helvétique'): 'Journal helvétique, janv. 1738',
    ('Anonyme', 'Journal helvétique, Août 1738'): 'Journal helvétique, août 1738',
    ('Roques', 'Deuxième lettre à Bourguet (Journal helvétique, nov. 1738)'): ROQ3,
    ('Roques', 'Troisième lettre (Journal helvétique, nov. 1738)'): ROQ3,
    ('Pope', 'Essai sur l\'homme (trad. Du Resnel)'): 'Essay on Man',
    ('Pope', 'Essay on Man (trad. Du Resnel)'): 'Essay on Man',
    ('Euripides', 'Théodicée (quoting Euripides)'): '(verse quoted in the Théodicée)',
    ('Chrysippus', 'Théodicée'): '(passage reported in the Théodicée)',
    ('Turrettini', 'Vindiciae providentiae divinae'): 'Vindiciae providentiae divinae',
    ('Turrettini (J. A.)', 'Vindiciae Providentiae Divinae'): 'Vindiciae providentiae divinae',
    ('J.-A. Turrettini', 'Theses de libertate humana'): 'De libertate humana',
    ('Turrettini', 'De libertate humana'): 'De libertate humana',
    ('Wolff', 'Cosmologia generalis, Praefatio'): 'Cosmologia generalis',
    ('Anonymous (Bibliothèque raisonnée)', 'Extrait de la Theologia naturalis de Wolff'): 'Theologia naturalis (extract in the Bibliothèque raisonnée)',
    ('Plato', ''): '(no work named)',
    ('Socrates', ''): '(saying reported by Leibniz, Théodicée § 146)',
}
AUTHOR_MAP = {'Cicero': 'Cicéron', 'Boileau (Despréaux)': 'Boileau', 'Turrettini': 'J.-A. Turrettini',
              'Turrettini (J. A.)': 'J.-A. Turrettini', '(anonyme)': 'Anonymous', 'Anonyme': 'Anonymous',
              'Ami de Vattel (anonyme)': 'Anonymous (a friend of Vattel)', 'Unknown': 'Anonymous',
              'Anonymous (Bibliothèque raisonnée)': 'Wolff', 'Plato': 'Platon', 'Socrates': 'Socrate',
              'Chrysippus': 'Chrysippe', 'Euripides': 'Euripide', 'Tacitus': 'Tacite', 'Aristote': 'Aristote'}

C = []
for f in sorted(glob.glob(os.path.join(WORK, 'def41', 'gold', 'o[0-9].json'))):
    C += json.load(open(f))['citations']
out = []
for c in C:
    a, w = c.get('author') or '', c.get('work') or ''
    w2 = WORK_MAP.get((a, w), w)
    a2 = AUTHOR_MAP.get(a, a)
    r = {'unit': c['unit'], 'where': c['where'], 'raw': c['raw'], 'author': a2, 'work': w2,
         'locus': c.get('locus') or '', 'container': c.get('container') or '', 'kind': c['kind'],
         'resolved': bool(c.get('resolved'))}
    if (c.get('work') or '') == 'Cosmologia generalis, Praefatio' and not r['locus']: r['locus'] = 'Praefatio'
    if c.get('note'): r['note'] = c['note']
    out.append(r)

by_author = Counter(r['author'] for r in out)
by_work = Counter((r['author'], r['work']) for r in out)
summary = {'citations': len(out), 'units_citing': len({r['unit'] for r in out}),
           'kinds': dict(Counter(r['kind'] for r in out)),
           'by_author': [{'author': a, 'n': n} for a, n in by_author.most_common()],
           'by_work': [{'author': a, 'work': w, 'n': n} for (a, w), n in by_work.most_common()]}
wolff = [r for r in out if r['author'] == 'Wolff']
W = {}
for r in wolff:
    W.setdefault(r['work'], []).append({'unit': r['unit'], 'locus': r['locus'], 'kind': r['kind']})
doc = {'format': 'nle-citations/1', 'text': 'vattel-defense-1741',
       'method': 'Every explicit citation (reference or quotation) in the text and notes, read unit by unit by Claude Sonnet '
                 '(prompt tools/transcription/GOLD_PROMPT_DEF41.md) from the transcription texts/vattel-defense-1741/DEF41.json; '
                 'Ibid., ubi supra and bare page numbers resolved from context ("resolved": true). Names normalized by '
                 'tools/transcription/gold_def41.py. Vattel\'s cross-references to his own paragraphs are left out.',
       'summary': summary, 'wolff': W, 'citations': out}
p = os.path.join(ROOT, 'editions', 'vattel-defense-1741', 'provenance', 'citations.json')
with open(p, 'w', encoding='utf-8') as f:
    json.dump(doc, f, ensure_ascii=False, indent=1); f.write('\n')
print(len(out), 'citations in', summary['units_citing'], 'units;', len(by_work), 'works;', by_author.most_common(8))
for (a, w), n in by_work.most_common(40): print(' ', n, a, '|', w)
