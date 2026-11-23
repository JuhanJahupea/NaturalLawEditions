# vattel_american.py: the data report "Which Vattel did the colonists cite? Sources of the passages, 1762-1776".
# Reads reports/data/vattel-american-citations.json (the §§ American writers cited, from three studies), the edition's
# reuse tables (match rows) and its divergence notes, and writes reports/vattel-american-sources.md and the report's
# entry in reports/index.json with the edition version it was built from. Run it again whenever the tables change.
import os, re, json, glob, collections, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ED, RID, DATA = 'vattel-1773', 'vattel-american-sources', 'reports/data/vattel-american-citations.json'
load = lambda p: json.load(open(os.path.join(ROOT, p), encoding='utf-8'))
man = load('editions/%s/edition.json' % ED); ver = man['version']
units = [u['id'] for u in load('editions/%s/text.json' % ED)['units'] if u['div'] in ('Prelim', 'I', 'II', 'III', 'IV')]
WOLFF = {'wolff-jus-gentium-1749': 'Jus gentium', 'wolff-institutiones-1750': 'Institutiones', 'wolff-jus-naturae-8-1748': 'Jus naturae VIII'}
RANK = {'verbatim': 5, 'translation': 5, 'close paraphrase': 4, 'loose paraphrase': 3, 'shared argument': 2, 'citation': 2, 'commonplace': 1}
SHORT = {'grotius-barbeyrac-1724': 'Grotius, DGP', 'pufendorf-barbeyrac-1734': 'Pufendorf, DNG', 'formey-principes-1758': 'Formey, Principes',
         'burlamaqui-1747': 'Burlamaqui, Principes du droit naturel', 'burlamaqui-droit-politique-1751': 'Burlamaqui, Droit politique',
         'vattel-loisir-1747': 'Vattel, Loisir philosophique', 'vattel-questions-1762': 'Vattel, Questions', 'vattel-poliergie-1757': 'Vattel, Poliergie',
         'vattel-amusemens-1765': 'Vattel, Amusemens', 'montesquieu-esprit-des-loix-1749': 'Montesquieu, Esprit des loix',
         'wicquefort-ambassadeur-1724': 'Wicquefort, Ambassadeur', 'bynkershoek-quaestiones-1737': 'Bynkershoek, Quaestiones',
         'bynkershoek-juge-competent-1723': 'Bynkershoek, Juge compétent'}
short = lambda tid: SHORT.get(tid, tid)
rows = collections.defaultdict(list)
for f in glob.glob(os.path.join(ROOT, 'reuse', ED + '__*.json')):
    tid = os.path.basename(f)[len(ED) + 2:-5]
    for r in json.load(open(f, encoding='utf-8'))['rows']:
        if r['status'] == 'match' and RANK.get(r['label'], 0): rows[r['unit']].append((tid, r))
dv = collections.defaultdict(list)
for x in load('editions/%s/layers/divergences.json' % ED)['items']: dv[x['unit']].append(x)
def best(u, wolff):
    c = [(RANK[r['label']], r['confidence'], t, r) for t, r in rows.get(u, []) if (t in WOLFF) == wolff]
    return max(c, key=lambda z: z[:2]) if c else None
def klass(u):
    w, o = best(u, True), best(u, False)
    if w and w[0] >= 4: return 'W'
    if o and o[0] >= 4: return 'O'
    if w and w[0] >= 3: return 'w'
    if o and o[0] >= 3: return 'O'
    return 'V'
LAB = {'W': 'Wolff, close', 'w': 'Wolff, loose', 'O': 'other source', 'V': 'no source found'}
bk = lambda u: u.split('.')[0]
order = lambda u: (['Prelim', 'I', 'II', 'III', 'IV'].index(bk(u)), int(u.split('.')[1]))
# baseline: every § of the work
base = collections.defaultdict(collections.Counter)
for u in units: base[bk(u)][klass(u)] += 1; base['all'][klass(u)] += 1
D = load(DATA)
def who(x):
    a = re.sub(r'\s*\(.*?\)|\s*\[.*?\]', '', x.get('author') or '').strip("' ")
    a = a.replace('Massachusetts House of Representatives', 'Mass. House').replace('Second Continental Congress', 'Congress')
    a = re.sub(r'^James Otis for the Mass\. House', 'Mass. House (Otis)', a)
    return '%s %s' % (a.replace("'", ''), (x.get('date') or '')[:4])
cit = collections.defaultdict(list); hyp = collections.defaultdict(list)
for x in D['citations']:
    for l in x.get('loci') or []: cit[l].append(x)
for x in D['hypotexts']:
    for l in x.get('loci') or []:
        if l not in cit: hyp[l].append(x)
def tab(src, users):
    out = ['| § | %s | Wolff | other source | departs from Wolff | class |' % users, '|---|---|---|---|---|---|']
    for u in sorted(src, key=order):
        w, o = best(u, True), best(u, False)
        ws = '%s %s (%s)' % (WOLFF[w[2]], w[3]['locus'] or 'PDF p. ' + w[3].get('page', '').split('pdf')[-1], w[3]['label']) if w else ''
        os_ = '%s %s (%s)' % (short(o[2]), o[3]['locus'], o[3]['label']) if o and o[0] >= 3 else ''
        dw = '; '.join('%s %s' % (WOLFF[x['text']], re.sub(r'^.*?(§+ ?[\d–-]+).*$', r'\1', x['locus'])) for x in dv.get(u, []) if x['text'] in WOLFF)
        us = ', '.join(sorted({who(x) for x in src[u]}, key=lambda s: s[-4:])) if users == 'cited by' else ', '.join(sorted({x['document'].split(',')[0][:48] for x in src[u]}))
        out.append('| [%s](../viewer/?ed=%s#%s) | %s | %s | %s | %s | %s |' % (u.replace('Prelim.', 'Prél. '), ED, u, us, ws, os_, dw, LAB[klass(u)]))
    return '\n'.join(out)
def count(src, weight=False):
    c = collections.Counter()
    for u in src: c[klass(u)] += len(src[u]) if weight else 1
    return c
cc, cw, hc = count(cit), count(cit, True), count(hyp)
nC = sum(cc.values()); nW = sum(cw.values())
exp = sum(base[bk(u)]['W'] / sum(base[bk(u)].values()) for u in cit)
dep = [u for u in cit if any(x['text'] in WOLFF for x in dv.get(u, []))]
pct = lambda a, b: '%d%%' % round(100 * a / b) if b else '–'
books = [('Prelim', 'Préliminaires'), ('I', 'Livre I'), ('II', 'Livre II'), ('III', 'Livre III'), ('IV', 'Livre IV')]
today = datetime.date.today().isoformat()
md = '''# Which Vattel did the colonists cite? Sources of the passages, 1762–1776

*Data report, built by `tools/reports/vattel_american.py` from the edition vattel-1773 %(ver)s (its reuse tables and divergence notes) and from a list of American citations of Vattel compiled from three studies: W. Ossipow and D. Gerber, "The Reception of Vattel's Law of Nations in the American Colonies", *American Journal of Legal History* 57 (2017); M. Somos, "Vattel's Reception in British America, 1761–1775", in P. Schröder (ed.), *Concepts and Contexts of Vattel's Political and Legal Thought* (2021); J. S. Schmeeckle, "Vattel's *The Law of Nations* and the Declaration of Independence" (2006/2016). The list is [data/vattel-american-citations.json](data/vattel-american-citations.json).*

The three studies report %(ncit)d citations of Vattel by American writers between 1762 and 1776. %(nloc)d of them name or quote a passage; together they concern %(nC)d §§. The studies also propose %(nH)d further §§ as sources of documents of 1775–1777 that do not cite Vattel.

## The cited §§ and their sources

Each § is classed by its strongest match in the edition's tables. *Wolff, close*: a close paraphrase, translation or verbatim match in Wolff's *Jus gentium*, *Institutiones* or *Jus naturae* VIII. *Other source*: no close match in Wolff, but a close match in another source, or a loose one where Wolff has none (Grotius, Pufendorf, Barbeyrac's notes, Burlamaqui, Formey, Vattel's earlier works). *Wolff, loose*: a loose paraphrase of Wolff and no close match elsewhere. *No source found*: none of these. *Departs from Wolff*: a divergence note of the edition, where Vattel had Wolff's passage before him and reached the opposite point.

| class | cited §§ | share | citations | share | all §§ of the work | share |
|---|---|---|---|---|---|---|
''' % dict(ver=ver, ncit=len(D['citations']), nloc=sum(1 for x in D['citations'] if x.get('loci')), nC=nC, nH=len(hyp))
for k in 'WOwV':
    md += '| %s | %d | %s | %d | %s | %d | %s |\n' % (LAB[k], cc[k], pct(cc[k], nC), cw[k], pct(cw[k], nW), base['all'][k], pct(base['all'][k], sum(base['all'].values())))
md += '''
%(W)d of the %(nC)d cited §§ have a close match in Wolff. If the cited §§ were drawn from their books at random, about %(exp).0f would. %(nd)d cited §§ depart from a passage of Wolff: %(dep)s.

By book, the share of §§ with a close Wolff match:

| book | cited §§ | Wolff, close | all §§ | Wolff, close |
|---|---|---|---|---|
''' % dict(W=cc['W'], nC=nC, exp=exp, nd=len(dep), dep=', '.join('[%s](../viewer/?ed=%s#%s)' % (u.replace('Prelim.', 'Prél. '), ED, u) for u in sorted(dep, key=order)))
for b, name in books:
    cu = [u for u in cit if bk(u) == b]
    if not cu: continue
    cw_ = sum(1 for u in cu if klass(u) == 'W'); nb = sum(base[b].values())
    md += '| %s | %d | %s | %d | %s |\n' % (name, len(cu), pct(cw_, len(cu)), nb, pct(base[b]['W'], nb))
md += '''
### Cited §§

%s

### §§ proposed as sources of documents of 1775–1777

These §§ are not cited in the documents. The studies propose them as parallels for the Declaration on Taking Up Arms (1775), *Thoughts on Government*, the Virginia Declaration of Rights, the Declaration of Independence and the Articles of Confederation.

%s

## Notes

- The tables are the edition's own (vattel-1773 %s), found by retrieval and judged by a language model, and partly read a second time. A § without a match may still have a source the collection does not hold. The collection has no table for Locke, Montesquieu's other works or the British authors the colonists also read.
- "Cited by" names the writers of the documents, with Ossipow and Gerber's, Somos's and Schmeeckle's attributions. Several writers cited several §§ in one document; each § counts once per document in the citation counts.
- The list follows the three studies. It is not a census of American citations of Vattel.
''' % (tab(cit, 'cited by'), tab(hyp, 'documents'), ver)
open(os.path.join(ROOT, 'reports', RID + '.md'), 'w', encoding='utf-8').write(md)
ip = os.path.join(ROOT, 'reports', 'index.json')
I = json.load(open(ip, encoding='utf-8'))
I['reports'] = [r for r in I['reports'] if r['id'] != RID]
I['reports'].insert(0, {'id': RID, 'kind': 'report', 'title': "Which Vattel did the colonists cite? Sources of the passages, 1762–1776",
    'summary': '%d §§ of Le droit des gens cited by American writers, 1762–1776, traced to their sources: %d to close paraphrases of Wolff, %d departing from him.' % (nC, cc['W'], len(dep)),
    'date': today, 'file': RID + '.md', 'editions': [ED], 'versions': {ED: ver}, 'generator': 'tools/reports/vattel_american.py'})
json.dump(I, open(ip, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(nC, dict(cc), dict(cw), 'expected W %.1f' % exp, 'dep', dep)
