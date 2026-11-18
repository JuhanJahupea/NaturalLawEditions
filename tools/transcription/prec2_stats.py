# prec2_stats.py <dir>: verdicts of the second precision sample and the estimate for all match rows
# (audited match rows are right; unaudited estimated from the sample). Wilson 95% intervals.
import sys, json, glob, math, collections
d = sys.argv[1]; S = json.load(open(d + '/sample.json')); pop = S['population']; smp = {s['key']: s for s in S['sample']}
V = {}
for f in glob.glob(d + '/out/*.json'):
    for it in json.load(open(f))['items']: V[it['key']] = it
def wilson(k, n, z=1.96):
    if not n: return (0, 0)
    p = k / n; c = (p + z * z / (2 * n)) / (1 + z * z / n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (c - h, c + h)
out = {}
for ed in pop:
    rows = [s for s in S['sample'] if s['edition'] == ed]; n = len(rows)
    c = collections.Counter(V[s['key']]['verdict'] for s in rows); lab = sum(1 for s in rows if not V[s['key']].get('label_ok', True))
    A, U = pop[ed]['audited'], pop[ed]['unaudited']; p = c['right'] / n; lo, hi = wilson(c['right'], n)
    est = (A + U * p) / (A + U); elo = (A + U * lo) / (A + U); ehi = (A + U * hi) / (A + U)
    wlo, whi = wilson(c['wrong'], n)
    out[ed] = {'n': n, 'right': c['right'], 'weak': c['weak'], 'wrong': c['wrong'], 'label_not_ok': lab, 'match_rows': A + U, 'audited': A,
               'unaudited': U, 'right_unaudited': [round(p, 3), round(lo, 3), round(hi, 3)], 'right_all_match': [round(est, 3), round(elo, 3), round(ehi, 3)],
               'wrong_unaudited': [round(c['wrong'] / n, 3), round(wlo, 3), round(whi, 3)],
               'by_table': {t: dict(collections.Counter(V[s['key']]['verdict'] for s in rows if s['table'] == t)) for t in sorted({s['table'] for s in rows})}}
print(json.dumps(out, indent=1))
json.dump(out, open(d + '/stats.json', 'w'), indent=1)
