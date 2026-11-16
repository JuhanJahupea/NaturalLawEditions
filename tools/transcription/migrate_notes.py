# migrate_notes.py <data.json> <edition> [--since K] [--write]: after editions/<edition>/corrections.json moves footnotes, the
# later-pass files that point into notes by unit and note index are remapped: pass rows (unit, at), attributions (unit, cuePart),
# divergence items (unit, when their passage stands in a moved note). --since K: the pass files already follow the first K
# moves; only the later ones are applied. Without --write it only reports.
import json, glob, re, sys, copy, html, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
R = ROOT
sys.path.insert(0, R + '/tools'); import nle
dataf, ed = sys.argv[1:3]; write = '--write' in sys.argv
K = int(sys.argv[sys.argv.index('--since') + 1]) if '--since' in sys.argv else 0
E = R + '/editions/' + ed
C = json.load(open(E + '/corrections.json'))['noteMoves']
D0 = json.load(open(dataf)); OLD = {s['id']: copy.deepcopy(s) for s in D0['sections']}
Db = copy.deepcopy(D0); Df = copy.deepcopy(D0)
dest_b, nmap_b = nle.apply_note_moves(Db['sections'], Db['rows'], C[:K])
dest_f, nmap_f = nle.apply_note_moves(Df['sections'], Df['rows'], C)
inv_b = {v: k for k, v in nmap_b.items()}
NEW = {s['id']: s for s in Df['sections']}; BASE = {s['id']: s for s in Db['sections']}
def plain(h): return html.unescape(re.sub(r'<[^>]+>', '', h))
def remap(unit, part):
    if not part.startswith('n'): return unit, part
    orig = inv_b.get((unit, int(part[1:])), (unit, int(part[1:])))
    u, i = nmap_f.get(orig, orig); return u, 'n%d' % i
rowunit = {}
for f in sorted(glob.glob(E + '/passes/*.json')):
    P = json.load(open(f)); ch = 0; name = f.split('/')[-1]
    for r in P.get('rows', []):
        if not r.get('at'): continue
        new = [remap(r['unit'], a[0]) for a in r['at']]; units = {u for u, _ in new}
        if len(units) > 1: print('SPLIT row', name, r['id'], r['unit'], r['at']); continue
        nu = units.pop()
        if nu != r['unit'] or any(p != a[0] for (u, p), a in zip(new, r['at'])):
            rowunit[(P['text'], r['unit'], r['page'], r['passage'], r['source'])] = nu
            r['unit'] = nu; r['at'] = [[p, a[1], a[2]] for (u, p), a in zip(new, r['at'])]; ch += 1
    for d in P.get('items', []):
        o = BASE.get(d['unit'])
        if not o: continue
        for i, n in enumerate(o['notes']):
            u2, p2 = remap(d['unit'], 'n%d' % i)
            if u2 != d['unit'] and d['passage'][:60] in plain(n['html']):
                print('DIV moves', name, d['unit'], '->', u2); d['unit'] = u2; ch += 1; break
    if write and ch:
        pretty = open(f).read().startswith('{\n')
        with open(f, 'w', encoding='utf-8') as fh:
            json.dump(P, fh, ensure_ascii=False, indent=1) if pretty else json.dump(P, fh, ensure_ascii=False, separators=(',', ':')); fh.write('\n')
    print(name, ch, 'changed')
moved_now = {rid: u for rid, u in dest_f.items() if dest_b.get(rid) != u}
rows_f = {r['id']: r for r in Df['rows']}
for rid, u in moved_now.items(): print('working row', rid, 'now in', u)
AP = E + '/passes/attributions.json'
if os.path.exists(AP):
    A = json.load(open(AP)); ch = 0; drop = []
    for a in A['attributions']:
        key = (a['text'], a['unit'], a['page'], a['passage'], a['source'])
        nu = rowunit.get(key)
        if nu is None:
            for rid, u in moved_now.items():
                r = rows_f[rid]
                if r['vp'] == a['passage'] and r['sp'] == a['source'] and r['page'] == a['page']: nu = u
        cu, cp = remap(a['unit'], a['cuePart']); nu = nu or a['unit']
        if cu != nu:
            u = NEW[nu]; parts = [('t', plain(u['html']))] + [('n%d' % i, plain(n['html'])) for i, n in enumerate(u['notes'])]
            hit = next((p for p, t in parts if a['cue'] in t), None)
            if hit: print('cue found again', a['unit'], '->', nu, hit); cu, cp = nu, hit
            else: print('CUE LEFT', a['unit'], a['text'], repr(a['cue'][:50]), 'row unit', nu, 'cue unit', cu); drop.append(a); continue
        if (nu, cp) != (a['unit'], a['cuePart']): a['unit'], a['cuePart'] = nu, cp; ch += 1
    print('attributions changed', ch, 'to drop', len(drop))
    if write:
        A['attributions'] = [a for a in A['attributions'] if a not in drop]
        with open(AP, 'w', encoding='utf-8') as f: json.dump(A, f, ensure_ascii=False, indent=1); f.write('\n')
