# wolff_loci2.py <work>: second locus check: the rows wolff_loci.py could not place, with the old text layer's spelling folded (et/&, ae/æ, oe/œ, j/i, v/u)
import json, re, sys, collections
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge_find import find
from paths import ROOT
R = ROOT; S = sys.argv[1]
fold = lambda s: re.sub(r'\s+', ' ', s.replace('ſ', 's').replace('&', 'et').replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'Ae').replace('j', 'i').replace('v', 'u').replace('J', 'I').replace('V', 'U'))
out = []; res = collections.Counter()
for k, t in (('JG', 'wolff-jus-gentium-1749'), ('INST', 'wolff-institutiones-1750')):
    D = json.load(open('%s/srcp/%s.json' % (S, k))); P = D['pages']; ix = {p['id']: i for i, p in enumerate(P)}
    F = [fold(p['text']) for p in P]
    for r in json.load(open('%s/reuse/vattel-1773__%s.json' % (R, t)))['rows']:
        if r['status'] == 'rejected': continue
        m = re.match(r'§\s*(\d+)$', (r.get('locus') or '').strip())
        if not m: continue
        o = int(m.group(1)); i0 = ix.get(r['page'])
        if i0 is None: continue
        sp = fold(r['source']); hit = None
        for i in [i0 + d for d in (0, 1, -1)]:
            if not 0 <= i < len(P): continue
            f = find(F[i], sp)
            if f and f[2] >= 0.9:
                # offsets in the folded text: map by searching § starts in the folded text
                par = P[i]['carried']
                for off, n in P[i]['starts']:
                    if len(fold(P[i]['text'][:off])) <= f[0] + 3: par = n
                hit = (P[i]['id'], par, f[2]); break
        if not hit: res[(k, 'not found')] += 1; continue
        if hit[1] == o: res[(k, 'same')] += 1; continue
        res[(k, 'other')] += 1
        out.append({'table': t, 'id': r['id'], 'unit': r['unit'], 'locus': r['locus'], 'page': r['page'], 'found_page': hit[0], 'found_para': hit[1], 'ratio': round(hit[2], 3), 'source': r['source'][:90]})
print(dict(res)); json.dump(out, open(S + '/loci2.json', 'w'), ensure_ascii=False, indent=1)
for x in out[:40]: print(x['id'], x['locus'], '->', x['found_para'], x['page'], x['found_page'], x['ratio'])
