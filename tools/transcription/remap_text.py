# remap_text.py <edition> <old text.json> [--write]: after a correction to an edition's text, move every offset that points
# into it to the corrected text. Reuse rows in passes/*.json ('at', and 'passage' re-read from the new text), attributions
# (passage, and cue in cuePart), and layers with sentence ranges ('fr' of the English layers) or anchored items ('at').
# Offsets are moved through a character diff of each part; a translation flag whose French phrase no longer occurs is reported.
# --base <layer>=<json {unit: text}>: the text a layer's offsets were computed on, if not the old text.json (main text only).
import sys, os, json, glob, difflib, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
ED, OLD = sys.argv[1], sys.argv[2]; WRITE = '--write' in sys.argv
BASE = dict(a.split('=', 1) for a in sys.argv[sys.argv.index('--base') + 1:sys.argv.index('--base') + 2]) if '--base' in sys.argv else {}
BASE = {k: json.load(open(v)) for k, v in BASE.items()}
# --layers a,b: only these layer files (others are rebuilt by the converter); default all
ONLY = set(sys.argv[sys.argv.index('--layers') + 1].split(',')) if '--layers' in sys.argv else None
R = ROOT; E = '%s/editions/%s' % (R, ED)
old = {u['id']: u for u in json.load(open(OLD))['units']}
new = {u['id']: u for u in json.load(open(E + '/text.json'))['units']}
assert set(old) == set(new)

def txt(U, u, p): return U[u]['text'] if p == 't' else U[u]['notes'][int(p[1:])]['text']
MAPS = {}
def mapper(u, p, base=None):
    k = (u, p, id(base))
    if k not in MAPS:
        a, b = (base[u] if base is not None else txt(old, u, p)), txt(new, u, p)
        ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if a != b else [('equal', 0, len(a), 0, len(a))]
        def f(x, end=False):
            # a start offset goes after text inserted at it, an end offset before
            for tag, i1, i2, j1, j2 in ops:
                if tag == 'equal' and ((i1 < x <= i2) if end else (i1 <= x < i2)): return j1 + x - i1
            for tag, i1, i2, j1, j2 in ops:
                if tag == 'equal' and i1 <= x <= i2: return j1 + x - i1
                if i1 <= x <= i2 and tag != 'equal': return j2 if end else j1
            raise ValueError((u, p, x))
        MAPS[k] = (a != b, f)
    return MAPS[k]

def move_passage(u, ps):
    """A passage stored without offsets (divergence items): found once in the old unit text or a note, it is read again from
    the corrected text; otherwise it stays."""
    if u not in old or not ps: return ps
    parts = ['t'] + ['n%d' % i for i in range(len(old[u].get('notes', [])))]
    hits = [(p, txt(old, u, p).find(ps)) for p in parts if txt(old, u, p).count(ps) == 1]
    if len(hits) != 1: return ps
    p, i = hits[0]; ch, m = mapper(u, p)
    return txt(new, u, p)[m(i):m(i + len(ps), True)] if ch else ps

changed = 0; pmap = {}
for f in sorted(glob.glob(E + '/passes/*.json')):
    if f.endswith('attributions.json'): continue
    P = json.load(open(f)); n = 0
    for r in P.get('rows', []):
        at2 = []
        for p, a, b in r['at']:
            ch, m = mapper(r['unit'], p)
            at2.append([p, m(a), m(b, True)])
        if at2 != r['at'] or (len(at2) == 1 and txt(new, r['unit'], at2[0][0])[at2[0][1]:at2[0][2]] != r['passage']):
            p, a, b = at2[0]; np_ = txt(new, r['unit'], p)[a:b]
            pmap[(r['unit'], r['passage'])] = np_
            if np_ != r['passage']: print('passage', r['id'], repr(r['passage'][:60]), '->', repr(np_[:60]))
            r['at'] = at2; r['passage'] = np_; n += 1
    for it in P.get('items', []):
        if 'at' not in it and it.get('passage'):
            p2 = move_passage(it['unit'], it['passage'])
            if p2 != it['passage']: it['passage'] = p2; n += 1
    if n:
        changed += n; print(os.path.basename(f), n, 'rows moved')
        if WRITE: json.dump(P, open(f, 'w'), ensure_ascii=False, indent=1)
A = E + '/passes/attributions.json'
if os.path.exists(A):
    P = json.load(open(A)); n = 0
    for a in P['attributions']:
        k = (a['unit'], a['passage'])
        if k in pmap and pmap[k] != a['passage']: a['passage'] = pmap[k]; n += 1
        if a.get('cue') and a.get('cuePart') and (a['cuePart'] == 't' or a['cuePart'][1:].isdigit()):
            ch, m = mapper(a['unit'], a['cuePart'])
            if ch:
                s = txt(old, a['unit'], a['cuePart']); i = s.find(a['cue'])
                if i >= 0:
                    c2 = txt(new, a['unit'], a['cuePart'])[m(i):m(i + len(a['cue']), True)]
                    if c2 != a['cue']: print('cue', a['unit'], repr(a['cue']), '->', repr(c2)); a['cue'] = c2; n += 1
    if n:
        print('attributions', n)
        if WRITE: json.dump(P, open(A, 'w'), ensure_ascii=False, indent=1)
for f in sorted(glob.glob(E + '/layers/*.json')):
    if ONLY is not None and os.path.basename(f)[:-5] not in ONLY: continue
    L = json.load(open(f)); n = 0; base = BASE.get(os.path.basename(f)[:-5])
    for u, rec in (L.get('units') or {}).items():
        parts = [('t', rec)] + [('n%d' % i, x) for i, x in enumerate(rec.get('notes', [])) if isinstance(x, dict)]
        for p, x in parts:
            if 'fr' in x and isinstance(x['fr'], list):
                if base is not None and p != 't': continue
                ch, m = mapper(u, p, base if p == 't' else None)
                if ch:
                    x2 = [[m(a), m(b, True)] for a, b in x['fr']]
                    if x2 != x['fr']: x['fr'] = x2; n += 1
            for fl in x.get('flags', []):
                if fl.get('fr') and re.sub(r'\s+', ' ', fl['fr']) != fl['fr']: fl['fr'] = re.sub(r'\s+', ' ', fl['fr']); n += 1
                if fl.get('fr') and fl['fr'] not in ' '.join(txt(new, u, q) for q in ['t'] + ['n%d' % i for i in range(len(new[u].get('notes', [])))]):
                    print('flag phrase not in new text', u, repr(fl['fr']))
    for it in L.get('items', []):
        if 'at' in it:
            at2 = [[p, mapper(it['unit'], p)[1](a), mapper(it['unit'], p)[1](b, True)] for p, a, b in it['at']]
            if at2 != it['at']: it['at'] = at2; n += 1
        elif it.get('passage'):
            p2 = move_passage(it['unit'], it['passage'])
            if p2 != it['passage']: it['passage'] = p2; n += 1
    if n:
        print(os.path.basename(f), n, 'ranges moved')
        if WRITE:
            with open(f, 'w') as o: json.dump(L, o, ensure_ascii=False, separators=(',', ':')); o.write('\n')
print('rows', changed, '(written)' if WRITE else '(dry run)')
