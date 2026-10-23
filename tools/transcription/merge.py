# merge.py <edition> <WORK> <judge dir[,judge dir...]> <old table> <first id> <out>: judge outputs -> reuse rows in the collection shape.
# A page outside the item's candidates is kept when it was in the batch the judge read (judges used it for a cited locus).
# Every passage is placed on the unit's text, notes or margin and every source passage on its page part; rows that fail are reported.
import sys, os, re, json, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
from merge_find import find
R = ROOT
ed, work, jd, old, first, out = sys.argv[1:7]; first = int(first)
units = {u['id']: u for u in json.load(open('%s/editions/%s/text.json' % (R, ed)))['units']}
oldt = json.load(open(old)); oldrows = oldt['rows']
WORKNAME = collections.Counter(r['work'] for r in oldrows).most_common(1)[0][0]
FAM = {'GRO24': 'G', 'PUF34': 'P'}[work]
ZOT = {'GRO24T1': 'S9FQXVJC', 'GRO24T2': 'LL8RR8X3', 'PUF34T1': 'L42CQ82S', 'PUF34T2': 'S7XSE8FS'}
IA = {'GRO24T1': 'le-droit-de-la-guerre-t-1-grotius', 'GRO24T2': 'le-droit-de-la-guerre-t-2',
      'PUF34T1': 'ledroitdelanatur01pufe', 'PUF34T2': 'ledroitdelanatur02pufe'}
LABELS = {'verbatim', 'close paraphrase', 'loose paraphrase', 'commonplace', 'citation', 'open disagreement'}

def place(u, passage):
    hs = [('t', u['text'])] + [('n%d' % i, n['text']) for i, n in enumerate(u.get('notes', []))]
    for p, h in hs:
        f = find(h, passage)
        if f: return [[p, f[0], f[1]]], h[f[0]:f[1]], f[2]
    f = find(u.get('margin', ''), passage)
    if f: return [], u['margin'][f[0]:f[1]], f[2]
    return None, None, 0

rows = []; fails = collections.Counter(); failed = []
offlist = 0
for fin in [f for d in jd.split(',') for f in sorted(glob.glob(d + '/in/b*.json'))]:
    fo = fin.replace('/in/', '/out/')
    if not os.path.exists(fo): fails['missing batch'] += 1; continue
    I = json.load(open(fin)); O = json.load(open(fo))
    items = {it['unit']: it for it in I['items']}
    for m in O.get('matches', []):
        u = units.get(m.get('unit'))
        if not u or m['unit'] not in items: fails['unit'] += 1; failed.append(m); continue
        if m.get('page_id') not in I['pages']: fails['page'] += 1; failed.append(m); continue
        if m['page_id'] not in items[m['unit']]['candidates']: offlist += 1
        if m.get('label') not in LABELS: fails['label'] += 1; failed.append(m); continue
        at, vp, vq = place(u, m.get('passage', ''))
        if at is None: fails['passage'] += 1; failed.append(m); continue
        parts = I['pages'][m['page_id']]['parts']
        k = m.get('k'); order = ([parts[k]] if isinstance(k, int) and 0 <= k < len(parts) else []) + parts
        sp = None
        for pt in order:
            f = find(pt['text'], m.get('source_passage', ''))
            if f: sp = (pt, pt['text'][f[0]:f[1]], f[2]); break
        if not sp: fails['source'] += 1; failed.append(m); continue
        pt, stext, sq = sp
        conf = float(m.get('confidence', 0))
        if conf < 0.3: fails['below 0.3'] += 1; continue
        vol, scan = m['page_id'].split('.p'); scan = int(scan)
        row = {'unit': u['id'], 'at': at}
        if not at: row['where'] = 'margin'
        row.update({'family': 'Bb' if pt['part'] == 'note' and pt.get('by') == 'Barbeyrac' else FAM, 'work': WORKNAME, 'locus': pt['locus'],
                    'page': m['page_id'], 'inNote': pt['part'] == 'note', 'label': m['label'], 'confidence': round(conf, 2),
                    'status': 'match' if conf >= 0.5 else 'possible', 'step': 'T', 'passage': vp, 'source': stext,
                    'reason': m.get('reason', ''),
                    'links': [['Zotero p. %d' % scan, 'zotero://open-pdf/library/items/%s?page=%d' % (ZOT[vol], scan)],
                              ['archive.org', 'https://archive.org/details/%s/page/n%d/mode/1up' % (IA[vol], scan - 1)]]})
        if m.get('quoting'): row['quoting'] = m['quoting']
        row['_q'] = (vq, sq)
        rows.append(row)

# one row per reused stretch and page: drop a row whose span lies inside a stronger row's span on the same page
def span(r): return (r['at'][0][0], r['at'][0][1], r['at'][0][2]) if r['at'] else ('m', 0, 0)
rows.sort(key=lambda r: (-r['confidence'], r['unit']))
keep = []
for r in rows:
    p, a, b = span(r)
    dup = any(k['unit'] == r['unit'] and k['page'] == r['page'] and span(k)[0] == p and
              min(b, span(k)[2]) - max(a, span(k)[1]) >= 0.8 * min(b - a, span(k)[2] - span(k)[1]) for k in keep)
    if dup: fails['duplicate'] += 1; continue
    keep.append(r)

# earliest witness: carried over from an old row on the same unit whose passage overlaps
def ov(r, o):
    if not r['at'] or not o['at'] or r['at'][0][0] != o['at'][0][0]: return 0
    a, b = r['at'][0][1:]; c, d = o['at'][0][1:]
    return max(0, min(b, d) - max(a, c)) / max(1, min(b - a, d - c))
carried = 0
for r in keep:
    best = max((o for o in oldrows if o['unit'] == r['unit'] and o.get('earliest')), key=lambda o: ov(r, o), default=None)
    if best and ov(r, best) >= 0.5: r['earliest'] = best['earliest']; carried += 1

uorder = {u: i for i, u in enumerate(units)}
keep.sort(key=lambda r: (uorder[r['unit']], span(r)[0] != 't', span(r)[1]))
for i, r in enumerate(keep): r['id'] = first + i
fuzzy = sum(1 for r in keep if min(r['_q']) < 1)
final = [{k: r[k] for k in ['id'] + [k for k in r if k not in ('id', '_q')]} for r in keep]
json.dump({'rows': final, 'failed': failed}, open(out, 'w'), ensure_ascii=False, indent=0)
lab = collections.Counter(r['label'] for r in final)
print(ed, work, len(final), 'rows;', sum(r['status'] == 'match' for r in final), 'match;', dict(lab))
print('  fails', dict(fails), '; off-list pages', offlist, '; fuzzy-placed', fuzzy, '; earliest carried', carried, '; units', len({r['unit'] for r in final}),
      '; families', dict(collections.Counter(r['family'] for r in final)))
