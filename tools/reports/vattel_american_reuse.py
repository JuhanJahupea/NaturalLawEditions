# vattel_american_reuse.py: the data report "Vattel in American documents, 1762–1776: a search of thirty volumes".
# Reads reports/data/vattel-american-reuse.json (built by tools/american/) and writes reports/vattel-american-reuse.md
# and the report's entry in reports/index.json.
import os, json, collections, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ED, RID = 'vattel-1773', 'vattel-american-reuse'
load = lambda p: json.load(open(os.path.join(ROOT, p), encoding='utf-8'))
ver = load('editions/%s/edition.json' % ED)['version']
D = load('reports/data/vattel-american-reuse.json'); X = D['reuses']
REL = {'wolff': 'Wolff, close', 'wolff-loose': 'Wolff, loose', 'other': 'other source', 'own': "Vattel's own",
       'against-wolff': 'against Wolff', 'other+own': "other source and Vattel's own", 'own+other': "Vattel's own and other source"}
LAB = {'quotation': 'quotation', 'verbatim': 'verbatim', 'close paraphrase': 'close paraphrase', 'loose paraphrase': 'loose paraphrase', 'quotes Leonard': 'quotes Leonard'}
sec = lambda u: u.replace('Prelim.', 'Prél. ')
link = lambda u: '[%s](../viewer/?ed=%s#%s)' % (sec(u), ED, u)
docs = sorted({(r['date'], r['doc']) for r in X}); nd = len(docs)
known = [r for r in X if r['in_studies']]; new = [r for r in X if not r['in_studies']]
cnt = lambda rs: collections.Counter(r['relation'] for r in rs)
ck, cn = cnt(known), cnt(new)
silence = [r for r in X if r['unit'] == 'I.34' and r['relation'].startswith('own')]
sadams = {r['doc'] for r in X if 'Samuel Adams' in r['author']}
units = collections.Counter(r['unit'] for r in X)
md = '''# Vattel in American documents, 1762–1776: a search of thirty volumes

*Data report, built by `tools/reports/vattel_american_reuse.py` from [data/vattel-american-reuse.json](data/vattel-american-reuse.json), which `tools/american/` builds. The edition vattel-1773 %(ver)s gives Vattel's English (London, 1797), his French and the sources of each French passage. Thirty volumes and pamphlets were searched against Vattel's English; candidate passages were read by one language model and every match by a second.*

The corpus holds the pamphlets of Otis (1762, 1764, 1765), Thacher, Dulany, Bland, Dickinson (1768, 1774), Jefferson's *Summary View*, Wilson, Hamilton, Seabury and Paine's *Common Sense*; the Boston *Votes and Proceedings* of 1772; Bradford's *Speeches of the Governors of Massachusetts* (1765–1775); the writings of Samuel Adams to 1776; John Adams's diary to 1776, his essays and *Novanglus* with Leonard's *Massachusettensis*; and the *Journals of the Continental Congress*, 1774–1776.

The search finds %(n)d reuses of %(nu)d sections of Vattel in %(nd)d documents, from 1764 to 1775. %(nk)d are among the citations that Ossipow and Gerber, Somos and Schmeeckle report ([Which Vattel did the colonists cite?](?r=vattel-american-sources)); %(nn)d are not. The journals of Congress, *Common Sense*, the *Summary View*, Wilson, Dickinson, Hamilton, Dulany, Seabury and Otis's *Vindications* have none. %(ns)d of the %(nd)d documents are by Samuel Adams or by the House in his drafting.

No document in the corpus names Wolff.

## Sources of the reused passages

For each reuse, the second reader found the French words that the English renders and the edition's sources for those words. *Wolff, close*: a close paraphrase or translation of Wolff covers them. *Wolff, loose*: only a loose paraphrase of Wolff. *Against Wolff*: a divergence note, where Vattel had Wolff's passage before him and reached the opposite point. *Other source*: Grotius, Pufendorf or Burlamaqui only. *Vattel's own*: no source in the tables.

| source of the French words | reported in the studies | found here only |
|---|---|---|
''' % dict(ver=ver, n=len(X), nu=len(units), nd=nd, nk=len(known), nn=len(new), ns=len(sadams))
for k in ('wolff', 'wolff-loose', 'against-wolff', 'other', 'own', 'other+own', 'own+other'):
    if ck[k] or cn[k]: md += '| %s | %d | %d |\n' % (REL[k], ck[k], cn[k])
md += '''
All %(w)d reuses of passages that Vattel took closely from Wolff are among those the studies report. None of the %(nn)d reuses found here only is one. They render sentences of Vattel's own or of Grotius, Pufendorf and Burlamaqui, or loose paraphrases of Wolff.

The last sentence of [I § 34](../viewer/?ed=%(ed)s#I.34), on a nation's silence as consent to a change of its constitution, has no source in the tables. Four documents of 1768–1771 use it: %(sll)s. The House's answer to Hutchinson of 26 January 1773 restates it without the words: the Governor's speech had left the House the choice "either of appearing by our silence to acquiesce in your Excellency's sentiments, or of thus freely discussing this point" (Bradford, 364).

## The reuses

| date | document | § | form | Vattel named | source of the French words | in the studies | pages | 1760 / 1797 |
|---|---|---|---|---|---|---|---|---|
''' % dict(w=ck['wolff'] + cn['wolff'], nn=len(new), ed=ED, sl=len(silence),
           sll='; '.join('%s, %s (%s)' % (r['author'].split(' (')[0], r['document'], r['pages']) for r in silence))
for r in X:
    md += '| %s | %s, %s | %s | %s | %s | %s | %s | %s | %s |\n' % (r['date'], r['author'], r['document'], link(r['unit']), LAB.get(r['label'], r['label']),
        'yes' if r['named'] else '', REL.get(r['relation'], r['relation']), 'yes' if r['in_studies'] else '', r['pages'],
        '%.2f / %.2f' % (r['en1760'], r['en1797']) if r.get('en1760') is not None else '')
tr = [r for r in X if r.get('en1760') is not None and r['label'] in ('quotation', 'verbatim', 'close paraphrase')]
n60 = sum(1 for r in tr if r['en1760'] > r['en1797'] + 0.1); n97 = sum(1 for r in tr if r['en1797'] > r['en1760'] + 0.1)
md += '''
## Which English

The first English translation (London, 1760; vol. II dated 1759) was compared with each quotation and paraphrase: the share of its word sequences of four found in the 1760 text, and in the section's text of 1797. Of %(n)d, %(n60)d share more with 1760 and %(n97)d more with 1797. The two nearer 1797 are Hutchinson's I § 210 and Samuel Adams's I § 223; in both the 1760 copy's OCR prints a word that breaks the comparison ("mothercountry"; a marginal note run into the text). No American text follows a reading peculiar to 1797.

- I § 210 in 1760 has both sentences, in the words of Otis's memorial: "antient possessions", "ought also to extend to its colonies". Hutchinson's quotation leaves out the second sentence and the words "a colony".
- I § 34 in 1760 has the memorial's and the House's words: "It is here demanded whether, if their power extends so far as to the fundamental laws", "the constitution of the state ought to be fixed" (1797: "It is asked whether their power extends to the fundamental laws", "ought to possess stability"). Somos's remark that the 1764 memorial was "not using the 1760 English translation" (2021, 210) does not hold.
- I § 24 in 1760 reads "it has cost rivers of blood". Thacher's "seas of blood" is his.
- III § 201 stands in chapter XIII in 1760, as in the French. Otis's "B. 3. C. 10." is a slip; Ossipow and Gerber's text gives the same chapter (2017, 534), their table XIII.
- I § 36 in 1760 reads "to judge and determine them, in conformity to its political constitution", the House's words of 1768 (1797: "conformably to"). II § 265 reads "neither the one nor the other of the interested, or contracting powers, has a right to interpret the act, or treaty, at his pleasure", the House's words of 1773 (1797: "according to his own fancy").

## The Declaration of Independence

The *Journals* hold Jefferson's draft and the adopted text. No passage of either shares wording with Vattel: the nearest sections reach a cosine of 0.11 to 0.14, against 0.25 to 0.55 for the quotations above. The sections that Ossipow and Gerber and Schmeeckle propose as its sources share a phrase or nothing.

One sentence joins Locke and Vattel. "All experience hath shewn, that mankind are more disposed to suffer, while evils are sufferable, than to right themselves by abolishing the forms to which they are accustomed" takes Locke's "the people, who are more disposed to suffer than right themselves by resistance, are not apt to stir" (*Second Treatise* § 230) and adds "while evils are sufferable". That clause is the distinction of [III § 290](../viewer/?ed=%(ed)s#III.290), which the 1760 translation words "Every citizen should even patiently suffer supportable evils, rather than disturb the public peace" (1797: "patiently endure evils which are not insupportable"). Bland had paraphrased the same sentence at Williamsburg in 1766: "to suffer patiently rather than disturb the publick Peace". Samuel Adams quoted another passage of III § 290 in 1772. Schmeeckle proposes III § 290 for the Declaration's sentence; the wording shows a shared verb and noun, not a quotation.

''' % dict(n=len(tr), n60=n60, n97=n97, ed=ED)
md += '''
## Checks

- Every quotation of Vattel that the three studies report in these volumes was found, except the House's quotation of [II § 265](../viewer/?ed=%(ed)s#II.265) in its answer of 26 January 1773, which the search for the wording of [II § 283](../viewer/?ed=%(ed)s#II.283) beside it brought up, and Samuel Adams's phrase of 1776 "with M. de Vattel, I account a state a moral person".
- The studies propose further silent sources in these volumes: Bland and Préliminaires §§ 4–5, the Circular Letter of 1768 and I § 34, Novanglus and I § 9, the Declaration on Taking Up Arms and III §§ 51–52, the Declaration of Independence. The search finds no shared wording at those places. Adams's "Distinct states may be united under one king" (Novanglus VII) states the point of I § 9 without its words.
- A probe of 36 candidates below the threshold gave no match.
- Three uses of the silence clause (the House to Franklin, 29 June 1771; Candidus, 19 August 1771) and the House's quotation of II § 265 were found by searching the corpus for the wording of verified matches, not by the retrieval.
- Several documents stand in two volumes (Bradford and Cushing; Adams's *Works* and the 1819 *Novanglus*). Each counts once.
- The pages are those of the editions named; Cushing is *The Writings of Samuel Adams* (1904–1906).
''' % dict(ed=ED)
open(os.path.join(ROOT, 'reports', RID + '.md'), 'w', encoding='utf-8').write(md)
ip = os.path.join(ROOT, 'reports', 'index.json')
I = json.load(open(ip, encoding='utf-8'))
I['reports'] = [r for r in I['reports'] if r['id'] != RID]
I['reports'].insert(0, {'id': RID, 'kind': 'report', 'title': 'Vattel in American documents, 1762–1776: a search of thirty volumes',
    'summary': '%d reuses of Vattel in %d documents, %d of them not reported before. Every reuse of a passage Vattel took closely from Wolff was known; the new ones are of Vattel\'s own sentences, above all the silence clause of I § 34.' % (len(X), nd, len(new)),
    'date': datetime.date.today().isoformat(), 'file': RID + '.md', 'editions': [ED], 'versions': {ED: ver}, 'generator': 'tools/reports/vattel_american_reuse.py'})
json.dump(I, open(ip, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(X), nd, len(known), len(new), dict(ck), dict(cn), len(silence))
