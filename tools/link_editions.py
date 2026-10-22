# Give each row of a reuse table whose `to` text is an edition the unit of that edition that holds the source passage.
# Usage: python tools/link_editions.py   (after the converters; rewrites the tables in reuse/ in place)
# Method: the row's page id gives the scan; the candidate units are those printed on that scan or the next; the passage
# picks among them by shared 5-letter sequences (accents folded, long s and f read as one letter, as in the OCR).
import collections, json, os, re, unicodedata
from nle import ROOT, load

MIN_SCORE = 0.5


def key(s):
    out = []
    for ch in s.lower():
        if ch in 'æ': out.append('ae'); continue
        if ch in 'œ': out.append('oe'); continue
        c = unicodedata.normalize('NFD', ch)[0]
        if c in 'ſf': c = 's'
        if 'a' <= c <= 'z': out.append(c)
    return ''.join(out)


def grams(k, n=5): return {k[i:i + n] for i in range(len(k) - n + 1)}


def unit_text(u): return ' '.join([u['text'], u.get('margin', '')] + [n['text'] for n in u.get('notes', [])])


cat = load(os.path.join(ROOT, 'catalogue.json'))
editions = {e['id']: e for e in cat['editions']}
report = []
for entry in cat['reuse']:
    if entry['to'] not in editions: continue
    T = load(os.path.join(ROOT, editions[entry['to']]['path'], 'text.json'))
    on_scan = collections.defaultdict(list); G = {}
    for u in T['units']:
        scans = {p['scan'] for p in u.get('pages', [])} | {b[2] for b in u.get('pb', [])}
        for s in scans: on_scan[s].append(u['id'])
        G[u['id']] = grams(key(unit_text(u)))
    path = os.path.join(ROOT, entry['path']); tb = load(path)
    scores = []; rows = []
    for r in tb['rows']:
        r = {k: v for k, v in r.items() if k not in ('toUnit', 'toScore')}
        m = re.search(r'\.(?:pdf|p|s)(\d+)$', r['page'])
        link = {}
        if m:
            scan = int(m.group(1)); q = grams(key(r['source']))
            cand = [(sum(1 for g in q if g in G[uid]) / max(1, len(q)), d == 0, uid)
                    for d in (0, 1, -1) for uid in on_scan.get(scan + d, [])]
            if cand:
                best = max(cand); scores.append(best[0])
                if best[0] >= MIN_SCORE: link = {'toUnit': best[2], 'toScore': round(best[0], 2)}
        # the new fields go after `source`
        rows.append(dict(sum(([(k, v)] + (list(link.items()) if k == 'source' else []) for k, v in r.items()), [])))
    head = {k: v for k, v in tb.items() if k not in ('rows', 'toUnits')}
    head['toUnits'] = ('toUnit: the unit of %s that holds the source passage, found from the page id and the passage '
                       '(share of its 5-letter sequences found in the unit, toScore >= %.1f).' % (entry['to'], MIN_SCORE))
    head['rows'] = rows; tb = head
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(tb, f, ensure_ascii=False, separators=(',', ':')); f.write('\n')
    n = sum('toUnit' in r for r in tb['rows'])
    report.append((entry['path'], len(tb['rows']), n, sorted(scores)[:5]))
for p, total, n, low in report: print(p, 'rows', total, 'linked', n, 'lowest scores', [round(x, 2) for x in low])

# A later text that repeats an edition (Burlamaqui's PDP 1751 repeats his 1747 text) carries reuse into that edition.
# For a row whose source is such a text, `repeats` names the unit of the edition the source passage repeats:
#   route "table": the edition's own table for the later text has a row on the same page whose passage overlaps (>= 0.5);
#   route "text":  else, the source passage's wording stands in one unit of the edition (>= 0.7, passage of 25 sequences or more).
TABLE_MIN, TEXT_MIN, MIN_GRAMS = 0.5, 0.7, 25
def page_key(p):
    m = re.search(r'(T\d)?\.(?:pdf|p|s)(\d+)$', p); return (m.group(1) or '', int(m.group(2))) if m else None
derived = {}
for entry in cat['reuse']:
    if entry['to'] in editions: continue
    t = load(os.path.join(ROOT, entry['path']))
    if t.get('direction') == 'derivative' and entry['from'] in editions: derived[entry['to']] = (entry['from'], t['rows'])
for entry in cat['reuse']:
    entry.pop('repeats', None)
    if entry['to'] not in derived or entry['from'] == derived[entry['to']][0]: continue
    ed, drows = derived[entry['to']]
    T = load(os.path.join(ROOT, editions[ed]['path'], 'text.json'))
    UG = {u['id']: grams(key(unit_text(u))) for u in T['units'] if u['kind'] != 'heading'}
    by_page = collections.defaultdict(list)
    for d in drows: by_page[page_key(d['page'])].append(d)
    path = os.path.join(ROOT, entry['path']); tb = load(path); n = collections.Counter()
    for r in tb['rows']:
        r.pop('repeats', None)
        q = grams(key(r['source'])); best = None
        for d in by_page.get(page_key(r['page']), []):
            g = grams(key(d['source'])); o = len(q & g) / max(1, min(len(q), len(g)))
            if o >= TABLE_MIN and d['unit'] in UG and (best is None or o > best[1]): best = (d['unit'], o, 'table')
        if best is None and len(q) >= MIN_GRAMS:
            s, uid = max((len(q & g) / len(q), uid) for uid, g in UG.items())
            if s >= TEXT_MIN: best = (uid, s, 'text')
        if best:
            r['repeats'] = {'edition': ed, 'unit': best[0], 'route': best[2], 'score': round(best[1], 2)}; n[best[2]] += 1
    tb['repeatsNote'] = ('repeats: the unit of %s that the source passage repeats. Route "table": a row of %s on the same page '
                         'with an overlapping passage (>= %.1f). Route "text": the passage stands in that unit (>= %.1f).') % (ed, ed, TABLE_MIN, TEXT_MIN)
    tb = {k: v for k, v in tb.items() if k != 'rows'} | {'rows': tb['rows']}
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(tb, f, ensure_ascii=False, separators=(',', ':')); f.write('\n')
    if n: entry['repeats'] = ed
    print(entry['path'], 'rows', len(tb['rows']), 'repeat', ed, dict(n))
with open(os.path.join(ROOT, 'catalogue.json'), 'w', encoding='utf-8') as f:
    json.dump(cat, f, ensure_ascii=False, indent=2); f.write('\n')
