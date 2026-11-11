# prep_shared.py <cand> <shared> <judged dir or -> <out new cand> <out recheck cand>
# New cand: old candidates plus pages with strong shared runs (max 3 new per unit), for units not yet judged.
# Recheck: for judged units, the pages with shared runs that no judge match covers.
import sys, json, glob, os, collections
cf, sf, jd, o1, o2 = sys.argv[1:6]
cand = json.load(open(cf))['cand']; SH = json.load(open(sf))
judged, matched = set(), collections.defaultdict(set)
if jd != '-':
    for f in glob.glob(jd + '/out/*.json'):
        i = json.load(open(f.replace('/out/', '/in/'))); o = json.load(open(f))
        judged |= {it['unit'] for it in i['items']}
        for m in o.get('matches', []): matched[m['unit']].add(m['page_id'])
def strong(rs): return max(r['n'] for r in rs) >= 7 or sum(r['n'] for r in rs) >= 11
new, rec = {}, {}
for u in set(cand) | set(SH):
    byp = collections.defaultdict(list)
    for r in SH.get(u, []): byp[r['page']].append(r)
    if u in judged:
        pg = [p for p in byp if p not in matched[u] and (p in cand.get(u, []) or strong(byp[p]))]
        if pg: rec[u] = sorted(pg, key=lambda p: -sum(r['n'] for r in byp[p]))[:4]
    else:
        add = sorted([p for p in byp if p not in cand.get(u, []) and strong(byp[p])], key=lambda p: -sum(r['n'] for r in byp[p]))[:3]
        c = list(cand.get(u, [])) + add
        if c: new[u] = c
json.dump({'cand': new}, open(o1, 'w')); json.dump({'cand': rec}, open(o2, 'w'))
print('new cand units', len(new), 'added pages', sum(len(v) for v in new.values()) - sum(len(cand.get(u, [])) for u in new),
      '| recheck units', len(rec), 'pages', sum(map(len, rec.values())))
