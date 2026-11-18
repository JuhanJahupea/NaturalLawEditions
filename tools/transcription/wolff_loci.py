# wolff_loci.py <work> [out]: place each Wolff row's source passage in the transcription (JG, INST) and compare the § there
# with the row's locus. Search the cited page and its neighbours first, then the whole text.
import sys, os, re, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import ROOT
from merge_find import find
R = ROOT; S = sys.argv[1]
def norm(s): return s.replace('ſ', 's').replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'Ae')
res = collections.Counter(); diffs = []
for ed in ('vattel-1773', 'burlamaqui-1747'):
  for k, t in (('JG', 'wolff-jus-gentium-1749'), ('INST', 'wolff-institutiones-1750')):
    p = '%s/reuse/%s__%s.json' % (R, ed, t)
    if not os.path.exists(p): continue
    D = json.load(open('%s/srcp/%s.json' % (S, k))); pages = D['pages']; ix = {pg['id']: i for i, pg in enumerate(pages)}
    for r in json.load(open(p))['rows']:
        if r['status'] == 'rejected': continue
        sp = norm(r['source']); i0 = ix.get(r['page'])
        order = ([i0 + d for d in (0, 1, -1, 2, -2)] if i0 is not None else []) 
        hit = None
        for i in [j for j in order if 0 <= j < len(pages)] + list(range(len(pages))):
            pg = pages[i]; f = find(pg['text'], sp)
            if f:
                par = pg['carried']
                for off, n in pg['starts']:
                    if off <= f[0] + 3: par = n
                hit = (pg['id'], par, f[2]); break
        if not hit: res[(ed, k, 'not found')] += 1; continue
        m = re.match(r'§\s*(\d+)', r.get('locus') or '')
        old = int(m.group(1)) if m else None
        if old == hit[1]: res[(ed, k, 'same §')] += 1
        else:
            res[(ed, k, 'other §')] += 1
            diffs.append({'edition': ed, 'table': t, 'id': r['id'], 'unit': r['unit'], 'status': r['status'], 'locus': r.get('locus'), 'page': r['page'],
                          'found_page': hit[0], 'found_para': hit[1], 'ratio': hit[2], 'source': r['source'][:120]})
for k, v in sorted(res.items()): print(k, v)
json.dump(diffs, open(sys.argv[2] if len(sys.argv) > 2 else S + '/wolff_loci.json', 'w'), ensure_ascii=False, indent=1)
