# note_clusters.py <out>: units whose number of footnote calls differs from their number of notes, grouped with the
# neighbouring units that share a printed page. Each cluster lists its pages (with MDZ scans) and, per unit, the calls
# (mark and the page they stand on) and the notes (mark and opening words).
import os, json, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
U = json.load(open(R + '/editions/vattel-1773/text.json'))['units']
def strip(h): return re.sub(r'<[^>]+>', '', h)
CALL = re.compile(r'[\(\[]\s*(\*+|[a-z†])\s*[\)\]]')
MDZ = {'T1': 'bsb10725331', 'T2': 'bsb10725332'}
def call_pages(u):
    t = u['text']; pbs = u.get('pb', []); first = u['pages'][0]
    out = []
    plain_pos = []  # pb positions refer to the text offsets in text.json units
    for m in CALL.finditer(t):
        pg = first; 
        for b in pbs:
            if b[0] <= m.start(): pg = {'vol': b[1], 'scan': b[2], 'printed': b[3]}
        out.append({'mark': m.group(1), 'page': pg.get('printed'), 'scan': pg['scan'], 'context': strip(t[max(0, m.start() - 80):m.start() + 6])})
    return out
info = []
for k, u in enumerate(U):
    calls = call_pages(u); notes = [n for n in u.get('notes', []) if n['mark'] not in ('cont', '')]
    info.append({'k': k, 'id': u['id'], 'calls': calls, 'notes': [{'index': i, 'mark': n['mark'], 'text': strip(n['text'])[:220]} for i, n in enumerate(u.get('notes', []))],
                 'nnotes': len(notes), 'pages': [(p.get('vol'), p['scan'], p['printed']) for p in u['pages']]})
bad = [x for x in info if len(x['calls']) != x['nnotes']]
share = lambda a, b: bool(set(a['pages']) & set(b['pages']))
clusters = []
for x in bad:
    k = x['k']; lo, hi = k, k
    while lo > 0 and share(info[lo - 1], info[lo]) and (len(info[lo - 1]['calls']) != info[lo - 1]['nnotes'] or lo == k): lo -= 1
    while hi + 1 < len(info) and share(info[hi], info[hi + 1]) and (len(info[hi + 1]['calls']) != info[hi + 1]['nnotes'] or hi == k): hi += 1
    rng = (lo, hi)
    if clusters and clusters[-1][1] >= lo: clusters[-1] = (clusters[-1][0], max(hi, clusters[-1][1]))
    else: clusters.append(rng)
out = []
for lo, hi in clusters:
    us = info[lo:hi + 1]; pages = sorted({p for u in us for p in u['pages']}, key=lambda p: (p[0], p[1]))
    out.append({'cluster': len(out), 'units': [{k: u[k] for k in ('id', 'calls', 'notes', 'pages')} for u in us],
                'scans': [{'vol': v, 'scan': s, 'printed': pr, 'image': 'https://api.digitale-sammlungen.de/iiif/image/v2/%s_%05d/full/1400,/0/default.jpg' % (MDZ[v], s)} for v, s, pr in pages]})
json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(bad), 'unbalanced units in', len(out), 'clusters;', sum(len(c['scans']) for c in out), 'pages')
print([ [u['id'] for u in c['units']] for c in out])
