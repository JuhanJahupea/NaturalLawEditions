# migrate_notes.py <data.json> [--write]: after editions/vattel-1773/corrections.json moves footnotes, the later-pass files
# that point into notes by unit and note index are remapped: pass rows (unit, at), attributions (unit, cuePart), divergence
# items (unit, when their passage stands in a moved note). Without --write it only reports.
import json, glob, re, sys, copy, html, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))); import nle
R = ROOT + '/editions/vattel-1773'
D = json.load(open(sys.argv[1])); write = '--write' in sys.argv
OLD = {s['id']: copy.deepcopy(s) for s in D['sections']}
C = json.load(open(R + '/corrections.json'))['noteMoves']
dest, nmap = nle.apply_note_moves(D['sections'], D['rows'], C)
NEW = {s['id']: s for s in D['sections']}
def plain(h): return html.unescape(re.sub(r'<[^>]+>', '', h))
def remap(unit, part):
    if part.startswith('n') and (unit, int(part[1:])) in nmap:
        u, i = nmap[(unit, int(part[1:]))]; return u, 'n%d' % i
    return unit, part
rowunit = {}  # (text id, old unit, page, passage, source) -> new unit, for attributions
for f in sorted(glob.glob(R + '/passes/*.json')):
    P = json.load(open(f)); ch = 0; name = f.split('/')[-1]
    for r in P.get('rows', []):
        if not r.get('at'): continue
        new = [remap(r['unit'], a[0]) for a in r['at']]
        units = {u for u, _ in new}
        if len(units) > 1: print('SPLIT row', name, r['id'], r['unit'], r['at']); continue
        nu = units.pop()
        if nu != r['unit'] or any(p != a[0] for (u, p), a in zip(new, r['at'])):
            rowunit[(P['text'], r['unit'], r['page'], r['passage'], r['source'])] = nu
            r['unit'] = nu; r['at'] = [[p, a[1], a[2]] for (u, p), a in zip(new, r['at'])]; ch += 1
    for d in P.get('items', []):
        o = OLD.get(d['unit']); 
        if not o: continue
        for i, n in enumerate(o['notes']):
            if (d['unit'], i) in nmap and nmap[(d['unit'], i)][0] != d['unit'] and d['passage'][:60] in plain(n['html']):
                print('DIV moves', name, d['unit'], '->', nmap[(d['unit'], i)][0]); d['unit'] = nmap[(d['unit'], i)][0]; ch += 1
    if write and ch:
        pretty = open(f).read().startswith('{\n')
        with open(f, 'w', encoding='utf-8') as fh:
            json.dump(P, fh, ensure_ascii=False, indent=1) if pretty else json.dump(P, fh, ensure_ascii=False, separators=(',', ':')); fh.write('\n')
    print(name, ch, 'changed')
# working-edition rows that moved with their notes
for r in D['rows']:
    if r['id'] in dest: print('working row', r['id'], 'now in', r['sec'])
# attributions
A = json.load(open(R + '/passes/attributions.json')); ch = 0; drop = []
wrows = {r['id']: r for r in D['rows']}
for a in A['attributions']:
    key = (a['text'], a['unit'], a['page'], a['passage'], a['source'])
    nu = rowunit.get(key)
    if nu is None:  # a working-edition row that moved with its note?
        for r in D['rows']:
            if r['id'] in dest and r['vp'] == a['passage'] and r['sp'] == a['source'] and r['page'] == a['page']: nu = dest[r['id']]
    cu, cp = remap(a['unit'], a['cuePart'])
    nu = nu or a['unit']
    if cu != nu:
        # the cue now stands in another unit than the row: look for it in the row's unit
        u = NEW[nu]; parts = [('t', plain(u['html']))] + [('n%d' % i, plain(n['html'])) for i, n in enumerate(u['notes'])]
        hit = next((p for p, t in parts if a['cue'] in t), None)
        if hit: print('cue found again', a['unit'], '->', nu, hit); cu, cp = nu, hit
        else: print('CUE LEFT', a['unit'], a['text'], repr(a['cue'][:50]), 'row unit', nu, 'cue unit', cu); drop.append(a); continue
    if (nu, cp) != (a['unit'], a['cuePart']): a['unit'], a['cuePart'] = nu, cp; ch += 1
print('attributions changed', ch, 'to drop', len(drop))
if write:
    A['attributions'] = [a for a in A['attributions'] if a not in drop]
    with open(R + '/passes/attributions.json', 'w', encoding='utf-8') as f: json.dump(A, f, ensure_ascii=False, indent=1); f.write('\n')
