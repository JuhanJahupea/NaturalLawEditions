# def41_merge.py <batches dir> <judge dir> [<check dir>]: the reuse rows of Vattel's Défense du système leibnitien (1741)
# from the judges (DEF41_JUDGE_PROMPT.md) and, if given, the second readers (DEF41_CHECK_PROMPT.md), plus Roques's
# letters from texts/roques-lettres-1737-1739/ROQ.json, into editions/vattel-defense-1741/provenance/reuse/<to>.json, one
# file per source text (format nle-reuse-rows/1: the rows of nle-reuse/1 before the edition build places them).
#  - A judge's passage must stand in its unit (text or the note named), a source passage in its segment: exact, or after
#    folding spaces, _ marks and [p. N]; otherwise fuzzy at 0.9 or more; rows that fail are listed and left out.
#  - status: match (confidence >= 0.5), possible (0.3-0.5); rows under 0.3 are left out. A second reader's verdict
#    (keep / weak / drop, with a label and confidence) replaces the judge's and is kept in `review`.
#  - Roques: verbatim passages are quotations (confidence 1); reported passages are citations (0.9).
import sys, os, re, json, glob, difflib, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
BD, JD = sys.argv[1], sys.argv[2]; CD = sys.argv[3] if len(sys.argv) > 3 else None
TODAY = datetime.date.today().isoformat()
SRC = {'EXA37': ('crousaz-examen-1737', 'Cr', 'Crousaz, Examen de l\'Essay de M. Pope sur l\'homme (1737)'),
       'COM38': ('crousaz-commentaire-1738', 'Cr', 'Crousaz, Commentaire sur la traduction de Du Resnel (1738)'),
       'THEO': ('leibniz-theodicee-1734', 'L', 'Leibniz, Essais de théodicée (1734)'),
       'PSR34': ('wolff-psychologia-rationalis-1734', 'W', 'Wolff, Psychologia rationalis (1734)')}
SEG = json.load(open(os.path.join(BD, 'segments.json')))
ITEMS = {}
for f in glob.glob(os.path.join(BD, 'b*.json')):
    for it in json.load(open(f))['items']: ITEMS[it['unit']] = it
norm = lambda t: re.sub(r'\s+', ' ', re.sub(r'\[p\. [^\]]*\]', ' ', t).replace('_', '')).strip()
def found(needle, hay):
    if needle in hay: return 1.0
    n, h = norm(needle), norm(hay)
    if n in h: return 1.0
    if len(n) < 12: return 0.0
    sm = difflib.SequenceMatcher(None, h, n, autojunk=False); best = 0.0
    for b in sm.get_matching_blocks():
        if b.size < 8: continue
        a = max(0, b.a - b.b); best = max(best, difflib.SequenceMatcher(None, h[a:a + len(n)], n, autojunk=False).ratio())
    return best
def hay_of(it, where):
    if where in ('', 'text', None): return it['text']
    mk = re.sub(r'note\s*', '', where).replace(' ', '')
    t = [n['text'] for n in it['notes'] if n['mark'].replace(' ', '') == mk]
    return ' '.join(t) if t else ' '.join(n['text'] for n in it['notes'])
REV = {}
if CD:
    for f in glob.glob(os.path.join(CD, '*.json')):
        for v in json.load(open(f))['verdicts']: REV[v['key']] = v
# Rows the second reader dropped as pointing to the wrong segment, where it named the segment that holds the words: the
# row is moved there (source passage checked by hand in that segment).
RETARGET = {
    'b005.2': ('THEO.T.353', 'dans ce système tout est lié et harmonique', 'close paraphrase', 0.7),
    'b012.16': ('THEO.T.303', 'ce petit détour des atomes, arrivant sans sujet et sans raison au sentiment d’Épicure', 'close paraphrase', 0.6),
    'b014.13': ('THEO.T.231', 'Dieu décerna de l’admettre à l’existence tel qu’il l’a vu : ce décret ne change point la nature des objets', 'close paraphrase', 0.8)}
rows, bad = {}, []
for f in sorted(glob.glob(os.path.join(JD, 'b*.json'))):
    b = os.path.basename(f)[:-5]
    for i, r in enumerate(json.load(open(f)).get('rows', [])):
        key = '%s.%d' % (b, i)
        if key in RETARGET:
            sg, sp, lb, cf = RETARGET[key]
            r = dict(r, seg=sg, source_passage=sp, label=lb, confidence=cf,
                     reason=r.get('reason', '') + ' [Moved to %s after the check: the words stand there.]' % sg)
        it = ITEMS.get(r.get('unit')); seg = SEG.get(r.get('seg', ''))
        if not it or not seg: bad.append((key, 'unit or segment unknown', r.get('unit'), r.get('seg'))); continue
        fp = found(r['passage'], hay_of(it, r.get('where', 'text'))); fs = found(r['source_passage'], seg['text'])
        if fp < 0.9 or fs < 0.9: bad.append((key, 'passage %.2f source %.2f' % (fp, fs), r['unit'], r['seg'])); continue
        conf, label = float(r.get('confidence', 0)), r.get('label', '')
        review = None
        if key in REV:
            v = REV[key]; review = {'step': 'C', 'verdict': v['verdict'], 'reason': v.get('reason', ''), 'date': TODAY}
            if v['verdict'] == 'drop' and key not in RETARGET: continue
            if key in RETARGET: v = dict(v, verdict='keep', confidence=r['confidence'], label=r['label'])
            conf = float(v.get('confidence') or conf); label = v.get('label') or label
            if v['verdict'] == 'weak': conf = min(conf, 0.45)
        if conf < 0.3: continue
        src = seg['src']; tid, fam, work = SRC[src]
        row = {'key': key, 'unit': r['unit'], 'where': r.get('where', 'text'), 'family': fam, 'work': work,
               'locus': seg['locus'], 'page': r['seg'], 'label': label, 'confidence': round(conf, 2),
               'status': 'match' if conf >= 0.5 else 'possible', 'step': 'C' if review else 'J',
               'passage': norm(r['passage']), 'source': norm(r['source_passage']), 'reason': r.get('reason', '')}
        for k in ('stance', 'quoting', 'via'):
            if r.get(k): row[k] = r[k]
        if r.get('named'): row['attributed'] = r['named']
        if review: row['review'] = review
        if fp < 1 or fs < 1: row['fuzzy'] = [round(fp, 3), round(fs, 3)]
        rows.setdefault(tid, []).append(row)
roq = json.load(open(os.path.join(ROOT, 'texts', 'roques-lettres-1737-1739', 'ROQ.json')))
for q in roq['passages']:
    verb = q['kind'] == 'verbatim'
    row = {'key': q['id'], 'unit': q['at']['unit'], 'where': q['at']['where'], 'family': 'Ro',
           'work': 'Roques, %s (%s, %s)' % (q['title'], q['journal'], q['issue']),
           'locus': 'lettre %d%s' % (q['letter'], ', p. %s' % q['page'] if q['page'] else ''), 'page': q['id'],
           'label': 'quotation' if verb else 'citation', 'confidence': 1.0 if verb else 0.9, 'status': 'match', 'step': 'Q',
           'passage': q['text'], 'source': q['text'] if verb else '',
           'reason': 'Vattel quotes Roques\'s letter' if verb else 'Vattel reports what Roques says'}
    if q.get('embedded'): row['quoting'] = ', '.join(sorted({e.get('author', '') for e in q['embedded'] if e.get('author')}))
    rows.setdefault('roques-lettres-1737-1739', []).append(row)
od = os.path.join(ROOT, 'editions', 'vattel-defense-1741', 'provenance', 'reuse'); os.makedirs(od, exist_ok=True)
STEPS = {'J': 'Judge: Claude Sonnet read each unit with candidate passages of the source (cited loci, shared runs of words, nearest by vocabulary) and wrote the rows',
         'C': 'Check: Claude Opus read the row again with the whole unit and the source segment',
         'Q': 'Quotation: Roques\'s letters exist only as Vattel quotes them; each quoted or reported passage is a row'}
from collections import Counter
nid = 0
for tid, rr in sorted(rows.items()):
    rr.sort(key=lambda r: (r['unit'].split('.')[0] != 'Ded', r['unit'].split('.')[0] != 'Pref', int(re.sub(r'\D', '', r['unit']) or 0)))
    for r in rr: r['id'] = nid; nid += 1
    doc = {'format': 'nle-reuse-rows/1', 'from': 'vattel-defense-1741', 'to': tid, 'steps': STEPS,
           'description': 'Reuse rows of step 4, before the edition build places the passages on the text. status match: confidence >= 0.5; possible: 0.3-0.5.',
           'rows': rr}
    json.dump(doc, open(os.path.join(od, tid + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(tid, len(rr), 'rows', dict(Counter(r['status'] for r in rr)), dict(Counter(r['label'] for r in rr)))
print('left out (passage or source not found):', len(bad)); [print('  ', b) for b in bad[:30]]
